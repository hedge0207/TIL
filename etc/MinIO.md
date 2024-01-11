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

