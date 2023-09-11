- 일부 field만 update하기

  - 아래와 같이 문서 전체를 교체하는 방식이 아니라 일부 field만 수정할 수 있다.

  ```python
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("http://localhost:9200")
  INDEX_NAME = "my_index"
  
  es_client.update(index=INDEX_NAME, id="1", body={"doc":{"foo":"bar"}})
  ```

  