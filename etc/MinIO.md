# MinIO

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

