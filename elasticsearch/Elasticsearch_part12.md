# 구현

## Exact Match 구현

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

