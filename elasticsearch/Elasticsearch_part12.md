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

