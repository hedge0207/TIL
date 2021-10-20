# 인덱스 생성하기

## Mappings

- Mapping 기본형

  - `properties` 아래에 정의하고자 하는 필드들을 정의한다.

  ```bash
  $ curl -XPUT 'localhost:9200/인덱스명' -H 'Content-Type: application/json' -d '{
      "mappings":{
          "properties":{
              "필드명":{
                  "type":"필드 타입"
              }
          }
      }
  }'
  ```



- `date_detection` 옵션

  - 미리 정의하지 않은 string 타입의 필드가 입력될 때, 만일 값이 date 필드의 형식에 부합하면 string이 아닌 date 타입으로 매핑한다.
    - boolean 값을 받으며, 기본값은 true이다.
  - `properties`와 동일한 수준에 정의한다.

  ```bash
  $ curl -XPUT 'localhost:9200/인덱스명' -H 'Content-Type: application/json' -d '{
      "mappings":{
      	"date_detection":true
          "properties":{
              ...
          }
      }
  }'
  ```

  - 예시

  ```bash
  PUT date_detection
  {
    "mappings": {
      "date_detection": true
    }
  }
  
  PUT date_detection/_doc/1
  {
    "today":"2015/09/02"
  }
  ```

  - 결과

  ```bash
  GET date_detection/_mappings
  
  # 응답
  {
    "date_detection" : {
      "mappings" : {
        "properties" : {
          "today" : {
            "type" : "date",
            "format" : "yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis"
          }
        }
      }
    }
  }
  ```



- `numeric_detection`

  - 미리 정의하지 않은 string 타입의 필드가 입력될 때, 만일 값이 숫자 형식이라면 string이 아닌 적합한 숫자 타입으로 매핑된다.
    - 기본값은 false이다.
  - `date_detection`과 같이 `properties`와 동일한 수준에 정의한다.

  - 예시

  ```bash
  PUT numeric_detection
  {
    "mappings": {
      "numeric_detection": true
    }
  }
  
  
  PUT numeric_detection/_doc/1
  {
    "my_float":   "1.0", 
    "my_integer": "1" 
  }
  ```

  - 결과
    - 가장 적합한 숫자형 타입으로 매핑된다.

  ```bash
  GET numeric_detection/_mapping
  
  # 응답
  {
    "numeric_detection" : {
      "mappings" : {
        "numeric_detection" : true,
        "properties" : {
          "my_float" : {
            "type" : "float"
          },
          "my_integer" : {
            "type" : "long"
          }
        }
      }
    }
  }
  ```



- `dynamic` 옵션

  - mapping을 정의할 때 dynamic mapping을 허용할 것인지 여부를 정할 수 있는데, 설정할 수 있는 값은 아래와 같다.
    - `true`: dynamic mapping을 허용한다.
    - `runtime`: dynamic mapping을 허용한다.
    - `false`: dynamic mapping을 허용하지 않는다.
    - `strict`: dynamic mapping을 허용하지 않는다.
  - `properties`와 동일한 수준에 정의한다.

  - `true`와 `runtime`의 차이
    - 같은 데이터가 들어와도 어떤 타입으로 매핑을 생성할지가 달라진다.

  | JSON data type                              | true                                                 | runtime                                              |
  | ------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
  | null                                        | No filed added                                       | No filed added                                       |
  | true/false                                  | boolean                                              | boolean                                              |
  | double                                      | float                                                | double                                               |
  | integer                                     | long                                                 | long                                                 |
  | object                                      | object                                               | No filed added                                       |
  | array                                       | array 내부의 null이 아닌 첫 번째 값에 따라 달라진다. | array 내부의 null이 아닌 첫 번째 값에 따라 달라진다. |
  | date detection에 걸린 string                | date                                                 | date                                                 |
  | numeric detection에 걸린 string             | float 또는 long                                      | double 또는 long                                     |
  | date/numeric detection에 걸리지 않은 string | keyword를 sub field로 가지는 text 필드               | keyword                                              |

  - `false`
    - `false`는 정적으로 정의되지 않은 필드가 들어올 경우 이를 무시한다.

  ```bash
  # false로 줄 경우
  PUT test_false
  {
    "mappings": {
      "dynamic":"false",
      "properties": {
        "name":{
          "type":"keyword"
        }
      }
    }
  }
  
  PUT test_false/_doc/1
  {
    "name":"theo",
    "age": 28
  }
  
  GET test_false/_mapping
  # return
  # 위에서 입력한 age필드가 동적으로 매핑되지 않은 것을 확인 가능하다.
  {
    "test_false" : {
      "mappings" : {
        "dynamic" : "false",
        "properties" : {
          "name" : {
            "type" : "keyword"
          }
        }
      }
    }
  }
  
  ```

  - `strict`

  ```bash
  # strict로 줄 경우
  PUT test_strict
  {
    "mappings": {
      "dynamic":"strict",
      "properties": {
        "name":{
          "type":"keyword"
        }
      }
    }
  }
  
  # 아래와 같이 미리 정의하지 않은 age 필드를 입력하면 error가 발생한다.
  PUT test_strict/_doc/1
  {
    "name":"theo",
    "age": 28
  }
  
  # erroor
  {
    "error" : {
      "root_cause" : [
        {
          "type" : "strict_dynamic_mapping_exception",
          "reason" : "mapping set to strict, dynamic introduction of [age] within [_doc] is not allowed"
        }
      ],
      "type" : "strict_dynamic_mapping_exception",
      "reason" : "mapping set to strict, dynamic introduction of [age] within [_doc] is not allowed"
    },
    "status" : 400
  }
  ```



- mapping 작성시 field명에 `.`을 넣으면  object 타입으로 생성된다.

  - 필드명에 `.`을 넣고 생성

  ```bash
  PUT mapping_test
  {
    "mappings": {
      "properties": {
        "user.name":{
          "type":"keyword"
        }
      }
    }
  }
  ```

  - 결과

  ```bash
  GET mapping_test/_mapping
  
  {
    "mapping_test" : {
      "mappings" : {
        "properties" : {
          "user" : {
            "properties" : {
              "name" : {
                "type" : "keyword"
              }
            }
          }
        }
      }
    }
  }
  ```

  



## settings

- `auto_expand_replicas`
  - data node의 수에 따라 레플리카 샤드의 수를 자동으로 늘린다.
  - `-`를 사이에 두고 하한값과 상한값을 설정한다(e.g. 0-3). 
    - 상한값은  `all`로 설정이 가능하다(e.g. 0-all)
    - 만일 `all`로 설정할 경우 [shard allocation awareness](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#shard-allocation-awareness)와 [`cluster.routing.allocation.same_shard.host`](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#cluster-routing-allocation-same-shard-host)는 무시된다.
  - 기본값은 false로 설정되어 있다.
  - 이 설정을 활성화할 경우 샤드 할당 정책으로 Index-level shard allocation filtering만을 적용 가능하다.









