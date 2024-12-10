# MinIO 개요

> https://github.com/minio/minio
>
> https://min.io/docs/minio/linux/index.html

- 개요
  - Open source로 개발된 distributed object stroage이다.
    - Go로 개발되어 속도가 빠르고, 빠른 배포가 가능하다.
  - AWS S3와 API가 호환된다.



- Docker로 MinIO 설치하기

  - MinIO image pull 받기

  ```bash
  $ docker pull minio/minio
  ```

  - Container 실행을 위한 compose file 작성하기

  ```yaml
  version: '3.2'
  
  
  services:
    minio:
      image: minio/minio:latest
      container_name: minio
      command: ["server", "/data", "--console-address", ":9001"]
      environment:
        - MINIO_ROOT_USER=foo
        - MINIO_ROOT_PASSWORD=changme1234
      volumes:
        - ./data:/data
      ports:
        - 9000:9000
        - 9001:9001
  ```

  - Container 실행하기

  ```bash
  $ docker compose up
  ```



- 각 문서들은 etag를 가진다.
  - MinIO의 etag는 내용이 같으면 같은 값으로 생성된다.
  - file명이 달라도 file의 내용이 같으면 같은 값으로 생성된다.



## Core Operational Concepts

- MinIO는 크게 세 가지 방식의 배포 방식이 있다.
  - Single Node Single Driver
    - 하나의 MinIO서버와 하나의 driver 혹은 folder로 구성된 형태.
    - 예를 들어 local PC에서 computer의 hard driver에 있는 folder를 사용하는 경우가 이에 해당한다.
  - Single Node Multi Drive
    - 하나의 MinIO 서버와 여러 개의 driver 혹은 folder로 구성된 형태.
    - 예를 들어 하나의 MinIO container에서 여러 개의 volume을 사용하는 경우가 이에 해당한다.
  - Multi Node Nulti Drive
    - 여러 개의 MinIO server와 여러 개의 driver 혹은 folder로 구성된 형태.



- 분산된 MinIO가 동작하는 방식
  - 대부분의 운영 환경에서 MinIO는 고가용성을 위해 여러 개의 server에 배포된다.
    - MinIO는 고가용성과 내결함성을 위해 하나의 server pool에 최소한 4개의 MinIO node로 cluster를 구성하는 것을 권장한다.
  - MinIO가 여러 개의 server를 관리하는 방식.
    - Server pool은 `minio server` node들의 집합이다.
    - MinIO는 이미 존재하는 MinIO deployments에 새로운 server를 추가하는 기능을 제공한다.
    - 만약 하나의 server pool이 down될 경우, MinIO는 정상화될 때 까지 모든 pool에 대한 I/O 작업을 정지한다.
  - MinIO가 여러개의 server pool들을 하나의 MinIO cluster로 연결하는 방식.
    - Cluster는 하나 이상의 server pool들로 구성된 전체 MinIO deployment를 의미한다.
    - Cluster에 속한 각각의 server pool들은 하나 이상의 erasure set을 가지고 있으며 erasure set의 개수는 pool 내의 driver와 node의 개수로 결정된다.
  - MinIO가 분산된 object들을 관리하는 방식
    - 새로운 object를 생성할 때 가장 가용 공간이 많은 server pool에 object를 생성하는 방식으로 storage를 최적화한다.
    - MinIO는 비용상의 문제로 오래된 pool에서 새로운 pool로 object들을 rebalancing하는 작업을 실행하지는 않는다.
    - 대신 새로운 object는 일반적으로 충분한 용량을 가진 새로운 pool에 저장된다.



- MinIO가 availability, redundancy, reliability를 제공하는 방식.
  - MinIO는 data redundancy와 reilability를 위해 Erasure Coding을 사용한다.
    - Erasure Coding은 MinIO를 여러 drive에 걸쳐서 배포하여 drive 혹은 node가 손실되더라도 바로 object들을 자동으로 재구성 할 수 있게 해주는 기능이다.
    - Erasure Coding은 RAID나 replication보다 훨씬 적은 overhead로 object 수준의 복구를 제공한다.
  - MinIO는 고가용성과 resiliency를 위해 data를 여러 Erasure Set들로 분산한다.
    - Erasure Set은 Erasure Coding을 지원하는 여러 drive들의 집합이다.
    - MinIO는 object를 shard라 불리는 덩어리로 나눈 후 이들을 Erasure Set 내의 여러 drive로 분산시켜 저장한다.
    - 가장 높은 수준의 redundancy 설정을 할 경우 MinIO를 구성하는 전체 drive들 중 절반이 동작하지 않아도, MinIO는 읽기 요청을 처리할 수 있다.
    - Server Pool 내의 Erasure Set의 크기와 개수는 set 내의 전체 dive의 개수와 minio server의 개수를 기반으로 계산된다.
  - 미사용 data를 보호하기 위한 Bit Rot Healing이 구현되어 있다.
    - Bit rot은 모든 storage device에서 발생할 수 있는 data의 손상을 의미한다.
    - Bit rot이 사용자의 부주의로 인해 발생하는 경우는 흔치 않으며, OS도 이를 탐지해 사용자에게 알려줄 수 있는 방법이 없다.
    - 일반적으로 driver의 노후화, drive firmware의 bug, driver error, 잘못된 방향으로 읽고 쓰는 등으로 인해 발생한다.
    - MinIO는 object의 무결성을 확인하기 위해 hashing algorithm을 사용한다.
    - 만약 object가 bit rot에 의해 손상되었다면, MinIO는 system topology와 availability에 따라 object를 복구할 수 있다.
  - MinIO는 Parity를 사용하여 object 수준의 data protection을 기록한다.
    - 여러 drive를 가진 MinIO는 가용한 drive들을 data drive와 parity drive로 나눈다.
    - MinIO는 object를 작성할 때 object의 내용에 관한 추가적인 hashing 정보를 parity drive에 저장한다.
    - Parity drive에 저장된 이 정보를 가지고 object의 무결성을 확인하고, object가 손실 혹은 손상될 경우 object를 복구하는 데 사용한다.
    - MinIO는 Erasure Set에서 가용한 parity device의 개수만큼의 drive가 손실되어도 object에 대한 모든 종류의 접근을 처리할 수 있다.



- 분산 구조
  - 운영 환경에서 MinIO는 최소 4개의 MinIO host로 구성하는 것이 바람직하다.
  - MinIO는 분산된 MinIO resource들을 하나의 pool로 통합하고, 이를 하나의 object storage service로 제공한다.
    - 각각의 pool은 각자의 Erasure Set을 가지고 있는 여러 개의 독립적인 node들의 그룹으로 구성된다.
  - MinIO는 NVMe나 SSD 같이 host maachine의 PCI-E controller board에 부착된 drive들을 사용할 때 최고의 성능을 보여준다.
    - MinIO는 drive나 controller 계층에서 caching을 권장하지 않는데, 이는 caching이 채워지고 비워질 때 I/O spike를 유발하여 예측할 수 없는 성능을 보일 수 있기 때문이다.
  - MinIO는 pool 내의 drive들을 Erasure Set으로 자동으로 묶어준다.
    - MinIO의 Erasure Set을 pool내의 node들 간에 대칭적으로 stripe하여 Erasure Set drive가 고르게 분배될 수 있게 한다.
    - Striping이란 데이터를 병렬로 분리하여 저장하는 방식을 의미한다.
  - 각 MinIO server 내에는 여러 개의 node들이 있을 수 있으며, client는 이 node들 중 어느 곳에나 연결하여 직접 작업을 수행할 수 있다.
    - 요청을 받은 node는 다른 MinIO server 내의 다른 node들에도 요청을 보내고 다른 node들로부터 응답을 받아 이를 취합하여 최종 응답을 반환한다.
    - Node를 추가, 삭제, 변경할 때 마다 client에도 이 정보를 update하는 것은 까다로운 일이므로, 일반적으로 앞단에 load balancer를 두고 load balancer에 이 정보를 update하는 방식을 사용한다.



- Erasure Coding
  - Erasure Coding(EC)이란
    - Storage에 data를 저장할 때 내결함성을 보장하고, 저장 공간의 효율성을 높이기 위해 설계된 데이터 복제 방식이다.
    - Data를 알고리즘에 따라 n개로 나눈 후에 나뉘어진 데이터들을 Erasure code codec을 사용하여 encoding하여 m개의 parity를 만든다.
    - 이후 data나 parity가 유실될 경우 남은 data와 parity들을 decoding하여 원래의 data를 복구한다.
    - 주의할 점은 drive를 data drive와 parity drive로 나누는 것이 아니고, object를 data shard와 parity shard로 나누어 각 drive에 무선적으로 저장한다는 점이다.
    - 즉 하나의 drive에 어떤 object의 data shard가 저장되어 있으면서 다른 object의 parity shard가 저장되어 있는 것도 가능하다.
  - 기존에 고가용성을 보장하던 방식과의 차이
    - 기존에는 보관할 data를 그대로 복제하는 방식을 사용했다.
    - 이 방식의 경우 data를 몇 벌씩 더 만드는 방식이기 때문에 보다 많은 저장 공간을 필요로 한다는 단점이 있다.
    - Erasure coding의 경우 기존 방식보다 적은 저장 공간으로 고가용성을 보장할 수 있게 해준다.
  - Object를 쓸 때 동작 방식
    - N개의 drive가 있을 때, object를 K개의 data fragment로 분할하고 이들을 encoding하여 M개의 parity fragment를 만든다.
    - 이때 $$N = K + M$$이다.
    - 새로운 object가 저장될 때, object는 K개의 fragment들로 분할되어, K개의 drive에 저장된다.
    - 만약 이 때 object의 내용의 길이가 K로 나누어 떨어지지 않는다면 padding을 하여 길이를 맞춘다.
    - 또한 이 때, object를 복원할 때 사용하기 위해 M개의 추가적인 fragment도 생성하여 data fragment가 저장되지 않은 drive에 저장한다.
    - Parity shard에 저장되는 fragment들은 object를 encoding하여 생성한다.
    - Encoding 방식에는 여러 가지가 있는데 가장 널리 사용되는 것은 Reed-Solomon coding이다.
  - Object를 읽을 때 동작 방식
    - 일부 shard에 문제가 생기더라도 parity shard를 통해 object의 복원이 가능하다.
    - 어떤 shard에도 문제가 없을 경우, 각 data shard들이 저장하고 있는 object fragment들을 모아서 object를 반환한다.
    - M개 이하의 shard에 문제가 있을 경우, 만약 문제가 생긴 M개의 shard에 parity shard가 포함되어 있다면 정상 상태인 parity shard를 사용하여 object를 복원한 후 반환한다. 만약 문제가 생긴 M개의 shard가 모두 parity shard라면, data shard에서 object fragment들을 모아서 object를 반환한다.
    - 따라서 Erasure coding은 M개 이하의 shard에서 문제가 생겼을 때만 고가용성을 보장한다.
  
  - 하나의 object에 대해서 하나의 drive는 하나 이상의 segment를 가질 수 없다.



- MinIO의 Erasure Coding

  - MinIO에서도 data redundancy와 가용성을 위해 Erasure Coding을 사용한다.
    - MinIO는 각 server pool의 drive들을 하나 이상의 같은 크기를 가진 Erasure Set으로 그룹화한다.
    - Erasure Set의 크기와 개수는 server pool을 처음으로 구성할 때 결정되며, server pool이 구성된 이후에는 변경할 수 없다.
    - 그러나 parity 개수는 변경이 가능하다.
  - 각 쓰기 작업마다 MinIO는 object를 data와 parity shard로 분할한다.
    - Parity의 개수는 0부터 Erasure Set size의 절반까지로 설정이 가능하다.
    - 예를 들어 Erasure Set의 size가 12라면, parity는 0부터 6 사이의 값으로 설정이 가능하다.
    - Erasure Set의 size(N)는 data shard의 개수(K) + parity shard의 개수(M)이다(결국 전체 drive의 개수).
  
  - Parity 개수는 변경이 가능하다.
    - 그러나 변경하더라도 변경 이전의 object들은 변경 이전의 설정이 적용된다.
  
  - MinIO는 object를 읽거나 쓸 때 정족수를 기반으로 한다.
    - 읽기를 위해서는 `ERASURE_SET_SIZE - EC:N`만큼의 정족수가 필요하다.
    - 쓰기를 위해서도 `ERASURES_SET_SIZE - EC:N`만큼의 정족수가 필요하다.
    - 단, 만약 `EC:N`의 값이 최댓값인 ERASURE_SET_SIZE의 절반이라면, 이 때는 `(ERASURES_SET_SIZE - EC:N) + 1`만큼의 정족수가 필요하다.
    - 결국 `EC:N`의 값이 커질수록 더 많은 drive 혹은 node가 내려가더라도 지속적인 서비스가 가능해진다.
  - `EC:N`의 값이 ERASURE_SET_SIZE의 절반일 때 쓰기 작업을 위해  `(ERASURES_SET_SIZE-EC:N) + 1` 만큼의 shard가 필요한 이유는 split-brain 문제를 예방하기 위함이다.
    - 만일 network 문제로 인해 4개의 node가 2개씩 나뉘게 되었을 때, `(ERASURES_SET_SIZE-EC:N)`만으로 쓰기 quorum을 충족하게 되면 2개씩 나뉜 두 그룹에 각각 쓰기 작업이 가능해진다. 
    - 이럴 경우 두 그룹 간에 data 불일치가 발생할 수 있다. 
    - 따라서 이 경우 쓰기 quorum은 `(ERASURES_SET_SIZE-EC:N)`에 1을 더해준 값으로 설정된다.



- Parity 개수 변경하기

  - MinIO는 erasure set size(erasure set 내의 전체 drive 개수)에 따라 parity의 개수를 아래와 같이 자동으로 설정한다.

  | Erasure Set Size | Default Parity (EC:N) |
  | ---------------- | --------------------- |
  | 1                | EC:0                  |
  | 2 ~ 3            | EC:1                  |
  | 4 ~ 5            | EC:2                  |
  | 6 ~ 7            | EC:3                  |
  | 8 ~ 16           | EC:4                  |

  - 이 기본 값은 `MINIO_STORAGE_CLASS_STANDARD` 환경변수를 수정하여 변경할 수 있다.
    - `EC:N` 형태로 설정한다.
    - 이렇게 설정하는 경우에도 최초로 server pool을 구성할 때 drive 개수의 절반을 넘길 수는 없다.

  ```bash
  $ export MINIO_STORAGE_CLASS_STANDARD="EC:8"
  ```



- MinIO는 최소 4대의 node로 하나의 erasure set을 구성하는 것을 권장한다.

  > https://github.com/minio/minio/discussions/18572

  - Node가 1대일 경우
    - 당연하게도, node가 내려가게 되면 지속적인 서비스가 불가능하다.
  - Node가 2대일 경우
    - Node 1대가 내려갈 경우 write quorum을 충족하지 못 해 쓰기 작업이 불가능해진다.

  - Node가 3대일 경우
    - Node 1대가 내려가더라도 write quorum을 충족하므로 읽기, 쓰기 작업이 모두 가능하다.
  - Node가 4대일 경우
    - Node 2대가 내려가더라도 read quorum을 충족하므로 읽기 작업이 가능하다.
  - Node가 4대일 때 부터 2개의 node가 내려가더라도 읽기 작업은 가능하므로, 최소 4대의 node로 server pool을 구성하는 것을 권장한다.



- Parity의 개수와 Storage Efficiency
  - Parity의 개수에 따라 가용성과 사용 가능한 storage의 양이 달라진다.
    - Parity의 개수가 증가할수록 가용성도 증가하지만 가용한 storage의 양은 감소한다.
  - Parity로 지정된 shard(drive)는 data를 저장하는 용도로는 사용할 수 없기 때문이다.



- MinIO는 Reed-Solomon coding을 사용한다.

  > https://www.cs.cmu.edu/~guyb/realworld/reedsolomon/reed_solomon_codes.html

  - Reed-Solomon code
    - Irving S. Reed와 Gustave Solomon이 소개한 block 기반의 오류 정정 코드이다.
    - Data storage나 network 상에서 오염된 data를 정정하기 위해 사용한다.
    - Reed-Solomon code는 BCH의 하위 집합이며, linear block code이다.
  - Encoder와 decorder로 구성된다.
    - Reed-Solomon encoder는 data를 block 단위로 받은 후 해당 불록에 정정을 위한 여분의 bits를 추가한다.
    - Reed-Solomon decoder는 data를 각 block을 처리하면서 error가 발생했다면, encoder에서 추가한 여분의 bits를 사용하여 정정한다.





## Object 관리하기

- Object와 Bucket
  - Objcet는 Image, audio file, spreadsheet, 실행 가능한 code 등의 binary file을 말한다.
  - Bucket object들을 그룹화 하기 위한 개념이다.
    - 최상위 filesystem 상에서 최상위 directory라고 생각하면 된다.



- Object Versioning

  - MinIO는 하나의 object 당 최대 1만개 까지의 version을 관리한다.
    - 특정 operation이 실행되면 object의 version이 1만개를 초과하게 될 경우, 해당 operation이 실행되지 못하게 막고 error를 반환한다.
    - 이 경우 1개 이상의 version을 삭제하고 해당 operation을 다시 실행해야한다.
  - Explicit directory object(prefixes)에 대한 생성, 수정, 삭제에 대해서는 version을 생성하지 않는다.
  - Object의 version은 bucket 단위로 관리된다.
    - Versioning은 bucket 단위로 활성화/비활성화 할 수 있다.
    - Object locking 또는 retention rule을 활성화하기 위해서는 반드시 활성화해야한다.
  - 활성화 여부에 따라 client의 일부 행동들이 달라질 수 있다.

  | Operation     | Versioning Enabled                                           | Versioning Disabled \| Suspended           |
  | ------------- | ------------------------------------------------------------ | ------------------------------------------ |
  | PUT(write)    | 객체의 버전을 "latest"로 새로 생성하고 unique한 version ID를 할당한다. | Object의 이름이 같으면 덮어쓴다.           |
  | GET(read)     | 가장 최신 버전인 object를 찾으며, version ID를 통해 특정 version의 object를 찾을 수도 있다. | Object를 탐색한다.                         |
  | LIST(read)    | 특정 bucket 혹은 prefix의 가장 최신 version인 object를 찾으며, version ID와 연결된 모든 객체를 찾는 것도 가능하다. | 특정 bucket 혹은 prefix의 object를 찾는다. |
  | DELETE(write) | 삭제 대상 object에 대해 0-byte delete marker를 생성한다(soft delete). 특정 version의 object를 삭제하는 것도 가능하다(hard delete). | Object를 삭제한다.                         |

  - Versioning은 namespace 단위로 관리된다.
    - 즉 bucket + object의 경로 + object명 까지 포함한 전체 namespace를 가지고 versioning을 한다.
    - 따라서 같은 bucket에 속해 있는 같은 이름의 object라 할지라도, 서로 다른 경로에 위치해 있다면 별도로 versioning된다.
  - Versioning과 Storage Capacity
    - MinIO는 추가된 부분만 versioning하거나 변경된 부분만 versioning하지 않는다.
    - 따라서 version이 증가할 수록 drive 사용량이 상당히 커질 수 있다.
    - 예를 들어 1GB짜리 object가 있다고 가정해보자.
    - 이 object에 100MB를 더해 1.1GB짜리 object로 PUT을 실행했다고 하면, MinIO는 1GB짜리 이전 version의 object와 1.1GB짜리 최신 version의 object를 모두 저장한다.
    - Drive 사용량이 지나치게 커지는 것을 방지하기 위하여 MinIO는 object lifecycle management rule을 통해 object가 자동으로 다른 곳으로 이동되고나 삭제되는 기능을 제공한다.
  - Version ID 생성
    - MinIO는 쓰기를 실행할 때 각 object의 version마다 unique하고 변경 불가능한 ID를 생성한다.
    - 각 object의 version ID는 128-bit fixed-size UUIDv4로 구성된다.
    - MinIO는 client에서 version ID를 설정하는 기능을 지원하지 않으며, 모든 version ID는 MinIO server에 의해 자동으로 생성된다.
    - 만약 versioning이 비활성화 되었거나 정지된 상태라면 `null`이라는 version ID를 부여한다.



- Object Retention(==MinIO Object Locking)

  > AWS S3의 기능, API와 호환된다.

  - MinIO Object Locking은 Write-Once Read-Many(WORM) 불변성을을 강제한다.
    - 이를 통해 version을 부여 받은 object가 삭제되지 않도록 보호한다.
    - Duration based object retention과 indefinite legal hold retention을 모두 지원한다.
  - WORM locked 상태인 object는 lock이 만료되거나 명시적으로 풀 때 까지 수정이 불가능하다.
  - WORM-locked object을 삭제할 때 version ID 명시 여부에 따라 결과가 달라지게 된다.
    - 삭제시에 version ID를 명시하지 않은 경우 해당 객체에 대한 delete marker가 생성되고, 해당 객체는 삭제된 것으로 취급된다.
    - WORM-locked object를 삭제할 때 version ID를 명시할 경우 WORM locking error가 발샐한다.
  - Object locking은 bucket을 생성할 때만 활성화 할 수 있다.
    - Locking을 활성화 하기 위해서는 versioning도 활성화해야한다.



- Object Lifecycle Management
  - Object Lifecycle Management는 시간을 기반으로 object가 자동으로 전이 혹은 만료가 되도록 rule을 설정할 수 있게 해준다.
    - 즉 들어 일정 기간이 지나면 object를 다른 곳으로 옮기거나, object가 삭제 되도록 할 수 있다.
  - Bucket에 versioning의 활성화 여부와 무관하게 동일하게 적용이 가능하다.
  - AWS S3 Lifecycle Management와 호환된다.
    - MinIO는 lifecycle management를 JSON format을 사용하여 하지만, AWS S3등에서 사용하려면 XML로의 변환은 필요할 수 있다.



## Site Replication

- Site Replication
  - 여러 개의 독립적인 MinIO instance들을 peer sites라 불리는 cluster로 묶어 replica들을 관리하는 것이다.
  - 같은 peer sites로 묶인 MinIO instance(peer site)는 아래와 같은 것들을 동기화한다.
    - Bucket 혹은 object의 생성, 수정 삭제와 관련된 것들(Bucket과 Object Configuration, policy, mc tag set, lock, encryption setting).
    - IAM user, group, policy 등의 생성 및 삭제.
    - Security Token Service(STS)의 생성.
    - Access key의 생성과 삭제(root user가 소유한 access key는 제외된다).
  - 같은 peer sites로 묶였다고 하더라도 아래와 같은 것들은 동기화하지 않는다.
    - Bucket notification
    - Lifecycle management(ILM) configuration
    - Site configuration setting
  - MinIO identity provicer(IDP) 또는 외부 IDP를 사용한다.
    - 외부 IDP를 사용할경우 sites에 속한 모든 site들은 동일한 configuration을 사용해야한다.
  - Site replication 최초로 활성화 할 경우 IAM(identity and access management) setting이 동기화되는데, 구체적인 순서는 어떤 IDP를 사용하느냐에 따라 다르며, 아래는 MinIO IDP를 사용할 경우의 순서이다.
    - Policy
    - Local user account
    - Group
    - Access Key(root user의 access key는 동기화되지 않는다)
    - 동기화된 user account에 대한 policy mapping
    - Security Token Service(STS) user에 대한 policy mapping



- 동기적 replication과 비동기적 replication
  - MinIO는 동기적 replication과 비동기적 replication을 모두 지원한다.
  - 비동기적 replication
    - Object가 실제 복제되기 전에 originating client에게는 복제가 성공했다는 응답이 전달될 수 있다.
    - 따라서 이 경우 복제가 누락될 수 있지만, 복제 속도는 빠르다는 장점이 있다.
  - 동기적 replication
    - Object의 복제가 성공했다는 응답을 보내기 전에 복제를 실행한다.
    - 그러나 복제가 성공하든 실패하든 성공했다는 응답을 반환하여 복제 속도가 지나치게 느려지는 것을 방지한다.
  - MinIO는 비동기적 replication을 사용하는 것을 강하게 권장하며, 기본값도 비동기적 replication을 사용하는 것이다.



- 다른 site로 proxy하기
  - MinIO는 같은 peer sites에 속한 다른 instance에게 `GET/HEAD` request를 proxy할 수 있다.
    - 이를 통해 모종의 이유로 instance들 간에 완전히 동기화가 되지 않아도, 요청으로 들어온 object를 반환할 수 있다.
  - 예시
    - Client가 siteA로 특정 object를 요청했다.
    - siteA는 복구가 진행중이라 아직 peer sites에 속한 다른 instance들과 완전히 동기화가 되지 않았다.
    - 따라서 siteA는 client가 요청한 object를 찾을 수 없으므로 이 요청을 siteB로 proxy한다.
    - siteB는 해당 object를 보관중이었으므로 이를 siteA로 반환한다.
    - siteA는 siteB가 반환한 object를 client에게 반환한다.



### Site replication 설정하기

- MinIO container 실행하기

  - Docker compose file을 아래와 같이 작성한다.

  ```yaml
  version: '3.2'
  
  
  services:
    minio1:
      image: minio/minio:latest
      container_name: minio1
      command: ["server", "/data", "--console-address", ":9001"]
      environment:
        - MINIO_ROOT_USER=theo
        - MINIO_ROOT_PASSWORD=chnageme1234
      volumes:
        - ./data:/data
      ports:
        - 9000:9000
        - 9001:9001
      networks:
        - minio
    
    minio2:
      image: minio/minio:latest
      container_name: minio2
      command: ["server", "/data", "--console-address", ":9001"]
      environment:
        - MINIO_ROOT_USER=theo
        - MINIO_ROOT_PASSWORD=chnageme1234
      volumes:
        - ./data2:/data
      ports:
        - 9010:9000
        - 9011:9001
      networks:
        - minio
  
  networks:
    minio:
      driver: bridge
  ```

  - Container 실행하기

  ```bash
  $ docker compose up
  ```



- Site replication 설정 전 확인해야 할 사항

  - Cluster setting을 backup한다.
    - 아래와 같은 명령어를 입력하여 bucket metadata와 IAM configuration을 backup한다.

  ```bash
  $ mc admin cluster bucket export
  $ mc admin cluster iam export
  ```

  - Site replication을 위해서는 오직 하나의 site에만 data가 있어야한다.
    - 다른 site들은 bucket이나 object등의 data가 있어선 안 된다.
  - 모든 site는 같은 IDP를 사용해야한다.
  - 모든 site의 MinIO server version이 같아야한다.
  - Site replication은 bucket versioning 기능을 필요로한다.
    - 모든 bucket에 자동적으로 bucket versioning을 적용한다.
    - Site replication을 사용하면서 bucket versioning을 비활성화 할 수는 없다.
  - Bucket replication과 multi-site replication은 함께 사용할 수 없다.
    - 따라서 이전에 bucket replication을 설정했다면, bucket replication rule을 삭제해야한다.



- Web UI를 통해 설정하기

  - 위에서 실행한 두 개의 MinIO 중 한 곳의 web UI에 접속한다.
  - 좌측 sidebar에서 `Administrator` - `Site Replication`을 선택한다.
  - `Add Sites`를 클릭 후 필요한 정보를 입력한다.
    - `Site Name`(optional): 원하는 이름을 입력하면 된다.
    - `Endpoint`(required): protocol, 주소, port를 입력하면 된다.
    - `Access Key`: 각 MinIO instance의 `MINIO_ROOT_USER`을 입력하면 된다.
    - `Secret Key`: 각 MinIO instance의 `MINIO_ROOT_PASSWORD`을 입력하면 된다.

  - 완료된 후에는 `Replication Status`를 통해 replication 상황을 확인할 수 있다.
  - 추후 추가도 마찬가지 방식으로 진행하면 되며, site에 대한 수정 및 삭제도 web UI를 통해 가능하다.



- MinIO Client를 통해 설정하기

  - 각 site에 대한 alias 설정하기

  ```bash
  $ mc alias set foo http://127.0.0.1:9000 theo chnageme1234
  $ mc alias set bar http://minio2:9000 theo chnageme1234
  ```

  - Site replication configuration을 추가한다.

  ```bash
  $ mc admin replicate add foo bar
  ```

  - 확인을 위해 site replication configuration을 확인한다.

  ```bash
  $ mc admin replicate info foo
  ```

  - Replication status를 확인한다.

  ```bash
  $ mc admin replicate status foo
  ```



- MinIO Client를 통해 site 추가, 수정 및 삭제하기

  - Site 추가하기

  ```bash
  $ mc alias set baz http://minio3:9000 theo chnageme1234
  
  # 기존의 peer site들 중 아무 곳에나 추가하면 된다.
  $ mc admin replicate add foo baz
  ```

  - Site endpoint 수정하기
    - 예를 들어, 위에서 등록한 bar site의 endpoint를 수정하려 한다고 가정해보자.

  ```bash
  # Deployment ID를 받아온다.
  $ mc admin replicate info bar
  
  # 위에서 받아온 deployment ID를 가지고 아래 명령어를 수행한다.
  $ mc admin replicate update ALIAS --deployment-id [DEPLOYMENT-ID] --endpoint [NEW-ENDPOINT]
  ```

  - Site 제거하기
    - 아래 명령어는 foo가 속한 peer sites에서 bar site를 제외시키는 명령어이다.

  ```bash
  $ mc admin replicate rm foo bar --force
  ```



- 주의사항

  - MinIO를 여러 개의 drive에 배포할 경우 MinIO는 가장 작은 drive의 용량을 가지고 capacity를 계산한다.
    - 예를 들어 15개의 10TB drive와 1개의 1TB drive가 있을 경우 MinIO는 drive별 capacity가 1TB라고 계산한다.
  - MinIO는 server가 restart 되더라도 물리 drive들이 동일한 순서가 보장된다고 가정한다.
    - 주어진 mount point가 항상 같은 formatted drive를 가리키도록 하기 위함이다.
    - 따라서 MinIO는 reboot시에 drive의 순서가 변경되지 않도록 `/etc/fstab`을 사용하거나 이와 유사한 file 기반의 mount 설정을 하는 것을 강하게 권장한다.

  ```bash
  $ mkfs.xfs /dev/sdb -L DISK1
  $ mkfs.xfs /dev/sdc -L DISK2
  $ mkfs.xfs /dev/sdd -L DISK3
  $ mkfs.xfs /dev/sde -L DISK4
  
  $ nano /etc/fstab
  # <file system>  <mount point>  <type>  <options>         <dump>  <pass>
  LABEL=DISK1      /mnt/disk1     xfs     defaults,noatime  0       2
  LABEL=DISK2      /mnt/disk2     xfs     defaults,noatime  0       2
  LABEL=DISK3      /mnt/disk3     xfs     defaults,noatime  0       2
  LABEL=DISK4      /mnt/disk4     xfs     defaults,noatime  0       2
  ```

  - MinIO에서 drive들을 지정할 때는 expansion notation(`x...y`)를 사용해야한다.
    - 예를 들어 MinIO 환경 변수 file에서 `MINIO_VOLUMES`에 여러 개의 drive를 지정하기 위해서는 아래와 같이 작성하면 된다.

  ```toml
  MINIO_VOLUMES="/data-{1...4}"
  ```



# MinIO 구성

## Single-Node Multi-Drive MinIO

- Docker를 사용하여 SNMD 방식으로 MinIO 배포하기

  - 먼저 MinIO Docker image를 pull 받는다.

  ```bash
  $ docker pull minio/minio
  ```

  - MinIO 환경 변수 file을 생성한다.
    - `.env` file로 생성하면 된다.

  ```toml
  MINIO_ROOT_USER=myminioadmin
  MINIO_ROOT_PASSWORD=minio-secret-key-change-me
  
  # Drive들의 경로를 입력하면 되며, 여기 입력한 경로들은 모두 존재해야하고, 비어있어야 한다.
  
  MINIO_VOLUMES="/data-{1...4}"
  ```

  - Docker container를 실행한다.

  ```bash
  $ docker run                                    \
    -p 9000:9000 -p 9001:9001                     \
    -v PATH1:/data-1                              \
    -v PATH2:/data-2                              \
    -v PATH3:/data-3                              \
    -v PATH4:/data-4                              \
    -v ENV_FILE_PATH:/etc/config.env              \
    -e "MINIO_CONFIG_ENV_FILE=/etc/config.env"    \
    --name "minio_local"                          \
    minio/minio server --console-address ":9001"
  ```





## Multi-Node Multi-Drive MinIO

- Docker를 사용하여 MinIO를 MNMD로 배포하기	

  - MinIO에서는 server pool을 설정할 때 `{x...y}` 형식의 expansion notation을 사용해야 한다.
    - MinIO에서는 아래와 같이 sequential한 hostname 또는 IP를 사용한는 것을 권장한다.
    - Hostname 혹은 IP를 sequential하게 사용할 경우 관리의 overhead가 줄어든다는 장점이 있다.
    - Sequential하게 설정하지 않더라도 정상 동작한다.

  ```bash
  # 예를 들어 아래와 같이 sequential하게 hostname을 설정했을 때
  minio-01.example.com
  minio-02.example.com
  minio-03.example.com
  minio-04.example.com
  
  # sever pool 설정은 아래와 같이 해준다.
  minio-0{1...4}.example.com
  
  
  # 만약 아래와 같이 non sequential하게 hostname을 설정했다면
  minio-foo.example.com
  minio-bar.example.com
  minio-baz.example.com
  minio-qux.example.com
  
  # sever pool 설정은 아래와 같이 해준다.
  minio-foo.example.com minio-bar.example.com minio-baz.example.com minio-qux.example.com
  ```

  - MinIO를 여러개의 node로 구성할 경우 Nginx와 같은 load balancer를 사용하는 것이 권장된다.
    - MinIO node가 추가 삭제될 때 마다 client에도 이를 추가하는 것이 번거롭기 때문이다.
    - 따라서 아래 예시에서는 Nignx도 함께 배포할 것이다.
  - 아래와 같이 Nginx 설정 파일을 작성한다.
    - Request body에 담겨서 오는 file 크기에 제한을 두지 않기 위해서 `client_max_body_size`의 값을 0으로 설정했다.

  ```nginx
  user  nginx;
  worker_processes  auto;
  
  error_log  /var/log/nginx/error.log warn;
  pid        /var/run/nginx.pid;
  
  events {
      worker_connections  4096;
  }
  
  http {
      include       /etc/nginx/mime.types;
      default_type  application/octet-stream;
  
      log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
  
      access_log  /var/log/nginx/access.log  main;
      sendfile        on;
      keepalive_timeout  65;
  
      # include /etc/nginx/conf.d/*.conf;
  
      upstream minio {
          server minio1:9000;
          server minio2:9000;
      }
  
      upstream console {
          ip_hash;
          server minio1:9001;
          server minio2:9001;
      }
  
      server {
          listen       9000;
          listen  [::]:9000;
          server_name  localhost;
  
          ignore_invalid_headers off;
          client_max_body_size 0;
          # To disable buffering
          proxy_buffering off;
          proxy_request_buffering off;
  
          location / {
              proxy_set_header Host $http_host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
  
              proxy_connect_timeout 300;
              proxy_http_version 1.1;
              proxy_set_header Connection "";
              chunked_transfer_encoding off;
  
              proxy_pass http://minio;
          }
      }
  
      server {
          listen       9001;
          listen  [::]:9001;
          server_name  localhost;
  
          ignore_invalid_headers off;
          client_max_body_size 0;
          proxy_buffering off;
          proxy_request_buffering off;
  
          location / {
              proxy_set_header Host $http_host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
              proxy_set_header X-NginX-Proxy true;
  
              real_ip_header X-Real-IP;
  
              proxy_connect_timeout 300;
              
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
              
              chunked_transfer_encoding off;
  
              proxy_pass http://console;
          }
      }
  }
  ```

  - `docker-compose` file을 아래와 같이 작성한다.
    - `command` 부분에 server pool을 `http://minio{1...2}/data{1...2}`와 같이 설정해준다.
    - 예시에서는 sequential한 hostname(minio1, minio2)을 사용하였지만, sequential하진 않은 hostname을 사용할 경우 주석 처리한 부분과 같이 따로 작성해주면 된다.

  ```yaml
  version: '3.7'
  
  
  x-minio-common: &minio-common
    image: minio/minio:latest
    command: server --console-address ":9001" http://minio{1...2}/data{1...2}
    # hostname 혹은 IP가 sequential하지 않을 경우
    # command: server --console-address ":9001" http://minio-foo/data{1...2} http://minio-bar/data{1...3}
    environment:
      MINIO_ROOT_USER: 'me'
      MINIO_ROOT_PASSWORD: 'minio_password'
  
  
  services:
    minio1:
      <<: *minio-common
      hostname: minio1
      volumes:
        - ./drives/data1-1:/data1
        - ./drives/data1-2:/data2
  
    minio2:
      <<: *minio-common
      hostname: minio2
      volumes:
        - ./drives/data2-1:/data1
        - ./drives/data2-2:/data2
  
    nginx:
      image: nginx:latest
      hostname: nginx
      volumes:
        - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      ports:
        - "9020:9000"
        - "9021:9001"
      depends_on:
        - minio1
        - minio2
  ```

  - Docker container들을 실행시킨다.

  ```bash
  $ docker compose up
  ```

  - 9020, 9021 port로 요청을 보내면 Nginx가 요청을 받게 되고, Nginx가 해당 요청을 minio1 혹은 minio2 node로 load balancing한다.





# Kafka와 함께 사용하기

## Camel Kafka Connector로 MinIO의 data를 Kafka로 전송하기

- Camel Kafka Connector 실행하기

  - 아래 site에서 package file을 받는다.

    - MinIO connector도 있지만 MinIO는 AWS S3와 호환되므로 여기서는 AWS S3 source connector를 사용할 것이다.

    > https://camel.apache.org/camel-kafka-connector/3.20.x/reference/index.html

  - 준비된 packag file을 Kafka connect package가 모여 있는 곳으로 옮긴 후 압축을 푼다.

    - `connect-distributed.properties` 혹은 `connect-standalone.properties` 중 사용하려는 property file의 `plugin.path`에 설정된 경로에 넣으면 된다.

    ```bash
    $ unzip camel-aws-s3-source-kafka-connector-<version>-package.tar.gz
    $ tar -xvf camel-aws-s3-source-kafka-connector-<version>-package.tar
    ```

  - Kafka connect를 실행한다.

    ```bash
    $ /bin/connect-standalone /etc/kafka/connect-standalone.properties
    ```

  - 각 connector에 맞는 양식으로 connector 생성 요청을 보낸다.

    - 예시는 [예시를 작성해둔 repository](https://github.com/apache/camel-kafka-connector-examples/tree/main)나 package의 압축을 풀었을 때 함께 풀린 `docs` directory에서 볼 수 있다.
    - 혹은 [document](https://camel.apache.org/camel-kafka-connector/3.20.x/reference/connectors/camel-aws-s3-source-kafka-source-connector.html)에서도 확인할 수 있다.
    - `camel.kamelet.aws-s3-source.overrideEndpoint`를 true로 주고, `camel.kamelet.aws-s3-source.uriEndpointOverride`에 MinIO의 URI를 입력한다.

  ```bash
  $ curl -XPOST 'localhost:8083/connectors' \
  --header 'Content-type: application/json' \
  --data-raw '{
    "name": "s3-source-connector",
    "config": {
      "connector.class": "org.apache.camel.kafkaconnector.awss3source.CamelAwss3sourceSourceConnector",
      "topics":"my-s3-topic",
      "camel.kamelet.aws-s3-source.bucketNameOrArn":"test",
      "camel.kamelet.aws-s3-source.deleteAfterRead":false,
      "camel.kamelet.aws-s3-source.accessKey":"user",
      "camel.kamelet.aws-s3-source.secretKey":"password",
      "camel.kamelet.aws-s3-source.region":"foo",
      "camel.kamelet.aws-s3-source.overrideEndpoint":true,
      "camel.kamelet.aws-s3-source.uriEndpointOverride":"http://<host_machine_IP>:9000"
    }
  }'
  ```

  - Kafka Connect 실행시 `value.converter`를 `org.apache.kafka.connect.json.JsonConverter`로 설정했다면 message는 아래와 같이 생성된다.

  ```json
  // body
  {
  	"schema": {
  		"type": "bytes",
  		"optional": false
  	},
  	"payload": "cHJpbnqwdgElbGxvIQghyvcITQIp"
  }
  
  // header
  {
  	"CamelHeader.CamelAwsS3VersionId": "<version_id>",
  	"CamelHeader.CamelMessageTimestamp": "1704862344000",
  	"CamelHeader.CamelAwsS3ContentType": "text/x-python",
  	"CamelHeader.CamelAwsS3ContentLength": "21",
  	"CamelHeader.aws.s3.key": "test.py",
  	"CamelHeader.CamelAwsS3Key": "test.py",
  	"CamelHeader.aws.s3.bucket.name": "test",
  	"CamelHeader.CamelAwsS3BucketName": "test",
  	"CamelHeader.CamelAwsS3ETag": "\"789gwg8w7g8g8e7g87879w87985400878\""
  }
  ```



- 주의사항
  - `camel.kamelet.aws-s3-source.region`
    - MinIO를 대상으로 data를 가져오는 것이므로  설정하지 않아도 된다고 생각할 수 있지만, 해당 옵션은 required 값으로 반드시 설정해야 한다.
    - 위 값처럼 아무 값이나 넣어주기만 하면 된다.
  - Docker로 실행할 경우 `camel.kamelet.aws-s3-source.uriEndpointOverride`에 docker network 상의 host명이나 docker network 상의 IP를 입력할 경우 정상적으로 실행되지 않으므로 반드시 host machine의 IP를 입력해야한다.
    - 당연히 MinIO Docker instance에서 port를 publish해야한다.
  - 기본적인 동작 방식이 bucket에서 data를 가져온 후 **해당 data를 삭제**하는 방식이다. 
    - 따라서 삭제를 원치 않을 경우 위와 같이 `camel.kamelet.aws-s3-source.deleteAfterRead` 옵션을 false로 줘야 한다.
    - 다만 이 경우 다음에 data를 push할 때 모든 data를 push하게 된다.





## Bucket의 event를 전송하기

> https://min.io/docs/minio/linux/administration/monitoring/bucket-notifications.html

- MinIO는 bucket에서 발생한 event를 Kafa, Elasticsearch, MySQL, PostgreSQL 등으로 전송하는 기능을 지원한다.
  - 전송을 지원하는 event type은 [AWS S3 Event Notification](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)과 완전히 호환된다.
  - 위에서 살펴본 Camel Kafka Connector의 경우 file 자체를 전송하여 message의 크기가 크다는 점과, 변경 사항 추적이 힘들다는 단점이 있다.



- MinIO는 `mc event add`를 사용하여 특정 bucket에 대한 event notification trigger를 추가할 수 있다.

  - 형식은 아래와 같다.

  ```bash
  mc [GLOBALFLAGS] event add \
                   [--event "string"]  \
                   [--ignore-existing] \
                   [--prefix "string"] \
                   [--suffix "string"] \
                   ALIAS               \
                   ARN
  ```

  - `--event`에 넣을 수 있는 값들은 아래와 같다.
    - 복수의 값을 event를 등록해야 할 경우 `--event put,get`과 같이 `,`로 구분하여 입력하면 된다.
    - 각 value들은 S3 Event와 호환된다.

  | Supported Value | Corresponding S3 Events                                      |
  | :-------------- | :----------------------------------------------------------- |
  | `put`           | `s3:ObjectCreated:CompleteMultipartUpload`<br />`s3:ObjectCreated:Copy`<br />`s3:ObjectCreated:DeleteTagging`<br />`s3:ObjectCreated:Post`<br />`s3:ObjectCreated:Put`<br />`s3:ObjectCreated:PutLegalHold`<br />`s3:ObjectCreated:PutRetention`<br />`s3:ObjectCreated:PutTagging` |
  | `get`           | `s3:ObjectAccessed:Head`<br />`s3:ObjectAccessed:Get`<br />`s3:ObjectAccessed:GetRetention`<br />`s3:ObjectAccessed:GetLegalHold` |
  | `delete`        | `s3:ObjectRemoved:Delete`<br />`s3:ObjectRemoved:DeleteMarkerCreated` |
  | `replica`       | `s3:Replication:OperationCompletedReplication`<br />`s3:Replication:OperationFailedReplication`]<br />`s3:Replication:OperationMissedThreshold`<br />`s3:Replication:OperationNotTracked`<br />`s3:Replication:OperationReplicatedAfterThreshold` |
  | `ilm`           | `s3:ObjectTransition:Failed`<br />`s3:ObjectTransition:Complete`<br />`s3:ObjectRestore:Post`<br />`s3:ObjectRestore:Completed` |
  | `scanner`       | `s3:Scanner:ManyVersions`<br />`s3:Scanner:BigPrefix`        |





## Bucket의 event를 Kafka로 전송하기

- 먼저 MinIO host에 대한 alias를 생성한다.

  ```bash
  $ mc alias set <alias> <URL> <ACCESS_KEY> <SECRET_KEY>
  
  # e.g. 위에서 Multi-Node Multi-Drive MinIO와 같이 구성했을 경우 아래와 같이 하면 된다.
  $ mc alias set foo http://<server_IP> me minio_password
  ```



- MinIO에 Kafka와 관련된 정보를 추가한다.

  > 각 설정에 대한 설명은 아래에서 확인할 수 있다.
  >
  > https://min.io/docs/minio/linux/reference/minio-server/settings/notifications/kafka.html#minio-server-config-bucket-notification-kafka

  - `ENDPOINT`에는 Kafka broker들을 `,`로 구분하여 입력하면 된다.
  - `IDENTIFIER`에는 unique한 값을 설정해주면 된다.
    - `notify_kafka`라는 service에 대한 대한 이름을 설정하는 것이다.
    - 만일 `notify_kafka`에 동일한 `IDENTIFIER`를 설정할 경우 해당 설정을 덮어쓰게 된다.
  - 아래와 같이 환경 변수로 설정할 수도 있고

  ```bash
  set MINIO_NOTIFY_KAFKA_ENABLE_<IDENTIFIER>="on"
  set MINIO_NOTIFY_KAFKA_BROKERS_<IDENTIFIER>="<ENDPOINT>"
  set MINIO_NOTIFY_KAFKA_TOPIC_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_SASL_USERNAME_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_SASL_PASSWORD_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_SASL_MECHANISM_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_TLS_CLIENT_AUTH_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_SASL_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_TLS_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_TLS_SKIP_VERIFY_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_CLIENT_TLS_CERT_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_CLIENT_TLS_KEY_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_QUEUE_DIR_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_QUEUE_LIMIT_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_VERSION_<IDENTIFIER>="<string>"
  set MINIO_NOTIFY_KAFKA_COMMENT_<IDENTIFIER>="<string>"
  ```

  - `mc admin config`를 사용하여 추가할 수도 있다.
    - `alias`에는 위에서 생성한 alias를 입력하면 된다.

  ```bash
  mc admin config set <alias>/ notify_kafka:<IDENTIFIER> \
     brokers="<ENDPOINT>" \
     topic="<string>" \
     sasl_username="<string>" \
     sasl_password="<string>" \
     sasl_mechanism="<string>" \
     tls_client_auth="<string>" \
     tls="<string>" \
     tls_skip_verify="<string>" \
     client_tls_cert="<string>" \
     client_tls_key="<string>" \
     version="<string>" \
     queue_dir="<string>" \
     queue_limit="<string>" \
     comment="<string>"
     
  # e.g.
  $ mc admin config set foo notify_kafka:foo brokers="<Kafka_brokers>" topic="foo"
  ```
  
  - 잘 설정됐는지 확인하려면, 아래와 같이 입력하면 된다.
  
  ```bash
  $ mc admin config get <alias> notify_kafka
  ```

  - MinIO deployment를 재실행한다.
    - 변경된 설정을 적용하기 위해서 아래와 같이 deployment를 재시작해야한다.
  
  ```bash
  $ mc admin service restart <alias>
  ```



- Bucket notification을 설정

  - 먼저 ARN 정보를 확인해야한다.
    - Bucket notification 설정시에 ARN 정보를 입력해야 한다.
    - 아래와 같은 방식으로 확인할 수 있다.
    - 결과에서 `info.sqsARN`을 확인하면 된다.

  ```bash
  $ mc admin info --json <alias>
  ```

  - Bucket notification을 설정한다.
    - Event를 publish할 alias와 bucket을 `<alias>/<bucket>` 형태로 입력한다.
    - 위에서 확인한 ARN을 그대로 `<ARN>`에 넣어준다.
    - `<events>`에는 위에서 확인한 값들을 넣으면 된다.

  ```bash
  $ mc event add <alias>/<bucket> <ARN> --event <events>
  
  # e.g.
  $ mc event add foo/bar arn:minio:sqs::some_identifier:kafka --event get,put,delete
  ```

  - 잘 설정되었는지 확인한다.

  ```bash
  $ mc event ls <alias>/<bucket> <ARN>
  ```



- 이미 설정한 Kafka 관련 설정 수정하기

  - 아래와 같이 설정을 변경할 수 있다.
    - 기존에 설정했던 `IDENTIFIER`를 알아야한다.

  ```bash
  $ mc admin config set <ALIAS>/ notify_kafka:<IDENTIFIER> \
     brokers="https://kafka1.example.net:9200, https://kafka2.example.net:9200" \
     topic="<string>"
  ```

  - 변경될 설정을 적용하기 위해 deployment를 재실행한다.

  ```bash
  $ mc admin service restart <alias>
  ```
  
  - 삭제하기
  
  ```bash
  $ mc event rm <alias>/<bucket> <ARN>
  
  # e.g.
  $ mc event rm foo/bar arn:minio:sqs::some_identifier:kafka
  ```



- 각 bucket 별로 다른 topic으로 전송하기

  - 먼저 두 개의 alias를 생성한다.

  ```bash
  $ mc alias set foo <URL> <ACCESS_KEY> <SECRET_KEY>
  $ mc alias set bar <URL> <ACCESS_KEY> <SECRET_KEY>
  ```

  - 각 alias 별로 Kafka 관련 설정을 해준다.
    - 주의할 점은 `notify_kafka:IDENTIFIER`부분을 아래와 같이 각기 다르게 설정해줘야 한다는 점이다.

  ```bash
  $ mc admin config set foo notify_kafka:foo \
     brokers="localhost:9092" \
     topic="minio_foo"
     
  $ mc admin config set foo notify_kafka:bar \
     brokers="localhost:9092" \
     topic="minio_bar"
     
  # 변경 사항 적용
  $ mc admin service restart <alias>
  ```

  - ARN 정보를 확인한다.
    - 위에서 설정한 `IDENTIFIER`가 포함된 alias들이 보일 것이다.

  ```json
  {
      "status": "success",
      "info": {
          "mode": "online",
          "sqsARN": [
              "arn:minio:sqs::prospector:kafka",
              "arn:minio:sqs::synap:kafka"
          ]
      }
      // ...
  }
  ```

  - Notification 설정시 각 alias/bucket별로 각기 다른 ARN을 적용한다.

  ```bash
  $ mc event add foo/foo arn:minio:sqs::foo:kafka --event get,put,delete
  $ mc event add bar/bar arn:minio:sqs::foo:kafka --event get,put,delete
  ```



- Bucket과 file 경로가 Kafka message의 key값이 된다.
  - 따라서 같은 file은 같은 partition으로 전송되는 것이 보장된다.





# MinIO Client

## MinIO command line tool

> https://min.io/docs/minio/linux/reference/minio-mc.html#command-mc

- MinIO는 `mc`라는 command line tool을 지원한다.

  - AWS S3 API와도 호환이 가능하다.

  - 아래와 같이 사용하면 된다.

  ```bash
  $ mc [GLOBALFAGS] COMMAND
  ```

  - MinIO에 내장되어 있지는 않으므로 사용하려면 별도의 설치가 필요하다.
    - MinIO 공식 Docker image를 사용할 경우 설치 없이 사용이 가능하다.
  - JSON 형식의 configuration file을 사용하며, 기본 위치는 `~/.mc/config.json`이다.



- `mc alias`

  - S3와 호환 가능한 hosts들을 관리하기 위한 기능이다.
  - `list`
    - Alias들의 목록을 보여준다.

  ```bash
  $ mc alias list
  ```

  - `set`
    - Alias를 추가하거나 기존의 alias를 수정한다.

  ```bash
  $ mc set <alias> <URL> <ACCESS_KEY> <SECRET_KEY>
  ```





## Python

> https://min.io/docs/minio/linux/developers/python/API.html

- MinIO Python SDK 설치하기

  - pip를 사용하여 설치

  ```bash
  $ pip install minio
  ```

  - Source를 사용하여 설치

  ```bash
  $ git clone https://github.com/minio/minio-py
  $ cd minio-py
  $ python setup.py install
  ```



- MinIO client

  - 주의 사항
    - MinIO object는 Python의 `threading` library와 함께 사용할 때 thread safe하다.
    - 그러나 `multiprocessing` package를 사용하여 여러 process에서 함께 사용할 때는 thread safe하지 않다.
    - 따라서 multi processing 환경에서 MinIO object를 사용해야 할 경우, 각 process마다 MinIO object를 생성해야한다.
  
  - MinIO client 시작하기
    - 접속정보를 잘 못 입력하더라도 error가 발생하지는 않는다.
  
  ```python
  from minio import Minio
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  ```
  
  - File upload
  
  ```python
  from minio import Minio
  from minio.error import S3Error
  
  def main():
      client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  
      # upload할 file의 경로
      source_file = "./tmp.json"
      # upload할 bucket
      bucket_name = "test"
      # MinIO 내에서의 이름
      destination_file = "tmp.json"
  
      client.fput_object(bucket_name, destination_file, source_file)
  
  if __name__ == "__main__":
      try:
          main()
      except S3Error as exc:
          print("error occurred.", exc)
  ```

  - Object 가져오기
    - `get_object` method를 사용한다.
    - response에서 object 정보를 읽은 후에는 `close` method를 호출하여 network resource를 release 해야한다.
    - 만약 connection을 다시 사용하고자 한다면 `release_conn` method를 호출하면 된다.
  
  ```python
  from minio import Minio
  
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  
  try:
      object_path = "tmp.json"
      response = client.get_object("test", object_path)
      with open(object_path, "wb") as binary:
          binary.write(response.read())
  finally:
      response.close()
      response.release_conn()
  
  # 특정 version의 object 가져오기
  try:
      response = client.get_object(
          "my-bucket", "my-object",
          version_id="dfbd25b3-abec-4184-a4e8-5a35a5c1174d",
      )
  finally:
      response.close()
      response.release_conn()
  
  # offset과 length로 object 가져오기
  try:
      response = client.get_object(
          "my-bucket", "my-object", offset=512, length=1024,
      )
  finally:
      response.close()
      response.release_conn()
  ```
  
  - Object 삭제하기
  
  ```python
  from minio import Minio
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  
  # object 삭제
  client.remove_object("my-bucket", "my-object")
  
  # object의 특정 version을 삭제
  client.remove_object(
      "my-bucket", "my-object",
      version_id="dfbd25b3-abec-4184-a4e8-5a35a5c1174d",
  )
  ```
  
  - Bucket 생성하기
  
  ```python
  from minio import Minio
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  bucket_name="my_bucket"
  found = client.bucket_exists(bucket_name)
  if not found:
      client.make_bucket(bucket_name)
      print("Created bucket", bucket_name)
  else:
      print("Bucket", bucket_name, "already exists")
  ```
  
  - Bucket 내의 object들 조회하기
    - `prefix`: 해당 prefix로 시작하는 object들만 조회한다.
    - `recursive`: object들을 재귀적으로 나열한다.
    - `start_after`: 해당 경로로 시작하는 object들만 조회한다.
    - `include_user_meta`: 사용자 metadata를 함께 조회할지 설정한다.
    - `include_version`: object의 version 정보도 함께 조회할지 설정한다.
  
  ```python
  from minio import Minio
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  
  objects = client.list_objects("my-bucket")
  for obj in objects:
      print(obj)
  ```
  



- MinIO Python client로 notification 설정하기

  - MinIO Python client로도 notification 설정이 가능하다.
  - 아래 code는 Kafka로 event를 publish 하도록 하는 code이다.
    - 다만, arn은 직접 설정해줘야한다.
    - `QueueConfig`의 첫 번째 인자로 arn을 입력하고, 두 번째 인자로 event들을 입력하면 된다.

  ```python
  from minio.notificationconfig import NotificationConfig, QueueConfig
  from minio import Minio
  
  
  client = Minio("localhost:9000", access_key="foo", secret_key="foo_auth", secure=False)
  
  config = NotificationConfig(queue_config_list=[
      QueueConfig(
          "<arn>", 
          ["s3:ObjectCreated:*","s3:ObjectRemoved:*"]
      )
  ])
  
  client.set_bucket_notification("bucket-name", config)
  ```








# AWS CLI

- AWS CLI를 설치한다.

  - pip를 사용하여 설치가 가능하다.

  ```bash
  $ pip install awscli
  ```

  - 설정을 실행한다.

  ```bash
  $ aws configure
  ```

  - MinIO에서 사용하기 위해 추가적인 설정을 해준다.

  ```bash
  $ aws configure set default.s3.signature_version s3v4
  ```



- 명령어

  - Bucket 목록 확인

  ```bash
  $ aws --endpoint-url http://localhost:9000 s3 ls
  ```

  - Bukcet 내의 object 목록 확인

  ```bash
  $ aws --endpoint-url http://localhost:9000 s3 ls s3://<bucket_name>
  ```

  - Bucket 생성

  ```bash
  $ aws --endpoint-url http://localhost:9000 s3 mb s3://<bucket_name>
  ```

  - Local storage와 bucket을 sync시키기
    - `--delete` option을 주면 삭제된 파일도 함께 동기화된다.

  ```bash
  # local의 파일들을 S3로 sync
  $ aws --endpoint-url http://localhost:9000 s3 sync <local_storage_path> s3://<bucket_name> --delete
  
  # S3의 파일들을 local로 sync
  $ aws --endpoint-url http://localhost:9000 s3 sync s3://<bucket_name> <local_storage_path> --delete
  ```
  
  - Sync뿐 아니라 copy도 가능하다.
    - 기본적으로 하나의 file만 복제가 가능하며, directory 단위로 복제하려면  `--recursive` 옵션을 줘야 한다.
    - `--recursive` 옵션을 줄 경우 하위 directory도 모두 복제된다.
  
  ```bash
  # local에서 S3로 복사
  $ aws --endpoint-url http://localhost:9000 s3 cp <local_storage_path> s3://<bucket_name>
  
  # S3에서 local로 복사
  $ aws --endpoint-url http://localhost:9000 s3 cp se://<bucket_name>/<path> <local_storage_path>
  ```
  
  - `cp`와 `sync` 명령어에서 사용되는 option
    - `--exclude`: 특정 객체를 제외
    - `--include`: 특정 객체를 포함
    - 위 두 옵션은 wildcard를 지원한다.
    - 위 두 옵션의 순서에 따라 실행 결과가 달라질 수 있다.
    - 또한 local path를 절대 경로로 하는지, 상대 경로로 하는지에 따라 include와 exclude의 동작이 달라진다.
  
  ```bash
  # 현재 directory(하위 directory 포함)의 file들 중 확장자가 txt인 파일들은 포함하고, foo로 시작하는 file들은 제외하지만, foo2로 시작하는 파일들은 포함시킨다.
  $ aws --endpoint-url http://localhost:9000 s3 sync . s3://my-bucket --include "*.txt" --exclude "foo*" --include "foo2"
  ```
  
  - Include와 exclude filter에 사용할 수 있는 pattern symbol들은 아래와 같다.
    - `*`: 모든 것을 matching시킨다.
    - `?`: 모든 single character를 matching시킨다.
    - `[sequence]`: `sequence`에 있는 모든 character를 matching시킨다.
    - `[!sequence]`: `sequence`에 포함되지 않는 모든 character를 matching시킨다
  
  - Include와 exclude의 순서에 따라 결과가 달라질 수 있다.
  
  ```bash
  # .txt 파일을만 포함시킨다.
  --exclude "*" --include "*.txt"
  
  # 모든 파일을 제외시킨다.
  --include "*.txt" --exclude "*"
  ```
  
  - 각 filter는 source directory에 대해 평가된다.
    - 만약 source location이 directory가 아닌 file일 경우 해당 source location에 해당하는 file을 저장하고 있는 directory가 source directory가 된다.
    - 아래 예시는 `aws s3 cp /tmp/foo s3://bucket/ --recursive --exclude ".git/*"`와 같이 실행했을 때 어떻게 동작하는지를 보여준다.
  
  ```bash
  # 폴더 구조가 아래와 같을 때
  /tmp/foo/
    .git/
    |---config
    |---description
    foo.txt
    bar.txt
    baz.jpg
  
  # 아래 명령어를 실행하면, source directory는 /tmp/foo가 된다.
  $ aws s3 sync /tmp/foo s3://bucket/ --exclude ".git/*"
  # 이 때 --exclude ".git/*" filter는 /tmp/foo/.git/*와 같이 적용된다.
  ```
  
  - 기본적으로 모든 파일은 include 대상이다.
    - 따라서 `--include`만 주는 것은 결과에 아무런 영향도 미치지 않는다.
  
  ```bash
  # 예를 들어 아래와 같은 파일들이 있을 때
  $ ls
  test.txt    text.txt    test.py    text.py
  
  # 기본적으로 모든 파일이 include 대상이므로 아래와 같이 include를 줘도, include와 match되는 파일만 sync되는 것이 아니라, 모든 파일이 sync된다.
  # 따라서 아래 명령어의 결과는 모두 같다.
  $ aws s3 sync . s3://bucket/ --include "*.py"
  $ aws s3 sync . s3://bucket/ --include "*.txt"
  $ aws s3 sync . s3://bucket/ --include "test.*"
  $ aws s3 sync . s3://bucket/ --include "text.*"
  ```







# Rclone

- Rclone
  - Cloud storage에 있는 파일을 관리하기 위한 commad-line program이다.
    - Go로 개발되었다.
    - Windows, macOS, Linux 등에서 모두 사용이 가능하다.
    - S3를 포함하여 [70개 이상의 cloud storage](https://rclone.org/#providers)를 지원한다.
  - 아래와 같은 기능을 지원한다.
    - Cloud storage에 file backup 혹은 encrypt.
    - Cloud storage로부터 file restore 혹은 decrypt.
    - Cloud storage의 data를 다른 cloud storage나 local로 mirror.
    - 서로 다른 cloud storage 사이의 data 이전.



- 설치하기

  - Ubuntu에 설치하기
    - 설치  과정에서 zip을 다룰 수 있는 package가 필요하다.

  ```bash
  # 만약 zip을 다룰 수 있는 package가 없다면, package를 먼저 설치한다.
  $ apt install zip
  
  # 아래 명령어로 간단하게 설치가 가능하다.
  $ curl https://rclone.org/install.sh | sudo bash
  ```

  - Docker image도 제공하며, 아래와 같이 실행이 가능하다.

  ```bash
  $ docker pull rclone/rclone:latest
  $ docker run --rm rclone/rclone:latest version
  ```

  - 설치 확인

  ```bash
  $ rclone version
  ```

  - 아래 명령어를 통해 rclone을 설정할 수 있다.
    - Storage 선택부터 storage에 접속할 수 있는 접속 정보까지 CLI를 통해서 설정이 가능하다.
    - 각 storage별 설정 정보는 [rclone 사이트](https://rclone.org/docs/)에서 확인이 가능하다.
    - Linux에서 configuration은 OS 계정별로 설정된다.
    - 설정한 내용은 `~/.config/rclone/rclone.conf`에 저장된다.
    - 해당 파일을 직접 수정해도 된다.

  ```bash
  $ rclone config
  ```

  - MinIO에 연결하려면, 아래와 같이 설정하면 된다.

  ```bash
  env_auth> 1
  access_key_id> USWUXHGYZQYFYFFIT3RE
  secret_access_key> MOJRH0mkL1IPauahWITSVvyDrQbEEIwljvmxdq03
  region>
  endpoint> http://10.11.22.33:9000
  location_constraint>
  server_side_encryption>
  ```



- rclone 사용해보기

  - 기본 문법
    - `<subcommand>`에는 `sync`, `copy`, `ls` 등을 사용할 수 있다.

  ```bash
  $ rclone <subcommand> [options] [parameter] [parameter...]
  ```

  - Configuration 상의 모든 remote 확인

  ```bash
  $ rclone listremotes
  ```

  - Sync시키기
    - 아래 예시는 MinIO bucket으로 sync시키는 예시이다.

  ```bash
  $ rclone sync /path/to/files <minio_remote_name>:<bucket_name>
  ```

  - `sync` 관련 옵션

    > 모든 option은 [rclone 문서](https://rclone.org/commands/rclone_sync/#sync-options) 참조

    - `--dry-run`: 실제 실행하진 않고, 실행 결과만을 보여준다.

    - `--delete-excluded`: Sync에서 제외된 file들을 dest에서 삭제한다.
    - `--exclude`: Pattern에 matching되는 file들은 제외한다.
    - `--exclude-from`: File에 작성된 exclude pattern을 읽어서 적용한다.
    - `--include`: Pattern에 matching되는 file들을 포함시킨다.
    - `--include-from`: File에 작성된 include pattern을 읽어서 적용한다.
    - `--filter`: Filtering rule을 추가한다.
    - `--filter-from`: File에 작성된 filtering pattern을 읽어서 적용한다.
    - `--ignore-case`: Filter에서 case를 무시한다.
    - `--include-from` 보다 `--include`가 우선하고, `--exclude-from`보다 `--exclude`가 우선하며, `--filter-from` 보다 `--filter`가 우선한다.



- Filter, include, exclude

  - Pattern
    - `pattern-list`에는 공백 없이 `,`로 구분된 pattern들을 입력한다.

  ```
  *         separator(/)가 아닌 모든 길이의 character를 matching시킨다.
  **        separator(/)를 포함한 모든 길이의 character를 matching시킨다.
  ?         separator(/)가 아닌 모든 single character를 matching시킨다.
  [ [ ! ] { character-range } ]
            character class (must be non-empty)
  { pattern-list }
            pattern alternatives
  {{ regexp }}
            regular expression to match
  c         matches character c (c != *, **, ?, \, [, {, })
  \c        matches reserved character c (c = *, **, ?, \, [, {, }) or character classㄴ
  ```

  - `character-range`

  ```
  c         matches character c (c != \, -, ])
  \c        matches reserved character c (c = \, -, ])
  lo - hi   matches character c for lo <= c <= hi
  ```

  - Pattern이 `/`로 시작할 경우, 오직 top level의 directory에서만 matching시킨다.

  ```
  file.jpg	- file.jpg를 matching시킨다.
  			- directory/file.jpg를 matching시킨다.
  
  /file.jpg	- top level directory에 있는 file.jpg를 matching시킨다.
  			- directory/file.jpg는 matching시키지 않는다.
  ```

  - `--filter` pattern에 `+` 혹은 `-`를 줘서 포함, 제외를 결정할 수 있다.
    - 예를 들어 아래와 같이 pattern 내에 `-`를 입력하면 모든 `.bak`을 제외하겠다는 의미이다.

  ```bash
  $ rclone ls remote: --filter "- *.bak"
  ```

  - `--filter +`는 `--include`와 다르다.
    - `--include`의 경우 `--exclude *` rule을 내포하고 있으나, `--filter +`는 그렇지 않다.
    - 즉, `--include`는 모든 file들이 exclude되었다고 가정하고 포함시킬 파일을 하나씩 추가해 나가는 과정이지만, `--filter`는 그렇지 않다.

  ```bash
  # 아래와 같은 파일이 있을 때
  foo.txt  bar.txt  foo.py  bar.py
  
  # --include "*.txt"가 포함시키는 파일은 아래의 두 개뿐이다.
  foo.txt  bar.txt
  
  # 그러나 --include "+ *.txt"는 모든 파일을 포함시킨다.
  ```

  - `--include...`, `--exclude...`, `--filter...`를 섞어서 사용해선 안 된다.
    - 섞어서 사용한다고 error가 발생하지는 않지만 예상치 못 한 결과가 나올 수 있다.
    - 일반적인 경우에는 `--filter...`를 사용하는 것이 권장된다.



- Rclone을 사용하여 원격 서버의 file을 MinIO로 sync하기

  - SFTP remote와 MinIO remote를 각각 생성한다.

  ```bash
  $ rclone config
  ```

  - 최종적인 설정 파일은 아래와 같다.

  ```ini
  [sftp-test]
  type = sftp
  host = my-host
  user = foo
  pass = ZVwmVwFIgevsUGWnhaEGEgfgrerU
  shell_type = unix
  md5sum_command = md5sum
  sha1sum_command = sha1sum
  
  [minio-test]
  type = s3
  provider = Minio
  access_key_id = my_access_key
  secret_access_key = my_secret_key
  endpoint = http://10.11.22.33:9000
  acl = private
  ```

  - 원격 서버의 file을 MinIO로 sync한다.

  ```bash
  $ rclone sync sftp-test:/path/to/file minio-test:<bucket_name>
  ```









