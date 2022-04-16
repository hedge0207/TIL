# 인덱스 생성하기

- mapping & setting 없이 아래와 같이 인덱스명 만으로 생성이 가능하다.

  ```bash
  $ curl -XPUT 'localhost:9200/<인덱스명>'
  ```



- 인덱스명 규칙
  - 소문자만 사용이 가능하다.
  -  `\`, `/`, `*`, `?`, `"`, `<`, `>`, `|`, ` ` (space character), `,`, `#`는 사용이 불가능하다.
  - `-`, `_`, `+`로 시작할 수 없다.
  - `.` 혹은 `..`으로 생성할 수 없다.
  - 255 bytes 이상으로 생성할 수 없다.
  - `.`으로 시작하는 인덱스는 deprecate 될 예정이다.
    - 오직 hidden index와 plugin에서 관리하는 내부 인덱스에만 허용된다.



## mappings

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



- `_source` 옵션

  - elasticsearch에서 색인과 저장은 다르다.
    - 색인은 들어온 데이터로 역색인 구조를 만드는 것이다.
    - 저장은 들어온 데이터를 그대로 저장하는 것이다.
    - elasticsearch는 indexing 요청이 들어올 때 모든 필드를 역색인구조로 색인한다.
    - 또한 original data를 `_source`라 불리는 필드에 저장한다.
  - elasticsearch는 index된 데이터에 검색을 실행하고, store된 데이터를 반환한다.
    - 즉, 실제 검색은 `_source` 필드에 행해지는 것이 아니라 역색인 테이블에 행해진다.
  - `_source` 필드는 overhead를 불러올 수 있지만 아래와 같은 이유로 저장이 필요하다.
    - response에 원본 데이터를 함께 반환하기 위해서(response의 `_source` 필드에 담아 보낸다)
    - reindexing, update, update_by_query 등을 사용하기 위해서(당연하게도 원본 데이터가 없다면 reindexing, update 등이 불가능하다).
    - highlight 기능을 사용하기 위해서.
  - `_source` 필드에 original data를 저장할지 저장하지 않을지 설정이 가능하다.
    - 아래와 같이 `_source.enabled`를 false로 주면 `_source` 필드를 저장하지 않는다.
    - 저장은 되지 않지만 색인은 진행되므로 검색은 가능하다.
    - 그러나 get이나 search를 했을 때 response에 `_source`필드, 즉 original data는 반환되지 않는다.

  ```json
  // PUT test
  {
    "mappings": {
      "_source": {
        "enabled": false
      }, 
      "properties": {
        "animal":{
          "type": "keyword"
        }
      }
    }
  }
  ```

  - 일부 데이터만 저장하거나, 일부 데이터를 저장하지 않는 것도 가능하다.
    - `_source.includes`, `_source.exclude`를 사용한다.

  ```json
  // PUT test
  {
    "mappings": {
      "_source": {
        "includes": [
          "*.count",
          "meta.*"
        ],
        "excludes": [
          "meta.description",
          "meta.other.*"
        ]
      }
    }
  }
  ```

  



- `copy_to`

  - 한 필드의 값을 다른 필드에 복사할 수 있는 기능이다.
    - 일반적으로 여러 필드를 한 필드를 통해 검색하기 위해 사용한다.
    - 여러 필드를 검색하는 것 보다 한 필드를 검색하는 것이 검색 성능이 더 뛰어나기 때문이다.

  - mapping 설정하기
    - 아래와 같이 하나의 필드만 설정해도 되고, array 안에 여러 개의 필드도 설정 가능하다.
    - object 형태의 필드에는 적용이 불가능하다.

  ```json
  // PUT test-inex
  {
    "mappings": {
      "properties": {
        "first_name": {
          "type": "text",
          "copy_to": "full_name" 
        },
        "last_name": {
          "type": "text",
          "copy_to": "full_name" 
        },
        "full_name": {
          "type": "text"
        }
      }
    }
  }
  ```

  - 데이터 색인하기

  ```json
  // PUT test-index/_doc/1
  {
    "first_name": "John",
    "last_name": "Smith"
  }
  ```

  - 검색
    - mapping상에는 존재하지만 검색 결과로 표출되지는 않는다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match": {
        "full_name": { 
          "query": "John Smith",
          "operator": "and"
        }
      }
    }
  }
  
  
  // output
  {
    "took" : 1,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.5753642,
      "hits" : [
        {
          "_index" : "test-index",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.5753642,
          "_source" : {
            "first_name" : "John",
            "last_name" : "Smith"
          }
        }
      ]
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









# 데이터 삭제

- delete api를 사용하여 삭제가 가능하다.

  - 기본형

  ```bash
  DELETE /<index>/_doc/<document_id>
  ```



- ES에서 문서가 삭제되는 과정
  - delete api를 통해 삭제 요청을 보낸다.
  - 삭제 요청이 들어온 문서에 삭제 했다는 표시를 하고 검색시에 검색하지 않는다.
  - 세그먼트 병합이 일어날 때 삭제 표시가 되어 있는 문서를 실제로 삭제한다.



- query parameter
  - `if_seq_no`: document가 이 파라미터에 설정해준 sequence number를 가지고 있을 때만 삭제가 수행된다.
  - `if_primary_term`: document가 이 파라미터에 설정해준 primary term을 가지고 있을 때만 삭제가 수행된다.
  - `refresh`
    - `true`로 설정할 경우 delete의 변경사항을 즉각 반영(검색이 가능하게)한다. 
    - `wait_for`로 설정할 경우 refresh를 기다리다 refresh가 발생하면 변경 사항이 반영(검색이 가능하게)된다.
    - `false`로 설정하면 



- `delete_by_query`를 통해 특정 쿼리와 일치하는 문서를 삭제하는 것도 가능하다.

  - 삭제할 문서들을 지정해줄 query를 작성한다.

  ```json
  POST /test-index/_delete_by_query
  {
      "query":{
          "match":{
              "name":"test"
          }
      }
  }
  ```

  

  

