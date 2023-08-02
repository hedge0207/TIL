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

