# 데이터 검색

## Search API

- 엘라스틱서치에서 검색을 실행할 때 어떤 일이 일어나는가?
  - 가장 기본적인 검색 라우팅 기능인 query_then_fetch를 기준으로 설명한다.
    - 라우팅 기능은 변경이 가능하다.
  - 과정
    - 검색 애플리케이션이 하나의 노드를 선택하고 선택한 노드에 검색 요청을 보낸다.
    - 요청을 받은 노드는 모든 노드의 모든 샤드에 검색 요청을 보낸다.
    - 모든 샤드에서 정렬 및 순위를 매긴 결과로부터 충분한 정보를 수집하면, 오직 반환될 도큐먼트 내용을 담고 있는 샤드만 해당 내용을 반환하도록 요청 받는다.



- search API

  - 모든 search API 검색 요청은 _search REST end point를 사용하고 GET이나 POST 요청 중 하나가 된다.
    - end point는 path라고도 불리며 URL에서 호스트와 포트 이후의 주소를 말한다.
  - 간단한 형태의 URI Search 형태를 제공한다.
  
  ```bash
  /인덱스명/_search?q=쿼리
  ```
  
  - RequestBody Search 형태도 제공한다.
  
  ```bash
  /인덱스명/_search
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
  
  ```bash
  curl "localhost:9200/_all/_search?q=쿼리"
  ```



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
    - _source 필드를 어떻게 반환할 것인가를 명시한다.
    - 기본값은 완전한 _source 필드를 반환하는 것이다.
    - _source 설정으로 반환되는 필드를 걸러낼 수 있다.
    - _source에 필드를 포함시키지 않아도 해당 필드에서 검색은 이루어진다.
    - 색인된 도큐먼트가 크고 결과에서 전체 내용이 필요하지는 않을 때 사용한다.
    - 이 옵션을 사용하려면, 색인 매핑에서 _source 필드를 비활성화하지 않아야 한다.
  - sort
    - 기본 정렬은 도큐먼트 점수에 따른다.
    - 점수 계산이 필요 없거나 동일 점수의 다수 도큐먼트가 예상된다면, sort를 추가해서 원하는 대로 순서를 제어할 수 있다.
  - fields
    - 검색을 실행 할 필드를 지정한다.
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



### Query Context

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

  ```bash
  $ curl 'localhost:9200/인덱스명/_search' -H 'Content-Type: application/json' -d '{
  "query": {
    "match_all":{}
  }
  }'
  ```



- mutli_match 쿼리

  - match와 동일하지만 두 개 이상의 필드에 match 쿼리를 날릴 수 있다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query": {
    "multi_match":{
      "query": "텀",
      "fields": ["필드1", "필드2"] 
    }
  }
  }'
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



### Filter Context

- term 쿼리

  - ES에서 term은 검색어를 말한다.
  - 역색인에 있는 토큰들 중 정확하게 일치하는 값을 찾는다.
    -  match 쿼리와 달리 검색어를 analyze하지 않는다.
    - analyze를 하지 않기 때문에 당연히 대소문자를 구분한다.
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
  - 예제

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query":{
    "term":{
      "필드": ["텀1","텀2"]
    }
  },
  "_source":["name","tags"]
  }'
  ```

  - 도큐먼트에서 최소 개수의 텀 일치를 강제하려면 `minimum_should_match` 파라미터를 설정한다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query":{
    "term":{
      "필드": ["텀1","텀2"],
      "minimum_should_match":2
    }
  },
  "_source":["name","tags"]
  }'
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
  | filter   | O                                           | X        | O    |
  | should   | O                                           | O        | X    |
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

  - 쿼리에 일치하지 않눈 문서를 검색하는 쿼리
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

  - `minimum_should_match` 옵션을 제공한다
    - should 항목에 포함된 쿼리 중 적어도 설정된 수치만큼의 쿼리가 일치할 때 검색 결과를 보여주는 옵션이다.
    - should절을 사용할 때 꼭 써야만 하는 옵션은 아니다.
    - 양수일 경우 그 이상의 쿼리가, 음수일 경우 총 쿼리 개수에서 음수를 뺀 만큼의 쿼리가 일치해야 한다.
    - 퍼센트로 설정하는 것도 가능하다.
    - 설정해 주지 않으면 `must` 혹은 `must_not`과 함께 사용할 경우에는 0, should만 사용할 경우에는 1이 default 값이다.
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





### Function score query

- Function score query

  - 쿼리를 통해 검색 된 문서들의 score를 조정할 수 있게 해준다.
  - score funcion이 score를 계산하는데 많은 자원을 소모하고, 문서 집합의 점수를 계산하는데 필요한 자원이 충분한 경우에 유용할 수 있다.
  - function을 하나만 사용한 예시

  ```bash
  GET /_search
  {
    "query": {
      "function_score": {
        "query": { "match_all": {} },
        "boost": "5",
        "random_score": {}, 
        "boost_mode": "multiply"
      }
    }
  }
  ```

  - 두 개 이상의 function을 사용하는 것도 가능하다.
    - 이 경우 document가 주어진 filter와 일치할 때만 해당 함수에서 정의 된 방식으로 score를 계산한다.
    - 만일 아무런 필터도 주지 않을 경우 `match_all`을 준 것과 동일한 결과가 나오게 된다.

  ```bash
  GET /_search
  {
    "query": {
      "function_score": {
        "query": { "match_all": {} },
        "boost": "5", 
        "functions": [
          {
            "filter": { "match": { "test": "bar" } },
            "random_score": {}, 
            "weight": 23
          },
          {
            "filter": { "match": { "test": "cat" } },
            "weight": 42
          }
        ],
        "max_boost": 42,
        "score_mode": "max",
        "boost_mode": "multiply",
        "min_score": 42
      }
    }
  }
  ```

  - 아래와 같은 score function을 제공한다.
    - script_score
    - weight
    - random_score
    - field_value_factor
    - decay functions: gauss, linear, exp



- 파라미터
  - `weight`
    - 점수는 각기 다른 척도로 계산 될 수 있으며, 때때로 점수에 각기 다른 함수를 적용하길 원할 수 있다.
    - 따라서 이를 위해 각 함수가 계산하는 점수를 조정하기 위해 `weight`를 사용한다.
    - `weigth`는 함수마다 하나씩 선언되며, 각각의 `weight`는 함수가 계산한 점수와 곱해진다.
    - 만일 함수의 선언 없이 `weigth`만 정의할 경우, `weight`는 `weight` 그 자체를 반환하는 함수처럼 동작한다.
  - `score_mode`
    - function에 의해 계산된 score 값들이 어떻게 결합될지를 결정하는 파라미터
    - 만일 scocre_mode가 avg로 설정되었을 경우에, 점수들은 weighted average로 결합된다.
    - 예를 들어 두 개의 함수가 각기 1, 2를 점수로 반환하였고, 각각의 weight가 3, 4로 주어졌다면, 점수는 `(1*3+2*4)/2`가 아닌`(1*3+3*4)/(3+4)`로 계산된다.
    - multifly: 점수를 곱한다(기본값).
    - sum: 점수를 합산한다.
    - avg: 점수의 평균을 낸다.
    - first: filter와 일치하는 첫 번째 함수를 적용한다.
    - max: 점수들 중 최댓값을 사용한다.
    - min: 점수들 중 최솟값을 사용한다.
  - `max_boost`
    - 계산된 점수의 최댓값을 설정할 수 있다.
    - 만일 계산 된 점수가 `max_boost`에 설정한 값 보다 높을 경우  점수는 `max_boost`에 설정한 값이 되게 된다.
    - 기본 값은 FLT_MAX(실수 형식으로 포함할 수 있는 최댓값)이다.
  - `boost_mode`
    - 계산된 점수가 query의 점수와 어떻게 결합 될 것인지를 결정하는 파라미터
    - multifly: 쿼리 score와 function score를 곱한다(기본값).
    - replace: function score를 사용한다.
    - sum: 쿼리 score와 function score를 더한다.
    - avg: 쿼리 score와 function score의 평균을 낸다.
    - max: 점수들 중 최댓값을 사용한다.
    - min: 점수들 중 최솟값을 사용한다.
  - `min_score`
    - 기본적으로, 조정 된 점수는 어떤 문서가 match될지에 영향을 주지 않는다.
    - `min_score`는 특정 점수를 충족하지 못하는 문서를 제외시킨다. 
    - `min_score`가 동작하려면 쿼리에서 반환 된 모든 문서에 점수를 매긴 다음 하나씩 필터링 해야 한다.



- script_score

  - 다른 쿼리를 래핑할 수 있게 해주고, 스크립트 표현식을 통해 문서의 숫자 필드 값을 활용하여 계산한 값으로 scoring을 할 수 있게 해준다.
  - `_score` 스크립트 파라미터를 사용하여 래핑 된 쿼리를 기반으로 점수를 검색 할 수 있다.
  - `custom_score` 쿼리와 달리, 쿼리의 score는 script가 계산 한 score에 곱해지게 된다.
    - 곱하는 것을 원하지 않는다면 `"boost_mode": "replace"`와 같이 설정해주면 된다.
  - 제약사항
    - ES에서 score는 32-bit 부동소수점 형식을 취한다.
    - 만일 script_score에서 이보다 더 정밀하게 계산하려 한다면 ES가 이를 2-bit 부동소수점에 맞게 변환한다.
    - 또한 score에는 음수를 사용할 수 없으며, 음수를 사용 할 경우, 에러가 발생한다.
  - 예시

  ```bash
  GET /_search
  {
    "query": {
      "function_score": {
        "query": {
          "match": { "message": "elasticsearch" }
        },
        "script_score": {
          "script": {
            "params": {
              "a": 5,
              "b": 1.2
            },
            "source": "params.a / Math.pow(params.b, doc['my-int'].value)"
          }
        }
      }
    }
  }
  ```



- `weight`

  - weight를 score에 곱한 score를 얻기 위해 사용한다.
    - 반드시 float 값을 줘야 한다.
  - 특정 쿼리에 설정 한 부스트 값은 정규화 되는 반면, weight를 통해 곱해진 점수는 정규화 되지 않는다.
  - 예시

  ```bash
  "weight" : float
  ```



- random

  - 0이상 1미만의 랜덤한 score를 생성한다.
    - 기본값으로 무선적인 값 생성을 위해 내부 Lucene 문서의 id들을 사용한다.
    - 이는 매우 효율적이지만 문서들이 병합에 의해 다시 넘버링 되기 때문에 reproducible하지는 않다.
    - reproducible하게 사용하려면 seed와 field를 주면 된다.
  - 최종 score는 seed, 점수가 매겨질 documents들의 field의 최솟값, 인덱스명과 샤드 id에 기반한 값을 기반으로 계산되므로, 같은 값을 가지고 있지만 다른 인덱스에 저장된 문서들은 각기 다른 값을 갖게 된다. 
    - 그러나, 같은 샤드에 같은 field의 같은 값을 지닌 문서들은 동일한 score를 갖게 된다.
    - 따라서 모든 document들이 고윳값을 가지고 있는 field(주로 `_seq_no` field)를 사용하는 것이 권장된다.
    - 단, 문서에 변경사항이 있으면 `_seq_no`도 변경되므로 점수도 변경되게 된다.
  - 예시

  ```bash
  GET /_search
  {
    "query": {
      "function_score": {
        "random_score": {
          "seed": 10,
          "field": "_seq_no"
        }
      }
    }
  }
  ```



- field_value_factor
  - 





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

  

