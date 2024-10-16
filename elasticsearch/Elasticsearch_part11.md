# Elasticsearch 최적화

## 색인 성능 최적화

> https://luis-sena.medium.com/the-complete-guide-to-increase-your-elasticsearch-write-throughput-e3da4c1f9e92

- 색인 성능 최적화의 필요성
  - ES는 클러스터 환경으로 구축할 수 있기 때문에 노드 추가를 통해 색인 성능을 더 높일 수 있다.
  - 그러나 ES 설정을 변경함으로써 불필요한 리소스를 줄일 수 있고, 이를 통해 색인 성능을 향상시킬 수 있다.



- 정적 매핑 적용하기

  - 앞서(Elasticsearch_part1) 살펴본 동적 매핑과 정적 매핑을 다시 간단하게 표로 정리하면 다음과 같다.

  | 방식      | 장점                                   | 단점                            |
  | --------- | -------------------------------------- | ------------------------------- |
  | 동적 매핑 | 미리 매핑 정보를 생성하지 않아도 된다. | 불필요한 필드가 생길 수 있다.   |
  | 정적 매핑 | 필요한 필드만 정의해서 사용할 수 있다. | 미리 매핑 정보를 생성해야 한다. |

  - 정적 매핑의 이점
    - 동적 매핑을 사용하면 불필요한 매핑 정보가 생성될 수 있으며, 이러한 불필요한 매핑 정보는 불필요한 색인 작업을 유발하게 되어 색인 성능을 저하시킬 수 있다.
    - 반대로 정적 매핑을 사용하면 필요한 필드들만 정의해서 사용할 수 있고 불필요한 매핑 정보를 사용하지 않기 때문에 색인 성능을 향상시킬 수 있다.
  - 문자열 형태의 필드에서 색인 성능 차이가 더 크게 발생한다.
    - 기존에 정의되지 않은 필드에 문자열 데이터를 추가할 경우(즉 동적 매핑을 할 경우), text 타입으로 생성이 되지만 동시에 keyword 타입으로도 생성이 된다.
    - 즉 , 문자열 데이터에 대한 동적 매핑 결과는 text 타입과 keyword 타입 두개 의 타입을 만든다.
    - 또한 동적 매핑에 의해 생성되는 keyword 타입은 `ignore_above`라는 속성이 하나 더 붙는데 문자열 중 해당 길이 이상인 값은 색인에 포함하지 않는다는 뜻이다.
    - 정적 매핑으로 문자열 데이터에 대한 타입을 미리 text 혹은 keyword로 생성해 놓으면 두 번 해야 할 색인 작업이 한 번으로 줄어들게 된다.

  ```json
  // 정적 매핑으로 문자열 데이터를 담을 필드를 추가한 경우
  {
    "name" : {
      "type" : "text"
    }
  }
  // 동적 매핑으로 문자열 데이터를 추가한 경우
  "ename" : {
    "type" : "text",
    "fields" : {
        "keyword" : {
            "type" : "keyword",
            "ignore_above" : 256
        }
     }
  },
  ```



- refresh_interval 변경하기

  - refresh
    - ES는 색인되는 모든 문서들을 메모리 버퍼 캐시에 먼저 저장한 후 특정 조건이 되면 메모리 버퍼 캐시에 저장된 색인 정보나 문서들을 디스크에 세그먼트 단위로 저장한다.
    - 색인된 문서는 이렇게 세그먼트 단위로 저장되어야 검색이 가능해지며, 이런 일련의 작업들을 refresh라 한다.
  - refresh_interval
    - 이 refresh를 얼마나 주기적으로 할 것인지를 결정하는 값이 refresh_interval이다.
    - 기본값은 1초이다.
    - ES가 준 실시간 검색 엔진이라 불리는 것은 refresh_interval이 1초로 설정되어 있어 문서가 색인되고 1초 후에 검색이 가능하기 때문이다.
    - refresh 작업은 디스크 I/O를 발생시키기 때문에 성능을 저하시킬 수 있다.
    - 그렇다고 I/O 발생을 늦추기 위해 refresh_interval을 길게 주면 색인된 문서를 검색할 수 없어 ES 본연의 기능에 문제가 생길 수 있다.
  - refresh_interval 변경
    - 실시간 검색 엔진으로 사용하고자 한다면 1초로 설정해야 한다.
    - 그러나 대용량의 로그를 수집하는 것이 주된 목적이고 색인한 로그를 당장 검색해서 사용할 필요가 없다면 refresh_interval을 충분히 늘려서 색인 성능을 확보할 수 있다.
    - 만일 문서가 1초에 한 건씩 들어오고  refresh_interval이 1초라면 초당 한 건씩 디스크에 문서를 저장하게 되고 총 5 번의 Disk I/O가 발생한다.
    - 반면에 문서는 그대로 1초에 한 건씩 들어오지만 refresh_interval이 5초라면 5건의 문서를 한 번에 저장하게 되고 총 한 번의 Disk I/O만 발생한다.
    - 인덱스의 settings API를 통해 변경이 가능하다.

  ```bash
  # -1을 주면 아예 비활성화 하는 것이 가능하다.
  $ curl -XPUT "localhost:9200/my_index/_settings" -H 'Content-type: application/json' -d'{
  "index.refresh_interval":"2h"
  }
  ```



- bulk API

  - 복수의 요청을 한 번에 전송할 때 사용한다.
    - 동작을 따로따로 수행하는 것 보다 속도가 훨씬 빠르다.
    - 하나의 문서를 처리할 때 시스템은 클라이언트와 네트워크 세션을 맺고 끊기를 반복하기 때문에 여러 건의 문서를 처리할 때 단건으로 맺고 끊기를 반복하는 방식으로 처리하면 시스템이 부하를 일으킨다. 따라서 여러 건의 문서를 처리할 때는 bulk API를 통해 작업하는 것이 좋다.
    - 예를 들어 단 건씩 작업했을 때 112s가 걸리는데 bulk를 사용하면 1s가 채 걸리지 않을 정도로 차이가 많이 난다.
  - bulk API 동작
    - index: 문서 색인, 인덱스에 지정한 문서 아이디가 있으면 업데이트.
    - create: 문서 색인, 인덱스에 지정한 문서 아이디가 없을 때에만 색인 가능.
    - update: 문서 변경
    - delete: 문서 삭제
  - 형식
    - delete를 제외하고는 명령문과 데이터문을 한 줄씩 순서대로 입력한다.
    - delete는 내용 입력이 필요 없기 때문에 명령문만 있다.
    - `_bulk`의 명령문과 데이터문은 반드시 한 줄 안에 입력이 되어야 하며 줄바꿈을 허용하지 않는다.
  - 예시

  ```json
  POST _bulk
  {"index":{"_index":"learning", "_id":"1"}} // 생성
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}} // 생성
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}} // 삭제
  {"create":{"_index":"learning", "_id":"3"}} // 생성
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}} // 수정
  {"doc":{"field":"deep learning"}}
  ```

  - 응답

  ```json
  {
    "took" : 1152,
    "errors" : false,
    "items" : [
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 0,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 1,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "delete" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 2,
          "result" : "deleted",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 2,
          "_primary_term" : 1,
          "status" : 200
        }
      },
      {
        "create" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "3",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 3,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "update" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 2,
          "result" : "updated",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 4,
          "_primary_term" : 1,
          "status" : 200
        }
      }
    ]
  }
  ```

  - 인덱스명이 모두 동일할 경우에는 아래와 같이 하는 것도 가능하다.

  ```json
  POST learning/_bulk
  
  {"index":{"_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_id":"2"}}
  {"create":{"_id":"3"}}
  {"field":"docker"}
  {"update":{"_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```



- json 파일에 실행할 명령을 저장하고 curl 명령으로 실행시킬 수 있다.

  - bulk.json 파일

  ```json
  {"index":{"_index":"learning", "_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}}
  {"create":{"_index":"learning", "_id":"3"}}
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```

  - 명령어
    - 파일 이름 앞에는 @를 입력한다.

  ```bash
  $ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
  ```



- 그 외에 색인 성능을 확보하는 방법들
  - 문서의 id 없이 색인하기
    - PUT 메서드로 문서의 id를 지정하여 색인하는 것 보다 POST 메서드로 ES가 문서의 id를 임의로 생성하게 하는 것이 더 빠르게 색인 된다.
    - PUT의 경우 사용자가 입력한 id가 이미 존재하는지 검증하는 과정을 거쳐야 하지만 POST의 경우 기존에 동일한 id를 가진 문서가 없다는 전제 조건하에 색인되기 때문에 이미 존재하는 문서인지 확인하는 과정을 생략한다.
  - 레플리카 샤드 갯수를 0으로 설정하기
    - 프라이머리 샤드에 색인 된 후 레플리카에 복제하는 시간을 줄일 수 있다.
    - 클러스터를 운영하는 환경에 복제본이 꼭 필요하지 않거나 하둡과 같은 별도의 저장소에 사용자의 문서를 복제하는 경우라면 고려해 볼 만 하다.
  - 더 빠른 hardware를 사용하기
    - SSD를 사용하면 색인 속도가 보다 빨라질 수 있다.



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



- Primary shard의 개수와 색인 속도

  > 아래에서는 node 3개로 구성된 cluster로 test를 진행했으나 single node에서도 결과는 마찬가지다.
  
  - Primary shard의 개수를 늘리면 색인 속도도 함께 증가한다.
    - 검색과 마찬가지로 shard의 개수가 증가하면 색인 요청을 처리하는 thread도 증가하게 되므로 보다 빠른 속도로 색인이 가능해진다.
    - Shard의 개수 증가로 인한 색인 속도의 증가는 요청을 처리하는 thread의 개수 외에도 요청을 처리하는 node 수의 증가도 영향을 미친다.
    - 만일 primary shard가 1개일 경우 해당 shard가 할당된 node에서만 모든 indexing을 처리하겠지만, 여러 개의 primary shard가 각 node에 분산된 경우 shard를 할당 받은 모든 node가 색인에 참여하므로 색인 속도가 더 빨라지게 된다.
  - 아래와 같이 색인 test용 data를 생성한다.
  
  ```python
  fake = Faker()
  bulk_data = []
  
  for i in range(100000):
      text = " ".join([fake.text() for _ in range(10)])
      bulk_data.append({
          "_index":"indexing_test",
          "_id":i,
          "_source":{
              "text":text
          }
      })
  
  with open("test.json", "w") as f:
      json.dump(f, bulk_data, indent="\t")
  ```

  - 아래와 같이 primary shard의 개수를 설정하여 index를 생성한다.
  
  ```json
  // PUT indexing_test
  {
    "settings": {
      "number_of_shards": 1
    }
  }
  ```

  - 색인을 실행한다.
  
  ```python
  es_client = Elasticsearch("http://localhost:9200")
  
  with open("test.json", "r") as f:
      bulk_data = json.load(f)
  
  st = time.time()
  helpers.bulk(es_client, bulk_data)
  print(time.time()-st)
  ```

  - Primary shard의 개수를 늘릴수록 색인 속도가 증가하는 것을 확인할 수 있다.
  
  | Primary shard 개수 | 색인 시간 |
  | ------------------ | --------- |
  | 1                  | 49.85     |
  | 2                  | 35.80     |
  | 5                  | 25.47     |
  | 10                 | 19.24     |
  
  - 위에서는 document의 `_id` 값을 지정했는데, 지정하든 지정하지 않든 primary shard가 증가할 수록 색인 속도는 증가한다.



- Hot spotting 피하기

  - Hot spotting은 node의 자원이나 shard 또는 request가 cluster 내에서 고르게 분배되지 않을 때 발생한다.

    - Elasticsearch는 cluster의 상태를 node 사이에 최대한 sync를 맞추는 방식으로 동작하기에, 지속적으로 hot spot이 되는 node가 있을 경우 전체 cluster의 성능을 저하시킬 수 있다.

    - 일시적인 hot spotting이 발상해는 것은 문제가 되지 않을 수 있지만, 반복적으로 혹은 긴 기간 동안 발생한다면 cluster 전체의 성능을 저하시킬 수 있으므로 주의 깊게 관찰해야한다.

  - Hot spotting 탐지하기

    - Hot spotting은 일반적으로 resource의 사용(`disk.percent`, `heap.percent`, `cpu`)이 상당히 높아질 때 발생한다.
    - 아래와 같이 `_cat/nodes` API를 사용하여 각 node들의 resource 사용량을 확인하거나, 별도의 monitoring tool을 사용하여 확인이 가능하다.

  ```http
  GET _cat/nodes?v&s=master,name&h=name,master,node.role,heap.percent,disk.used_percent,cpu
  ```

  - `_cat/thread_pool` API로 hot spot 탐지하기
    - 아래와 같이 node들의 thread_pool을 확인하여 hot spot을 탐지할 수 있다.
    - 예를 들어 아래 예시에서 node_1은 다른 node들에 비해 많은 수의 쓰기 요청이 queue에서 대기중인 것을 확인할 수 있다.
    - 또한 node_3은 다른 node들에 비해서 처리를 완료한 쓰기 요청이 압도적으로 많은 것을 확인할 수 있다.

  ```http
  GET _cat/thread_pool/write,search?v=true&s=n,nn&h=n,nn,q,a,r,c
  
  n      nn       q a r    c
  search node_1   3 1 0 1287
  search node_2   0 2 0 1159
  search node_3   0 1 0 1302
  write  node_1 100 3 0 4259
  write  node_2   0 4 0  980
  write  node_3   1 5 0 8714
  ```

  - Hardware의 문제로 인해 발생하는 hot spotting

    - Resource가 균등하게 분배되지 않을 경우 발생할 수 있다. Elasticsearch는 모든 data node의 hardware가 같은 spec을 가질 것이라 예상하기 때문이다.
    - Elasticsearch는 node가 실행중인 host에 다른 service들을 실행시키는 것을 권장하지 않는다. 만약 host에 node 이외의 service가 함께 실행중일 경우 해당 service도 resource를 소비하게 되므로, 다른 service들과 함께 실행중인 node는 hot spot이 될 수 있다.

    - Node들 간에 network나 disk throughput이 고르게 분배되지 않을 경우 더 많은 throughput을 받는 node가 hot spot이 될 수 있다.
    - 31GB를 초과하는 JVM heap이 설정된 node는 hot spot이 될 수 있다.
    - Memory swapping을 사용하는 node는 hot spot이 될 수 있다.

  - Shard가 고르게 분배되지 못 할 경우에도 hot spot이 될 수 있다.

    - 예를 들어 아래 표와 같이 3개의 node가 있다고 가정해보자.
    - node2는 최근에 추가되어 아직 많은 shard들을 할당 받지는 못했다.
    - Elasticsearch는 index의 shard들을 최대한 고르게 분배하려고 하기에, rollover 등이 발생할 경우 가장 적은 shard를 할당 받은 node2에 새로운 shard가 많이 생성될 것이다.
    - 따라서 이 경우 node2가 hot spot이 될 수 있다.
    - Shard들이 고르게 분배되지 못하는 것도 문제지만, 고르게 분배된다고 하더라도 shard들의 크기에서 차이가 나는 것도 문제이다.
    - 예를 들어 아래 표에서 node1과 node2는 shard의 개수는 크게 차이가 나지 않지만, disk 사용량은 2배 이상 차이가 난다.

    | node | shards | disk.indices |
    | ---- | ------ | ------------ |
    | 1    | 231    | 100.2gb      |
    | 2    | 22     | 30gb         |
    | 3    | 232    | 210.3gb      |

  - Task load가 잘 못 될 경우에도 hot spotting이 발생할 수 있다.

    - Shard가 고르게 분배되지 못 할 경우 일반적으로 task도 고르게 분배되지 못한다.
    - 따라서 task를 고르게 분배하기 위해서는 우선 shard를 고르게 분배해야한다.

    - 아래와 같이 `_cat/task` 명령어를 통해 task들을 monitoring하여 어떤 node에서 어떤 task들이 실행되고 있는지 모니터링이 가능하다.

  ```http
  GET _cat/tasks?v&s=time:desc&h=type,action,running_time,node,cancellable
  ```



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



### Indexing pressure

- Lucene은 문서 하나의 크기를 2GB로 제한하고 있다.
  - Elasticsearch는 `http.max_content_length` 설정을 통해 간접적으로 문서의 최대 크기를 조정한다.
  - 2GB 제한이 걸려있다고 하더라도, 큰 document는 일반적으로 비효율적이다.
    - Network에 더 많은 부하를 주고, 더 많은 메모리와 더 많은 disk를 사용한다.



- 하나의 문서가 색인되기 위해서는 3 단계를 거쳐야 한다.
  - Coordinating
    - Document id를 기반(기본값)으로 어떤 replication group에 routing될지 결정된다.
    - Replication group이란 primary shard와 replica shard가 모두 포함되어 있는 group을 의미한다.
    - 어떤 replication group에 색인될지 선택되면 선택된 replication group 내의 primary shard에 색인 요청을 전달한다.
  - Primary
    - 색인 관련 동작(색인 혹은 삭제)을 검증하고, 이를 replica shard에 전달하는 단계이다.
    - 먼저 색인 동작을 검증하고, 검증 결과 유효하지 않은 형식이면 색인을 거절한다(예를 들어 datetime field에 integer를 색인하는 경우 등).
    - 색인 관련 동작을 실행하는데, 이전 단계에서 동작의 형식을 검증한다면, 이 단계에서는 내용을 검증하고, 유효하지 않은 내용(keyword field에 너무 긴 text를 색인하려 하는 등)이면 색인을 거절한다.
    - Replica shard에 색인 관련 동작을 전송한다.
    - 일부 replica shard가 offline 상태일 수 있기에 primary가 모든 replica shard에 데이터를 복제할 필요는 없다.
    - Elasticsearch는 색인 동작을 받을 수 있는 상태인 shard들의 목록을 master node에 저장하고 있는데, 이 목록을 in-sync copies라 부른다.
    - Primary shard는 이 목록에 있는 shard들에만 복제 동작을 전송한다.
  - Replica
    - Primary shard에게 전달 받은 색인 관련 동작을 수행한다.
    - 색인이 완료되면 primary shard에게 완료되었다는 응답을 보낸다.



- Memory limit
  - `indexing_pressure.memory.limit`
    - 아직 색인되지 않은 data를 위해 전체 heap memory에서 몇 %의 메모리를 사용할지를 설정한다.
    - Node 단위로 설정하며, 기본값 보다 더 큰 값을 설정하려는 경우 매우 주의깊게 설정해야 한다.
    - 기본값은 10%이다.
  - 색인의 각 단계가 시작될 때 Elasticsearch는 색인 request에 필요한 memory를 차지하고 있다.
    - 이는 오직 색인이 종료될 때만 release 된다.
    - 이는 앞선 단계는 아랫 단계가 모두 종료될 때 까지 memory를 차지하고 있다는 의미이다.
    - 예를 들어 coordinating stage는 primary, replica stage가 완료될 때 까지 memory를 차지하고 있다.
  - Node는 coordinating, primary, replica 단계에서 색인 memory가 `indexing_pressure.memory.limit`를 초과할 경우 새로운 색인 요청을 거절한다.
    - coordinating, primary, replica 단계에서 색인 memory가 `indexing_pressure.memory.limit`를 초과할 경우, coordinating, primary 단계에서 새로운 색인 요청을 거절한다.
    -  replica 단계에서 색인 memory가 `indexing_pressure.memory.limit`의 1.5배를 초과할 경우, replica 단계에서 새로운 색인 요청을 거절한다.
  - `_nodes/stats` API의 `indexing_pressure`를 통해 관련 지표를 확인할 수 있다.



- `es_rejected_execution_exception`
  - Elasticsearch가 memory상의 이유로 새로운 색인을 거절할 경우 발생하는 exception이다.
  - 즉, request body의 제한인 100mb를 지킨다고 해도, 색인이 실패할 수 있는 것이다.
  -  `http.max_content_length`의 기본값을 초과하는 요청에 대해서는 413 status code(Content Too Large)를 반환하지만, `indexing_pressure.memory.limit`를 초과하여 색인할 수 없는 경우 429 status code(Too Many Requests)와 함께 `es_rejected_execution_exception`을 반환한다.





## 검색 성능 최적화

### ES 캐시 활용하기

- ES 캐시의 종류와 특성

  - ES로 요청되는 다양한 검색 쿼리는 동일한 요청에 대해 좀 더 빠른 응답을 주기 위해 해당 쿼리의 결과를 메모리에 저장한다.
  - 결과를 메모리에 저장해 두는 것을 캐싱이라 하며 이 때 사용하는 메모리 영역을 캐시 메모리라 한다.
  - ES에서 제공하는 대표적인 캐시 영역들

  | 캐시 영역           | 설명                                                     |
  | ------------------- | -------------------------------------------------------- |
  | Node query cache    | 쿼리에 의해 각 노드에 캐싱되는 영역이다.                 |
  | Shard request cache | 쿼리에 의해 각 샤드에 캐싱되는 영역이다.                 |
  | Field data cache    | 쿼리에 의해 필드를 대상으로 각 노드에 캐싱되는 영역이다. |



- Node Query Cache

  - Filter context에 의해 검색된 문서의 결과가 캐싱되는 영역
    - 사용자가 filter context로 구성된 쿼리로 검색하면 내부적으로 각 문서에 0과 1로 설정할 수 있는 bitset을 생성한다.
    - Bitset은 segment마다 생성되며, segment가 병합되면 다시 생성해야한다.
    - Filter context로 호출한 적이 있는 문서는 bitset을 1로 설정하여 사용자가 호출한적이 있다는 것을 문서에 표시해둔다.
    - ES는 문서별로 bitset을 설정하면서, 사용자의 쿼리 횟수와 bitset이 1인 문서들 사이에 연관 관계를 지속적으로 확인한다.
    - Bitset이 1인 문서들 중에 자주 호출되었다고 판단한 문서들을 노드의 메모리에 캐싱한다.
  - Caching되는 조건들
    - Lucene의 `TermQuery`, `DocValuesFieldExistsQuery`, `MatchAllDocsQuery` 등의 query는 cache 없이도 충분히 빠르기 때문에 caching되지 않는다([코드 참고](https://github.com/apache/lucene/blob/releases/lucene-solr/8.8.1/lucene/core/src/java/org/apache/lucene/search/UsageTrackingQueryCachingPolicy.java#L57-L94)).
    - Lucene의 `MatchNoDocsQuery` 역시 문서가 없을 때 사용하는 query이므로 caching되지 않는다.
    - Segment 하나에 저장된 문서의 수가 1만개 미만이거나, segment에 저장된 문서의 개수가 shard에 저장된 전체 문서의 개수의 3% 미만일 경우에는 filter context를 사용하더라도 캐싱되지 않는다.
    - 또한 잘 사용되지 않는 filter를 caching하는 것은 비효율 적이므로 일정 횟수 이상 사용된 filter만 caching하며, 횟수는 query에 따라 달라진다.
    - Script query의 경우 Lucene에서는 사용되지 않기 때문에 caching이 되지 않는 것으로 보인다.
    - `profile`을 추가하면 caching이 되지 않는 것으로 보인다.
    - 이 외에도 다양한 조건이 있다.
  - 아래 명령어로 Query Cache Memory의 용량을 확인 가능하다.
  
  ```bash
  # node별 query cache 확인
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,qcm"
  $ curl -XGET "http://localhost:9200/_nodes/stats/indices/query_cache?human&pretty"
  
  # query cache 확인
  $ curl -XGET "http://localhost:9200/_stats/query_cache?human&pretty"
  
  # 특정 index의 query cache 확인
  $ curl -XGET "http://localhost:9200/<index_name>/_stats/query_cache?human&pretty"
  ```
  
  - 기본적으로 활성화되어 있으며, 아래와 같이 변경이 가능하다.
    - Dynamic setting이 아니기에 인덱스를 close로 바꾸고 설정해줘야 한다.
  
  ```bash
  # 인덱스를 close 상태로 변경하고
  $ curl -XGET "http://localhost:9200/my_index/_close" -H 'Content-Type: application/json'
  
  # 바꿔준다.
  $ curl -XGET "http://localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'{
  "index.queries.cache.enable":true # false면 비활성화
  }'
  
  # 인덱스를 다시 open 상태로 변경한다.
  $ curl -XGET "http://localhost:9200/my_index/_open" -H 'Content-Type: application/json'
  ```
  
  - 많은 문서가 캐싱되어 허용된 캐시 메모리 영역이 가득 차면 LRU(Least Recently Used Algorithm) 알고리즘에 의해 캐싱된 문서를 삭제한다.
    - LRU: 캐시 영역에 저장된 내용들 중 가장 오래된 내용을 지우는 알고리즘
    - elasticsearch.yml 파일에서 `indices.queries.cache.size: 10%`와 같이 수정하여 Node Query Cache 영역을 조정할 수 있다.
    - 위와 같이 비율로도 설정할 수 있고, 512mb처럼 절댓값을 주는 것도 가능하다.
    - 수정 후 노드를 재시작해야한다.
  - 서로 다른 query라 할지라도 공통된 filter context query를 사용하면 cache 결과를 재사용한다.
    - 각 query들에 공통으로 들어간 filter context query의 결과로 생성된 문서들을 먼저 추린다.
    - 그 후에 추려진 문서들을 대상으로 filter context에 속하지 않는 부분으로 마저 검색을 수행한다.



- Node Query Cache 예시

  - 아래에서 `match` query는 Lucene query로 변환 될 때 `TermQuery`로 변환되므로 caching이 발생하지 않는다.

  ```json
  // GET cache_test/_search
  {
      "query": {
          "bool": {
              "filter": [
                  {
                      "match": {
                          "text": "모니터링"
                      }
                  }
              ]
          }
      }
  }
  ```

  - 반면에 같은 `match` query라고 하더라도 아래와 같이 term을 2개 이상 주면 Lucene query로 변환될 때 `BooleanQuery`로 변환되어 caching이 된다.

  ```json
  // GET cache_test/_search
  {
      "query": {
          "bool": {
              "filter": [
                  {
                      "match": {
                          "text": "모니터링 기반의"
                      }
                  }
              ]
          }
      }
  }
  ```



- Shard Request Cache

  - Node Query Cache가 노드에 할당된 캐시 영역이라면 Shard Request Cache는 샤드를 대상으로 캐싱되는 영역이다.
    - 특정 필드에 의한 검색이기 때문에 전체 샤드에 캐싱된다.
    - Node Query Cache와 달리 문서의 내용을 캐싱하는 것이 아니라, aggregation query의 집계 결과 혹은 ReqeustBody의 파라미터 중 size를 0으로 설정했을 때의 쿼리 응답 결과에 포함되는 매칭된 문서의 수(total hits)에 대해서만 캐싱한다.
    - Node Query Cache가 검색 엔진에 활용하기 적합한 캐시 영역이라면 Shard Request Cache는 분석 엔진에서 활용하기 적합한 캐시 영역이라고 할 수 있다.
    - 다만 이 영역은 refresh 동작을 수행하면 캐싱된 내용이 사라진다.
    - 즉, 문서 색인이나 업데이트를 한 후 refresh를 통해 샤드의 내용이 변경되면 기존에 캐싱된 결과가 초기화 된다.
    - 따라서 계속해서 색인이 일어나고 있는 인덱스에는 크게 효과가 없다.
  - 아래 명령으로 Shard Request Cache의 상황을 볼 수 있다.

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,rcm"
  ```

  - Shard Request Cache도 ES 클러스터에 기본적으로 활성화되어 있다.
    - 다만 dynamic setting이어서 인덱스를 대상으로 온라인중에 설정이 가능하다.

  ```bash
  $ curl -XGET "http://localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'{
  "index.requests.cache.enable":true # false면 비활성화
  }'
  ```

  - 검색시에도 활성/비활성화가 가능하다.
    - size를 0으로 줬으므로 본래 Shard Request Cache가 생성되어야 하지만 `request_cache=false`로 인해 생성되지 않는다.

  ```bash
  $ curl -XGET "http://localhost:9200/my_index/_search?request_cache=false" -H 'Content-Type: application/json' -d'{
  "size":0,	# size가 0일 때 Shard Request Cache가 생성된다.
  "aggs":{
  	"cityaggs":{
  		"terms":{"field":"city.keyword"}
  	}
  }
  }'
  ```

  - 가이드라인
    - Shard Request Cache 설정을 기본으로 활성화한 다음, 색인이 종료된 과거 인덱스는 request_cache를 true로 집계하고 색인이 한참 진행 중인 인덱스는 false로 집계하는 방식으로 사용한다 
    - 이렇게 하면 과거 인덱스에 대해서는 캐싱 데이터를 리턴해서 빠르게 결과를 전달 받고, 색인이 빈번하게 진행 중이어서 캐싱이 어려운 인덱스는 불필요하게 캐싱하는 낭비를 막을 수 있다.
    - 또한 과거 인덱스에 색인이 들어오면 캐싱된 데이터가 초기화되기 때문에 인덱스를 쓰지 못하도록 read only 처리하는 것도 캐싱 데이터를 유지시킬 수 있는 방법이다.

  - 각 노드의  elasticsearch.yml 파일에서 다음과 같이 Shard Request Cache 영역을 조정 가능하다.
    - `indices.requests.cache.size: 10%`
    - 이 경우 노드를 재시작해야 한다.



- Field Data Cache

  - 인덱스를 구성하는 필드에 대한 캐싱
    - 주로 검색 결과를 정렬하거나 집계 쿼리를 수행할 때 지정한 필드만을 대상으로 해당 필드의 모든 데이터를 메모리에 저장하는 캐싱 영역이다.
    - 예를 들어 A 노드에 a, b 샤드, B 노드에 c 샤드가 있다고 가정
    - a샤드에는 age:20이라는 데이터가, b 샤드에는 age:21이라는 데이터가, B 노드에는 age:22라는 데이터가 색인되어 있다고 할 때
    - age 필드를 대상으로 정렬하는 검색을 진행하면
    - A 노드에는 age 필드의 값이 20,21 인 데이터가, B 노드애는 age 필드의 값이 22인 데이터가 캐싱된다.
  - Field Data Cache 영역은 text 필드 데이터 타입에 대해서는 캐싱을 허용하지 않는다.
    - 다른 필드 데이터 타입에 비해 캐시 메모리에 큰 데이터가 저장되기 때문에 메모리를 과도하게 사용하게 되기 때문이다.

  - Field Data Cache 사용 현황 확인

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,fm"
  ```

  - 마찬가지로 elasticsearch.yml 파일에서 다음과 같이 Field Data Cache 영역을 조정 가능하다.
    - `indices.fielddata.cache.size: 10%`
    - 역시 노드를 재시작해야 한다.



- 캐시 영역 클리어

  - 전체 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear"
  ```

  - Node Query Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?query=true" -H 'Content-type:application/json'
  ```

  - Shard Request Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?request=true" -H 'Content-type:application/json'
  ```

  - Field Data Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?fielddata=true" -H 'Content-type:application/json'
  ```



### 검색 쿼리 튜닝하기

- copy_to

  - 쿼리를 어떻게 만드느냐가 검색 성능에 큰 영향을 미친다.
  - 검색 성능을 떨어뜨리는 요인 중 하나는 너무 많은 필드를 사용하는 것이다.
    - 처음에 인덱스의 매핑 정보를 생성할 때 우선적으로 불필요한 필드들을 제외해야 하지만 매핑 구조에 따라 필드가 많아지는 경우도 있다.
    - 이런 경우에는 별수 없이 많은 필드에 걸쳐 검색을 해야 하는 경우도 생긴다.
  - 여러 개의 필드를 대상으로 검색하는 예시
    - `first_name`과 `last_name`이라는 2개의 필드를 대상으로 검색하기
    - `match` 쿼리를 두 번 사용해서 검색해야 한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_search?pretty" -H 'Content-type:application/json' -d'
  {
  	"query":{
  		"bool":{
  			"must":[
  				{"match":{"first_name":"John"}},
  				{"match":{"last_name":"Doe"}}
  			]
  		}
  	}
  }
  '
  ```

  - 이렇게 많은 필드를 모아서 검색할 수 있는 기능이 copy_to 기능이다.
    - 가능하면 매핑 스키마 계획을 세울 때 최소한의 필드를 사용할 수 있도록 한다.
    - 그러나 불가피하게 많은 필드를 대상으로 검색해야 한다면 copy_to를 최대한 활용한다.



- copy_to를 활용하여 검색하기

  - mapping할 때 `copy_to`를 추가한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_mappings?pretty" -H 'Content-type:application/json' -d'
  {
  	"_doc":{
  		"properties":{
  			"first_name":{
  				"type":"text",
  				"copy_to":"full_name"	# copy_to 추가
  			},
  			"last_name":{
  				"type":"text",
  				"copy_to":"full_name"
  			},
  			"full_name":{		# copy_to를 위한 필드 생성
  				"type":"text"
  			}
  		}
  	}
  }
  ```

  - 색인할 때 copy_to를 위해 생성한 필드(`full_name`) 필드에는 따로 데이터를 넣어줄 필요가 없다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_mappings?pretty" -H 'Content-type:application/json' -d'
  {
  	"first_name":"John",
  	"last_name":"Doe"
  }
  ```

  - 검색
    - copy_to를 위해 생성한 필드(`full_name`)를 대상으로 검색한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_search?pretty" -H 'Content-type:application/json' -d'
  {
  	"query":{
  		"match":{
  			"full_name":"John Doe"
  		}
  	}
  }
  '
  ```



- 불필요하게 사용되는 쿼리 제거하기
  - Query Context와 Filter Context 구분하기
    - match 쿼리는 Query Context에 속하는 쿼리다.
    - Query Context는 analyzer를 통해 검색어를 분석하는 과정이 포함되기 때문에 분석을 위한 추가 시간이 필요하다.
    - 반면에 Filter Context에 속하는  term 쿼리는 검색어를 분석하는 과정을 거치지 않는다.
    - 따라서 match 쿼리보다 term 쿼리가 성능이 더 좋다.
  - keyword 필드 데이터 타입으로 매핑된 문자열 필드는 term 쿼리를 사용하는 것이 성능상 유리하다.
    - keyword 필드는 분석하지 않는 필드이다.
    - 따라서 검색할 때도 검색어를 분석하지 않는 term 쿼리가 더 적합하다.
  - ES에서는 수치 계산에 사용되지 않는 숫자형 데이터는 keyword 필드 데이터 타입으로 매핑하도록 권고한다.
    - 이 경우에도 keyword 타입으로 정의하고 term 쿼리를 사용하는 것이 적합하다.
    - 단, keyword 타입으로 저장된 숫자들은 계산이 되지 않는다.





### Shard

- 샤드 배치를 적절히 하지 못할 경우 아래와 같은 문제들이 발생할 수 있다.

  - 데이터 노드 간 디스크 사용량 불균형
    - 노드는 3대이고 프라이머리 샤드는 4개로 설정했다고 가정
    - 한 노드는 2개의 샤드를 가져갈 수 밖에 없다.
    - 시간이 흐를수록 2개의 샤드를 가져간 노드의 디스크 사용량이 높아지게 된다.
    - 따라서 노드의 개수에 맞게 샤드 개수를 설정해야 한다.
  - 색인/검색 성능 부족
    - 노드는 3대이고 프라이머리 샤드는 2개로 설정했다고 가정
    - 하나의 노드는 샤드를 할당받지 못한다.
    - 샤드를 할당받지 못한 노드는 클러스터에 속해 있어도 색인과 검색에 참여할 수 없다.
  - 데이터 노드 증설 후에도 검색 성능이 나아지지 않음
    - 최초에 노드의 개수와 샤드의 개수를 동일하게 클러스터를 구성했다고 가정
    - 이 상황에서 노드의 개수를 증가시킨다 하더라도 해당 노드에 할당할 샤드가 없으므로 노드 추가로 인한 성능 개선을 기대하기 어렵다.
    - 따라서 처음에 클러스터를 구성할 때 어느 정도의 증설을 미리 계획하여 최초 구성한 노드의 개수와 증설된 이후 노드의 개수의 최소공배수로 샤드의 개수를 설정하면 위와 같은 문제를 모두 예방할 수 있다.
  - 클러스터 전체의 샤드 개수가 지나치게 많음
    - 이 경우 마스터 노드를 고려해야 한다.
    - 샤드의 개수가 많아질수록 마스터 노드가 관리해야 하는 정보도 많아지게 된다.
    - 따라서 데이터 노드의 사용량에는 큰 문제가 없는데 클러스터의 성능이 제대로 나오지 않는 문제가 발생할 수 있다.
    - 하나의 노드에서 조회할 수 있는 샤드의 개수를 제한하는 것도 방법이다.

  ```json
  // PUT cluster/settings
  {
  	"transient":{
  		"cluster.max_shards_per_node":2000	// 노드당 검색 요청에 응답할 수 있는 최대 샤드 개수를 2000개로 설정
  	}
  }
  
  // index 단위로는 아래와 같이 설정할 수 있다.
  // PUT my-index-000001/_settings
  {
    "index" : {
      "routing.allocation.total_shards_per_node" : 5
    }
  }
  ```



- Shard의 개수 조절
  - Shard의 개수를 증가시키면 검색 속도가 빨라진다.
    - 정확히는 일정 개수 까지는 shard의 개수와 검색 속도가 정비례하지만 일정 개수 부터는 shard가 증가할 수록 검색 속도가 감소하게 된다.
  - Elasticsearch에서 query는 shard당 단일 thread로 실행된다.
    - 따라서 shard의 개수가 증가할 경우 multi-thread로 query를 수행할 수 있게 되어 검색 속도가 빨라지게 된다.
    - 많은 개수의 작은 shard에 대한 query 작업은 shard당 처리 속도는 빨라질 수 있지만 search thread pool을 고갈시킬 수 있으므로 더 적은 개수의 큰 shard를 검색하는 것 보다 반드시 빠르다고는 할 수 없다.
    - 일반적으로 천 개의 50MB짜리 shard들을 대상으로 검색하는 것이 50GB짜리 shard하나에 검색하는 것 보다 상당히 많은 resource를 필요로 한다.
  - 너무 많은 shard 개수를 설정하는 것은 overhead를 크게 증가시킬 수 있다.
    - 모든 index와 index 내부의 shard들은 memory와 CPU를 필요로한다.
    - 대부분의 경우에 적은 수의 큰 shard들이 많은 수의 작은 shard들 보다 더 적은 resource를 사용한다.
    - 또한 샤드가 많을 수록 병렬 처리해야 하는 양이 많아진다는 의미이므로 네트워크 통신과 병렬 처리 오버헤드가 증가한다.
  - Segment와 shard
    - Elasticsearch는 빠른 검색을 위해서 segment들의 metadata를 heap memory에 저장한다.
    - Shard의 크기가 커질수록 segment들은 보다 적은 수로 병합되면서 크기가 점차 증가한다.
    - 이를 통해 segment의 개수가 감소하게 되고, heap memory에 저장해야 하는 metadata의 크기도 감소하게 된다.
  - Segment와 field
    - 모든 segment는 mapping된 field의 이름을 저장하기 위해서도 heap memory를 사용한다.
    - 일반적으로 여기에 사용되는 heap memory는 매우 적은 양이지만, field의 개수가 많아지거나, field의 이름이 길 경우 이로 인한 overhead도 고려해야한다.



- Shard의 적절한 크기
  - Shard의 물리적 크기에 대한 hard limit은 없다.
    - 각각의 shard는 이론적으로 20억 개 이상의 문서를 저장할 수 있다.
  - 그러나 경험적으로는 적절한 크기가 있다.
    - 2억개 미만의 문서
    - 10GB에서 50GB사이의 크기



- 적절한 샤드 수를 찾기 위한 테스트
  - 구성
    - 먼저 데이터 노드 한 대로 클러스터를 구성하고, 해당 노드에 데이터를 저장한 후 사용자의 검색 쿼리에 대한 응답을 100ms 이하로 줄 수 있는지 테스트한다.
    - 이때 클러스터 구성은 데이터 노드 한 대, 레플리카 샤드 없이 프라이머리 샤드만 1개로 구성한다.
    - 그리고 해당 샤드에 데이터를 계속 색인하면서 샤드의 크기가 커짐에 따라 검색 성능이 어떻게 변화하는지를 측정한다.
    - 이렇게 구성해야 데이터 노드가 샤드 하나로 검색 요청을 처리할 때의 성능을 측정할 수 있다.
    - 샤드 하나당 하나의 검색 스레드만 사용해야 검색 스레드 큐에 검색 쿼리가 너무 많이 쌓이지 않아서 하나의 샤드에서 측정된 검색 성능을 보장할 수 있기 때문이다.
  - 테스트
    - 쿼리에 대한 응답 데이터 중 took 필드를 통해 확인할 수 있다.
    - 이 값이 100ms 이하로 나오면 사용자의 검색 엔진 요구에 맞는 엔진이 되는 것이다.
    - 색인과 검색을 반복하다가 사용자가 원하는 응답 속도인 100ms에 근접한 값이 나오면 색인을 멈춘다.
    - 테스트에 사용한 인덱스는 단일 샤드로 구성되었기 때문에 이 시점에서의 인덱스의 크기가 곧 단일 샤드의 크기가 된다.
    - 이렇게 노드 한 대가 사용자의 요구인 100ms의 속도로 검색 결과를 리턴해줄 수 있는 샤드의 적정 크기를 측정한다.
    - 실제 서비스할 전체 데이터의 크기를 테스트를 통해 산정한 인덱스의 크기로 나누면 그 값이 사용자가 원하는 응답 속도를 보여줄 수 있는 프라이머리 
    - 샤드의 개수가 된다.



- Primary shard의 개수를 증가시켰을 때, thread pool이 고갈되어 오히려 전체 검색 속도는 감소할 수 있다.

  - Elasticsearch에서 검색은 shard 하나 당 thread 하나에서 실행된다.
    - Shard의 개수를 늘릴수록 검색 속도가 증가하는 것도 이 때문으로, shard가 하나일 경우 single thread로 검색이 실행되지만, shard가 여러 개면 multi thread로 검색이 실행되기 때문이다.
  - 위와 같은 동작 방식으로 인해 primary shard를 늘리면 검색 속도가 증가하지만, 지나치게 늘리면 오히려 검색 속도가 감소하게 된다.
  - 테스트를 위해 아래와 같이 동일한 구성에 primary shard의 개수만 다른 index 2개를 생성한다.
    - Cluster에 속한 모든 node의 `search_worker` thread pool의 size는 5로 설정했다.
    - Node 3개로 구성된 cluster에서 test했기에 replica shard의 개수를 2로 줬다.
    - 만일 node가 3개인데, replica shard가 0일 경우, primary shard의 개수를 1로 설정한 index의 경우 shard를 할당 받지 못 한 node가 생길 수 있다.
    - 이로 인한 전체 검색 속도의 차이가 생길 수 있으므로 primary shard가 1이라 할지라도 모든 node에 replica shard가 분배되도록 replica shard의 개수를 조정해야한다.

  ```json
  // PUT single_shard
  {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 2, 
      "analysis": {
        "analyzer": {
          "nori_analyzer":{
            "tokenizer":"nori_tokenizer"
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "name":{
          "type": "text",
          "fields": {
            "keyword":{
              "type":"keyword"
            }
          }
        },
        "address":{
          "type":"text",
          "analyzer": "nori_analyzer"
        },
        "gender":{
          "type":"keyword"
        },
        "age":{
          "type":"integer"
        },
        "content":{
          "type":"text",
          "analyzer": "nori_analyzer"
        }
      }
    }
  }
  
  // primary shard가 5개인 index는 number_of_shards를 제외한 모든 구성이 위와 동일하다.
  // PUT five_shard
  {
    "settings": {
      "number_of_shards": 5,
      // ...
    },
    // ...
  }
  ```

  - 테스트용 data를 색인한다.
    - 아래에서 replica shard 개수 증가에 따른 전체 검색 처리 속도 증가를 테스트 하기 위한 test data를 만드는 code와 동일하다.
    - 한 index에 먼저 색인 후 다른 index에 reindex 한다.

  ```python
  import random
  
  from faker import Faker
  from elasticsearch import Elasticsearch, helpers
  
  
  class Bulker:
      def __init__(self):
          self.es_client = Elasticsearch("http://localhost:9200")
  
      def bulk_ko_data(self):
          fake = Faker("ko-KR")
          gender = ["남", "여", "무"]
          for i in range(100):
              bulk_data = []
              for _ in range(10000):
                  text = ""
                  for _ in range(50):
                      text += fake.catch_phrase() + " "
                  bulk_data.append({
                      "_index":"search_test",
                      "_source":{
                          "name":fake.name(),
                          "address":fake.address(),
                          "gender":random.choice(gender),
                          "age":random.randrange(20, 100),
                          "content":text.rstrip()
                      }
                  })
              helpers.bulk(self.es_client, bulk_data)
  
      
  if __name__ == "__main__":
      bulker = Bulker()
      bulker.bulk_ko_data()
  ```

  - 아래와 같이 두 index 각각의 단일 검색 요청의 평균 시간을 구한다.

  ```python
  from elasticsearch import Elasticsearch
  
  
  def search(index_name):
      es_client = Elasticsearch("localhost:9200")
      total = 0
      N = 100
      for i in range(N):
          query = {
              "bool": {
                  "must": [
                      {
                          "script": {
                              "script": "doc['name.keyword'].value.length() > 2"
                          }
                      },
                      {
                          "match": {
                              "content": "분석"
                          }
                      },
                      {
                          "match_phrase": {
                              "content": "휴리스틱"
                          }
                      }
                  ]
              }
          }
          total += es_client.search(index=index_name, query=query)["took"]
      print(total/N)
  
  if __name__ == "__main__":
      search("single_shard")
      search("five_shard")
  ```

  - 아래와 같이 여러 검색 요청을 동시에 처리했을 때 두 index의 총 소요 시간을 구한다.

  ```python
  import time
  import asyncio
  
  from elasticsearch import AsyncElasticsearch
  
  
  async def search(index_name):
      es_client = AsyncElasticsearch("http://localhost:9200")
      N = 500
      query = {
          "bool": {
              "must": [
                  {
                      "script": {
                          "script": "doc['name.keyword'].value.length() > 2"
                      }
                  },
                  {
                      "match": {
                          "content": "분석"
                      }
                  },
                  {
                      "match_phrase": {
                          "content": "휴리스틱"
                      }
                  }
              ]
          }
      }
      for i in range(N):
          await es_client.search(index=index_name, query=query)
      await es_client.close()
  
  
  async def main(index_name):
      await asyncio.wait([asyncio.create_task(search(index_name)) for _ in range(30)])
  
  
  if __name__ == "__main__":
      st = time.time()
      asyncio.run(main("single_shard"))
      print(time.time()-st)
  
      st = time.time()
      asyncio.run(main("five_shard"))
      print(time.time()-st)
  ```

  - 단일 검색일 때와 아래 script를 통해서 여러 개의 검색 요청을 연속해서 보냈을 때 두 index의 시간 차이는 아래와 같다.
    - 단일 검색 요청은 shard가 5개인 쪽이 훨씬 빠르지만, 여러 개의 검색 요청이 들어왔을 때 이들을 처리하는 것은 shard가 1개인 쪽이 더 빠른 것을 확인할 수 있다.

  | shard의 개수 | 단일 검색 요청 | 전체 검색 요청 |
  | ------------ | -------------- | -------------- |
  | 1            | 148.52         | 146.331        |
  | 5            | 70.91          | 266.603        |

  - 위와 같은 결과가 나오는 이유.
    - Primary shard가 1이고 replica가 2라고 하더라도, 결국 검색은 고유한 shard 하나에서만 이루어지므로, 실제 검색은 저 세 shard들 중 한 곳에서만 실행되므로 single thread로 실행된다.
    - 반면에 primary shard가 5라면 5개의 thread로 실행되므로 단일 검색 속도는 더 빠르다.
    - 그러나 이는 바꿔 말하면, 한 번의 검색에 5개의 thread가 필요하다는 의미이다.
    - Thread pool의 size가 5인 상태에서 primary shard의 개수가 1인 index에 15개의 검색 요청이 동시에 들어올 경우, 15개의 shard만 보면 되므로 각 node들은 5개의 thread를 모두 사용하여 queue에 대기하는 shard 조회 task 없이 15개의 검색 요청을 동시에 처리할 수가 있다.
    - 그러나 primary shard의 개수가 5인 index에 15개의 검색 요청이 동시에 들어올 경우, 각 요청 당 5개의 shard를 봐야 하므로 총 75개의 shard를 봐야 하지만, thread 당 shard 1개씩 밖에 볼 수 없으므로 동시에 최대 15개의 shard밖에 볼 수 없다.
    - 따라서 남은 60개의 shard를 조회하는 task는 queue에 들어가게 된다.
    - 위와 같은 이유로 인해, primary shard의 개수가 증가할 수록 thread pool의 고갈이 발생하게 되고, 전체적인 검색 속도 저하가 발생하게 된다.





### Number of Segments

- Segment의 개수가 늘어날수록 읽어야 하는 segment의 개수가 많아지기에 검색 속도가 감소하게 된다.

  - 샤드에 여러 개의 세그먼트가 있다면 해당 세그먼트들이 모두 검색 요청에 응답을 주어야 한다.
    - 쿼리마다 많은 세그먼트에 접근해야 한다면 이는 곧 I/O를 발생시켜 성능 저하로 이어질 것이다.
    - 하지만 세그먼트가 하나로 합쳐져 있다면, 사용자의 검색 요청에 응답해야 하는 세그먼트가 하나이기 떄문에 성능이 더 좋아질 수 있다.
    - 따라서 검색 속도를 증가시키기 위해서는 segment의 개수를 줄여야한다.

  - Force merge API를 통해 segment들을 병합시킬 수 있다.

  ```http
  POST <target_index>/_forcemerge
  ```

  - Force merge API는 아래와 같은 query parameter들을 받는다.
    - `flush`: Force merge 이후에 flush를 실행할지 여부를 설정하며, 기본값은 true이다.
    - `wait_for_completion`: Force merge request가 완료될 때 까지 block될지 여부를 설정하며, 기본값은 true이다.
    - `max_num_segments`: 몇 개의 segment로 병합할지를 설정하며, 기본값은 merge를 수행해야하면 수행하고, 그렇지 않다면 수행하지 않는 것이다. 완전한 최적화를 하고자 한다면 1로 설정하면 된다. 1로 주면 shard 당 최대 segment의 개수를 1로 제한하겠다는 것이다(인덱스 전체의 segment가 1이 되는 것이 아니다). 예를 들어 primary shard가 2, replica shard가 2일 때, `max_num_segments`를 1로 설정하면, shard 당 1개씩 4개의 segment로 병합된다.
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
  - 무조건 세그먼트가 적다고 좋은 것은 아니다.
    - 샤드 하나의 크기가 100GB 정도인데 세그먼트가 하나라면 작은 크기의 문서를 찾을 때에도 100GB 전체를 대상으로 검색해야 해서 병합 전보다 성능이 떨어질 수 있다.
    - 세그먼트를  병합했는데 이후에 색인이 발생하면 다시 세그먼트가 늘어나게 되어 병합 작업의 효과를 보기 어렵다.
    - 색인이 모두 끝난 인덱슨는 병합 작업을 진행하고 난 이후 readonly 모드로 설정하여 더 이상 세그먼트가 생성되지 못하게 하는 것이 좋다.
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





### 그 외의 방법들

- ES 권고사항

  - 문서를 모델링할 때 가급적이면 간결하게 구성하도록 권고한다.
    - Parent/Child 구조의 join 구성이나, nested 타입 같이 문서를 처리할 때 문서 간의 연결 관계 처리를 필요로 하는 구성은 권장하지 않는다.

  - painless script를 사용하여 하나의 문서를 처리할 때마다 부가적으로 리소스를 사용하지 않도록 하는 것도 권고사항이다.
    - painless script: 쿼리만으로 원하는 데이터를 조회할 수 없을 때 사용하는 ES 전용 스크립트 언어

  - 레플리카 샤드를 가능한 한 충분히 두는 것이 좋다.
    - 노드 1에 프라이머리 샤드 0과 레플리카샤드 1이 있고, 노드 2에 프라이머리샤드 1과 레플리카샤드 0이 있다고 가정
    - 두 개의 검색 요청이 들어왔고 두 요청에 대한 응답을 줄 데이터가 모두 샤드 0번에 있을 경우
    - 한 요청을 노드1로, 다른 요청은 노드 2로 들어왔을 때, 두 노드 모두 0번 샤드를 지니고 있으므로 동시에 들어온 검색 요청에  서로 다른 노드가 응답해 줄 수 있다.
    - 다만 레플리카 샤드는 인덱싱 성능과 볼륨 사용량의 낭비가 발생하니 클러스터 용량을 고려해서 추가하는 것이 좋다.



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







### 검색 속도에 영향을 주지 않는 것들

- Node 개수만 늘리면 검색 속도가 증가하는가?

  - Node가 하나뿐인 cluster를 구성

  ```yaml
  version: '3.2'
  
  
  services:
    node1:
      image: elasticsearch:latest
      container_name: node1
      environment:
        - node.name=node1
        - cluster.name=es-docker-cluster
        - cluster.initial_master_nodes=node1
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports: 
        - 9200:9200
      restart: always
      networks:
        - elastic
  
  networks:
    elastic:
      driver: bridge
  ```

  - Test용 index 생성
    - Node가 하나뿐이라 replica가 많아도 할당되지 않을 것이므로 1개만 생성한다.

  ```json
  // PUT search_performance_test
  {
    "settings": {
      "number_of_replicas": 0
    }
  }
  ```

  - 임의의 data를 색인한다.

  ```python
  from elasticsearch import Elasticsearch, helpers
  from faker import Faker
  
  
  es_client = Elasticsearch("http://localhost:9200")
  INDEX_NAME = "search_performance_test"
  fake = Faker()
  
  cnt = 0
  for i in range(100):
      bulk_data = []
      for _ in range(10000):
          content = ""
          for _ in range(30):
              content += fake.text()
          
          bulk_data.append({"_index":INDEX_NAME, "_source":{"title":fake.sentence(), "content":content, "num":cnt}})
          cnt += 1
      helpers.bulk(es_client, bulk_data)
  ```

  - Segment의 개수를 1로 조정한다.

  ```http
  POST search_performance_test/_forcemerge?max_num_segments=1
  ```

  - Segment의 개수가 1로 조정되면 아래와 같이 검색 속도를 측정한다.

  ```python
  from faker import Faker
  from elasticsearch import Elasticsearch
  
  
  fake = Faker()
  es_client = Elasticsearch("http://localhost:9200")
  INDEX_NAME = "search_performance_test"
  
  N = 1000
  total = 0
  for i in range(N):
      body = {
          "query":{
              "bool":{
                  "should":[
                      {
                          "match":{
                              "title":fake.word()
                          }
                      },
                      {
                          "match":{
                              "content":" ".join([fake.word() for _ in range(2)])
                          }
                      },
                      {
                          "match_phrase_prefix": {
                              "content": "{}.*".format(fake.word())
                          }
                      }
                  ]
              }
          }
      }
      res = es_client.search(index=INDEX_NAME, body=body)
      total += res["took"]
  print(total//N)
  ```

  - 그 후 아래와 같이 node의 개수를 늘려서 다시 cluster를 구성한다.

  ```yaml
  version: '3.2'
  
  
  services:
    node1:
      image: tmp-elasticsearch:latest
      container_name: node1
      environment:
        - node.name=node1
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node2,node3
        - cluster.initial_master_nodes=node1,node2,node3
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports: 
        - 9200:9200
      restart: always
      networks:
        - elastic
  
    node2:
      image: tmp-elasticsearch:latest
      container_name: node2
      environment:
        - node.name=node2
        - node.attr.my_attr=bar
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node1,node3
        - cluster.initial_master_nodes=node1,node2,node3
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      networks:
        - elastic
  
    node3:
      image: tmp-elasticsearch:latest
      container_name: node3
      environment:
        - node.name=node3
        - node.attr.my_attr=baz
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node1,node2
        - cluster.initial_master_nodes=node1,node2,node3
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      networks:
        - elastic
  
  networks:
    elastic:
      driver: bridge
  ```

  - 기존 index를 대상으로 다시 검색 속도를 측정한다.
    - 측정을 해보면 단순히 node의 개수를 늘리는 것 만으로는 검색 속도에 차이가 없는 것을 확인할 수 있다.
  - 단, node를 추가하면서, 새롭게 추가된 node에 replica shard를 할당할 경우, 검색 요청이 많을 때에 한해서는 node의 추가로 전체 검색 처리 속도는 증가할 수 있다.
    - 다만, 문서를 검색하는 속도 자체가 증가하는 것은 아니다.
    - 자세한 내용은 아래 replica shard 부분 참고



- Replica shard를 늘리면 검색 속도가 증가하는가?

  - 위에서는 primary1, replica 0, segment 1로 test를 했었다.
  - node가 3개이기 때문에 아래와 같이 replica shard의 개수를 2개로 늘린다.

  ```json
  // PUT search_performance_test/_settings
  {
    "index" : {
      "number_of_replicas" : 2
    }
  }
  ```

  - 다시 검색 속도를 측정해본다.
    - Replica shard를 늘리기 전과 후에 검색 속도 차이가 없는 것을 확인할 수 있다.
  - 차이가 없는 이유
    - Elasticsearch에서 검색이 이루어지는 과정은 고유한 shard들의 목록을 생성하는 것에서부터 시작한다.
    - 고유한 shard들의 목록을 생성하고, 해당 목록에 있는 shard를 대상으로 query를 실행한다.
    - 따라서 replica를 늘린다고 해도 고유한 shard의 개수가 늘어나는 것은 아니므로 검색 속도가 증가하지는 않는다.



- Replica shard를 늘렸을 때 처리 속도가 증가할 수도 있다.

  - 위에서 확인했듯이 replica shard의 수를 늘려도 검색 속도가 증가하지는 않는다.
  - 그러나 replica의 개수를 늘리는 것이 전반적인 처리 속도를 증가시킬 수는 있다.
    - 예를 들어 아래와 같은 상황에서는 replica shard를 늘리는 것이 처리 속도를 증가시켜 줄 수 있다.
    - 3개의 node로 구성된 cluster에 primary shard와 replica shard를 각각 1개씩 가지고 있는 index가 있다.
    - 해당 index를 대상으로 검색을 실행할 경우, primary 혹은 replica shard를 가지고 있는 node에서만 검색을 실행하게 된다.
    - 즉, node가 3대 임에도 실제 검색은 두 대에서만 이루어지게 된다.
    - 이 때 replica의 개수를 2로 변경하여 모든 node가 shard를 갖게 할 경우 단일 검색에서 검색 속도에는 처리가 없지만, 전체적인 검색 처리 속도는 증가할 수 있다.
  - 즉 어떤 index가 replica shard를 할당할 수 있는 node가 남아 있고, shard를 할당 받은 node들로만 검색 요청을 처리하는 것이 버거운 상황이라면 replica 개수를 늘리는 것이 전체적인 검색 처리 속도를 증가시킬 수 있다.
    - 정확히 해야 할 것은 replica를 늘려서 검색 속도가 빨라지는 것이 아니라는점이다.
    - Replica를 추가함으로써 해당 replica를 할당 받은 node가 추가적으로 검색에 참여하게 되고, 검색 처리 요청이 더 많은 node로 분산되어 전체적인 검색 처리 속도가 증가하게 된다는 것이다.

  - Test를 위해 아래와 같은 구성으로 cluster를 생성한다.
    - node1, node2, node3
    - 세  노드의 구성은 모두 완전히 동일하게 한다.
    - 보다 간단한 test를 위해서 아래와 같이 search_worker의 thread 개수를 조정한다.

  ```yaml
  network.host: 0.0.0.0
  
  thread_pool:
      search_worker:
          size: 5
  ```

  - Test를 위한 index를 생성하고 data를 색인한다.
    - Primary와 replica shard의 개수를 각각 1로 설정한다.
    - Replica shard 수 변경에 따른 전체 처리 속도의 변화를 보기 위해 100만 건의 data를 색인한다.

  ```python
  import random
  
  from faker import Faker
  from elasticsearch import Elasticsearch, helpers
  
  
  class Bulker:
      def __init__(self):
          self.es_client = Elasticsearch("http://localhost:9200")
  
      def bulk_ko_data(self):
          fake = Faker("ko-KR")
          gender = ["남", "여", "무"]
          for i in range(100):
              bulk_data = []
              for _ in range(10000):
                  text = ""
                  for _ in range(50):
                      text += fake.catch_phrase() + " "
                  bulk_data.append({
                      "_index":"search_test",
                      "_source":{
                          "name":fake.name(),
                          "address":fake.address(),
                          "gender":random.choice(gender),
                          "age":random.randrange(20, 100),
                          "content":text.rstrip()
                      }
                  })
              helpers.bulk(self.es_client, bulk_data)
  
      
  if __name__ == "__main__":
      bulker = Bulker()
      bulker.bulk_ko_data()
  ```

  - 검색 속도 측정을 위한 스크립트를 작성한다.
    - 단일 검색의 속도 차이가 없다는 건 위에서 확인했으므로, 여기서는 1만 5천 번을 검색하는 데 걸리는 전체 시간을 확인해 볼 것이다.
    - 검색을 test하기 위한 quey는 검색 결과가 너무 빠르게 나오지는 않는 걸로 설정한다.

  ```python
  import time
  import asyncio
  
  from elasticsearch import AsyncElasticsearch
  
  
  async def search():
      es_client = AsyncElasticsearch("http://localhost:9200")
      N = 500
      query = {
          "bool": {
              "must": [
                  {
                      "script": {
                          "script": "doc['name.keyword'].value.length() > 2"
                      }
                  },
                  {
                      "match": {
                          "content": "분석"
                      }
                  },
                  {
                      "match_phrase": {
                          "content": "휴리스틱"
                      }
                  }
              ]
          }
      }
      for _ in range(N):
          await es_client.search(index="search_test", query=query)
      await es_client.close()
  
  
  async def main():
      await asyncio.wait([asyncio.create_task(search()) for _ in range(30)])
  
  
  if __name__ == "__main__":
      st = time.time()
      asyncio.run(main())
      print(time.time()-st)
  ```

  - 예상
    - 위 script는 30개의 검색 요청을 비동기적으로 거의 동시에 보낸다.
    - Cluster를 구성할 때 모든 node의 search_worker thread의 개수를 5로 설정했다.
    - 따라서 하나의 node에서 동시에 처리할 수 있는 검색 요청은 5개 뿐이므로, 두 node가 처리하는 10개의 검색 요청을 제외한 20개의 검색 요청은 queue에 쌓일 것이다.

  - 테스트를 실행한다.
    - 위 script가 실행되는 동안 아래 API를 통해 `search_worker`의 thread pool을 확인해보면 아래와 같은 결과가 나오는 것을 볼 수 있다.
    - `psz`는 thread pool 내의 thread의 개수, `a`는 현재 사용하고 있는 thread의 개수, `q`는 queue에서 대기 중인 검색 요청의 개수를 의미한다.
    - Shard를 가지고 있는 node1과 node2의 모든 thread가 활성화 되어 각각 5개씩 검색 요청을 처리하고 있고, 남은 20개의 요청이 queue에서 대기 중인 것을 확인할 수 있다.
    - node3은 shard를 할당 받지 않았으므로 아무 thread도 활성화 되지 않았고, queue에도 대기중인 요청도 없는 것을 확인할 수 있다.

  ```http
  GET _cat/thread_pool/search_worker?h=nn,n,t,psz,a,q&v
  
  nn    n             t     psz a  q
  node1 search_worker fixed   5 5 12
  node2 search_worker fixed   5 5  8
  node3 search_worker fixed   5 0  0
  ```

  - 이번에는 replica shard의 개수를 늘려 기존에는 shard를 할당 받지 않았던 node3도 shard를 할당 받아 검색에 참여하도록 한다.
    - 아래와 같이 replica shard의 개수를 변경한 후, 위와 동일한 script로 test를 실행한다.

  ```json
  // PUT search_test/_settings
  {
    "index" : {
      "number_of_replicas" : 2
    }
  }
  ```

  - 결과
    - Replica가 1개일 때 보다 2개일 때 전체 검색에 소요된 시간이 감소한 것을 확인할 수 있다.

  | replica의 개수 | 1    | 2    |
  | -------------- | ---- | ---- |
  | 시간           | 212  | 149  |

  - 주의
    - 상기했듯 이는 검색 속도 자체가 빨라지는 것은 아니다. 
    - 따라서 shard를 할당 받은 node들 만으로 검색을 처리하는 데 무리가 없다면(queue에 요청이 거의 쌓이지 않는다면) replica를 늘리더라도 별 효과는 없을 것이다.







