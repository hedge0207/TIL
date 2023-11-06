# 구현

## Exact Match

- Test용 data 색인 및 일반 검색 test

  - 아래와 같이 test용 index를 생성한다.

  ```json
  // PUT exact-search-test
  {
    "settings": {
      "analysis": {
        "filter": {
          "synonym": {
            "type": "synonym",
            "synonyms": []
          }
        },
        "tokenizer": {
          "mixed_nori_tokenizer": {
            "type": "nori_tokenizer",
            "decompound_mode": "mixed"
          }
        },
        "analyzer": {
          "nori_analyzer": {
            "type": "custom",
            "tokenizer": "mixed_nori_tokenizer",
            "filter": [
              "synonym"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "title":{
          "type":"text",
          "analyzer": "nori_analyzer",
          "fields": {
            "keyword":{
              "type":"keyword"
            }
          }
        }
      }
    }
  }
  ```

  - Python의 `faker` package를 사용하여 무작위 data를 생성한 후 색인한다.

  ```python
  from faker import Faker
  import json
  
  from elasticsearch import Elasticsearch, helpers
  
  fake = Faker("ko-KR")
  
  bulk_data = []
  for i in range(10000):
      bulk_data.append({
          "_index":"exact-search-test",
          "_source":{"title":fake.catch_phrase()}
      })
  helpers.bulk(Elasticsearch("http://localhost:9200"), bulk_data)
  ```

  - `match` query를 사용하여 "비즈니스 중점적 다이나믹 융합"을 검색하면 아래와 같은 결과가 나온다.
    - 모든 token이 다 들어있는 문서가 가장 위에 노출되긴 하지만, 다른 문서들도 함께 검색된다.

  ```json
  // GET exact-search-test/_search
  {
      "size":3,
      "query": {
          "match": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      }
  }
  
  // response
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "wQPmyooBe-YwzRmmNUVd",
          "_score": 19.411142,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "_1",
          "_score": 19.411142,
          "_source": {
              "title": "다이나믹 비즈니스 중점적 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "5",
          "_score": 16.317135,
          "_source": {
              "title": "새로운 비즈니스 중점적 다이나믹 융합 모델"
          }
      }
  ]
  ```



- 정확히 동일한 검색어가 정확히 동일한 순서로 나와야 하는 기능을 구현해야 하는 경우 아래의 방법들을 사용할 수 있다.

  - Analyzing하지 않은 text를 대상으로 검색하는 방식.
    - 만일 검색 대상 field의 값이 단어 2~3개로 짧을 경우, keyword field를 대상으로 검색하면 된다.
  - `keyword` field를 대상으로 검색

  ```json
  // GET exact-search-test/_search
  {
    "query": {
      "match": {
        "title.keyword": "비즈니스 중점적 다이나믹 융합"
      }
    }
  }
  
  // 응답
  // 검색어와 정확히 일치하는 문서 1개만 검색된다.
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "wQPmyooBe-YwzRmmNUVd",
          "_score": 8.8049755,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      }
  ]
  ```



- 정확히 일치하지는 않는 방식

  > 순서까지 맞는 검색어가 높은 score로 상단에 노출되기만 하면 되는 경우, 아래의 방법들 중 match_phrase를 사용하는 것을 고려해 볼 수 있다.

  - `and` operator를 활용하는 방식.
    - Elasticsearch에서 operator는 다양한 검색식에 들어가는데, 대부분의 경우 default 값은 `or`이다.
    - 이 값을 `and`로 변경할 경우 모든 token이 포함된 문서만 대상으로 검색한다.
    - 아래 결과에 볼 수 있듯이, token의 순서와 무관하게 token이 모두 포함되어 있기만 하면 검색되기에 token의 순서도 일치해야하는 경우 사용할 수 없다.

  ```json
  // GET exact-search-test/_search
  {
      "query": {
          "match": {
              "title": {
                  "query": "비즈니스 중점적 다이나믹 융합",
                  "operator": "and"
              }
          }
      }
  }
  
  // 응답
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "wQPmyooBe-YwzRmmNUVd",
          "_score": 19.483356,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "_1",
          "_score": 19.458757,
          "_source": {
              "title": "다이나믹 비즈니스 중점적 융합"
          }
      }
  ]
  ```

  - `match_phrase` query 사용
    - 입력된 검색어들이 정확히 같은 순서로 배치된 문서들을 대상으로 검색하지만, 아래와 같이 앞이나 뒤에 다른 token이 있어도 검색된다.

  ```json
  // GET exact-search-test/_search
  {
      "query": {
          "match_phrase": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      }
  }
  
  // 응답
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "wQPmyooBe-YwzRmmNUVd",
          "_score": 19.411144,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "5",
          "_score": 16.317135,
          "_source": {
              "title": "새로운 비즈니스 중점적 다이나믹 융합 모델"
          }
      }
  ]
  ```

  - `query_string` query 사용
    - 위의 `match_phrase`와 동일한 query가 생성되며, 따라서 동일한 문제를 공유한다.

  ```json
  // GET exact-search-test/_search
  {
      "profile": true, 
      "query": {
          "query_string": {
              "default_field": "title",
              "query": "\"비즈니스 중점적 다이나믹 융합\""
          }
      }
  }
  
  // 응답
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "wQPmyooBe-YwzRmmNUVd",
          "_score": 19.411144,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "5",
          "_score": 16.317135,
          "_source": {
              "title": "새로운 비즈니스 중점적 다이나믹 융합 모델"
          }
      }
  ]
  ```



- 공백과 특수 문자가 제거된 하나의 token만 생성하여 검색

  - Analyzer 사용
    - Tokenizer 중 `keyword` tokenizer를 사용하여 하나의 token만을 생성할 수 있도록 한다.
    - `pattern_replace` character filter를 사용하여 특수 문자를 모두 제거한다.

  ```json
  // PUT
  {
      "settings": {
          "analysis": {
              "char_filter": {
                  "remove_special_char": {
                      "type": "pattern_replace",
                      "pattern": "[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅑ가-힣]",
                      "replacement": ""
                  }
              },
              "analyzer": {
                  "single_token_analyzer": {
                      "type": "custom",
                      "tokenizer": "keyword",
                      "char_filter": [
                          "remove_special_char"
                      ]
                  }
              }
          }
      },
      "mappings":{
          "properties":{
              "title":{
                  "type":"text",
                  "analyzer":"single_token_analyzer"
              }
          }
      }
  }
  ```

  - 위에서 설정한 analyzer를 통해 형태소 분석을 하면 결과는 아래와 같다.

  ```json
  [
      {
  
          "source": "비즈니스 중점적 다이나믹 융합",
          "result": "비즈니스중점적다이나믹융합"
  
      },
      {
  
          "source": "비즈니스 중점적 다이나믹 융합!",
          "result":"비즈니스중점적다이나믹융합"
  
      },
      {
  
          "source": "새로운! 비즈니스 중점적, 다이나믹 융합 모델",
          "result":"새로운비즈니스중점적다이나믹융합모델"
      }
  ]
  ```

  - 이제 title field를 대상으로 검색하면, 결과는 아래와 같다.
    - "비즈니스 중점적 다이나믹 융합"라는 검색어 역시 "비즈니스중점적다이나믹융합"라는 하나의 token으로 분석된다.
    - 특수문자, 공백을 제외한 문자들이 완전히 일치하면 검색되게 된다.

  ```json
  // GET exact-search-test/_search
  {
      "query": {
          "match":{
              "title":"비즈니스 중점적 다이나믹 융합"
          }
      }
  }
  
  // 검색 결과
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "YgiV0IoBe-YwzRmmOag4",
          "_score": 8.294649,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "hwiV0IoBe-YwzRmmRKiu",
          "_score": 8.294649,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합!"
          }
      }
  ]
  ```

  - Normalizer 사용
    - 아래와 같이 normalizer를 정의하고, 검색 대상 field를 keyword type으로 설정 후, normalizer를 적용한다.

  ```json
  // PUT exact-search-test
  {
      "settings": {
          "analysis": {
              "char_filter": {
                  "remove_special_char": {
                      "type": "pattern_replace",
                      "pattern": "[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅑ가-힣]",
                      "replacement": ""
                  }
              },
              "normalizer": {
                  "my_normalizer": {
                      "type": "custom",
                      "char_filter": [
                          "remove_special_char"
                      ]
                  }
              }
          }
      },
      "mappings":{
          "properties":{
              "title":{
                  "type":"keyword",
                  "normalizer":"my_normalizer"
              }
          }
      }
  }
  ```

  - 검색
    - 검색 결과는 analyzer를 사용한 것과 같다.

  ```json
  // GET exact-search-test/_search
  {
      "query": {
          "match":{
              "title":"비즈니스 중점적 다이나믹 융합"
          }
      }
  }
  
  // 검색 결과
  "hits": [
      {
          "_index": "exact-search-test",
          "_id": "YgiV0IoBe-YwzRmmOag4",
          "_score": 8.294649,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합"
          }
      },
      {
          "_index": "exact-search-test",
          "_id": "hwiV0IoBe-YwzRmmRKiu",
          "_score": 8.294649,
          "_source": {
              "title": "비즈니스 중점적 다이나믹 융합!"
          }
      }
  ]
  ```

  - `keyword` field를 대상으로 검색하는 것과의 차이
    - `keyword` field를 대상으로 검색할 때 보다 유연하게 적용이 가능하다.
    - `keyword` field의 경우 특수 문자나 공백이 하나라도 다를 경우 검색이 안 되는데 반해, 이 방식은 보다 유연한 적용이 가능하다.
    - 또한 요구사항에 따라 숫자를 빼거나, 영어를 빼는 등 유연하게 대응할 수 있다.



## Query Auto Completion

> https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/cai-survey-2016.pdf

- Query Auto Completion(QAC)
  - 검색어의 prefix가 주어졌을 때, prefix를 확장시켜 full query를 제안하는 기능이다.
    - QAC는 두 가지 방식으로 사용자 경험을 향상시킨다.
    - 사용자가 검색어를 입력하는 수고를 덜어준다.
    - 사용자가 원하는 검색 결과를 얻기 위해서 보다 나은 query를 입력하도록 안내한다(오타 방지를 포함).
  - QAC를 구현할 때는 아래 3가지를 염두에 두어야한다.
    - QAC는 매우 짧은 응답 시간이 요구된다.
    - 검색 결과가 없는 query 혹은 검색 된 적 없는 query의 경우 자동 완성 검색어를 생성하는데 맥락 정보를 활용하기 어렵기 때문에, 자동 완성 결과의 품질이 떨어질 수 있다.
    - 검색어 log에 강하게 의존한다.
  - 검색어 자동 완성은 일반적으로 두 단계로 이루어진다.
    - 자동 완성된 검색어 후보군 생성.
    - 검색어 후보군 순위 매기기.



- 사용자는 검색어 자동 완성 기능을 어떻게 사용하는가?

  > https://www.microsoft.com/en-us/research/wp-content/uploads/2014/07/sigirsp190-mitra.pdf 참고
  >
  > Bing의 사용자 data를 기반으로 사용자가 어떤식으로 검색어 자동 완성 기능을 사용하는지를 분석한 글이다.

  - 일반적으로 사용자는 자동 완성된 검색어 중 첫 번째나 두 번재를 사용하며, 세 번째로 제시된 검색어 부터는 사용률이 20%도 되지 않는다.
    - 첫 번째를 사용하는 비율은 90%, 두 번째를 사용하는 비율은 40% 정도이다.
    - 이러한 결과가 나온 원인은 아래와 같을 것이다.
    - 순위가 낮은 자동 완성 검색어가 관련성이 적다.
    - 사용자들이 높은 순위의 검색어가 보다 정확한 결과를 얻게 해줄 것이라는 편견을 가졌기 때문이다.
  - Query의 종류에 따라서 자동 완성된 검색어를 사용하는 비율이 달라진다.
    - 길 찾기나 일상적 질문글과 같이 많이 검색되는 글은 자동 완성된 검색어를 사용하는 비율이 높다.
    - 반면에 재정(finance)과 관련될 질문은 자동 완성된 검색어를 사용하는 비율이 낮다.
    - 이는 일상적인 질문에 대해 보다 관련성이 높은 자동 완성 검색어를 반환하기 때문으로 보인다.
    - 검색 log를 기반으로 하는 자동 완성 기능의 특성상 많이 검색될 수록 보다 관련성 있는 자동 완성 검색어가 반환될 가능성이 커지기 때문이다.
  - 사용자는 검색어에 포함된 단어를 얼마나 입력했을 때 자동 완성된 검색어를 선택하는가?
    - 아래 내용은 모두 알파벳으로 검색할 때를 기준으로한다.
    - 일반적으로 단어를 완성시키기 위해서 입력해야 할 알파벳이 4개가 남을 때 까지 자동 완성된 검색어를 선택하는 비율이 증가하다 4개 미만으로 남았을 때 부터는 감소하기 시작한다.
    - 예를 들어 conclusion이라는 단어를 검색한다고 가정했을 때 "c"~"conclus"을 입력할 때 까지는 자동 완성된 검색어를 선택하는 비율이 증가하다가 "conclus"~"conclusion"을 입력할 때 까지는 자동 완성된 검색어를 선택하는 비율이 감소한다.
    - 38%의 user가 단어 하나를 모두 입력한 후에야 자동 완성된 검색어를 선택했고, 15% 정도가 space를 입력한 후 자동 완성된 검색어를 선택했다.
    - 즉 많은 수의 user가 단어를 완성시킨 후 자동 완성된 검색어를 선택했다.

  - 사용자는 전체 query의 어느 정도를 입력한 뒤에 자동 완성된 검색어를 선택하는가?
    - 50~60%를 입력했을 때 자동 완성된 검색어를 선택하는 비율이 20% 정도로 가장 높은 정규 분포 형태를 따른다.
    - 흥미로운 점은 query를 모두 완성시킨 상태(100%)에서 자동 완성된 검색어를 선택하는 비율이 10% 정도로 상당히 높다는 점이다.
  - Spelling이 어려울수록 자동 완성된 검색어를 선택하는 비율이 높다.
    - 검색어를 3-gram, 4-gram으로 자른 후, 잘린 n-gram character들 중에서 사용 빈도가 가장 낮은 character들을 추출한다.
    - 그 후 이 character들을 기준으로 사용자들이 언제 자동 완성된 검색어를 선택하는지를 분석했을 때, 이 character에 가까울수록 자동 완성된 검색어를 선택하는 비율이 높았다.
    - 예를 들어 Hello World라는 query가 있고, 그 중 "orl"이라는 3-gram character가 잘 사용되지 않는 character라고 가정했을 때, Hello World라는 전체 query 중에서 "orl"을 기준으로 언제 자동 완성된 검색어를 선택했는지를 살펴보는 식이다.
    - "orl"은 흔치 않은 character 이므로 사용자들은 이를 typing하기 힘들 것이고, 따라서 "orl"을 입력해야하는 때가 되면("orl"에 가까워질수록) 자동 완성된 검색어를 선택하는 비율이 높을 것이다.
  - 키보드 상에서 자판의 거리에 따라 자동 완성를 선택하는 비율이 달라진다.
    - 키보다 상에서 character와 다음 character 사이의 거리가 멀 수록 자동 완성된 검색어를 선택하는 비율이 높아지지만, 거리가 5~6일 때 감소하고, 7~9일 때 다시 증가하는 양상을 보인다.
    - 이는 거리를 한 손을 기준으로 계산했기 때문인 것으로 보이며, 양손을 기준으로 할 경우 결과가 달라질 수 있다.



- QAC와 시간 사이의 관계
  - QAC의 단계중 ranking 단계를 구현하는 가장 단순하면서도 직관적인 model은 most popular completion(MPC) model이다.
    - 이 model은 자동 완성된 검색어 후보군들 중에서 검색 로그를 기반으로 가장 많이 검색된 query에 높은 rank를 매기는 방식이다.
    - 이 모델은 현재의 query popularity가 과거나 현재나 변하지 않을 것이라는 가정 하에 rank를 매긴다.
  - Query의 popularity는 시간에 따라 변화한다.
    - 예를 들어 "movie"라는 query는 금~일요일에 가장 많이 검색 될 것이고, "new year"라는 검색어는 연말연시에 가장 많이 검색 될 것이며, 큰 지진이 발생한다면 지진과 관련된 검색어가 많이 검색될 것이다.
    - Web이 점차 platform에 가까워질 수록 실시간으로 일어나는 사건에 영향을 많이 받으므로, 자연스럽게 검색에서 시간이 미치는 영향도 증가하게 된다.
    - 예를 들어 도서관의 소장 도서를 검색하는 검색 시스템은 Naver나 Google 등의 검색 platform에 비해서 시간에 따른 영향을 덜 받는다.
    - 실제로 Google의 경우 매일 가장 많이 검색 된 query 중 15%는 이전에는 검색된 적 없는 query이며, 이러한 query들은 대부분 그 날 발생한 사건들의 영향을 받는다.
  - 따라서 자동 완성 후보군의 ranking 역시 시간에 따라 변화하는 query popularity를 고려해서 이루어져야한다.
    - 이는 보통 검색 log에서 자동 완성된 검색어 후보군을 집계할 때 기간을 조정하는 식으로 이루어진다.
    - 특히 변화하는 정보를 빨리 반영하는 것이 중요한 news 검색이나 상품 검색의 경우 집계 기간을 더 짧게 설정하는 것이 좋다.



- 사용자 중심 QAC model
  - 사용자가 검색한 검색어를 분석함으로써 사용자가 원하는 것을 보다 잘 파악할 수 있다.
  - 사용자 중심 QAC model은 크게 두 종류로 나눌 수 있다.
    - 사용자가 현재 session에서 검색한 log들만 고려하는 방법(short-term).
    - 사용자가 검색한 모든 log들을 고려하난 방법(long-term).
    - 일반적으로 short-term search log가 long-term search log에 비해 더 정확한 후보를 제시할 수 있다.
  - 두 방법 모두 방식은 유사하며, 두 방식을 조합하여 사용하는 것도 가능하다.
    - 먼저 사용자가 입력한 prefix에 대한 후보군을 추출하고 vector화한다.
    - 사용자가 검색한 query들(session내 혹은 전체)을 vector화 하고 후보군을 vector화 한 값과 cosine similarity를 구해서 높은 순으로 ranking을 매긴다.
    - 만약 두 방식을 조합한다면 기본적으로 모든 검색 log를 대상으로 하되, session 내에서 검색한 query인 경우 가중치를 주는 방식을 사용할 수 있을 것이다.



- QAC 평가 지표

  - Mean Reciprocal Rank(MRR)
    - QAC 평가뿐 아니라 특정 순위가 올바르게 매겨졌는지를 평가하는데 널리 사용되는 지표이다.
  - Reciprocal Rank(RR)은 아래와 같이 구한다.
    - $p$가 사용자가 입력한 prefix, $q$가 전체 query set $Q$의 원소일 때, $Q_I(p)$는 $p$에 대한 QAC 후보이다.
    - $q'$는 사용자가 최종적으로 선택한 query이다.

  $$
  RR = 
  \begin{cases}
  1 \over rank\ \ of \ \ q'\ in\ \ Q_I(p), & \mbox{if }q'\in Q_I(p)\\
  0, & \mbox{otherwise.}
  \end{cases}
  $$

  - MRR은 전체 RR 값의 합을 시행 횟수로 나눠서 구한다.
    - 예를 들어 총 4번의 시행의 결과가 아래와 같았다고 가정해보자.
    - 사용자가 세 번째로 제시된 자동 완성 검색어를 선택했다. → RR은 1/3
    - 사용자가 네 번째로 제시된 자동 완성 검색어를 선택했다. → RR은 1/4
    - 사용자가 첫 번째로 제시된 자동 완성 검색어를 선택했다. → RR은 1
    - 사용자가 두 번째로 제시된 자동 완성 검색어를 선택했다. → RR은 1/2
    - MRR은 $(1/3+1/4+1+1/2) / 4$가 된다.
  - MRR 방식의 문제점
    - MRR은 특정 prefix로 후보군을 만드는 난이도는 고려하지 않고, 모든 prefix를 동일하게 취급한다.
    - 예를 들어 "c"라는 prefix로 후보군을 만드는 것이 "z"라는 prefix로 후보군을 만드는 것 보다 더 어려운데, 이는 "c"가 "z"보다 더 흔한 prefix이기 때문에 보다 많은 후보군을 가질 것이기 때문이다.



# Shard routing

- `_routing`

  - Elasticsearch에서 document는 아래 방식에 따라 특정 shard에 routing된다.
    - `routing_factor = num_routing_shards / num_primary_shards`
    - `shard_num = (hash(_routing) % num_routing_shard) / routing_factor`
    - 여기서 `num_routing_shards `의 값은 index settings의 `index.number_of_routing_shards`의 값이고, `num_primary_shards`는 index settings의 `index.number_of_shards`의 값이다.
    - `_routing`의 기본 값은 문서의 `_id`이다.
  - 기본적으로 routing에 문서의 `_id` 값을 사용하지만, 문서 색인시에 이 값을 변경할 수 있다.
    - 이 경우 문서를 get, update, delete 할 때 동일한 routing 값을 넣어줘야한다.

  ```json
  // 아래와 같이 routing 값을 설정할 수 있다.
  // PUT my-index/_doc/1?routing=foo1
  {
    "title": "This is a document"
  }
  
  // 동일한 routing 값을 넣어줘야한다.
  // GET my-index/_doc/1?routing=foo1
  ```

  - 검색시에도 활용할 수 있다.
    - 아래와 같이 검색할 때 routing 값을 주면 해당 routing value와 일치하는 shard에만 검색을 수행하여 검색 비용을 줄일 수 있다.

  ```json
  // GET my-index/_search?routing=foo1,foo2
  {
    "query": {
      "match": {
        "title": "document"
      }
    }
  }
  ```

  - Index 생성시에 `mappings`에 아래와 같이 설정할 경우 문서 CRUD시에 routing 값을 반드시 주도록 강제할 수 있다.
    - 만일 `mappings._routing.required`를 true로 설정했는데, CRUD시에 routing을 주지 않으면 `routing_missing_exception`를 throw한다.

  ```json
  // 아래와 같이 설정하고
  // PUT my-index
  {
      "mappings": {
          "_routing": {
              "required": true 
          }
      }
  }
  
  // 아래와 같이 routing 값 없이 CRUD를 실행하려 할 경우 
  // PUT my-index/_doc/1 
  {
    "text": "No routing value provided"
  }
  ```

  - Custom한 `_routing` 값을 사용할 경우 `_id` 값의 고유함이 보장되지 않는다.
    - 따라서 같은 `_id`를 가진 서로 다른 document가 각기 다른 shard에 저장되어 있을 수 있다.
  - `_routing` value가 특정한 하나의 shard가 아니라 전체 shard들 중 일부 부분 집합을 가리키도록 할 수 있다.
    - 이를 통해 shard들 간의 불균형 문제를 완화시킬수 있다.
    - Index 생성시에 `index.routing_partition_size`를 설정하면 된다.
    - `index.routing_partition_size` 값이 증가할수록 문서들이 여러 shard에 더 고르게 분배되지만, 검색시에 더 많은 shard들을 검색하게 돼 검색 비용이 증가한다.
    - 이 값을 줄 경우 shard를 결정하는 방식은 아래와 같이 변경된다.
    - `routing_factor = hash(_routing) + hash(_id) % routing_partition_size`
    - `shard_num = (routing_value % num_routing_shards) / routing_factor`
    - 단, 이 기능을 활성화 할 경우 join field를 사용할 수 없으며, `mappings._routing.required`이 true로 설정된다.



## Search shard routing

- Search shard routing
  - Elasticsearch는 검색시에 검색 대상 index의 data를 저장하고 있는 node를 선택하고 해당 node의 shard들에게 search request를 전달한다. 
  - 이 과정을  search shard routing 혹은 routing이라 부른다.



- Adaptive replica selection
  - Elasticsearch가 search request를 route하기 위해 기본값으로 사용하는 방식이다.
  - 이 방식은 shard allocation awareness와 함께 아래 기준들을 고려하여 적합한 node를 선택한다.
    - 이전 request에서 대상 node가 coordinator node에 응답을 반환한 시간.
    - 대상 node가 이전 검색을 수행하는 데 걸린 시간.
    - 대상 node의 search threadpool의 queue size.
  - Adaptive replica selection은 빠른 검색 속도를 위해 고안되었다. 
    - `cluster.routing.use_adaptive_replica_selection`값을 false로 줄 경우 비활성화 시킬 수 있다.
    - 비활성화 시킬 경우 Elasticsearch는 search request를 round-robin 방식으로 routing하며, 따라서 검색 속도가 느려질 수 있다.
  - 기본적으로 adaptive replica selection은 모든 검색 대상 node와 shard들을 대상으로 선택을 수행한다.



- `preference` 설정하기

  - 특정 node로 routing을 수행하고자 할 때 사용하는 옵션이며, 보통 아래와 같은 경우 사용한다.
    - Local에 있는 node로 routing하고자 할 경우.
    - Hardware를 기반으로 특정 node에 routing하고자 할 경우(우수한 hardware를 가진 node에 비용이 많이 드는 검색을 routing하고자 하는 경우 등).
    - Caching을 위해 같은 shard에 반복적으로 검색을 수행하고자 하는 경우.
  - 아래의 값들 중 하나를 주면 된다.
    - `_only_local`: local에 있는 node의 shard들만 대상으로 검색을 routing한다.
    - `_local`: 가능하면 local에 있는 node의 shard들만 대상으로 검색을 routing하며, 만약 local node에 검색 대상 index의 shard가 없을 경우 adaptive replica selection을 사용하여 routing할 node를 정한다.
    - `_only_nodes:<node_id>,<node_id>`: 입력된 node들만 대상으로 검색을 routing하며, 만일 검색 대상 shard가 여러 입력된 여러 node들에 동시에 있을 경우 adaptive replica selection을 사용하여 routing하며, 어떤 node에도 검색 대상 shard가 없을 경우에도 adaptive replica selection를 사용하여 routing할 node를 선택한다.
    - `_prefer_nodes:<node_id>,<node_id>`: 입력된 node들만 대상으로 검색을 routing하며, 만일 검색 대상 index의 shard가 없을 경우 adaptive replica selection을 사용하여 routing할 node를 정한다.
    - `_shards:<shard>,<shard>`: 입력된 shard들만 대상으로 검색을 routing하며, 다른 routing value와 결합하여 사용하는 것이 가능하지만, 반드시 `_shards`가 맨 앞에 와야 한다(e.g. `_shards:1,2|_local`)
    - `<custom-string>`: `_`로 시작하지 않는 아무 string이나 주며, cluster state와 선택된 shard가 변하지 않으면, 같은 custom string를 설정하여 수행한 검색은 항상 같은 shard에 routing된다.
  - 예시

  ```json
  // GET /my-index/_search?preference=_local
  {
      "query": {
          "match": {
              "title": "foo"
          }
      }
  }
  ```



- routing value 설정하기

  - Index에 document를 색인할 때 routing value를 준 경우, 색인시에 사용한 routing value를 검색시에 동일하게 주면, document가 색인된 shard로 검색을 routing할 수 있다.

  - 예를 들어 문서 색인시에 아래와 같이 routing value를 줬다면

  ```json
  // POST /my-index/_doc?routing=my-routing-value
  {
    "title": "foo"
  }
  ```

  - 검색시에 색인에 사용했던 것과 동일한 routing value를 주면 document가 색인된 shard로 검색을 routing할 수 있다.

  ```json
  // GET /my-index/_search?routing=my-routing-value
  {
    "query": {
      "match": {
        "title": "foo"
      }
    }
  }
  ```





# Suggester

- Suggester
  - 유사해 보이는 term을 제안하는 기능이다.
  - 아래와 같은 네 종류의 suggester 를 제공한다.
    - Term suggester: 편집거리에 기반하여 주어진 term과 유사한 term을 제안한다.
    - Phrase suggester: 주어진 term과 가장 유사한 phrase를 제안한다.
    - Completion suggester: 주어진 term의 자동 완성 결과를 제안한다.
    - Context suggester: 주어진 term과 가장 유사한 context를 제안한다.
  - 모든 suggester는 아래와 같은 공통 option을 받는다.
    - `text`: 제안을 받을 대상 text를 받는다.
    - `field`: 제안 후보를 생성할 field를 받는다.
    - `analyzer`: `text`로 들어온 값을 분석할 analyzer를 받는다.
    - `size`: 각 text token 당 최대 제안 결과수를 받는다.
    - `sort`: 제안 목록을 어떻게 정렬할지를 받는다(`score`, `frequency` 둘 중 하나의 값).
    - `suggest_mode`: 어떤 경우에 suggestion을 반환할지를 받는다.
  - `suggest_mode`
    - `missing`:`text`로 받은 값이 index에 없을 경우에만 suggestion을 반환한다. 
    - `popular`:`text`로 주어진 값이 문서들에 등장하는 빈도보다 많은 문서에 등장하는 suggestion들만 반환한다(예를 들어 `text`로 주어진 term이 3개 의 문서에서 등장하고, suggestion 후보 중 하나인 term A가 2개의 문서에서 등장한다면, A는 제안되지 않는다, 반면에 suggestion 후보 중 하나인 term B가 4개의 문서에서 등장한다면, B는 제안된다).
    - `always`: 항상 suggestion을 반환한다.



- Term Suggester

  - 편집거리를 사용하여 비슷하 단어를 제안한다.
  - Option들
    - `max_edits`: edit distance의 최댓값을 받는다(기본값은 2).
    - `prefix_length`: suggestion에 포함되기 위해 일치해야 하는 prefix character 개수의 최솟값을 받는다(기본값은1).
    - `min_word_length`: suggestion에 포함되기 위한 term의 최소 길이를 받는다(기본 값은 4).
    - `min_doc_freq`: suggestion에 포함되기 위해 term이 전체 문서들 중 몇 개의 문서에 포함되어야 하는지를 지정한다. 정수를 주면 문서의 개수, 0~1 사이의 소수를 주면 percent가 설정된다.
    - `max_term_freq`: suggestion에 포함되기 위해 term이 전체 문서들 중 몇 개 미만의 문서에 포함되어야 하는지를 지정한다. 정수를 주면 문서의 개수, 0~1 사이의 소수를 주면 percent가 설정된다.
    - `string_distance`: edit distance를 구하는 방식을 선택한다.
  - `string_distance`는 아래 5가지 중 하나를 선택할 수 있다.
    - `internal`: `damerau_levenshtein`를 최적화한 방식이다.
    - `damerau_levenshtein`: Damerau-Levenshtein algorithm 기반의 방식이다.
    - `levenshtein`: Levenshtein edit distance algorithm 기반의 방식이다.
    - `ngram`: n-gram 기반의 방식이다.
  - Test data 색인하기

  ```json
  // PUT term_suggest_test/_doc/1
  {
    "text":"adapt"
  }
  
  // PUT term_suggest_test/_doc/2
  {
    "text":"adept"
  }
  
  // PUT term_suggest_test/_doc/3
  {
    "text":"adopt"
  }
  
  // PUT term_suggest_test/_doc/4
  {
    "text":"child"
  }
  ```

  - Suggest 기능을 사용하여 유사한 단어를 제안 받는다.
    - response의 `options`에 제안된 단어들이 담겨 있다.

  ```json
  // GET term_suggest_test/_search
  {
    "suggest": {
      "my_suggestion": {
        "text": "adwpt",
        "term": {
          "field": "text"
        }
      }
    }
  }
  
  // response
  {
      // ...
      "suggest": {
      "my_suggestion": [
        {
          "text": "adwpt",
          "offset": 0,
          "length": 5,
          "options": [
            {
              "text": "adapt",
              "score": 0.8,
              "freq": 1
            },
            {
              "text": "adept",
              "score": 0.8,
              "freq": 1
            },
            {
              "text": "adopt",
              "score": 0.8,
              "freq": 1
            }
          ]
        }
      ]
    }
  }
  ```

  - 여러 token으로 구성된 term이 들어올 경우 각 token에 대한 제안을 반환한다.

  ```json
  // GET term_suggest_test/_search
  {
    "suggest": {
      "my_suggestion": {
        "text": "adopted chil",
        "term": {
          "field": "text"
        }
      }
    }
  }
  
  // response
  {
      // ...
      "suggest": {
      "my_suggestion": [
        {
          "text": "adopted",
          "offset": 0,
          "length": 7,
          "options": [
            {
              "text": "adopt",
              "score": 0.6,
              "freq": 1
            }
          ]
        },
        {
          "text": "chil",
          "offset": 8,
          "length": 4,
          "options": [
            {
              "text": "child",
              "score": 0.75,
              "freq": 1
            }
          ]
        }
      ]
    }
  }
  ```



- Completion Suggest API

  - 자동 완성 기능을 제공하기 위한 suggester이다.
    - 사용자가 typing을 하면 가능한 빨리 결과를 반환해야하기 때문에 속도가 중요하다.
    - 따라서 Elasticsearch는 memory를 많이 사용하지만 속도가 빠른 FST(Finite State Transducer)라는 자료구조를 사용한다.
    - FST는 검색어가 모두 메모리에 로드되는 구조이며, 색인 중에 FST를 작성한다.
  - Completion suggester를 사용하려면 대상 field의 type을 `completion` type으로 설정해야한다.

  ```json
  // PUT completion_suggest_text
  {
    "mappings": {
      "properties": {
        "term":{
          "type":"completion"
        }
      }
    }
  }
  ```

  - 문서를 색인한다.

  ```json
  // PUT completion_suggest_text/_doc/1
  {
    "term":"hell"
  }
  
  // PUT completion_suggest_text/_doc/2
  {
    "term":"hello"
  }
  
  // PUT completion_suggest_text/_doc/3
  {
    "term":"hello world"
  }
  
  // PUT completion_suggest_text/_doc/4
  {
    "term":"say hello"
  }
  ```

  - 자동 완성 결과를 확인한다.

  ```json
  // GET completion_suggest_text/_search
  {
    "suggest": {
      "my_suggestion": {
        "text":"hel",
        "completion": {
          "field": "term"
        }
      }
    }
  }
  
  // response
  {
      // ...
      "suggest": {
      "my_suggestion": [
        {
          "text": "hel",
          "offset": 0,
          "length": 3,
          "options": [
            {
              "text": "hell",
              "_index": "completion_suggest_text",
              "_id": "1",
              "_score": 1,
              "_source": {
                "term": "hell"
              }
            },
            {
              "text": "hello",
              "_index": "completion_suggest_text",
              "_id": "2",
              "_score": 1,
              "_source": {
                "term": "hello"
              }
            },
            {
              "text": "hello world",
              "_index": "completion_suggest_text",
              "_id": "3",
              "_score": 1,
              "_source": {
                "term": "hello world"
              }
            }
          ]
        }
      ]
    }
  }
  ```

  - Prefix에 해당하지 않아도 검색되게 하기 위해선 배열 형태로 색인해야한다.
    - 위 결과를 보면 "hello"가 포함되어 있지만, "hello"로 시작하지는 않는 "say hello"는 포함되지 않은 것을 볼 수 있다.
    - 만약 "say hello"도 검색되게 하고자 한다면 아래와 같이 배열로 색인해야한다.

  ```json
  // PUT completion_suggest_text/_doc/1
  {
    "term":{
      "input":["hell"]
    }
  }
  
  // PUT completion_suggest_text/_doc/2
  {
    "term":{
      "input":["hello"]
    }
  }
  
  // PUT completion_suggest_text/_doc/3
  {
    "term":{
      "input":["hello", "world"]
    }
  }
  
  // PUT completion_suggest_text/_doc/4
  {
    "term":{
      "input":["say", "hello"]
    }
  }
  ```

  - 자동 완성 결과 확인
    - 아까와는 달리 say hello도 포함된 것을 볼 수 있다.

  ```json
  // GET completion_suggest_text/_search
  {
    "suggest": {
      "my_suggestion": {
        "text":"hel",
        "completion": {
          "field": "term"
        }
      }
    }
  }
  
  // response
  {
      // ...
      "suggest": {
      "my_suggestion": [
        {
          "text": "hel",
          "offset": 0,
          "length": 3,
          "options": [
            // ...
            {
              "text": "hello",
              "_index": "completion_suggest_text",
              "_id": "4",
              "_score": 1,
              "_source": {
                "term": {
                  "input": [
                    "say",
                    "hello"
                  ]
                }
              }
            }
          ]
        }
      ]
    }
  }
  ```







# Mapping explosion

> https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-explosion.html

- Mapping explosion
  - Mapping에서 field의 개수가 너무 많거나, 많아질 가능성이 있는 상황을 의미한다.
  - 아래와 같은 증상이 나타날 수 있다.
    - 간단한 검색에도 많은 시간이 걸린다.
    - 색인에 많은 시간이 걸린다.
    - Heap memory 사용량과 CPU 사용량이 증가한다.



- Mapping explosion을 방지하기 위한 방법들

  - Flattened data type을 사용한다.
    - 아래 예시와 같이 object 형식의 data를 색인하면, object 내의 data가 sub field로 생성된다.
    - 즉 foo field의 sub field로 bar, qux field가 생성된다.
    - 그러나 flattened type으로 색인할 경우 sub field를 생성하지 않고 object 내의 모든 data를 단일 field에 색인하여 전체 field의 개수를 줄일 수 있다.

  ```json
  // PUT test
  {
    "mappings": {
      "properties": {
        "foo":{
          "type":"flattened"
        }
      }
    }
  }
  
  // PUT test/_doc/1
  {
    "foo": {
      "bar": "baz",
      "qux": "quxx"
    }
  }
  
  // GET test/_mapping
  /* output
  {
    "test": {
      "mappings": {
        "properties": {
          "foo": {
            "type": "flattened"
          }
        }
      }
    }
  */
  ```

  - Dynamic mapping을 비활성화한다.

