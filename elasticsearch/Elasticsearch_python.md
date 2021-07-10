- readtimeout error

  - 아래와 같이 ES 클라이언트를 생성후 ES에 요청을 보냈을 때,  readtimeout 에러가 뜨는 경우가 있다.

  ```python
  from elasticsearch import Elasticsearch
  
  es = Elasticsearch('10.11.12.103:9200')
  ```

  - 이럴 때는 아래와 같이 다양한 옵션을 통해 timeout 관련 설정을 해줄 수 있다.
    - timeout은 기본값은 10으로, timeout error가 발생하기 까지의 시간(초)을 의미한다.
    - max_retries는 error가 발생할 경우 최대 몇 번까지 재시도를 할지 설정하는 것이다.
    - retry_on_timeout는 timeout이 발생했을 때, 재시도를 할지 여부를 설정하는 것이다.

  ```python
  from elasticsearch import Elasticsearch
  
  es = Elasticsearch('10.11.12.103:9200', timeout=30, max_retries=5,retry_on_timeout=True)
  ```




- CSV 파일 bulk

  ```python
  import csv
  # helpers import
  from elasticsearch import helpers, Elasticsearch 
  
  
  es = Elasticsearch(['localhost:9200'])
  
  with open('/test.csv') as f: 
      reader = csv.DictReader(f) 
      helpers.bulk(es, reader, index="my_index")
  ```

  