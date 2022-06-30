# Elasticsearch 8

- client

  - elasticsearch package 8.X 이상을 설치해야 한다.
  - 기존과 달리 `ca_certs`, `basic_auth parameter`를 넘겨야 한다.

  ```python
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("https://localhost:9210", 
                          ca_certs="./http_ca.crt", 
                          basic_auth=("elastic", "<password>"))
  ```
  
  - Elasticsearch Python client의 버전이 7.x일 경우 `basic_auth`가 아닌 `http_auth` 파라미터를 넣는다.
  
  ```python
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("https://localhost:9210", 
                          ca_certs="./ca.crt", 
                          http_auth=("elastic", "<password>"))
  
  # 혹은 아래와 같이 url에 사용자명과 password를 추가한다.
  es_client = Elasticsearch("https://elastic:<password>@localhost:9210", 
                          ca_certs="./ca.crt")
  ```
  
  




# elasticsearch-dsl

- elasticsearch-dsl

  - Python에서 보다 깔끔하게 dsl을 작성하도록 도와주는 library
    - Python에서 ES를 사용하다보면 쿼리 때문에 코드가 지저분해진다.
    - elasticsearch-dsl을 사용하면 보다 깔끔하게 작성이 가능하다.
  - 설치

  ```bash
  $ pip install elasticsearch-dsl
  ```



# ETC

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

