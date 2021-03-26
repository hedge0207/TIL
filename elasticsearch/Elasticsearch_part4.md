# 분석 엔진으로 활용하기

- Elastic Stack이란
  - Elastic Stack은 로그를 수집, 가공하고 이를 바탕으로 분석하는 데 사용되는 플랫폼을 의미한다.
    - 이전에는 Elastic Stack을 ELK Stack이라고 불렀다.
    - Elastic Stack은 가급적 모든 구성 요소의 버전을 통일시키는 것이 좋다.
  - Elastic Stack은 아래와 같다.
    - 로그를 전송하는 Filebeat
    - 전송된 로그를 JSON 형태의 문서로 파싱하는 Logstash
    - 파싱된 문서를 저장하는 Elasticsearch
    - 데이터를 시각화 할 수 있는 kibana
  - Filebeat
    - 지정된 위치에 있는 로그 파일을 읽어서 Logstash 서버로 보내주는 역할을 한다.
    - Filebeat은 로그 파일을 읽기만 하고 별도로 가공하지 않기 때문에, 로그 파일의 포맷이 달라지더라도 별도의 작업이 필요치 않다.
    - 로그 파일의 포맷이 달라지면 로그 파일을 실제로 파싱하는 Logstash의 설정을 바꿔주면 되기 때문에 Filebeat과 Logstash의 역할을 분명하게 나눠서 사용하는 것이 확장성이나 효율성 면에서 좋다.
  - Logstash
    - Filebeat으로부터 받은 로그 파일들을 룰에 맞게 파싱해서 JSON 형태의 문서로 만드는 역할을 한다.
    - 하나의 로그에 포함된 정보를 모두 파싱할 수도 있고, 일부 필드만 파싱해서 JSON 문서로 만들 수도 있다.
    - 파싱할 때는 다양한 패턴을 사용할 수 있으며 대부분 **grok 패턴**을 이용해서 파싱 룰을 정의한다.
    - grok: 비정형 데이터를 정형 데이터로 변경해 주는 라이브러리
  - Elasticsearch
    - Logstash가 파싱한 JSON 형태의 문서를 인덱스에 저장한다.
    - 이 때의 ES는 데이터 저장소 역할을 한다.
    - 대부분의 경우 날짜가 뒤에 붙는 형태로 인덱스가 생성되며 해당 날짜의 데이터를 해당 날짜의 인덱스에 저장한다.
  - Kibana
    - ES에 저장된 데이터를 조회하거나 시각화할 때 사용한다.
    - 데이터를 기반으로 그래프를 그리거나 데이터를 조회할 수 있다.
    - Elastic Stack에서 사용자의 인입점을 맡게 된다.



- Elastic Stack 설치하기
  - 추후 추가(p.251-271)



- Elastic Stack의 이중화
  - Elastic Stack의 어느 한 구성 요소에 장애가 발생하더라도 나머지 요소들이 정상적으로 동작할 수 있도록 이중화하는 작업이 반드시 필요하다.
  - 추후 추가





# 검색 엔진으로 활용하기

## inverted index와 analyzer

- inverted index(역색인)

  - "I am a boy", "You are a girl" 이라는 두 문자열이 있다고 가정한다.
    - 위 두 개의 문자열을 공백을 기준으로 나누면 각각의 문자열은 4개의 단어로 나뉜다.
    - I, am, a, boy
    - you, are, a girl
  - 토큰
    - 위와 같이 나뉜 단어들을 **토큰**이라 부른다. 
    - 토큰을 만들어 내는 과정을 **토크나이징**이라고 한다.
  - 특정한 기준에 의해 나뉜 토큰들은 아래와 같은 형태로 저장되는데 이것을 역색인이라 부른다.

  | Tokens | Documents |
  | ------ | --------- |
  | I      | 1         |
  | am     | 1         |
  | a      | 1, 2      |
  | boy    | 1         |
  | girl   | 2         |
  | you    | 2         |
  | are    | 2         |

  - 위와 같은 역색인이 생성된 상태에서 사용자가 "a boy"라는 문자열을 찾고 싶다고 가정한다.
    - 검색어로 a boy라는 문자열을 입력하면 이 문자열은 공백을 기준으로 a, boy라는 두 개의 토큰으로 나뉜다.
    - 이렇게 나뉜 토큰을 바탕으로 역색인을 검색한다.
    - 두 단어가 모두 포함되어 있는 문서 1번이 검색 결과로 반환된다.
  - 대소문자 구분
    - 검색 결과를 얻기 위해서는 토큰이 대소문자까지 정확하게 일치해야 한다.
    - 역색인에 대문자 I만 존재할 뿐 소문자 i는 존재하지 않는다.
    - 따라서 소문자 i로 검색하면 아무런 검색 결과를 얻지 못한다.



- ES는 어떻게 토크나이징을 하는가

  - ES는 analyze라는 API를 제공한다
    - analyzer에는 토크나이징에 사용할 analyzer를 입력한다.
    - text에는 토크나이징 할 문자열을 입력산다.

  ```bash
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "analyzer":"standard",
  "text":"I am a boy"
  }'
  ```

  - 응답
    - 토크나이징의 결과로 토큰의 배열을 반환한다.
    - 아래 토큰을 보면 대문자 I가 아닌 소문자 i로 토크나이징 된 것을 볼 수 있는데, standard analyzer의 동작 중에 모든 문자를 소문자화하는 과정이 포함되어 있기 때문이다.

  ```json
  {
    "tokens" : [
      {
        "token" : "i",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- analyzer 
  - analyzer는 역색인을 만들어주는 것이다.
    - analyzer는 운영 중에 동적으로 변경할 수 없다. 
    - 따라서 기존 인덱스에 설정한 analyzer를 바꾸고 싶을 때는 인덱스를 새로 만들어서 재색인(reindex)해야 한다.
  - ES의 analyzer는 다음과 같이 구성된다.
    - character filter
    - tokenizer
    - token filter
  - character filter
    - analyzer를 통해 들어온 문자열들은 character filter가 1차로 변형한다.
    - 예를 들어 <, >, ! 등과 같은 의미 없는 특수 문자들을 제거한다거나 HTML 태그들을 제거하는 등 문자열을 구성하고 있는 문자들을 특정한 기준으로 변경한다.
  - tokenizer
    - tokenizer는 일정한 기준(공백이나 쉼표)에 의해 문자열은 n개의 토큰으로 나눈다.
    - analyzer를 구성할 때는 tokenizer를 필수로 명시해야 하며, 하나의 tokenizer만 설정할 수 있다.
    - 반면 character filter와 token filter는 필요하지 않을 경우 기술하지 않거나, 여러 개의 character filter와 token filter를 기술할 수 있다.
  - token filter
    - 토큰을 전부 소문자로 바꾸는 lowercase token filter가 대표적인 token filter이다.



- standard analyzer

  - filter
    - character filter가 정의되어 있지 않다.
    - standard tokenizer가 정의되어 있다.
    - lowercase token filter가 정의되어 있다.
    - stopwords로 지정한 단어가 토큰들 중에 존재 한다면 해당 토큰을 없애는 stop token filte가 존재하지만 기본값으로 비활성화 되어 있다.
  - standard tokenizer 요청
    - `analyzer`가 아닌 `tokenizer`를 입력한다.
    - 아직 token filter를 거치지 않았기에 I가 대문자이다.

  ```json
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "tokenizer":"standard",
  "text":"I am a boy"
  }'
  
  
  {
    "tokens" : [
      {
        "token" : "I",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- custom analyzer

  > https://esbook.kimjmin.net/06-text-analysis/6.3-analyzer-1/6.4-custom-analyzer 참고

  - 추후 추가



- analyzer와 검색의 관계

  - analyze의 중요성
    - analyzer를 통해 생성한 토큰들이 역색인에 저장되고, 검색할 때는 이 역색인에 저장된 값을 바탕으로 문서를 찾는다.
    - 따라서 검색 니즈를 잘 파악해서 적합한 analyzer를 설정해야 한다.
  - 테스트 인덱스 생성

  ```bash
  $ curl -XPUT "localhost:9200/books?pretty" -H 'Content-type:application/json' -d '{
  "mappings":{
  "properties":{
  "title":{"type":"text"},
  "content":{"type":"keyword"}
  }
  }
  }'
  ```

  - 테스트 문서 색인

  ```bash
  $ curl -XPUT "localhost:9200/books/_doc/1?pretty" -H 'Content-type:application/json' -d '{
  "title":"Elasticsearch Training Book",
  "content":"Elasticsearch is open source search engine"
  }'
  ```

  - title로 검색하기
    - 정상적으로 검색이 된다.

  ```json
  $ curl "localhost:9200/books/_search?pretty&q=title:Elasticsearch"
  
  {
    "took" : 743,
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
          "_index" : "books",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.6931471,
          "_source" : {
            "title" : "Elasticsearch Training Book",
            "content" : "Elasticsearch is open source search engine"
          }
        }
      ]
    }
  }
  ```

  - content로 검색하기

  ```json
  $ curl "localhost:9200/books/_search?pretty&q=content:Elasticsearch"
  
  {
    "took" : 2,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 0,
        "relation" : "eq"
      },
      "max_score" : null,
      "hits" : [ ]
    }
  }
  ```

  - content 필드는 검색이 정상적으로 이루어지지 않았다.
    - title 필드는 text, content 필드는 keyword 타입으로 정의했다.
    - text 타입의 기본 analyzer는 standard analyzer이고, keyword 타입의 기본 analyzer는 keyword analyzer이다.
    - keyword analyzer는 standard analyzer와는 달리 문자열을 나누지 않고 통으로 하나의 토큰을 구성한다.
    - 즉 역색인에는 "Elasticsearch is open source search engine"라는 토큰만 존재한다.



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
    - 색인된 도큐먼트가 크고 결과에서 전체 내용이 필요하지는 않을 때 사용한다.
    - 이 옵션을 사용하려면, 색인 매핑에서 _source 필드를 비활성화하지 않아야 한다.
  - sort
    - 기본 정렬은 도큐먼트 점수에 따른다.
    - 점수 계산이 필요 없거나 동일 점수의 다수 도큐먼트가 예상된다면, sort를 추가해서 원하는 대로 순서를 제어할 수 있다.



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
  - Filter Context
    - Term Level Query라고도 부른다.
    - 검색어가 문서에 존재하는지 여부를 Yes나 No 형태의 검색 결과로 보여준다. 
    - score 값을 가지지 않는다.
  - 둘 사이의 가장 큰 차이점은 analyze를 하는가의 여부이다.



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

  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  "query":{
    "wildcard":{
      "publisher.keyword":"*Media*"
    }
  }
  }'
  ```



## bool query

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
            "descrption": "performance"
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











