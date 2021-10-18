- pymongo

  > https://pymongo.readthedocs.io/en/stable/

  - mongodb 공식 라이브러리
  - Python에서 mongodb를 보다 쉽게 사용할 수 있게 해주는 라이브러리.
  - 설치

  ```bash
  $ pip install pymongo
  ```



- 사용해보기

  - mongodb에 연결하기 위한 클라이언트를 생성한다.

  ```python
  import pymongo
  
  # 방법1
  clinet = MongoClient('<mongodb host>', '<mongodb port>')
  
  # 방법2
  clinet = MongoClient('mongodb://<mongodb host>:<mongodb port>/')
  
  # 인증이 필요할 경우
  client = MongoClient("<mongodb host>:<mongodb port>",username="<username>",password="<password>",authSource="admin")
  ```
  
  