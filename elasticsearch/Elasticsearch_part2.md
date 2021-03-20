# 데이터 처리

## 새로운 데이터 색인

- curl 명령의 기본 형식

  ```bash
  curl -X 메소드 'http://연결할 일레스틱 서치 노드의 호스트명:연결할 포트/색인명/_doc/문서id'
  ```

  - `-X` 
    - request시 사용할 메소드의 종류를 기술한다. 메소드와 띄어 써도 되지만 붙여 써도 된다.
    - 새로운 문서 입력은 PUT, 기존 문서의 수정은 POST, 삭제는 DELETE, 조회는 GET을 사용한다.
    - `-XGET`의 경우 생략이 가능하다.

  - _doc
    - ES5 버전 이하에서는 멀티 타입을 지원해서 하나의 인덱스 안에 다양한 타입의 데이터를 저장할 수 있었다.
    - ES6  버전부터는 하나의 인덱스에 하나의 타입만 저장할 수 있게 되었기에 본래 타입이 올 자리에 _doc을 입력한다.



- 삽입

  - curl을 활용하여 삽입
    - 파라미터로 들어간 `pretty` 또는 `pretty-true`는 JSON  응답을 더 보기 좋게 해준다.
    - `-H` 옵션은 header를 지정한다.
    - `-d` 옵션은 body를 지정한다.

  ```bash
  $ curl -XPUT 'localhost:9200/company/_doc/1?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Theo",
  "age":"28"
  }'
  ```

  - 응답
    - 응답은 색인, 타입, 색인한 문서의 ID를 포함한다.

  ```json
  {
    "_index" : "company",
    "_type" : "colleague",
    "_id" : "1",
    "_version" : 1,
    "result" : "created",  // 새로 생성한 것이므로 created로 뜨지만, 수정할 경우 updated라고 뜬다.
    "_shards" : {
      "total" : 2,
      "successful" : 1,
      "failed" : 0
    },
    "_seq_no" : 0,
    "_primary_term" : 1
  }
  ```

  - POST 메서드로도 추가가 가능하다.
    - 둘의 차이는 POST의 경우 도큐먼트id를 입력하지 않아도 자동으로 생성하지만 PUT은 자동으로 생성하지 않는다는 것이다.

  - 실수로 기존 도큐먼트가 덮어씌워지는 것을 방지하기 위해 입력 명령어에 `_doc` 대신 `_create`를 사용해서 새로운 도큐먼트의 입력만 허용하는 것이 가능하다.
    - 이 경우 이미 있는 도큐먼트id를 추가하려 할 경우 오류가 발생한다.
    - 이미 위에서 도큐먼트id가 1인 도큐먼트를 추가했으므로 아래 예시는 오류가 발생한다. 

  ```json
  PUT company/_create/1
  
  {
      "nickname":"Theo",
      "message":"안녕하세요!"
  }
  ```




- 색인 과정
  - 추후 추가



- 색인 생성과 매핑 이해하기(ES6부터는 하나의 인덱스에 하나의 타입만 저장할 수 있도록 변경)

  - curl 명령은 색인과 매핑타입을 자동으로 생성한다.
    - 위 예시에서 company라는 색인과 colleague라는 매핑 타입을 생성한 적이 없음에도 자동으로 생성되었다.
    - 수동으로 생성하는 것도 가능하다.
  - 색인을 수동으로 생성하기

  ```bash
  $ curl -XPUT 'localhost:9200/new-index'
  ```

  - 수동 생성의 응답

  ```json
  {
    "acknowledged" : true,
    "shards_acknowledged" : true,
    "index" : "test-index"
  }
  ```

  - 스키마 확인
    - 스키마를 보기 위해 url에 `_mapping`을 추가한다.
    - ES 6.x 이상의 경우 _doc타입이 아닌 타입을 따로 지정했을 경우 아래와 같이 `include_type_name=true` 또는 `include_type_name`을 파라미터로 넣어야 한다.

  ```bash
  $ curl 'localhost:9200/company/_mapping/colleague?include_type_name&pretty'
  ```

  - 응답
    - 색인 명, 타입, 프로퍼티 목록, 프로퍼티 옵션 등의 데이터가 응답으로 넘어 온다.

  ```json
  {
    "company" : {
      "mappings" : {
        "colleague" : {
          "properties" : {
            "age" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        }
      }
    }
  }
  ```



## 데이터 검색

- 검색하기

  - 검색을 위해 데이터를 더 추가

  ```bash
  $ curl -XPUT 'localhost:9200/company/colleague/2?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Kim",
  "age":"26"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/3?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Lee",
  "age":"27"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/4?pretty' -H 'Content-Type: application/json' -d '{
  "name":"An",
  "age":"27"
  }'
  ```

  - 데이터 검색하기
    - `q`파라미터는 검색할 내용이 들어간다.
    - 특정 필드에서만 찾고자 할 때는 `q=name:Kim`과 같이 작성하면 된다.
    - 아래와 같이 필드를 지정해주지 않을 경우 `_all`이라는 모든 필드의 내용을 색인하는 필드가 자동으로 들어가게 된다.
    - `_source` 파라미터는 특정 필드만 반환되도록 한다(유사한 파라미터로 `stored_fileds`가 있다).
    - `size` 파라미터는 일치하는 데이터들 중 반환할 데이터의 수를 지정한다(기본값은 10이다).

  ```json
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 어디를 검색할지 설정하기

  - 다수의 타입에서 검색하기
    - url에서 타입을 콤마로 구분하여 검색하면 된다.
    - ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/colleague, department/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 모든 타입에서 검색하기
    - 타입을 지정하지 않고 검색하면 된다.
    - 역시 ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 다수의 색인을 검색하기
    - url에서 인덱스를 콤마로 구분하여 검색하면 된다.
    - 만일 검색하려는 색인이 없는 경우 에러가 발생하는데 에러를 무시하려면 `ignore_unavailable` 플래그를 주면 된다.

  ```bash
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty"
  
  # 없는 인덱스도 포함해서 검색하기
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty&ignore_unavailable"
  ```

  - 모든 색인을 검색하기
    - url의 색인이 올 자리에 `_all`을 입력하거나 아예 색인을 빼면 모든 색인에서 검색한다.

  ```bash
  $ curl "localhost:9200/_all/_search?q=Kim&_source=name&size=1&pretty"
  
  $ curl "localhost:9200/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 응답 내용

  - 요청

  ```bash
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 응답

  ```json
  {
    // 요청이 얼마나 걸렸으며, 타임아웃이 발생했는가
    "took" : 1,
    "timed_out" : false,
    // 몇 개의 샤드에 질의 했는가
    "_shards" : {
    "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      // 일치하는 모든 문서에 대한 통계
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      // 결과 배열
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim"
          }
        }
      ]
    }
  }
  ```

  - 시간
    - `took` 필드는 ES가 요청을 처리하는 데 얼마나 걸렸는지 말해준다(단위는 밀리 초).
    - `timed_out` 필드는 검색이 타임아웃 되었는지 보여준다.
    - 기본적으로 검색은 절대로 타임아웃이 되지 않지만, 요청을 보낼 때`timeout` 파라미터를 함께 보내면 한계를 명시할 수 있다.
    - `$ curl "localhost:9200/_search?q=Kim&timeout=3s"`와 같이 작성할 경우 3초가 지나면 타임아웃이 발생하고 `timed_out`필드의 값은 true가 된다.
    - 타임아웃이 발생할 경우 타임아웃될 때까지의 결과만 반환된다.
  - 샤드
    - 총 몇 개의 샤드에 질의 했고 성공한 것과 스킵한 것, 실패한 것에 대한 정보를 반환한다.
    - 만일 특정 노드가 이용 불가 상태라 해당 노드의 샤드를 검색하지 못했다면 질의에 실패한 것이 된다.
  - 히트 통계
    - `total`은 전체 문서 중 일치하는 문서 수를 나타낸다.
    - `total`은 `size`를 몇으로 줬는지와 무관하게 일치하는 모든 문서의 수를 표시해주므로 total과 실제 반환 받은 문서의 수가 다를 수 있다.
    - `max_score`는 일치하는 문서들 중 최고 점수를 볼 수 있다.
  - 결과 문서
    - 히트 배열에 담겨 있다.
    - 일치하는 각 문서의 색인, 타입, ID, 점수 등의 정보를 보여준다.



- 쿼리로 검색하기

  - 지금까지는 URI 요청으로 검색했다.
    - 간단한 검색에는 좋지만 복잡한 검색에는 적절치 못한 방법이다.
  - `query_string` 쿼리 타입으로 검색하기
    - 쿼리스트링 타입의 쿼리를 실행하는 명령문이다.
    - `default_field`는 검색을 실행할 필드를 특정하기 위해 사용한다.
    - `default_operator`는 검색할 단어들이 모두 일치하는 문서를 찾을 지, 하나라도 일치하는 문서를 찾을지를 설정한다(기본값은 OR로 하나라도 일치하는 문서는 모두 찾는다).
    - 위 두 옵션(`default_field`, `default_operator`)을 다음과 같이 쿼리 스트링 자체에 설정하는 것도 가능하다.
    - `"query":"name:Kim AND name:Lee"`

  ```bash
  $ curl 'localhost:9200/company/colleague/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
      "query_string":{
        "query":"Kim",
        "default_field":"name",
        "default_operator":"AND"
      }
    }
  }'
  ```

  - 응답

  ```json
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
      "max_score" : 0.6931471,
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim",
            "age" : "26"
          }
        }
      ]
    }
  }
  ```



- 필터 사용(ES 6.X 부터 사용 불가)

  - 필터는 결과에 점수를 반환하지 않는다.
    - 쿼리는 결과와 함께 각 결과의 점수를 반환한다.
    - 필터는 오직 키워드가 일치하는지만 판단하여 일치하는 값들을 반환한다.
  - 필터 검색

  ```bash
  $ curl 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
    	"filtered":{
    	  "filter":{
      	"term" :{
            "name":"Kim"
          }
    	  }
    	}    
    }
  }'
  ```



- ID로 문서 가져오기

  - 검색은 준실시간인데 반해 문서 ID로 문서를 찾는 것은 실시간이다.
  - 특정 문서를 가져오려면 문서가 속한 색인과 타입, 그리고 ID를 알아야 한다.
    - 그러나 타입은 현재 사라졌기 때문에 type 자리에 `_doc`을 입력하여 검색한다.
    - 타입을 입력해도 검색은 되지만 경고문이 뜬다.

  ```json
  // _doc 사용
  $ curl 'localhost:9200/company/_doc/1?pretty'
  
  // 타입 사용
  $ curl 'localhost:9200/company/colleague/1?pretty'
  ```

  - 응답
    - 만일 찾는 문서가 존재하지 않으면 아래 `found`는 false가 된다.

  ```json
  {
    "_index" : "company",
    "_type" : "_doc",
    "_id" : "1",
    "_version" : 5,
    "_seq_no" : 5,
    "_primary_term" : 1,
    "found" : true,
    "_source" : {
      "name" : "Theo",
      "age" : "28"
    }
  }
  ```





## 데이터 수정, 삭제

- 삭제

  - 도큐먼트 또는 인덱스 단위의 삭제가 가능하다.
    - 도큐먼트를 삭제하면 `"result":"deleted"`가 반환된다.
    - 도큐먼트는 삭제되었지만 인덱스는 남아있는 경우, 삭제된 도큐먼트를 조회하려하면 `"found":false`가 반환된다.
    - 삭제된 인덱스의 도큐먼트를 조회하려고 할 경우(혹은 애초에 생성된 적 없는 도큐먼트를 조회할 경우) 에러가 반환된다.

  - 도큐먼트를 삭제하는 경우

  ```json
  DELETE office/_doc/1
  ```

  - 도큐먼트 삭제의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "deleted",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 삭제된 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 삭제된 도큐먼트를 조회했을 경우의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "found": false
  }
  ```

  - 인덱스를 삭제

  ```json
  DELETE office
  ```

  - 인덱스 삭제의 응답

  ```json
  {
      "acknowledged": true
  }
  ```

  - 삭제된 인덱스의 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 응답

  ```json
  {
      "error": {
          "root_cause": [
              {
                  "type": "index_not_found_exception",
                  "reason": "no such index [office]",
                  "resource.type": "index_expression",
                  "resource.id": "office",
                  "index_uuid": "_na_",
                  "index": "office"
              }
          ],
          "type": "index_not_found_exception",
          "reason": "no such index [office]",
          "resource.type": "index_expression",
          "resource.id": "office",
          "index_uuid": "_na_",
          "index": "office"
      },
      "status": 404
  }
  ```



- 수정

  - 위에서 삭제한 데이터를 다시 생성했다고 가정
  - 수정 요청

  ```json
  POST office/_doc/1
  
  {
      "nickname":"Oeht",
      "message":"!요세하녕안"
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "updated",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 수정할 때 특정 필드를 뺄 경우 해당 필드가 빠진 채로 수정된다.
    - POST 메서드로도 수정이 가능한데 POST 메서드를 사용해도 마찬가지다.

  ```json
  // 요청
  POST office/_doc/1
  
  {
      "nickname":"Theo"
  }
  
  // 응답
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "_seq_no": 9,
      "_primary_term": 1,
      "found": true,
      "_source": {
          // message 필드가 사라졌다.
          "nickname": "Theo"
      }
  }
  ```

  - `_update`
    - `_update`를 활용하면 일부 필드만 수정하는 것이 가능하다.
    - 업데이트 할 내용에 `"doc"`이라는 지정자를 사용한다.

  ```json
  // 도큐먼트id가 2인 새로운 도큐먼트를 생성했다고 가정
  POST office/_update/2
  
  {
      "doc":{
          "message":"반갑습니다.!"
      }
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "2",
      "_version": 2,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
          "nickname": "Oeht",
          "message": "반갑습니다!"
      }
  }
  ```



## 벌크 API

- `_bulk`

  - 복수의 요청을 한 번에 전송할 때 사용한다.
    - 동작을 따로따로 수행하는 것 보다 속도가 훨씬 빠르다.
    - 대량의 데이터를 입력할 때는 반드시 `_bulk` API를 사용해야 불필요한 오버헤드가 없다.
  - 형식
    - index, create, update, delete의 동작이 가능하다.
    - delete를 제외하고는 명령문과 데이터문을 한 줄씩 순서대로 입력한다.
    - delete는 내용 입력이 필요 없기 때문에 명령문만 있다.
    - `_bulk`의 명령문과 데이터문은 반드시 한 줄 안에 입력이 되어야 하며 줄바꿈을 허용하지 않는다.

  - 예시

  ```json
  POST _bulk
  {"index":{"_index":"learning", "_id":"1"}} // 생성
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}} // 생성
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}} // 삭제
  {"create":{"_index":"learning", "_id":"3"}} // 생성
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}} // 수정
  {"doc":{"field":"deep learning"}}
  ```

  - 응답

  ```json
  {
    "took" : 1152,
    "errors" : false,
    "items" : [
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 0,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 1,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "delete" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 2,
          "result" : "deleted",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 2,
          "_primary_term" : 1,
          "status" : 200
        }
      },
      {
        "create" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "3",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 3,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "update" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 2,
          "result" : "updated",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 4,
          "_primary_term" : 1,
          "status" : 200
        }
      }
    ]
  }
  ```

  - 인덱스명이 모두 동일할 경우에는 아래와 같이 하는 것도 가능하다.

  ```json
  POST learning/_bulk
  
  {"index":{"_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_id":"2"}}
  {"create":{"_id":"3"}}
  {"field":"docker"}
  {"update":{"_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```



- json 파일에 실행할 명령을 저장하고 curl 며영으로 실행시킬 수 있다.

  - bulk.json 파일

  ```json
  {"index":{"_index":"learning", "_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}}
  {"create":{"_index":"learning", "_id":"3"}}
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```

  - 명령어
    - 파일 이름 앞에는 @를 입력한다.

  ```bash
  $ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
  ```



# 엘라스틱서치 모니터링

## Head

- Head
  - 클러스터의 상태를 모니터링 할 수 있는 모니터링 도구 중 하나.
  - 가장 큰 장점 중 하나는 샤드 배치 정보를 확인할 수 있다는 점이다.



- 설치하기
  - 기존에는 플러그인 방식을 사용했지만 ES6 이상부터는 보안상의 이유로 플러그인 방식을 사용하지 않는다.
  - https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm 에서 확장 프로그램을 추가하여 사용이 가능하다.



- Overview
  - 클러스터를 구성하는 노드들의 이름과 인덱스 이름, 인덱스를 구성하는 샤드와 인덱스에 저장된 문서의 건수를 살펴볼 수 있다.
  - 노드의 Info 버튼
    - Cluster Node Info는 해당 노드의 호스트명과 아이피 등의 여러 가지 설정을 확인 가능하다. 
    - Node Stats는 노드의 기본 정보와 클러스터에서 수행된 동작들의 통계 정보를 확인할 수 있다. 간단한 수치이기 때문에 특별히 유의미한 정보는 아니다.
  - 노드의 Actions 버튼
    - Shutdown 메뉴는 동작하지 않는다.
    - 프로세스의 종료는 가급적이면 시스템에 접근하여 실행하는 것이 로그나 클러스터 상태를 살피기에 좋다.
  - 인덱스의 Info 버튼
    - Index Status는 해당 인덱스의 문서 개수나 삭제된 문서 개수, 사이즈, 해당 인덱스를 대상으로 수행한 동작들의 통계 정보를 보여준다. 이 값도 단순한 수치이기 때문에 특별히 유의미한 정보는 아니다.
    - Index Metadata는 인덱스의 open/close 여부와 함께 인덱스를 구성하는 정보인 settings, mappings, aliases 정보를 보여준다. 해당 정보는 인덱스가 어떻게 구성되어 있는지 한 눈에 확인할 때 유용하다.
  - 인덱스의 Actions 버튼
    - New Alias, Refresh, Flush 등의 드롭다운 메뉴가 존재한다.
    - 인덱스 alias, refresh, forcemerge, close, delete 등 인덱스에 수행할 수 있는 다양한 작업을 진행 가능하다.



- Indices
  - 클러스터 내에 생성한 인덱스의 이름과 크기, 문서의 개수를 요약하여 보여준다.
  - Overview 탭에서도 확인 가능하지만 인덱스가 많아져 전체 인덱스를 한 눈에 확인하기 어려울 때 사용한다.



- Browser
  - 생성한 인덱스와 타입, 문서의 필드에 해당하는 내용들을 확인 가능하다.
  - 검색 API를 사용하지 않고도 인덱스내에 어떤 문서들이 어떤 타입으로 생성되어 있는지 하나씩 확인 가능하다.



- Structured Query
  - 특정 인덱스를 선택하여 간단하게 쿼리를 해볼 수 있는 탭이다.
  - 드롭다운 메뉴에서 항목들을 선택하고 Search 버튼을 누르면 원하는 검색 결과를 확인할 수 있다.'



- Any Request
  - Head에 연결시킨 클러스터에 쿼리를 요청할 수 있다.
  - Structured Query가 구조화된 검색 쿼리만 요청할 수 있는 반면, 다양한 요청을 전달할 수 있다.
  - 기본으로는 POST 메서드로 _search API를 호출하도록 되어 있다.
  - 하단의 Request를 클릭하면 정의한 사항들을 클러스터에 요청한다.





## X-Pack

- X-Pack
  - 베이직 라이선스로 활용할 수 있으며, 베이직 라이선스는 무료로 사용할 수 있다.
  - 6.3 이전 버전은 1년에 한 번 베이직 라이선스를 재활성화하기 위해 클러스터의 노드를 전부 삭제해야 한다.
  - 6.3 이후 버전부터 라이선스를 규칙적으로 갱신하지 않아도 모니터링 기능을 사용할 수 있다.



- 설치하기

  - Kibana를 설치해야 한다.

    - Kibana는 ES에 저장된 로그를 검색하거나 그래프 등으로 시각화할 때 사용하는 도구다.
    - 사실상 ES의 웹 UI와 같은 역할을 하는 도구라고 생각하면 된다.

    - 공식 홈페이지에서 다운로드 가능하다.



- 프로메테우스
  - 위의 두 가지 외에도 프로메테우스를 사용해서도 모니터링이 가능하다.
  - 오픈 소스 기반의 모니터링 시스템
  - 데이터를 시간의 흐름대로 저장할 수 있는 시계열 데이터베이스의 일종.
  - 수집된 데이터를 바탕으로 임계치를 설정하고 경고 메세지를 받을 수 있는 오픈소스 모니터링 시스템이다.
  - ES 외에도 많은 시스템을 모니터링할 수 있게 해준다.
  - 컴포넌트 구성
    - 중앙에 TSDB(Time Series Data Base)의 역할을 하는 Prometheus Server가 존재한다.
    - 각종 지표들을 Exporter라는 컴포넌트를 통해서 가져올 수 있다.
    - Push Gateway를 통해서 입력할 수도 있다.
    - 각 항목에 대한 임계치를 설정하여 Alert Manager를 통해 경고 메시지를 받을 수도 있다.



# 엘라스틱서치 설정하기

- 클러스터 이름 명시하기
  - 엘라스틱서치의 주 설정 파일은 config 디렉터리의 `elasticsearch.yml`이다.
  - `elasticsearch.yml`의 `cluster.name`을 주석 해제 후 변경한다.
    - 이후 엘라스틱서치를 정지하고 재실행한다.
    - 만일 데이터를 색인 한 후 클러스터명을 변경했다면 엘라스틱서치를 재시작했을 때 기존에 색인한 데이터가 사라져 있을 수도 있다.
    - 클러스터명을 다시 되돌리면 색인한 데이터도 다시 돌아온다.



- 자세한 로깅 명시하기
  - 엘라스틱서치의 로그를 봐야 한다면 logs 디렉터리를 확인하면 된다.
    - 엘라스틱서치 로그 엔트리는 세 가지 파일 형태로 구성된다
    - 메인 로그(클러스터명.log 파일): 엘라스틱서치가 동작 중일 때 무슨 일이 일어났는지에 대한 일반적인 정보를 담고 있다.
    - 느린 검색 로그(클러스터명_index_search_slowlog.log 파일): 쿼리가 너무 느리게 실행될 때(쿼리가 0.5초 넘게 걸릴 경우) 엘라스틱서치가 로그를 남기는 곳이다.
    - 느린 색인 로그(클러스터명_index_indexing_slowlog.log 파일): 느린 검색 로그와 유사하지만 기본으로 색인 작업이 0.5초 이상 걸리면 로그를 남긴다.
  - 로깅 옵션을 변경하려면 elasticsearch.yml과 같은 위치에 있는 logginh.yml 파일을 수정하면 된다.



- JVM 설정 조정하기

  - 엘라스틱서치는 JAVA 애플리케이션이므로 JVM에서 실행한다.
  - 엘라스틱서치에 의해 사용하는 대부분 메모리는 힙이라고 부른다.
    - 기본 설정은 ES가 힙으로 초기에 256MB를 할당해서 1GB까지 확장한다.
    - 검색이나 색인 작업이 1GB 이상의 RAM이 필요하면, 작업이 실패하고 로그에서 OOM(Out of Memory) 에러를 보게 될 것이다.
    - 엘라스틱서치에 얼마만큼의 메모리를 사용할지 변경하기 위해 `ES_HEAP_SIZE` 환경변수를 사용할 수 있다.

  ```bash
  # heap을 늘린 후 elasticsearch를 실행한다.
  SET ES_HEAP_SIZE=500m & bin\elasticearch.bat
  ```



# 클러스터에 노드 추가하기

- 클러스터 상태 확인하기

  - 아래 명령어를 통해 현재 클러스터 정보를 확인할 수 있다.
    - cat API는 JSON을 반환하지 않는다.

  ```bash
  $ curl 'localhost:9200/_cat/shards?v'
  ```

  - 새로운 노드를 추가한 적이 없으므로 오직 하나의 노드만 존재한다.
    - 샤드는 primary 샤드와 replica 샤드가 존재하는데 노드는 한 개만 존재하므로 replica 샤드는 할당되지 못한 상태이다(UNASSIGNED).
    - 미할당 레플리카는 클러스터의 상태를 yellow로 만든다.
    - yellow는 primary 샤드들은 할당되었으나 모든 레플리카가 할당된 것은 아니라는 것을 의미한다.
    - primary 샤드가 할당되지 않았다면, 클러스터는 red 상태가 된다.
    - 모든 샤드가 할당되었다면 클러스터는 green이 된다.



- 두 번째 노드 생성하기
  - 방법
    - `elasticsearch.yml` 파일에 `node.max_local_storage_nodes: 생성할 노드 수` 코드를 추가한다(`:`와 생성할 노드 수 사이에 공백이 있어야 한다).
    - 엘라스틱서치가 실행 중인 상태에서 다른 터미널에서 엘라스틱서치를 실행한다.
    - 이렇게 하면 같은 머신에 다른 ES 인스턴스를 시작하게 된다.
    - 현업에서는 추가적인 프로세싱 파워의 이득을 얻기 위해 다른 머신에 새로운 노드를 시작한다.
    - 혹은 그냥 엘라스틱서치 폴더를 복사해서 각자 실행시키면 된다.
  - 두 번째 노드는 멀티캐스트로 첫 번째 노드를 찾아서 클러스터에 합류하게 된다.
    - 첫 번째 노드는 클러스터의 마스터 노드다.
    - 즉 어떤 노드가 클러스터에 있고 샤드가 어디에 있는지 같은 정보를 유지하는 역할을 하는데, 이 정보를 클러스터 상태라고 부르고 다른 노드에도 복제 된다.
    - 마스터 노드가 내려가면 다른 노드가 마스터 노드가 된다.
  - 이제 추가한 노드에 레플리카가 할당되어 클러스터가 green으로 변경된 것을 확인 가능하다.







