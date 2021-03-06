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



- 미할당 샤드 수동으로 재할당하기

  ```bash
  POST _cluster/reroute?retry_failed=true
  ```

  



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
  
  - `s`로 정렬이 가능하다.
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/indices?s=<정렬 할 내용>'
  
  #e.g.
  $ curl -XGET 'http://localhost:9200/_cat/indices?s=docs.count:desc'
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

  - 미할당 샤드가 있을 경우, `h` 옵션을 통해 미할당 된 원인을 확인할 수 있다.
    - `클러스터 운영하기`에서 살펴본  `explain`을 통해서도 확인이 가능하다.
    - 각 원인에 대한 설명은 [공식 가이드](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html#cat-shards-query-params) 참고

  ```bash
  # 어떤 인덱스의 어떤 샤드가 왜 미할당 상태인지 확인하는 명령어
  $ curl -XGET 'http://localhost:9200/_cat/shards?h=index,shard,prirep,unassigned.reason | grep -i UNASSIGNED'
  ```
  
  - 보다 정확한 원인을 알려주는 API
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cluster/allocation/explain'
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



- segment 상태 확인

  - `v`, `h`, `format` 옵션을 모두 사용 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/segments'
  ```

  

## stats API로 지표 확인하기

- GC(Garbage Collector)

  - 정의

    - Java로 만든 애플리케이션은 기본적으로 JVM이라는 가상 머신 위에서 동작하는데 OS는 JVM이 사용할 수 있도록 일정 크기의 메모리를 할당해준다.
    - 이 메모리 영역을 힙 메모리라고 부른다.
    - JVM은 힙 메모리 영역을 데이터를 저장하는 용도로 사용한다.
    - 시간이 갈수록 사용 중인 영역이 점점 증가하다가 어느 순간 사용할 수 있는 공간이 부족해지면 사용 중인 영역에서 더 이상 사용하지 않는 데이터들을 지워서 공간을 확보하는데 이런 일련의 과정을 가비지 컬렉션이라 부른다.

    - 사용 중인 영역은 young 영역과  old 영역 두 가지로 나뉜다.

  - Stop-The-World

    - GC 작업을 할 때, 즉 메모리에서 데이터를 지우는 동안에는 다른 스레드들이 메모리에 데이터를 쓰지 못하도록 막는다.
    - GC가 진행되는 동안에너는 다른 스레드들이 동작하지 못하기 때문에 애플리케이션이 응답 불가 현상을 일으키고 이를 Stop-The-World 현상이라 한다.
    - 특히 old GC는 비워야 할 메모리의 양이 매우 많기 때문에 경우에 따라서는 초 단위의 GC 수행 시간이 소요되기도 한다.
    - 이럴 경우 ES 클러스터가 초 단위의 응답 불가 현상을 겪게 된다.

  - Out Of Memory

    - GC를 통해 더 이상 메모리를 확보할 수 없는 상황에서 애플리케이션이 계쏙해서 메모리를 사용하고자 하면 가용할 메모리가 없다는 OOM 에러를 발생시킨다.
    - OOM  에러는 애플리케이션을 비정상 종료시키기 때문에 클러스터에서 노드가 아예 제외되는 현상이 발생한다.



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

- 주요 성능
  - 색인 성능
    - 초당 몇 개의 문서를 색인할 수 있는지, 그리고 각 문서를 색인하는 데 소요되는 시간이 어느 정도인지
    - 클러스터 전체 성능과 노드의 개별 성능으로 나누어 측정한다.
  - 검색 성능
    - 초당 몇 개의 쿼리를 처리할 수 있는지, 그리고 각 쿼리를 처리하는 데 소요되는 시간이 어느 정도인지
    - 클러스터 전체 성능과 노드의 개별 성능으로 나누어 측정한다.
  - GC 성능
    - GC가 너무 자주, 오래 발생하면 Stop-The-World 같은 응답 불가 현상이 발생한다.
    - Stop-The-World가 얼마나 자주, 오래 발생하는지를 나타낸다.
  - rejected
    - 클러스터가 처리할 수 없는 수준의 요청이 들어오면 클러스터는 요청을 거절하게 되는데 그 횟수를 나타낸다.



- 색인 성능

  - `_stats` 를 통해 확인 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_shards" : {
      "total" : 14,
      "successful" : 14,
      "failed" : 0
    },
    "_all" : {
      "primaries" : {		// 프라이머리 샤드에 대한 색인 성능
        "docs" : {
          "count" : 10,
          "deleted" : 1
        },
        "store" : {
          "size_in_bytes" : 92866
        },
        "indexing" : {
          "index_total" : 24,
          "index_time_in_millis" : 209,
          // (...)
        },
        // (...)
      "total" : {		// 전체 샤드에 대한 색인 성능
       // 내용은 primaries와 동일하다.
       //(...)
      }
    }
  }
  ```

  - 성능 측정
    - 위 요청을 10초 간격으로 보냈을 때, 첫 번째 호출시 색인된 문서의 수는 0개, 두 번째 호출시 색인된 문서의 수는 200개 라고 가정
    - 10 초 동안 200개의 문서가 색인됐다고 할 수 있다.
    - 또한 첫 번째 호출시 색인 소요 시간이 0초, 두 번째 호출 시 색인 소요 시간이 100ms라고 가정
    - 즉 10초 동안 200개의 문서를 색인했고, 색인하는데 10ms가 걸렸기 때문에 각각의 문서를 색인하는데 에는 200/100=2ms의 시간이 소요되었음을 알 수 있다.
    - 즉, 이 클러스터의 프라이머리 샤드에 대한 색인 성능은 2ms이다.
    - 색인하는 양이 많으면 많을수록 색인에 소요되는 시간도 늘어나기 때문에 두 값의 절대적인 값보다는 하나의 문서를 색인하는 데 시간이 얼마나 소요되는지를 더 중요한 성능 지표로 삼아야 한다.



- 검색 성능

  - query와 fetch
    - A, B, C 노드가 있을 때 사용자가 search API를 통해 A 노드에 검색 요청을 입력했다고 가정한다.
    - 그럼 노드 A는 자신이 받은 검색 쿼리를 B, C 노드에 전달한다.
    - 각각의 노드는 자신이 가지고 있는 샤드 내에서 검색 쿼리에 해당하는 문서가 있는지 찾는 과정을 진행한다.
    - 이 과정이 query이다.
    - 그리고 이렇게 찾은 문서들을 리스트 형태로 만들어서 정리하는 과정이 fetch이다.
    - 검색은 이렇게 query와 fetch의 과정이 모두 끝나야 만들어지기 때문에 검색 성능을 측정할 때 두 과정을 모두 포함하는 것이 좋다.
  - `_stats`을 통해 확인 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_shards" : {
      "total" : 14,
      "successful" : 14,
      "failed" : 0
    },
    "_all" : {
      // (...)
        "search" : {
          "open_contexts" : 0,
          "query_total" : 10916,	// 호출하는 시점까지 처리된 모든 query의 총합
          "query_time_in_millis" : 5496,
          "query_current" : 0,
          "fetch_total" : 10915,	// 호출하는 시점까지 처리된 모든 fetch의 총합
          "fetch_time_in_millis" : 476,
          "fetch_current" : 0,
          "scroll_total" : 9741,
          "scroll_time_in_millis" : 18944,
          "scroll_current" : 0,
          "suggest_total" : 0,
          "suggest_time_in_millis" : 0,
          "suggest_current" : 0
        },
      // (...)
      }
    }
  }
  ```

  - 성능 측정
    - 색인 성능 측정과 동일한 방식으로 진행하면 된다.
    - query와 fetch를 나눠서 진행한다.



- GC 성능 측정

  - 각 노드에서 발생하기 때문에 `_nodes/stats`를 통해 확인한다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표

  ```json
  // (...)
  "jvm" : {
      // (...)
    "gc" : {
      "collectors" : {
          "young" : {
              "collection_count" : 333,
              "collection_time_in_millis" : 1697
          },
          "old" : {
              "collection_count" : 3,
              "collection_time_in_millis" : 53
          }
      }
  }
  // (...)
  ```

  - 성능 측정
    - 색인과 동일한 방법으로 측정한다.
    - old, young을 각각 측정한다.
    - 상황에 따라 다르지만 보통 수십에서 수백 ms 정도의 성능을 내는 것이 안정적이다.



- rejected 성능 측정

  - rejected 에러
    - ES는 현재 처리할 수 있는 양보다 많은 양의 요청이 들어올 경우 큐에 요청을 쌓아놓는다.
    - 하지만 큐도 꽉 차서 더 이상 요청을 쌓아놓을 수 없으면 rejected 에러를 발생시키며 요청을 처리하지 않는다.
    - 보통 요청이 점차 늘어나서 초기에 구성한 클러스터의 처리량이 부족한 경우나, 평상시에는 부족하지 않지만 요청이 순간적으로 늘어나서 순간 요청을 처리하지 못하는 경우에 발생한다.
  - node별로 측정이 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표
    - 각 스레드 별로 확인할 수 있다.

  ```json
  // (...)
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
  // (...)
  ```

  - rejected 문제 해결
    - 만일 초기에 구성한 클러스터의 처리량이 부족하다면 데이터 노드를 증설하는 방법 외에는 특별한 방법이 없다.
    - 그러나 순간적으로 밀려들어오는 요청을 처리하지 못한다면 큐를 늘리는 것이 도움이 될 수 있다.
    - ` elasticsearch.yml` 파일에 아래와 같이 설정하면 된다.

  | 스레드 이름         | 스레드 풀 타입        | 설정 방법                                | 예시                                    |
  | ------------------- | --------------------- | ---------------------------------------- | --------------------------------------- |
  | get, write, analyze | fixed                 | thread_pool.[스레드 이름].queue_size     | thread_pool.write.queue_size=10000      |
  | search              | fixed_auto_queue_size | thread_pool.[스레드 이름].max_queue_size | thread_pool.search.max_queue_size=10000 |





# 분석 엔진으로 활용하기

- Elastic Stack이란
  - Elastic Stack은 로그를 수집, 가공하고 이를 바탕으로 분석하는 데 사용되는 플랫폼을 의미한다.
    - 이전에는 Elastic Stack을 ELK Stack이라고 불렀다.
    - Elastic Stack은 가급적 모든 구성 요소의 버전을 통일시키는 것이 좋다.
  - Elastic Stack은 아래와 같다.
    - 로그를 전송하는 Filebeat
    - 전송된 로그를 JSON 형태의 문서로 파싱하는 Logstash
    - 파싱된 문서를 저장하는 Elasticsearch
    - 데이터를 시각화 할 수 있는 kibana
  - Filebeat
    - 지정된 위치에 있는 로그 파일을 읽어서 Logstash 서버로 보내주는 역할을 한다.
    - Filebeat은 로그 파일을 읽기만 하고 별도로 가공하지 않기 때문에, 로그 파일의 포맷이 달라지더라도 별도의 작업이 필요치 않다.
    - 로그 파일의 포맷이 달라지면 로그 파일을 실제로 파싱하는 Logstash의 설정을 바꿔주면 되기 때문에 Filebeat과 Logstash의 역할을 분명하게 나눠서 사용하는 것이 확장성이나 효율성 면에서 좋다.
  - Logstash
    - Filebeat으로부터 받은 로그 파일들을 룰에 맞게 파싱해서 JSON 형태의 문서로 만드는 역할을 한다.
    - 하나의 로그에 포함된 정보를 모두 파싱할 수도 있고, 일부 필드만 파싱해서 JSON 문서로 만들 수도 있다.
    - 파싱할 때는 다양한 패턴을 사용할 수 있으며 대부분 **grok 패턴**을 이용해서 파싱 룰을 정의한다.
    - grok: 비정형 데이터를 정형 데이터로 변경해 주는 라이브러리
  - Elasticsearch
    - Logstash가 파싱한 JSON 형태의 문서를 인덱스에 저장한다.
    - 이 때의 ES는 데이터 저장소 역할을 한다.
    - 대부분의 경우 날짜가 뒤에 붙는 형태로 인덱스가 생성되며 해당 날짜의 데이터를 해당 날짜의 인덱스에 저장한다.
  - Kibana
    - ES에 저장된 데이터를 조회하거나 시각화할 때 사용한다.
    - 데이터를 기반으로 그래프를 그리거나 데이터를 조회할 수 있다.
    - Elastic Stack에서 사용자의 인입점을 맡게 된다.



- Elastic Stack 설치하기
  - 추후 추가(p.251-271)



- Elastic Stack의 이중화
  - Elastic Stack의 어느 한 구성 요소에 장애가 발생하더라도 나머지 요소들이 정상적으로 동작할 수 있도록 이중화하는 작업이 반드시 필요하다.
  - 추후 추가





# 검색 엔진으로 활용하기

## inverted index와 analyzer

- inverted index(역색인)

  - "I am a boy", "You are a girl" 이라는 두 문자열이 있다고 가정한다.
    - 위 두 개의 문자열을 공백을 기준으로 나누면 각각의 문자열은 4개의 단어로 나뉜다.
    - I, am, a, boy
    - you, are, a girl
  - 토큰
    - 위와 같이 나뉜 단어들을 **토큰**이라 부른다. 
    - 토큰을 만들어 내는 과정을 **토크나이징**이라고 한다.
  - 특정한 기준에 의해 나뉜 토큰들은 아래와 같은 형태로 저장되는데 이것을 역색인이라 부른다.

  | Tokens | Documents |
  | ------ | --------- |
  | I      | 1         |
  | am     | 1         |
  | a      | 1, 2      |
  | boy    | 1         |
  | girl   | 2         |
  | you    | 2         |
  | are    | 2         |

  - 위와 같은 역색인이 생성된 상태에서 사용자가 "a boy"라는 문자열이 포함된 문서를 찾고 싶다고 가정한다.
    - 검색어로 a boy라는 문자열을 입력하면 이 문자열은 공백을 기준으로 a, boy라는 두 개의 토큰으로 나뉜다.
    - 이렇게 나뉜 토큰을 바탕으로 역색인을 검색한다.
    - 두 단어가 모두 포함되어 있는 문서 1번이 검색 결과로 반환된다.
  - 대소문자 구분
    - 검색 결과를 얻기 위해서는 토큰이 대소문자까지 정확하게 일치해야 한다.
    - 역색인에 대문자 I만 존재할 뿐 소문자 i는 존재하지 않는다.
    - 따라서 소문자 i로 검색하면 아무런 검색 결과를 얻지 못한다.



- ES는 어떻게 토크나이징을 하는가

  - ES는 `_analyze`라는 API를 제공한다.
    - analyzer에는 토크나이징에 사용할 analyzer를 입력한다.
    - text에는 토크나이징 할 문자열을 입력한다.

  ```bash
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "analyzer":"standard",
  "text":"I am a boy"
  }'
  ```

  - 응답
    - 토크나이징의 결과로 토큰의 배열을 반환한다.
    - 아래 토큰을 보면 대문자 I가 아닌 소문자 i로 토크나이징 된 것을 볼 수 있는데, standard analyzer의 동작 중에 모든 문자를 소문자화하는 과정이 포함되어 있기 때문이다.

  ```json
  {
    "tokens" : [
      {
        "token" : "i",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- analyzer 
  - analyzer는 역색인을 만들어주는 것이다.
    - analyzer는 운영 중에 동적으로 변경할 수 없다. 
    - 따라서 기존 인덱스에 설정한 analyzer를 바꾸고 싶을 때는 인덱스를 새로 만들어서 재색인(reindex)해야 한다.
  - ES의 analyzer는 다음과 같이 구성된다.
    - character filter
    - tokenizer
    - token filter
  - character filter
    - analyzer를 통해 들어온 문자열들은 character filter가 1차로 변형한다.
    - 예를 들어 <, >, ! 등과 같은 의미 없는 특수 문자들을 제거한다거나 HTML 태그들을 제거하는 등 문자열을 구성하고 있는 문자들을 특정한 기준으로 변경한다.
  - tokenizer
    - tokenizer는 일정한 기준(공백이나 쉼표)에 의해 문자열은 n개의 토큰으로 나눈다.
    - analyzer를 구성할 때는 tokenizer를 필수로 명시해야 하며, 하나의 tokenizer만 설정할 수 있다.
    - 반면 character filter와 token filter는 필요하지 않을 경우 기술하지 않거나, 여러 개의 character filter와 token filter를 기술할 수 있다.
  - token filter
    - 토큰을 전부 소문자로 바꾸는 lowercase token filter가 대표적인 token filter이다.



- standard analyzer

  - 아무 설정을 하지 않을 경우 디폴터로 적용되는 애널라이저
  - filter
    - character filter가 정의되어 있지 않다.
    - standard tokenizer가 정의되어 있다.
    - lowercase token filter가 정의되어 있다.
    - stopwords로 지정한 단어가 토큰들 중에 존재 한다면 해당 토큰을 없애는 stop token filter가 존재하지만 기본값으로 비활성화 되어 있다.
  - standard tokenizer 요청
    - `analyzer`가 아닌 `tokenizer`를 입력한다.
    - 아직 token filter를 거치지 않았기에 I가 대문자이다.
  
  ```json
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "tokenizer":"standard",
  "text":"I am a boy"
  }'
  
  
  {
    "tokens" : [
      {
        "token" : "I",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- custom analyzer

  > https://esbook.kimjmin.net/06-text-analysis/6.3-analyzer-1/6.4-custom-analyzer
  >
  > https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html
  
  - 내장 애널라이저로 충분하지 않을 경우 직접 애널라이저를 만들 수 있다.
  - 애널라이저 정의 하기
    - type: `custom`을 입력하거나 아예  type 자체를 입력하지 않는다.
    - tokenizer: 애널라이저에 사용할 토크나이저를 입력한다(필수).
    - char_filter: 사용할 character filter들을 입력한다.
    - filter: 사용할 token filter들을 입력한다.
  
  ```bash
  $ curl -XPUT "localhost:9200/my_index" -H 'Content-type:application/json' -d '{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {	# 커스텀 애널라이저의 이름
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
  }'
  ```
  
  - 위에서 적용한 tokenizer, char_filter, filter도 custom해서 적용하는 것이 가능하다.
  
  ```bash
  $ curl -XPUT "localhost:9200/my_index" -H 'Content-type:application/json' -d '
  {
    "settings": {
      "analysis": {
        "analyzer": {
          "my_custom_analyzer": { 
            "char_filter": [
              "emoticons"	# 아래에서 custom한 emoticons라는 char_filter를 적용
            ],
            "tokenizer": "punctuation",	# 아래에서 custom한 punctuation이라는 tokenizer 적용
            "filter": [
              "lowercase",
              "english_stop"	# 아래에서 custom한 english_stop이라는 filter 적용
            ]
          }
        },
        "tokenizer": {
          "punctuation": { 
            "type": "pattern",
            "pattern": "[ .,!?]"
          }
        },
        "char_filter": {
          "emoticons": { 
            "type": "mapping",
            "mappings": [
              ":) => _happy_",
              ":( => _sad_"
            ]
          }
        },
        "filter": {
          "english_stop": { 
            "type": "stop",
            "stopwords": "_english_"
          }
        }
      }
    }
  }
  ```



- analyzer와 검색의 관계

  - analyze의 중요성
    - analyzer를 통해 생성한 토큰들이 역색인에 저장되고, 검색할 때는 이 역색인에 저장된 값을 바탕으로 문서를 찾는다.
    - 따라서 검색 니즈를 잘 파악해서 적합한 analyzer를 설정해야 한다.
  - 테스트 인덱스 생성

  ```bash
  $ curl -XPUT "localhost:9200/books?pretty" -H 'Content-type:application/json' -d '{
  	"mappings":{
  		"properties":{
  			"title":{"type":"text"},
  			"content":{"type":"keyword"}
  		}
  	}
  }'
  ```

  - 테스트 문서 색인

  ```bash
  $ curl -XPUT "localhost:9200/books/_doc/1?pretty" -H 'Content-type:application/json' -d '{
  "title":"Elasticsearch Training Book",
  "content":"Elasticsearch is open source search engine"
  }'
  ```

  - title로 검색하기
    - 정상적으로 검색이 된다.

  ```json
  $ curl "localhost:9200/books/_search?pretty&q=title:Elasticsearch"
  
  {
    "took" : 743,
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
          "_index" : "books",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.6931471,
          "_source" : {
            "title" : "Elasticsearch Training Book",
            "content" : "Elasticsearch is open source search engine"
          }
        }
      ]
    }
  }
  ```

  - content로 검색하기

  ```json
  $ curl "localhost:9200/books/_search?pretty&q=content:Elasticsearch"
  
  {
    "took" : 2,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 0,
        "relation" : "eq"
      },
      "max_score" : null,
      "hits" : [ ]
    }
  }
  ```

  - content 필드는 검색이 정상적으로 이루어지지 않았다.
    - title 필드는 text, content 필드는 keyword 타입으로 정의했다.
    - text 타입의 기본 analyzer는 standard analyzer이고, keyword 타입의 기본 analyzer는 keyword analyzer이다.
    - keyword analyzer는 standard analyzer와는 달리 문자열을 나누지 않고 통으로 하나의 토큰을 구성한다.
    - 즉 역색인에는 "Elasticsearch is open source search engine"라는 토큰만 존재한다.