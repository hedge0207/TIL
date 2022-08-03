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





## 카프카 커맨드 라인 툴

- 카프카 커맨드 라인 툴
  - 카프카 브로커 운영에 필요한 다양한 명령을 내릴 수 있다.
  - 카프카 클라이언트 애플리케이션을 운영할 때 토픽이나 파티션 개수 변경과 같은 명령을 실행해야 하는 경우가 자주 발생하므로, 카프카 커맨드 라인 툴과 각 툴별 옵션에 대해서 알고 있어야 한다.
  - `wurstmeister/kafka`이미지의 경우 `/opt/kafka/bin`에서 찾을 수 있다.



- Kafka-topics.sh
  - 토픽과 관련된 명령을 수행하는 커맨드라인.
  - 토픽 생성
    - `--create` 명령을 사용한다.
    - `--replication-factor`는 복제 파티션의 개수를 지정하는 것인데 1이면 복제 파티션을 사용하지 않는다는 의미이다.
  
  ```bash
  $ kafka-topics.sh \
  > --create \
  > --bootstrap-server 127.0.0.1:9092 \	# 카프카 호스트와 포트 지정
  > --partitions 3 \							# 파티션 개수 지정
  > --replication-factor 1 \					# 복제 파티션 개수 지정
  > --config retention.ms=172800000 \			# 추가적인 설정
  > --topic hello.kafka						# 토픽 이름 지정
  ```
  
  - 토픽 리스트 조회
    - `--list` 명령을 사용한다.
    - `--exclude-internal` 옵션을 추가하면 내부 관리를 위한 인터널 토픽을 제외하고 보여준다.
  
  ```bash
  $ kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
  ```
  
  - 특정 토픽 상세 조회
    - `--describe` 명령을 사용한다.
    - `Partition`은 파티션 번호, `Leader`는 해당 파티션의 리더 파티션이 위치한 브로커의 번호, `Replicas`는 해당 파티션의 복제 파티션이 위치한 브로커의 번호를 의미한다.
  
  ```bash
  $ kafka-topics.sh --describe --bootstrap-server 127.0.0.1:9092 --topic hello.kafka
  
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
  $ kafka-topics.sh --alter --bootstrap-server 127.0.0.1:9092 --topic hello.kafka --partitions 4
  
  # 리텐션 기간 수정
  $ kafka-configs.sh --alter --add-config retention.ms=86400000 \
  --bootstrap-server 127.0.0.1:9092 \
  --entity-type topics \
  --entity-name hello.kafka
  ```
  
  - 토픽 삭제
  
  ```bash
  $ kafka-topics.sh --delete --bootstrap-server 127.0.0.1:9092 --topic <삭제할 topic 이름>
  ```
  



- kafka-console.producer.sh

  - 프로듀서와 관련된 명령을 수행하는 커맨드라인
    - 이 커맨드라인으로 전송되는 레코드 값은 UTF-8을 기반으로 Byte로 변환된다.
    - 즉 스트링만 전송이 가능하다.
  - 메시지 값만 보내기
    - 메시지 입력 후 엔터를 누르면 별 다른 메시지 없이 전송된다.

  ```bash
  $ kafka-console-producer.sh --bootstrap-server 127.0.0.1:9092 --topic hello.kafka
  >hello
  >world
  >1
  >True
  >[1,2,3]
  ```

  - 메시지 키와 값 같이 보내기
    - `key.separator`를 설정하지 않을 경우 기본 값은 `\t`dlek.

  ```bash
  kafka-console-producer.sh --bootstrap-server 127.0.0.1:9092 \
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
  $ kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic kafka.test --from-beginning
  ```

  - 메시지 키와 값을 함께 확인
    - `--property` 옵션을 사용한다.
    - `--group` 옵션을 통해 새로운 컨슈머 그룹을 생성하였는데, 이 컨슈머 그룹을 통해 토픽에서 가져온 메시지에 대하 커밋을 진행한다.

  ```bash
  kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 \
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
  $ kafka-consumer-groups.sh --list --bootstrap-server 127.0.0.1:9092 
  ```

  - 컨슈머 그룹 상세 정보 확인
    -  특정 컨슈머 그룹의 상세 정보를 확인하기 위해 쓰인다.

  ```bash
  $ kafka-consumer-groups.sh --describe --group test-group --bootstrap-server 127.0.0.1:9092
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



- kafka-verifiable-producer/consumer.sh

  - 카프카 클러스터 설치가 완료된 이후에 토픽에 데이터를 전송하여 간단한 네트워크 통신 테스트를 할 때 유용하게 사용이 가능하다.
  - 메시지 보내기
    - 최초 실행 시점이 `startup_complete` 메시지와 함께 출력된다.
    - 메시지별로 보낸 시간과 메시지 키, 메시지 값, 토픽, 저장된 파티션, 저장된 오프셋 번호가 출력된다.
    - `--max-message`에서 지정해준 만큼 전송이 완료되면 통계값이 출력된다.

  ```bash
  $ kafka-verifiable-producer.sh --bootstrap-server 127.0.0.1:9092 --max-message 10 --topic kafka.test
  {"timestamp":1633505763219,"name":"startup_complete"}
  {"timestamp":1633505763571,"name":"producer_send_success","key":null,"value":"0","partition":0,"topic":"kafka.test","offset":4}
  {"timestamp":1633505763574,"name":"producer_send_success","key":null,"value":"1","partition":0,"topic":"kafka.test","offset":5}
  {"timestamp":1633505763574,"name":"producer_send_success","key":null,"value":"2","partition":0,"topic":"kafka.test","offset":6}
  ...
  {"timestamp":1633505763598,"name":"tool_data","sent":10,"acked":10,"target_throughput":-1,"avg_throughput":26.17801047120419}
  ```

  - 메시지 확인하기

  ```bash
  $ kafka-verifiable-consumer.sh --bootstrap-server 127.0.0.1:9092  --topic kafka.test --group-id test-group
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
  $ kafka-delete-records.sh --bootstrap-server 127.0.0.1:9092 --offset-json-file delete-data.json
  ```



- Topic 내의 message 개수 가져오기

  - 결과는 `<topic>:<partition_num>:<message_num>` 형태로 출력된다.

  ```bash
  $ kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list <HOST1:PORT,HOST2:PORT> --topic <topic>
  ```

  



## Python에서 사용하기

- Python에서 Kafka에 접근할 수 있게 해주는 라이브러리에는 아래와 같은 것들이 있다.
  - confluent-kafka-python
    - 성능이 가장 좋다.
    - C로 만든 라이브러리를 호출하여 사용하는 방식이므로 별도의 설치과정이 존재한다.
  - kafka-python
    - pure python이기에 confluent-kafka-python에 비해 속도는 느리다.
    - 사용법이 직관적이고 간결하다.



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



- Consumer 구현

  ```python
  from kafka import KafkaConsumer
  from json import loads
  
  
  consumer = KafkaConsumer('test',bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest', \
                          enable_auto_commit=True, group_id="my-group", value_deserializer=lambda x: loads(x.decode('utf-8')),\
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
  
  bootstrap_servers='127.0.0.1:9092',
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
      consumer.commit()
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

  
