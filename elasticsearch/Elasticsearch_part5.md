# 색인 성능 최적화

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



- _all 필드 비활성화

  - **5.X 이하 버전에만 해당**한다.

  - 필요할 경우 찾아 볼 것(p.360~370)



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





# 검색 성능 최적화

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

  - filter context에 의해 검색된 문서의 결과가 캐싱되는 영역
    - 사용자가 filter context로 구성된 쿼리로 검색하면 내부적으로 각 문서에 0과 1로 설정할 수 있는 bitset을 설정한다.
    - filter context로 호출한 적이 있는 문서는 bitset을 1로 설정하여 사용자가 호출한적이 있다는 것을 문서에 표시해둔다.
    - ES는 문서별로 bitset을 설정하면서, 사용자의 쿼리 횟수와 bitset이 1인 문서들 사이에 연관 관계를 지속적으로 확인한다.
    - bitset이 1인 문서들 중에 자주 호출되었다고 판단한 문서들을 노드의 메모리에 캐싱한다.
    - 다만 세그먼트 하나에 저장된 문서의 수가 1만개 미만이거나, 검색 쿼리가 인입되고 있는 인덱스가 전체 인덱스 사이즈의 3% 미만일 경우에는 filter context를 사용하더라도 캐싱되지 않는다.
  - 아래 명령어로 Query Cache Memory의 용량을 확인 가능하다.

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,qcm"
  ```

  - 기본적으로 활성화되어 있으며, 아래와 같이 변경이 가능하다.
    - dynamic setting이 아니기에 인덱스를 close로 바꾸고 설정해줘야 한다.

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



- Shard Request Cache

  - Node Query Cache가 노드에 할당된 캐시 영역이라면 Shard Request Cache는 샤드를 대상으로 캐싱되는 영역이다.
    - 특정 필드에 의한 검색이기 때문에 전체 샤드에 캐싱된다.
    - Node Query Cache와 달리 문서의 내용을 캐싱하는 것이 아니라, 집계 쿼리의 집계 결과 혹은 ReqeustBody의 파라미터 중 size를 0으로 설정했을 때의 쿼리 응답 결과에 포함되는 매칭된 문서의 수에 대해서만 캐싱한다.
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

  - Node Query Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/my_index/_cache/clear?query=true" -H 'Content-type:application/json'
  ```

  - Shard Request Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/my_index/_cache/clear?request=true" -H 'Content-type:application/json'
  ```

  - Field Data Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/my_index/_cache/clear?fielddata=true" -H 'Content-type:application/json'
  ```

  