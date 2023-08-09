# Elasticsearch 최적화

## 검색 최적화

- `_id` field를 retrieve하지 않기

  > https://luis-sena.medium.com/stop-using-the-id-field-in-elasticsearch-6fb650d1fbae

  - Elasticsearch의 모든 document는 `_id` field를 갖는다.
    - `_id` field는 stored_fields를 통해 저장되는데, stored_fields는 doc_values와 비교했을 때 읽어올 때 overhead가 더 크다.
    - 따라서 `_id` field를 retrieve하지 않는 것 만으로도 검색 성능을 향상시킬 수 있다.
  - 테스트용 data 색인
    - `_id` 값과 동일한 값을 저장할 `my_id` field도 함께 색인한다.

  ```python
  from elasticsearch import Elasticsearch, helpers
  from faker import Faker
  
  INDEX_NAME = "test-index"
  es_client = Elasticsearch("http://localhost:9200")
  fake = Faker()
  
  bulk_data = [
      {
          "_index":INDEX_NAME, 
          "_id": i, 
          "_source":{"title":fake.sentence(), "content":fake.text(), "my_id":i}
      }
      for i in range(1_000_000)]
  helpers.bulk(es_client, bulk_data)
  ```

  - 검색 속도 비교
    - `_id`를 반환 받지 않고, `_id`와 동일한 값을 doc_values를 사용하여 retrieve 하는 쪽이 훨씬 빠른 것을 확인할 수 있다.
    - 현재는 비교적 크기가 작은 document를 대상으로 했지만, document의 크기가 커질수록 차이가 커질 수 있다.

  ```python
  from elasticsearch import Elasticsearch, helpers
  from faker import Faker
  
  N = 10000
  without_id = 0
  with_id = 0
  for i in range(N):
      query = {
          "match":{
              "content":fake.word()
          }
      }
      es_client.indices.clear_cache(index=INDEX_NAME)
      res = es_client.search(index=INDEX_NAME, stored_fields="_none_", docvalue_fields=["my_id"], query=query)
      without_id += res["took"]
  
      es_client.indices.clear_cache(index=INDEX_NAME)
      res = es_client.search(index=INDEX_NAME, _source=False, query=query)
      with_id += res["took"]
  
  print(without_id / N)	# 1.1176
  print(with_id / N)		# 2.3076
  ```

  - `_id`를 제외시켰을 때 속도가 빨라지는 이유
    - `_id`가 저장되는 stored fields는 row 형태로 저장되기에 column 형태로 저장되는 doc_values에 비해 retrieve 속도가 느리다.



### Number of Segments

- Segment의 개수가 늘어날수록 읽어야 하는 segment의 개수가 많아지기에 검색 속도가 감소하게 된다.

  - 따라서 검색 속도를 증가시키기 위해서는 segment의 개수를 줄여야한다.
  - Force merge API를 통해 segment들을 병합시킬 수 있다.

  ```http
  POST <target_index>/_forcemerge
  ```

  - Force merge API는 아래와 같은 query parameter들을 받는다.
    - `flush`: Force merge 이후에 flush를 실행할지 여부를 설정하며, 기본값은 true이다.
    - `wait_for_completion`: Force merge request가 완료될 때 까지 block될지 여부를 설정하며, 기본값은 true이다.
    - `max_num_segments`: 몇 개의 segment로 병합할지를 설정하며, 기본값은 merge를 수행해야하면 수행하고, 그렇지 않다면 수행하지 않는 것이다. 완전한 최적화를 하고자 한다면 1로 설정하면 된다.
    - `only_expunge_deletes`: `index.merge.policy.expunge_deletes_allowed`에서 설정해준 값(기본값은 10) 이상의 비율로 삭제된 document를 저장하고 있는 segment들을 삭제할지를 설정하며, 기본값은 false이다.
    - `max_num_segments`와 `only_expunge_deletes`는 동시에 줄 수 없다.
  - Force merge API는 읽기 전용 index(현재 뿐만 아니라 추후에도 더 이상 색인이 이루어지지 않는 index)에만 사용하는 것을 추천한다.
    - Document들이 수정되거나 삭제되어도, 기존 document는 즉시 삭제되지 않고, tombstone으로 표시해두는데 이를 soft-delete라고 한다.
    - Soft-delete 된 문서들은 segment가 병합될 때 자동으로 정리된다.
    - 그러나 force merge를 실행하면 5GB 이상의 매우 큰 segment가 생성될 수도 있다.
    - 문제는, segment merge policy가 5GB까지만 병합 대상으로 본다는 것이다.
    - 따라서 한 segment의 크기가 5GB가 넘어가게 되면 더 이상 병합이 발생하지 않게된다.
    - 만약 이 segment에 저장된 문서들의 대부분이 삭제된다고 해도, 이 segment는 병합 대상이 아니므로 해당 문서들은 영원히 삭제되지 않은채로 남아있게 된다.
    - 이는 disk의 사용량을 증가시킬뿐만 아니라 검색 속도도 느리게 만들 수 있다.
  - ILM policy를 사용하여 자동으로 segment의 개수와 크기를 최적화할 수 있다.



- Segment 개수에 따른 검색 속도 측정

  - Test용 data 생성

  ```python
  from faker import Faker
  import josn
  import random
  
  
  fake = Faker()
  for i in range(10):
      docs = []
      for _ in range(100_000):
          docs.append({
              "title":fake.sentence(),
              "description":"".join([fake.text() for _ in range(10)]),
              "pages": random.randrange(1, 1500),
              "author":fake.name(),
              "published_date":fake.date()
          })
      with open("./fake_data/fake_{}.json".format(i), "w") as f:
          json.dump(docs, f)
  ```

  - Test data 색인

  ```python
  import json
  
  from elasticsearch import Elasticsearch, helpers
  
  
  INDEX_NAME = "test-index"
  es_client = Elasticsearch("http://localhost:9200")
  
  for i in range(10):
      with open("./fake_data/fake_{}.json".format(i), "r") as f:
          fake_data = json.load(f)
      bulk_data = [{"_index":INDEX_NAME, "_source":source} for source in fake_data]
      helpers.bulk(es_client, bulk_data)
  ```

  - Segment 개수 조정.
    - Segment의 개수를 15개로 조정한다.

  ```http
  POST test-index/_forcemerge?max_num_segments=15
  ```

  - 평균 검색 속도 측정

  ```python
  from faker import Faker
  
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("http://localhost:9200")
  fake = Faker()
  N = 10000
  content_term = " ".join([fake.word() for _ in range(5)])
  title_term = " ".join([fake.word() for _ in range(5)])
  prefix = fake.word()
  for i in range(N):
      query = {
          "bool": {
              "should": [
                  {
                      "match":{
                          "content": content_term
                      }
                  },
                  {
                      "match":{
                          "title": title_term
                      }
                  },
                  {
                      "match_phrase_prefix": {
                          "content": "{}.*".format(prefix)
                      }
                  }
              ]
          }
      }
      res = es_client.search(index="test-index", query=query)
      total_time += res["took"]
  
  print(total_time/N)
  ```

  - Segment의 수를 점차 감소시키면서 검색에 걸리는 시간을 기록한 결과는 아래 표와 같다.
    - 점점 검색에 걸리는 시간이 감소하는 것을 확인할 수 있다.

  | Segment 개수 | 평균 검색 시간(milliseconds) |
  | ------------ | ---------------------------- |
  | 15           | 11.18                        |
  | 10           | 11.17                        |
  | 5            | 10.23                        |
  | 1            | 9.41                         |

  







# 색인 최적화

> https://luis-sena.medium.com/the-complete-guide-to-increase-your-elasticsearch-write-throughput-e3da4c1f9e92

- Client의 최적화 전략
  - Bulk API 사용
    - Bulk API를 사용하여 색인하는 것이 문서를 한 건씩 색인하는 것 보다 훨씬 빠르다.
    - 단, benchmark를 통해 최적의 batch size를 정해야한다.
  - 병렬화
    - 여러 개의 worker를 통해 색인을 한다.
    - 단, Elasticsearch의 thread pool queue가 전부 차면 발생하는 `TOO_MANY_REQUESTS(429)` error등은 주의해야한다.



- Index 전략
  - `refresh_interval`을 조정한다.
    - 기본적으로 Elasticsearch는 매 초 refresh를 실행한다.
    - 만일 바로 검색될 필요가 없는 데이터라면, `refresh_interval`을 길게 줌으로써 색인 성능을 향상시킬 수 있다.
    - 색인 전에 `refresh_interval`을 늘린 후, 색인 후에 다시 돌려 놓는다.
  - 자동으로 생성되는 `_id`를 사용.
    - 자동으로 생성되는 `_id`를 사용할 경우 Elasticsearch가 `_id`의 고유성을 확인할 필요가 없으므로 색인 속도가 빨라질 수 있다.
    - 만약 Lucene friendly한 format으로 `_id`를 사용한다면, 자동 생성되는 `_id`를 사용하지 않아도 색인 속도가 크게 느려지지는 않는다.
  - Replica shard를 비활성화한다.
    - Replica shard가 있을 경우, primary에 색인이 완료된 후 replica에 복사까지 해야하므로 색인 속도가 느려진다.
    - 따라서 색인 전에 replica shard를 비활성화 한 후 색인이 완료되면 다시 활성화시킨다.



- Node 전략

  - Indexing Buffer size 관련 옵션을 조정한다.

    > https://www.elastic.co/guide/en/elasticsearch/reference/current/indexing-buffer.html

    - Elasticsearch가 색인을 위해 얼마만큼의 memory를 확보하고 있을지를 설정하는 옵션이다.
    - 기본값은 노드에 할당된 전체 heap memory의 10%이다.
    - 노드의 모든 shard들이 공유하는 값이다.

  - Translog 관련 옵션을 조정한다.

    > https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-translog.html#_translog_settings

    - Elasticsearch에서 flush가 실행되는 주기는 trasnlog의 size에 의해서 결정된다.
    - Translog가 일정 크기에 도달하면 flush가 실행되는데, flush가 실행되면 memory에 저장되어 있던 여러 개의 segment들이 하나로 병합되면서 disk에 저장된다.
    - 이는 비용이 많이 드는 작업이므로, 빈번하게 발생할 경우 색인 속도가 감소할 수 있다.
    - 따라서 trasnlog의 크기를 늘림으로써 색인 속도를 향상시킬 수 있다.
