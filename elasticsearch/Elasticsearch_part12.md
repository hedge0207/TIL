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





## 오타 교정

- 한글과 term suggester
  - 영문의 경우 term suggester를 사용하여 간단하게 오타 교정이 가능하다.
  - 그러나 한글의 경우 영문에 비해 유니코드 체계가 복잡하기 때문에 편집거리 기반의 term suggester를 사용하여 오타 교정을 하는 것이 쉽지 않다.
  - 따라서 한글로 이루어진 query를 편집거리 기반의 term suggester로 오타 교정을 하기 위해서는 한글을 자모 단위로 끊어야 한다.
  - 이를 위해 [javacafe에서 개발한 plugin](https://github.com/javacafe-project/elasticsearch-plugin)을 설치해야 한다.



- 한글 오타 교정

  - Index를 생성한다.

  ```json
  // PUT test-index
  {
    "settings": {
      "analysis": {
        "analyzer": {
          "jamo-analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "javacafe_jamo"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "text": {
          "type": "text",
          "analyzer": "jamo-analyzer"
        }
      }
    }
  }
  ```

  - 문서를 색인한다.

  ```json
  // PUT test-index/_doc/1
  {
    "text":"논현역"
  }
  ```

  - `text` field를 대상으로 오타가 포함된 query로 검색을 실행해본다.
    - 아무 결과도 나오지 않는 것을 볼 수 있다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match": {
        "text":"넌현역"
      }
    }
  }
  ```

  - Term suggester를 사용해 오타 교정을 실행한다.

  ```json
  // GET test-index/_search
  {
    "suggest": {
      "my-suggestion": {
        "text": "넌현역",
        "term": {
          "field": "text"
        }
      }
    }
  }
  ```

  - 결과는 아래와 같다.

  ```json
  {
      // ...
      "suggest" : {
      "my-suggestion" : [
        {
          "text" : "ㄴㅓㄴㅎㅕㄴㅇㅕㄱ",
          "offset" : 0,
          "length" : 3,
          "options" : [
            {
              // 논현역이 반환된다.
              "text" : "ㄴㅗㄴㅎㅕㄴㅇㅕㄱ",
              "score" : 0.8888889,
              "freq" : 1
            }
          ]
        }
      ]
    }
  }
  ```

  - 반환 결과를 query로 사용하여 다시 검색하면 원하는 결과가 잘 나오는 것을 볼 수 있다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match": {
        "text":"ㄴㅗㄴㅎㅕㄴㅇㅕㄱ"
      }
    }
  }
  ```



- 한영/영한 오타 교정

  - javacafe plugin의 `kor2eng`, `eng2kor` filter를 사용하여 한영/영한 오타 교정이  가능하다.
  - Index를 생성한다.
    - 보다 간편하게 사용하기 위해 `copy_to`를 사용하여 색인한다.
    - 두 filter는 검색시에만 동작하고 색인시에는 동작하지 않는 것으로 보인다.
    - 따라서 "논현역"을 입력해도 `kor2eng` filter에 의해 "shsgusdur"으로 token이 생성되는 일은 없으므로 `search_analyzer`와 `analyzer`를 구분해서 정의할 필요는 없을 듯 하다. 

  ```json
  // PUT test-index
  {
    "settings": {
      "analysis": {
          "analyzer": {
          "kor2eng_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "javacafe_kor2eng"
            ]
          },
          "eng2kor_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "javacafe_eng2kor"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "text":{
          "type":"text",
          "copy_to": ["kor2eng", "eng2kor"]
        },
        "kor2eng":{
          "type":"text",
          "search_analyzer": "kor2eng_analyzer"
        },
        "eng2kor":{
          "type":"text",
          "search_analyzer": "eng2kor_analyzer"
        }
      }
    }
  }
  ```

  - 문서를 색인한다.

  ```json
  // PUT test-index/_doc/1
  {
    "text":"논현역"
  }
  
  // PUT test-index/_doc/2
  {
    "text":"Elasticsearch"
  }
  ```

  - 한영, 영한이 전환된 상태로 검색을 실행한다.
    - 둘 다 검색 결과가 나오지 않는다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match": {
        "text": "shsgusdur"
      }
    }
  }
  
  // GET test-index/_search
  {
    "query": {
      "match": {
        "text": "shsgusdur"
      }
    }
  }
  ```

  - 한영, 영한 오타 교정 field를 대상으로 검색한다.
    - 한영, 영한이 변환되어 검색 결과가 제대로 나오게 된다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match": {
        "eng2kor":"shsgusdur"
      }
    }
  }
  
  // GET test-index/_search
  {
    "query": {
      "match": {
        "kor2eng":"딤ㄴ샻ㄴㄷㅁㄱ초"
      }
    }
  }
  ```







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



- 시간 기반 QAC model

  - MPC(Most Popular Completion)
    - QAC에서 순위 매기기 단계를 구현하는 가장 직관적인 방법은 query의 인기도(빈도)를 기반으로 하는 Maximum Likelihood Extimation(MLE)이다.
    - 이러한 유형의 ranking model을 MPC라 부른다.
    - MPC model에서는 현재의 query popularity 분포가 과거에 관찰된 것과 같을 것이라고 가정한다.
    - 즉 현재의 query popularity가 과거나 현재나 변하지 않을 것이라는 가정 하에 rank를 매긴다.
  - MPC 계산 방식
    - $f(q)$는 전체 검색 로그 집합 $Q$에서 query $q$가 등장한 횟수(frequency)를 의미한다.
    - $C(p)$는 prefix $p$로 시작하는 자동완성 후보군들의 집합을 의미한다.

  $$
  MPC(p)\ = \ arg\ \underset{q\in C(p)}{max}\ w(q),\ \ where\ w(q)={f(q) \over \sum_{q_i \in Q} f(q_i)}
  $$

  - Query의 popularity는 시간에 따라 변화한다.
    - 예를 들어 "movie"라는 query는 금~일요일에 가장 많이 검색 될 것이고, "new year"라는 검색어는 연말연시에 가장 많이 검색 될 것이며, 큰 지진이 발생한다면 지진과 관련된 검색어가 많이 검색될 것이다.
    - Web이 점차 platform에 가까워질 수록 실시간으로 일어나는 사건에 영향을 많이 받으므로, 자연스럽게 검색에서 시간이 미치는 영향도 증가하게 된다.
    - 예를 들어 도서관의 소장 도서를 검색하는 검색 시스템은 Naver나 Google 등의 검색 platform에 비해서 시간에 따른 영향을 덜 받는다.
    - 실제로 Google의 경우 매일 가장 많이 검색 된 query 중 15%는 이전에는 거의 검색된 적 없는 query이며, 이러한 query들은 대부분 그 날 발생한 사건들의 영향을 받는다.

  - 따라서 자동 완성 후보군의 ranking 역시 시간에 따라 변화하는 query popularity를 고려해서 이루어져야한다.
    - 이는 보통 검색 log에서 자동 완성된 검색어 후보군을 집계할 때 기간을 조정하는 식으로 이루어진다.
    - 특히 변화하는 정보를 빨리 반영하는 것이 중요한 news 검색이나 상품 검색의 경우 집계 기간을 더 짧게 설정하는 것이 좋다.

  - 시간을 고려한(Time-Sensitive) 계산 방식

    - 위에서 살펴본 MPC 계산 방식은 현재의 query popularity 분포가 과거에 관찰된 것과 같을 것이라고 가정한 것이다.
    - 그러나 시간에 따라 query popularity는 변화하므로 시간을 고려해야 하며, 아래와 같이 구할 수 있다.

    - $C(p)$는 prefix $p$로 시작하는 자동완성 후보군들의 집합을 의미한다.
    - $\hat{f_t}(q)$는 특정 시간 $t$에  전체 query log 집합 $Q$에서 query $q$의 추정된 빈도를 의미한다.

  $$
  TS(p, t)\ = \ arg\ \underset{q\in C(p)}{max}\ w(q|t),\ \ where\ w(q|t)={\hat{f_t}(q) \over \sum_{q_i \in Q} \hat{f_t}(q_i)}
  $$

  - Query의 미래의 frequncy인 $\hat{y}_{t+1}$은 아래와 같은 방식으로 예측할 수 있다.
    - 이전에 관찰된 $y_t$와 smooth된 output인 $\bar{y}_{t-1}$을 기반으로 단일 지수 평활법(single exponential smoothing method)를 사용하여 구한다.
    - $λ$는 0에서 1 사이의 trade-off parameter이다.

  $$
  \hat{y}_{t+1} = \bar{y}_t=λ \cdot y_t + (1-λ) \cdot \bar{y}_{t-1}
  $$





- 사용자 중심 QAC model
  - 사용자가 검색한 검색어를 분석함으로써 사용자가 원하는 것을 보다 잘 파악할 수 있다.
  - 사용자 중심 QAC model은 크게 두 종류로 나눌 수 있다.
    - 사용자가 현재 session에서 검색한 log들만 고려하는 방법(short-term).
    - 사용자가 검색한 모든 log들을 고려하는 방법(long-term).
    - 일반적으로 short-term search log가 long-term search log에 비해 더 정확한 후보를 제시할 수 있다.
  
  - 두 방법 모두 방식은 유사하며, 두 방식을 조합하여 사용하는 것도 가능하다.
    - 먼저 사용자가 입력한 prefix에 대한 후보군을 추출하고 vector화한다.
    - 사용자가 검색한 query들(session내 혹은 전체)을 vector화 하고 후보군을 vector화 한 값과 cosine similarity를 구해서 높은 순으로 ranking을 매긴다.
    - 만약 두 방식을 조합한다면 기본적으로 모든 검색 log를 대상으로 하되, session 내에서 검색한 query인 경우 가중치를 주는 방식을 사용할 수 있을 것이다.
  - Context를 고려한 자동완성 결과는 아래와 같이 구할 수 있다.
    - 사용자가 현재 session에서 이전에 검색한 query들을 context라고 본다.
    - Prefix $p$에 대한 자동 완성 결과의 집합을 $q_c$라 한다.
    - $v_q$는 $q_c$를 vector화 한 값이며, $v_C$는 content $C$와 가장 높은 cosine similarity를 의미한다.
    - $Q_I(p)$는 $p$를 확장한 자동완성 후보들의 집합이다.
  
  $$
  q_c ← arg\ \underset{q\in Q_I(p)}{max} {v_q \cdot v_C \over ||v_q|| \cdot ||v_C||}
  $$
  





- Mean Reciprocal Rank(MRR)

  - QAC를 평가하기 위한 지표이다.
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
    - 그러나 MRR은 모든 prefix를 동일하게 취급하므로 QAC에 대한 정확한 평가에 제한이 있을 수 있다.



- pSaved, eSaved

  -  MRR과 마찬가지로 QAC를 평가하기 위한 지표이다.
    - MRR과 달리 사용자의 만족도를 반영하여 평가한다.
    - Log로 기록한 사용자의 행동으로 QAC를 평가한다.
  - pSaved
    - Query를 작성하는 동안 query suggestion 결과를 사용할 가능성으로 정의된다.
    - 사용자가 입력한 query를 $q$라 하고, $q$의 길이를 $|q|$라 하며, 길이가 $i$인 $q$의 prefix를 $q[1, ..., i]$라 한다.
    - $S_{ij}$는 사용자가 prefix $q[1, ..., i]$에 대해 주어진 suggestion 중 $j$번째 suggestion에 만족했는 지를 표현한다.
    - 예를 들어 $S_{ij}$에서 $i=5$, $j=3$이라면 사용자는 query의 5번째 prefix까지 입력했을 때, 제안된 자동완성 결과중 3번째 결과를 선택했다는 의미이다.
    - $I(S_{ij})$는 만약 사용자가 query suggestion을 click했으면 1, 아닐 경우 0의 값을 가진다.
    - $P(S_{ij})$는 사용자가 만족했을 가능성을 정의하며, user model에 따라 달라진다.
    - $\sum_jP(S_{ij}=1)$는 $q[1..i]$까지만 query를 작성할 확률과 같다(즉 $i$번째 까지만 작성하고 자동 완성 결과를 선택할 확률과 같다).

  $$
  pSaved(q)=\sum_{i=1}^{|q|} \sum_j I(S_{ij})P(S_{ij}=1)=\sum_{i=1}^{|q|} \sum_jP(S_{ij}=1)
  $$

  - eSaved
    - Query suggestion mechanism으로 인해 사용자가 누르지 않아도 되는 keypress의 정규화된 양을 의미한다.

  $$
  eSaved(q)=\sum_{i=1}^{|q|}(1-{i \over |q|}) \sum_jP(S_{ij}=1)
  $$







- QAC의 구현상의 효율성
  - QAC는 기능의 특성상 빠른 속도가 매우 중요하다.
    - 따라서 효율적인 알고리즘과 자료구조를 사용해야한다.
  - Trie
    - 자동 완성 후보군들을 저장하기 위해서 일반적으로 사용하는 자료구조이다.
    - Character들을 tree 형태로 저장하여 상대적으로 빠른 속도로 prefix로부터 자동 완성 후보군들을 찾아낼 수 있다.
    - 일반적으로 root node는 빈 character를 저장하고, leaf node에는 마지막 node라는 표시와 함께 query frequency 등의 정보를 저장한다.
  - Copletion Trie, RMQ Trie, Score-Decomposed Trie
    - 자동 완성 set이 너무 커서 메모리에 올리기 위해 압축이 필요한 경우 사용하기 위해 Hsu와 Ottaviano가 trie를 기반으로 고안한 자료구조이다.
    - 각각은 공간과 속도, 복잡도에서 trade-off 관계이다.



- Completion suggester 사용하여 구현하기

  - Index를 생성한다.
    - 자동 완성 대상 field를 `completion` type으로 생성한다.

  ```json
  // PUT qac-index
  {
    "mappings": {
      "properties": {
        "text":{
          "type":"completion"
        }
      }
    }
  }
  ```

  - 자동 완성 후보군을 색인한다.

  ```json
  // PUT qac-index/_doc/1
  {
    "text":"붕어빵"
  }
  
  // PUT qac-index/_doc/2
  {
    "text":"잉어빵"
  }
  
  // PUT qac-index/_doc/3
  {
    "text":"황금붕어빵"
  }
  
  // PUT qac-index/_doc/4
  {
    "text":"붕어빵가게"
  }
  ```

  - Completion suggester를 사용하여 자동 완성 후보군을 받아온다.
    - "붕어빵"과 "붕어빵가게"만 반환되는 것을 확인할 수 있다.

  ```json
  // GET qac-index/_search
  {
    "suggest": {
      "my_suggestion": {
        "text": "붕어",
        "completion": {
          "field": "text"
        }
      }
    }
  }
  
  // response
  {
      // ...
      "suggest" : {
      "my_suggestion" : [
        {
          "text" : "붕어",
          "offset" : 0,
          "length" : 2,
          "options" : [
            {
              "text" : "붕어빵",
              "_index" : "qac-index",
              "_type" : "_doc",
              "_id" : "1",
              "_score" : 1.0,
              "_source" : {
                "text" : "붕어빵"
              }
            },
            {
              "text" : "붕어빵가게",
              "_index" : "qac-index",
              "_type" : "_doc",
              "_id" : "4",
              "_score" : 1.0,
              "_source" : {
                "text" : "붕어빵가게"
              }
            }
          ]
        }
      ]
    }
  }
  ```

  - Completion suggester를 사용하는 방식의 한계
    - Prefix 방식의 매칭만 지원하기 때문에 시작 부분이 반드시 일치해야한다.
    - 이로 인해 위 예시에서 황금붕어빵은 검색되지 않았다.
    - 또한 "빵"으로 검색하면 어떤 결과도 반환되지 않는다.



- Ngram tokenizer와 filter를 사용하여 구현하기

  - 아래와 같이 index를 생성하고, data는 위와 동일하게 색인한다.
    - 전방 일치, 부분 일치, 후방 일치가 모두 가능하도록 할 것이다.
  
  ```json
  // PUT qac-index
  {
    "settings": {
      "index":{
        "max_ngram_diff":50
      },
      "analysis": {
        "analyzer": {
          "ngram_analyzer":{
            "type":"custom",
            "tokenizer":"standard",
            "filter":[
              "ngram_filter"
            ]
          }
        }, 
        "filter": {
          "ngram_filter":{
            "type":"ngram",
            "min_gram":2,
            "max_gram":50
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "text":{
          "type":"text",
          "analyzer":"ngram_analyzer"
        }
      }
    }
  }
  ```
  
  - 검색한다.
    - 전방, 부분, 후방 일치 모두 잘 동작하는 것을 확인할 수 있다.
  
  ```json
  // GET qac-index/_search
  {
    "query": {
      "match": {
        "text": "붕어"
      }
    }
  }
  
  // GET qac-index/_search
  {
    "query": {
      "match": {
        "text": "어빵"
      }
    }
  }
  
  // GET qac-index/_search
  {
    "query": {
      "match": {
        "text": "가게"
      }
    }
  }
  ```
  
  - 한계
    - ngram을 사용하여 형태소 분석을 하면 매우 많은 token이 생성되게 된다.
    - 이는 색인 시간, index 크기, 검색 시간을 모두 증가시킬 수 있으므로 주의해서 사용해야한다.



- 한글 자모 대상으로 자동 완성 하기

  - 한글의 경우 초성, 중성, 종성이 결합되어 하나의 글자를 이루는 형태로 자동완성을 완벽하게 구현하기가 영문에 비해 까다롭다.
    - 예를 들어 사용자가 붕어빵을 검색하기 위해 "부"까지 검색할 경우 자모 단위로 token이 분리되지 않으면 븡어빵을 자동완성 결과로 제안해 줄 수 없다.
    - 붕어빵은 ngram으로 자른다고 하더라도 ["붕", "붕어", "붕어빵", "어", "어빵", "빵"]으로 분할된다.
    - 따라서 최소한 "붕"까지는 입력해야 붕어빵을 제안할 수 있다.
    - 또 다른 문제는 자음이 종성으로 온 것인지 다음 글자의 초성으로 온 것인지 알 수 없다는 것이다.
    - 예를 들어 가게를 검색하기 위해서는 ㄱ-가-각-가게의 과정을 거치게 된다.
    - 가게는 ["가","가게"]로 분할된다.
    - 이 때 "가"까지 입력하면 "가게"가 자동 완성으로 제안되겠지만, 마저 입력하기 위해 "ㄱ"을 추가로 입력하면 각"이 되어 "가게"는 자동 완성으로 제안되지 못하게 된다.
    - 위와 같은 문제들로 인해 정확한 한글 자동 완성 기능을 위해서는 반드시 자모단위로 끊어야 한다.

  - Index 생성하기
    - ngram filter를 사용한다.
    - java-cafe plugin을 사용하여 색인시에 token들을 자모로 변환한다.

  ```json
  // PUT ko-qac-index
  {
    "settings": {
      "index":{
        "max_ngram_diff":8
      },
      "analysis": {
        "analyzer": {
          "my_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "javacafe_jamo",
              "ngram"
            ]
          }
        },
        "filter": {
          "ngram":{
            "type":"ngram",
            "min_gram":2,
            "max_gram":10
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "text": {
          "type": "text",
          "analyzer": "my_analyzer"
        }
      }
    }
  }
  ```

  - 검색하기
    - "부"만 검색해도 붕어빵이 포함된 모든 문서가 반환된다.
    - "각"을 입력해도 "붕어빵 가게"가 반환된다.

  ```json
  // GET ko-qac-index/_search
  {
    "query": {
      "match": {
        "text": "부"
      }
    }
  }
  
  // GET ko-qac-index/_search
  {
    "query": {
      "match": {
        "text": "각"
      }
    }
  }
  ```

  - 순서 문제
    - 아래와 같이 두 개의 문서가 있다고 가정해보자.

  ```json
  // PUT ko-qac-index/_doc/7
  {
    "text":"붕어빵 기계"
  }
  
  // PUT ko-qac-index/_doc/8
  {
    "text":"기계 붕어빵"
  }
  ```

  - 아래와 같이 검색할 경우, "기계 붕어빵"이 순서까지 정확함에도 둘의 점수가 같아 "붕어빵 기계"가 더 상단에 노출된다.

  ```json
  // GET ko-qac-index/_search
  {
    "query": {
      "match": {
        "text": "기계 붕어빵"
      }
    }
  }
  
  // response
  {
      // ...
      "hits" : [
        {
          "_index" : "ko-qac-index",
          "_type" : "_doc",
          "_id" : "7",
          "_score" : 0.7749381,
          "_source" : {
            "text" : "붕어빵 기계"
          }
        },
        {
          "_index" : "ko-qac-index",
          "_type" : "_doc",
          "_id" : "8",
          "_score" : 0.7749381,
          "_source" : {
            "text" : "기계 붕어빵"
          }
        }
      ]
  }
  ```

  - `match_phrase_prefix` query를 사용한다.
    - `match_phrase_prefix`로 순서까지 일치하는 "기계 붕어빵"이 더 상단에 노출된다.

  ```json
  // GET ko-qac-index/_search
  {
    "query": {
      "bool": {
        "should": [
          {
            "match":{
              "text":"기계 붕어빵"
            }
          },
          {
            "match_phrase_prefix": {
              "text": "기계 붕어빵"
            }
          }
        ]
      }
    }
  }
  ```

  - 사용자의 요구에 따라 query나 analyzer 등을 변경해서 적용하면 되며, 정답은 없다.



- 초성 검색하기

  - 방식은 한글 자모를 대상으로 자동완성 기능을 구현하는 것과 동일하다.

  - Index를 생성하고 위와 같은 data를 색인한다.

  ```json
  // PUT chosung-index
  {
    "settings": {
      "index": {
        "max_ngram_diff": 8
      },
      "analysis": {
        "analyzer": {
          "my_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "javacafe_chosung",
              "edge_ngram"
            ]
          }
        },
        "filter": {
          "edge_ngram": {
            "type": "edge_ngram",
            "min_gram": 2,
            "max_gram": 10
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "text": {
          "type": "text",
          "analyzer": "my_analyzer"
        }
      }
    }
  }
  ```

  - 검색한다.

  ```json
  // GET chosung-index/_search
  {
    "query": {
      "match": {
        "text": "ㅂㅇㅃ"
      }
    }
  }
  ```







### QAC와 관련된 기능들

- Query suggestion(=query recommendation)
  - 사용자의 input(query의 일부)이 주어졌을 때, 이와 관련된 query를 추천해주는 기능이다.
    - 사용자가 자신이 원하는 정보를 찾기 위한 query를 작성하기 어려울 때 도움이 된다.

  - QAC와의 차이
    - QAC는 사용자가 입력한 query를 prefix로 사용하여 해당 prefix로 시작하는 query들을 제안한다.
    - Query suggestion은 사용자가 입력한 query와 의미가 유사한 query를 제안한다.
    - 일반적으로 QAC에는 엄격한 matching 정책을 적용하지만, query suggestion은 그렇지 않다.
    - 또한 자동완성은 일반적으로 사용자가 query를 입력하고 있는 중에만 표출되지만, query suggestion은 사용자가 query를 모두 입력한 뒤에도 표출된다.

  - Query suggestion은 일반적으로 아래의 두 가지 접근법을 따른다.
    - 검색 결과 기반으로 query를 제안
    - 검색 log 기반으로 query를 제안(이 경우 session 내에서 발생한 click 등의 사용자의 행동도 고려한다).




- Query expansion
  - 원본 query를 확장하여 query에 사용된 term들을 사용자의 의도를 더 정확히 드러내는 term들로 확장하는 기법이다.
    - Term들을 유의어나 다의어, 동음이의어 등으로 확장한다.
    - 일반적으로 query expansion은 사용자에게 노출되지는 않는다.
  - 일반적으로 검색 log를 분석하여 확장할 term들을 추출하는 방식을 사용한다.



- Query correction(=query spelling correction)

  - 철자가 틀리게 입력된 query를 교정해주는 기능이다.

    - 단순히 철자 뿐 아니라 띄어쓰기 등도 검사해준다.

  - 일반적으로 machine learning에 기반한 기법들이 많이 사용된다.

    - 대량의 text 집합이나 검색 log 집합을 가지고 학습시킨다.






## 유사도 검색

- Elasticsearch의 유사도 검색

  - Elasticsearch는 7.3부터 `dense_vector` field를 지원한다.

    - 마찬가지로 7.3부터 `script_score` query에서 `cosine_similarity` 함수를 지원한다.

  - 8.0부터 `_search` API에서 `kNN` search를 지원한다.

  - 8.0부터 ANN(Approximate Nearest Neighbor) 검색을 지원한다.

    - 저차원 vector에서 kNN에 활용하기 위한 KD-trees라는 자료구조가 있다.
    - Elasticsearch에는 지리 data나 숫자 data를 처리하기 위해 이미 KD-trees가 내장되어 있다.

    - 그러나, 현대의 text 또는 image embedding model들은 대부분 100~1000 사이, 혹은 그 이상의 고차원 vector를 생성한다.
    - 이렇게 큰 차원에서는 가까운 이웃을 찾는 것이 쉽지 않다.

  - ANN
    - Approximate Nearest Neighbor algorithm은 Nearest Neighbor algorithm에서 정확도를 희생하여 속도를 개선시킨 algorithm이다.
    - 항상 정확한 k개의 가장 가까운 vector를 반환하지는 않는다.
    - 그러나 효율적으로 동작하며, 성능을 유지하면서 거대한 data를 scaling할 수 있게 해준다.
    - ANN algorithm은 학술적으로 매우 활발히 연구되고 있어 많은 algorithm들이 나와 있다.
    - 이 algorithm들은 일반적으로 검색 속도와 구현의 복잡성 그리고 색인 속도에서 서로 다른 trade-off를 가지고 있다.
    - Elasticsearch에서는 HNSW(Hierarchical Navigable Small World graphs) algorithm을 사용한다.
    - HNSW는 여러 ANN algorithm들을 대상으로 한 benchmark에서 뛰어는 검색 성능을 보여 줬으며, 이미 많은 업계에서 널리 사용되고 있다.



### Script score query

- Script score query

  - 검색 결과로 반환된 document들의 점수를 script를 사용하여 변경하는 query이다.
    - 아래와 같이 `script_score` 내부의 `query`로 문서들을 검색하고, `script`로 검색된 문서들의 점수를 조정한다.
    - 주의할 점은 최종 점수가 음수일 수는 없다는 것인데, 이는 Lucene이 score를 0 미만으로 설정할 수 없게 되어있기 때문이다.
    - `min_score`는 여기에 설정한 점수 보다 낮은 점수를 가진 document는 반환되지 않게 하기 위한 option이다.
    - `boost`는 `script`에 의해 계산 된 점수에 곱해 최종 점수를 구할 때 사용한다(즉, 최종 점수는 `script가 산출한 점수 * boost`가 된다).

  ```json
  // GET /_search
  {
      "query": {
          "script_score": {
              "query": {
                  "match": { "message": "elasticsearch" }
              },
              "script": {
                  "source": "doc['my-int'].value / 10 "
              },
              "min_score":0.1
          }
      }
  }
  ```

  - 아래와 같이 `_score`를 사용하여 document의 원래 `_score` 값에 접근하는 것이 가능하다.

  ```json
  // GET /_search
  {
      "query": {
          "script_score": {
              "query": {
                  "match": { "message": "elasticsearch" }
              },
              "script": {
                  "source": "_score / 10 "
              }
          }
      }
  }
  ```

  - 주의 사항

    - 비용이 많이 드는 query이므로 `search.allow_expensive_queries`가 false로 설정되어 있다면 사용할 수 없다.

    - `script`를 변경할 때 마다 다시 컴파일해야 하므로, `script`내에서 빈번히 변경되는 값은 `params`로 따로 빼 놓으면 불필요한 컴파일을 막을 수 있다.
    - 특정 document에 script에 사용하는 field의 값이 없는 경우를 check하고자 한다면, 아래와 같이 작성하면 된다.

  ```json
  "script" : {
      "source" : "doc['field'].size() == 0 ? 1 : doc['field'].value() * 2",
  }
  ```

 

- `script_score` query에서 사용할 수 있는 함수들

  - Elasticsearch는 `script_score`에서 사용할 수 있도록 미리 몇 개의 함수를 만들어 두었다.
    - 이 함수들과 동일한 방식을 가진 script를 직접 작성하는 것 보다 미리 정의된 함수를 사용하는 것이 더 효율적이다.
    - 이 함수들은 Elasticsearch 내부적으로 최적화가 되어 있기 때문이다.
  - `saturation`
    - `saturation(value, k) = value/(k + value)`
  - `sigmoid`
    - `sigmoid(value, k, a) = value^a / (k^a + value^a)`
  - `randomScore`
    - 0이상 1미만의 점수를 고르게 분배하여 무선적인 점수를 생성한다.
    - `randomScore(<seed>[,field_name])` 형태로 사용한다.
    - 만약 `field_name`이 생략된 경우 내부적으로 Lucene document id를 사용하는데, merge로 인해 document id가 변경될 경우 값이 점수가 달라질 수 있다는 점에 유의해야 한다.
    - 또한 설정한 `field_name`에 해당하는 값이 같고, 같은 shard에 속해 있는 문서들 끼리는 같은 점수를 받게 되므로, 고유한 값을 가지는 field를 `field_name`의 값으로 사용하는 것이 좋다.

  - `decay`
    - 숫자 field, geo field, date field 마다 사용 방법이 다르다.
    - 각 field별 사용법은 공식문서 참고
  - 그 밖에 `dense_vector` field에만 사용할 수 있는 함수들이 있는데, 이는 아래에서 설명한다.



- `dense_vector` field에서 사용할 수 있는 함수들.

  - Script 내에서 아래와 같이 vector에 접근할 수 있다.
    - `doc[<field>].vectorValue`: vector의 값을 반환한다.
    - `doc[<field>].magnitude`: vector의 magnitude를 반환한다.
  - `cosineSimilarity`
    - 주어진 query vector와 document vector 사이의 cosine similarity를 계산한다.

  ```json
  "script": {
      "source": "cosineSimilarity(params.query_vector, 'my_dense_vector_field') + 1.0", 
      "params": {
          "query_vector": [4, 3.4, -0.2]  
      }
  }
  ```

  - `dotProduct`
    - 주어진 query vector와 document vector 사이의 dot product를 계산한다.

  ```json
  "script": {
      "source": """
          double value = dotProduct(params.query_vector, 'my_dense_vector');
     		return sigmoid(1, Math.E, -value); 
  	""",
      "params": {
          "query_vector": [4, 3.4, -0.2]
      }
  }
  ```

  - `l1norm`
    - 주어진 query vector와 document vector 사이의 L<sup>1</sup> distance (Manhattan distance)를 계산한다.
    - `_score`에 두 vector 사이의 거리값이 오기 때문에, `_score`가 클수록 두 vector 사이의 연관성이 없다는 것을 의미한다.
    - 따라서, 1을 L<sup>1</sup> distance로 나눠서 L<sup>1</sup> distance의 역수를 `_score`로 사용한다.

  ```json
  "script": {
          "source": "1 / (1 + l1norm(params.queryVector, 'my_dense_vector'))", 
          "params": {
            	"queryVector": [4, 3.4, -0.2]
          }
  }
  ```

  - `l2norm`
    - 주어진 query vector와 document vector 사이의 L<sup>2</sup> distance (Euclidean distance)를 계산한다.
    - L<sup>1</sup> distance와 마찬가지 이유로 L<sup>2</sup> distance의 역수를 `_score`로 사용한다.

  ```json
  "script": {
      "source": "1 / (1 + l2norm(params.queryVector, 'my_dense_vector'))",
      "params": {
          "queryVector": [4, 3.4, -0.2]
      }
  }
  ```

  - 주의사항
    - `cosineSimilarity`, `dotProduct`, `l1norm`,  `l2norm` 함수들은 script 내에서 한 번만 호출하는 것이 권장된다.
    - 만일 이들을 loop 내에서 여러번 호출해야하는 경우가 있을 경우, 위 함수들을 사용하지 말고 `doc[<field>].vectorValue` 등을 사용하여 script를 직접 작성하는 것을 권장한다.



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







### Function score query

- Function score query

  - 쿼리를 통해 검색 된 문서들의 score를 조정할 수 있게 해준다.
  - score funcion이 score를 계산하는데 많은 자원을 소모하고, 문서 집합의 점수를 계산하는데 필요한 자원이 충분한 경우에 유용할 수 있다.
  - `script_score` query가 보다 단순하므로, 가능하면 `script_score` query를 쓰는 것이 권장된다.
  - Script score와 달리 여러 개의 함수를 사용할 수 있다.
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
  - `score_mode`
    - function에 의해 계산된 score 값들이 어떻게 결합될지를 결정하는 파라미터
    - 만일 scocre_mode가 avg로 설정되었을 경우에, 점수들은 weighted average로 결합된다.
    - 예를 들어 두 개의 함수가 각기 1, 2를 점수로 반환하였고, 각각의 weight가 3, 4로 주어졌다면, 점수는 `(1*3+2*4)/2`가 아닌`(1*3+3*4)/(3+4)`로 계산된다.
    - `multifly`: 점수를 곱한다(기본값).
    - `sum`: 점수를 합산한다.
    - `avg`: 점수의 평균을 낸다.
    - `first`: matching filter를 가지고 있는 첫 번째 function을 적용한다.
    - `max`: 점수들 중 최댓값을 사용한다.
    - `min`: 점수들 중 최솟값을 사용한다.
  
  ```json
  // GET test/_search
  // 예를 들어 아래와 같이 `sum`으로 주면 function A로 계산된 점수와 function B로 계산된 점수를 더한다.
  {
    "query": {
      "function_score": {
        "query": {
          "match": {
            "foo": "dog"
          }
        },
        "score_mode": "sum",
        "functions": [
          // function A
          {
            "filter": { "match": { "foo": "cat" } },
            "weight": 100
          },
          // function B
          {
            "filter": { "match": { "foo": "cute" } },
            "weight": 10
          }
        ]
      }
    }
  }
  ```
  
  - `max_boost`
    - 계산된 점수의 최댓값을 설정할 수 있다.
    - 만일 계산 된 점수가 `max_boost`에 설정한 값 보다 높을 경우  점수는 `max_boost`에 설정한 값이 되게 된다.
    - 기본 값은 FLT_MAX(실수 형식으로 포함할 수 있는 최댓값)이다.
  - `boost_mode`
    - 기존 점수와 function score로 새롭게 계산된 점수로 어떻게 최종 score를 계산할지를 설정하는 옵션이다.
    - `multifly`: 쿼리 score와 function score를 곱한다(기본값).
    - `replace`: 기존 점수는 사용하지 않고, function score만 사용한다.
    - `sum`: 쿼리 score와 function score를 더한다.
    - `avg`: 쿼리 score와 function score의 평균을 낸다.
    - `max`: 점수들 중 최댓값을 사용한다.
    - `min`: 점수들 중 최솟값을 사용한다.
  
  ```json
  GET test/_search
  {
    "query": {
      "function_score": {
        "query": {
          "match": {
            "foo": "dog"
          }
        },
        "boost_mode": "sum",
        "functions": [
          {
            "filter": { "match": { "foo": "cat" } },
            "weight": 100
          },
          {
            "filter": { "match": { "foo": "cute" } },
            "weight": 10
          }
        ]
      }
    }
  }
  ```
  
  - `min_score`
    - 기본적으로, 조정 된 점수는 어떤 문서가 match될지에 영향을 주지 않는다.
    - `min_score`는 특정 점수를 충족하지 못하는 문서를 제외시킨다. 
    - `min_score`가 동작하려면 쿼리에서 반환 된 모든 문서에 점수를 매긴 다음 하나씩 필터링 해야 한다.



- script score

  - `function_score` 내에서 `script_score`를 사용할 수 있다.
  - 예시

  ```json
  // GET /_search
  {
    "query": {
      "function_score": {
        "query": {
          "match": { "message": "elasticsearch" }
        },
        "script_score": {
          "script": {
            "source": "Math.log(2 + doc['my-int'].value)"
          }
        }
      }
    }
  }
  ```



- weight

  - weight를 score에 곱한 score를 얻기 위해 사용한다.
    - 반드시 float 값을 줘야 한다.
  - weight를 사용하는 이유
    - 점수는 각기 다른 척도로 계산 될 수 있으며, 때때로 점수에 각기 다른 함수를 적용하길 원할 수 있다.
    - 따라서 이를 위해 각 함수가 계산하는 점수를 조정하기 위해 `weight`를 사용한다.

  - `weigth`는 함수마다 하나씩 선언되며, 각각의 `weight`는 함수가 계산한 점수와 곱해진다.
    - 만일 함수의 선언 없이 `weigth`만 정의할 경우, `weight`는 `weight` 그 자체를 반환하는 함수처럼 동작한다.

  - 특정 쿼리에 설정 한 부스트 값은 정규화 되는 반면, weight를 통해 곱해진 점수는 정규화 되지 않는다.
  - 예시

  ```bash
  "weight" : float
  ```



- random

  - 0이상 1미만의 랜덤한 score를 생성한다.
    - 기본값으로 무선적인 값 생성을 위해 내부 Lucene 문서의 id들을 사용한다.
    - 이는 매우 효율적이지만 문서들이 병합에 의해 다시 넘버링 되기 때문에 reproducible하지는 않다.
    - reproducible하게 사용하려면 `seed`와 `field`를 주면 된다(`seed` 값과 `field` 값을 동일하게 주면 항상 동일한 값을 얻을 수 있다.).
  - 최종 score는 seed, 점수가 매겨질 documents들의 field의 최솟값, 인덱스명과 샤드 id에 기반한 값을 기반으로 계산되므로, 같은 값을 가지고 있지만 다른 인덱스에 저장된 문서들은 각기 다른 값을 갖게 된다. 
    - 그러나, 같은 샤드에 같은 field의 같은 값을 지닌 문서들은 동일한 score를 갖게 된다.
    - 따라서 모든 document들이 고윳값을 가지고 있는 field(주로 `_seq_no` field)를 사용하는 것이 권장된다.
    - 단, 문서에 변경사항이 있으면 `_seq_no`도 변경되므로 점수도 변경되게 된다.
  - 예시

  ```json
  // GET /_search
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



- `field_value_factor`

  - 점수에 가중치를 주기 위해 document에 있는 field를 사용하는 방식이다.
  - 만일 여러 값을 가진 filed를 사용할 경우, 첫 번째 값만 가중치 계산에 사용된다.
  - 상세 옵션은 [공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html#function-field-value-factor) 참고
  - 예시

  ```json
  // GET /_search
  {
    "query": {
      "function_score": {
        "field_value_factor": {
          "field": "my-int",
          "factor": 1.2,
          "modifier": "sqrt",
          "missing": 1
        }
      }
    }
  }
  ```



- `function_score` query를 `script_score` query로 변환하기.

  - `script_score` query가 `function_score` query보다 단순하므로, 가능하면 `script_score`를 쓰는 사용하는 것이 권장된다.
    - 아래와 같은 `function_score`query의 function들을 `script_score` query로 변환하는 것이 가능하다.
  - `weight`
    - `weight` function은 `script_score`로 아래와 같이 변환할 수 있다.

  ```json
  "script" : {
      "source" : "params.weight * _score",
      "params": {
          "weight": 2
      }
  }
  ```

  - `random_score`
    - `script_score`의 `randomScore`로 변환이 가능하다.
  - `field_value_factor`
    - 아래와 같이 `script_score`로 변환이 가능하다.

  ```json
  "script" : {
      "source" : "Math.log10(doc['field'].value * params.factor)",
      "params" : {
          "factor" : 5
      }
  }
  ```










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

  - 편집거리를 사용하여 비슷한 단어를 제안한다.
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
  
  - 한글의 경우 영문보다 복잡한 유니코드 체계를 가지고 있어 일반적인 방법으로는 오타 교정을 할 수 없다.
    - 한글을 자소 단위로 분해해주는 플러그인을 설치하여 이를 통해 형태소 분석을 해야 한다.



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







