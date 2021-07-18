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