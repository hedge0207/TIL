# Shorts

- 사용자가 입력한 검색어를 Elasticsearch analyzer가 아닌 곳에서 변형하는 것이 옳은가?

  - 일반적으로 사용자가 입력한 검색어가 Elasticsearch로 갈 때까지는 몇 개의 단계를 거치게 된다.
    - 예를 들어, 사용자가 검색 화면에서 검색어를 입력할 경우 web application이 해당 검색어를 받아 server API로 전송한다.
    - Server API는 client의 요청에 따라 Elasticsearch query를 구성하여, Elasticsearch에 검색 요청을 전송한다.
  - 예를 들어 아래와 같은 index가 있다고 가정해보자.

  ```json
  // PUT my-index
  {
      "settings": {
          "analysis": {
              "tokenizer": {
                  "my_nori_tokenizer":{
                      "type":"nori_tokenizer",
                      "user_dictionary_rules":[
                          "K리그"
                      ]
                  }
              },
              "analyzer": {
                  "my_analyzer":{
                      "type": "custom",
                      "tokenizer": "my_nori_tokenizer"
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "content":{
                  "type":"text",
                  "analyzer": "my_analyzer"
              }
          }
      }
  }
  ```

  - 아래와 같은 문서를 색인한다.

  ```json
  // PUT my-index/_doc/1
  {
    "content":"김철수는 K리그 최고의 감독이다."
  }
  ```

  - 사용자가 화면에서 검색어를 입력하고 검색 버튼을 누르면 web application은 API server로 검색 요청를 보낸다.
    - API server의 host를 `my-search-api`라고 가정한다.
    - 문제는 이 때, web application이 사용자가 입력한 검색어에 lowercase를 적용한다는 것이다.

  ```json
  // POST my-search-api/v1/search
  {
      "query":"k리그"
  }
  ```

  - Web application으로부터 검색 요청을 받은 API server는 요청을 Elasticsearch query로 변환해서 Elasticsearch로 검색 요청을 보낸다.

  ```json
  // my-index/_search
  {
      "query":{
          "match":{
              "content":"k리그"
          }
      }
  }
  ```

  - 이 처럼 최종적으로 검색을 수행하는 Elasticsearch가 아닌 web application이나 API server에서 검색어를 수정하면 예상치 못 한 문제가 발생할 수 있다.
    - 위 예시에서 소문자로 변환 된 "k리그"라는 검색어를 입력 받은 Elasticsearch는 ["k", "리그"]로 token을 생성한다.
    - 반면에 검색 대상 문서에 포함된 "K리그"는 사용자 사전에 등록되어 있으므로, ["K리그"]와 같이 token이 생성된다.
    - 따라서 사용자는 분명히 "K리그"로 검색했음에도, "K리그"가 포함 된 문서가 검색되지 않는 문제가 발생한다.

  - Elasticsearch 이외의 곳에서 임의로 검색어를 수정했을 때 발생할 수 있는 가장 큰 문제는, 문제의 원인을 추적하기가 힘들다는 점이다.
    - 만약 위 예시에서 web application과 API server의 개발, 그리고 Elasticsearch index 설정을 모두 한 사람이 했다고 가정해보자.
    - 이 사람은 다행이 자신이 web application에서 API server로 요청을 보낼 때, lowercase를 적용했다는 것을 기억해냈고, 이 부분을 수정하여 문제를 해결했다.
    - 그러나 만약 세 부분을 모두 다른 사람이 개발했다고 가정해보자.
    - 사용자는 "K리그"로 검색을 했고, 분명 "K리그"가 포함된 문서가 있음에도 검색되지 않는다고 문제를 보고한다.
    - 처음에는 Elasticsearch의 analyzer에 문제가 있을 것이라 생각하여, 문제가 보고 된 "K리그"라는 검색어로 Elasticsearch에서 직접 검색을 실행한다.
    - "K리그"로 검색을 하면 정상적으로 검색 결과가 나올 것이므로 Elasticsearch에는 이상이 없는 것으로 판단하고, API server에서 Elasticsearch로 넘기는 query에 이상이 있는지 점검한다.
    - 점검 결과 API server에도 이상이 없는 것으로 밝혀져, 마지막으로 web application을 살펴보고, API server로 요청을 전송할 때 검색어에 lowercase를 적용하는 것을 발견하게 된다.
    - 예시에서는 오직 web application에서만 검색어를 수정한다고 가정했지만, 여러 단계를 거치며 각 단계에서 모두 검색어의 수정을 수행한다면, 검색 결과에 문제가 있을 때 원인을 추적하기가 점점 더 힘들어질 것이다.