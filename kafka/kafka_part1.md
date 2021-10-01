# Kafka란

- Kafka
  - 링크드인에서 스칼라로 개발한 메시지 프로젝트
  - Kafka라는 이름은 소설가 프란츠 카프카에서 따왔다.
  - Pub-Sub 모델의 메시지 큐
  - 분산 환경에 특화되어 있다는 특징을 가지고 있다.



- Pub/Sub 구조
  - 링크드인에서 기존에 사용하던 Point to Point 구조를 Pub/Sub 구조로 변경하였다.
    - A,B,C,D가 있다고 할 때 A가 누구에게 메시지를 보내야 할지 모르므로 A는 B,C,D와 모두 연결되어 있어야 하며, 이는 B, C, D도 마찬가지다.
    - Pub/Sub 구조는 A,B,C,D가 모두 연결되어 있는 것이 아니라 발신자, 수신자가 지정되어 있고 발신자는 카프카에만 요청을 보내고, 수신자는 카프카에게서만 메시지를 받는 구조이다(단방향 구조).
    - 따라서 발신자와 수신자 모두 Kafka와만 연결되어 있으면 된다.
  - Publish(Producer)
    - 발신자는 카프카에게 전송만 하면 되고, 수신자가 누구인지 알 필요가 없다.
    - 따라서 특별히 수신자를 정해놓지 않고 서버에 전송하게 되는 심플한 구조를 갖게 된다.
    - 카프카는 내부에 발신자의 메시지를 토픽이라는 주소로 저장하게 된다.
  - Subscribe(Consumer)
    - 수신자는 카프카에 원하는 토픽을 구독한다.
    - 즉, 수신자 역시 발신자가 누구인지 관심은 없고 필요한 메시지만 구독을 하게 되는 것이다.



- 구성 요소
  - Event
    - Producer와 Consumer가 데이터를 주고 받는 단위
    - 메시지라고도 부른다.
  - Topic
    - 이벤트가 쓰이는 곳.
    - Producer는 Topic에 이벤트를 게시한다.
    - Consumer는 Topic으로부터 이벤트를 가져와서 처리한다.
    - Topic은 파일 시스템의 디렉터리와 유사하며, 이벤트는 디렉터리 안의 파일과 유사하다.
  - Broker
    - 카프카 서버
    - Producer에게 메시지를 받아서, Consumer에게 전달해주는 역할을 한다.
    - Topic이 저장되어 있는 곳이다.
    - Elasticsearch의 node와 유사하다.
  - Producer
    - Kafka 이벤트를 게시(post)하는 클라이언트 어플리케이션
  - Consumer
    - Topic을 구동하고 이로부터 얻어낸 이벤트를 처리하는 클라이언트 어플리케이션
  - Partition
    - Topic은 여러 Broker에 분산되어 저장되며 이렇게 분산된 Topic을 Partition이라고 한다.
    - 어떤 이벤트가 Partition에 저장될지는 이벤트의 key에 의해 정해지며, 같은 키를 가지는 이벤트는 항상 같은 Partition에 저장된다.
    - Topic의 Partition에 지정된 Consumer가 항상 정확히 동일한 순서로 Partition의 이벤트를 읽을 것을 보장한다.
  - Zookeeper
    - Broker에 분산 처리된 메시지 큐의 정보들을 관리한다.
    - Kafka는 Zookeeper 없이는 실행되지 않는다.



- 카프카를 비롯한 대부분의 분산 시스템의 장점
  - 높은 확장성
    - 카프카의 단일 브로커(노드)로는 처리가 힘들 경우 브로커를 늘리기만 하면 된다.
    - 또한 브로커를 추가하는 것이 매우 쉽다.
  - 안정성
    - 동일한 역할을 수행하는 브로커들 중 일부 브로커의 장애 발생시 나머지 브로커들이 장애 발생 노드 분까지 처리를 맡게 된다.
    - 이르 통해 안정적인 서비스 운영이 가능하다.



## 주요 개념

- Producer와 Consumer의 분리
  - Producer와 Consumer는 완전 별개로 동작한다.
    - Producer는  Broker의 Topic에 메시지를 게시하기만 하면 되며, Consumer는 Broker의 특정 Topic에서 메시지를 가져와서 처리만 하면 된다.
  - 이를 통해 Kafka는 높은 확장성을 지니게 된다.
    - 즉, Producer와 Consumer를 필요에 의해 스케일 인 아웃하기에 용이한 구조이다.
    - 만약 Producer와 Consumer가 별개로 동작하지 않는다면 확장 또는 축소시 이들을 모두 연결하거나 연결해제 해줘야 했을 것이다.



- Push 모델과  Pull 모델
  - Kafka의 Consumer는 Pull 모델을 기반으로 메시지 처리를 진행한다.
    - 즉, Broker가 Consumer에게 메시지를 전달하는 것이 아닌, Consumer가 필요할 때 Broker로 부터 메시지를 가져와 처리하는 형태이다.
  - 만일 Push 모델이라면(즉, Broker가 Consumer에게 메시지를 전달한다면) Consumer를 관리하기 어렵지만, Pull 모델은 Consumer가 처리 가능한 때에 메시지를 가져와 처리하기 때문에 Consumer를 관리하기 쉽다.
  - 또한 Push 모델일 경우에는, 여러 메시지를 한 번에 처리하도록 하기 위해 전송을 지연시킬 수 있다. 따라서, 메시지를 처리할 수 있는 Consumer가 있어도 메시지를 받을 때 까지 대기해야 한다.
  - 반면에 Pull 모델은 Consumer가 마지막으로 처리된 메시지 이후의 메시지를 처리 가능할 때 모두 가져오기 때문에 불필요한 지연이 발생하지 않는다.



- 소비된 메시지 축적(Commit과 Offset)

  - 메세지는 지정된 Topic에 전달된다.
    - Topic은 다시 여러 Partition으로 나뉠 수 있다.
    - 각 Partition에 저장된 메시지를 log라고 부른다.
    - 메시지는 partition에 순차적으로 추가되며, 이 메시지의 상대적인 위치를 offset이라 한다. 

  - Commit과 Offset

    - Consumer의 `poll()`은 이전에 commit한 offset이 존재하면, 해당 offset 이후의 메시지를 읽어온다.
    - 또 읽어온 뒤, 마지막 offset을 commit한다.
    - 이어서 `poll()`이 실행되면 방금전 commit한 offset 이후의 메시지를 읽어와 처리하게 된다.

  - 메시지 소비 중에는 다음과 같은 문제들이 발생할 수도 있다.

    - Broker가 메시지를 네트워크를 통해 Consumer에게 전달할 때 마다, 전달 즉시 메시지를 소비 된 메시지로 기록하면, Consumser가 메세지 처리를 실패할 경우 해당 메시지는 처리되지 못하고 소비 된 상태로 남게 된다.
    - 따라서, Broker는 메시지가 소비되었음을 기록하기 위해서, Consumer의 승인을 기다린다.
    - 그러나 이러한 방식은 다시 아래와 같은 문제를 발생시키게 된다.

    - Consumer가 메시지를 성공적으로 처리한 뒤 Broker에 승인을 보내기 전에 Broker가 실패하였다고 판단하고 다시 메시지를 보낼 경우, Consumer는 동일한 메시지를 두 번 처리하게 된다.
    - 따라서 Consumer는 멱등성을 고려해야 한다.
    - 즉 같은 메시지를 특수한 상황에 의해 여러 번 받아서 여러 번 처리하더라도, 한 번 처리한 것과 같은 결과를 가지도록 설계해야 한다. 

  - 메시지 전달 컨셉

    - At most once(최대 한 번): 메시지가 손실 될 수 있지만, 재전달은 하지 않는다.
    - At least once(최소 한 번): 메시지가 손실 되지 않지만, 재전달이 일어난다.
    - Exactly once(정확히 한 번): 메시지는 단 한 번만 전달 된다.



- Consumer Group

  - Consumer Group은 하나의 Topic을 구독하는 여러  Consumer들의 모음이다.
    - Topic을 구독하는 Consumer들을 Group화 하는 이유는, 가용성 때문이다.
    - 하나의 Topic을 처리하는 Consumer가 1개인 것 보다 여러개라면 당연히 가용성은 증가할 것이다.
    - Consumer Group의 각 Consumer들은 하나의 Topic의 각기 다른 Partition의 내용만을 처리할 수 있는데, 이를 통해 Kafka는 메시지 처리 순서를 보장한다.
    - 따라서 특정 Partition을 처리하던 Consumer가 처리 불가 상태가 된다면, 해당 Partition의 메시지를 처리할 수 없는 상태가 되어버린다.

  - Rebalance
    - 특정 Partition을 처리하던 Consumer가 처리 불가 상태가 될 경우, Partition과 Consumer를 재조정하여, 남은 Consumer Group 내의 Consumer들이 Partition을 적절하게 나누어 처리하게 된다.
    - 또한 Consumer Group 내에서 Consumer들 간에 Offset 정보를 공유하고 있기 때문에, 특정 Consumer가 처리불가 상태가 되었을 때, 해당 Consumer가 처리한 마지막 Offset 이후 부터 처리를 이어서 할 수 있다.
    - 이처럼 Partition을 나머지 Consumer들이 다시 나누어 처리하는 것을 Rebalance라고 한다.
  - Consumer Group과 Partition
    - 무조건 Consumer Group 내의 Consumer들은 모두 각기 다른 Partition에 연결되어야 한다.
    - 이를 통해 Consumer의 메시지 처리 순서를 보장하게 된다.
  - Consumer 확장
    - Consumer의 성능이 부족해, 이를  확장할 때, Consumer의 수가 Partition보다 많다면 Partition의 개수도 늘려줘야 한다.
    -  각 Consumer는 동일한 Partition을 처리할 수 없기 때문에 Consumer의 수가 Partition보다 많다면 Partitiom과 연결되지 않은 Consumer가 아무 처리도 하지 않는 상황이 발생할 수 있기 때문이다.



- Leader와 Follower
  - ES의 primary와 replica와 유사하다.
  - Topic을 복제해서 Follower에 저장한다.
  - 메시지를 생성하고 소비하는 작업은 모두 leader가 처리하고, follower들은 복제해서 가지고 있기만 한다.



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
    - 힙 메모리의 기본 설정은 카프카 브로커의 경우 1GB, 주키퍼는 512GB로 설정되어 있다.

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
    - config 폴더에 있는 server.properties 파일에 카프카 브로커가 클러스터 운영에 필요한 옵션들을 지정할 수 있다.

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



# 사용하기

## Docker로 설치하기

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
    -  `compression_type`: 데이터를 압축해서 보낼 수 있다(None, gzip, snappy, lz4 중 선택).
    - `retries`: 오류로 전송 실패한 데이터를 다시 보낼지 여부
    - `batch_size`: 어러 데이터를 배치로 보내는 것을 시도한다.
    - `linger_ms`: 배치 형태 작업을 위해 기다리는 시간 조정, 배치 사이즈에 도달하면 옵션과 관계 없이 전송, 배치 사이즈에 도달하지 않아도 제한 시간 도달 시 메시지 전송
    - `max_request_size`: 한 번에 보낼 수 있는 메시지 바이트 사이즈(기본 값은 1mb)



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
  
  
  producer = KafkaProducer(bootstrap_servers=['192.168.0.237:9092'],
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





# 참고

- https://galid1.tistory.com/793
- https://needjarvis.tistory.com/category/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B0%8F%20DB/%EC%B9%B4%ED%94%84%EC%B9%B4%28Kafka%29
- https://kafka-python.readthedocs.io/en/1.1.0
- https://kontext.tech/column/streaming-analytics/474/kafka-topic-partitions-walkthrough-via-python#h__1
