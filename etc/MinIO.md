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
    - MinIO는 object를 shard라 불리는 덩어리로 나눈 후 이드을 Erasure Set 내의 여러 drive로 분산시켜 저장한다.
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
  - 각 MinIO server 내에는 여러 개의 node들이 있을 수 있으며, client는 이 node들 중 어느 곳에나 연결하여 직접 작업을 수행할 수 있다.
    - 요청을 받은 node는 다른 MinIO server 내의 다른 node들에도 요청을 보내고 다른 node들로부터 응답을 받아 이를 취합하여 최종 응답을 반환한다.
    - Node를 추가, 삭제, 변경할 때 마다 client에도 이 정보를 update하는 것은 까다로운 일이므로, 일반적으로 앞단에 load balancer를 두고 load balancer에 이 정보를 update하는 방식을 사용한다.



- MinIO의 Erasure Coding

  - Erasure Coding(EC)이란
    - Storage에 data를 저장할 때 내결함성을 보장하고, 저장 공간의 효율성을 높이기 위해 설계된 데이터 복제 방식이다.
    - Data를 알고리즘에 따라 n개로 나눈 후에 나뉘어진 데이터들을 Erasure code codec을 사용하여 encoding하여 m개의 parity를 만든다.
    - 이후 data나 parity가 유실될 경우 남은 data와 parity들을 decoding하여 원래의 data를 복구한다.

  - MinIO에서도 data redundancy와 가용성을 위해 Erasure Coding을 사용한다.
    - MinIO는 각 server pool의 drive들을 하나 이상의 같은 크기를 가진 Erasure Set으로 그룹화한다.
    - Erasure Set의 크기와 개수는 server pool을 처음으로 구성할 때 결정되며, server pool이 구성된 이후에는 변경할 수 없다.
  - 각 쓰기 작업마다 MinIO는 object를 data와 parity shard로 분할한다.
    - Parity의 개수는 0부터 Erasure Set size의 절반까지로 설정이 가능하다.
    - 예를 들어 Erasure Set의 size가 12라면, parity는 0부터 6 사이의 값으로 설정이 가능하다.
    - Erasure Set의 size(N)는 data shard의 개수(K) + parity shard의 개수(M)이다.
  - 읽기 작업을 위해서는 shard의 종류와 상관 없이 최소 data shard의 개수 만큼의 shard가 필요하다.
    - 예를 들어 data shard의 개수가 12개, parity shard의 개수가 4개라고 가정해보자.
    - 읽기를 위해서는 data shard의 개수 만큼의 shard가 필요하므로 12개의 shard가 필요하다.
    - 이 때 data shard 중 4개에 문제가 생겼다고 하더라도 남은 data shard의 개수 8개에 parity shard의 개수 4를 더하면 아직 12개의 shard가 남아 있으므로 읽기 작업은 여전히 가능하다.
  - 쓰기 작업을 위해서도 최소 K개의 drive가 필요하다.
    - 만약 parity가 Erasure set의 절반이라면 쓰기 작업을 위해서는 data shard의 개수 + 1개 만큼의 shard가 필요하다.
    - 이는 split-brain 문제를 예방하기 위함이다.



- MinIO는 Reed-Solomon coding을 사용한다.

  > https://www.cs.cmu.edu/~guyb/realworld/reedsolomon/reed_solomon_codes.html

  - Reed-Solomon code
    - Irving S. Reed와 Gustave Solomon이 소개한 block 기반의 오류 정정 코드이다.
    - Data storage나 network 상에서 오염된 data를 정정하기 위해 사용한다.
    - Reed-Solomon code는 BCH의 하위 집합이며, linear block code이다.
  - Encoder와 decorder로 구성된다.
    - Reed-Solomon encoder는 data를 block 단위로 받은 후 해당 불록에 정정을 위한 여분의 bits를 추가한다.
    - Reed-Solomon decoder는 data를 각 block을 처리하면서 error가 발생했다면, encoder에서 추가한 여분의 bits를 사용하여 정정한다.





## MinIO Client

> https://min.io/docs/minio/linux/reference/minio-mc.html#command-mc

- MinIO Client

  - MinIO는 `mc`라는 command line tool을 제공한다.
    - AWS S3와 호환이 가능하다.
  - 아래와 같이 사용한다.

  ```bash
  $ mc [GLOBALFLAGS] COMMAND
  ```

  - MinIO에 내장되어 있지는 않으므로 별도의 설치가 필요하다.
    - Docker로 설치한 경우 `mc`가 내장되어 있어 설치 없이 사용이 가능하다.



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
  | PUT(write)    | 객체의 버전을 "latest"로 새오 생성하고 unique한 version ID를 할당한다. | Object의 이름이 같으면 덮어쓴다.           |
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





# Single-Node Multi-Drive MinIO

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









# Camel Kafka Connector로 MinIO의 data를 Kafka로 전송하기

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





# Python에서 사용하기

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
  









