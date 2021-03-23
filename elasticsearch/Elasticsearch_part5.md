# bulk API

- bulk API
  - 한 번에 다량의 문서를 색인, 삭제, 수정할 때 사용할 수 있는 API이다.
  - 사용하는 이유
    - 하나의 문서를 처리할 때 시스템은 클라이언트와 네트워크 세션을 맺고 끊기를 반복하기 때문에 여러 건의 문서를 처리할 때 단건으로 맺고 끊기를 반복하는 방식으로 처리하면 시스템에 부하를 일으킨다.
    - 따라서 여러 건의 문서를 처리할 때는 bulk API를 통해 문서 색인, 업데이트 등의 작업을 모아서 한 번에 수행하는 것이 좋다.



- bulk API 사용 방법

  - 수행할 동작들을 json 형태로 나열하여 사용
    - 처음에는 수행할 동작 index를 정의하고 동작을 수행할 인덱스의 메타 데이터를 나열한다.
    - 

  ```bash
  $ curl "localhost:9200/_search?pretty" -H 'Content-type:application/json' -d '{
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"1"}}
  {"mydoc":"first doc"}
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"2"}}
  {"mydoc":"second doc"}
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"3"}}
  {"mydoc":"third doc"}
  }
  ```

  