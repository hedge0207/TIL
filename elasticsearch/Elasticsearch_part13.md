# alias

- Alias
  - Alias는 index 혹은 data stream에 별칭을 부여하는 기능이다.
    - Elasticsearch에서 제공하는 대부분의 API에서 index 혹은 data stream을 입력하는 자리에 alias를 입력할 수 있다.
  - Data stream alias와 index alias가 있으며, 하나의 alias가 index와 data stream을 모두 가리킬 수는 없다.
    - 또한 data stream의 backing index에 alias를 추가할 수 없다.



- Alias 추가 및 제거

  - 아래와 같이 `add` action을 사용하여 alias를 추가할 수 있다.
    - `index` parameter에 wildcard(`*`)를 사용할 수 있다.
    - 만약 wildcard가 index와 data stream을 모두 matching시킨다면 error가 반환된다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - Alias 제거
    - 아래와 같이 `remove` action을 사용하여 alias를 추가할 수 있다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "remove": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - `actions`에 한 번에 여러 개의 action을 설정하는 것도 가능하다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "remove": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      },
      {
        "add": {
          "index": "logs-my_app-default",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - Index 생성시에 alias를 설정할 수도 있다.

  ```json
  // PUT alias-test
  {
    "aliases": {
      "my-alias": {}
    }
  }
  ```

  - Alias가 가리키는 index 혹은 data stream이 모두 삭제될 경우 alias도 함께 삭제된다.



- Alias 조회

  - 아래와 같이 조회할 수 있다.

  ```http
  GET _alias
  ```

  - 앞에 index 혹은 data stream을 입력하여 해당 index 혹은 data stream에 설정된 alias를 볼 수 있다.

  ```http
  GET <index | data_stream>/_alias
  ```

  - 뒤에 alias를 입력하여 alias에 해당하는 index와 data stream을 볼 수 있다.

  ```http
  GET _alias/<alias>
  ```



- 부가 기능

  - Write index
    - `is_write_index` parameter를 true로 줄 경우 alias로 보낸 write 요청을 해당 index 혹은 data stream으로 보낸다.
    - 만약 alias가 여러 개의 index 혹은 data stream을 가리키고 있으면서, `is_write_index`가 설정되어 있지 않을 경우, write 요청은 거절된다.
    - 만약 alias가 가리키는 index가 하나뿐일 경우 해당 index는 write index로 동작한다. 
    - 그러나 alias가 가리키는 data stream이 하나라고 하더라도 data stream은 write가 불가능하다. 
    - 따라서 alias가 가리키는 data stream이 하나라 할지라도 data stream은 반드시 `is_write_index`를 설정해야한다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "logs-my_app-default",
          "alias": "logs",
          "is_write_index": true
        }
      }
    ]
  }
  ```

  - `filter`를 통해 alias가 접근할 수 있는 문서를 제한할 수 있다.
    - 아래와 같이 설정할 경우 `my-alias`라는 alias는 `my-index-2099.05.06-000001` index의 전체 doucment 중 `user.id`가 "kimchy"인 doucment에만 접근이 가능하다.

  ```json
  POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "filter": {
            "bool": {
              "filter": [
                {
                  "term": {
                    "user.id": "kimchy"
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
  ```

  - routing
    - `routing` 옵션을 사용하여 request를 특정 shard에 routing하는 것이 가능하다.
    - `routing`으로 검색과 색인에 동일한 routing 값을 사용할 수도 있고, `search_routing`과 `index_routing`을 따로 설정하는 것도 가능하다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "routing": "1"
        }
      }
    ]
  }
  
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "search_routing": "1",
          "index_routing": "2"
        }
      }
    ]
  }
  ```

  



