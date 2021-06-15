# Redis

- 캐시

  - 한 번 읽어온 데이터를 임의의 공간에 저장하여 다음에 읽을 때는 빠르게 결과값을 받을 수 있도록 도와주는 공간

  - cache 사용 구조
    - cache Hit: DB에 데이터를 요청하기 전에 Cache에 데이터가 있는지 확인하고 있으면, 데이터를 DB에 요청하지 않고 캐시에서 가져오는 것.
    - cache Miss: cache 서버에 데이터가 없어 DB에 해당 데이터를 요청하는 것, DB에서 요청 받을 데이터를 다음 번에는 캐시에서 사용하기 위해 캐시에 저장한다.
  - 캐시를 사용하는 경우
    - 영구적으로 저장해야 하는 데이터가 아닐 경우에 DB가 아닌 캐시에 저장하면 보다 빠르게 데이터에 접근 할 수 있고, DB의 부하도 감소시킬 수 있다.
    - 동시다발적인 쓰기가 발생하는 경우, 갑자기 쓰기 요청이 몰려들 경우 DB에 과부하가 걸릴 수 있다. 따라서, 캐시에 일시적으로 저장 한 후 캐시에 저장된 데이터를 DB에 순차적으로 삽입하는 방식을 사용하면, 이러한 부하를 감소시킬 수 있다.
  - 한계
    - 캐시 서버는 속도를 위해 주로 메모리를 사용한다.
    - 따라서 서버에 장애가 나면 메모리가 날아가서 데이터가 손실될 수 있다.



- Redis
  - 키-값 기반의 인-메모리 데이터 저장소.
    - 인-메모리란 컴퓨터의 메인 메모리(RAM)에 DB 데이터와 같은 주요 데이터를 저장하는 것을 말한다.
  - 특징
    - 키-값 기반이기 때문에 키만 알고 있다면 바로 값에 접근할 수 있다.
    - 또한 디스크에 데이터를 쓰는 구조가 아니라 메모리에서 데이터를 처리하기 때문에 속도가 상당히 빠르다.
    - Single threaded로 한 번에 단 하나의 명령어만 실행할 수 있다.
    - 다양한 데이터 구조를 제공하여, 캐시 데이터 저장 외에도 인증 토큰 저장, Ranking Board 등으로도 주로 사용된다.
  - Redis가 제공하는 데이터 구조
    - Strings: 단순한 키-값 매핑 구조.
    - Lists: 배열 형식의 데이터 구조, 처음과 끝에 데이터를 넣고 빼는 것은 속도가 빠르지만, 중간에 데이터를 삽입할 때는 어려움이 있다.
    - Sets: 순서가 없는 Strings 데이터 집합, 중복된 데이터는 하나로 처리하기 때문에, 중복에 대한 걱정을 하지 않아도 된다.
    - Sorted Sets: Sets과 같은 구조지만, Score를 통해 정렬이 가능하다.
    - Hashes: 키-값 구조를 여러개 가진 object 타입을 저장하기 좋은 구조이다.



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
    - allkeys-lfu: 가장 적게 액세서한 키를 제거하여 공간을 확보한다.
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
    - Buffer에 모아두었던 쓰기 명령들을 전부  slave로 보내준다.



- Master가 죽는 경우
  - Master가 죽을 경우 Slave는 Sync 에러를 발생시킨다.
    - 이 상태에서는 쓰기는 불가능하고 읽기만 가능하다.
    - 따라서 Slave를 Master로 승격시켜야 한다.



- Redis Cluster
  - 여러 노드가 hash 기반의 slot을 나눠 가지면서 클러스터를 구성하여 사용하는 방식.
  - 전체 slot은 16384이며, hash 알고리즘은 CRC16을 사용한다.
    - Key를 CRC16으로 해시한 후에 이를 16384로 나누면 해당 key가 저장될 slot이 결정된다.
  - 클러스터를 구성하는 각 노드들은 master 노드로, 자신만의 특정 slot range를 갖는다.
    - 데이터를 이중화하기 위해 slave 노드를 가질 수 있다.
    - 만약 특정 master 노드가 죽게 되면, 해당 노드의 slave 중 하나가 master로 승격하여 역할을 수행하게 된다.





# 참조

- Redis 기본 정리

> https://brunch.co.kr/@jehovah/20

