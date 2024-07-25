# Java Application monitoring

- jcmd

  - 실행중인 JVM의 상태를 확인할 수 있게 해주는 명령어이다.
    - JDK에 기본적으로 내장되어 있어 별도의 설치 없이 사용이 가능하다.
  - Native memory를 monitoring하기 위해서는 아래와 같이 옵션을 추가해야 한다.

  ```bash
  -XX:NativeMemoryTracking=detail
  ```

  - 아래와 같은 형식으로 사용한다.

  ```bash
  $ jcmd [pid | main-class] command... | PerfCounter.print | -f filename
  ```

  - Native memory 확인하기

  ```bash
  $ jcmd <pid> VM.native_memory summary
  ```

  - `summary.diff`를 사용하여 native memory 변경 사항을 확인 할 수 있다.
    - `baseline`을 실행한 시점과의 차이를 확인할 수 있다.	

  ```bash
  # 먼저 기준이 될 memory를 설정한다.
  $ jcmd <pid> VM.native_memory baseline
  # baseline으로 설정된 시점과의 차이를 확인한다.
  $ jcmd <pid> VM.native_memory.diff
  ```



- VisualVM

  - 실행중인 JVM의 상태를 확인할 수 있게 해주는 tool이다.
    - 이름에서 알 수 있는 것 처럼 시각화가 가능하다.
    - Local에서 실행중인 Java application뿐 아니라 remote에서 실행중인 Java application도 monitoring이 가능하다.
    - [홈페이지](https://visualvm.github.io/)에서 다운이 가능하다.
    - 압축을 해제하여 나온 `visualvm.exe` 파일을 통해 실행한다.
  - JMX를 활용하여 monitoring을 수행한다.
    - JMX(Java Management eXtensions)는 Java에 내장되어 있는 API이다.
    - Java 실행시에 특정 옵션을 주면 활성화된다.
    - **운영 환경에서는 활성화시켜선 안 된다.**
  - Monitoring용 Java application을 실행한다.
    - 아래 예시에서는 Kafka Connect container를 실행한다.
    - `Djava.rmi.server.hostname`에는 docker container의 IP나 localhost 등을 주면 안 되며, host machine의 IP를 입력해야한다.
    - `Dcom.sun.management.jmxremote.port`와 `Dcom.sun.management.jmxremote.rmi.port`의 port는 같은 값을 설정해야 하며, 이 port를 publish해야 한다.
  
  ```yaml
  version: '3.2'
  
  
  services:
  
    kafka-connect:
      image: confluentinc/cp-kafka-connect:7.5.3
      container_name: kafka-connect
      environment:
        EXTRA_ARGS: "-XX:NativeMemoryTracking=detail 
        			   -Dcom.sun.management.jmxremote=true 
                     -Dcom.sun.management.jmxremote.local.only=false 
                     -Dcom.sun.management.jmxremote.ssl=false 
                     -Dcom.sun.management.jmxremote.authenticate=false 
                     -Djava.rmi.server.hostname=<host_ip>
                     -Dcom.sun.management.jmxremote.port=8098 
                     -Dcom.sun.management.jmxremote.rmi.port=8098"
      # port를 publish한다.
      ports:
        - 8098:8098
  ```
  
  - Remote의 Java application monitoring하기
    - 실행 후 좌측 sidebar의 remote tap에서 `Remote`를 클릭하여 remote host를 입력한 후 remote를 생성한다.
    - Local의 경우 별도의 등록 없이 VisualVM이 자동으로 탐지한다.
    - 그 후 추가 된 remote를 우클릭하여 `Add JMX Connection...`을 클릭한 후 위에서 publish한 port(`8098`)와 remote server의 IP를 입력한다.



- Jconsole
  - VisualVM과 마찬가지로 JMX를 활용하여 monitoring하는 tool이다.
    - 시각화가 가능하다.