# 클러스터 성능 모니터링과 최적화

## 클러스터의 상태 확인하기

- `_cat/health`

  - 클러스터의 상태를 확인하는 API
  - 기본형

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health'
  ```

  - `v` 옵션을 추가
    - 결과 값에 header를 추가해서 보여준다.

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health?v'
  ```

  - format 옵션을 추가
    - 지정한 format으로 보여준다.

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health?format=json'
  ```





- 클러스터 상태 정보

  - `format=json` 옵션을 줬을 때의 응답

  ```json
  [
    {
      "epoch" : "1620718739",		// API를 호출한 시간을 UNIX 시간 형태로 표현한 숫자
      "timestamp" : "07:38:59",	// API를 호출한 시간
      "cluster" : "es-docker-cluster",	// 클러스터 이름
      "status" : "green",		// 클러스터 상태
      "node.total" : "4",		// 전체 노드의 개수
      "node.data" : "3",		// 데이터 노드의 개수
      "shards" : "6",			// 샤드의 개수
      "pri" : "3",			// 프라이머리 샤드의 개수
      "relo" : "0",			// 클러스터에서 재배치되고 있는 샤드의 개수
      "init" : "0",			// 초기화되고 있는 샤드의 개수
      "unassign" : "0",		// 배치되지 않은 샤드의 개수
      "pending_tasks" : "0",	// 클러스터의 유지, 보수를 위한 작업 중 실행되지 못하고 큐에 쌓여 있는 작업의 개수
      "max_task_wait_time" : "-",	// pending_tasks에서 확인한 작업이 실행되기까지 소요된 최대 시간
      "active_shards_percent" : "100.0%"	// 정상적으로 동작하는 샤드의 비율
    }
  ]
  ```

  - `relo`
    - 0이 아니라면 샤드들이 재배치 되고 있다는 의미이다.
    - 지나치게 많은 샤드들이 재배치 되고 있을 경우 색인이나 검색 성능에 악영향을 줄 수 있기 때문에 재배치 되는 원인을 확인해 봐야 한다.

  - `init`
    - 0이 아니라면 그만큼의 프라이머리 혹은 레플리카 샤드가 새롭게 배치되고 있다는 의미이다.

  - `pending_tasks`
    - 0이 아니라면 클러스터가 부하 상황이거나 특정 노드가 서비스 불능 상태일 가능성이 있다.
  - `max_task_wait_time`
    - 이 값이 클수록 작업이 실행되지 못하고 오랫동안 큐에 있었다는 뜻이다.
    - 클러스터의 부하 상황을 나타내는 지표로 활용된다.
  - `active_shards_percent`
    - 100%가 아니라면 초기화중이거나 배치되지 않은 샤드가 존재한다는 의미이다.



- 클러스터의 상탯값

  | 값                                       | 의미                                                         |
  | ---------------------------------------- | ------------------------------------------------------------ |
  | <span style="color:green">green</span>   | 모든 샤드가 정상적으로 동작하고 있는 상태                    |
  | <span style="color:orange">yellow</span> | 모든 프라이머리 샤드는 정상적으로 동작하고 있지만, 일부 혹은 모든 레플리카 샤드가 정상적으로 동작하고 있지 않은 상태 |
  | <span style="color:red">red</span>       | 일부 혹은 모든 프라이머리/레플리카 샤드가 정상적으로 동작하고 있지 않은 상태, 데이터 유실이 발생할 수 있다. |





## 노드의 상태와 정보 확인하기

- `_cat/nodes`

  - 노드의 상태를 확인하는 API
  - `v`, `format`등의 옵션을 사용 가능하다.
  - `h` 옵션을 사용 가능하다.

  ```bash
  # 아래 명령을 사용하면 h 옵션에서 사용 가능한 값들을 확인 가능하다.
  $ curl -XGET 'http://localhost:9200/_cat/nodes?help'
  
  # h 옵션은 아래와 같이 주면 된다.
  $ curl -XGET 'http://localhost:9200/_cat/nodes?h=id,name,disk.used_percent'
  ```



- 노드 상태 정보

  ```json
  [
    {
      "ip" : "123.123.456.4",	// 노드의 IP 주소
      "heap.percent" : "15",	// 힙 메모리의 사용률
      "ram.percent" : "49",	// 메모리 사용률
      "cpu" : "4",			// 노드의 CPU 사용률
      "load_1m" : "2.11",		// 각각 1,5,15분의 평균 Load Average를 의미한다.
      "load_5m" : "2.21",
      "load_15m" : "2.20",
      "node.role" : "dilm",	// 노드의 역할
      "master" : "-",			// 마스터 여부, 마스터 노드는 *로 표시된다.
      "name" : "node2"		// 노드의 이름
    }
  ]
  ```

  - `heap.percent`
    - 이 값이 크면 클수록 사용 중인 힙 메모리의 양이 많다는 뜻이다.
    - 일정 수준 이상 커지면  old GC에 의해서 힙 메모리의 사용률이 다시 내려간다.
    - 만약 이 값이 낮아지지 않고 85% 이상을 계속 유지하면 OOM(Out Of Memory)이 발생할 가능성이 크기 때문에 힙 메모리가 올라가는 이유를 확인해 봐야 한다.
  - `ram.percent`
    - `heap.percent`가 JVM이 할당받은 힙 메모리 내에서의 사용률이라면 `ram.percent`는 노드가 사용할 수 있는 전체 메모리에서 사용 중인 메모리의 사용률이다.
    - 이 값은 대부분 90% 이상의 높은 값을 나타내는데, JVM에 할당된 힙 메모리 외의 영역은 OS에서 I/O 부하를 줄이기 위한 페이지 캐시로 사용하기 때문이다.

  - `cpu`
    - 이 값이 크면 CPU를 많이 사용하고 있다는 뜻이며, 경우에 따라서는 클러스터에 응답 지연 현상이 발생할 수 있다.

  - `load_nm`
    - 이 값이 크면 노드에 부하가 많이 발생하고 있다는 뜻이며 클러스터의 응답 지연이 발생할 수 있다.
    - Load Average는 노드에 장착된 CPU 코어의 개수에 따라 같은 값이라도 그 의미가 다를 수 있기 때문에 CPU Usage와 함께 살펴보는 것이 좋다.
    - CPU Usage와 Load Average가 모두 높다면 부하를 받고 있는 상황이다.
  - `node.role`
    - d는 데이터, m은 마스터, i는 인제스트, l은 머신러닝을 의미한다.



## 인덱스의 상태와 정보 확인하기

- `_cat/indices`

  - 인덱스의 상태도 green, yellow, red로 표현된다.
    - 인덱스들 중 하나라도 yellow면 클러스터도 yellow, 하나라도 red면 클러스터도 red가 된다.
  - `v`, `h`, `format` 옵션을 모두 사용 가능하다.
  - 확인
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/indices'
  ```
  



- 인덱스 상태 정보

  ```json
  // GET _cat/indices?format=json
  [
      {
          "health" : "green",	// 인덱스 상탯값
          "status" : "open",	// 사용 가능 여부
          "index" : "test",	// 인덱스명
          "uuid" : "cs4-Xw3WRM2FpT4bpocqFw",
          "pri" : "1",		// 프라이머리 샤드의 개수
          "rep" : "1",		// 레플리카 샤드의 개수
          "docs.count" : "0",		// 저장된 문서의 개수
          "docs.deleted" : "0",	// 삭제된 문서의 개수
          "store.size" : "566b",		// 인덱스가 차지하고 있는 전체 용량(프라이머리+레플리카)
          "pri.store.size" : "283b"	// 프라이머리 샤드가 차지하고 있는 전체 용량
        }
  ]
  ```



## 샤드의 상태 확인하기

- `_cat/shards`

  - 마찬가지로 `v`, `h`, `format` 모두 사용 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/shards'
  ```

  - `grep`을 사용 가능하다.
    - 아래와 같이 입력하면 state가 `UNASSIGNED`인 샤드만을 반환한다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/shards | grep UNASSIGNED'
  ```

  - 미할달 샤드가 있을 경우, `h` 옵션을 통해 미할당 된 원인을 확인할 수 있다.
    - `클러스터 운영하기`에서 살펴본  `explain`을 통해서도 확인이 가능하다.
    - 각 원인에 대한 설명은 [공식 가이드](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html#cat-shards-query-params) 참고

  ```bash
  # 어떤 인덱스의 어떤 샤드가 왜 미할당 상태인지 확인하는 명령어
  $ curl -XGET 'http://localhost:9200/_cat/shards?h=index,shard,prirep,unassigned.reason | grep -i UNASSIGNED'
  ```



- 응답

  ```json
  [
  	{
          "index" : "test",		// 샤드가 속한 인덱스명
          "shard" : "0",			// 샤드 번호
          "prirep" : "p",			// 프라이머리인지 레플리카인지(레플리카는 r)
          "state" : "STARTED",	// 샤드의 상태
          "docs" : "0",			// 샤드에 저장된 문서의 수
          "store" : "283b",		// 샤드의 크기
          "ip" : "123.456.789.1",	// 샤드가 배치된 노드의 IP
          "node" : "node2"		// 샤드가 배치된 데이터 노드의 노드 이름
    	}
  ]
  ```

  - state

  | 값           | 의미                                                         |
  | ------------ | ------------------------------------------------------------ |
  | STARTED      | 정상적인 상태                                                |
  | INITIALIZING | 샤드를 초기화하는 상태. 최초 배치 시, 혹은 샤드에 문제가 발생하여 새롭게 배치할 때의 상태 |
  | RELOCATING   | 샤드가 현재의 노드에서 다른 노드로 이동하고 있는 상태. 새로운 데이터 노드가 추가되거나, 기존 데이터 노드에 문제가 생겨서 샤드가 새로운 노드에 배치되어야 할 때의 상태 |
  | UNASSIGNED   | 샤드가 어느 노드에도 배치되지 않은 상태. 해당 샤드가 배치된 노드에 문제가 생기거나 클러스터의 라우팅 정책에 의해 배치되지 않은 상태. |



## stats API로 지표 확인하기

- 클러스터 성능 지표 확인하기

  - 명령어

  ```bash
  $ curl -XGET 'http://localhost:9200/_cluster/stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_nodes" : {
      "total" : 4,
      "successful" : 4,
      "failed" : 0
    },
    "cluster_name" : "es-docker-cluster",
    "cluster_uuid" : "bOfgi147StyhjT2sOzdPYw",
    "timestamp" : 1620780055464,
    "status" : "green",
    "indices" : {
      // (...)
      "docs" : {
        "count" : 9,		// 색인된 전체 문서의 수
        "deleted" : 1		// 삭제된 전체 문서의 수
      },
      "store" : {
        "size_in_bytes" : 140628	// 저장 중인 데이터의 전체 크기를 bytes 단위로 표시
      },
      "fielddata" : {
        "memory_size_in_bytes" : 0,	// 필드 데이터 캐시의 크기
        "evictions" : 0
      },
      "query_cache" : {
        "memory_size_in_bytes" : 0,	// 쿼리 캐시의 크기
        // (...)
      },
      "completion" : {
        "size_in_bytes" : 0
      },
      "segments" : {
        "count" : 17,		// 세그먼트의 수
        "memory_in_bytes" : 28061,	// 세그먼트가 차지하고 있는 메모리의 크기
        // (...)
      }
    },
    // (...)
      "versions" : [	// 클러스터를 구성하고 있는 노드들의 버전
        "7.5.2"
      ],
      // (...)
      "jvm" : {
        "max_uptime_in_millis" : 69843238,
        "versions" : [	// 클러스터를 구성하고 있는 노드들의 JVM 버전
          {
            "version" : "13.0.1",
            "vm_name" : "OpenJDK 64-Bit Server VM",
            "vm_version" : "13.0.1+9",
            "vm_vendor" : "AdoptOpenJDK",
            "bundled_jdk" : true,
            "using_bundled_jdk" : true,
            "count" : 4
          }
        ],
     // (...)
  }
  ```

  - `fielddata.memory_size_in_bytes`
    - 필드 데이터는 문자열 필드에 대한 통계 작업을 할 때 필요한 데이터이다.
    - 필드 데이터의 양이 많으면 각 노드의 힙 메모리 공간을 많이 차지하기 때문에 이 값이 어느 정도인지 모니터링해야 한다.
    - 노드들의 힙 메모리 사용률이 높다면 우선적으로 필드 데이터의 유무를 확인하는 것이 좋다.

  - `query_cache.memory_size_in_bytes`
    - 모든 노드들은 쿼리의 결과를 캐싱하고 있다.
    - 이 값이 커지면 힙 메모리를 많이 차지하기에 이 값이 어느정도인지 모니터링해야 한다.

  - `segments.memory_in_bytes`
    - 세그먼트도 힙 메모리 공간을 차지하기 때문에 힙 메모리의 사용률이 높을 경우 세그먼트의 메모리가 어느 정도를 차지하고 있는지 살펴봐야 한다.
    - forcemerge API를 사용하여 세그먼트를 강제 병합하면 세그먼트의 메모리 사용량도 줄일 수 있다.



- 노드의 성능 지표

  - 명령어

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_nodes" : {
      "total" : 4,
      "successful" : 4,
      "failed" : 0
    },
    "cluster_name" : "es-docker-cluster",
    "nodes" : {
      "rrqnQp2mRUmPh8OGqTj0_w" : {	// 노드의 ID, 클러스터 내부에서 임의의 값을 부여한다.
        "timestamp" : 1620781452291,
        "name" : "node2",				// 노드의 이름
        "transport_address" : "192.168.240.5:9300",
        "host" : "192.168.240.5",
        "ip" : "192.168.240.5:9300",
        "roles" : [		// 노드가 수행할 수 있는 역할
          "ingest",
          "master",
          "data",
          "ml"
        ],
        "attributes" : {
          "ml.machine_memory" : "134840213504",
          "ml.max_open_jobs" : "20",
          "xpack.installed" : "true"
        },
        "indices" : {
          "docs" : {
            "count" : 9,		// 노드가 지니고 있는 문서의 수
            "deleted" : 1
          },
          "store" : {
            "size_in_bytes" : 70928	// 노드가 저장하고 있는 문서의 크기를 byte 단위로 표시
          },
          "indexing" : {
            "index_total" : 23,		// 지금까지 색인한 문서의 수
            "index_time_in_millis" : 192,	// 색인에 소요된 시간
            // (...)
          },
          "get" : {			// REST API의 GET 요청으로 문서를 가져오는 성능에 대한 지표(검색 성능보다는 문서를 가져오는 성능을 의미한다)
            // (...)
          },
          "search" : {		// 검색 성능과 관련된 지표
            // (...)
          },
          "merges" : {		// 세그먼트 병합과 관련된 성능 지표
            // (...)
          },
          // (...)
          "query_cache" : {		// 쿼리 캐시와 관련된 지표
            // (...)
          },
          "fielddata" : {			// 필드 데이터 캐시와 관련된 지표
            "memory_size_in_bytes" : 0,
            "evictions" : 0
          },
          "completion" : {
            "size_in_bytes" : 0
          },
          "segments" : {			// 노드에서 사용중인 세그먼트와 관련된 지표
            // (...)
          },
          // (...)
        },
        "os" : {
          "timestamp" : 1620781452298,
          "cpu" : {
            "percent" : 3,	// 노드의 CPU 사용률
            "load_average" : {	// 노드의 Load Average 사용률(각 1,5,15분 평균을 의미)
              "1m" : 1.99,
              "5m" : 1.9,
              "15m" : 1.9
            }
          },
          // (...)
          "gc" : {		// GC와 관련된 성능 지표
            "collectors" : {
              "young" : {
                "collection_count" : 317,
                "collection_time_in_millis" : 1595
              },
              "old" : {
                "collection_count" : 3,
                "collection_time_in_millis" : 53
              }
            }
          },
          // (...)
        },
        "thread_pool" : {		// 노드의 스레드 풀 상태
          // (...)
          "search" : {
            "threads" : 73,
            "queue" : 0,
            "active" : 0,
            "rejected" : 0,
            "largest" : 73,
            "completed" : 10917
          },
          // (...)
          "write" : {
            "threads" : 32,
            "queue" : 0,
            "active" : 0,
            "rejected" : 0,
            "largest" : 32,
            "completed" : 32
          }
        },
        "fs" : {
          "timestamp" : 1620781452302,
          "total" : {		// 디스크의 사용량을 의미한다.
            "total_in_bytes" : 1753355112448,
            "free_in_bytes" : 1117627813888,
            "available_in_bytes" : 1028490833920	// 현재 남아 있는 용량
          },
          // (...)
      }
    }
  }
  ```

  - `indexing.index_total`
    - 카운터 형식의 값으로 0부터 계속해서 값이 증가한다.
    - 지금 호출한 값과 1분 후에 호출한 값이 차이가 나며 이 값의 차이가 1분 동안 색인된 문서의 개수를 나타낸다.
    - 색인 성능을 나타내는 매우 중요한 지표 중 하나이다.

  - `thread_pool`
    - 검색에 사용하는 search 스레드, 색인에 사용하는 write 스레드 등  스레드들의 개수와 큐의 크기를 보여준다.
    - rejected가 매우 중요한데, 현재 노드가 처리할 수 있는 양보다 많은 요청이 들어오고 있기 때문에 더 이상 처리할 수 없어서 처리를 거절한다는 의미이기 때문이다.

 



## 성능 확인과 문제 해결













# 데이터 처리

## 새로운 데이터 색인

- curl 명령의 기본 형식

  ```bash
  curl -X 메소드 'http://연결할 일레스틱 서치 노드의 호스트명:연결할 포트/색인명/_doc/문서id'
  ```

  - `-X` 
    - request시 사용할 메소드의 종류를 기술한다. 메소드와 띄어 써도 되지만 붙여 써도 된다.
    - 새로운 문서 입력은 PUT, 기존 문서의 수정은 POST, 삭제는 DELETE, 조회는 GET을 사용한다.
    - `-XGET`의 경우 생략이 가능하다.

  - _doc
    - ES5 버전 이하에서는 멀티 타입을 지원해서 하나의 인덱스 안에 다양한 타입의 데이터를 저장할 수 있었다.
    - ES6  버전부터는 하나의 인덱스에 하나의 타입만 저장할 수 있게 되었기에 본래 타입이 올 자리에 _doc을 입력한다.



- 삽입

  - curl을 활용하여 삽입
    - 파라미터로 들어간 `pretty` 또는 `pretty-true`는 JSON  응답을 더 보기 좋게 해준다.
    - `-H` 옵션은 header를 지정한다.
    - `-d` 옵션은 body를 지정한다.

  ```bash
  $ curl -XPUT 'localhost:9200/company/_doc/1?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Theo",
  "age":"28"
  }'
  ```

  - 응답
    - 응답은 색인, 타입, 색인한 문서의 ID를 포함한다.

  ```json
  {
    "_index" : "company",
    "_type" : "colleague",
    "_id" : "1",
    "_version" : 1,
    "result" : "created",  // 새로 생성한 것이므로 created로 뜨지만, 수정할 경우 updated라고 뜬다.
    "_shards" : {
      "total" : 2,
      "successful" : 1,
      "failed" : 0
    },
    "_seq_no" : 0,
    "_primary_term" : 1
  }
  ```

  - POST 메서드로도 추가가 가능하다.
    - 둘의 차이는 POST의 경우 도큐먼트id를 입력하지 않아도 자동으로 생성하지만 PUT은 자동으로 생성하지 않는다는 것이다.

  - 실수로 기존 도큐먼트가 덮어씌워지는 것을 방지하기 위해 입력 명령어에 `_doc` 대신 `_create`를 사용해서 새로운 도큐먼트의 입력만 허용하는 것이 가능하다.
    - 이 경우 이미 있는 도큐먼트id를 추가하려 할 경우 오류가 발생한다.
    - 이미 위에서 도큐먼트id가 1인 도큐먼트를 추가했으므로 아래 예시는 오류가 발생한다. 

  ```json
  PUT company/_create/1
  
  {
      "nickname":"Theo",
      "message":"안녕하세요!"
  }
  ```




- 색인 과정
  - 추후 추가



- 색인 생성과 매핑 이해하기(ES6부터는 하나의 인덱스에 하나의 타입만 저장할 수 있도록 변경)

  - curl 명령은 색인과 매핑타입을 자동으로 생성한다.
    - 위 예시에서 company라는 색인과 colleague라는 매핑 타입을 생성한 적이 없음에도 자동으로 생성되었다.
    - 수동으로 생성하는 것도 가능하다.
  - 색인을 수동으로 생성하기

  ```bash
  $ curl -XPUT 'localhost:9200/new-index'
  ```

  - 수동 생성의 응답

  ```json
  {
    "acknowledged" : true,
    "shards_acknowledged" : true,
    "index" : "test-index"
  }
  ```

  - 스키마 확인
    - 스키마를 보기 위해 url에 `_mapping`을 추가한다.
    - ES 6.x 이상의 경우 _doc타입이 아닌 타입을 따로 지정했을 경우 아래와 같이 `include_type_name=true` 또는 `include_type_name`을 파라미터로 넣어야 한다.

  ```bash
  $ curl 'localhost:9200/company/_mapping/colleague?include_type_name&pretty'
  ```

  - 응답
    - 색인 명, 타입, 프로퍼티 목록, 프로퍼티 옵션 등의 데이터가 응답으로 넘어 온다.

  ```json
  {
    "company" : {
      "mappings" : {
        "colleague" : {
          "properties" : {
            "age" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        }
      }
    }
  }
  ```



## 데이터 검색

- 검색하기

  - 검색을 위해 데이터를 더 추가

  ```bash
  $ curl -XPUT 'localhost:9200/company/colleague/2?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Kim",
  "age":"26"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/3?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Lee",
  "age":"27"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/4?pretty' -H 'Content-Type: application/json' -d '{
  "name":"An",
  "age":"27"
  }'
  ```

  - 데이터 검색하기
    - `q`파라미터는 검색할 내용이 들어간다.
    - 특정 필드에서만 찾고자 할 때는 `q=name:Kim`과 같이 작성하면 된다.
    - 아래와 같이 필드를 지정해주지 않을 경우 `_all`이라는 모든 필드의 내용을 색인하는 필드가 자동으로 들어가게 된다.
    - `_source` 파라미터는 특정 필드만 반환되도록 한다(유사한 파라미터로 `stored_fileds`가 있다).
    - `size` 파라미터는 일치하는 데이터들 중 반환할 데이터의 수를 지정한다(기본값은 10이다).

  ```json
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 어디를 검색할지 설정하기

  - 다수의 타입에서 검색하기
    - url에서 타입을 콤마로 구분하여 검색하면 된다.
    - ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/colleague, department/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 모든 타입에서 검색하기
    - 타입을 지정하지 않고 검색하면 된다.
    - 역시 ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 다수의 색인을 검색하기
    - url에서 인덱스를 콤마로 구분하여 검색하면 된다.
    - 만일 검색하려는 색인이 없는 경우 에러가 발생하는데 에러를 무시하려면 `ignore_unavailable` 플래그를 주면 된다.

  ```bash
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty"
  
  # 없는 인덱스도 포함해서 검색하기
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty&ignore_unavailable"
  ```

  - 모든 색인을 검색하기
    - url의 색인이 올 자리에 `_all`을 입력하거나 아예 색인을 빼면 모든 색인에서 검색한다.

  ```bash
  $ curl "localhost:9200/_all/_search?q=Kim&_source=name&size=1&pretty"
  
  $ curl "localhost:9200/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 응답 내용

  - 요청

  ```bash
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 응답

  ```json
  {
    // 요청이 얼마나 걸렸으며, 타임아웃이 발생했는가
    "took" : 1,
    "timed_out" : false,
    // 몇 개의 샤드에 질의 했는가
    "_shards" : {
    "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      // 일치하는 모든 문서에 대한 통계
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      // 결과 배열
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim"
          }
        }
      ]
    }
  }
  ```

  - 시간
    - `took` 필드는 ES가 요청을 처리하는 데 얼마나 걸렸는지 말해준다(단위는 밀리 초).
    - `timed_out` 필드는 검색이 타임아웃 되었는지 보여준다.
    - 기본적으로 검색은 절대로 타임아웃이 되지 않지만, 요청을 보낼 때`timeout` 파라미터를 함께 보내면 한계를 명시할 수 있다.
    - `$ curl "localhost:9200/_search?q=Kim&timeout=3s"`와 같이 작성할 경우 3초가 지나면 타임아웃이 발생하고 `timed_out`필드의 값은 true가 된다.
    - 타임아웃이 발생할 경우 타임아웃될 때까지의 결과만 반환된다.
  - 샤드
    - 총 몇 개의 샤드에 질의 했고 성공한 것과 스킵한 것, 실패한 것에 대한 정보를 반환한다.
    - 만일 특정 노드가 이용 불가 상태라 해당 노드의 샤드를 검색하지 못했다면 질의에 실패한 것이 된다.
  - 히트 통계
    - `total`은 전체 문서 중 일치하는 문서 수를 나타낸다.
    - `total`은 `size`를 몇으로 줬는지와 무관하게 일치하는 모든 문서의 수를 표시해주므로 total과 실제 반환 받은 문서의 수가 다를 수 있다.
    - `max_score`는 일치하는 문서들 중 최고 점수를 볼 수 있다.
  - 결과 문서
    - 히트 배열에 담겨 있다.
    - 일치하는 각 문서의 색인, 타입, ID, 점수 등의 정보를 보여준다.



- 쿼리로 검색하기

  - 지금까지는 URI 요청으로 검색했다.
    - 간단한 검색에는 좋지만 복잡한 검색에는 적절치 못한 방법이다.
  - `query_string` 쿼리 타입으로 검색하기
    - 쿼리스트링 타입의 쿼리를 실행하는 명령문이다.
    - `default_field`는 검색을 실행할 필드를 특정하기 위해 사용한다.
    - `default_operator`는 검색할 단어들이 모두 일치하는 문서를 찾을 지, 하나라도 일치하는 문서를 찾을지를 설정한다(기본값은 OR로 하나라도 일치하는 문서는 모두 찾는다).
    - 위 두 옵션(`default_field`, `default_operator`)을 다음과 같이 쿼리 스트링 자체에 설정하는 것도 가능하다.
    - `"query":"name:Kim AND name:Lee"`

  ```bash
  $ curl 'localhost:9200/company/colleague/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
      "query_string":{
        "query":"Kim",
        "default_field":"name",
        "default_operator":"AND"
      }
    }
  }'
  ```

  - 응답

  ```json
  {
    "took" : 1,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim",
            "age" : "26"
          }
        }
      ]
    }
  }
  ```



- 필터 사용(ES 6.X 부터 사용 불가)

  - 필터는 결과에 점수를 반환하지 않는다.
    - 쿼리는 결과와 함께 각 결과의 점수를 반환한다.
    - 필터는 오직 키워드가 일치하는지만 판단하여 일치하는 값들을 반환한다.
  - 필터 검색

  ```bash
  $ curl 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
    	"filtered":{
    	  "filter":{
      	"term" :{
            "name":"Kim"
          }
    	  }
    	}    
    }
  }'
  ```



- ID로 문서 가져오기

  - 검색은 준실시간인데 반해 문서 ID로 문서를 찾는 것은 실시간이다.
  - 특정 문서를 가져오려면 문서가 속한 색인과 타입, 그리고 ID를 알아야 한다.
    - 그러나 타입은 현재 사라졌기 때문에 type 자리에 `_doc`을 입력하여 검색한다.
    - 타입을 입력해도 검색은 되지만 경고문이 뜬다.

  ```json
  // _doc 사용
  $ curl 'localhost:9200/company/_doc/1?pretty'
  
  // 타입 사용
  $ curl 'localhost:9200/company/colleague/1?pretty'
  ```

  - 응답
    - 만일 찾는 문서가 존재하지 않으면 아래 `found`는 false가 된다.

  ```json
  {
    "_index" : "company",
    "_type" : "_doc",
    "_id" : "1",
    "_version" : 5,
    "_seq_no" : 5,
    "_primary_term" : 1,
    "found" : true,
    "_source" : {
      "name" : "Theo",
      "age" : "28"
    }
  }
  ```





## 데이터 수정, 삭제

- 삭제

  - 도큐먼트 또는 인덱스 단위의 삭제가 가능하다.
    - 도큐먼트를 삭제하면 `"result":"deleted"`가 반환된다.
    - 도큐먼트는 삭제되었지만 인덱스는 남아있는 경우, 삭제된 도큐먼트를 조회하려하면 `"found":false`가 반환된다.
    - 삭제된 인덱스의 도큐먼트를 조회하려고 할 경우(혹은 애초에 생성된 적 없는 도큐먼트를 조회할 경우) 에러가 반환된다.

  - 도큐먼트를 삭제하는 경우

  ```json
  DELETE office/_doc/1
  ```

  - 도큐먼트 삭제의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "deleted",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 삭제된 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 삭제된 도큐먼트를 조회했을 경우의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "found": false
  }
  ```

  - 인덱스를 삭제

  ```json
  DELETE office
  ```

  - 인덱스 삭제의 응답

  ```json
  {
      "acknowledged": true
  }
  ```

  - 삭제된 인덱스의 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 응답

  ```json
  {
      "error": {
          "root_cause": [
              {
                  "type": "index_not_found_exception",
                  "reason": "no such index [office]",
                  "resource.type": "index_expression",
                  "resource.id": "office",
                  "index_uuid": "_na_",
                  "index": "office"
              }
          ],
          "type": "index_not_found_exception",
          "reason": "no such index [office]",
          "resource.type": "index_expression",
          "resource.id": "office",
          "index_uuid": "_na_",
          "index": "office"
      },
      "status": 404
  }
  ```



- 수정

  - 위에서 삭제한 데이터를 다시 생성했다고 가정
  - 수정 요청

  ```json
  POST office/_doc/1
  
  {
      "nickname":"Oeht",
      "message":"!요세하녕안"
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "updated",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 수정할 때 특정 필드를 뺄 경우 해당 필드가 빠진 채로 수정된다.
    - POST 메서드로도 수정이 가능한데 POST 메서드를 사용해도 마찬가지다.

  ```json
  // 요청
  POST office/_doc/1
  
  {
      "nickname":"Theo"
  }
  
  // 응답
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "_seq_no": 9,
      "_primary_term": 1,
      "found": true,
      "_source": {
          // message 필드가 사라졌다.
          "nickname": "Theo"
      }
  }
  ```

  - `_update`
    - `_update`를 활용하면 일부 필드만 수정하는 것이 가능하다.
    - 업데이트 할 내용에 `"doc"`이라는 지정자를 사용한다.

  ```json
  // 도큐먼트id가 2인 새로운 도큐먼트를 생성했다고 가정
  POST office/_update/2
  
  {
      "doc":{
          "message":"반갑습니다.!"
      }
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "2",
      "_version": 2,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
          "nickname": "Oeht",
          "message": "반갑습니다!"
      }
  }
  ```



## 벌크 API

- `_bulk`

  - 복수의 요청을 한 번에 전송할 때 사용한다.
    - 동작을 따로따로 수행하는 것 보다 속도가 훨씬 빠르다.
    - 대량의 데이터를 입력할 때는 반드시 `_bulk` API를 사용해야 불필요한 오버헤드가 없다.
  - 형식
    - index, create, update, delete의 동작이 가능하다.
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



- json 파일에 실행할 명령을 저장하고 curl 며영으로 실행시킬 수 있다.

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



# 참고

https://esbook.kimjmin.net/