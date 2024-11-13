# Redis

- 캐시

  - 한 번 읽어온 데이터를 임의의 공간에 저장하여 다음에 읽을 때는 빠르게 결과값을 받을 수 있도록 도와주는 공간

  - Cache 사용 구조
    - Cache Hit: DB에 데이터를 요청하기 전에 Cache에 데이터가 있는지 확인하고 있으면, 데이터를 DB에 요청하지 않고 캐시에서 가져오는 것.
    - Cache Miss: cache 서버에 데이터가 없어 DB에 해당 데이터를 요청하는 것, DB에서 요청 받을 데이터를 다음 번에는 캐시에서 사용하기 위해 캐시에 저장한다.
  - 캐시를 사용하는 경우
    - 영구적으로 저장해야 하는 데이터가 아닐 경우에 DB가 아닌 캐시에 저장하면 보다 빠르게 데이터에 접근 할 수 있고, DB의 부하도 감소시킬 수 있다.
    - 동시다발적인 쓰기가 발생하는 경우, 갑자기 쓰기 요청이 몰려들 경우 DB에 과부하가 걸릴 수 있다. 따라서, 캐시에 일시적으로 저장 한 후 캐시에 저장된 데이터를 DB에 순차적으로 삽입하는 방식을 사용하면, 이러한 부하를 감소시킬 수 있다.
  - 한계
    - 캐시 서버는 속도를 위해 주로 메모리를 사용한다.
    - 따라서 서버에 장애가 나면 메모리가 날아가서 데이터가 손실될 수 있다.



- Redis(Remote Dictionary Server)
  - 키-값 기반의 인-메모리 데이터 저장소.
    - 인-메모리란 컴퓨터의 메인 메모리(RAM)에 DB 데이터와 같은 주요 데이터를 저장하는 것을 말한다.
    - 오픈소스이다.
  - 특징
    - 키-값 기반이기 때문에 키만 알고 있다면 바로 값에 접근할 수 있다.
    - 또한 디스크에 데이터를 쓰는 구조가 아니라 메모리에서 데이터를 처리하기 때문에 속도가 상당히 빠르다.
    - Single threaded로 한 번에 단 하나의 명령어만 실행할 수 있다.
    - 다양한 데이터 구조를 제공하여, 캐시 데이터 저장 외에도 인증 토큰 저장, Ranking Board 등으로도 주로 사용된다.
  - Redis는 굉장히 다양한 자료구조를 지원한다.
    - Strings: 단순한 키-값 매핑 구조.
    - Lists: 배열 형식의 데이터 구조, 처음과 끝에 데이터를 넣고 빼는 것은 속도가 빠르지만, 중간에 데이터를 삽입할 때는 어려움이 있다.
    - Sets: 순서가 없는 Strings 데이터 집합, 중복된 데이터는 하나로 처리하기 때문에, 중복에 대한 걱정을 하지 않아도 된다.
    - Sorted Sets: Sets과 같은 구조지만, Score를 통해 정렬이 가능하다.
    - Hashes: 키-값 구조를 여러개 가진 object 타입을 저장하기 좋은 구조이다.
    - Bitmaps: 0,1로 이루어진 구조.
    - Bit field 
    - Geospatial Index: 지구상 두 지점의 경도(longitude)와 위도(latitude)를 저장
    - Hyperloglogs: 집합의 카디널리티(원소의 갯수)를 추정하기 위한 데이터 구조.
    - Streams: 로그를 처리하는데 최적화된 자료 구조



- Redis의 메모리 관리
  - maxmemory
    - Redis의 메모리 한계 값을 설정한다.
  - maxmemory 초과로 인해서 데이터가 지워지게 되는 것을 eviction이라고 한다.
    - Redis에 들어가서 INFO 명령어를 친 후 `eviced_keys` 수치를 보면 eviction이 왜 발생했는지 알 수 있다.
    - Amazon Elasticache를 사용하는 경우 mornitoring tab에 들어가면 eviction에 대한 그래프가 있는데, 이를 통해 Eviction 여부에 대한 알람을 받는 것이 가능하다.
  - maxmemory-policy
    - maxmemory에서 설정해준 수치까지 메모리가 다 차는 경우 추가 메모리를 확보하는 방식에 관한 설정.
    - noeviction: 기존 데이터를 삭제하지 않는다. 메모리가 꽉 차면 OOM 에러를 반환하고 새로운 데이터는 버린다.
    - allkeys-lru: LRU(Least Recently Used)라는 페이지 교체 알고리즘을 통해 데이터를 삭제하여 공간을 확보한다.
    - volatile-random: expire set을 가진 것 중 랜덤으로 데이터를 삭제하여 공간을 확보한다.
    - volatile-ttl: expire set을 가진 것 중 TTL(Time To Live) 값이 짧은 것부터 삭제한다.
    - allkeys-lfu: 가장 적게 액세스한 키를 제거하여 공간을 확보한다.
    - volate-lfu: expire set을 가진 것 중 가장 적게 액세스한 키부터 제거하여 공간을 확보한다.
  - COW(Copy On Write)
    - 쓰기 요청이 오면 OS는 `fork()`를 통해서 자식 프로세스를 생성한다.
    - `fork()`시에는 다른 가상 메모리 주소를 할당받지만 물리 메모리 블록을 공유한다.
    - 쓰기 작업을 시작하는 순간에는 수정할 메모리 페이지를 복사한 후에 쓰기 작업을 진행한다.
    - 즉 기존에 쓰던 메모리보다 추가적인 메모리가 필요하다.
    - 전체 페이지 중에서 얼마나 작업이 진행될지를 모르기 때문에 fork시에는 기본적으로 복사할 사이즈만큼의 free memory가 필요하다.
    - Redis를 직접 설치할 때 `/proc/sys/vm/overcommit_memory` 값을 1로 설정하지 않아 장애가 발생할 때가 있는데, `overcommit_memory`가 0이면 OS는 주어진 메모리량보다 크게 할당할 수가 없다.
    - 즉 `fork()`시에 충분한 메모리가 없다고 판단하여 에러를 발생시킨다.
    - 따라서 일단은 1로 설정해서 OS가 over해서 메모리를 할당할 수 있도록 한 후 maxmemory에 도달한 경우 policy에 따라 처리되도록 설정하는 것이 좋다.
  - used_memory_rss
    - RSS값은 데이터를 포함해서 실제로 redis가 사용하고 있는 메모리인데, 이 값은 실제로 사용하고 있는 used_memory 값보다 클 수 있다.
    - OS가 메모리를 할당할 때 page 사이즈의 배수만큼 할당하기 때문이다.
    - 이를 파편화(Fragmentations) 현상이라고 한다.



- Redis Replication
  - Redis를 구성하는 방법 중 Read 분산과 데이터 이중화를 위한 Master/Slave 구조가 있다.
    - Master 노드는 쓰기/읽기를 전부 수행하고, Slave는 읽기만 가능하다.
    - 이렇게 하려면 Slave는 Master의 데이터를 전부 가지고 있어야 한다.
    - Replication은 마스터에 있는 데이터를 복제해서 Slave로 옮기는 작업이다.
  - Master-Slave간 Replication 작업 순서
    - Slave Configuration 쪽에 `replicaof <master IP> <master PORT>` 설정을 하거나 REPLCAOF 명령어를 통해 마스터에 데이터 Sync를 요청한다.
    - Master는 백그라운드에서 RDB(현재 메모리 상태를 담은 파일) 파일 생성을 위한 프로세스를 진행하는데, 이 때 Master는 fork를 통해 메모리를 복사한다. 이후에 fork한 프로세스에서 현재 메모리 정보를 디스크에 덤프뜨는 작업을 진행한다.
    - Master가  fork할 때 자신이 쓰고 있는 메모리 만큼 추가로 필요해지므로 OOM이 발생하지 않도록 주의해야 한다.
    - 위 작업과 동시에 Master는 이후부터 들어오는 쓰기 명령들을 Buffer에 저장해 놓는다.
    - 덤프 작업이 완료되면 Master는 Slave에 해당 RDB 파일을 전달해주고, Slave는 디스크에 저장한 후에 메모리로 로드한다.
    - Buffer에 모아두었던 쓰기 명령들을 전부 slave로 보내준다.



- Redis Cluster
  - 여러 노드가 hash 기반의 slot을 나눠 가지면서 클러스터를 구성하여 사용하는 방식.
  - 전체 slot은 16384이며, hash 알고리즘은 CRC16을 사용한다.
    - Key를 CRC16으로 해시한 후에 이를 16384로 나누면 해당 key가 저장될 slot이 결정된다.
  - 클러스터를 구성하는 각 노드들은 master 노드로, 자신만의 특정 slot range를 갖는다.
    - 데이터를 이중화하기 위해 slave 노드를 가질 수 있다.
    - 만약 특정 master 노드가 죽게 되면, 해당 노드의 slave 중 하나가 master로 승격하여 역할을 수행하게 된다.
    - 하나의 master node는 여러 개의 slave node를 가질 수 있다.





# Data Persistence

- 용어 정리
  - Persistence: 영속성, 데이터를 생성한 프로그램의 실행이 종료되어도 사라지지 않는 데이터의 특성.
  - Durability: 지속성, 성공적으로 수행 된 트랜잭션은 영원히 반영되어야 함.
  - RDB: 특정 시점의 redis 데이터셋을 일정한 간격마다 .rdb 파일로 저장하는 방식
  - AOF(Append Only File): 서버에 입력된 write operation(쓰기 명령)을 파일에 추가해서 저장하는 방식.
    - 서버가 시작될 때마다 입력됐던 명령을 재실행해 dataset을 다시 만들어낸다.
  - fsync: 파일 내부 저장 상태를 장치와 동기화시키는 함수(버퍼에 있는 데이터를 파일로 옮긴다).



- RDB 장단점
  - 장점
    - Redis의 부모 process가 수행해야 할 유일한 작업은 나머지 모든 작업을 수행 할 자식을 포크하는 것 뿐이므로, Redis의 성능을 최대화 한다.
    - 부모 인스턴스는 disk I/O와 같은 작업들을 절대 수행하지 않는다.
    - 데이터 센터나 아마존 S3로 전송할 수 있는 하나의 압축된 파일이므로 재난 복구에 매우 적합하다.
    - RDB는 AOF와 비교해서 큰 데이터 셋으로 더 빠르게 재시작된다.
  - 단점
    - 스냅샷을 생성 한 후 다음 스냅샷이 생성되기 전에 레디스가 작동을 멈춘다면 해당 기간만큼의 데이터는 손실된다.
    - 포크는 데이터 셋이 큰 경우 시간이 많이 소비될 수 있고, 데이터 셋이 크고 CPU의 성능이 좋지 않은 경우 몇 밀리초 또는 1초 동안 레디스의 클라이언트 서비스를 멈추게 할 수 있다.
    - AOF도 포크를 해야 하지만 지속성의 성능 감소 없이 로그를 rewrite 하는 빈도를 수정할 수 있다.



- RDB의 동작 방식
  - SAVE의 경우
    - 메인 프로세스에서 메모리에 있는 데이터를 새 RDB temp 파일에 작성한다.
    - 작성이 완료되면 기존 RDB 파일을 지우고 새 파일로 교체한다.
  - BGSAVE의 경우
    - fork를 통해 자식 프로세스를 생성한다.
    - 자식 프로세스는 임시 RDB 파일에 데이터 세트를 저장하기 시작한다.
    - 자식 프로세스가 새로운 RDB 파일 작성이 끝나면 이전의 것과 변경한다.



- AOF의 장단점
  - 장점
    - RDB에 비해 지속성이 훨씬 뛰어나다.
    - 다양한 fsync 정책을 가질 수 있다.
    - AOF가 너무 커졌을 때 백그라운드에서 자동으로 재작성 할 수 있다(rewrite).
    - 실수로 flushall과 같은 명령어를 입력하여 데이터가 전부 삭제되어도 해당 명령을 제외하고 그 동안 입력되었던 명령들을 재시작하여 데이터를 복구할 수 있다.
  - 단점
    - AOF 파일은 일반적으로 동일한 데이터셋의 RDB 파일보다 크다.
    - 정밀한 fsync 정책에서는 RDB 보다 느릴 수 있다.
    - 과거에는 특정 operation(BRPOPLPUSH 등)에서 버그가 발생해서 AOF가 다시 로드될 때 완벽한 데이터셋을 만들어 내지 못했다.



- AOF 관련 이슈
  - 내구성
    - 디스크의 데이터에 fsync를 얼마나 수행할지를 설정할 수 있다.
    - ` appendfsync alway`: 매번 새로운 command가 AOF에 추가될 때마다 fsync를 수행한다. 매우 느리지만 매우 안전하다.
    - ` appendfsync everysec`: fsync 매 초마다 수행한다. 스냅샷 만큼 빠르며, 재난 발생시 1초의 데이터를 잃을 수 있다(권장).
    -  `appendfsync no`: 디스크에 쓰는 시점을 OS에 맡긴다(리눅스는 일반적으로 30초 간격으로 내려 쓴다).
  - AOF가 잘리는 경우
    - AOF 파일이 작성되는 동안 서버가 꺼지거나 AOF 파일 작성 시점에 저장 공간이 가득 찬 경우에 발생할 수 있다.
    - 잘못된 형식의 명령이 존재하는 경우 이를 무시하고 계속 진행하는 것이 기본값으로 설정되어 있다.
    - 그러나 설정을 변경하여 레디스를 강제 중단하도록 할 수 도 있다.
    - AOF 파일의 백업 파일을 생성하고 redis에서 제공하는 redis-check-aof 툴을 사용하면, 형식에 맞지 않는 명령을 수정할 수 있다.
  - AOF 파일이 손상되는 경우
    - 단순히 잘린 것이 아니고 손상된 경우에는 보다 까다롭다.
    - `--fix` 옵션 없이 redis-check-aof 툴을 실행 한 다음 문제점을 확인하고 파일 안에 해당하는 오프셋으로 이동해서 파일을 수동으로 복구할 수 있는지 확인하는 것이다.
    - 파일을 edis-check-aof 툴로 `--fix`을 넣어서 수정하도록 할 수 있지만 이렇게 하면 AOF의 유효하지 않은 부분에서 파일 끝까지의 부분이 제거될 수 있으므로 주의해야 한다.
  - rewrite
    - AOF는 파일의 크기가 너무 커지게 되면 자동으로 rewrite를 수행할 수 있다.
    - AOF의 목적은 모든 연산을 기록하는 것이 아닌, 현재 데이터셋을 생성할 수 있는 연산을 기록하는 것이다.
    - 예를 들어 현재 redis 내부에는 `{'some_key':1000}`이라는 하나의 데이터만이 존재하는데, 이 데이터는 `{'some_key':0}`부터 시작해서  value를 `+1`  씩 올리는 write 연산을 통해 총 1000번의 write 연산 결과 쓰여진 것이라고 가정한다.
    - 일반적으로 AOF 파일의 크기가 RDB 파일의 크기보다 큰 것은 이때문이다.
    - 이와 같이 AOF 파일의 크기가 지나치게 커질 경우 AOF 파일은 rewrtie를 1000번 진행하는 연산이 아닌 `set some_key 1000`이라는 연산을 작성하게 된다.
  - log rewrite 동작 방식
    - fork를 통해서 자식 프로세스를 생성한다.
    - 자식 프로세스는 임시 파일에 새로운 AOF를 작성한다.
    - 부모 프로세스는 인 메모리 버퍼에 새로운 변경 사항을 축적한다.
    - 자식 프로세스의 rewriting 파일 작성이 끝나면 부모 클래스는 신호를 받고 자식 프로세스가 생성한 AOF 파일 끝에 인 메모리 버퍼에 축적한 내용을 추가한다.
    - 레디스는 원자적으로 새로운 파일의 이름을 이전 파일의 이름으로 변경하고 새로운 파일에 새로운 데이터를 추가한다.



- 무엇을 사용해야 하는가?
  - 레디스를 캐시 용도로 사용할 때에는 RDB와 AOF를 사용하지 않는 것이 권장된다.
    - persistence 기능으로 인한 장애 발생 가능성이 크다.
    - fork로 인한 COW(Copy-On-Write)로 전체 성능 저하가 발생할 수 있다.
  - 두 가지 방식을 모두 사용하는 것을 권장한다.
  - Snapshotting
    - dump.rdb라 불리는 바이너리 파일에 데이터 셋을 저장한다.
    - 데이터에 N초마다 M개 이상의 변경 사항이 있는 경우저장하도록 설정하거나 SAVE, BGSAVE 명령을 수동으로 호출할 수 있다.
  - Log rewrting
    - 쓰기 작업이 수행될 수록 AOF의 크기가 커진다.
    - 클라이언트에 대한 서비스 중단 없이 백그라운드에서 AOF를 재구성할 수 있다.
    - BGREWRITEOF를 레디스에 요청할 때마다 메모리에서 현재의 dataset을 재구성하는 데 필요한 최소한의 명령 시퀀스를 작성한다.





# HA

- 레디스는 단일 인스턴스만으로도 충분히 운영이 가능하다.
  - 그러나 아래와 같은 경우 다른 운영 방식을 도입할 필요가 있다.
    - 물리 머신이 가진 메모리의 한계를 초과하는 데이터 저장
    - Failover에 대한 처리를 통해 HA(High Availability, 고가용성)을 보장
  - Master가 죽을 경우 Slave는 Sync 에러를 발생시킨다.
    - 이 상태에서는 쓰기는 불가능하고 읽기만 가능하다.
    - 따라서 Slave를 Master로 승격시켜야 한다.
  - 다음과 같은 운영 방식이 존재한다.
    - Replication
    - 센티넬(Sentienl)
    - 클러스터(Cluster)



- Replication

  - Master - Replica 형태의 복제를 제공한다.
    - Master-Slave 혹은, Leader-Follower 라고도 한다.
    - 한 개의 마스터 노드에 여러 개의 레플리카 노드가 있을 수 있고, 레플리카 노드에 또 다른 레플리카 노드가 연결되는 것도 가능하다.
    - 단, 한 개의 복제 그룹에서는 항상 한 개의 마스터 노드만 존재한다.
    - 복제가 연결되어 있는 동안 마스터 노드의 데이터는 실시간으로 레플리카 노드에 복사된다.
    - 따라서 서비스를 제공하던 마스터 노드가 다운되더라도 레플리카 노드에 어플리케이션을 재연결 해주면 서비스를 계속 할 수 있다.
    - Master는 읽기와 쓰기를 담당하며 Slave는 읽기만을 담당한다.
    - Slave에 쓰기도 가능하게 설정할 수 있지만 성능상 효율이 매우 떨어진다.

  - 복제하기

  ```bash
  $ replicaof <master의 host> <master의 port>
  ```

  - 과정
    - `replicaof` 명령어를 받은 마스터 노드는 자식 프로세스를 생성하여 백그라운드로 덤프 파일을 만든다.
    - 이를 네트워크를 통해 레플리카 노드에 보낸다.
    - 이 파일을 받은 레플리카 노드는 데이터를 메모리로 로드한다.
  - 마스터까지만 데이터가 입력된 후 마스터 노드가 죽는다면 이 데이터는 레플리카까지 전달되지 않았기에 유실이 발생할 수 있다.
    - 현재는 이 현상을 디버깅하기 힘들 정도로 데이터의 전달 속도가 매우 빠르기 때문에 유실이 자주 발생되지는 않을 것이다.



- Sentinel
  - 레디스 프로세스가 다운되면 메모리 내에 저장됐던 데이터는 유실된다.
    - 마스터 노드에 연결된 복제 노드가 있어도, 운영 중인 서비스에서 어플리케이션이 마스터에 연결된 상태였다면 다음 과정을 직접 수행해야 한다.
    - 복제 노드에 접속해서 `REPLICAOF NO ONE` 커맨드를 통해 마스터 연결 해제
    - 어플리케이션 코드에서 레디스 연결 설정을 변경(마스터 노드의 IP에서 복제 노드의 IP로)
    - 배포
  -  Sentinel은 위와 같은 과정을 자동으로 수행해준다.
    - 마스터 노드와 복제 노드를 계속 모니터링하면서 장애 상황이 발생하면 복제 노드를 마스터로 승격시키기 위해 자동 failover를 진행한다.
    - failover: 시스템 장애시 대체본으로 자동으로 변경되어서 장애를 극복하는 것
    - 담당자에게 메일을 보내도록 알림을 설정하는 것도 가능하다.
  - Sentinel 인스턴스
    - 정상적인 기능을 위해서는 적어도 3개의 Sentinel 인스턴스가 필요하다(3개 이상의 홀수 인스턴스가 필요하다).
    - 각 Sentinel 인스턴스는 레디스의 모든 노드를 감시하며 서로 연결되어 있다.
    - 과반수 이상이 동의해야만 failover를 시작할 수 있다.
    - 어플리케이션은 마스터나 복제 노드에 직접 연결하지 않고, Sentinel 노드와 연결한다.
    - Sentinel 노드는 어플리케이션에게 현재 마스터의 IP. Port를 알려주며, failover 이후에는 새로운 마스터의 IP, Port 정보를 알려준다.
  - Failover 과정
    - 마스터가 다운되고, 이를 감시하고 있던 Sentinel은 마스터에 진짜 연결할 수 없는지에 대한 투표를 시작한다.
    - 과반수 이상이 동의하면 failover를 시작한다.
    - 연결이 안되는 마스터에 대한 복제 연결을 끊고, 복제 노드 중 한 개를 마스터로 승격시킨다.
    - 만일 다른 복제 노드가 있다면 해당 노드를 새로 승격된 마스터 노드에 연결시킨다.
    - 만일 다운되었던 기존 마스터 노드가 다시 살아나면 새로운 마스터에 복제본으로 연결된다.



- Cluster

  - 위에서 살펴본 모든 방식에 샤딩 기능까지 더해진 운영 방식
    - 확장성, 고성능, 고가용성이 특징이다.
  - 구성
    - 모든 노드는 서로 연결된 Full Mesh 구조를 이루고 있다.
    - 모든 마스터와 복제 노드는 서로 연결되어 있으며, 가십 프로토콜을 이용해 통신한다.
    - 클러스터를 사용하기 위해서는 최소 세 개의 마스터 노드가 필요하다.
  - 샤딩
    - 어플리케이션으로부터 들어오는 모든 데이터는 해시 슬롯에 저장된다.
    - 레디스 클러스터는 총 16384개의 슬롯을 가지며, 마스터 노드는 슬롯을 나누어 저장한다.
    - 예를 들어 노드가 2개인 경우 노드  A는 0~16384//2까지, 노드B는 16384//2+1~ 16834까지 저장하는 방식이다.
    - 입력되는 모든 키는 CRC16 알고리즘을 사용하여 슬롯에 매핑된다.
    - 해시 슬롯은 마스터 노드 내에서 자유롭게 옮겨질 수 있으며, 이를 위한 다운타임은 필요하지 않다.

  - Client Redirection
    - 어플리케이션은 아무 노드에나 쿼리를 보낼 수 있다.
    - 단, 요청한 키가 쿼리를 보낸 노드에 존재하지 않을 수 있는데, 이 때 해당 노드는 요청한 키가 존재하는 노드 정보를 반환한다.
    - 이를 리다이렉트 메세지라 한다.

  - failover
    - Sentinel 구조와 마찬가지로 자동으로 failover가 발생한다.
    - Sentinel 구조에서는 Sentinel 프로세스가 노드들을 감시했지만, 레디스 클러스터 구조에서는 모든 노드가 서로 감시한다는 점에 차이가 있다.







# Redis 사용해보기

## 설치

- Docker로 Redis 설치하기

  - Redis 이미지 받기

  ```bash
  $ docker pull redis[:원하는 버전]
  ```

  - Docker network 생성하기
    - redis와 redis-cli 사이의 통신에 필요하다.
    - redis-cli를 사용하지 않을 경우 생성하지 않아도 된다.

  ```bash
  $ docker network create <network 이름>
  ```

  - Docker 컨테이너 생성 및 실행
    - 기본 port는 6379이다.
  
  
  ```bash
  $ docker run --network <network 이름> -p <port 번호>:<port 번호> redis
  ```
  
  - redis-cli로 redis 접속하기
    - `--rm` 옵션을 주면 컨테이너가 내려갈 시에 컨테이너도 함께 삭제되며, 컨테이너를 띄울 때에도 같은 이름의 컨테이너가 있으면 해당 컨테이너를 삭제하고 띄운다.
  
  ```bash
  $ docker run -it --network <network 이름> --rm redis-cli -h <redis 컨테이너 이름>
  ```
  
  - redis-cli를 docker로 띄우지 않고도 접속이 가능하다.
    - 아래와 같이 설치 후 사용하면 된다.
    - `-a`의 경우 `requirepass`를 설정해줬으면 해당 password를 입력하면 된다.
  
  ```bash
  # 설치
  $ sudo apt-get install redis-tools
  
  # 사용
  $ redis-cli [-h 호스트 주소] [-p 포트] [-a password]
  ```
  
  - 설정 변경하기
    - redis.cfg 파일을 생성하고 설정하고 싶은 내용을 작성한다.
    - 이후 해당 파일을  컨테이너 내부의 `/usr/local/etc/redis/redis.conf` 경로에 볼륨을 잡아준다.
  
  ```bash
  $ docker run --network <network 이름> -v <redis.cfg 파일 경로>:</usr/local/etc/redis/redis.conf> redis
  ```



- 레디스 설치 후 꼭 확인해야 할 파라미터들

  - 보안 관련 파라미터
    - `protected-mode`는 yes로 준다(기본값).
    - `requirepass`에 접속할 때 사용할 패스워드를 입력한다.

  ```yaml
  bind <서버 IP>
  protected-mode yes
  requirepass <"password">
  ```

  - persistence 관련 파라미터
    - save는 time 동안 count 만큼의 key 변경이 발생하면(time 만큼의 시간이 지났을 때) rdb 파일로 저장한다(사용하지 안을 경우 `""`로 주면 된다).
    - save는 여러 개 지정할 수 있으며 or 연산이므로 지정한 조건들 중 하나라도 일치하면 저장된다.
    - stop-writes-on-bgsave-error가 yes인 경우 RDB 파일을 작성하다 실패하면 이후 모든 쓰기 요청을 막는다(SAVE 명령에만 적용되며 BGSAVE에는 적용되지 않는다).
    - appendonly: AOF 기능을 사용할지 여부를 설정한다.
    - appendfsync: AOF 파일에 기록하는 시점을 설정한다.
  - auto-aof-rewrite-percentage: AOF 파일 사이즈가 숫자값 % 이상으로 커지면 rewrite한다(%의 기준은 레디스 서버가 시작할 시점의 AOF 파일 사이즈이다).
  
  ```txt
  # RDB
  save [time], [count]
  stop-writes-on-bgsave-error <yes/no>
  
  # AOF
  appendonly <yes/no>
  appendfsync [always/everysec/no]
  auto-aof-rewrite-percentage [0-100]
  ```
  
  - replica 관련 파라미터들
  
  ```bash
  replicaof <마스터 IP> <마스터 port>
  masterauth <"마스터의 requirepass"
  ```
    - back/foreground 실행 설정
        - no로 설정할 경우(default) foregrund로 실행된다.
  
  ```bash
  daemonize [yes/no]
  ```
  
    - 메모리 관련 설정
      - 64bit 환경에서는 maxmemory의 default 값은 0이며, swap 메모리를 사용할 때까지 계속해서 커지게 된다.
      - 32bit 환경에서는 3GB가 기본 값이다.
  
  ```bash
  maxmemory <가용 메모리의 60~70%>
  maxmemory-policy <policy>
  ```





## Cluster로 설치하기

- Clustering 관련 설정은 아래와 같다.

  - `cluster-enabled`
    - Cluster mode로 실행할지 여부를 설정한다.
    - `yes`로 줄 경우 cluster mode로 실행된다.
  - `cluster-config-file`
    - 클러스터의 상태를 기록하는 파일의 위치를 설정한다.
    - 클러스터의 상태가 변경될 때 마다 설정된 경로의 파일에 변경 사항이 기록된다.
    - `redis` docker image 기준으로 `/data`를 기준으로 경로가 설정된다.
  - `cluster-node-timeout`
    - Cluster를 구성 중인 node가 down되었다고 판단하는 시간이다.
    - 단위는 millisecond이다.

  ```toml
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  ```

  - Port
    - 기본 포트에 10000을 더한 포트를 클러스터 버스 포트로 사용한다.
    - 따라서 기본 포트와 기본 포트에 10000을 더한 포트 모두 사용 가능해야 한다.



- 각 redis node 별로 설정 파일을 준비한다.

  - `redis1.conf`

  ```toml
  port 7001
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  ```

  - `redis2.conf`

  ```toml
  port 7002
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  ```

  - `redis3.conf`

  ```toml
  port 7003
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  ```



- Docker compose로 실행하기

  - 아래와 같이 docker compose file을 작성한다.

  ```yaml
  services:
    redis1:
      image: redis:6.2.6
      container_name: redis1
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis1.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7001:7001
        - 17001:17001
    
    redis2:
      image: redis:6.2.6
      container_name: redis2
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis2.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7002:7002
        - 17002:17002
    
    redis3:
      image: redis:6.2.6
      container_name: redis3
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis3.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7003:7003
        - 17003:17003
  ```

  - 실행하기

  ```bash
  $ docker compose up
  ```



- 클러스터 설정하기

  - Docker container 내부에 attach한다.

  ```bash
  $ docker exec -it redis1 /bin/bash
  ```

  - redis-cli를 사용하여 cluster를 구성한다.

  ```bash
  $ redis-cli --cluster create <host>:7001 <host>:7002 <host>:7003
  ```

  - 정상적으로 구성 됐는지 확인한다.

  ```bash
  $ redis-cli -p 7001
  cluster nodes
  cluster info
  ```



- Slave 추가하기

  - 위 구조에서는 slave를 설정하지 않았기 때문에, 고가용성이 보장되지 않는다.
    - 고가용성이 보장되도록 하기 위해서는 아래와 같이 slave node를 함께 띄워야 한다.

  - Slave node들을 위한 설정 파일을 작성한다.

  ```toml
  # redis-slave1.conf
  port 7101
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  
  # redis-slave2.conf
  port 7102
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  
  # redis-slave3.conf
  port 7103
  cluster-enabled yes
  cluster-config-file nodes.conf
  cluster-node-timeout 3000
  appendonly yes
  ```

  - Docker compose file에 slave 노드을 추가한다.

  ```yaml
  services:
    redis1:
      image: redis:6.2.6
      container_name: redis1
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis1.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7001:7001
        - 17001:17001
    
    redis2:
      image: redis:6.2.6
      container_name: redis2
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis2.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7002:7002
        - 17002:17002
    
    redis3:
      image: redis:6.2.6
      container_name: redis3
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis3.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7003:7003
        - 17003:17003
    
    redis-slave1:
      image: redis:6.2.6
      container_name: redis-slave1
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave1.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7101:7101
        - 17101:17101
      
    redis-slave2:
      image: redis:6.2.6
      container_name: redis-slave2
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave2.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7102:7102
        - 17102:17102
      
    redis-slave3:
      image: redis:6.2.6
      container_name: redis-slave3
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave3.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      ports:
        - 7103:7103
        - 17103:17103
  ```

  - Cluster를 설정한다.

  ```bash
  $ docker exec -it redis1 /bin/bash
  $ redis-cli --cluster create <host>:7001 <host>:7002 <host>:7003
  $ redis-cli -p 7001
  cluster info
  cluster nodes
  ```

  - Slave를 추가한다.

  ```bash
  $ redis-cli --cluster add-node <host>:7101 <host>:7001 --cluster-slave
  $ redis-cli --cluster add-node <host>:7102 <host>:7002 --cluster-slave
  $ redis-cli --cluster add-node <host>:7103 <host>:7003 --cluster-slave
  ```

  - 정상적으로 추가 됐는지 확인한다.

  ```bash
  $ redis-cli -p 7001
  cluster info
  cluster nodes
  ```



- 고가용성 확인하기

  - Redis CLI에 접속한다.
    - `-c` 옵션은 cluster mode로 접속하는 option으로 다른 node에도 접근할 수 있게 해준다.

  ```bash
  $ redis-cli -p 7001 -c
  ```

  - Key와 value를 설정한다.
    - 세 개의 master node에 모두 분배되도록 한다.

  ```bash
  set foo bar
  set bar baz
  set baz qux
  ```

  - 세 개의 master node에 분배된 상태에서 아래와 같이 하나의 master node를 정지한다.
    - `redis1` node에는 baz:qux가 저장되어 있었다.

  ```bash
  $ docker stop redis1
  ```

  - 다른 container에 attach한다.

  ```bash
  $ docker exec -it redis2 /bin/bash
  ```

  - Redis CLI에 접속하여 cluster 상태를 확인한다.
    - 기존에 `redis1` node의 slave였던 `redis-slave1` node가 master가 된 것을 확인할 수 있다.

  ```bash
  $ redis-cli -p 7002 -c
  cluster nodes
  ```

  - 기존에 `redis1` node에 저장되어 있던 baz key로 조회가 가능한지 확인한다.
    - `redis-slave1` node에서 값을 redirect 해주는 것을 확인할 수 있다.

  ```bash
  get baz
  Redirected to slot [4813] located at <docker_network_host>:7101
  ```



- 주의사항

  - 주의할 점은 예전 버전에서는 cluster 생성시에 hostname이 아닌 IP를 입력해야 한다는 것이다.
    - 6.2.6 버전에서는 hostname이 사용 불가능한 것을 확인
    - 7.2.0 버전에서는 hostname이 사용 가능한 것을 확인

  - 예를 들어 아래와 같이 같은 docker network를 사용한도록 구성했을 때
    - 모든 노드가 기본 포트(6379)를 사용하도록 설정한다.

  ```yaml
  services:
    redis1:
      image: redis:6.2.6
      container_name: redis1
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis1.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
    
    redis2:
      image: redis:6.2.6
      container_name: redis2
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis2.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
    
    redis3:
      image: redis:6.2.6
      container_name: redis3
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis3.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
    
    redis-slave1:
      image: redis:6.2.6
      container_name: redis-slave1
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave1.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
  
    redis-slave2:
      image: redis:6.2.6
      container_name: redis-slave2
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave2.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
    
    redis-slave3:
      image: redis:6.2.6
      container_name: redis-slave3
      environment:
        - TZ=Asia/Seoul
      volumes:
        - ./config/redis-slave3.conf:/etc/redis.conf
      command: redis-server /etc/redis.conf
      restart: always
      networks:
        - redis-test
  
  networks:
    redis-test:
      driver: bridge
  ```

  - 아래와 같이 hostname을 사용하더라도 clustering은 불가능하다.

  ```bash
  $ redis-cli --cluster create redis1:6379 redis2:6379 redis3:6379
  ```







## CLI

- redis-cli 실행

  - 아래 명령어로 redis-cli를 실행시킨다.
    - 기본 port는 6379이다.
  

  ```bash
  $ redis-cli [-h 호스트 주소] [-p 포트] [-n db 번호] [-s 소켓] [-a 비밀번호] [-u 서버 url]
  ```
  
  - 비밀번호 입력
    - redis-cli를 실행할 때 `-a`를 입력하지 않았으면 아래 명령어를 통해 인증이 가능하다.
  
  ```bash
  > auth <password>
  ```




- Redis 정보 확인

  ```bash
  > info
  ```

  - config 정보 확인

  ```bash
  > config get <확인할 정보>
  ```

  - grep 사용하기
    - redis-cli 내부가 아닌 외부에서 아래 명령어 실행

  ```bash
  $ redis-cli [-h 호스트 주소] [-p 포트] [-n db 번호] [-s 소켓] [-a 비밀번호] [-u 서버 url] | grep <찾을 내용>
  ```

  - 도움말

  ```bash
  > help
  ```

  - 모니터링

  ```bash
  > monitor
  ```



- 데이터 삽입
  - 옵션으로ttl(초)을 줄 수 있다.

  ```bash
  > set <key> <value> [ex seconds]
  ```

  - 데이터 여러 개 삽입

  ```bash
  > mset <key1> <value1> <key2> <value2> ...
  ```

  - list 자료형의 맨 앞 부터 삽입 삽입
    - 문자열이라도 `"`는 붙이지 않아도 된다.
    - space 로 구분한다.

  ```bash
  > lpush my_list Hello
  > lpush my_list World
  > lpush my_list Hello World
  > lpush my_list HelloWorld
  ```

  - list 자료형의 맨 뒤 부터 삽입
    - `rpush` 사용
    - 나머지는 `lpush`와 동일

  - 소멸 시간 지정해서 삽입
    - 단위는 초

  ```bash
  > setex <key> <시간> <value>
  ```




- 데이터 조회
  - 찾으려는 키가 없는 경우 `(nil)`을 반환한다.

  ```bash
  > get <key>
  ```

  - 데이터 여러 개 조회

  ```bash
  > mget <key1> <key2> ...
  ```

  - 리스트 데이터 앞에서부터 조회
    - 뒤의 숫자는 몇 번째 부터 몇 번째 까지를 조회할지를 선택하는 것이다.

  ```bash
  lrange my_list 0 -1
  
  # 출력, 마지막에 넣은 것이 가장 먼저 나온다.
  1) "HelloWorld"
  2) "World"
  3) "Hello"
  4) "World"
  5) "Hello"
  ```
  
  - 모든 key 확인
    - redis는 single thread이다.
    - 이 명령을 처리하기 위해 뒤의 작업들은 멈춰버리므로 가급적 사용을 자제하는 것이 좋다.
    - scan을 사용하는 것이 좋다.
  
  ```bash
  > keys *
  ```
  
  - scan
    - cursor 기반으로 key들을 출력한다.
    - 첫 번째 응답(`1)`)으로 다음번 cursor가 오는데 다시 이 것을 cursor애 넣고 명령어를 입력하는 것을 반복하다 0이 나오면 모든 key를 조회했다는 뜻이 된다.
    - 첫 scan에서 아무것도 안 나온다고 결과가 없는 것이 아닐 수도 있다.
  
  ```bash
  > scan <cursor> [Match pattern] [Count]
  
  # 예시
  > scan 0
  
  #응답
  1) "88"
  2)  1) "key62"
      2) "key71"
      3) "key85"
      4) "key19"
      5) "key92"
      6) "key84"
      7) "key20"
      8) "key40"
      9) "key34"
     10) "key21"
     11) "key2"
  ```
  




- 데이터 삭제
  - `(integer) 1`은 삭제 성공, `(integer) 0`은 삭제하려는 데이터가 없을 경우 반환된다.

  ```bash
  > del <key>
  ```

  - 모든 데이터 삭제

  ```bash
  > flushall
  ```

  - 리스트형 데이터에서 맨 뒤의 데이터 삭제
    - 맨 앞의 데이터 삭제는 `lpop`

  ```bash
  > rpop my_list
  ```

  - 리스트형 데이터에서 맨 뒤의 데이터 삭제 후, 삭제한 값을 다른 list에 삽입(deprecated)

  ```bash
  > rpop my_list other_list
  ```

  - 리스트형 데이터에서 head나 tail을 삭제하고 이를 다른 list의 head나 tail에 삽입

  ```bash
  # my_list의 tail(right)을 빼서 other_list의 head(left)에 삽입
  > lmove my_list other_list rigth left
  ```

  - 리스트형 데이터에서 일정 범위 제외하고 삭제
    - 삭제할 범위가 아닌 삭제하지 않을 범위를 지정한다.

  ```bash
  > ltrim my_list <시작> <끝>
  ```




- key 이름 변경
  - rename의 경우 변경하려는 이름의 key가 이미 존재할 경우 덮어 쓴다.
  - renamenx의 경우 변경하려는 이름의 key가 있을 경우 `(integer) 0`을 반환한다.

  ```bash
  > rename <key>
  
  > renamenx <key>
  ```

  - 리스트형 데이터 변경

  ```bash
  # my_list의 value인 리스트에서, 첫 번째 인자를 Bye로 변경
  LSET my_list 0 "Bye"
  ```




- 기타

  - 타임 아웃까지 남은 시간 확인
    - `(integer) -1`은 기한이 없는 경우, `(integer) -2`는 키 값이 없거나 소멸된 경우 반환된다.

  ```bash
  # 초 단위로 반환
  > ttl <key>
  
  # 밀리 초 단위로 반환
  > pttl <key>
  ```

  - 리스트 길이 확인

  ```bash
  > llen my_list
  ```

  - ttl(time to live) 제거하기
    - 특정 키를 삭제하지 않고 redis에 계속 저장하고 싶을 때 사용한다.

  ```python
  > persist <key>
  ```

  - ttl(time to live) 설정하기
    - 기본적으로 expire 명령을 통해 타임아웃을 설정해주지 않으면 -1(무기한)로 설정된다.

  ```bash
  > expire <key> <seconds>
  ```





## Python

- Python에서 사용하기

  - Redis 패키지 설치

  ```bash
  $ pip install redis
  ```

  - 테스트
    - 호스트와 포트를 지정해주고 `ping()` 메서드를 통해 테스트 해본다.
    - 그 밖에도 password, decode_response 등의 옵션을 줄 수 있다.
    - `Redis`, 혹은 `RedisStrict`를 사용할 수 있는데 둘 사이의 차이는 없다.
    - `RedisStrict`가 구버전에서 사용하던 것이다.
  
  ```python
  import redis
  
  
  r = redis.Redis(host="localhost",port=6379)
  # 비밀번호를 서정한 경우
  r = redis.Redis(host="localhost",port=6379,password=1234)
  print(r.ping())	# True
  ```
  
  - 데이터 삽입
    - list, set, dictionary 등은 삽입이 불가능하다.
    - json 패키지를 통해 dumps, loads를 사용하면 삽입, 조회가 가능하다.
  
  ```bash
  import redis
  
  
  r = redis.Redis(host="localhost", port=6379)
  r.set("key", "value")
  
  my_dict = {"a":1,"B":2}
  r.set("my_dict", jsonDataDict)
  result_data = r.get("my_dict").decode('utf-8')
  result = dict(json.loads(result_data))
  ```
  
  - 데이터 여러 개 삽입
  
  ```python
  import redis
  
  
  r = redis.Redis(host="localhost", port=6379)
  r.mset({"key":"value","key2":"value2"})
  ```
  
  - 데이터 조회
  
  ```bash
  import redis
  
  
  r = redis.Redis(host="localhost", port=6379)
  print(r.get("key")) 	# b'value'
  print(r.get("key").decode("utf-8"))		# value
  ```
  
  - scan을 통한 데이터 조회
  
  ```python
  import redis
  
  
  r = redis.StrictRedis('localhost', port=6379)
  init = 0 # cursor 값 0으로 스캔 시작
  
  while(True):
      ret = r.scan(init)
      print(init)
      init = ret[0]
      print(ret[1])
      if (init == 0): # 반환된 cursor 값이 0이면 스캔 종료
          break
  ```
  
  - 데이터 삭제
  
  ```bash
  import redis
  
  
  r = redis.Redis(host="localhost",port=6379)
  r.delete("key")
  ```
  
  - 데이터 전체 삭제
  
  ```python
  import redis
  
  
  r = redis.Redis(host="localhost",port=6379)
  r.flushdb()
  ```







# Redis 사용 전략

- Look Aside(==Lazy Loading)
  - 필요할 때만 데이터를 캐시에 로드하는 캐싱 전략
  - 캐시는 DB와 어플리케이션 사이에 위치한다.
    - 어플리케이션에서 data를 가져올 때 redis를 먼저 찔러보고, redis에 data가 있으면 data를 반환한다.
    - 없을 경우 어플리케이션은 DB에 data를 요청하고, 어플리케이션이 이 데이터를 받아 레디스에 저장한다.
  - 장점
    - 실제로 사용되는 데이터만 캐시할 수 있다.
    - 레디스의 장애가 어플리케이션에 치명적인 영향을 주지 않는다.
  - 단점
    - 캐시(redis)에 없는 데이터를 쿼리할 때 오랜 시간이 걸린다.
    - 캐시가 최신 데이터를 가지고 있다는 것을 보장하지 못한다(redis에 해당 key 값이 없을 때만 캐시에 대한 업데이트가 일어나기 때문).



- Write-Through
  - DB에서 데이터를 작성할 때마다 캐시에 데이터를 추가하거나 업데이트한다.
  - 장점
    - 캐시의 데이터는 항상 최신 상태로 유지된다.
  - 단점
    - 데이터 입력 시 두 번의 과정을 거쳐야 하기 때문에 지연 시간이 증가한다.





# 참조

- redis 공식 문서

> https://redis.io/commands

- Redis 기본 정리

> https://brunch.co.kr/@jehovah/20

- redis-cli에서 redis 사용

> https://freeblogger.tistory.com/10

- python에서 redis 사용

> https://soyoung-new-challenge.tistory.com/117

- Redis의 SCAN은 어떻게 동작하는가

> https://tech.kakao.com/2016/03/11/redis-scan/

- 개발자를 위한 레디스 튜토리얼

> https://meetup.toast.com/posts/226

- [Redis\] redis.conf 의 파라미터 의미 파악하기

> https://mozi.tistory.com/368?category=1102290
