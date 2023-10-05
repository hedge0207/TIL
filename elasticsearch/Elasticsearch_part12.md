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




# Elasticsearch shard allocation

> Part2의 샤드 배치 방식 변경에 넣을 것

- Elasticsearch는 shard가 어떤 노드에 할당될지를 설정할 수 있는 다양한 설정 값들을 제공한다. 
  - 특정 index의 shard가 어떤 node에 할당될지를 설정할 수 있는 [index level](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html)의 설정값들이 있다.
  - [Cluster level](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#cluster-shard-allocation-filtering)에서 어떻게 할당할지를 설정할 수 있는 설정값들이 있다.



## Index level

- Index level에서 shard 할당 설정하기

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html#shard-allocation-filtering

  - Node의 속성값을 기반으로 특정 index의 shard가 어떤 노드에 할당될지를 설정할 수 있다.
    - ILM에서 사용하는 data tier에 따라 shard를 재할당하는 방식도 이 설정값을 기반으로 하는 방식이다.
    - Custom한 속성값을 사용할 수도 있고, Elasticsearch에 내장되어 있는 속성값들을 사용할 수도 있다.
  - Index level에서 shard 할당 방식을 설정한다해도 예상과 다르게 동작할 수 있다.
    - Index level 설정은 cluster level 설정과 결합하여 동작한다.
    - Primary shard와 replica shard가 같은 node에 있을 수 없다는 것 같은 shard 할당의 기본적인 제약을 무시하면서 동작하지는 않는다.



- Custom 속성값 작성하기

  - 각 node의 `elasticsearch.yml` 파일에 아래와 같이 `node.attr.<custom_attribute>: <attribute>` 형식으로 작성한다.

  ```yaml
  node.attr.my_attr: foo
  ```

  - 만일 Docker compose를 사용해 cluster를 구성한다면, 아래와 같이 하면 된다.

  ```yaml
  version: '3.2'
  
  
  services:
    node1:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node1
      environment:
        - node.name=node1
        - node.attr.my_attr=foo
        # ...
  
    node2:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node2
      environment:
        - node.name=node2
        - node.attr.my_attr=bar
        # ...
  
    node3:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node3
      environment:
        - node.name=node3
        - node.attr.my_attr=baz
        # ...
  ```

  - `_cat/nodeattrs` API를 통해 attribute가 제대로 설정되었는지 확인할 수 있다.

  ```http
  GET _cat/nodeattrs
  ```

  - 그 후 index를 생성할 때 `settings.index.routing.allocation.include.<custom_attribute>`에 attribute를 입력하면, 해당 attribute에 해당하는 node에 할당된다.
    - 아래의 경우 node1이나 2에 할당되게 된다.

  ```json
  // PUT test
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "my_attr":"foo,bar"
                      }
                  }
              }
          }
      }
  }
  ```

  - 만일 `node.attr.<custom_attribute>`에 설정해준 적 없는 값을 줄 경우 어떤 node에도 할당되지 않는다.

  ```json
  // 아래의 경우나
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "qwe":"foo"
                      }
                  }
              }
          }
      }
  }
  
  // 아래의 경우에는 아무 곳에도 할당되지 않는다.
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "my_attr":"qwe"
                      }
                  }
              }
          }
      }
  }
  ```



- 위에서는 include를 사용했지만 include 외에 exclude, require를 사용하는 것도 가능하다.
  - `settings.index.routing.allocation.include.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`이나 `attr2`로 설정된 node 들 중 한 곳에 할당된다.
  - `settings.index.routing.allocation.require.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`과 `attr2`가 모두 설정된 node에만 할당된다.
  - `settings.index.routing.allocation.include.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`과 `attr2`가 모두 설정되지 않은 node에만 할당된다.



- 내장 속성 사용하기

  - 아래의 bulit-in attribute들을 사용할 수 있다.
    - `_name`: node의 이름
    - `_host_ip` : node의 host ip
    - `_publish_ip` : node의 publish ip
    - `_ip`: `_host_ip` 혹은 `_publish_ip`
    - `_host`: node의 hostname
    - `_id`: node의 id
    - `_tier`: node의 data tier
  - 예를 들어 아래 index의 shard는 node1이라는 이름을 가진 node에 할당된다.

  ```json
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "_name":"node1"
                      }
                  }
              }
          }
      }
  }
  ```



- 아래와 같이 index 생성 후에 변경하는 것도 가능하다.

  - 변경 사항은 바로 반영된다.
  - 그러나 이는 매우 무거운 작업이므로 빈번히 사용하는 것은 권장되지 않는다.

  ```json
  // PUT test/_settings
  {
    "index.routing.allocation.include._name": "node2"
  }
  ```



- Replica shard 역시 설정을 공유한다.

  - 따라서 아래와 같이 attribute의 값을 하나만 줄 경우 replica의 할당이 이루어지지 않을 수 있다.
    - 아래에서는 `_name`라는 built-in attribute의 값으로 `node1`이라는 하나의 값만을 줬다.
    - Primary와 replica는 이 값을 공유하므로 primary와 replica 모두 `node1`에 할당하려 할 것이다.
    - 그런데 `node1`에 primary가 할당되면, replica는 primary와 같은 node에 할당될 수 없으므로, unassigned 상태가 된다.

  ```json
  PUT test
  {
      "settings": {
          "index": {
              "routing": {
                  "allocation": {
                      "include": {
                          "_name": "node1"
                      }
                  }
              }
          }
      }
  }
  ```

  - 이를 `_cluster/allocation/explain` API를 통해 미할당된 이유를 확인해보면 아래와 같다.
    - `node2`와 `node3`의 my_attr 값은 각각 bar와 baz인데 index의 my_attr값은 foo이므로 node2, node3에는 할당할 수 없고, `node1`에는 이미 primary shard가 할당되어 있으므로 할당할 수 없다는 설명을 확인할 수 있다.

  ```json
  // _cluster/allocation/explain
  {
    // ...
    "index": "test",
    // ...
    "primary": false,
    "current_state": "unassigned",
    // ...
    "node_allocation_decisions": [
      {
        // ...
        "node_name": "node3",
        // ...
        "node_attributes": {
          // ...
          "my_attr": "baz",
          // ...
        },
        // ...
        "deciders": [
          {
            "decider": "filter",
            "decision": "NO",
            "explanation": """node does not match index setting [index.routing.allocation.include] filters [_name:"node1"]"""
          }
        ]
      },
      {
        // ...
        "node_name": "node2",
        // ...
        "node_attributes": {
          "my_attr": "bar",
          // ...
        },
        // ...
        "deciders": [
          {
            "decider": "filter",
            "decision": "NO",
            "explanation": """node does not match index setting [index.routing.allocation.include] filters [_name:"node1"]"""
          }
        ]
      },
      {
        // ...
        "node_name": "node1",
        // ...
        "node_attributes": {
          // ...
          "my_attr": "foo"
        },
        // ...
        "deciders": [
          {
            "decider": "same_shard",
            "decision": "NO",
            "explanation": "a copy of this shard is already allocated to this node [[test][0], node[bDGjyx9-RTGnb54PVlGxFQ], [P], s[STARTED], a[id=S1dC8DYGScqaUMt_BJ296Q], failed_attempts[0]]"
          }
        ]
      }
    ]
  }
  ```

  - 따라서 replica shard의 할당도 고려하여 아래와 같이 복수의 attribute 값을 설정해야한다.

  ```json
  PUT test
  {
      "settings": {
          "index": {
              "routing": {
                  "allocation": {
                      "include": {
                          "_name": "node1,node2"
                      }
                  }
              }
          }
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

