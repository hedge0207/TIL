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
  
  # Uncomment the following line if you don't like systemctl's auto-paging feature:
  # export SYSTEMD_PAGER=
  
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
  
  # The address the socket server listens on. It will get the value returned from 
  # java.net.InetAddress.getCanonicalHostName() if not configured.
  #   FORMAT:
  #     listeners = listener_name://host_name:port
  #   EXAMPLE:
  #     listeners = PLAINTEXT://your.host.name:9092
  # 카프카 브로커가 통신을 위해 열어둘 인터페이스 IP, port, 프로토콜을 설정할 수 있다
  # 설정하지 않을 경우 모든 IP, port에서 접속이 가능하다.
  #listeners=PLAINTEXT://:9092
  
  # Hostname and port the broker will advertise to producers and consumers. If not set, 
  # it uses the value for "listeners" if configured.  Otherwise, it will use the value
  # returned from java.net.InetAddress.getCanonicalHostName().
  # 카프카 클라이언트 또는 카프카 커맨드 라인 툴에서 접속할 때 사용하는 IP와 port 정보다.
  #advertised.listeners=PLAINTEXT://your.host.name:9092
  
  # Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
  # SASL_SSL, SASL_PLAIN 보안 설정 시 프로토콜 매핑을 위한 설정
  #listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
  
  # The number of threads that the server uses for receiving requests from the network and sending responses to the network
  # 네트워크를 통한 처리를 할 때 사용할 네트워크 스레드 개수 설정이다.
  num.network.threads=3
  
  # The number of threads that the server uses for processing requests, which may include disk I/O
  # 카프카 브로커 내부에서 사용할 스레드 개수를 지정할 수 있다.
  num.io.threads=8
  
  # (...)
  
  
  ############################# Log Basics #############################
  
  # A comma separated list of directories under which to store log files
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
  
  # The following configurations control the disposal of log segments. The policy can
  # be set to delete segments after a period of time, or after a given size has accumulated.
  # A segment will be deleted whenever *either* of these criteria are met. Deletion always happens
  # from the end of the log.
  
  # The minimum age of a log file to be eligible for deletion due to age
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



- Topic 생성하기

  ```bash
  $ docker exec -t <컨테이너 명> kafka-topics.sh --bootstrap-server <host 명>:9092 --create --topic <토픽 이름>
  ```



- cluster 구성하기
  - `KAFKA_ZOOKEEPER_CONNECT` 정보만 동일하게 주면 cluster가 구성된다.



## 주요 옵션

### server.properties

- `message.max.bytes`
  - 단일 요청의 최대 크기
    - `max.request.size`가 producer와 관련된 설정이라면, 이는 broker와 관련된 설정이다.
  - 기본값은 1048576 bytes(1MB).



- Kafka Listener

  > https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/
  >
  > https://www.confluent.io/blog/kafka-listeners-explained/?utm_source=github&utm_medium=rmoff&utm_campaign=ty.community.con.rmoff-listeners&utm_term=rmoff-devx
  
  - Client(producer와 consumer)가 시작될 때 특정 topic에 대한 leader partition이 어느 broker에 속했는지를 확인하기 위해 모든 broker에 대한 metadata를 요청한다.
    - Metadata에는 leader partition을 가지고 있는 broker의 endpoint에 대한 정보가 포함되어 있어 client들은 이를 활용하여 leader partition을 가진 broker에 연결한다.
    - 주의할 점은 metadata를 받아올 때 사용하는 broker의 접속 정보와 응답으로 받아와 message를 read/write하기 위해 사용하는 metadata에 담긴 broker의 접속 정보가 별개라는 점이다.
  - 결국 client가 partition에서 message를 read/write하기 위해서는 아래 두 단계를 거쳐야 한다.
    - Client 최초 실행시 broker에 연결하여 metadata를 받아오는 단계.
    - 이전 단계에서 broker로부터 받아온 metadata를 가지고 broker에 연결하는 단계.
  - 첫 단계에서 broker가 반환하는 metadata에는 `advertised.listeners`에서 설정한 값이 담겨있다.
    - Client가 topic에서 message를 read/write하기 위해서는 `advertised.listeners`에 설정된 listner로 요청을 보내야 한다.
  - Listner는 아래의 조합으로 구성된다.
    - Host/IP
    - Port
    - Protocol



- Listner 관련 설정들

  - `listeners`(`KAFKA_LISTENERS `)
    - Broker 내부에서 사용할 주소를 설정한다.
    - 콤마로 구분된 listner들의 목록을 설정한다.
    - Listner와 host/IP + port를 `:`를 통해 bind한다(e.g. `LISTNER_FOO://localhost:29092`).
    
  - `advertised.listeners`(`KAFKA_ADVERTISED_LISTENERS `)
    - Broker 외부로 노출할 주소를 설정한다.
    - 콤마로 구분된 listner들의 목록을 설정한다.
    - Listner와 host/IP + port를 `:`를 통해 bind한다.
    - 이 정보가 client 최초 실행시에 broker가 반환하는 metadata에 담기게 된다.
    - 설정하지 않을 경우 `listeners`에 설정한 값이 기본으로 설정된다.
  
  - `listener.security.protocol.map`(`KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`)
    - 각 listner에서 사용할 security protocol을 key-value 쌍으로 설정한다.
    - Key가 listner가 되고, value가 security protocol이 된다.
  - `inter.broker.listener.name`(`KAFKA_INTER_BROKER_LISTENER_NAME`)
    - 같은 cluster에 속한 Kafka broker들 간의 통신에 사용되는 listner를 설정한다.
  
  ```yaml
  KAFKA_LISTENERS: LISTENER_FOO://kafka0:29092,LISTENER_BAR://localhost:9092
  KAFKA_ADVERTISED_LISTENERS: LISTENER_FOO://kafka0:29092,LISTENER_BAR://localhost:9092
  KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_FOO:PLAINTEXT,LISTENER_BAR:PLAINTEXT
  KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_FOO
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





### producer.properties

- `max.request.size`
  - Producer가 broker로 한 번 요청을 보낼 때 요청의 최대 크기
  - 기본값은 1048576 bytes(1MB).





## 카프카 커맨드 라인 툴

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

  - 컨슈머 그룹과 관련된 명령을 수행하는 커맨드라인
  - 컨슈머 그룹 목록 확인
    - `--list` 명령으로 실행한다.

  ```bash
  $ kafka-consumer-groups --list --bootstrap-server 127.0.0.1:9092 
  ```

  - 컨슈머 그룹 상세 정보 확인
    -  특정 컨슈머 그룹의 상세 정보를 확인하기 위해 쓰인다.

  ```bash
  $ kafka-consumer-groups --describe --bootstrap-server 127.0.0.1:9092 --group test-group
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
  
  - Consumer group의  offset  초기화
  
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






## Python에서 사용하기

- Python에서 Kafka에 접근할 수 있게 해주는 라이브러리에는 아래와 같은 것들이 있다.
  - confluent-kafka-python
    - 성능이 가장 좋다.
    - C로 만든 라이브러리를 호출하여 사용하는 방식이므로 별도의 설치과정이 존재한다.
  - kafka-python
    - pure python이기에 confluent-kafka-python에 비해 속도는 느리다.
    - 사용법이 직관적이고 간결하다.
  - aiokafka
    - Benchmark 상으로 성능이 가장 좋다.
    - kafka-python 기반으로 만들어졌다.



- 설치하기(kafka-python)

  ```bash
  $ pip install kafka-python
  ```



- Producer 구현

  ```python
  from kafka import KafkaProducer
  from json import dumps
  import time
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  
  data = {'Hello':'World!'}
  producer.send('test',value=data)
  producer.flush()
  ```

  - Producer 옵션

    > 상세는 https://kafka-python.readthedocs.io/en/1.1.0/apidoc/KafkaProducer.html#kafkaproducer 참고

    - `bootstrap_servers`: 브로커들을 리스트 형태로 입력한다.
    - `acks`: 메시지를 보낸 후 요청 완료 전 승인 수, 손실과 성능의 트레이드 오프로, 낮을수록 성능은 좋고 손실이 커진다.
    - `buffer_memory`: 카프카에 데이터를 보내기전 잠시 대기할 수 있는 메모리(byte)
    - `compression_type`: 데이터를 압축해서 보낼 수 있다(None, gzip, snappy, lz4 중 선택).
    - `retries`: 오류로 전송 실패한 데이터를 다시 보낼지 여부
    - `batch_size`: 여러 데이터를 배치로 보내는 것을 시도한다.
    - `linger_ms`: 배치 형태 작업을 위해 기다리는 시간 조정, 배치 사이즈에 도달하면 옵션과 관계 없이 전송, 배치 사이즈에 도달하지 않아도 제한 시간 도달 시 메시지 전송
    - `max_request_size`: 한 번에 보낼 수 있는 메시지 바이트 사이즈(기본 값은 1MB, 1048576 Bytes)
  
  - Partitioner
  
    - kafka-python과, kafka-python 기반의 aiokafka 패키지의 기본 partitioner는 round-robin, sticky partitioner가 아닌 random이다.
    - key가 있을 경우 kafka의 murmur2를 python으로 포팅하여 사용한다.
  
  ```python
  @classmethod
  def __call__(cls, key, all_partitions, available):
      """
      Get the partition corresponding to key
      :param key: partitioning key
      :param all_partitions: list of all partitions sorted by partition ID
      :param available: list of available partitions in no particular order
      :return: one of the values from all_partitions or available
      """
      if key is None:
          if available:
              return random.choice(available)
          return random.choice(all_partitions)
  
      idx = murmur2(key)
      idx &= 0x7fffffff
      idx %= len(all_partitions)
      return all_partitions[idx]
  ```



- Consumer 구현

  ```python
  from kafka import KafkaConsumer
  from json import loads
  
  
  consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', 
                          enable_auto_commit=True, group_id="my-group", value_deserializer=lambda x: loads(x.decode('utf-8')),
                          consumer_timeout_ms=1000)
  
  for message in consumer:
      print(message.topic)		# test
      print(message.partition)	# 0
      print(message.offset)		# 0
      print(message.key)			# None
      print(message.value)		# {'Hello': 'World!'}
  ```

  - Consumer 옵션
    - `bootstrap_servers`: 브로커들을 리스트 형태로 입력한다.
    - `auto_offset_reset`: earliest(가장 초기 오프셋값), latest(가장 마지막 오프셋값), none(이전 오프셋값을 찾지 못할 경우 에러) 중 하나를 입력한다.
    - `enable_auto_commit`: 주기적으로 offset을 auto commit
    - `group_id`: 컨슈머 그룹을 식별하기 위한 용도
    - `value_deserializer`: producer에서 value를 serializer를 한 경우 사용.
    - `consumer_timeout_ms`: 이 설정을 넣지 않으면 데이터가 없어도 오랜기간 connection한 상태가 된다. 데이터가 없을 때 빠르게 종료시키려면 timeout 설정을 넣는다.



- Kafka Consumer Multiprocessing

  - Broker에서 이벤트를 받아와서 각 프로세스들이 처리하게 하는 방법
    - `multiprocessing`의 `Process`와 `Queue`를 사용한다.

  - main.py
    - 이벤트를 처리하고자 하는 프로세스+1개의 프로세스를 생성한다.
    - 하나의 프로세스는 `Queue`에 지속적으로 이벤트를 추가한다.
    - 나머지 프로세스는 `Queue`를 공유하면서 이벤트를 받아와서 처리한다.

  ```python
  from multiprocessing import Process, Queue
  import consumer
  from kafka import KafkaConsumer
  import json
  
  
  def deserializer_value(value):
      try:
          return json.loads(value)
      except Exception as e:
          print(e)
  
  
  kconsumer = KafkaConsumer('test',
                          bootstrap_servers='127.0.0.1:9092',
                          group_id='test-group',
                          value_deserializer=deserializer_value,
                          auto_offset_reset='earliest',
                          max_poll_records=1,
                          max_poll_interval_ms=3600000,
                          enable_auto_commit=True)
  
  
  if __name__ == '__main__':
      queue = Queue()
      processes=[]
      def put_items(queue):
          # queue에 이벤트를 추가한다.
          for msg in kconsumer:
              queue.put(msg)
      
      for i in range(4):
          if i == 0:
              # Queue에 이벤트를 추가할 프로세스
              processes.append(Process(target=put_items, args=[queue]))	# queue를 인자로 넘긴다.
          else:
              # 실제 이벤트를 처리할 프로세스들
              processes.append(Process(target=consumer.consume_message, args=[queue]))  # queue를 인자로 넘긴다.
      
      for process in processes:
          process.start()
      for process in processes:
          process.join()
  ```

  - consumer.py

  ```python
  import os
  
  def consume_message(queue):
      while True:
          # 이벤트를 받아와서
          msg = queue.get()
         	# PID 확인
          print('PID:', os.getpid())
          # 필요한 처리를 수행한다.
          print(msg.value.get('message'))
          print("-"*50)
  ```

  - producer.py

  ```python
  import json
  from kafka import KafkaProducer
  
  
  producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                          max_block_ms=1000 * 60 * 10,
                          buffer_memory=104857600 * 2,
                          max_request_size=104857600)
  
  msg_list = ['Hello', 'World', 'Good', 'Morning']
  for msg in msg_list:
      value = {
          'message':msg
      }
      producer.send(topic='test', value=value)
      producer.flush()
  ```



- Kafka Consumer에 topic과 partition을 지정하는 방법

  - partition을 2개 이상 생성해줘야 한다.
    - 만일 docker-compose로 kafka를 띄운다면 `environment`의 `KAFKA_CREATE_TOPICS`에 `토픽명:partition 개수:replica 개수` 형태로 파티션 개수를 설정해준다.
    - 만일 kafka를 띄울 때 partition 생성을 하지 않았다면 아래와 같이 파티션을 생성해준다.

  ```python
  from kafka import KafkaAdminClient
  from kafka.admin import NewPartitions
  
  bootstrap_servers='127.0.0.1:9092'
  topic = 'test'
  
  # {topic명:NewPartition 인스턴스} 형태의 딕셔너리를 생셩한다.
  topic_partitions = {}
  topic_partitions[topic] = NewPartitions(total_count=3)
  
  admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
  # create_partitions 메서드에 위에서 생성한 딕셔너리를 인자로 넘겨 파티션을 생성한다.
  admin_client.create_partitions(topic_partitions)
  ```

  - producer
    - producer 쪽에서는 특별히 해줄 것이 없다.
    - 만일 특정 partition에 메시지를 보내고 싶다면 `send` 메서드에 `partition=파티션 번호` 인자를 추가해주면 된다.

  ```python
  import json
  from kafka import KafkaProducer
  
  
  producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                          max_block_ms=1000 * 60 * 10,
                          buffer_memory=104857600 * 2,
                          max_request_size=104857600)
  
  msg_list = ['Hello', 'World', 'Good']
  topic = 'test'
  for msg in msg_list:
      value = {
          'message':msg
      }
      producer.send(topic=topic, value=value)
      producer.flush()
  ```

  - consumer
    - `assign` 메서드를 통해 토픽과 파티션을 할당한다.

  ```python
  import json
  
  from kafka import KafkaAdminClient, KafkaConsumer
  from kafka.structs import TopicPartition
  from kafka.admin import NewPartitions
  
  
  
  def deserializer_value(value):
      try:
          return json.loads(value)
      except Exception as e:
          print(e)
  
  bootstrap_servers='127.0.0.1:9092',
  topic = 'test'
  
  # enable_auto_commit(default True) 값을 아래와 같이 False로 주면, 수동으로 커밋을 해줘야 한다.
  consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                          group_id='test-group', 
                          value_deserializer=deserializer_value, 
                          auto_offset_reset='earliest', 
                          enable_auto_commit=False)
  # topic과 partition을 할당
  consumer.assign([TopicPartition(topic, 1)])
  
  for msg in consumer:
      print(msg.value.get('message'))
      partitions = consumer.assignment()
      print(partitions)
      # enable_auto_commit을 False로 줬기에 아래와 같이 수동으로 commit을 해준다.
      consumer.commit()
  ```



- Kafka python topic 생성하기

  ```python
  from kafka import KafkaAdminClient
  from kafka.admin import NewTopic
  
  
  kafka_admin_client = KafkaAdminClient(bootstrap_servers="127.0.0.1:9092")
  topic = NewTopic("my-topic", 3, 1)
  kafka_admin_client.create_topics([topic])
  ```



- future

  - 모종의 이유로 producer에서 partition으로 message를 전송하지 못하더라도 error가 발생하지는 않는다.
    - message의 누락은 발생하는데, error는 발생하지 않으므로 누락이 생겨도 모를 수가 있다.
    - 따라서 누락이 생겼을 경우 이를 캐치해서 예외처리를 해 줄 필요가 있다.
  - Future는 `KafKaProducer.send` 메서드의 결과 반환되는 값으로 message의 적재가 성공했는지, 실패했는지 알 수 있다.
    - `Future.succeeded`, `Future.failed`를 통해 성공했는지 실패했는지를 알 수 있다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  
  time.sleep(0.1)
  print(future.succeeded())	# True
  print(future.failed())		# False
  
  producer.flush()
  ```

  - 주의할 점은 적재가 완료될 때까지는 성공/실패 여부를 알 수 없다.
    - 위 예시에서 `time.sleep`을 통해 잠시 멈춘 것은 적재가 완료되기를 기다리기 위해서다.
    - 아래는 `Future.succeeded`, `Future.failed` 메서드의 실제 코드로, `self.is_done`이 True여야, 즉 적재가 완료 되어야 True를 반환한다.

  ```python
  class Future(object):
      # (...)
      def succeeded(self):
          return self.is_done and not bool(self.exception)
  
      def failed(self):
          return self.is_done and bool(self.exception)
  ```

  - `FutureRecordMetadata.get` 메서드는 성공시 message의 상세 정보를 반환하다.
    - `FutureRecordMetadata.get` 메서드의 경우, `timeout`으로 설정한 시간 동안 적재가 완료될 때까지 기다리기 때문에,  `time.sleep`을 주지 않아도 된다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localgost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  try:
  	print(future.get(timeout=10))
  except Exception as e:
      print(e)
  print(future.succeeded())		# True
  print(future.failed())			# False
  
  producer.flush()
  ```

  - `FutureRecordMetadata.get`를 실행했을 때, 적재가 실패한 경우에는 exception을 raise한다.
    - `max_request_size`를 1로 줬으므로 적재에 실패하게 되고, exception을 raise한다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localgost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'), \
                          max_request_size=1)
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  try:
  	print(future.get(timeout=10))
  except Exception as e:
      print(e)
  print(future.succeeded())		# False
  print(future.failed())			# True
  
  producer.flush()
  ```

  - 아래와 같이 callback 형식으로도 사용이 가능하다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  def on_send_success(record_metadata):
      print(record_metadata.topic)
      print(record_metadata.partition)
      print(record_metadata.offset)
  
  def on_send_error(excp):
      print(excp)
      # handle exception
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  producer.send(topic,value={"foo":"bar"}).add_callback(on_send_success).add_errback(on_send_error)
  producer.flush()
  ```





# 카프카 확장

## Kafka Connect

- Kafka Connect
  - 프로듀서, 컨슈머 애플리케이션을 만드는 것은 좋은 방법이지만 반복적인 파이프라인 생성 작업이 있을 때는 매번 프로듀서, 컨슈머 애플리케이션을 개발하고 배포, 운영하는 것이 비효율적일 수 있다.
  - 커넥트는 특정 작업 형태를 템플릿으로 만들어 놓은 connector를 실행함으로써 반복 작업을 줄일 수 있다.
  - Connector
    - Pipeline 생성시 자주 반복되는 값들을 파라미터로 받는 connector를 코드로 작성하면 이후에 pipeline을 실행할 때는 코드를 작성할 필요가 없다.
    - Connector에는 프로듀서 역할을 하는 source connector와 컨슈머 역할을 하는 sink connector가 있다.
    - [컨플루언트 허브](https://www.confluent.io/hub)에서 다른 사람이 제작한 connector를 가져와서 사용할 수도 있고, 직접 제작하여 사용할 수도 있다.



- Docker로 설치하기

  - Python script로 producer를 생성하여 broker로 메시지를 전송하고,  elasticsearch sink plugin를 사용하여 메시지를 elasticsearch에 색인하는 connect를 만들어보기
  - Docker hub에서 image 받기
    - Docker Hub에 kafka connect 이미지가 올라가 있지만 elasticsearch sink plugin을 설치한 custom connect를 사용할 것이므로 아래와 같이 base image를 받는다.
  
  ```bash
  $ docker pull confluentinc/cp-server-connect-base
  ```
  
    - Elasticsearch sink connector 받기
  
      > https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch
  
      - 위 링크에서 zip 파일을 다운 받을 수 있다.
      - 혹은 지금 다운 받지 않고 dockerfile을 build할 때 설치하는 것도 가능하다.
  
  
    - docker image 생성하기
  
      - 아래와 같이 dockerfile을 작성하고 image를 build한다.
  
  ```dockerfile
  # 위에서 zip 파일을 다운 받은 경우
  FROM confluentinc/cp-server-connect-base:latest
  COPY /<zip 파일 경로>/confluentinc-kafka-connect-elasticsearch-14.0.0.zip /tmp/confluentinc-kafka-connect-elasticsearch-14.0.0.zip
  RUN confluent-hub install --no-prompt /tmp/confluentinc-kafka-connect-elasticsearch-14.0.0.zip
  
  
  # 다운 받지 않은 경우
  FROM confluentinc/cp-server-connect-base:latest
  RUN confluent-hub install confluentinc/kafka-connect-elasticsearch:latest
  ```
  
    - docker-compose.yml 파일 작성하기
  
      > 전체 설정은 https://github.com/confluentinc/cp-demo의 docker-compose.yml 파일에서 확인 가능하다.
  
  ```yaml
  connect:
      image: <위에서 build한 image명>
      container_name: connect
      restart: always
      ports:
        - 8083:8083
      environment:
        CONNECT_BOOTSTRAP_SERVERS: <kafka broker의 url list>
        CONNECT_GROUP_ID: "connect-cluster"
  
        CONNECT_CONFIG_STORAGE_TOPIC: connect-configs
        CONNECT_OFFSET_STORAGE_TOPIC: connect-offsets
        CONNECT_STATUS_STORAGE_TOPIC: connect-statuses
  
        CONNECT_REPLICATION_FACTOR: 1
        CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR: 1
        CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR: 1
        CONNECT_STATUS_STORAGE_REPLICATION_FACTOR: 1
  
        CONNECT_KEY_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
        CONNECT_VALUE_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
        CONNECT_INTERNAL_KEY_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
        CONNECT_INTERNAL_VALUE_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
        CONNECT_KEY_CONVERTER_SCHEMAS_ENABLE: "true"
        CONNECT_value_CONVERTER_SCHEMAS_ENABLE: "true"
        CONNECT_REST_ADVERTISED_HOST_NAME: "localhost"
        CONNECT_PLUGIN_PATH: "/usr/share/java,/usr/share/confluent-hub-components"
  ```



  - Sink connect 생성하기

    - Connect container 실행 후 connect API를 이용하여 elasticsearch sink connector를 생성한다.
      - Connector가 생성되면 `connect-<connector-name>` 형식으로 consumer group이 생성된다.
      - `topic.index.map` 옵션은 11 버전부터 삭제 됐다.
    
    ```bash
    curl -XPOST <kafka connect url>/connectors -H "Content-Type:application/json" -d '{
        "name":"elasticsearch-sink",
        "config":{
            "connector.class":"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            # 실행할 task(consumer)의 개수를 입력한다.
            "tasks.max":"1",
            # message를 받아올 topic을 입력한다.
            "topics":"<topic 명>",
            "connection.url":"<elasticsearch url>",
            "type.name":"log",
            "key.ignore":"true",
            "schema.ignore":"false",
            "value.converter.schemas.enable": "false"
        }
    }'
    ```
    
    - 잘 생성 되었는지 확인한다.
    
    ```bash
    $ curl <kafka connect url>/connectors/elasticsearch-sink/status
    ```
    
    - 요청 format
        - 위에서 `JsonConverter`를 사용한다고 명시했으므로 반드시 아래의 형식으로 보내야한다.
        - 최상단에 `schema`와 `payload` 필드가 위치해야하며, `schema`에는 이름 그대로 schema에 대한 정보가, `payload`에는 색인하고자 하는 문서를 입력하면 된다.
    
    ```json
    // 예시
    {
        "schema":{
            "type":"struct",
            "fields":[
                {
                    "type":"string",
                    "optional":"false",
                    "field":"name"
                },
                {
                    "type":"int64",
                    "optional":"false",
                    "field":"age"
                }
            ]
        },
        "payload":{"name":"John", "age":22}
    }
    ```
    
      - Python script 작성하기
        - 아래 script를 실행하면 message가 broker로 전송되고, elasticsearch sink connector가 해당 메시지를 가져가서 es에 적재한다.
    
    ```python
    from kafka import KafkaProducer
    from json import dumps
    
    TOPIC = "test"
    producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=["kafka_broker_url"], \
                            value_serializer=lambda x: dumps(x).encode('utf-8'))
    try:
    	msg = {
    		"schema":{
                    "type":"struct",
                    "fields":[
                        {
                            "type":"string",
                            "optional":"false",
                            "field":"name"
                        },
                        {
                            "type":"int64",
                            "optional":"false",
                            "field":"age"
                        }
                    ]
                },
                "payload":{"name":"John", "age":22}
            }
        producer.send(TOPIC, value=msg)
        producer.flush()
    except Exception as e:
        print(e)
    ```





- Kafka Connect API

  | method   | endpoint                                              | description                                     |
  | -------- | ----------------------------------------------------- | ----------------------------------------------- |
  | `GET`    | /                                                     | 실행 중인 connect 정보 확인                     |
  | `GET`    | /connectors                                           | 실행 중인 connector 목록 확인                   |
  | `POST`   | /connectors                                           | 새로운 connector 생성                           |
  | `GET`    | /connectors/<connector 이름>                          | 실행 중인 connector 정보 확인                   |
  | `GET`    | /connectors/<connector 이름>/config                   | 실행 중인 connector 설정값 확인                 |
  | `PUT`    | /connectors/<connector 이름>/config                   | 실행 중인 connector의 설정값 변경               |
  | `GET`    | /connectors/<connector 이름>/status                   | 실행 중인 connector 상태 확인                   |
  | `POST`   | /connectors/<connector 이름>/restart                  | 실행 중인 connector 재시작                      |
  | `PUT`    | /connectors/<connector 이름>/pause                    | 실행 중인 connector 중지                        |
  | `PUT`    | /connectors/<connector 이름>/resume                   | 중지 된 connector 재실행                        |
  | `DELETE` | /connectors/<connector 이름>                          | 실행 중인 connector 종료                        |
  | `GET`    | /connectors/<connector 이름>/tasks                    | 실행 중인 connector의 task 정보 확인            |
  | `GET`    | /connectors/<connector 이름>/tasks/\<task id>/status  | 실행 중인 connector의 task 상태 확인            |
  | `POST`   | /connectors/<connector 이름>/tasks/\<task id>/restart | 실행 중인 connector의 task 재시작               |
  | `GET`    | /connectors/<connector 이름>/topics                   | Connector별 연동된 토픽 정보 확인               |
  | `GET`    | /connector-plugins                                    | Connect에 존재하는 connector 플러그인 목록 확인 |
  | `PUT`    | /connector-plugins/<플러그인 이름>/validate           | Connector 생성 시 설정값 유효성 확인            |







### JDBC Connector

- JDBC Connector
  - JDBC driver를 사용하는 관계형 DB로부터 data를 가져와서 Kafka에 넣거나, Kafka에서 데이터를 가져와서 JDBC driver를 사용하는 관계형 DB로 넣을 수 있게 해주는 kafka connector이다.
    - 즉 source connector와 sink connector를 모두 지원한다.
  - Confluent에서 관리하고 있다.



- JDBC Connector 설치하기

  - 아래 사이트에서 JDBC connector를 다운 받는다.

  > https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc

  - 아래 사이트에서 MySQL connector를 다운 받는다([참고](https://docs.confluent.io/kafka-connectors/jdbc/current/jdbc-drivers.html#mysql-server)).
    - MySQL connector는 JDBC 혹은 ODBC를 사용하는 application에서 MySQL에 접속할 수 있도록 connector를 제공한다(Kafka connector와는 다르다).
    - JDBC Connector에는 PostgreSQL과 SQLite에 접속하기 위한 driver는 포함되어 있지만, MySQL을 위한 driver는 포함되어 있지 않으므로 다운을 받아야한다.
    - 아래 사이트에서 Platform Independent를 선택하여 다운 받은 후 zip 파일을 풀면 나오는 `.jar` 파일을 위에서 받은 JDBC connector 내부의 `lib` 폴더에 추가한다.

  > https://dev.mysql.com/downloads/connector/j/

  - Kafka connector config file 수정하기
    - `connect.standalone.properties` file에서 아래 property들만 수정해준다.
    - 운영 환경에서는 `connect-distributed.properties` file을 사용하여 분산 실행하는 것이 권장된다.

  ```properties
  bootstrap.servers=localhost:29093
  key.converter=org.apache.kafka.connect.json.JsonConverter
  value.converter=org.apache.kafka.connect.json.JsonConverter
  key.converter.schemas.enable=true
  value.converter.schemas.enable=true
  offset.storage.file.filename=/tmp/connect.offsets
  offset.flush.interval.ms=10000
  plugin.path=/usr/share/java
  ```

  - 아래와 같이 `docker-compose.yml` file을 작성한다.
    - 위에서 받은 connector의 압축을 풀어서 나온 directory와 `connect.standalone.properties` file을 bind-mount한다.
    - MySQL driver는 결국 `/usr/share/java/confluentinc-kafka-connect-jdbc-10.7.4/lib` 경로에 들어가게 된다.

  ```yaml
  version: '3.2'
  
  
  services:
    mysql:
      image: mysql:latest
      container_name: mysql
      environment:
        - TZ=Asia/Seoul
        - POSTGRES_PASSWORD=1234
      ports:
        - 3307:3306
      networks:
        - etl
    
    zookeeper:
      container_name: zookeeper
      image: confluentinc/cp-zookeeper:latest
      environment:
        - ZOOKEEPER_CLIENT_PORT=2181
      networks:
        - etl
  
    kafka:
      image: confluentinc/cp-kafka:latest
      container_name: kafka
      environment:
        - KAFKA_ZOOKEEPER_CONNECT=theo-etl-zookeeper:2181
        - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:29093
        - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
      volumes:
        - ./confluentinc-kafka-connect-jdbc-10.7.4:/usr/share/java/confluentinc-kafka-connect-jdbc-10.7.4
        - ./connect-standalone.properties:/etc/kafka/connect-standalone.properties
      ports:
        - 9093:9092
      depends_on:
        - zookeeper
      networks:
        - test
  
  networks:
    test:
      driver: bridge
  ```

  - Container들을 실행한다.

  ```bash
  $ docker compose up
  ```



- Test용 data를 생성한다.

  - Database 생성

  ```sql
  CREATE DATABASE etl_test;
  ```

  - Table 생성

  ```sql
  CREATE TABLE product (
    id INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    updated_time TIMESTAMP NOT NULL default current_timestamp,
    PRIMARY KEY (id)
  );
  ```

  - Data 삽입

  ```sql
  INSERT INTO product (id, name) VALUES (0, 'iPad');
  
  INSERT INTO product (id, NAME) VALUES (1, 'iPhone');
  
  INSERT INTO product (id, NAME) Vetl_testproductALUES (2, 'AirPods');
  ```



- Kafka Connect 실행하기

  - Kafka container에 attach한다.

  ```bash
  $ docker exec -it kafka /bin/bash
  ```

  - Kafka Connect를 실행한다.

  ```bash
  $ /bin/connect-standalone /etc/kafka/connect-standalone.properties
  ```

  - 정상적으로 실행됐는지 확인한다.
    - 정상적으로 실행됐다면, 위에서 추가한 JDBC source connector와 sink connector가 응답으로 올 것이다.

  ```bash
  $ curl localhost:8083/connector-plugins
  ```



- Source Connector 실행하기

  - 실행하기

  ```bash
  $ curl -XPOST 'localhost:8083/connectors' \
  --header 'Content-type: application/json' \
  --data-raw '{
    "name": "my-jdbc-source-connector",
    "config": {
      "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
      "connection.url": "jdbc:mysql://mysql:3306/etl_test",
      "connection.user": "root",
      "connection.password": "1234",
      "topic.prefix": "my-mysql-",
      "table.whitelist": "product",
      "mode":"bulk"
    }
  }'
  ```

  - 정상적으로 생성 됐는지 확인

  ```bash
  $ curl localhost:8083/connectors/my-jdbc-source-connector/status
  ```

  - Consumer를 통해 확인
    - Message가 잘 consuming되면 connector가 정상적으로 실행되는 것이다.

  ```sh
  $ /bin/kafka-console-consumer --bootstrap-server 127.0.0.1:29093 --topic my-mysql-product --from-beginning
  ```



- Source Connector의 주요 설정들

  - `mode`
    - `bulk`: table 전체를 bulk한다.
    - `incrementing`: 각 table에서 증가하는 column을 기준으로 새롭게 추가된 row들만 추출하며, 수정되거나 삭제 된 row들은 추출이 불가능하다.
    - `timestamp`: timestamp-like clumn을 사용하여 새로 추가되거나 변경된 row들을 추출한다.
    - `timestamp+incrementing`: timestamp-like column을 사용하여 추가 되거나 변경된 row들을 탐지하고, 점차 증가하는 고유한 column을 사용하여 각 row들이 고유한 stream offset을 할당 받을 수 있게 한다.
  
  
  - `connection` 관련 옵션들
      - `url`: JDBC connection URL을 작성하며, RDBMS의 종류에 따라 형식이 다를 수 있다.
      - `user`: JDBC connection user를 설정한다.
      - `password`: JDBC connection password를 설정한다.
  - `table` 관련 옵션
      - 기본적으로 JDBC source connector는 system table이 아닌 모든 table을 대상으로 data를 가져온다.
      - 그러나, `table.whitelist` 혹은 `table.blacklist`를 통해 data를 가져올 table을 설정할 수 있다.
      - 둘 중 하나의 값만 설정이 가능하다.
      - 두 설정 모두 컴마로 구분 된 table명을 String으로 받는다(e.g. `"Product, User, Email"`)
      - `table.whitelist`: data를 가져올 table들을 나열한다.
      - `table.blacklist`: data를 가져오지 않을 table들을 나열한다.
  
  
    - `query`
      - 수집 대상 row들을 조회하는 query를 설정한다.
      - Query에 table도 지정하므로, 이 값을 설정하면 모든 table에서 data를 가져오지는 않는다.
      - 일반적으로 특정 row만 수집하고자 하거나, table들을 join하거나, table 내의 일부 column들만 필요할 경우 사용한다.
      - `mode`가 `bulk`일 경우 `WHERE` 절을 사용할 수 있으며, 다른 `mode`를 사용할 경우 가능할 수도 있고, 불가능 할 수 도 있다.
  
  - `poll.interval.ms`
    - 각 table에서 새로운 data를 가져올 주기를 ms단위로 설정한다.
      - 기본값은 100ms이다.





## Kafka Streams

- 토픽에 적재된 데이터를 실시간으로 변환하여 다른 토픽에 적재하는 라이브러리.
  - 카프카에서 공식적으로 지원하는 라이브러리다.
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







## etc

- 카프카 커넥트
  - 프로듀서, 컨슈머 애플리케이션을 만드는 것은 좋은 방법이지만 반복적인 파이프라인 생성 작업이 있을 때는 매번 프로듀서, 컨슈머 애플리케이션을 개발하고 배포, 운영하는 것이 비효율적일 수 있다.
  - 커넥트는 특정 작업 형태를 템플릿으로 만들어 놓은 커넥터를 실행함으로써 반복 작업을 줄일 수 있다.
  - 필요할 경우 추후 추가
    - 아파치 카프카 애플리케이션 프로그래밍(p.153)



- 카프카 미러메이커2
  - 서로 다른 두 개의 카프카 클러스터 간에 토픽을 복제하는 애플리케이션
  - 필요할 경우 추후 추가
    - 아파치 카프카 애플리케이션 프로그래밍(p.188)

