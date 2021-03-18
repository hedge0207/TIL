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



# 데이터 검색

## 검색 요청의 구조

- 엘라스틱서치에서 검색을 실행할 때 어떤 일이 일어나는가?
  - 가장 기본적인 검색 라우팅 기능인 query_then_fetch를 기준으로 설명한다.
    - 라우팅 기능은 변경이 가능하다.
  - 과정
    - 검색 애플리케이션이 하나의 노드를 선택하고 선택한 노드에 검색 요청을 보낸다.
    - 요청을 받은 노드는 모든 노드의 모든 샤드에 검색 요청을 보낸다.
    - 모든 샤드에서 정렬 및 순위를 매긴 결과로부터 충분한 정보를 수집하면, 오직 반환될 도큐먼트 내용을 담고 있는 샤드만 해당 내용을 반환하도록 요청 받는다.



- 검색 범위 지정하기

  - 모든 REST 검색 요청은 _search REST 종단점을 사용하고 GET이나 POST 요청 중 하나가 된다.
  - 클러스터 전체를 검색하거나 요청 URL에 색인 이름 또는 타임을 지정해서 범위를 제한할 수 있다.

  

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



- URL 기반 검색 요청

  - URL 기반 검색 요청은 curl로 요청할 때 유용하다.
    - 그러나 모든 검색 기능이 URL 기반 검색을 사용할 수 있는 것은 아니다.
  - form과 size를 활용
    - from으로 결과의 시작 위치를 지정하고, size로 각 결과 페이지의 크기를 지정한다.
    - from이 7이고, size가 3인 경우, ES는 8, 9, 10 번째 결과를 반환한다.
    - 이들 두 개의 파라미터가 전달되지 않았다면 ES는 첫 결과의 시작(0번째)을 기본 값으로 사용하고 응답 결과와 함께 10건의 결과를 전송한다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_search?from=7&size=3'
  ```

  - sort를 활용
    - 일치하는 모든 도큐먼트를 날짜 오름차순으로 정렬한 결과 중 최초 10개를 반환한다.

  ```bash
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



- 본문 기반 검색 요청

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

  - _source로 반환한 필드에서 와일드카드
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

  - 결과에서 순서 정렬
    - 정렬 순서를 지정하지 않으면, ES는 일치한 도큐먼트를 _score 값의 내림차순으로 정렬해서 가장 적합성이 높은(가장 높은 점수를 가진) 도큐먼트 순서로 반환한다.
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



## 쿼리와 DSL 소개

- match 쿼리

  - match 쿼리를 활용하여 일치하는 도큐먼트만 반환하도록 할 수 있다.
    - title 필드에 hadoop이 있는 도큐먼트만 반환한다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -d '{
  "query": {
    "match": {
      "title": "hadoop"
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



- query_string 쿼리

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
      "default_field":"description",
      "query":"텀"
    }
  }'
  ```

  - 이 밖에 다양한 쿼리 스트링 문법이 존재하는데 자세한 내용은 아래 링크 참조

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html



- term 쿼리

  - ES에서 term은 검색어를 말한다.
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

  - term 쿼리와 유사하게, terms 쿼리로 도큐먼트 필드에서 다중 텀으로 검색할 수 있다.
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



- match 쿼리

  - match 쿼리는 검색하려는 필드와 검색하려는 문자열을 포함하는 해시 맵(딕셔너리)이다.
  - 필드 또는 한 번에 모든 필드를 검색하는 _all 필드가 올 수 있다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query": {
    "match":{
      "필드":"텀"
    }
  }
  }'
  ```

  - boolean 쿼리 가능

    - 기본적으로 매치 쿼리는 boolean 기능과 or 연산을 사용한다.

    - 이를 수정할 수 있다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_doc/_search' -H 'Content-Type: application/json' -d '{
  "query": {
    "match":{
      "필드": {
        "query": "텀",
        "operator": "and"
      }
    }
  }
  }'
  ```



- multi_match 쿼리

  - 다중 필드의 값을 검색할 수 있게 해준다.

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

  





