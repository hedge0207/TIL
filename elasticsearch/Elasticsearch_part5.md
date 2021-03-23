# bulk API

- bulk API
  - 한 번에 다량의 문서를 색인, 삭제, 수정할 때 사용할 수 있는 API이다.
  - 사용하는 이유
    - 하나의 문서를 처리할 때 시스템은 클라이언트와 네트워크 세션을 맺고 끊기를 반복하기 때문에 여러 건의 문서를 처리할 때 단건으로 맺고 끊기를 반복하는 방식으로 처리하면 시스템에 부하를 일으킨다.
    - 따라서 여러 건의 문서를 처리할 때는 bulk API를 통해 문서 색인, 업데이트 등의 작업을 모아서 한 번에 수행하는 것이 좋다.
  - 성능
    - 단일 색인 요청을 1만번 실행 했을 때 1분 52초가 소요되었다.
    - bulk API로 동일한 문서들을 색인하면 1초가 채 걸리지 않는다.



- bulk API 사용 방법

  - 수행할 동작들을 json 형태로 나열하여 사용
    - 처음에는 수행할 동작 index를 정의하고 동작을 수행할 인덱스의 메타 데이터를 나열한다.
    - 다음 줄에 실제 색인할 문서를 정의한다.

  ```bash
  $ curl -XPOST "localhost:9200/_bulk?pretty" -H 'Content-type:application/json' -d '{
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"1"}}
  {"mydoc":"first doc"}
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"2"}}
  {"mydoc":"second doc"}
  {"index":{"_index":"bulk_index", "_type":"_doc", "_id":"3"}}
  {"mydoc":"third doc"}
  }
  ```

  - 수행할 동작들을 JSON 파일로 작성하여 수행
    - JSON 파일의 마지막 줄에 빈 줄이 한 줄 있어야 한다.

  ```json
  // bulk.json 파일
  {"index":{"_index":"test","_type":"_doc","_id":"1"}}
  {"field":"value one"}
  {"index":{"_index":"test","_type":"_doc","_id":"2"}}
  {"field":"value two"}
  {"delete":{"_index":"test","_type":"_doc","_id":"2"}}
  {"create":{"_index":"test","_type":"_doc","_id":"3"}}
  {"field":"value three"}
  {"update":{"_index":"test","_type":"_doc","_id":"1"}}
  {"doc":{"field":"value two"}}
  
  ```

  - 실행

  ```bash
  $ curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-type:application/json' --data-binary @bulk.json
  ```



- bulk API 동작

  | bulk API 동작 | 설명                                                         |
  | ------------- | ------------------------------------------------------------ |
  | index         | 문서 색인. 인덱스에 지정한 문서 아이디가 있을 때는 업데이트  |
  | create        | 문서 색인. 인덱스에 지정한 문서 아이디가 없을 때에만 색인 가능 |
  | delete        | 문서 삭제                                                    |
  | update        | 문서 변경                                                    |
  - URL에 인덱스의 이름과 타입 정보를 주면 bulk API의 메타 정보로 문서의 id만 줄 수 있다.
    - 문서의 id도 입력하지 않을 경우 ES가 문서의 id를 임의로 만들어서 색인할 수도 있다.

  ```bash
  $ curl "localhost:9200/my_index/_doc/_bulk?pretty" -H 'Content-type:application/json' -d '{
  {"index":{"_id":"4"}}
  {"mydoc":"first doc"}
  {"update":{"_id":"4"}}
  {"doc":{"mydoc":"updated doc"}}
  {"delete":{"_id":"4"}}
  }
  ```





























