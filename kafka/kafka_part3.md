# 카프카 시작해보기

## 카프카 설치 및 실행

- JDK 설치

  - 카프카 브로커를 실행하기 위해서는 JDK가 필요하다.

  ```bash
  $ sudo yum install -y java-1.8.0-openjdk-devel.x86_64
  ```

  - 설치 확인

  ```bash
  $ java -version
  ```



- 카프카 설치 및 설정

  - 카프카 브로커 실행을 위해 카프카 바이너리 패키지를 다운로드한다.
    - 카프카 바이너리 패키지에는 자바 소스코드를 컴파일하여 실행하기 위해 준비해 놓은 바이너리 파일들이 들어 있다.

  ```bash
  # 다운
  $ wget https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz
  
  # 압축 풀기
  $ tar xvf kafka_2.12-2.5.0.tgz
  ```

  - 카프카 브로커 힙 메모리 확인
    - 카프카 브로커는 레코드의 내용은 페이지 캐시로 시스템 메모리를 사용하고, 나머지 객체들은 힙 메모리에 저장하여 사용한다는 특징이 있다.
    - 따라서 카프카 브로커를 운영할 때 힙 메모리를 5GB 이상으로 설정하지 않는 것이 일반적이다.
    - 힙 메모리의 기본 설정은 카프카 브로커의 경우 1GB, 주키퍼는 512MB로 설정되어 있다.

  ```sh
  # ~/user-name/kafka_2.12-2.5.0/bin/kafka-start.sh
  
  if [ $# -lt 1 ];
  then
          echo "USAGE: $0 [-daemon] server.properties [--override property=value]*"
          exit 1
  fi
  base_dir=$(dirname $0)
  
  if [ "x$KAFKA_LOG4J_OPTS" = "x" ]; then
      export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:$base_dir/../config/log4j.properties"
  fi
  
  if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
      export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"  # 따로 환경변수로 지정해주지 않았을 경우 1GB로 설정되어 있다.
  fi
  
  EXTRA_ARGS=${EXTRA_ARGS-'-name kafkaServer -loggc'}
  
  COMMAND=$1
  case $COMMAND in
    -daemon)	# deamon 옵션으로 인해 백그라운드에서 실행된다.
      EXTRA_ARGS="-daemon "$EXTRA_ARGS
      shift
      ;;
    *)
      ;;
  esac
  
  exec $base_dir/kafka-run-class.sh $EXTRA_ARGS kafka.Kafka "$@"
  ```

  - 카프카 브로커 힙 메모리 설정
    - `KAFKA_HEAP_OPTS`라는 이름으로 환경변수를 설정해준다.
    - `export`의 경우 터미널 세션이 종료되면 초기화 되므로 bash 쉘이 실행될 때마다 입력된 스크립트를 실행시켜주는 `~/.bashrc` 파일에 export 명령어를 입력해준다.

  ```bash
  # 터미널 세션이 종료되면 초기화 된다.
  $ export KAFKA_HEAP_OPTS="-Xmx400m -Xmx400m"
  
  # ~/.bashrc
  # .bashrc
  
  # Source global definitions
  if [ -f /etc/bashrc ]; then
          . /etc/bashrc
  fi
  
  # User specific aliases and functions
  # 추가해준다.
  export KAFKA_HEAP_OPTS="-Xmx400m -Xmx400m"
  
  # 이후 적용한 내용을 터미널 재실행 없이 다시 실행시키기 위해 아래 명령어를 입력한다.
  $ source ~/.bashrc
  ```
  
  - 카프카 브로커 실행 옵션 지정
    - config 폴더에 있는 `server.properties` 파일에 카프카 브로커가 클러스터 운영에 필요한 옵션들을 지정할 수 있다.

  ```properties
  # ...전략
  
  # The id of the broker. This must be set to a unique integer for each broker.
  # 클러스터 내에서 브로커를 구분하기 위한 id로 클러스터 내에서 고유해야 한다.
  broker.id=0
  
  ############################# Socket Server Settings #############################
  
  #   FORMAT:
  #     listeners = listener_name://host_name:port
  #   EXAMPLE:
  #     listeners = PLAINTEXT://your.host.name:9092
  # 카프카 브로커가 통신을 위해 열어둘 인터페이스 IP, port, 프로토콜을 설정할 수 있다
  # 설정하지 않을 경우 모든 IP, port에서 접속이 가능하다.
  #listeners=PLAINTEXT://:9092
  
  # 카프카 클라이언트 또는 카프카 커맨드 라인 툴에서 접속할 때 사용하는 IP와 port 정보다.
  #advertised.listeners=PLAINTEXT://your.host.name:9092
  
  # SASL_SSL, SASL_PLAIN 보안 설정 시 프로토콜 매핑을 위한 설정
  
  # 네트워크를 통한 처리를 할 때 사용할 네트워크 스레드 개수 설정이다.
  num.network.threads=3
  
  # 카프카 브로커 내부에서 사용할 스레드 개수를 지정할 수 있다.
  num.io.threads=8
  
  # (...)
  
  
  ############################# Log Basics #############################
  
  # 통신을 통해 가져온 데이터를 파일로 저장할 디렉토리 위치이다.
  # 디렉토리가 생성되어 있지 않으면 오류가 발생할 수 있으므로 브로커 실행 전에 디렉토리 생성 여부를 확인한다.
  log.dirs=/tmp/kafka-logs
  
  # The default number of log partitions per topic. More partitions allow greater
  # parallelism for consumption, but this will also result in more files across
  # the brokers.
  # 파티션 개수를 명시하지 않고 토픽을 생성할 때 기본 설정되는 파티션 개수.
  # 파티션 개수가 많아지만 병렬처리 데이터 양이 늘어난다.
  num.partitions=1
  
  # (...)
  
  ############################# Log Retention Policy #############################
  
  # 카프카 브로커가 저장한 파일이 삭제되기까지 걸리는 시간을 설정한다.
  # 가장 작은 단위를 기준으로 하므로 log.retention.hours보다는 log.retention.ms 값을 설정하여 운영하는 것을 추천한다.
  # -1로 설정할 경우 파일은 영원히 삭제되지 않는다.
  log.retention.hours=168
  
  # (...)
  
  # The maximum size of a log segment file. When this size is reached a new log segment will be created.
  # 카프카 브로카가 저장할 파일의 최대 크기를 지정한다.
  # 데이터양이 많아 이 크기를 채우게 되면 새로운 파일이 생성된다.
  log.segment.bytes=1073741824
  
  # The interval at which log segments are checked to see if they can be deleted according
  # to the retention policies
  # 카프카 브로커가 지정한 파일을 삭제하기 위해 체크하는 간격을 지정할 수 있다.
  log.retention.check.interval.ms=300000
  
  ############################# Zookeeper #############################
  
  # Zookeeper connection string (see zookeeper docs for details).
  # This is a comma separated host:port pairs, each corresponding to a zk
  # server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
  # You can also append an optional chroot string to the urls to specify the
  # root directory for all kafka znodes.
  # 카프카 브로커와 연동할 주키퍼의 IP와 port를 지정한다.
  zookeeper.connect=localhost:2181
  
  # Timeout in ms for connecting to zookeeper
  # 주키퍼의 세션 타임아웃 시간을 정한다.
  zookeeper.connection.timeout.ms=18000
  
  # (...)
  ```



- 주키퍼 실행

  - 카프카 바이너리가 포함된 폴더에는 브로커와 같이 실행할 주키퍼가 준비되어 있다.
  - 주키퍼를 상용 환경에서 안전하게 운영하기 위해서는 3대 이상의 서버로 구성하여 사용하지만 실습에서는 동일한 서버에 카프카와 동시에 1대만 실행시켜 사용할 수도 있다.
    - 1대만 실행시키는 주키퍼를 Quick-and-dirty single-node라 하며, 이름에서도 알 수 있지만 비정상적인 운영 방식이다.
    - 실제 운영환경에서는 1대만 실행시켜선 안된다.

  - 실행하기
    - 백그라운드 실행을 위해 `--daemon` 옵션을 준다.
    - 주키퍼 설정 경로인 `config/zookeeper.properties`를 함께 입력한다.

  ```bash
  $ bin/zookeeper-server-start.sh --daemon config/zookeeper.properties
  ```

  - 제대로 실행중인지 확인
    - jps는 JVM 프로세스 상태를 보는 도구이다.
    - `-m` 옵션은 main 메서드에 전달된 인자를, `-v` 옵션은 JVM에 전달된 인자를 함께 확인 가능하다.

  ```bash
  $ jps -vm
  ```



- 카프카 브로커 실행

  - 실행

  ```bash
  $ bin/kafka-server-start.sh -daemon config/server.properties
  ```

  - 확인

  ```bash
  $ jps -m
  ```



- 로컬 컴퓨터에서 카프카와 통신 확인

  - 로컬 컴퓨터에서 원격으로 카프카 브로커로 명령을 내려 정상적으로 통신하는지 확인.
  - kafka-broker-api-versions.sh 명령어를 로컬 컴퓨터에서 사용하려면 로컬 컴퓨터에 카프카 바이너리 패키지를 다운로드 해야한다.

  ```bash
  $ curl https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz --output kafka.tgz
  ```



### Docker로 설치하기

> 아래 내용은 모두 wurstmeister/kafka 이미지를 기준으로 한다.

- 이미지 받기

  - kafka 이미지 받기
    - 예시에서 사용한 `wurstmeister/kafka`외에도 `bitnami/kafka`, `confluentinc/cp-kafka`

  ```bash
  $ docker pull wurstmeister/kafka
  ```

  - zookeeper 이미지 받기

  ```bash
  $ docker pull zookeeper
  ```



- docker-compose.yml 작성

  - `wurstmeister/kafka`이미지를 사용할 경우 `KAFKA_CREATE_TOPICS` 옵션을 통해 컨테이너 생성과 동시에 토픽 생성이 가능하다.
    - `토픽명:partition 개수:replica 개수`
    - 뒷 부분의 `compact`는 clean up policy이며, 다른 옵션도 선택 가능하다.

  ```yaml
  version: '3'
  
  services:
    zookeeper:
      container_name: zookeeper
      image: wurstmeister/zookeeper
      ports:
        - "2181:2181"
  
    kafka:
      image: wurstmeister/kafka
      ports:
        - "9092:9092"
      environment:
        KAFKA_ADVERTISED_HOST_NAME: localhost
        KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
        KAFKA_CREATE_TOPICS: "Topic1:1:3,Topic2:1:1:compact"
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
  ```

  - 설정 변경하기
    - kafka broker의 설정 변경을 위해 `server.properties`를 수정해야 할 경우가 있다.
    - 이 경우 두 가지 선택지가 있는데 docker-compose의 `environment`를 활용하여 설정을 변경하거나, kafka container 내부의 `/opt/kafka/config`폴더(이미지 마다 경로는 다를 수 있다)를 volume 설정해서 직접 수정할 수 있다.
    - `wurstmeister/zookeeper` 이미지의 경우 docker-compose의 `environment`를 활용하는 것을 추천한다.
    - `wurstmeister/zookeeper` 이미지의 경우 두 방법 다 사용할 경우 error가 발생하면서 컨테이너가 실행이 안되므로 주의해야 한다.



- Cluster 구성하기
  - 아래와 같이 docker-compose.yml 파일을 작성한다.
    - 테스트용이므로 zookeeper는 하나만 생성한다.
  
  ```yaml
  version: '3'
  
  services:
  
    test-zoopkeeper:
      container_name: test-zoopkeeper
      image: confluentinc/cp-zookeeper:latest
      environment:
        - ZOOKEEPER_CLIENT_PORT=2181
      networks:
        - test-kafka
      restart: always
  
    test-kafka1:
      image: confluentinc/cp-kafka:7.5.3
      container_name: test-kafka1
      environment:
        - KAFKA_BROKER_ID=1
        - KAFKA_ZOOKEEPER_CONNECT=test-zoopkeeper:2181
        - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        - KAFKA_LISTENERS=INTERNAL://:29092,EXTERNAL://0.0.0.0:9092
        - KAFKA_ADVERTISED_LISTENERS=INTERNAL://:29092,EXTERNAL://127.0.0.1:9097
        - KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=3
      ports:
        - 9097:9092
      depends_on:
        - test-zoopkeeper
      networks:
        - test-kafka
      restart: always
    
    test-kafka2:
      image: confluentinc/cp-kafka:7.5.3
      container_name: test-kafka2
      environment:
        - KAFKA_BROKER_ID=2
        - KAFKA_ZOOKEEPER_CONNECT=test-zoopkeeper:2181
        - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        - KAFKA_LISTENERS=INTERNAL://:29092,EXTERNAL://0.0.0.0:9092
        - KAFKA_ADVERTISED_LISTENERS=INTERNAL://:29092,EXTERNAL://127.0.0.1:9098
        - KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=3
      ports:
        - 9098:9092
      depends_on:
        - test-zoopkeeper
      networks:
        - test-kafka
      restart: always
    
    test-kafka3:
      image: confluentinc/cp-kafka:7.5.3
      container_name: test-kafka3
      environment:
        - KAFKA_BROKER_ID=3
        - KAFKA_ZOOKEEPER_CONNECT=test-zoopkeeper:2181
        - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        - KAFKA_LISTENERS=INTERNAL://:29092,EXTERNAL://0.0.0.0:9092
        - KAFKA_ADVERTISED_LISTENERS=INTERNAL://:29092,EXTERNAL://127.0.0.1:9099
        - KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=3
      ports:
        - 9099:9092
      depends_on:
        - test-zoopkeeper
      networks:
        - test-kafka
      restart: always
  
    test-kafka-ui:
      container_name: test-kafka-ui
      image: provectuslabs/kafka-ui:latest
      ports:
        - 8091:8080
      environment:
        DYNAMIC_CONFIG_ENABLED: true
        KAFKA_CLUSTERS_0_NAME: test
        KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: test-kafka1:29092,test-kafka2:29092,test-kafka3:29092
      networks:
        - test-kafka
      restart: always
  
  
  networks:
    test-kafka:
      driver: bridge
  ```
  
  - 실행한다.
  
  ```bash
  $ docker compose up
  ```
  





### KRaft

- Kafka와 Zookeeper
  - Kafka는 자체적인 분산 coordinating 기능이 없어 Zookeeper에 의존했다.
  - Zookeeper가 Kafka에서 하는 일들은 아래와 같다.
    - 주로 metadata를 관리하는 역할을 한다.
    - leader partition이 내려갔을 때 새로운 leader partition을 선출한다.
    - 클러스터 내의 브로커들의 정보를 관리.
    - Kafka의 topic 정보를 저장한다. 현재 존재하는 토픽과 각 토픽의 파티션 정보, replica들의 수 등을 저장.
    - 각 토픽에 누가 접근하여 message를 읽고 쓸 수 있는지, consumer group의 목록, 각 consumer group에 속한 멤버들이 누구인지와 각 consumer group의 offset등에 대한 정보를 담은 엑세스 제어 목록(Access Control Lists, ACLs)을 관리.
    - Kafka의 데이터에 접근하는 클라이언트에 관한 정보 관리.
  - 그러나 Apache Kafka 3.5부터 Zookeeper가 deprecate됐고, 4.0부터는 Zookeeper 사용이 불가능해질 예정이다.



- KRaft(Kafka Raft)

  - Zookeeper에 대한 의존성을 제거하기 위해 소개된 합의 protocol이다.
  - KRaft의 등장 배경
    - 기존에 Kafka는 모든 topic과 parition에 대한 metadata를 zookeeper에서 읽어야했으며, 이 때 병목 현상이 발생할 가능성이 있다.
    - 또한 Kafka broker에서 가지고 있는 metadata와 Zookeeper의 metadata가 일치하지 않는 상황도 발생할 수 있다.
    - 그리고 Zookeeper와 Kafka는 완전히 다른 application임에도 Kafka를 사용하기 위해선 Zookeeper가 필수였기에 관리상의 어려움이 있었다.
    - Zookeeper를 걷어냄으로써 Kafka의 전체 구조를 훨씬 간결하게 만들 수 있다.
    - Zoopkeeper와 달리 KRaft는 Kafka의 일부이기 때문에 Kafka라는 단일 시스템만으로 완전한 운영이 가능하다.

  - KRaft controller node는 Kafka metadata log를 관리하기 위한 Raft quorum을 구성한다.
    - 이 log에는 cluster의 metadata에 관한 변경 사항이 저장된다.
    - 기존에 Zookeeper에서 관리하던 topic, parition, ISRs, configuration 등의 모든 정보가 이 log에 저장된다.
    - Metadata log의 leader를 active controller라고 부르며, active controller는 broker에서 생성된 모든 RPC를 처리한다.
    - Follower controller들은 active controller에 쓰인 데이터를 복제하여 active controller에 문제가 생길 경우에 대비한다.
    - 주기적으로 controller들은 metadata의 snapshot을 disk에 저장한다.
    - Zookeeper를 사용할 때와 마찬가지로 KRaft 역시 과반수의 node가 실행되어야 서비스가 가능하다.
    - 예를 들어 3개의 node로 구성할 경우 둘 이상의 node가 실행중이어야 서비스가 유지된다.
  - Zookeeper와 함께 사용할 때의 controller
    - Zookeeper를 사용할 경우 Kafka cluster 중 하나의 broker가 controller 역할을 하게 된다.
    - Controller는 parition의 leader를 선출하는 역할을 하며, leader 선출 정보를 모든 broker에게 전파하고 Zookeeper에 leader 정보를 기록하는 역할을 한다.
    - Controller의 선출은 Zookeeper의 임시 노드를 통해 이루어진다.
    - 임시 노드에 가장 먼저 연결에 성공한 broker가 controller가 되고, 다른 broker들은 해당 임시 노드에 이미 controller가 있다는 사실을 통해 Kafka cluster 내에 controller가 있다는 것을 인지하게 된다.
    - 이를 통해 한 cluster에 하나의 controller만 있도록 보장된다.
  - KRaft를 사용할 때의 controller
    - Zookeeper 모드에서 1개였던 controller가 3개로 늘어나고, 이 중 하나의 controller가 active controller, 즉 leader 역할이 된다.
    - Leader 역할을 하는 controller가 write 역할을 한다.
  - KRaft를 사용하더라도 broker와 KRaft를 분리된 서버에 배치하는 것이 강력히 권장된다.
    - 즉 broker와 별개로 KRaft 서버를 할당하여 운영하는 것이 권장된다.
    - 이렇게 구성함으로써 controller와 broker를 분리하여 높은 가용성과 안정성을 확보할 수 있다.
    - 그러나, 서버의 리소스가 한정적인 경우에는 어쩔 수 없이 KRaft와 broker를 동시에 운영할 수도 있다.



- KRaft mode로 실행하기

  > https://docs.confluent.io/platform/current/installation/docker/config-reference.html#required-ak-configurations-for-kraft-mode

  - KRaft mode로 실행하기 위해 반드시 설정해야 하는 것들
    - `KAFKA_PROCESS_ROLES`: `controller`,`broker`, `broker,controller`중 하나의 값으로 설정한다.
    - `KAFKA_NODE_ID`: Broker의 node ID를 설정한다.
    - `KAFKA_CONTROLLER_QUORUM_VOTERS`: 정족에 참여하는 voter들의 list를 comma로 구분하여 설정한다(`{KAFKA_NODE_ID}@{host}:{port}` 형식으로 설정).
    - `KAFKA_CONTROLLER_LISTENER_NAMES`: Controller가 사용할 listener들의 목록을 comma로 구분하여 설정하며, 첫 번째 listener만 broker에 의해 사용된다.
    - `CLUSTER_ID `: 고유한 cluster ID를 설정한다.

  - 단일 broker로 실행하기
    - 단일 broker로 실행할 때는 `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR` 환경 변수를 1로 줘야 한다.

  ```yaml
  version: '3'
  
  services:
    KRaft-Kafka:
      container_name: KRaft-Kafka
      image: confluentinc/cp-kafka:7.5.3
      ports:
        - "9097:9097"
      environment:
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        KAFKA_ADVERTISED_LISTENERS: INTERNAL://:29092,EXTERNAL://127.0.0.1:9097
        KAFKA_LISTENERS: INTERNAL://:29092,CONTROLLER://:29093,EXTERNAL://0.0.0.0:9097
        KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
        KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
        
        # KRaft에서 필수적인 설정들
        CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
        KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
        KAFKA_PROCESS_ROLES: 'broker,controller'
        KAFKA_NODE_ID: 1
        KAFKA_CONTROLLER_QUORUM_VOTERS: 1@KRaft-Kafka:29093
  ```

  - Cluster로 구성하기

  ```yaml
  version: '3.8'
  
  services:
    kafka-1:
      container_name: kafka-1
      image: confluentinc/cp-kafka:7.5.3
      ports:
        - "9097:9092"
      environment:
        KAFKA_NODE_ID: 1
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        KAFKA_LISTENERS: INTERNAL://:29092,CONTROLLER://:29093,EXTERNAL://0.0.0.0:9092
        KAFKA_ADVERTISED_LISTENERS: INTERNAL://:29092,EXTERNAL://127.0.0.1:9097
        KAFKA_PROCESS_ROLES: 'broker,controller'
        KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka-1:29093,2@kafka-2:29093,3@kafka-3:29093
        KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
        KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
        CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
  
    kafka-2:
      container_name: kafka-2
      image: confluentinc/cp-kafka:7.5.3
      ports:
        - "9098:9092"
      environment:
        KAFKA_NODE_ID: 2
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        KAFKA_LISTENERS: INTERNAL://:29092,CONTROLLER://kafka-2:29093,EXTERNAL://0.0.0.0:9092
        KAFKA_ADVERTISED_LISTENERS: INTERNAL://:29092,EXTERNAL://127.0.0.1:9098
        KAFKA_PROCESS_ROLES: 'broker,controller'
        KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka-1:29093,2@kafka-2:29093,3@kafka-3:29093
        KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
        KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
        CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
  
    kafka-3:
      container_name: kafka-3
      image: confluentinc/cp-kafka:7.5.3
      ports:
        - "9099:9092"
      environment:
        KAFKA_NODE_ID: 3
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        KAFKA_LISTENERS: INTERNAL://:29092,CONTROLLER://kafka-3:29093,EXTERNAL://0.0.0.0:9092
        KAFKA_ADVERTISED_LISTENERS: INTERNAL://:29092,EXTERNAL://127.0.0.1:9099
        KAFKA_PROCESS_ROLES: 'broker,controller'
        KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka-1:29093,2@kafka-2:29093,3@kafka-3:29093
        KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
        KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
        CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
  ```









## 주요 옵션

### server.properties

- `message.max.bytes`
  - 단일 요청의 최대 크기
    - `max.request.size`가 producer와 관련된 설정이라면, 이는 broker와 관련된 설정이다.
  - 기본값은 1048576 bytes(1MB).



- Kafka Listeners

  > https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/
  >
  > https://www.confluent.io/blog/kafka-listeners-explained/?utm_source=github&utm_medium=rmoff&utm_campaign=ty.community.con.rmoff-listeners&utm_term=rmoff-devx

  - Kafka는 크게 두 개의 통신이 가능해야 한다.
    - Cluster 내의 broker들 사이의 통신
    - Cluster 외부의 client(consumer, producer)들과의 통신

  - Client에서 Kafka cluster에 접근하기 위해 설정하는 정보는 cluster의 broker들에 대한 metadata를 받아오기 위한 정보이지, 실제 data에 접근하기 위한 정보가 아니다.
    - 예를 들어 아래와 같이 Python client(producer)에 Kafka에 대한 접속 정보를 설정했다고 생각해보자.
    - 이 때 client에 설정한 `10.11.22.33:9092`라는 접속 정보는 실제 broker에 event를 읽고 쓰기 위한 접속 정보가 아니라, Kafka cluster에 속한 broker들의 metadata를 받아오기 위한 접속 정보이다.
    - 실제 data를 받아오기 위한 host 혹은 IP는 아래에서 설정한 접속 정보를 통해 첫 connection이 이루어지면 broker가 client로 보내준다.

  ```python
  from kafka import KafkaProducer
  
  producer = KafkaProducer(bootstrap_servers=['10.11.22.33:9092'])
  ```

    - Kafka broker들은 여러 개의 listener를 가질 수 있으며, 각 listener들은 아래 요소들의 조합으로 구성된다.
      - Protocol
      - Host/IP
      - Port

    - Listener에 대한 설정은 아래와 같은 것들이 있다(아래 이름들은 Docker의 환경 변수로 설정할 때 사용하는 것으로, 괄호 안에는 server.properties에 설정할 때의 이름이다).
      - `KAFKA_LISTENERS`(`listeners`): Kafka의 host/IP, port를 어떤 listener와 binding할지 설정한다(기본값은 0.0.0.0).
      - `KAFKA_ADVERTISED_LISTENERS`(`advertised.listeners`): listener들의 host/IP와 port를 설정하며, 첫 connection이후 client에 반환되는 metadata에 이 정보가 포함된다(즉, 결국 여기 설정된 listener들을 사용하여 client가 실제 event를 읽고 쓴다).
      - `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`(`listener.security.protocol.map`): listener에서 사용할 security protocol을 `listener_name:protocol` 형식으로 설정한다.
      - `KAFKA_INTER_BROKER_LISTENER_NAME`(`inter.broker.listener.name`): Kafka cluster 내의 broker들 사이의 통신에 사용할 listener를 설정한다.

  ```yaml
  # LISTENER_BOB을 kafka0:29092에 binding하고, LISTENER_FRED를 localhost:9092에 binding한다.
  KAFKA_LISTENERS: LISTENER_BOB://kafka0:29092,LISTENER_FRED://localhost:9092
  
  # Client는 아래 listener들을 통해 event를 읽고 쓴다.
  KAFKA_ADVERTISED_LISTENERS: LISTENER_BOB://kafka0:29092,LISTENER_FRED://localhost:9092
  
  # 각 listener의 security protocol을 listener_name:protocol 형식으로 설정한다.
  KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_BOB:PLAINTEXT,LISTENER_FRED:PLAINTEXT
  
  # Broker들 사이의 통신에 사용할 listener를 설정한다.
  KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_BOB
  ```

    - Client와 broker 사이의 첫 통신 시에 broker가 어떤 listener에 대한 정보를 반환할 지는 client가 어떤 port로 첫 통신을 시도했는지에 따라 달라진다.
      - 예를 들어 위와 같이 설정했을 때, client가 `kafka0:9092`로 접속 정보를 설정(`LISTENER_FRED`)했다면, broker는 `localhost:9092`를 client에게 반환한다.
      - 반면에 client가 `kafka0:29092`로 접속 정보를 설정(`LISTENER_BOB`)했다면, broker는 `kafka0:29092`를 client에게 반환한다.

  - Host를 설정하지 않을 경우 default network interface에 binding된다.
    - 예를 들어 아래와 같이 설정했다고 가정해보자.
    - `INTERNAL` listener의 경우 `INTERNAL://:29092`와 같이 host를 설정하지 않았다.
    - 이럴 경우 default network interface에 binding된다.
    - 아래 예시의 경우 Docker로 실행했으므로 docker network상에서 docker container가 부여 받은 IP에 binding된다.

  ```yaml
  version: '3'
  
  services:
    Kafka:
      # ...
      environment:
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
        KAFKA_LISTENERS: INTERNAL://:29092,CONTROLLER://:29093,EXTERNAL://0.0.0.0:9092
        KAFKA_ADVERTISED_LISTENERS: INTERNAL://:29092,EXTERNAL://127.0.0.1:9092
  ```



- `advertised.listeners` 설정시 주의사항
  - 상기했듯, client가 최초 실행 될 때 broker로 부터 metadata를 받아온다.
    - 이 metadata에는 `advertised.listeners`가 담겨있으며, client는 이 주소를 통해 broker에 요청을 보낸다.
  - 만약 client와 broker가 각기 다른 machine에서 실행중인 상황에서 `advertised.listeners` 값이 localhost로 설정되어 있다면, 문제가 생길 수 있다.
    - A machine에서 실행중인 client가 B machine에서 실행 중인 broker에서 metadata를 요청한다.
    - Broker는 `advertised.listeners` 값인 localhost를 반환한다.
    - Client는 broker로 부터 받은 metadata를 읽어 localhost로 요청을 보낸다.
    - 즉, broker는 B machine에서 실행중임에도 A machine으로 요청을 보내게 되고, A machine에는 Kafka가 실행중이 아니므로 요청은 실패하게 된다.
  - 혹은 같은 client는 Docker container 밖에서, broker는 docker container로 실행된다면, 이 역시 문제가 될 수 있다.
    - 예를 들어 IP가 11.22.33.44인 server에서 `KAFKA_ADVERTISED_LISTENERS`의 값을 `PLAINTEXT://my-kafka:29092`와 같이 설정하고, 29092 port를 pulbish하여 container를 실행했다고 가정해보자.
    - 이 때 container 외부에 있는 client는 broker container가 속한 docker network에 접근할 수 없으므로 server의 IP를 사용하여 `11.22.33.44:29092`로 요청을 보낸다.
    - 이 경우 bootstrap은 성공하여 broker로부터 metadata는 받아오며, metadata에는 `KAFKA_ADVERTISED_LISTENERS`에 설정한 `my-kafka:29092`가 담겨서 온다.
    - `my-kafka:29092`의 host에 해당하는 `my-kafka`는 docker network 내에서만 사용 가능하므로, docker network에 속하지 않은 client는 해당 listner로 요청을 보낼 수 없게 된다.



- Docker를 사용하여 Kafka cluster를 구성할 때의 listener 설정

  - 상황
    - Kafka cluster에 속하는 모든 broker는 같은 docker network를 사용한다.
    - 일부 client는 Kafka cluster와 동일한 docker network를 사용하지만 일부 client는 docker network를 사용하지 않는다.
    - 단, docker network를 사용하지 않는 client라 하더라도 container와 같은 host machine에서 실행된다.
  - 아래와 같이 docker compose file을 작성한다.

  ```yaml
    kafka0:
      image: "confluentinc/cp-enterprise-kafka:5.2.1"
      ports:
        - '9092:9092'
        - '29094:29094'
      depends_on:
        - zookeeper
      environment:
        KAFKA_BROKER_ID: 0
        KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
        KAFKA_LISTENERS: LISTENER_BOB://kafka0:29092,LISTENER_FRED://kafka0:9092,LISTENER_ALICE://kafka0:29094
        KAFKA_ADVERTISED_LISTENERS: LISTENER_BOB://kafka0:29092,LISTENER_FRED://localhost:9092,LISTENER_ALICE://never-gonna-give-you-up:29094
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_BOB:PLAINTEXT,LISTENER_FRED:PLAINTEXT,LISTENER_ALICE:PLAINTEXT
        KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_BOB
  ```

  - Docker network를 사용하는 client
    - 이 client들은 `LISTENER_BOB` listener(kafka0:29092)를 이용하여 Kafka와 통신하면 된다.
    - 첫 통신에서 이들은 event를 읽고 쓰기 위한 접속 정보인 `kafka0`라는 hostname을 받게 된다.
  - Docker network를 사용하지 않는 client
    - 이 client들은 `LISTENER_FRED` listener(localhost:9092)를 이용하여 Kafka와 통신하면 된다.
    - 9092 port가 Docker container에 의해 expose되었기 때문에 localhost:9092를 통해 통신이 가능하다.
    - Client가 broker와 처음으로 통신할 때 localhost라는 hostname을 받게 된다.



### producer.properties

- `max.request.size`
  - Producer가 broker로 한 번 요청을 보낼 때 요청의 최대 크기
  - 기본값은 1048576 bytes(1MB).





## Kafka Command Line Tool

> 전체 tool에 대한 설명은 [공식 문서](https://kafka.apache.org/081/documentation.html#basic_ops_leader_balancing) 참고

- 카프카 커맨드 라인 툴
  - 카프카 브로커 운영에 필요한 다양한 명령을 내릴 수 있다.
  - 카프카 클라이언트 애플리케이션을 운영할 때 토픽이나 파티션 개수 변경과 같은 명령을 실행해야 하는 경우가 자주 발생하므로, 카프카 커맨드 라인 툴과 각 툴별 옵션에 대해서 알고 있어야 한다.
  - `wurstmeister/kafka`이미지의 경우 `/opt/kafka/bin`에서 찾을 수 있다.



- kafka-configs.sh

  - Kafka의 각종 설정을 확인 및 수정할 수 있다.
    - 다양한 옵션이 있으므로 `--help` 옵션을 통해 확인해보고 사용하면 된다.
  - 예시
    - broker들의 설정을 확인하는 명령어이다.

  ```bash
  $ kafka-configs.sh --bootstrap-server 127.0.0.1:9092 --describe --entity-type brokers --all
  ```




- kafka-topics.sh
  - 토픽과 관련된 명령을 수행하는 커맨드라인.
  - 토픽 생성
    - `--create` 명령을 사용한다.
    - `--replication-factor`는 복제 파티션의 개수를 지정하는 것인데 1이면 복제 파티션을 사용하지 않는다는 의미이다.
  
  ```bash
  $ kafka-topics \
  > --create \
  > --bootstrap-server 127.0.0.1:9092 \		# 카프카 호스트와 포트 지정
  > --partitions 3 \							# 파티션 개수 지정
  > --replication-factor 1 \					# 복제 파티션 개수 지정
  > --config retention.ms=172800000 \			# 추가적인 설정
  > --topic hello.kafka						# 토픽 이름 지정
  ```
  
  - 토픽 리스트 조회
    - `--list` 명령을 사용한다.
    - `--exclude-internal` 옵션을 추가하면 내부 관리를 위한 인터널 토픽을 제외하고 보여준다.
  
  ```bash
  $ kafka-topics --list --bootstrap-server 127.0.0.1:9092
  ```
  
  - 특정 토픽 상세 조회
    - `--describe` 명령을 사용한다.
    - `Partition`은 파티션 번호, `Leader`는 해당 파티션의 리더 파티션이 위치한 브로커의 번호, `Replicas`는 해당 파티션의 복제 파티션이 위치한 브로커의 번호를 의미한다.
  
  ```bash
  $ kafka-topics --describe --bootstrap-server 127.0.0.1:9092 --topic hello.kafka
  
  Topic: hello-kafka      PartitionCount: 3       ReplicationFactor: 1    Configs: segment.bytes=1073741824,retention.ms=172800000
  Topic: hello-kafka      Partition: 0    Leader: 1001    Replicas: 1001  Isr: 1001
  Topic: hello-kafka      Partition: 1    Leader: 1001    Replicas: 1001  Isr: 1001
  Topic: hello-kafka      Partition: 2    Leader: 1001    Replicas: 1001  Isr: 1001
  ```
  
  - 토픽 옵션 수정
    - `kafka-topics.sh` 또는  `kafka-config.sh`에서 `--alert`옵션을 사용해서 수정해야 한다.
    - 각기 수정할 수 있는 옵션이 다르므로 확인 후 사용해야 한다.
    - `kafka-configs.sh`의 `--add-config`는 수정하려는 옵션이 이미 존재하면 추가하고, 없으면 수정한다는 의미이다.
  
  ```bash
  # 파티션 개수 변경
  $ kafka-topics --alter --bootstrap-server 127.0.0.1:9092 --topic hello.kafka --partitions 4
  
  # 리텐션 기간 수정
  $ kafka-configs --alter --add-config retention.ms=86400000 \
  --bootstrap-server 127.0.0.1:9092 \
  --entity-type topics \
  --entity-name hello.kafka
  ```
  
  - 토픽 삭제
  
  ```bash
  $ kafka-topics --delete --bootstrap-server 127.0.0.1:9092 --topic <삭제할 topic 이름>
  ```
  



- kafka-console.producer.sh

  - 프로듀서와 관련된 명령을 수행하는 커맨드라인
    - 이 커맨드라인으로 전송되는 레코드 값은 UTF-8을 기반으로 Byte로 변환된다.
    - 즉 스트링만 전송이 가능하다.
  - 메시지 값만 보내기
    - 메시지 입력 후 엔터를 누르면 별 다른 메시지 없이 전송된다.

  ```bash
  $ kafka-console-producer --bootstrap-server 127.0.0.1:9092 --topic hello.kafka
  >hello
  >world
  >1
  >True
  >[1,2,3]
  ```

  - 메시지 키와 값 같이 보내기
    - `key.separator`를 설정하지 않을 경우 기본 값은 `\t`dlek.

  ```bash
  $ kafka-console-producer --bootstrap-server 127.0.0.1:9092 \
  > --topic hello.kafka \
  > --property "parse.key=true" \	# 키를 보낸다는 것을 알려주고
  > --property "key.separator=:"	# 키워 값의 구분자를 :로 설정
  >my_key:my_value
  ```



- kafka-console.consumer.sh

  - 컨슈머와 관련된 명령을 수행하는 커맨드라인
  - 토픽에 저장된 데이터 확인
    - `--from-beginning` 옵션은 토픽에 저장된 가장 처음 데이터부터 출력한다.

  ```bash
  $ kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic kafka.test --from-beginning
  ```

  - 메시지 키와 값을 함께 확인
    - `--property` 옵션을 사용한다.
    - `--group` 옵션을 통해 새로운 컨슈머 그룹을 생성하였는데, 이 컨슈머 그룹을 통해 토픽에서 가져온 메시지에 대하 커밋을 진행한다.

  ```bash
  $ kafka-console-consumer --bootstrap-server 127.0.0.1:9092 \
  --topic kafka.test \
  --property print.key=true \
  --property key.separator="-" \
  --group test-group \	# 새로운 컨슈머 그룹 생성.
  --from-beginning
  ```



- kafka-consumer-groups.sh

  - Cosnuemr group과 관련된 명령을 수행하는 커맨드라인
  - Cosnuemr group 목록 확인
    - `--list` 명령으로 실행한다.

  ```bash
  $ kafka-consumer-groups --list --bootstrap-server 127.0.0.1:9092 
  ```

  - Cosnuemr group 상세 정보 확인
    -  특정 컨슈머 그룹의 상세 정보를 확인하기 위해 쓰인다.

  ```bash
  $ kafka-consumer-groups --describe --bootstrap-server 127.0.0.1:9092 --group <group>
  ```

  - Cosnuemr group 삭제
    - 특정 topic에 대해서만 삭제하는 것은 불가능하다.
  
  ```bash
  $ kafka-consumer-groups --bootstrap-server localhost:29093 --delete --group <group>
  ```
  
  - 응답

    - TOPIC과 PARTITION은 조회한 컨슈머 그룹이 구독하고 있는 토픽과 할당된 파티션을 나타낸다.
  
    - CURRENT-OFFSET은 각 파티션 별 최신 오프셋이 몇 번인지를 나타낸다(0번 파티션은 4이므로 4개의 데이터가 들어갔다는 것을 알 수 있다).
    - LOG-END-OFFSET은 컨슈머가 몇 번 오프셋까지 커밋했는지를 알 수 있다.
    - LAG는 컨슈머 그룹이 파티션의 데이터를 가져가는 데 얼마나 지연이 발생하는지를 나타내는데, `CURRENT-OFFSET - LOG-END-OFFSET` 으로 계산한다.
    - HOST는 컨슈머가 동작하는 host명을 나타낸다.
  
  ```bash
  GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG     CONSUMER-ID     HOST            CLIENT-ID
  test-group      kafka.test      0          4               4               0       -               -               -
  test-group      kafka.test      1          8               8               0       -               -               -
  test-group      kafka.test      2          1               1               0       -               -               -
  test-group      kafka.test      3          4               4               0       -               -               -
  ```
  
  - Consumer group의 offset 초기화
  
    - `--dry-run`: offset reset시에 예상 결과를 보여준다.
    - `--execute`: offset을 초기화한다.
  
  
  ```bash
  # 예상 결과 출력
  $ kafka-consumer-groups --bootstrap-server <host:port> --group <group> --topic <topic> --reset-offsets --to-earliest --dry-run
  
  # offset 초기화
  $ kafka-consumer-groups --bootstrap-server <host:port> --group <group> --topic <topic> --reset-offsets --to-earliest --execute
  ```



- kafka-verifiable-producer/consumer.sh

  - 카프카 클러스터 설치가 완료된 이후에 토픽에 데이터를 전송하여 간단한 네트워크 통신 테스트를 할 때 유용하게 사용이 가능하다.
  - 메시지 보내기
    - 최초 실행 시점이 `startup_complete` 메시지와 함께 출력된다.
    - 메시지별로 보낸 시간과 메시지 키, 메시지 값, 토픽, 저장된 파티션, 저장된 오프셋 번호가 출력된다.
    - `--max-message`에서 지정해준 만큼 전송이 완료되면 통계값이 출력된다.

  ```bash
  $ kafka-verifiable-producer --bootstrap-server 127.0.0.1:9092 --max-message 10 --topic kafka.test
  {"timestamp":1633505763219,"name":"startup_complete"}
  {"timestamp":1633505763571,"name":"producer_send_success","key":null,"value":"0","partition":0,"topic":"kafka.test","offset":4}
  {"timestamp":1633505763574,"name":"producer_send_success","key":null,"value":"1","partition":0,"topic":"kafka.test","offset":5}
  {"timestamp":1633505763574,"name":"producer_send_success","key":null,"value":"2","partition":0,"topic":"kafka.test","offset":6}
  ...
  {"timestamp":1633505763598,"name":"tool_data","sent":10,"acked":10,"target_throughput":-1,"avg_throughput":26.17801047120419}
  ```

  - 메시지 확인하기

  ```bash
  $ kafka-verifiable-consumer --bootstrap-server 127.0.0.1:9092  --topic kafka.test --group-id test-group
  ```



- kafka-delete-records.sh

  - 적재된 토픽의 데이터를 삭제하는 커맨드라인
    - 삭제하고자 하는 데이터에 대한 정보를 파일로 저장해서 사용해야 한다.

  - 파일 생성
    - test라는 토픽의 0번 파티션에 저장된 데이터 중 0부터 50번째 offset까지의 데이터를 삭제하려면 아래와 같이 파일을 작성한다.

  ```bash
  $ vi delete-data.json
  {"partitions":[{"topic":"test", "partition": 0, "offset":50}]}, "version":1}
  ```

  - 삭제

  ```bash
  $ kafka-delete-records --bootstrap-server 127.0.0.1:9092 --offset-json-file delete-data.json
  ```



- Topic 내의 message 개수 가져오기

  - 결과는 `<topic>:<partition_num>:<message_num>` 형태로 출력된다.

  ```bash
  $ kafka-run-class kafka.tools.GetOffsetShell --broker-list <HOST1:PORT,HOST2:PORT> --topic <topic>
  ```



- `kafka-reassign-partitions.sh`

  - Partition을 재분배한다.
    - Parition 설정을 명시한 JSON 파일을 인자로 받아, 명시된 대로 parition을 재설정한다.

  - 재할당을 진행할 topic들을 명시하여 아래와 같은 JSON 파일을 작성한다.

  ```json
  // tmp.json
  {
      "version":1,
      "topics": [
          {"topic":"foo"},
          {"topic":"bar"}
      ]
  }
  ```

  - `kafka-reassign-partitions.sh`를 통해 재할당 후보들을 받아온다.
    - `--generate` 옵션을 통해 재할당에 관한 제안을 받을 수 있다.
    - `--topics-to-move-json-file`에 위에서 작성한 JSON파일 경로를 입력한다.
    - `--broker-list` 옵션에 재할당하고자 하는 broker id를 입력한다.

  ```json
  // bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --topics-to-move-json-file tmp.json --broker-list "5,6" --generate 
  
  // 현재 할당 상황
  Current partition replica assignment
  
  {"version":1,
   "partitions":[{"topic":"foo","partition":2,"replicas":[1,2]},
                 {"topic":"foo","partition":0,"replicas":[3,4]},
                 {"topic":"bar","partition":2,"replicas":[1,2]},
                 {"topic":"bar","partition":0,"replicas":[3,4]},
                 {"topic":"foo","partition":1,"replicas":[2,3]},
                 {"topic":"bar","partition":1,"replicas":[2,3]}]
  }
  
  // 재할당 제안
  Proposed partition reassignment configuration
  
  {"version":1,
   "partitions":[{"topic":"foo","partition":2,"replicas":[5,6]},
                 {"topic":"foo","partition":0,"replicas":[5,6]},
                 {"topic":"bar","partition":2,"replicas":[5,6]},
                 {"topic":"bar","partition":0,"replicas":[5,6]},
                 {"topic":"foo","partition":1,"replicas":[5,6]},
                 {"topic":"bar","partition":1,"replicas":[5,6]}]
  }
  ```

  - 위에서 제안 받은 내용을 JSON 파일로 작성한다.
    - 전까지의 과정은 필수적인 과정은 아니며, 바로 현재 단계부터 시작해도 된다.

  ```json
  // proposed.json
  {"version":1,
   "partitions":[{"topic":"foo","partition":2,"replicas":[5,6]},
                 {"topic":"foo","partition":0,"replicas":[5,6]},
                 {"topic":"bar","partition":2,"replicas":[5,6]},
                 {"topic":"bar","partition":0,"replicas":[5,6]},
                 {"topic":"foo","partition":1,"replicas":[5,6]},
                 {"topic":"bar","partition":1,"replicas":[5,6]}]
  }
  ```

  - 재할당을 실행한다.
    - `--reassignment-json-file` 옵션에 위에서 작성한 JSON 파일 경로를 입력한다.
    - `--execute` 옵션을 주면 재할당 결과를 미리 볼 수 있다.

  ```json
  // bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --reassignment-json-file proposed.json --execute
  Current partition replica assignment
  
  {"version":1,
   "partitions":[{"topic":"foo1","partition":2,"replicas":[1,2]},
                 {"topic":"foo1","partition":0,"replicas":[3,4]},
                 {"topic":"foo2","partition":2,"replicas":[1,2]},
                 {"topic":"foo2","partition":0,"replicas":[3,4]},
                 {"topic":"foo1","partition":1,"replicas":[2,3]},
                 {"topic":"foo2","partition":1,"replicas":[2,3]}]
  }
  
  Save this to use as the --reassignment-json-file option during rollback
  Successfully started reassignment of partitions
  {"version":1,
   "partitions":[{"topic":"foo1","partition":2,"replicas":[5,6]},
                 {"topic":"foo1","partition":0,"replicas":[5,6]},
                 {"topic":"foo2","partition":2,"replicas":[5,6]},
                 {"topic":"foo2","partition":0,"replicas":[5,6]},
                 {"topic":"foo1","partition":1,"replicas":[5,6]},
                 {"topic":"foo2","partition":1,"replicas":[5,6]}]
  }
  ```

  - 재할당 과정 확인하기
    - `--verify` 옵션을 주면 재할당 진행 과정을 확인할 수 있다.

  ```json
  // bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --reassignment-json-file proposed.json --verify
  Status of partition reassignment:
  Reassignment of partition [foo1,0] completed successfully
  Reassignment of partition [foo1,1] is in progress
  Reassignment of partition [foo1,2] is in progress
  Reassignment of partition [foo2,0] completed successfully
  Reassignment of partition [foo2,1] completed successfully 
  Reassignment of partition [foo2,2] completed successfully 
  ```

  





# 카프카 확장

## Kafka Streams

- Topic에 적재된 데이터를 실시간으로 변환할 수 있게 해주는 library
  - Streams DSL 또는  processor API 라는 2 가지 방법으로 개발이 가능하다.
  - JMV에서만 실행이 가능하다.
  - Python에도 아래와 같은 라이브러리가 존재하기는 하지만 현재 관리가 되지 않고 있다.
    - [robinhood/faust](https://github.com/robinhood/faust)
    - [wintincode/winton-kafka-streams](https://github.com/wintoncode/winton-kafka-streams)



- 토폴로지(topology)
  - 2개 이상의 노드들과 선으로 이루어진 집합.
  - 카프카 스트림즈에서는 토폴로지를 이루는 하나의 노드를 프로세서, 노드 사이를 연결한 선을 스트림이라고 부른다.
  - 스트림은 토픽의 데이터를 뜻하는데, 프로듀서와 컨슈머에서 활용했던 레코드와 동일하다.
  - 프로세서
    - 소스 프로세서, 스트림 프로세서, 싱크 프로세서 3가지가 있다.
    - 소스 프로세서는 데이터를 처리하기 위해 최초로 선언하는 노드로, 하나 이상의 토픽에서 데이터를 가져오는 역할을 한다.
    - 스트림 프로세서는 다른 프로세서가 반환한 데이터를 처리하는 역할을 한다.
    - 싱크 프로세서는 데이터를 특정 카프카 토픽으로 저장하는 역할을 하며, 스트림즈로 처리된 데이터의 최종 종착지다.



- Streams DSL
  - 레코드의 흐름을 추상화한 개념인 KStream, GLobalKTable, KTable에 대해 알아야 한다.
    - 세 개념 모두 Streams DSL에서만 사용되는 개념이다.
  - KStream
    - 레코드의 흐름을 표현한 것으로 메시지 키와 값으로 구성되어 있다.
    - 컨슈머로 토픽을 구독하는 것과 유사하다고 볼 수 있다.
  - KTable
    - 메시지를 키를 기준으로 묶어서 사용한다.
    - KStream은 토픽의 모든 레코드를 조회할 수 있지만 KTable은 유니크한 메시지 키를 기준으로 가장 최신 레코드를 사용한다.
    - KTable로 데이터를 조회하면 메시지 키를 기준으로 가장 최신에 추가된 레코드의 데이터가 출력된다.
  - GlobalKTable
    - Ktable과 동일하게 메시지 키를 기준으로 묶어서 사용된다.
    - 그러나 KTable로 선언된 토픽은 1개 파티션이 1개 태스크에 할당되어 사용되고, GlobalKTable로 선언된 토픽은 모든 파티션 데이터가 각 테스크에 할당되어 사용된다는 차이점이 있다.





## Kafka Burrow

> https://github.com/linkedin/Burrow

- Consumer lag을 모니터링하는 애플리케이션이다.
  - Linkedin에서 개발했다.
  - Go로 개발되었다.



- 왜 필요한가?
  - Consumer lag은 Kafka의 주요 성능 지표 중 하나다.
  - Kafka의 command line tool로도 각 consumer group 별 lag을 조회가 가능하다.
    - 그러나 클러스터 내의 모든 broker들의 lag을 통합적으로 확인할 수 있는 방법이 없다.
    - 또한 단순히 consumer lag 수치만 확인할 수 있을 뿐 이에 대한 판단은 직접 내려야한다.
    - 또한 consumer lag 수치 만으로는 정확한 판단을 내리기 힘들 수도 있다.
  - Kafka Burrow는 클러스터 내의 모든 consumer group에 대한 lag monitoring이 가능하다.
  - Kafka Burrow는 consumer lag의 수치만 보고 상태를 판단하지 않고 일정한 rule에 따라 상태를 판단한다.



- Status
  - `NOTFOUND`: Cluster 내에서 consumer group을 찾을 수 없음
  - `OK`: Group 또는 partition이 정상적인 상태
  - `WARN`: Group 또는 partition에 주의를 기울여야 하는 상태.
  - `ERR`: Group에 문제가 생긴 상태
  - `STOP`: Partition이 멈춘 상태
  - `STALL`: Partition이 감속중인 상태.



- Consumer lag evaluation rules

  - Burrow는 sliding window algorithm을 통해 lag를 평가한다.
    - sliding window란 고정된 크기의 윈도우가 이동하면서 윈도우 내에 있는 데이터를 사용하는 알고리즘이다.
    - 예를 들어 [1,2,3,4,5] 라는 배열이 있고 size가 3이라면, [1,2,3], [2,3,4], [3,4,5]와 같이 윈도우를 이동시켜 해당 윈도우 내에 있는 값만을 사용하는 방식이다.
  - Evaluation rules
    - 만일 window 내의 어떤 lag 값이 0이라면, `OK`라고 판단한다.
    - 만일 consumer의 committed offset이 window의 변화에 따라 변하지 않고, lag가 고정되어 있거나 증가한다면, `ERR`이라고 판단하고, partition은 `STALLED` 상태가 된다.
    - 만일 consumer의 committed offset이 window의 변화에 따라 증가하지만, lag에 변화가 없거나 증가한다면, `WARN`이라고 판단한다.
    - 만일 consumer offset의 가장 최근 시간과 현재시간 차이가 가장 최근 시간과 가장 오래된 오프셋 시간보다  크다면, consumer를 `ERR` 상태로 판단하고, partition은 `STOPPED` 상태로 판단한다. 그러나 consumer의 offset과 broker의 현재 offset이 동일하다면, `ERR`로 판단하지 않는다.
    - lag가 -1이라면 `OK`로 판단한다. 이는 Burrow가 이제 막 실행되어, broker의 offset을 아직 받아오지 못한 상태이다.
  - 예시1
    - offset은 commit 된 offset을 뜻한다.
    - timestamp는 임의의 시점 부터 경과한 시간을 의미한다.
    - Window 중 lag가 0인 값을 가지는 window가 있으므로 첫 번째 rule에 따라 아래는 `OK`로 판단한다.

  |           | W1   | W2   | W3    | W4    | W5    | W6    | W7    | W8    | W9    | W10   |
  | --------- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
  | offset    | 10   | 20   | 30    | 40    | 50    | 60    | 70    | 80    | 90    | 100   |
  | lag       | 0    | 0    | 0     | 0     | 0     | 0     | 1     | 3     | 5     | 5     |
  | timestamp | T    | T+60 | T+120 | T+180 | T+240 | T+300 | T+360 | T+420 | T+480 | T+540 |

  - 예시2
    - consumer의 committed offset이 시간이 지나도 변화하지 않고, lag은 증가하고 있으므로, 두 번째 rule에 따라 partition은 `STALLED` 상태가 되고, consumer의 status는 `ERR`이라고 판단한다. 

  |           | W1   | W2   | W3    | W4    | W5    | W6    | W7    | W8    | W9    | W10   |
  | --------- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
  | offset    | 10   | 10   | 10    | 10    | 10    | 10    | 10    | 10    | 10    | 10    |
  | lag       | 1    | 1    | 1     | 1     | 1     | 2     | 2     | 2     | 3     | 3     |
  | timestamp | T    | T+60 | T+120 | T+180 | T+240 | T+300 | T+360 | T+420 | T+480 | T+540 |

  - 예시3
    - committed offset은 시간이 흐름에 따라 증가하지만, lag 역시 증가하므로 세 번째 rule에 따라 `WARN`으로 판단한다.

  |           | W1   | W2   | W3    | W4    | W5    | W6    | W7    | W8    | W9    | W10   |
  | --------- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
  | offset    | 10   | 20   | 30    | 40    | 50    | 60    | 70    | 80    | 90    | 100   |
  | lag       | 1    | 1    | 1     | 1     | 1     | 2     | 2     | 2     | 3     | 3     |
  | timestamp | T    | T+60 | T+120 | T+180 | T+240 | T+300 | T+360 | T+420 | T+480 | T+540 |

  - 예시4
    - 만일 아래와 같은 window가 존재하고 status evaluation을 하는 시점이 T+1200이라면, 네 번째 rule에 따라 partition은 `STOPPED`, consumer는 `ERR` 상태가 된다.
    - 첫 offset(W1)과 마지막 offset(W10)의 시간 차이가 540이고, 현재와 마지막 offset의 시간 차이는 660이다.

  |           | W1   | W2   | W3    | W4    | W5    | W6    | W7    | W8    | W9    | W10   |
  | --------- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
  | offset    | 10   | 20   | 30    | 40    | 50    | 60    | 70    | 80    | 90    | 100   |
  | lag       | 5    | 3    | 5     | 2     | 1     | 1     | 2     | 1     | 4     | 6     |
  | timestamp | T    | T+60 | T+120 | T+180 | T+240 | T+300 | T+360 | T+420 | T+480 | T+540 |



- 설치하기

  - 공식 github에서 repo를 clone 받는다.

  ```bash
  $ git clone https://github.com/linkedin/Burrow.git
  ```

  - `./docker-config/burrow.toml`파일을 상황에 맞게 수정한다.

  ```toml
  [zookeeper]
  servers=[ "<zookeeper_host>:<zookeeper_port>" ]
  timeout=6
  root-path="/burrow"
  
  [client-profile.profile]
  kafka-version="2.0.0"
  client-id="docker-client"
  
  [cluster.local]
  client-profile="profile"
  class-name="kafka"
  servers=[ "<kafka_host>:<kafka_port>" ]
  topic-refresh=60
  offset-refresh=30
  groups-reaper-refresh=30
  
  [consumer.local]
  class-name="kafka"
  cluster="local"
  servers=[ "<kafka_host>:<kafka_port>" ]
  group-denylist="^(console-consumer-|python-kafka-consumer-).*$"
  group-allowlist=""
  
  [consumer.local_zk]
  class-name="kafka_zk"
  cluster="local"
  servers=[ "<zookeeper_host>:<zookeeper_port>" ]
  zookeeper-path="/local"
  zookeeper-timeout=30
  group-denylist="^(console-consumer-|python-kafka-consumer-).*$"
  group-allowlist=""
  
  [httpserver.default]
  address=":8000"
  ```

  - `./dockerfile`을 빌드한다.

  ```bash
  $ docker build -t <image_name>:<tag> .
  ```

  - docker-compose.yml을 작성하고 실행한다.

  ```yaml
  version: '3'
  
  services:
    zookeeper:
      container_name: my-zookeeper
      image: wurstmeister/zookeeper
      ports:
        - "2188:2181"
  
    kafka:
      image: wurstmeister/kafka
      container_name: my-kafka
      ports:
        - "9092:9092"
      environment:
        KAFKA_ADVERTISED_HOST_NAME: <kafka_host>
        KAFKA_ZOOKEEPER_CONNECT: <zookeeper_host>:<zookeeper_port>
        KAFKA_LOG_DIRS: "/kafka/kafka-logs"
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
  
    burrow:
      image: <위에서 빌드한 이미지>
      container_name: my-burrow
      volumes:
        - <burrow.toml 파일이 있는 폴더의 경로>:/etc/burrow/
      ports:
        - 8000:8000
      depends_on:
        - zookeeper
        - kafka
      restart: always
  ```



- http endpoint

  > https://github.com/linkedin/Burrow/wiki/HTTP-Endpoint#request-endpoints

  - consumer lag 확인하기
    - `<cluster>`에는 `burrow.toml`에서 작성한 cluster name(위 예시의 경우 local)을 입력한다.

  ```bash
  $ curl <burrow_host>:<burrow_port>/v3/kafka/<cluster>/consumer/<consumer_group_name>/lag
  ```

  - 응답

  ```json
  {
          "error": false,
          "message": "consumer status returned",
          "status": {
                  "cluster": "local",
                  "group": "MyConsumerGroup",
                  "status": "OK",
                  "complete": 1,
                  "partitions": [
                          {
                                  "topic": "test",
                                  "partition": 0,
                                  "owner": "/<kafka_host>",
                                  "client_id": "aiokafka-0.7.2",
                                  "status": "OK",
                                  "start": {
                                          "offset": 343122,
                                          "timestamp": 1660809543330,
                                          "observedAt": 1660809543000,
                                          "lag": 57026
                                  },
                                  "end": {
                                          "offset": 345657,
                                          "timestamp": 1660809588336,
                                          "observedAt": 1660809588000,
                                          "lag": 87957
                                  },
                                  "current_lag": 87957,
                                  "complete": 1
                          },
                          // ...
                  ],
                  "partition_count": 3,
                  "maxlag": {
                          "topic": "test",
                          "partition": 0,
                          "owner": "/<kafka_host>",
                          "client_id": "aiokafka-0.7.2",
                          "status": "OK",
                          "start": {
                                  "offset": 343122,
                                  "timestamp": 1660809543330,
                                  "observedAt": 1660809543000,
                                  "lag": 57026
                          },
                          "end": {
                                  "offset": 345657,
                                  "timestamp": 1660809588336,
                                  "observedAt": 1660809588000,
                                  "lag": 87957
                          },
                          "current_lag": 87957,
                          "complete": 1
                  },
                  "totallag": 262813
          },
          "request": {
                  "url": "/v3/kafka/local/consumer/MyConsumerGroup/lag",
                  "host": "2r34235325"
          }
  }
  ```





## Kafka-UI

> https://github.com/provectus/kafka-ui
>
> https://docs.kafka-ui.provectus.io/overview/readme

- UI for Apache Kafka
  - Kafka를 UI를 통해 관리할 수 있게 해주는 open source wev UI이다.



- 설치 및 실행

  - Docker image를 pull 받는다.

  ```bash
  $ docker pull provectuslabs/kafka-ui
  ```

  - Docker compose file을 작성한다.
    - Kafka-ui를 통해 관리하고자 하는 kafka cluster를 configuration file이나 environment등을 사용하여 미리 설정할 수 있다.
    - 아래의 경우 environment를 통해 설정했으나, 미리 설정하지 않더라도 kafka-ui를 먼저 실행하고 UI에서 설정하는 것도 가능하다.
    - Bootstrap server를 설정할 때는 Kafka의 `advertised.listeners`에 설정한 값을 입력해야한다.

  ```yaml
  version: '3.2'
  
  
  services:
    my-zookeeper:
      container_name: my-zookeeper
      image: confluentinc/cp-zookeeper:latest
      environment:
        - ZOOKEEPER_CLIENT_PORT=2181
      networks:
        - kafka
  
    my-kafka:
      image: confluentinc/cp-kafka:latest
      container_name: my-kafka
      environment:
        - KAFKA_BROKER_ID=1
        - KAFKA_ZOOKEEPER_CONNECT=my-zookeeper:2181
        - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://my-kafka:29093
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
      ports:
        - 9092:9092
      depends_on:
        - my-zookeeper
      networks:
        - kafka
      restart: always
    
    my-kafka-ui:
      container_name: my-kafka-ui
      image: provectuslabs/kafka-ui:latest
      ports:
        - 8080:8080
      environment:
        DYNAMIC_CONFIG_ENABLED: true
        KAFKA_CLUSTERS_0_NAME: test
        KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: my-kafka:29093
      networks:
        - kafka
  
  networks:
    kafka:
      driver: bridge
  ```



## etc.

- 카프카 미러메이커2
  - 서로 다른 두 개의 카프카 클러스터 간에 토픽을 복제하는 애플리케이션
  - 필요할 경우 추후 추가
    - 아파치 카프카 애플리케이션 프로그래밍(p.188)

