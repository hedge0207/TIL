# 데이터 검색

## Search API

- Elasticsearch에서 검색이 이루어지는 과정

  > https://steve-mushero.medium.com/elasticsearch-search-data-flow-2a5f799aac6a

  - Coordinator 역할을 수행하는 node에 검색 요청이 도착한다.
  - Coordinator는 적절한 shard로 해당 query를 routing시킨다.
    - Routing을 위해 Coordinator는 요청에 담겨서 온 index pattern 혹은 alias를 기반으로 검색 대상 index의 목록을 생성한다.
    - 그 후 target index들의 shard들의 목록을 생성하는데, 여기에 포함되는 shard들은 고유해야한다(primary일 수도 있고, replica일 수도 있다.).
    - 예를 들어 2개의 primary shard와 2개의 replica shard가 있다면 총 shard의 개수는 6개이지만, 고유한 shard의 개수는 2개 뿐이고, shard의 목록에는 고유한 shard들만 있어야한다.
    - Coordinator는 이 고유한 shard들의 목록을 바탕으로, query를 보내야 하는 shard와 해당 shard들이 포함된 node들을 확정한다.
  - Query Phase
    - Coordinator는 확정된 shard들에게 query를 전송한다.
    - Coordinator로부터 query를 받은 shard들은 query와 일치하는 document들을 찾고, scoring을 실행한다.
    - 이 때, 각 shard 당 하나의 thread만 실행되기에, primary shard의 개수가 많아질수록 검색 속도가 빨라질 수 있다.
    - Query를 받은 각 shard들은 query 대상이 되는 field와 Lucene의 data fields를 mapping하고, query에 포함된 검색어를 analyzing하고, Lucene에서 실행할 수 있는 형태로 query를 재구성한다.
    - 이렇게 재구성된 정보들을 바탕으로 segment 수준에서 실제 검색이 실행된다.
    - 그 결과로 query와 일치하는 document들의 ID들이 저장된 우선순위 큐가 생성된다.
    - 이 배열 내의 document들은 추후에 점수가 매겨지고, 점수에 따라 혹은 `sort`에  담긴 기준에 따라 정렬이 실행된다.
    - 만약 document의 특정 field를 대상으로 정렬해야 한다면, doc values를 사용한다.
    - 만약 query에 `aggs`도 포함되어 있다면, 이 역시 마찬가지로 doc values를 통해 실행된다.
    - 각 shard는 일치하는 document ID들 중 `size` 만큼의 ID들만 coordinator에게 반환한다.
  - Fetch Phase
    - Coordinator는 각 shard들로 부터 받은 일치하는 document들의 ID가 담긴 배열을 병합하고, client에 반환할 최종 document들의 id를 확정한다.
    - 집계도 마찬가지로 각 shard들이 반환한 집계 정보를 종합한다.
    - Coordinator는 `_source` field를 반환하기위해 shard들에게 각 document ID에 해당하는 document들의 `_source` 값을 요청한다.
    - Shard들로부터 `_source` 값까지 받아오면 coordinator는 이를 가지고 최종 결과를 생성하고 client에게 반환한다.



- Search API

  - 모든 search API 검색 요청은 _search REST end point를 사용하고 GET이나 POST 요청 중 하나가 된다.
    - end point는 path라고도 불리며 URL에서 호스트와 포트 이후의 주소를 말한다.
  - 간단한 형태의 URI Search 형태를 제공한다.
  
  ```http
  GET <index_name>/_search?q=<query>
  ```
  
  - RequestBody Search 형태도 제공한다.
  
  ```json
  // GET <index_name>/_search
  {
    "query":{
      "term":{
        "field1":"test"
      }
    }
  }
  ```
  
    - 인덱스명에 한 개 이상의 인덱스를 지정해서 다수의 인덱스에 동시에 쿼리를 날릴 수 있다.
    - 아래와 같이 인덱스명이 올 자리에 `_all`을 입력하면 모든 인덱스에 쿼리를 날린다.
  
  ```http
  GET _all/_search?q=<query>
  ```



- Query profile

  - query의 parameter로 `profile`을 `true`로 주면 query의 profiling이 가능하다.
    - Kibana의 profile 탭에서도 사용이 가능하다.
  
  
  ```json
  {
      "query":{
          "profile":true,
          "match_all":{}
      }
  }
  ```
  
  - response 중 description에 아래와 같이 Lucene explation text가 담겨 있다.
  
  ```json
  {
      // ...
      "description" : "-((+bar:hello +bar:world) | (+foo:hello +foo:world)) #*:*"
      // ...
  }
  ```
  
  - 기호
    - `<field>:<term>`: field에 term이 포함되어야 한다는 의미이다.
    - `+`: 뒤에 오는 값이 문서에 반드시 포함되어 있어야 한다는 의미이다.
    - `-`: 뒤에 오는 값이 문서에 반드시 포함되어 있지 않아야 한다는 의미이다.
    - `*`: 정규 표현식의 `*`와 유사한 용도로 사용된다.
    - `|`: or와 같은 뜻이다.
  
  - 즉 위 쿼리는 다음과 같이 볼 수 있다.
    - `(+bar:hello +bar:world)`: `bar` field에 "hello"와 "world"가 반드시 포함.
    - `(+foo:hello +foo:world))`: `foo` field에 "hello"와 "world"가 반드시 포함.
    - `|`: 둘 중 하나로 매칭 되는 것을
    - `*:*`: 전체 문서에서
    - `-`: 제외한 나머지를 검색한다.



- 검색 요청의 기본 구성 요소

  - 구성 요소는 반환할 도큐먼트 개수를 제어하고, 최적의 도큐먼트를 선택하기 하며, 원치 않는 도큐먼트는 결과에서 걸러내도록 한다.
  - q(query)
    - 검색 요청에 있어 가장 중요한 구성 요소.
    - 점수 기반으로 최적의 도큐먼트를 반환하거나 원치 않는 도큐먼트를 걸러내도록 설정한다.
    - 이 구성 요소는 쿼리와 DSL 필터를 사용해서 구성한다.
  - size
    - 반환할 도큐먼트 개수를 의미한다.
  - from
    - size와 함께 페이지 매김(pagination)에 사용한다.
  - _source
    - _source는 어떤 필드를 반환할 것인지를 지정할 때 사용한다.
    - 기본값은 완전한 _source 필드를 반환하는 것이다.
    - _source 설정으로 반환되는 필드를 걸러낼 수 있다.
    - _source에 필드를 포함시키지 않아도 해당 필드에서 검색은 이루어진다.
    - 색인된 도큐먼트가 크고 결과에서 전체 내용이 필요하지는 않을 때 사용한다.
    - 이 옵션을 사용하려면, 색인 매핑에서 _source 필드를 비활성화하지 않아야 한다.
    - `false`를 주면 아무 field도 반환하지 않는다.
  - sort
    - 기본 정렬은 도큐먼트 점수에 따른다.
    - 점수 계산이 필요 없거나 동일 점수의 다수 도큐먼트가 예상된다면, sort를 추가해서 원하는 대로 순서를 제어할 수 있다.
  - fields
    - 검색 결과로 반환할 filed들을 입력한다.
    - 응답 값으로 오는 `_source` filed와 별개로 `fields`라는 filed에 지정한 filed들이 응답에 담겨서 온다.
    - `_source`와 마찬가지로 꼭 검색 대상 filed가 포함될 필요는 없다.
    - `_source`와는 달리 date type을 포함한 특정 field들의 format을 지정하는 것도 가능하다.
  
  ```json
  PUT test_index/_doc/1
  {
      "foo":"foo",
      "bar":"bar",
      "user_name":"John Doe",
      "user_email":"hello@world.com"
  }
  
  GET test_index/_search
  {
      "query": {
          "match": {
              "foo": "foo"
          }
      },
      "fields": [		// filed만 줘도 되고, format등을 지정해줄 수도 있다.
          "bar",
          "user_*",
          {
              "field": "last_login",
              "format": "epoch_millis"
          }
      ]
  }
  
  // 응답
  "hits": [
      {
          "_index": "test_index",
          "_id": "1",
          "_score": 0.2876821,
          "_source": {
              "foo": "foo",
              "bar": "bar",
              "user_name": "John Doe",
              "user_email": "hello@world.com",
              "last_login": "2023-08-01"
          },
          "fields": {
              "user_name.keyword": [
                  "John Doe"
              ],
              "bar": [
                  "bar"
              ],
              "user_email": [
                  "hello@world.com"
              ],
              "user_email.keyword": [
                  "hello@world.com"
              ],
              "user_name": [
                  "John Doe"
              ],
              "last_login": [
                  "1690848000000"
              ]
          }
      }
  ]
  ```
  
  - explain
    - boolean 값을 준다.
    - true로 설정할 경우 점수가 계산된 방식을 함께 반환한다.
  - seq_no_primary_term
    - boolean 값을 준다.
    - true로 설정할 경우 seqeunce number와 primary term을 함께 반환한다.



- URI Search

  - URL 기반 검색 요청은 curl로 요청할 때 유용하다.
    - 그러나 모든 검색 기능이 URL 기반 검색을 사용할 수 있는 것은 아니다.
  - form과 size를 활용
    - from의 기본 값은 0, size의 기본 값은 10이다.
    - from으로 결과의 시작 위치를 지정하고, size로 각 결과 페이지의 크기를 지정한다.
    - from이 7이고, size가 3인 경우, ES는 8, 9, 10 번째 결과를 반환한다.
  - 이들 두 개의 파라미터가 전달되지 않았다면 ES는 첫 결과의 시작(0번째)을 기본 값으로 사용하고 응답 결과와 함께 10건의 결과를 전송한다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?from=7&size=3'
  ```

  - sort를 활용
    - 일치하는 모든 도큐먼트를 날짜 오름차순으로 정렬한 결과 중 최초 10개를 반환한다.

  ``` bash
  $ curl 'localhost:9200/인덱스명/_search?sort=date:asc'
  ```
    - _source를 활용
      - 검색 결과의 일부 필드만 요청하도록 설정
        - title과 date _source 필드에 포함되어 반환된다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?_source=title,date'
  ```

    - q를 활용
        - title 필드에 elasticsearch라는 단어를 포함하는 도큐먼트만 검색

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?q=title:elasticsearch'
  ```



- RequestBody Search

  - 본문 기반 검색 요청은 유연하면서 더 많은 옵션을 제공한다.
  - from과 size를 활용

  ```bash
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "match_all":{}
  },
  "from":10,
  "size":10
  }'
  ```

  - _source를 활용
    - _source를 활용하면 개별 도큐먼트에서 반환할 필드 목록을 지정할 수 있다.
    - _source를 지정하지 않는다면, 엘라스틱서치는 기본적으로 도큐먼트의 _source 전체를 반환하거나 저장된 _source가 없다면 일치하는 _id, _type, _index, _socre와 같은 도큐먼트에 관한 메타데이터만 반환한다.
    - 아래 명령어는 검색의 응답으로 name과 date 필드만 반환하라는 것이다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "match_all":{}
  },
  "_source":["name","date"]
  }'
  ```

  - _source를 활용하여 원하는 필드만 가져오기
    - 필드 목록을 각각 지정해서 반환하는 것 외에도 와일드카드를 사용할 수도 있다.
    - 예를 들어 name과 nation 필드 둘 다 반환하려면 "na*"와 같이 지정하면 된다.
    - exclude 옵션을 사용하여 반환하지 않을 필드도 지정할 수 있다.
    - 아래 명령은 location 필드(object 타입)를 모두 반환하지만 location의 하위 필드 중 geolocation은 빼고 반환하라는 것이다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "match_all":{}
  },
  "_source":{
    "include": ["location.*"],
    "exclude": ["location.geolocation"]
  }
  }'
  ```

  - sort를 통한 정렬
    - 정렬 순서를 지정하지 않으면, ES는 일치한 도큐먼트를 _score 값의 내림차순으로 정렬해서 가장 적합성이 높은(가장 높은 점수를 가진) 도큐먼트 순서로 반환한다.
    - sort 옵션은 keyword나 integer와 같이 not analyzed가 기본인 필드를 기준으로 해야 한다.
  - 아래 예시는 먼저 생성일을 기준으로 오름차순 정렬을 하고, 그 다음 name을 알파벳 역순으로 정렬한 후, 마지막으로 _socre 값으로 정렬을 하라는 명령어다.
  
  ```bash
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "match_all":{}
  },
  "sort":{
    {"created_on":"asc"},
    {"name":"desc"},
    "_score"
  }
  }'
  ```
  
  - highlight 옵션을 활용한 검색
    - 검색 결과 중 어떤 부분이 쿼리문과 일치하여 검색되었는지 궁금할 때 사용한다.
    - 검색 결과 중 어떤 필드에 highlighting 효과를 줄 거것인지 설정할 수 있다.
    - 이 결과는 _source 필드가 아닌 별도의 highlight라는 필드를 통해 제공된다.
    - 별도의 추가 옵션을 통해 다양한 표현식을 연출할 수 있다(공식 도움말 참고)
  
  ```bash
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "term":{"title":"Elasticsearch"}
  },
  "highlight": {
    "fileds":{"title":{}}
  }
  }'
  ```
  
  - boost를 통함 검색
    - 검색 결과로 나온 스코어를 변경할 때 사용한다.
    - 특정 검색 쿼리의 스코어를 높이거나 낮추고 싶을 때 boost 옵션을 활용하면 검색 결과로 나온 스코어를 대상으로 boost 옵션에 설정된 값을 곱한 값이 스코어로 지정된다(따라서 낮게 주고 싶을 경우 소수점을 활용하면 된다).
    - boost 옵션을 사용할 때는 match 쿼리와 term 쿼리 중 어떤 것을 사용하는가에 각기 다른 옵션을 줘야 한다.
  
  ```bash
  # match 쿼리
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "match":{
      "title":{
        "query":"Elasticsearch",
        "boost":4
      }
  },
  }'
  
  # term 쿼리
  $ curl 'localhost:9200/인덱스명/_search'-H 'Content-Type: application/json' -d '{
  "query":{
    "term":{
      "title":{
        "value":"Elasticsearch",
        "boost":4
      }
  },
  }'
  ```
  
  - scroll 옵션을 활용하여 검색
    - 검색 결과를 n개 단위로 나눠서 볼 때 사용한다.
    - from/size와 유사해 보이지만 검색 당시의 스냅샷을 제공해 준다는 점에서 다르다.
    - from/size를 통해 pagination을 하는 동안에 새로운 문서가 추가되면 기존 검색 결과에 영향을 줄 수 있지만, scroll 옵션을 사용하면 새로운 문서가 추가된다고 해도 scroll id가 유지되는 동안에는 검색 결과가 바뀌지 않는다.
    - scroll 옵션은 API 호출 시 인자로 scroll_id를 유지하는 기간을 설정해야 하는데(최초 1회만) 이는 힙 메모리 사용량에 영향을 주기 때문에 반드시 필요한 만큼만 설정해야 한다.
  
  ```bash
  # 최초 1회
  $ curl 'localhost:9200/인덱스명/_search?scroll=1m'-H 'Content-Type: application/json' -d '{
  "query":{
    "match":{
      "title":"Elasticsearch"
    }
  },
  }'
  
  # 이후
  $ curl 'localhost:9200/인덱스명/_search?scroll'-H 'Content-Type: application/json' -d '{
  "query":{
    "match":{
      "title":"Elasticsearch"
    }
  },
  }'
  ```



## Query DSL

- Query DSL(Domain Specific Language)
  - search API에서 가장 중요한 부분을 담당한다.
  - 검색 쿼리라고도 불린다.



- Query Context와 Filter Context로 분류한다.
  - Query Context
    - Full text search를 의미한다.
    - 검색어가 문서와 얼마나 매칭되는지를 표현하는 score라는 값을 가진다.
    - analyzer를 활용하여 검색한다.
  - Filter Context
    - Term Level Query라고도 부른다.
    - 검색어가 문서에 존재하는지 여부를 Yes나 No 형태의 검색 결과로 보여준다. 
    - score 값을 가지지 않는다.
    - analyzer를 활용하지 않는다.



## Query Context

- match 쿼리

  - 검색어로 들어온 문자열을 analyzer를 통해 분석한 후 역색인에서 해당 문자열의 토큰을 가지고 있는 문서를 검색한다.
    - 문서의 해당 필드에 설정해 놓은 analyzer를 기본으로 사용한다.
    - 별도의 analyzer를 사용할 때는 직접 명시해 주면 된다.

  - 토큰이 둘 이상일 경우 꼭 두 토큰을 모두 포함하는 문서만을 반환하는 것은 아니다.
    - score를 계산하여 score 순으로 문서를 반환한다.
  - match 쿼리는 어떤 토큰이 먼저 있는지에 대한 순서는 고려하지 않는다.
    - 즉 python guide가 들어오든 guide python이 들어오든 같은 결과를 보여준다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -d '{
  "query": {
    "match": {
      "title": "hadoop"
    }
  }
  }'
  ```



- match_phrase 쿼리

  - match_phrase는 match 쿼리와 달리 검색어의 순서도 고려한다.
    - 즉 아래의 경우 title에 guide가 python보다 먼저 나오는 문서는 검색 되지 않는다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -d '{
  "query": {
    "match_phrase": {
      "title": "python guide"
    }
  }
  }'
  ```



- match_all 쿼리

  - 모든 도큐먼트를 일치하게 한다.
    - 즉 모든 도큐먼트를 반환한다.

  - 사용

  ```json
  // GET <index_name>/_doc/_search
  {
      "query": {
        	"match_all":{}
      }
  }'
  ```



- mutli_match 쿼리

  - match와 동일하지만 두 개 이상의 필드에 match 쿼리를 날릴 수 있다.

  ```json
  // GET <index_name>/_doc/_search
  {
      "query": {
            "multi_match":{
                  "query": "term1 term2",
                  "fields": ["field1", "field2"] 
        }
  }
  ```
  
  - `operator`
    - 옵션으로 `operator`를 줄 수 있다.
    - 주의할 점은 `operator`가 각 filed 사이에 적용되는 것이 아니라, 각 term마다 적용된다는 것이다.
    - 예를 들어 위 예시에서 `operator`를 `and`로 주는 것은 `field1`에도 term1, term2가 포함되고, `filed2`에도 term1, term2가 포함된 문서를 찾는 것이 아니라, `field1`에 term1, term2가 모두 포함된 문서나 `field2`에 term1, term2가 모두 포함된 문서를 찾는것이다.
    - 만약, field 사이에 and를 적용시키고자 한다면 `type`을 `cross_field`로 주면 된다.
  - `minimum_shoud_match`
    - `operator`와 마찬가지로 동작한다.
  
  - `^` field명 뒤에 `^n`과 같이 특정 필드에 가중치를 줄 수 있다.
  
  ```json
  // GET <index_name>/_doc/_search
  {
      "query": {
            "multi_match":{
                  "query": "term1 term2",
                  "fields": ["field1^3", "field2"] 
        }
  }
  ```
  



- match_phrase_prefix

  - 검색어가 주어진 순서대로 존재하는 문서를 검색한다.
  - 마지막 검색어는 prefix로 취급된다.
  - 예시 데이터 색인

  ```json
  // PUT test/_bulk
  {"index":{"_id":"1"}}
  {"title":"quick brown fox"}
  {"index":{"_id":"2"}}
  {"title":"two quick brown ferrets"}
  {"index":{"_id":"3"}}
  {"title":"the fox is quick and brown."}
  ```

  - 검색
    - 1번, 2번 문서는 hit되지만, 3번 문서는 순서가 맞지 않기에 hit되지 않는다.

  ```json
  GET test/_search
  {
    "query":{
      "match_phrase_prefix": {
        "title": {
          "query":"quick brown f"
        }
      }
    }
  }
  ```

  - 옵션
    - `query`: 검색어를 입력한다.
    - `analyzer`: 검색어를 분석할 analyzer를 입력한다.
    - `slop`: matching된 토큰들 사이에 몇 개의 토큰을 허용할 것인지를 설정한다. 순서가 바뀐경우 slop은 2로 계산된다. 기본값은 0.
    - `max_expansions`: prefix로 취급되는 마지막 검색어가 확장될 최대 수를 지정한다(기본값은 50).
    - `zero_terms_query`: anayzer가 모든 토큰을 제거하여 hit된 doc이 없을 때, 어떻게 할지를 설정한다(default는 `none`). `none`은 아무 문서도 반환하지 않고 `all`일 경우 `match_all`과 같이 모든 문서를 반환한다.
  - `slop` 상세 설명
    - `the fox is quick and brown.`를 찾기 위해 `the`, `brown`을 검색했다면. `the`와 `brown`이라는 matching된 토큰들 사이에 `fox`, `is`, `quick`, `and`라는 4개의 토큰이 존재하므로 slop은 4로 설정해야한다.
    - 만일 `quick brown fox`를 찾기 위해 `brown quick`을 입력했다면, 원래 토큰의 순서가 뒤바뀐 것이므로 slop은 2로 설정해야한다.
    - 몇 번의 테스트 결과, 결과가 이상하게 나오는 경우가 있어 확인이 필요하다.
  - match_phrase_prefix 쿼리의 동작 방식
    - `quick brown f`라는 검색어가 들어왔을 때 prefix 쿼리로 동작하는 맨 마지막 어절(`f`)을 제외한 어절들(`quick brown`)은 match_phrase 쿼리로 동작한다.
    - 마지막 어절의 prefix를 위해서 인덱스 내의 토큰들 중 f로 시작하는 것을 사전순으로 찾는다.
    - 찾은 토큰들을 match_phrase 쿼리에 추가한다.
    - 즉 이 때 찾은 토큰의 개수만큼 쿼리가 생성된다.
  - 예시

  ```json
  GET test/_search
  {
    "query":{
      "match_phrase_prefix": {
        "title": {
          "query":"quick brown f"
        }
      }
    }
  }
  // 위 쿼리는 내부적으로 아래와 같이 동작한다.
  // 1. 맨 마지막 어절을 제외한 나머지 어절들로 match_phrase query를 생성한다.
  // 2. f로 시작하는 token을 사전순으로 찾는다(ferrets, fox)
  // 3. 해당 token들을 match_phrase query에 추가하여 검색한다.
  GET test/_search
  {
    "query":{
      "bool":{
          "should":[
              {
                  "match_phrase":{
                      "title":"quick brown ferrets"
                  }
              },
              {
                  "match_phrase":{
                      "title":"quick brown fox"
                  }
              }
          ]
      }
    }
  }
  ```

  - `max_expansions` 상세 설명
    - 상기했듯 match_phrase_prefix는 마지막 어절의 prefix를 위해서 인덱스 내의 토큰들 중 마지막 어절로 시작하는 토큰을 찾는 과정을 거친다.
    - 이 때, 몇 개의 토큰을 찾을지 설정하는 값이 `max_expansions`이다.
    - 따라서 찾으려는 값이 사전순으로 뒤로 밀려 있어서 `max_expansions`보다 뒤에 있다면, 찾지 못하는 경우가 생길 수 있다.
    - 또한 `max_expansion` 값이 너무 크고, 마지막 어절로 시작하는 토큰이 너무 많을 경우 검색 성능에 영향을 줄 수 있다.
    - 예를 들어 "aaaaaa", "aaaaab", "aaaaac", ..., "azzzzz"와 같이 색인된 문서가 있고, `max_expansions`값이 10000일 때, "a"로 검색하면 10000개의 쿼리가 생성되게 된다.
    - 이는 한 번의 query에 담을 수 있는 최대 clause의 개수(기본값은 4096)을 훨씬 뛰어 넘는 개수이므로 error가 발생하게 된다.

  ```json
  // 예시 데이터 bulk
  PUT test/_bulk
  {"index":{"_id":"1"}}
  {"title":"the word abuse"}
  {"index":{"_id":"2"}}
  {"title":"the word acid"}
  {"index":{"_id":"3"}}
  {"title":"the word advancement"}
  {"index":{"_id":"4"}}
  {"title":"the word aerialist"}
  
  // 검색
  GET test/_search
  {
    "query":{
      "match_phrase_prefix": {
        "title": {
          "query":"the word a",
          "max_expansions": 1
        }
      }
    }
  }
  
  // 응답
  // 위에서 max_expansions를 1로 줬으므로 a로 시작하는 토큰 중 사전순으로 가장 먼저 있는 abuse로만 query가 생성된다.
  // 따라서 the word abuse만 검색되게 된다.
  {
      // (...)
      "hits" : [
        {
          "_index" : "test",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 1.4146937,
          "_source" : {
            "title" : "the word abuse"
          }
        }
      ]
  }
  ```



- query_string 쿼리

  - 모든 필드를 검색하는 것이 가능하다.
    - 기존에는 `"fields":"_all"` 속성을 줘서 모든 필드에서 검색이 가능했지만 6.X 버전부터 막혔다.
    - 이제는 필드에 `copy_to` 속성을 줘서 모든 필드를 검색하는 기능을 구현할 수 있다.
    - 그러나 query_string은 굳이 모든 필드에 `copy_to` 속성을 주지 않아도 모든 필드를 검색하는 것이 가능하다.
  - and나 or 같은 검색어 간 연산이 필요한 경우에 사용한다.
  - 경우에 따라서 match 쿼리나 multi_match와 동일하게 동작할 수도 있고 정규표현식 기반의 쿼리가 될 수도 있다.
    - 와일드카드 검색도 가능하다.
    - 그러나 query_string을 통한 와일드 카드 검색은 스코어링을 하지 않을 뿐더러(모든 score가 1로 계산), 성능도 좋지 않기에 사용을 자제해야 한다. 
  - 요청 URL을 사용하여 검색

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?q=텀'
  ```

  - 본문 기반 검색

  ```bash
  $ curl 'localhost:9200/인덱스명/_search' -H 'Content-Type: application/json' -d '{
  "query":{
    "query_string":{
    	"query":"텀"
    }
  }'
  ```

  - 기본적으로 query_string 필드는 _all 필드를 검색한다.
    - 특정 필드를 지정하는 것이 가능하다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?q=필드명:텀'
  
  $ curl 'localhost:9200/인덱스명/_search' -H 'Content-Type: application/json' -d '{
  	"query":{
  		"query_string":{
  			"fields":"필드",
  			"query":"텀"
  	}
  }'
  ```

  - 이 밖에 다양한 쿼리 스트링 문법이 존재하는데 자세한 내용은 아래 링크 참조

      > https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html



- query string syntax

  - query string은 일련의 term들과 operator들로 파싱된다.
    - term은 한 단어일 수도 있고 큰따옴표로 묶인 문장일 수도 있다.
  - Field 지정하기

  | type                           | example               | description                                                  |
  | ------------------------------ | --------------------- | ------------------------------------------------------------ |
  | 기본형                         | `color:red`           | `:` 왼쪽에 쓰고, 오른쪽에 term을 쓴다.                       |
  | 여러 term 검색                 | `color:(red or blue)` | color field의 값이 red나 blue인 문서를 찾는다.               |
  | 정확한 순서로 검색             | `name:"John Doe"`     | name filed에서 정확히 John Doe 순서로 등장하는 값만 찾는다.  |
  | field 명에 space가 들어갈 경우 | `first\ name:John`    | `\`를 사용하여 space를 표현한다.                             |
  | 모든 sub field를 대상으로 검색 | `movie.\*:action`     | `movie.title`, `movie.genre`등 movie의 모든 sub field를 대상으로 검색한다. |
  | 값이 있는 field만 검색         | `_exists:title`       | title 필드에 값이 있는 문서만 검색한다.                      |

  - Wildcard
    - `term`의 시작 부분에 wildcard를 사용하는 것은 특히 더 많은 자원을 필요로 한다.
    - `bro*`는 일단 `bro`로 시작하는 것들을 찾으면 되지만 `*wn`은 일단 모든 단어를 찾고 이후에 `wn`이 들어가는지를 확인해야 하기 때문이다.
    - `allow_leading_wildcard`를 false로 줌으로써 시작 부분에 wildcard를 사용하지 못하도록 막을 수 있다.

  | type | example | description                                    |
  | ---- | ------- | ---------------------------------------------- |
  | `?`  | `qu?ck` | Single character를 대체하기 위해 사용한다.     |
  | `*`  | `bro*`  | 0개 이상의 character를 대체하기 위해 사용한다. |

  - Range

  | type                 | example                                   | description                                   |
  | -------------------- | ----------------------------------------- | --------------------------------------------- |
  | 날짜형 데이터에 사용 | `created_date:[2021-01-01 TO 2022-12-31]` | 2021년에 생성된 모든 data를 보여준다.         |
  | 숫자형 데이터에 사용 | `age:[1 TO 10]`                           | age field의 값이 1~10인 문서를 검색한다.      |
  | wildcard 사용        | `count:[10 TO *]`                         | count field의 값이 10 이상인 문서를 검색한다. |
  | 기준 값 제외         | `age:{1 TO 10}`                           | age filed의 값이 2~9인 문서를 검색한다.       |
  | 복합                 | `age:[1 TO 10}`                           | age filed의 값이 1~9인 문서를 검색한다.       |
  | 간단한 방식          | `age:<=10`                                | age filed의 값이 10이하인 문서를 검색한다.    |

  - Fuzziness
    - `~`를 사용하여 fuzzy query를 실행할 수 있다.
    - Fuzzy query에는 normalizer가 적용되므로, 소수의 filter만 적용 가능하다.
    - Damerau–Levenshtein distance를 사용하며, 기본값으로 설정된 편집거리는 2이다.
    - 그러나 사실 편집 거리가 1만 되어되 80%의 오타를 잡아낼 수 있다.
    - `quick~`과 같이 사용하며 edit distanc를 변경하고자 할 경우 `quick~2`와 같이 주면 된다.
    - proximity search에도 사용할 수 있는데, `"fox quick"~5`과 같이 사용하면 순서가 다르더라도 편집거리 5 이라면 검색된다.
    - `~`는 minimun_should_match에서도 사용되는데, `(title:foo title:bar title:baz)~2`는 foo, bar, baz 중 최소 둘 이상이 match되어야 한다는 뜻이다.
  - Boosting
    - `^`를 사용하여 특정 query에 가중치를 줄 수 있다.
    - `quick^2 fox`
    - term 뿐 아니라 문장(`"John Doe"^2`)이나 group(`(foo bar)^3`)에도 가중치를 줄 수 있다.
  - Boolean operation
    - 기본적으로 하나의 term만 matching되면, 다른 모든 term은 optional하다.
    - 예를 들어 `name:foo bar baz`와 같은 query_string의 경우 name이라는 필드에 foo, bar 혹은 baz 중 하나만 포함되어 있으면 검색 된다.
    - Boolean operation은 이러한 동작 방식을 변경하기 위해 사용한다.
    - `foo bar +baz -qux`는 `((foo AND baz) or (bar and baz) or baz) AND NOT qux`로 변경된다.
    - 즉, foo와 bar는 포함되던 안되던 baz가 포함되고, qux가 포함되지 않는다면 모든 문서가 검색된다.

  | type | example      | description                                                  |
  | ---- | ------------ | ------------------------------------------------------------ |
  | `+`  | quick +brown | brown을 포함하는 문서만 검색(quick은 포함되지 않아도 되지만, 포함되면 점수가 올라간다) |
  | `-`  | quick -brown | brown을 포함하지 않는 문서만 검색(quick은 포함되지 않아도 되지만, 포함되면 점수가 올라간다) |

  - 예약어
    - `\+ - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /`는 모두 예약어이므로, operator가 아닌 일반 문자로 사용하고자 한다면 `\`를 통해 escape 처리를 해줘야한다.
    - range query를 만들 때 사용하는 `<`와 `>`는 escape가 불가능하다.



## Filter context

- Filter Context
  - 단순히 해당 값이 해당 필드에 존재하는지 여부만 확인하고 스코어링은 하지 않는다(score는 1로 고정).
  - Filter context는 검색 결과를 캐싱하지만 Query context는 검색 결과를 캐싱하지 않는다.
  - 아래와 같은 것들이 filter context에 속한다.
    - bool query의 filter와 must_not parameter.
    - constant_score query의 filter parameter.
    - filter aggregation
  - Exact value query
    - 아래서에서 소개하는 term, terms, terms_set, range, wildcard 등은 단순히 검색어가 일치하는지 여부만을 판단한다.
    - 기본적으로 검색어를 analyzing하지 않지만, filter context가 아닌 곳에서 사용할 경우 score 값은 반환한다.
    - 그러나 문서의 일치 여부를 yes/no로만 판단하므로 모두 같은 점수가 나오게 된다.
    - 그러나 filter context에서 검색하는 것은 아니므로 결과를 caching하지는 않는다.



- term 쿼리

  - ES에서 term은 검색어를 말한다.
  - 역색인에 있는 토큰들 중 정확하게 일치하는 값을 찾는다.
    -  match 쿼리와 달리 검색어를 analyze하지 않는다.
    -  analyze를 하지 않기 때문에 당연히 대소문자를 구분한다.
  - 필드와 term을 지정해서 도큐먼트 내에서 검색할 수 있다.
    - 검색한 텀이 분석되지 않았기 때문에 완전히 일치하는 도큐먼트 결과만 찾는다.
  - 예제
    - 특정 term이 특정 필드에 있으면 해당 도큐먼트의 name과 tags를 반환한다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query":{
    "term":{
      "필드": "텀"
    }
  },
  "_source":["name","tags"]
  }'
  ```



- terms 쿼리

  - 둘 이상의 term을 검색할 때 사용하는 쿼리.
    - 여러 개의 term 중 하나라도 일치하면 검색 된다.

  - 예제

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query":{
    "terms":{
      "필드": ["텀1","텀2"]
    }
  },
  "_source":["name","tags"]
  }'
  ```

  - 만열 하나 이상의 term이 일치할 경우에만 검색되게 하려면 `terms_set` query를 사용해야 한다.



- `terms_set`

  - 여러 term 중 하나만 일치하면 검색 되는 `terms` 쿼리와 달리, 몇 개의 term이 일치해야 검색될지를 설정 가능하다.
  - 옵션
    - `minimum_should_match_field`: 몇 개가 일치해야 검색 결과로 반환할지를 저장하고 있는 Numeric field를 받는다.
    - `minimum_should_match_script`: 몇 개가 일치해야 검색 결과로 반환할지를 결정하는 script를 받는다.

  - 예시

  ```json
  // 아래와 같은 data가 있을 때
  PUT /job-candidates/_doc/2?refresh
  {
    "name": "Jason Response",
    "programming_languages": [ "java", "php" ],
    "required_matches": 2
  }
  
  // 아래와 같이 검색하면, "c++", "java", "php" 중 둘 이상이 포함된 문서만 검색된다.
  GET /job-candidates/_search
  {
    "query": {
      "terms_set": {
        "programming_languages": {
          "terms": [ "c++", "java", "php" ],
          "minimum_should_match_field": "required_matches"
        }
      }
    }
  }
  
  // 아래와 같이 검색하면 "c++", "java", "php" 중 하나 이상이 포함된 문서만 검색된다.
  GET /job-candidates/_search
  {
    "query": {
      "terms_set": {
        "programming_languages": {
          "terms": [ "c++", "java", "php" ],
          "minimum_should_match_script":{
            "source": "1"
          }
        }
      }
    }
  }
  ```





- Elasticsearch는 mapping되어 있는 field에 값을 넣지 않는 것이 가능하다.

  - Elasticsearch를 사용하다 보면 특정 필드에 값이 있는 문서의 개수가 몇 개인지 알아야 할 때가 있음에도 불구하고, 이러한 특성 때문에 특정 필드의 값을 가진 문서의 개수를 정확히 알 수 업는 경우가 많다.

  ```json
  PUT test-index
  {
      "mappings":{
          "properties":{
              "foo":{
                "type": "text"
              },
              "bar":{
                "type": "text"
              },
              "baz":{
                "type":"integer"
              }
          }
      }
  }
  
  PUT test-index/_doc/1
  {
    "foo":"hello world!"
  }
  
  PUT test-index/_doc/2
  {
    "bar":"goodbye world!"
  }
  
  PUT test-index/_doc/3
  {
    "baz":0
  }
  ```

  - 이 때 query string query를 사용하면 쉽게 구할 수 있다.
    - query string syntax 중 `_exists_`를 사용한다.

  ```json
  GET test-index/_search
  {
    "query": {
      "query_string": {
        // foo 필드에 값이 있는 문서만 반환한다.
        "query": "_exists_:foo"
      }
    }
  }
  ```



- range 쿼리

  - 범위를 지정하여 특정 값의 범위 이내에 있는 경우를 검색할 때 사용한다.
    - 아래 예시는 release_date를 기준으로 특정 범위 내의 값들을 검색하는 예시이다.

  ```bash
  $ curl "localhost:9200/인덱스명/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "range":{
      "release_date":{
        "gte":"2015/01/01",
        "lte":"2015/12/31"
      }
    }  
  }
  }'
  ```
  
  - format을 지정할 수 있다.
    - 주지 않을 경우 검색 대상 index의 해당 field의 format을 기본 값으로 사용한다.
    - `"format":"yyyy-MM-dd'T'HH:mm:ss.SSS"`와 같은 형태로 주면 된다.
  
  - Elasticsearch의 **Date Math**
  
    - ES에서 date를 기준으로 쿼리를 작성하는 경우(range query, daterange aggs 등)아래와 같은 Date Math를 사용 가능하다.
    - `now`의 기준은 UTC이므로 한국에서 사용한다면 `+09:00`을 해줘야 한다.
    - 또한 `now`는 `range` query에서 설정 가능한 `timezone` 옵션의 영향을 받지 않는다.
  
  | 기호 | 뜻             | 기호   | 뜻        |
  | ---- | -------------- | ------ | --------- |
  | y    | years          | h(==H) | hours     |
  | M    | months         | m      | minutes   |
  | w    | weeks          | s      | seconds   |
  | d    | days           | now    | 현재 시간 |
  | /    | 내림 또는 올림 | +, -   | 시간 +, - |
  
    - 예시
      - `now`가 `2021-01-01 12:00:00`일 경우
      - `now+1h`: `2021-01-01 13:00:00`
      - `now+1d`: `2021-01-02 12:00:00`
      - `now-1h/d`: `now`에서 한 시간을 뺀 뒤 내림(rounded down)해서 `2021-01-01 00:00:00`이 된다.
      - `2021-02-01||+1M/d`: 1달을 추가한 뒤 내림해서 `2021-03-01 00:00:00`이 된다.
    - `gt`, `gte`, `lt`, `lte` 중 어디에 쓰이는지에 따라서도 달라진다.
      - `gt`: Rounds up to the first millisecond not covered by the rounded date.
      - `gte`: Rounds down to the first millisecond.
      - `lt`: Rounds down to the last millisecond before the rounded value.
      - `lte`: Rounds up to the latest millisecond in the rounding interval.
  
  - 쿼리 예시
  
    - 1시간 전 데이터 검색
  
  
  ```bash
  # 예시 데이터 bulk
  PUT time-test/_bulk
  {"index":{"_id":"1"}}
  {"test_time":"2021-01-01T00:00:00"}
  {"index":{"_id":"2"}}
  {"test_time":"2021-01-01T00:15:00"}
  {"index":{"_id":"3"}}
  {"test_time":"2021-01-01T00:30:00"}
  {"index":{"_id":"4"}}
  {"test_time":"2021-01-01T00:45:00"}
  {"index":{"_id":"5"}}
  {"test_time":"2021-01-01T00:59:59"}
  {"index":{"_id":"6"}}
  {"test_time":"2021-01-01T01:00:00"}
  {"index":{"_id":"7"}}
  {"test_time":"2021-01-01T01:15:00"}
  {"index":{"_id":"8"}}
  {"test_time":"2021-01-01T01:30:00"}
  {"index":{"_id":"9"}}
  {"test_time":"2021-01-01T01:45:00"}
  {"index":{"_id":"10"}}
  {"test_time":"2021-01-01T01:59:99"}
  {"index":{"_id":"11"}}
  {"test_time":"2021-01-01T02:00:00"}
  
  # 1시간 전 데이터 검색
  GET time-test/_search
  {
    "query": {
      "range":{
        "test_time": {
          "gte": "2021-01-01T01:00:00||-1h",
          "lt": "2021-01-01T01:00:00"
        }
      }
    }
  }
  ```
  
  - `now`를 활용하여 1시간 전 data를 검색하는 쿼리
    - `now`는 UTC기준이므로 현재는 `now+9h`가 된다.
  
  ```json
  GET test-index/_search
  {
    "query": {
      "range": {
        "my_date_field": {
          "gte": "now+8h/h",
          "lt": "now+9h/h"
        }
      }
    }
  }
  ```
  




- wildcard 쿼리

  - 와일드카드 특수문자를 이용한 일종의 Full-Scan 검색이 가능한 쿼리이다.
    - 와일드카드 쿼리는 역색인을 하나하나 확인하기 때문에 검색 속도가 매우 느리다.
    - 따라서 꼭 와일드카드 쿼리를 써야 하는 상황이 아니면 사용을 자제하는 것이 좋다.
  - text 필드가 아닌 keyword 타입의 쿼리에 사용해야 한다.
    - keyword 타입에 사용해야 하므로 아래 예시에서도 text 타입인 pushlisher 필드가 아닌 publisher.keyword 필드를 사용하여 키워드 타입에 사용했다.
    - text 필드에도 사용은 가능하다. 그러나 이 경우 역색인을 기준으로 결과를 검색한다.
  
  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "wildcard":{
      "publisher.keyword":"*Media*"
    }
  }
  }'
  ```



### bool query

- bool query

  - Query Context와 Filter Context만 가지고는 검색 조건을 맞추기가 불가능하다.
  - 따라서 두 가지 이상의 쿼리를 조합해서 사용해야 하는 경우가 있다.
  - 이를 가능하게 하는 방법 중에서도 가장 대중적이고 많이 사용되는 방법이 bool query이다.
  - bool query에서 사용할 수 있는 항목들
    - 아래 특성들을 기준으로 어디서 실행될지가 결정된다.
    - 스코어링을 하는 must, should는 Query Context에서 실행된다.
    - 스코어링을 하지 않는 filter, must_not은 Filter Context에서 실행된다.

  | 항목     | 항목 내 쿼리에 일치하는 문서를 검색하는가?  | 스코어링 | 캐싱 |
  | -------- | ------------------------------------------- | -------- | ---- |
  | must     | O                                           | O        | X    |
  | should   | O                                           | O        | X    |
  | filter   | O                                           | X        | O    |
  | must_not | X(항목 내 쿼리에 일치하지 않는 문서를 검색) | X        | O    |

  - 예시
    - match 쿼리와 range 쿼리 두 개를 조합.

  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "bool": {
      "must":[
        {
          "match":{
            "title":"elasticsearch"
          }
        }
      ],
      "filter":[
        {
          "range": {
            "release_date": {
              "gte":"2016/01/01",
              "lte":"2017/12/31"
            }
          }
        }
      ]
    }
  }
  ```
  
  - must와 should의 차이
    - must는 must내에 있는 모든 쿼리가 일치해야 한다(and 조건).
    - should는 should 내에 있는 쿼리 중 하나라도 일치하면 된다(or 조건).
    - 단, should의 경우 많이 일치된 문서일수록 socre가 높아진다.



- Filter Context에 포함되는 쿼리들은 filter 절에 넣는 것이 좋다.

  - 아래 예시 코드 보다 위 예시 코드가 더 빠르다.

  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "bool": {
      "must":[
        {
          "match":{
            "title":"elasticsearch"
          }
        },
        {
          "range": {
            "release_date": {
              "gte":"2016/01/01",
              "lte":"2017/12/31"
            }
          }
        }
      ],
    }
  }
  ```

  - 이유
    - must 절에 포함된 Filter Context들은 score를 계산하는 데 활용되기 때문에 불필요한 연산이 들어가지만, filter절에 포함되면 Filter Context에 맞게 score 계산이 되지 않기 때문이다.
    - 또한 filter절에서 실행된 range 쿼리는 캐싱의 대상이 되기 때문에 결과를 빠르게 응답 받을 가능성이 높다.

  - 결론
    - 검색 조건이 yes/no 만을 포함하는 경우라면 filter절에 넣어 Filter Context에서 실행되게 한다.
    - 매칭의 정도가 중요한 조건이라면 must 혹은 should 절에 포함시켜서 Query Context에서 실행되도록 해야 한다.



- must_not

  - 쿼리에 일치하지 않는 문서를 검색하는 쿼리
  - 특징
    - filter 절과 마찬가지로 Filter Context에서 실행되어 score 계산을 하지 않는다.
    - 문서 캐싱의 대상이 된다.

  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "bool": {
      "must":[
        {
          "match":{
            "title":"elasticsearch"
          }
        },
        {
          "range": {
            "release_date": {
              "gte":"2016/01/01",
              "lte":"2017/12/31"
            }
          }
        }
      ],
      "must_not":[
        {
          "match": {
            "descrption": "performance"
          }
        }
      ]
    }
  }
  ```



- should

  - 검색된 결과 중 should절 내에 있는 term과 일치하는 부분이 있는 문서는 스코어가 올라가게 된다.
    - 아래 결과를 should를 사용하지 않은 일반적인 쿼리문과 비교해 보면 같은 문서임에도 score가 다른 것을 확인 가능하다.
  
  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "bool": {
      "must":[
        {
          "match":{
            "title":"elasticsearch"
          }
        },
        {
          "range": {
            "release_date": {
              "gte":"2016/01/01",
              "lte":"2017/12/31"
            }
          }
        }
      ],
      "should":[
        {
          "match": {
            "description": "performance"
          }
        },
        {
          "match": {
            "description": "search"
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
  ```
  
  - `minimum_should_match` 옵션을 제공한다.
    - `should` 절에 포함되지 않아 bool query 전체에 적용되는 옵션 같지만 should 절에만 적용되는 옵션이다.
    - should 항목에 포함된 쿼리 중 적어도 설정된 수치만큼의 쿼리가 일치할 때 검색 결과를 보여주는 옵션이다.
    - should절을 사용할 때 꼭 써야만 하는 옵션은 아니다.
    - 양수일 경우 그 이상의 쿼리가, 음수일 경우 총 쿼리 개수에서 음수를 뺀 만큼의 쿼리가 일치해야 한다.
    - 퍼센트로 설정하는 것도 가능하다.
    - 설정해 주지 않으면 `must` 혹은 `must_not`, `filter`등 다른 bool query와 함께 사용할 경우에는 0, should만 사용할 경우에는 1이 default 값이다.
  
  ```json
  // 예를 들어 아래와 같은 경우 should절의 query들 중 match되는 것이 아무 것도 없어도 must절에만 match된다면 검색이 된다.
  {
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "name": "John"
            }
          }
        ],
        "should": [
          {
            "match": {
              "age": 28
            }
          }
        ]
      }
    }
  }
  
  // 반면 아래의 경우 should절의 query들 중 적어도 하나는 match가 되어야 검색이 된다.
  {
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "name": "John"
            }
          }
        ],
        "should": [
          {
            "match": {
              "age": 28
            }
          }
        ],
        "minimum_should_match":1
      }
    }
  }
  ```
  







## multi-match

- `best_fields`(default)

  - 모든 field들을 대상으로 검색을 하지만 가장 높은 점수가 나온 field의 점수를 최종 점수로 사용한다.
    - 따라서 여러 개의 term이 하나의 field에 많이 나올수록 점수가 높아진다.
    - 예를 들어 "brown fox"라는 term이 있을 때 "brown"과 "fox"가 하나의 field에 나오는 것이 "brown", "fox"가 각기 다른 field에 나오는 것 보다 높은 점수를 받게 된다.
  - 각각의 field에 대해 `match` query를 생성하고, 생성된 `match` query들을 `dix_max` query로 묶는다.
    - 이는 가장 많은 term이 matching된 field를 찾기 위함이다.

  ```json
  // 예를 들어 아래와 같이 best_fields를 사용한 query는
  {
      "query": {
          "multi_match" : {
              "query":      "brown fox",
              "type":       "best_fields",
              "fields":     [ "subject", "message" ],
              "tie_breaker": 0.3
          }
      }
  }
  
  // 아래와 같은 dis_max query로 변환된다.
  {
      "query": {
          "dis_max": {
              "queries": [
                  { "match": { "subject": "brown fox" }},
                  { "match": { "message": "brown fox" }}
              ],
              "tie_breaker": 0.3
          }
      }
  }
  ```

  - `tie_breaker`
    - 기본적으로, `best_fields`는 가장 검색어가 matching이 많이 된 하나의 field의 점수를 사용한다.
    - 그러나 `tie_breaker`를 줄 경우, 다른 모든 matching filed의 점수에 `tie_breaker`의 값을 곱한 값을 가장 검색어가 matching이 많이 된 하나의 field의 점수에 더해 결과를 계산한다.

  - 점수 계산 방식 확인을 위한 data 색인

  ```json
  // PUT score-test/_doc/1
  {
    "field1":"foo bar",
    "field2":"foo",
    "field3":"bar"
  }
  ```

  - Test data를 대상으로 type이 `best_fields`인 `multi_match` query를 실행한다.

  ```json
  GET score-test/_search
  {
      "explain": true, 
      "query": {
          "multi_match": {
              "query": "foo bar",
              "fields": [
                  "field1",
                  "field2",
                  "field3"
              ],
              "tie_breaker": 0.5
          }
      }
  }
  ```

  - 응답
    - 검색어 "foo"와 "bar"가 모두 포함되어 있는 `field1`의 점수가 최고 점수(0.5753642)가 되며, `tie_breaker`를 주지 않았을 경우 이 점수가 최종 점수가 된다.
    - 그러나 위 query에서는 `tie_breaker`를 줬으므로 다른 matching된 다른 field들의 점수에 `tie_breaker` 값을 곱한 값을 더해야한다.
    - "foo"가 matching된 `field2`의 점수 0.2876821에 `tie_breaker` 값을 곱한 0.14384105과 "bar"가 matching된 `field1`의 점수 0.2876821에 `tie_breaker` 값을 곱한 0.14384105를 더해준다.
    - 결국 최종 점수는 `0.5753642 + 0.14384105 + 0.14384105=0.8630463`가 된다.

  ```json
  {
  	"_explanation": {
  		"value": 0.8630463,
  		"description": "max plus 0.5 times others of:",
  		"details": [
  			{
  				"value": 0.2876821,
  				"description": "sum of:",
  				"details": [
  					{
  						"value": 0.2876821,
  						"description": "weight(field3:bar in 0) [PerFieldSimilarity], result of:",
  						// ...
  					}
  				]
  			},
  			{
  				"value": 0.2876821,
  				"description": "sum of:",
  				"details": [
  					{
  						"value": 0.2876821,
  						"description": "weight(field2:foo in 0) [PerFieldSimilarity], result of:",
  						// ...
  					}
  				]
  			},
  			{
  				"value": 0.5753642,
  				"description": "sum of:",
  				"details": [
  					{
  						"value": 0.2876821,
  						"description": "weight(field1:foo in 0) [PerFieldSimilarity], result of:",
  						// ...
  					},
  					{
  						"value": 0.2876821,
  						"description": "weight(field1:bar in 0) [PerFieldSimilarity], result of:",
  						// ...
  					}
  				]
  			}
  		]
  	}
  }
  ```



- `most_fields`

  - 모든 field들을 대상으로 검색을 하고, 각 field들의 점수를 결합한다.
    - 각기 다른 analyzer로 분석된 같은 text를 대상으로 검색할 때 유용하게 사용할 수 있다.
    - 예를 들어 어떤 field의 한 sub field는 synonym과 stemming으로 analyzing했고, 다른 sub field는 standard tokenizer만 사용하여 색인한 경우 이들 두 sub field의 점수를 결합하여 검색어가 여러 field에서 종합적으로 matching된 문서를 상단으로 올릴 수 있다.
  - `should`와 동일하게 동작한다고 생각하면 된다.

  ```json
  // 예를 들어 아래와 같은 query는
  {
      "query": {
          "multi_match" : {
              "query":      "quick brown fox",
              "type":       "most_fields",
              "fields":     [ "title", "title.original", "title.shingles" ]
          }
      }
  }
  
  // 아래의 should query와 동일하다.
  {
      "query": {
          "bool": {
              // should 라는 것에 주목해야 한다.
              "should": [
                  { "match": { "title":          "quick brown fox" }},
                  { "match": { "title.original": "quick brown fox" }},
                  { "match": { "title.shingles": "quick brown fox" }}
              ]
          }
      }
  }
  ```



- `cross_fields`

  - 같은 analyzer를 사용하는 field들을 하나의 field처럼 처리하여, 각 term이 어떤 field에 있던 검색한다.
    - Term들이 여러 field에서 matching되는 것이 나을 때 유용하게 사용할 수 있다.
    - 얘를 들어 "George Washington"이라는 검색어가 있고, `first_name`, `last_name`이라는 field들이 있을 때, "George"가 `first_name`에 "Washington"이 `last_name`에서 검색되는 것이 더 자연스럽다.

  - 그냥 `most_fields`를 쓰면 되는 것 아닌가?
    - `cross_fields` 대신 `most_fields`를 쓰기에는 두 가지 문제가 있다.
    - 첫 번째 문제는 `most_fields`의 경우  `operator`와 `minium_should_match`는 각 field마다 적용된다는 점이다.
    - 두 번째 문제는 각 field의 서로 다른 term frequency가 예상치 못한 결과를 반환할 수 있다는 점이다.
    - 예를 들어 각기 "George Washington"과 "Washington Irving"에 대한 문서가 있다고 가정해보자. 
    - "Washington"은 매우 흔한 last name이므로, `last_name`에 "Washington"이 들어가는 경우 term frequency가 높아 높은 점수를 받지 못할 것이다.
    - 반면에, first name으로 쓰이는 "Washington"은 그리 흔하지 않으므로, `first_name`에 "Washington"이 들어가는 경우 term frequency가 낮아 높은 점수를 받게 될 것이다.
    - 따라서 "George Washington"을 검색할 경우 `last_name`에 "Washington"이 들어간 문서보다 `first_name`에 "Washington"이 들어간 문서가 더 높은 점수를 받을 것이다.
    - 즉, `first_name:George last_name:Washington`이라는 보다 더 많은 term이 matching되는 문서가 있음에도, `first_name:Washington`인 문서가 더 높은 점수로 검색 결과의 상단에 올라올 위험이 있다.
  
  - best_fields와 most_fields는 field-centric한 접근법을 취한다.
    - 각 field마다 `match` query를 생성한다.
  
  - `cross_fields`는 term-centric한 접근법이다.
    - 위 문제를 해결하는 가장 간단한 방법은 index시에 `first_name`과 `last_name`을 `full_name`이라는 하나의 field에 색인하는 것이다.
    - 이는 `best_fields`나 `most_fields`가 취하는 field-centric한 접근법이다.
    - 반면에 `cross_fields`는 term-centric한 접근법으로 index time이 아니라 query time에 이를 해결할 수 있게 해준다.
  - `cross_fields`는 검색어를 여러 개의 term으로 쪼갠 후 각 term이 여러 field들 중 어디에든 포함되어 있는지를 살핀다.
    - 즉 여러 field들을 하나의 field인 것 처럼 취급한다.
    - `best_fields`의 경우 `operator`를 `and`로 줄 경우 한 field에 모든 term이 들어가 있는 문서를 검색한다(field-centric).
    - `cross_fields`의 경우 `operator`를 `and`로 줄 경우 모든 term이 검색 대상 field들 중 어디에든 들어가 있는 문서를 검색한다(term-centric).
  
  ```json
  // 아래와 같이 cross_fields를 적용한 query는
  {
      "query": {
          "multi_match" : {
              "query":      "George Washington",
              "type":       "cross_fields",
              "fields":     [ "first_name", "last_name" ],
              "operator":   "and"
          }
      }
  }
  
  // 아래와 같이 처리된다.
  +(last_name:george | first_name:george) +(last_name:washington | first_name:washington)
  
  // 만약 위에서 cross_fields가 아닌 best_fields를 사용했다면, 아래와 같이 처리된다.
  ((+last_name:george +last_name:washington) | (+first_name:george +first_name:washington))
  ```
  
  - 위와 같이 query를 생성함으로써 `cross_fields`는 term frequency가 달라지는 문제를 해결한다.
    - 모든 field들의 term frequency를 혼합한다.
    - 위 예시에서 `first_name:washington`는  `last_name:washington`와 동일한 frequency를 갖는 것 처럼 처리된다.
    - 물론 이 경우에도 `last_name:washington`이 약간 더 점수를 높이긴 한다.
    - 다만, 이처럼 `cross_fields`를 사용하여 term frequency를 조정하는 방식은 `boost`가 1인 짧은 string field에만 유효하다는 점을 기억해야한다.
    - `boost`나 length normalization은 모든 field들의 term frequency를 혼합하여 term frequency를 조정하는 방식을 의미 없게 만든다.
  - `cross_fields`는 같은 analyzer를 사용한 field들 끼리만 하나의 field로 취급한다.
    - 즉 같은 analyzer를 사용하는 field들을 하나의 group으로 묶어 이들을 하나의 field처럼 취급한다.
  
  ```json
  // 예를 들어 아래와 같이 index를 생성하고
  // PUT score-test
  {
      "settings": {
          "analysis": {
              "analyzer": {
                  "nori_analyzer":{
                      "type":"custom",
                      "tokenizer":"nori_tokenizer"
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "A":{
                  "type":"text"
              },
              "B":{
                  "type":"text",
                  "analyzer": "nori_analyzer"
              },
              "C":{
                  "type":"text",
                  "analyzer": "nori_analyzer"
              }
          }
      }
  }
  
  // 아래와 같이 검색을 하면
  // GET score-test/_search
  {
      "query": {
          "multi_match": {
              "query": "안녕 세상",
              "type":"cross_fields", 
              "fields": [
                  "A",
                  "B",
                  "C"
              ],
              "operator": "and"
          }
      }
  }
  
  // 아래와 같이 같은 analyzer를 사용한 field들끼리 묶인다.
  ((+A:안녕 +A:세상) | (+(C:안녕 | B:안녕) +(B:세상 | C:세상)))
  ```
  
  - 위와 같이 각기 다른 analyzer들을 multi_match의 대상 field로 묶는 방식 자체는 별 문제가 되지 않지만, `operator`나 `minimum_should_match`를 사용할 때는 `most_fields`나 `best_fields`에서 `operator`나 `minimum_should_match`를 사용할 때 겪는 문제를 동일하게 겪을 수 있다.
    - 따라서 `operator`나 `minimum_should_match`를 사용해야 할 때는 같은 analyzer를 사용하는 fields들 끼리 묶어서 아래와 같이 `dis_max` query를 사용하는 것이 권장된다.
  
  ```json
  {
      "query": {
          "dis_max": {
              "queries": [
                  {
                      "multi_match" : {
                          "query":      "안녕 세상",
                          "type":       "cross_fields",
                          "fields":     [ "A" ],
                          "minimum_should_match": "50%" 
                      }
                  },
                  {
                      "multi_match" : {
                          "query":      "안녕 세상",
                          "type":       "cross_fields",
                          "fields":     [ "B", "C" ]
                      }
                  }
              ]
          }
      }
  }
  ```



- `multi_match` query의 type을 `phrase`나 `phrase_prefix`로 줄 경우.

  - 기본적으로 `best_field` 같이 동작한다.
    - 다만 `match_query` 대신 `match_phrase` 혹은 `match_phrase_prefix` query를 사용한다는 차이가 있다.

  ```json
  // 아래와 같은 query는
  {
      "query": {
          "multi_match" : {
              "query":      "quick brown f",
              "type":       "phrase_prefix",
              "fields":     [ "subject", "message" ]
          }
      }
  }
  
  // 아래와 같이 실행된다.
  {
      "query": {
          "dis_max": {
              "queries": [
                  { "match_phrase_prefix": { "subject": "quick brown f" }},
                  { "match_phrase_prefix": { "message": "quick brown f" }}
              ]
          }
      }
  }
  ```

  - 둘 다 `slop` parameter를 사용할 수 있으며, `phrase_prefix`의 경우 추가적으로 `max_expansions`를 사용할 수 있다.





## Count API

- 쿼리와 일치하는 문서의 개수를 셀 때 사용하는  API

  - 기본형

  ```bash
  GET /<target>/_count
  ```

  - `<target>`에는 아래와 같은 것들이 올 수 있다.
    - 인덱스 이름(wildcard 사용 가능)
    - alias
    - `_all`(또는 `*`)
    - data streams
    - 위의 것들을 포함하는 리스트



- 주요 query parameters

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/search-count.html

  - `allow_no_indices`(Optional, Boolean)
    - false로 설정하면 검색 대상 인덱스 중 닫혀 있거나 존재하지 않는 인덱스가 있을 경우 error를 반환한다.
  - `analyzer`(Optional, String)
    - query string에 사용할 analyzer를 지정한다.
  - `analyze_wildcard`(Optional, Boolean, Default:true)
    - wildcard와 프리픽스 쿼리에 analyzer를 적용할지 여부를 지정.
  - `default_operator`(Optional, String, Default:OR)
    - query string의 기본 operator를 설정한다.
    - AND, OR 중 선택 가능하다.
  - `df`(Optional, String)
    - query string에 필드를 지정하지 않았을 경우 기본 필드로 사용할 필드를 지정한다.
  - `expand_wildcards`(Optional, String, Default:open)
    - wildcard 검색이 match시킬 인덱스의 타입을 지정한다.
    - 아래의 값들을 콤마로 구분하여 하나 이상 사용 가능하다.
    - `all`: hidden 인덱스나 데이터 스트림을 포함하여 모든 것들을 match시킨다.
    -  `open`: open , non-hidden 인덱스 또는 non-hidden data stream을 match 시킨다.
    -  `close`: closed, non-hidden 인덱스 또는 non-hidden data stream을 match 시킨다.
    - `hidden`: hidden 인덱스 또는 hidden data stream을 match 시킨다.
    - `none`: wildcard가 어떤 것도 match시키지 않는다.
  - `q`(Optional, string)
    - count 대상 문서를 찾을 쿼리를 입력한다.

  - etc



## Retrieve inner hits

- inner hists

  - Parent-join 필드와 nested 필드는 각기 다른 scope에서 쿼리와 일치하는 문서들을 검색할 수 있다는 특징이 있다.
    - parent/child의 경우 쿼리와 일치하는 parent documents를 기반으로 child document를 검색할 수 있고, 쿼리와 일치하는 child document를 기반으로 parent documents를 검색할 수 있다.
    - nested 필드의 경우, nested 내부의 쿼리와 일치하는 objects를 기반으로 문서를 검색할 수 있다.
  - 두 경우 모두 검색의 기반이 되는 문서들이 감춰지게 된다.
    - 예를 들어  parent documents를 기반으로 child document를 검색할 경우 parent documents는 감춰지게 된다.
  - inner hists는 이와 같이 감춰진 문서들을 보는 데 사용하는 기능이다.
    - 각각의 search hit가 도출되게 한 기반이 되는 문서들을 함께 반환한다.
    - `inner_hits`는 `nested`, `has_child`, `has_parent` 쿼리 혹은 필터에 정의하여 사용한다.
    - 만일 `inner_hits`가 쿼리에 정의되었다면 각각의 search hit는 `inner_hits` json object를 함께 반환한다.
  - 기본형
    - `from`: 반환된 search hits에서 fetch 할 첫 번째 hit의 offset을 설정
    - `size`: 각각의 inner_hits가 반환 할 hits의 최댓값(기본값은 3)
    - `sort`: 각각의 inner_hits에서 inner_hits를 어떻게 정렬할지 설정(기본값은 score를 기반으로 정렬)
    - `name`: 특정한 inner hit에 사용할 이름을 정의한다. 다수의 inner hits가 정의되었을 경우 유용하다.

  ```json
  "<query>":{
  	"inner_hits":{
          <inner_hits_options>
      }
  }
  ```

  - 아래와 같은 기능들을 제공한다.
    - 하이라이팅
    - Explain(점수 계산 방식 설명)
    - Search fields(검색할 필드 특정)
    - Source filtering(반환 받을 필드 특정)
    - Script fileds(script를 사용하여 검색)
    - Doc value fields
    - Include versions(doument의 버전도 함께 반환)
    - Include Sequence Numbers and Primary Terms(sequence number and primary term을 함께 반환)



- Nested inner hits

  - nested 필드의 inner hits를 확인할 때 사용한다.
  - 테스트 인덱스 생성

  ```bash
  PUT test
  {
    "mappings": {
      "properties": {
        "comments": {
          "type": "nested"
        }
      }
    }
  }
  ```

  - 테스트 데이터 색인

  ```bash
  PUT test/_doc/1?refresh
  {
    "title": "Test title",
    "comments": [
      {
        "author": "kimchy",
        "number": 1
      },
      {
        "author": "nik9000",
        "number": 2
      }
    ]
  }
  ```

  - 검색

  ```bash
  POST test/_search
  {
    "query": {
      "nested": {
        "path": "comments",
        "query": {
          "match": { "comments.number": 2 }
        },
        "inner_hits": {}	//inner_hits를 정의
      }
    }
  }
  ```

  - 응답
    - 정렬과 scoring으로 인해, inner_hits내부에 있는 hit object의 위치는 일반적으로 nested 필드에 정의 된 object의 위치와 달라지게 된다.
    - 기본값으로 inner_hits 내부의 hit objects에 대한 `_source`도 반환되지만, `_source` 필터링 기능을 통해 source를 변경하거나 비활성화 할 수 있다.
    - `fields`를 설정하여 nested 내부에 정의된 필드도 반환 할 수 있다.
    - `inner_hits` 내부의 hits들의 `_source`는 기본적으로  `_nested`의 metadata만을 반환한다. 아래 예시에서도 comment가 포함 된 문서의 전체 source가 이닌, comments 부분만 반환된 것을 확인 가능하다.

  ```json
  {
    ...,
    "hits": {
      "total": {
        "value": 1,
        "relation": "eq"
      },
      "max_score": 1.0,
      "hits": [
        {
          (...)
          // inner_hits 정보
          "inner_hits": {
            "comments": { 
              "hits": {
                "total": {
                  "value": 1,
                  "relation": "eq"
                },
                "max_score": 1.0,
                "hits": [
                  {
                    "_index": "test",
                    "_type": "_doc",
                    "_id": "1",
                    "_nested": {
                      "field": "comments", // 어떤 nested 필드에서 hit한 것인지 표시
                      "offset": 1
                    },
                    "_score": 1.0,
                    "_source": {
                      "author": "nik9000",
                      "number": 2
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }
  }
  ```



- Nested inner hits와 `_source`

  - 문서의 전체 source가 상위 document의 `_source`필드에 저장되어 있기 때문에 nested 문서는 `_source` 필드가 존재하지 않는다.
    - nested 문서에 소스를 포함시키려면 상위 문서의 source가 파싱 되어야 하고, nested 문서에 관련된 부분만 inner hit의 source로 포함되어야 한다.
    - 쿼리와 일치하는 각각의 nested 문서에 위 작업을 수행하면, 전체 검색 요청을 수행하는 시간에 영향을 미치게 된다.
    - 특히 `size`와 inner hits의 `size`가 기본값보다 높게 설정되어 있를 때 더 큰 영향을 미치게 된다.
  - nested inner hits에서 `source`를 추출하는데 상대적으로 많은 비용이 들어가는 것을 피하기 위해서 source를 포함시키지 않고, 오직 doc value 필드에만 의존하게 할 수 있다.

  ```bash
  # 인덱스 생성
  PUT test
  {
    "mappings": {
      "properties": {
        "comments": {
          "type": "nested"
        }
      }
    }
  }
  
  # 문서 색인
  PUT test/_doc/1?refresh
  {
    "title": "Test title",
    "comments": [
      {
        "author": "kimchy",
        "text": "comment text"
      },
      {
        "author": "nik9000",
        "text": "words words words"
      }
    ]
  }
  
  # 데이터 검색
  GET test/_search
  {
    "query": {
      "nested": {
        "path": "comments",
        "query": {
          "match": { "comments.text": "words" }
        },
        "inner_hits": {
          "_source": false,
          "docvalue_fields": [	// docvalue_fields를 설정
            "comments.text.keyword"
          ]
        }
      }
    }
  }
  ```



- 계층적 nested object 필드와 inner hits

  - nested 필드가 계층적으로  매핑되었다면 각각의 계층은 온점(`.`)을 통해서 접근이 가능하다.
  - 만일 nested 필드 내부의 특정 계층을 바로 반환받고 싶다면 아래와 같이 하면 된다.
    - 쿼리에 inner hits를 넣어주면 상위 doucment가 검색되게 한 계층이 검색 결과와 함께 나오게 된다.

  ```bash
  # 인덱스 생성
  PUT test
  {
    "mappings": {
      "properties": {
        "comments": {
          "type": "nested",
          "properties": {
            "votes": {
              "type": "nested"
            }
          }
        }
      }
    }
  }
  
  # 데이터 색인
  PUT test/_doc/1?refresh
  {
    "title": "Test title",
    "comments": [
      {
        "author": "kimchy",
        "text": "comment text",
        "votes": []
      },
      {
        "author": "nik9000",
        "text": "words words words",
        "votes": [
          {"value": 1 , "voter": "kimchy"},
          {"value": -1, "voter": "other"}
        ]
      }
    ]
  }
  
  # 검색
  GET test/_search
  {
    "query": {
      "nested": {
        "path": "comments.votes",
          "query": {
            "match": {
              "comments.votes.voter": "kimchy"
            }
          },
          "inner_hits" : {}
      }
    }
  }
  ```



- Parent/child inner hits

  - Parent/child `inner_hits`는 child/parent를 반환 결과에 포함시키기 위해 사용한다.
  - 예시
    - `has_child` 쿼리는 쿼리와 일치하는 child documents의 parent doucment를 반환한다.
    - `inner_hits`를 사용하면 어떤 child documents가 일치하여 해당 parent document가 반환 된 것인지 알 수 있다.

  ```bash
  PUT test
  {
    "mappings": {
      "properties": {
        "my_join_field": {
          "type": "join",
          "relations": {
            "my_parent": "my_child"
          }
        }
      }
    }
  }
  
  PUT test/_doc/1?refresh
  {
    "number": 1,
    "my_join_field": "my_parent"
  }
  
  PUT test/_doc/2?routing=1&refresh
  {
    "number": 1,
    "my_join_field": {
      "name": "my_child",
      "parent": "1"
    }
  }
  
  GET test/_search
  {
    "query": {
      "has_child": {
        "type": "my_child",
        "query": {
          "match": {
            "number": 1
          }
        },
        "inner_hits": {}    
      }
    }
  }
  ```



## search after(pagination)

- Elasticsearch의 pagination
  - 방법은 다음과 같은 것들이 있다.
    - `from`, `size`를 활용한 방법.
    - search after를 활용하는 방법.
    - scroll api를 활용하는 방법.
  - 위 셋 중 ES에서 추천하는 방법은 searach after+pit를 활용하는 것이다.
    - `from`, `size`의 경우 두 값의 합이 10000을 넘을 수 없다. 즉 최대 10000건의 데이터만 pagination이 가능하다.
    - scroll api의 경우 7버전 이전까지는 ES가 추천하는 방법이었으나 7버전부터는 추천하지 않는다.
    - searach after 역시 page jump(e.g from page 1 to 5)를 할 수 있는 방법이 없다는 문제가 있다.
  - `from`, `size`의 경우 ES 설정을 변경하여 10000개 이상도 가능하게 할 수 있지만 권장되지 않는다.
    - `index.max_result_window` 설정을 변경하면 된다.



- Point in Time(PIT)

  - PIT는 동일한 시점에 대해서 서로 다른 검색을 하기 위해서 사용된다.
  - search_after를 정확히 사용하기 위해서는 PIT도 함께 사용해야 한다.
    - PIT를 활용하지 않고 search after를 사용할 경우 pagination을 하는 중에 문서의 추가나 삭제 등으로 refresh가 발생하면 순서가 보장되지 않는다.
    - 또한 PIT를 검색에 활용할 때 자동으로 `_shard_doc`이라는 필드가 tiebreak(동점일 때 승자를 정하는 것, 즉 이 경우 정렬시 동일한 점수일 때 순서를 정하는 것)를 위해 포함되게 된다(기본값은 오름차순).
    - `_shard_doc`은 각 문서마다 고유하므로, 추가적인 tiebreak이 필요 없다.
    - 만일 PIT없이 search_after를 사용하려 한다면 반드시 별도의 tiebreaker를 설정해줘야 하며, 그렇지 않을 경우 일부 문서가 누락되거나 중복되어 나올 수 있다.
  - ES에서 검색은 기본적으로 검색 대상 인덱스의 가장 최근 상태에 행해진다.
    - 예를 들어 검색 중에 데이터가 들어온다 하더라도 해당 데이터는 검색 결과에 영향을 미치지 못한다.
    - 즉 검색 직전에 인덱스의 상태를 사진을 찍어 놓고 해당 사진의 상태를 기반으로 검색을 수행하는 것이다.
    - 이 시점을 PIT라 부른다.
  - 생성하기
    - `_pit` api를 통해 생성한다.
    - PIT를 생성할 인덱스명과  `keep_alive` 쿼리 파라미터가 필요하다.

  ```bash
  POST /my-index-000001/_pit?keep_alive=1m
  ```

  - 응답
    - pit의 고유 id가 반환된다.

  ```json
  {
    "id" : "u5mzAwELc2FtcGxlLWRhdGEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAWUk9CSkRNY3FTT1M3NFdIdFNhak1aUQAAAAAAABPZLhZHYnNneFNwZVFUbXNsVmZLU2ZpQmx3AAEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAA"
  }
  ```

  - 활용하기
    - 검색시에 request body에 `pit`을 추가한다.
    - `keep_alive`를 주면 해당 시간만큼 `keep_alive` 시간이 연장된다.

  ```json
  POST /_search 
  {
      "size": 100,
      "query": {
          "match" : {
              "title" : "elasticsearch"
          }
      },
      "pit": {
  	    "id":  "u5mzAwELc2FtcGxlLWRhdGEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAWUk9CSkRNY3FTT1M3NFdIdFNhak1aUQAAAAAAABPZLhZHYnNneFNwZVFUbXNsVmZLU2ZpQmx3AAEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAA", 
  	    "keep_alive": "1m"  
      }
  }
  ```

  - 아래 요청을 통해 얼마나 많은 pit가 생성되어 있는지 확인 가능하다.
    - `indices.search.open_contexts`에서 볼 수 있다.

  ```bash
  GET /_nodes/stats/indices/search
  ```

  - 삭제하기

  ```bash
  DELETE /_pit
  {
      "id" : "u5mzAwELc2FtcGxlLWRhdGEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAWUk9CSkRNY3FTT1M3NFdIdFNhak1aUQAAAAAAABPZLhZHYnNneFNwZVFUbXNsVmZLU2ZpQmx3AAEWd1BSSXdMa2VReTJyMWt3dUxSakRVZwAA"
  }
  ```



- 정렬하기

  - PIT 생성

  ```bash
  POST /my-index-000001/_pit?keep_alive=1m
  ```

  - 검색하기
    - PIT가 index 기반으로 생성되기 때문에 요청 url에 index name이 포함되지 않는다.
    
    - 상기했듯 PIT를 활용하는 모든 검색은 _shard_doc라는 필드가 tiebreaker로 들어가는데, 내림차순으로 정렬하고자하면 아래와 같이 직접 추가한다.
    
      정렬 대상 field가 date 타입일 경우  format을 추가 가능하다. foramt은 아래와 같이 직접 패턴을 넣어도 되고, ES에서 [미리 정의한 format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html)을 사용해도 된다.
  
  ```json
  GET /_search
  {
    "size": 10000,
    "query": {
      "match" : {
        "user.id" : "elkbee"
      }
    },
    "pit": {
      "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
      "keep_alive": "1m"
    },
    "sort": [ 
      {"@timestamp": {"order": "asc", "format":"yyyy-MM-dd'T'HH:mm:ss"}}
      {"_shard_doc":"desc"}
    ]
  }
  ```
  
  - 응답
    - `sort` 부분에 마지막으로 hits된 문서의 sort 값들이 온다.
    - search after 검색시에 이 값들을 사용하면 된다.
  
  ```json
  {
    "pit_id" : "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
    "took" : 17,
    "timed_out" : false,
    "_shards" : ...,
    "hits" : {
      "total" : ...,
      "max_score" : null,
      "hits" : [
        ...
        {
          "_index" : "my-index-000001",
          "_id" : "FaslK3QBySSL_rrj9zM5",
          "_score" : null,
          "_source" : ...,
          "sort" : [                                
            "2021-05-20T05:30:04.832Z",
            4294967298                              
          ]
        }
      ]
    }
  }
  ```

  - search after 검색하기
    - 응답의 `sort`에 왔던 값들을 `search_after` 부분에 추가해준다.
  
  ```json
  GET /_search
  {
    "size": 10000,
    "query": {
      "match" : {
        "user.id" : "elkbee"
      }
    },
    "pit": {
      "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
      "keep_alive": "1m"
    },
    "sort": [
      {"@timestamp": {"order": "asc", "format": "strict_date_optional_time_nanos"}}
    ],
    "search_after": [                                
      "2021-05-20T05:30:04.832Z",
      4294967298
    ]                 
  }
  ```



## Fuzzy query

- term과 유사한 token을 포함하고 있는 documents를 반환하는 query

  -  두 단어 사이의 Levenshtein distance를 통해 두 term이 유사한지 아닌지 판단한다.
  -  오타 교정 기능, 혹은 자동 완성 기능을 구현하기 위해 사용한다.
  -  옵션들
     - `field`(required): 검색 하고자 하는 field를 입력한다.
     - `value`(required): 검색하고자 하는 term을 입력한다.
     - `fuzziness`: Levenshtein distance 값을 입력한다. 0, 1, 2, AUTO 중 하나의 값을 받는다. 3 이상을 줘도 error는 나지 않으나, 제대로 동작하지는 않는다.
     - `max_expansions`: 생성할 후보군의 최대 개수를 설정한다.
     - `prefix_length`: 후보군을 생성할 때, term의 첫 번째 문자부터 몇 번째 글자까지 변경 없이 fix 시킬 것인지를 설정한다.
     - `transpositions`: Levenshtein distance를 계산할 때, 인접한 두 문자의 교환(ab -> ba)도 거리로 계산할 것인지 설정한다.
     - `rewrite`: [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-term-rewrite.html) 참조
  -  `fuzziness`는 `AUTO[:low,high]`와 같이 설정이 가능하다.
     - 기본값은 `AUTO:3,6`이다.
     - term의 길이가 low이하면 반드시 matching되어야 한다.
     - term의 길이가 lowd 초과, high 미만이면 1번의 edit이 허용된다.
     - term의 길이가 high 이상이면 2번의 edit이 허용된다.
  -  3 이상의 edit distance를 지원하지 않는 이유
     - Fuzzy query의 기본적인 목적은 간단한 typing 실수를 찾아내기 위한 것이다.
     - 3자 이상이 틀릴 경우 사람이 쉽게 인식할 수 있으므로 3자 이상은 지원하지 않는다.
  -  후보 term들을 선정하는 방식
     - Elasticsearch는 잘못 입력된 term을 가지고`prefix_length`에서 고정된 문자열들을 가지고 `fuzziness`만큼의 edit이 발생한 term들을 `max_expansions` 값 만큼 생성한다.
  -  예시
  
  ```json
  // GET /_search
  {
    "query": {
      "fuzzy": {
        "user.id": {
          "value": "ki",
          "fuzziness": "AUTO",
          "max_expansions": 50,
          "prefix_length": 0,
          "transpositions": true,
          "rewrite": "constant_score"
        }
      }
    }
  }
  ```
  
  - `match_phrase_prefix` query와 함께 사용하여 자동완성에 사용하기도 한다.
  
  ```json
  // GET /_search
  {
    "query": {
      "bool": {
        "should": [
          {
            "multi_match": {
              "query": "worl",
              "fields": ["title"],
              "fuzziness": 1
            }
          },
          {
            "multi_match": {
              "type": "phrase_prefix", 
              "query": "worl",
              "fields": ["title"]
            }
          }
        ]
      }
    }
  }
  ```



- Fuzzy query의 동작 방식

  - 동작 방식
    - Fuzzy query는 입력으로 들어온 term을 analyzer를 사용하여 token 단위로 분해한다.
    - 분해된 각 token들가지고 색인된 token들 중에서 `fuzziness`에 설정된 edit distance 내에 속하는 token들을 `max_expansions`만큼 찾는다.
    - 해당 token들을 가지고 검색한 결과를 반환한다.
  - Index 생성
    - 아래와 같이 index를 생성한다.

  ```json
  // PUT korean-fuzzy-test
  {
      "settings": {
          "analysis": {
              "tokenizer": {
                  "my_nori_tokenizer": {
                      "type": "nori_tokenizer"
                  }
              },
              "analyzer": {
                  "my_nori_analyzer": {
                      "type": "custom",
                      "tokenizer": "my_nori_tokenizer"
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "text": {
                  "type": "text",
                  "analyzer": "my_nori_analyzer"
              }
          }
      }
  }
  ```

  - 문서 2건을 색인한다.
    - 한글은 ["한글"], 스마트폰은 ["스마트", "폰"]와 같이 token이 생성된다.

  ```json
  // PUT korean-fuzzy-test/_doc/1
  {
      "text":"한글"
  }
  
  // PUT korean-fuzzy-test/_doc/2
  {
      "text":"스마트폰"
  }
  ```

  - 검색을 실행한다.
    - 결과를 보면 1, 2번 문서가 모두 검색되는 것을 확인할 수 있다.

  ```json
  // GET korean-fuzzy-test/_search
  {
      "query": {
          "match": {
              "text": {
                  "query": "한굴",
                  "fuzziness": "1"
              }
          }
      }
  }
  ```

  - 한글이 검색된 이유
    - 검색어로 입력된 "한굴"을 형태소 분석하면 ["한", "굴"]로 token이 생성된다.
    - "한", "굴"에 1 edit distance만으로 만들 수 있는 token을 1, 2번 문서의 token들 중에 찾는다.
    - "한" token에 1번의 삽입 연산을 통해 "한글"을 만들 수 있으므로, "한글"로 query를 다시 작성하여 검색을 실행한다.
    - 따라서 "한글"이라는 token을 가진 1번 문서가 검색이 된다.
  - 스마트폰이 검색된 이유
    - 검색어로 입력된 "한굴"을 형태소 분석하면 ["한", "굴"]로 token이 생성된다.
    - "한", "굴"에 1edit distance만으로 만들 수 있는 token을 1, 2번 문서의 token들 중에 찾는다.
    - "한", "굴" 모두 한 번의 수정 연산을 통해 "폰"을 만들 수 있으므로 "폰"으로 query를 다시 작성하여 검색을 실행한다.
    - 따라서 "폰"이라는 token을 가진 2번 문서가 검색이 된다.



- Fuzzy query는 개별 token을 대상으로 적용된다.

  - 아래와 같이 문서를 색인하고

  ```json
  // PUT fuzzy-test/_doc/1
  {
    "text":"Hello John"
  }
  ```

  - 아래와 같이 검색을 해보면 1번 문서가 검색이 되는 것을 확인할 수 있다.
    - `operator`를 `and`로 줬으므로 잘 못 입력된 "hellp"와 "Johm"이 모두 교정 된 후 matching되어야 1번 문서가 검색된다.
    - 그런데, 아래 문서를 대상으로 검색을 해보면 1번 문서가 검색이 되는 것을 확인할 수 있다.

  ```json
  // GET fuzzy-test/_search
  {
      "query": {
          "match": {
              "text":{
                  "query":"Hellp, Johm",
                  "fuzziness": 1,
                  "operator": "and"
              }
          }
      }
  }
  ```

  - Profile을 통해 아래와 같이 두 token이 모두 오타 교정이 된 채로 검색이 실행되는 것을 확인할 수 있다.

  ```json
  "+(text:hello)^0.8 +(text:john)^0.75"
  ```

  - `fuzziness` 값 중 `AUTO:[low],[high]`에서 low, high의 값은 전체 term이 아닌 개별 token의 길이를 가지고 계산하는 것이다.



- Fuzzy query와 한글

  - Fuzzy query는 기본적으로 영문과 같은 언어를 위해 고안 된 것이다.
    - 따라서 초성, 중성, 종성으로 구분 된 한글에는 적절하지 않을 수 있다.
    - 한글의 경우 초성, 중성, 종성 단위로 적용되지 않고, 음절 단위로 적용된다.
  - 아래와 같이 한글 문서를 색인하기 위한 index를 생성한다.

  ```json
  // PUT korean-fuzzy-test
  {
      "settings": {
          "analysis": {
              "analyzer": {
                  "my_nori_analyzer": {
                      "type": "custom",
                      "tokenizer": "nori_tokenizer"
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "text": {
                  "type": "text",
                  "analyzer": "my_nori_analyzer"
              }
          }
      }
  }
  ```

  - 한글 문서를 색인한다.

  ```json
  // PUT korean-fuzzy-test/_doc/1
  {
      "text":"한글"
  }
  ```

  - `fuzziness`를 1로 주고 "헉글"이라는 잘 못 입력한 term으로 검색한다.
    - "헉글"이 "한글"이 되기 위해서는 `"헉글"→ "학글"`, `"학글" → "한글"`와 같이 2번의 편집이 필요하다.
    - 그러나 아래에서 edit distance를 1로 줬음에도 정상적으로 검색이 되는 것을 확인할 수 있다.

  ```json
  // GET korean-fuzzy-test/_search
  {
      "query": {
          "match": {
              "text": {
                  "query": "헉글",
                  "fuzziness": "1"
              }
          }
      }
  }
  ```





# Exist query

- exist query

  - 특정 field에 색인 된 값이 존재하는 document들을 검색하는 query
    - 값이 null이거나 빈 배열(`[]`)이면 값이 없는 것으로 판단한다.
    - 그러나 빈 문자열, `"-"`, null과 다른 값을 함께 가진 배열(e.g. `[null, "foo"]`), custom_null value 등은 값이 있는 것으로 판단한다.

  ```json
  // GET /_search
  {
    "query": {
      "bool": {
        "must_not": {
          "exists": {
            "field": "user.id"
          }
        }
      }
    }
  }
  ```





# Nested query

- Nested field를 검색하기 위한 query이다.

  - nested field는 object field와는 다른 검색 식으로 검색해야한다.
    - 예를 들어 아래와 같이 검색할 수 없다.

  ```json
  PUT nested_test
  {
    "mappings": {
      "properties": {
        "human": {
          "type": "nested",
          "properties": {
            "name": {
              "type": "text"
            },
            "age": {
              "type": "integer"
            }
          }
        }
      }
    }
  }
  
  PUT nested_test/_doc/1
  {
    "human":{
      "name":"Park",
      "age":28
    }
  }
  
  // 검색 결과가 나오지 않는다.
  GET nested_test/_search
  {
    "query": {
      "match": {
        "human.name": "park"
      }
    }
  }
  ```

  - `nested` query는 root parent document를 반환한다.
    - nested query는 기본적으로 중첩되어 있는 모든 필드가 개별 문서로 색인된다.
    - 따라서 match 등의 일반적인 query로는 검색과 nested field를 포함하고 있는 root parent document의 반환이 불가능하다.

  - Nested field에 script query를 사용할 경우 nested document의 doc value에만 접근이 가능하며, parent 또는 root document에는 접근이 불가능하다.



- nested query 사용하기

  - nested filed를 가진 index를 생성하고 data를 색인한다.

  ```json
  PUT nested_test
  {
    "mappings": {
      "properties": {
        "human": {
          "type": "nested",
          "properties": {
            "name": {
              "type": "text"
            },
            "age": {
              "type": "integer"
            }
          }
        }
      }
    }
  }
  
  PUT nested_test/_doc/1
  {
    "human":{
      "name":"Park",
      "age":28
    }
  }
  ```

  - nested query로 검색한다.

  ```json
  GET nested_test/_search
  {
    "query": {
      "nested": {
        "path": "human",
        "query": {
          "match": {
            "human.name": "park"
          }
        }
      }
    }
  }
  ```



- Options
  - path(required)
    - Nested object의 path를 입력한다.
  - query(required)
    - path에서 실행할 query로 실행할 실제 query를 입력한다.
  - score_mode
    - nested query가 반환할 root parent document의 점수 계산 방식을 설정한다.
    - avg(default), max, min, none, sum 등으로 설정이 가능하다.
  - ignore_unmapped
    - mapping되지 않은 path를 무시할지 여부를 설정한다.
    - 기본 값은 false이며, true로 줄 경우 mapping에 없는 filed를 path에 입력해도 error를 발생시키지 않는다.



- must_not query를 사용할 때 주의할 점

  - 아래와 같은 데이터가 있다고 할 때

  ```json
  PUT my-index
  {
    "mappings": {
      "properties": {
        "comments": {
          "type": "nested"
        }
      }
    }
  }
  
  PUT my-index/_doc/1?refresh
  {
    "comments": [
      {
        "author": "kimchy"
      }
    ]
  }
  
  PUT my-index/_doc/2?refresh
  {
    "comments": [
      {
        "author": "kimchy"
      },
      {
        "author": "nik9000"
      }
    ]
  }
  
  PUT my-index/_doc/3?refresh
  {
    "comments": [
      {
        "author": "nik9000"
      }
    ]
  }
  ```

  - 아래의 쿼리는 1, 2번 document를 반환한다.
    - 2번에 `"author": "nik9000"`가 있음에도 2번 document가 반환되는 이유는, 또 다른 nested object인 `"author": "kimchy"`가 match 되었기 때문이다.
    - 즉, `"author": "nik9000"`는 match되지 않았지만, `"author": "kimchy"`가 match 되었기에 root parent document가 반환된 것이다.

  ```json
  POST my-index/_search
  {
    "query": {
      "nested": {
        "path": "comments",
        "query": {
          "bool": {
            "must_not": [
              {
                "term": {
                  "comments.author": "nik9000"
                }
              }
            ]
          }
        }
      }
    }
  }
  ```



## inner hits

- `nested` query, `has_child` query, `has_parent` 쿼리 등 중첩된 검색할 때 활용할 수 있는 옵션이다.

  - 기본적으로 `nested` query는 match된 nested document를 반환하는 것이 아니라, 해당 document의 root parent document를 반환한다.
  - 따라서 어떤 nested document가 match된 것인지는 확인할 수 있는 방법이 없는데, `inner_hits`를 사용하면 어떤 nested document들이 match된 것인지 확인이 가능하다.
  - 예를 들어 위에서 살펴본 [must_not query를 사용할 때 주의할 점]의 query에 `inner_hits`를 추가하여 아래와 같이 검색이 가능하다.
    - `inner_hits`를 통해 어떤 nested document가 match된 것인지를 확인할 수 있다.

  ```json
  POST my-index/_search
  {
    "query": {
      "nested": {
        "inner_hits": {}
        "path": "comments",
        "query": {
          "bool": {
            "must_not": [
              {
                "term": {
                  "comments.author": "nik9000"
                }
              }
            ]
          }
        }
      }
    }
  }
  ```

  - 그 결과는 다음과 같다.

  ```json
  // ...
  "hits" : {
      // ...
      "hits" : [
        {
          "_index" : "my-index",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.0,
          "_source" : {
            "comments" : [
              {
                "author" : "kimchy"
              }
            ]
          },
          "inner_hits" : {
            "comments" : {
              "hits" : {
                "total" : {
                  "value" : 1,
                  "relation" : "eq"
                },
                "max_score" : 0.0,
                "hits" : [
                  {
                    "_index" : "my-index",
                    "_type" : "_doc",
                    "_id" : "1",
                    "_nested" : {
                      "field" : "comments",
                      "offset" : 0
                    },
                    "_score" : 0.0,
                    "_source" : {
                      "author" : "kimchy"
                    }
                  }
                ]
              }
            }
          }
        },
        {
          "_index" : "my-index",
          "_type" : "_doc",
          "_id" : "2",
          "_score" : 0.0,
          "_source" : {
            "comments" : [
              {
                "author" : "kimchy"
              },
              {
                "author" : "nik9000"
              }
            ]
          },
          "inner_hits" : {
            "comments" : {
              "hits" : {
                "total" : {
                  "value" : 1,
                  "relation" : "eq"
                },
                "max_score" : 0.0,
                "hits" : [
                  {
                    "_index" : "my-index",
                    "_type" : "_doc",
                    "_id" : "2",
                    "_nested" : {
                      "field" : "comments",
                      "offset" : 0
                    },
                    "_score" : 0.0,
                    "_source" : {
                      "author" : "kimchy"
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }
  ```



- Options
  - `from`, `size`, `sort` 등의 옵션을 사용 가능하다.
  - `name` 옵션으로 반환 받을 `inner_hits`의 이름을 설정 가능하다.
  - 그 밖의 옵션은 [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/inner-hits.html#inner-hits-options)참조



# 검색 관련 옵션

- track_total_hits
  - 실제 문서 수가 1만건을 넘더라도 search request의 응답으로 온 `total.value`의 값은 최대 10000이다.
    - 이는 검색 순간에 일치한 모든 문서를 전부 count하지 않고는 정확한 계산이 불가능하기 때문이다.
    - 따라서 ES에서는 검색 속도를 높이기 위해서 전부 count하는 대신 10000개만 count하는 방식을 사용한다.
  - 검색시에 request body에 `track_total_hits` 값을 true로 주면 실제 일치하는 모든 문서를 count한다.
  - boolean 값이 아닌 integer도 줄 수 있는데, 해당 숫자 만큼만 count한다.



- document의 `_version` field 로 정렬하기

  - `_version` 필드는 색인된 필드가 아니라 `sort`의 대상 필드가 될 수 없다.
  - 그러나 painless script를 사용하면 sort가 가능하다.

  ```json
  // GET <index>/_search
  {
    "query": {
      "match": {
        "<field>": <term>
      }
    },
    "sort": {
      "_script": {
        "type": "number",
        "script": {
          "lang": "painless",
          "source": "doc['_version']"
        },
        "order": "asc"
      }
    }
  }
  ```

