

# Debug Elasticsearch

- Elasticsearch debugging하기

  > 8.9버전 기준 Windows에서 실행할 경우 알 수 없는 error가 계속 발생한다(encoding 관련 문제인 것으로 추정)
  >
  > 따라서 아래에서는 Docker Container를 생성하여 실행했다.
  >
  > Gradle을 설치해야 한다는 글도 있지만 Elasticsearch는 gradlew를 통해 build하기 때문에 gradle은 설치하지 않아도 된다.

  - Ubuntu docker container 생성

    > [링크 참조](https://github.com/hedge0207/TIL/blob/master/devops/ubuntu_docker.md#docker%EB%A1%9C-ubuntu-%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0)

    - 위 링크를 참조해서 Ubuntu docker container를 생성한다.
    - Container 생성 후 내부에 접속해서 root user의 비밀번호를 재설정한다.

  ```bash
  $ passwd
  ```

  - 컨테이너 내부에서 추가적으로 필요한 패키지들을 설치한다.

  ```bash
  $ apt-get update
  $ apt install vim curl sudo wget git
  ```

  - Elasticsearch 정책상 root user로 elasticsearch를 실행시킬 수 없으므로 사용자를 추가한다.
    - 사용자 추가 후 필요하다면 사용자를 sudo 그룹에 추가한다.

  ```bash
  $ adduser <추가할 사용자>
  $ usermod -aG sudo <추가한 사용자>
  $ su <추가한 사용자>
  ```

  - JDK를 설치한다.

    > 8.9버전 기준 jdk 17버전이 필요하다(17버전 이상이 아니라 정확히 17버전이 필요하다).
    >
    > 링크에서 x64 Compressed Archive 파일을 다운로드 받는다.

  ```bash
  # 파일을 다운받고
  $ wget https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz
  # 압축을 푼 뒤
  $ gzip -d jdk-17_linux-x64_bin.tar.gz
  # 묶인 파일을 푼다.
  $ tar -xvf jdk-17_linux-x64_bin.tar
  ```

  - 환경변수를 추가한다.
    - Elasticsearch가 실행될 때 아래 두 환경변수를 참조하여 실행된다.

  ```bash
  $ vi ~/.bashrc
  # 아래 두 줄을 추가한다.
  export JAVA_HOME=<jdk 설치 경로>/jdk-17.0.7
  export PATH=$PATH:$JAVA_HOME/bin
  
  # 적용한다.
  $ source ~/.bashrc
  
  # 확인
  $ echo ${JAVA_HOME}		# 위에서 설정한 경로가 뜨면 잘 등록된 것이다.
  ```

  - Elasticsearch 다운 받기
    - `git clone`을 통해 받는 것이 가장 편한 방법이지만 Elasticsearch repository의 크기가 너무 커서 `fatal: fetch-pack: invalid index-pack output`와 같은 error가 발생할 것이다.

  ```bash
  # 아래 명령어로 clone 받을 수 없다면
  $ git clone https://github.com/elastic/elasticsearch.git
  
  # 아래와 같이 일부만 clone 받는다.
  $ git config --global core.compression 0
  # 그 후 clone 받은 directory로 이동해서
  $ cd elasticsearch
  # 나머지를 받는다.
  $ git fetch --unshallow 
  # 마지막으로 pull을 해준다.
  $ git pull --all
  ```

  - 혹은 위 과정을 Dockerfile로 image를 build하면서 한 번에 해도 된다.
    - **root user로 실행하려 할 경우 error가 발생한다.**
    - Elasticsearch source file을 bind-mount하여 container에서 사용할 것이므로 Docker를 실행시킬 host user의 user id와 group id로 container 내부의 group과 user를 생성한다.

  ```dockerfile
  FROM ubuntu:22.04
  
  ENV DEBIAN_FRONTEND=noninteractive
  
  RUN ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime
  
  RUN apt-get update
  
  RUN apt-get install curl -y openjdk-17-jdk -y
  
  # host user의 GID와 UID와 동일하게 group과 user를 생성한다.
  RUN groupadd -g <host_user_GID> es
  RUN useradd -r -u <host_user_UID> -g es es
  
  RUN chmod 777 /home
  
  # root로 실행시 error가 발생하므로 일반 user로 변경한다.
  USER es
  
  WORKDIR /home
  
  ENTRYPOINT /bin/bash
  ```

  - 위 Dockerfile로 image를 build한다.

  ```bash
  $ docker build -t debugging-elasticsearch .
  ```

  - 위 image로 container를 실행한다.

  ```bash
  $ docker run -it --name debugging-elasticsearch debugging-elasticsearch
  ```

  - Elasticsearch 실행하기
    - elasticsearch를 clone 받은 directory에서 아래 명령어를 수행한다.
    - 이 때 9200, 9300 port를 사용 중인 process가 있을 경우 error가 발생한다.
    - 만일 실패할 경우 `./gradlew clean`을 수행한 후 다시 실행한다.

  ```bash
  $ ./gradlew :run
  ```

  - 만일 root user로 실행할 경우 아래와 같은 error가 발생하므로 반드시 일반 user로 실행해야한다.

  ```
  process was found dead while waiting for ports files, node{::runTask-0}
  ```

  - 아래와 같은 message가 출력되면 정상적으로 실행된 것이다.

  ```
  [2024-02-27T14:50:35,167][INFO ][o.e.h.AbstractHttpServerTransport] [runTask-0] publish_address {127.0.0.1:9200}, bound_addresses {[::1]:9200}, {127.0.0.1:9200}
  [2024-02-27T14:50:35,169][INFO ][o.e.n.Node               ] [runTask-0] started
  ```

  - 정상적으로 실행 됐는지 확인하기
    - Elasticsearch 8부터는 security 기능이 자동으로 활성화 된 상태이기 때문에 `-u` option으로 user와 password를 입력해야한다.
    - 기본 user/password는 elastic/password이다.
  
  ```bash
  $ curl -u elastic:password localhost:9200
  ```





## UUID 생성 과정

- Elasticsearch의 UUID는 [Flake ID](https://archive.md/2015.07.08-082503/http://www.boundary.com/blog/2012/01/flake-a-decentralized-k-ordered-unique-id-generator-in-erlang/)를 기반으로 한다.
  - 그러나 추후 살펴볼 내용처럼 이를 변형해서 사용한다.
  - Flake ID와 차이점은 아래와 같다.
    - Flake ID는 첫 64bits를 timestamp를 사용하여 생성하므로 ID 순으로 정렬시 시간 순서대로 정렬되지만, Elasticsearch의 UUID는 첫 두 개의 byte를 생성할 때 sequence number를 사용하기에 Flake ID처럼 ID로 정렬한다고 시간순으로 정렬되지는 않는다.
    - 또한 FlakeID는 timestamp를 8bytes, sequence number에 2 bytes를 사용하지만, Elasticsearch UUID는 timestamp를 6bytes, sequence number를 3bytes 사용한다.
  - 그대로 사용하지 않는 이유는, Lucene term dictionary 구조에서 더 잘 활용할 수 있도록 하기 위함이다.



- Elasticsearch의 UUID 생성과 관련된 class들이다.

  - `server.src.main.java.org.elasticsearch.common.TimeBasedUUIDGenerator`의 `getBase64UUID()` method를 통해 생성한다.

  ```java
  package org.elasticsearch.common;
  
  import java.util.Base64;
  import java.util.concurrent.atomic.AtomicInteger;
  import java.util.concurrent.atomic.AtomicLong;
  
  
  class TimeBasedUUIDGenerator implements UUIDGenerator {
  	
      // 무작위 정수 하나를 생성한다.
      // INSTANCE는 static variable로 instance의 생성 없이도 접근이 가능하며, 한 번만 생성되는 것이 보장된다.
      //java.util.concurrent의 type들은 원자성이 보장되는 type들이다.
      private final AtomicInteger sequenceNumber = new AtomicInteger(SecureRandomHolder.INSTANCE.nextInt());
  
      // 초기값을 0으로 설정한 AtomicLong type 값을 선언한다.
      private final AtomicLong lastTimestamp = new AtomicLong(0);
  	
      // MAC address 값을 가져온다.
      private static final byte[] SECURE_MUNGED_ADDRESS = MacAddressProvider.getSecureMungedAddress();
  
      static {
          assert SECURE_MUNGED_ADDRESS.length == 6;
      }
  
      private static final Base64.Encoder BASE_64_NO_PADDING = Base64.getUrlEncoder().withoutPadding();
  
      protected long currentTimeMillis() {
          // 현재 시간을 long type으로 변환하여 반환한다.
          return System.currentTimeMillis();
      }
  
      protected byte[] macAddress() {
          return SECURE_MUNGED_ADDRESS;
      }
  
      @Override
      public String getBase64UUID() {
          
          final int sequenceId = sequenceNumber.incrementAndGet() & 0xffffff;
  
          long timestamp = this.lastTimestamp.accumulateAndGet(
              currentTimeMillis(),
              sequenceId == 0 ? (lastTimestamp, currentTimeMillis) -> Math.max(lastTimestamp, currentTimeMillis) + 1 : Math::max
          );
  
          final byte[] uuidBytes = new byte[15];
          int i = 0;
  
          uuidBytes[i++] = (byte) sequenceId;
          uuidBytes[i++] = (byte) (sequenceId >>> 16);
  
          uuidBytes[i++] = (byte) (timestamp >>> 16); // changes every ~65 secs
          uuidBytes[i++] = (byte) (timestamp >>> 24); // changes every ~4.5h
          uuidBytes[i++] = (byte) (timestamp >>> 32); // changes every ~50 days
          uuidBytes[i++] = (byte) (timestamp >>> 40); // changes every 35 years
          byte[] macAddress = macAddress();
          assert macAddress.length == 6;
          System.arraycopy(macAddress, 0, uuidBytes, i, macAddress.length);
          i += macAddress.length;
  
          uuidBytes[i++] = (byte) (timestamp >>> 8);
          uuidBytes[i++] = (byte) (sequenceId >>> 8);
          uuidBytes[i++] = (byte) timestamp;
  
          assert i == uuidBytes.length;
  
          System.out.println("-------------------------------------------");
          System.out.println(BASE_64_NO_PADDING.encodeToString(uuidBytes));
          System.out.println("-------------------------------------------");
          return BASE_64_NO_PADDING.encodeToString(uuidBytes);
      }
  }
  ```
  
  - `server.src.main.java.org.elasticsearch.common.SecureRandomHolder`
    - 무작위 정수 생성을 위한 class이다.
  
  ```java
  package org.elasticsearch.common;
  
  import java.security.SecureRandom;
  
  class SecureRandomHolder {
      // 무작위 정수를 담고 있는 INSTACNE 변수는 한 번만 생성된다는 것이 보장된다.
      public static final SecureRandom INSTANCE = new SecureRandom();
  }
  ```
  
  - `server.src.main.java.org.elasticsearch.common.MacAddressPRovider`
    - Elasticsearch를 실행한 machine의 MAC address를 가져오기 위한 class이다.
  
  ```java
  package org.elasticsearch.common;
  
  import java.net.NetworkInterface;
  import java.net.SocketException;
  import java.util.Enumeration;
  
  public class MacAddressProvider {
  
      private static byte[] getMacAddress() throws SocketException {
          Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
          if (en != null) {
              while (en.hasMoreElements()) {
                  NetworkInterface nint = en.nextElement();
                  if (nint.isLoopback() == false) {
                      // Pick the first valid non loopback address we find
                      byte[] address = nint.getHardwareAddress();
                      if (isValidAddress(address)) {
                          return address;
                      }
                  }
              }
          }
          // Could not find a mac address
          return null;
      }
  
      private static boolean isValidAddress(byte[] address) {
          if (address == null || address.length != 6) {
              return false;
          }
          for (byte b : address) {
              if (b != 0x00) {
                  return true; // If any of the bytes are non zero assume a good address
              }
          }
          return false;
      }
  
      public static byte[] getSecureMungedAddress() {
          byte[] address = null;
          try {
              address = getMacAddress();
          } catch (SocketException e) {
              // address will be set below
          }
  
          if (isValidAddress(address) == false) {
              address = constructDummyMulticastAddress();
          }
  
          byte[] mungedBytes = new byte[6];
          SecureRandomHolder.INSTANCE.nextBytes(mungedBytes);
          for (int i = 0; i < 6; ++i) {
              mungedBytes[i] ^= address[i];
          }
  
          return mungedBytes;
      }
  
      private static byte[] constructDummyMulticastAddress() {
          byte[] dummy = new byte[6];
          SecureRandomHolder.INSTANCE.nextBytes(dummy);
          /*
           * Set the broadcast bit to indicate this is not a _real_ mac address
           */
          dummy[0] |= (byte) 0x01;
          return dummy;
      }
  
  }
  ```



- UUID 생성에 필요한 `sequenceId`와 `timestamp` 생성

  - Elasticsearch는 UUID 생성에 정수와 milliseconde 단위로 변환된 timestamp, 그리고 Elasticsearch가 실행되는 machine의 MAC address를 사용한다.
    - 최초의 난수는 `SecureRandomHolder`를 통해 생성하며, 음수를 포함한 어떤 정수든 나올 수 있다.
    - 난수는 최초 실행시에만 생성되고, 이후에는 생성된 난수에 1을 더하여 사용한다.
    - 따라서 정확히는 최초 실행시에만 난수를 사용하고, 이후부터는 1씩 증가하는 값을 사용한다.
    - Timestamp는 현재 시간과 마지막으로 색인된 시간 중 더 큰 값을 사용하는데, 이는 모종의 이유로 시간이 뒤로 돌아가게 되는 경우를 대비하기 위함이다.
    - Timestamp 6bytes, secuence number 3bytes, MAC address 6bytes를 조합하여 UUID를 생성한다.
    - 이 중 secure number는 정수를 3bytes로 제한하기 위해 추가적인 연산을 수행하고, MAC address는 원래 6bytes로 구성되므로 추가적인 연산을 수행하지 않는다.

  - 무작위 정수 생성
    - 무작위 정수를 1증가시킨 후 16진수 0xffffff를 and 연산을 하여 24bit로 제한한다.
    - 16진수 0xffffff는 2진수로 변환하면 11111111 111111111 11111111으로 모든 bit 값이 1인 24bit(3byte) 숫자이다.
    - 무작위 정수를 사용하는 이유는 JVM, OS, machine등이 내려가고, 모종의 이유로 시간도 다시 돌아가게 되더라도 Elasticsearch가 재시작 할 때 같은 ID값이 생성될 확률을 낮추기 위해서다.

  ```java
  final int sequenceId = sequenceNumber.incrementAndGet() & 0xffffff;
  ```

  - `timestamp` 값을 결정한다.
    - `accumulateAndGet` method는 현재 값과 첫 번째 인자로 받은 값에 두 번째 인자로 받은 함수를 적용하여 object의 값을 update하고, 그 값을 반환한다.
    - 즉, 아래 code는 `lastTimestamp`값과 `currentTimeMillis()`가 반환하는 값(현재 시간을 millisecond 단위로 long type으로 변환한 값)에 lambda 함수를 적용하여 반환하는 code이다.
    - 만약 `sequenceId`가 0이면 `Math.max(lastTimestamp, currentTimeMillis) + 1`가 실행되어 둘 중 더 큰 값에 0을 더해 반환한다.
    - 만약 `sequenceId`가 0이 아니면 `Math::max`가 호출되어` lastTimestamp`, `currentTimeMillis` 중 더 큰 값을 반환한다.
    - `sequenctId`가 0일때만 다른 처리를 해주는 이유는 아직 모르겠다.

  ```java
  long timestamp = this.lastTimestamp.accumulateAndGet(
      currentTimeMillis(),
      sequenceId == 0 ? (lastTimestamp, currentTimeMillis) -> Math.max(lastTimestamp, currentTimeMillis) + 1 : Math::max
  );
  ```

  - MAC address 값을 가져온다.

  ```java
  byte[] macAddress = macAddress();
  ```



- Byte 순서 최적화

  - Elasticsearch는 아래와 같은 방식으로 UUID를 최적화한다.
    - Id의 시작 부분에 고유한 byte를 배치함으로써 정렬을 빠르게 하여 색인 속도를 높인다.
    - 일정 id들이 공통된 prefix를 공유하게 함으로써 압축률을 높인다.
    - 가능한한 leading byte를 통해 segment를 식별할 수 있도록 하여 id 값으로 문서를 찾는 속도를 높인다.
  - `sequenceId`의 첫 번째 byte와 세 번째 byte를 UUID의 가장 앞쪽에 배치하여 정렬을 빠르게 하여 색인 속도를 높인다.
    - 주석에 따르면 처음에는 하위 두 개의 byte를 사용했으나, 이 경우 하나의 segment에 대략적으로 2백만 개의 문서가 색인되는 순간부터 압축의 효가가 나타나기 시작했다고 한다. 
    - 이로 인해 첫 번째와 세 번째 byte를 사용하도록 변경하였고, 기존 보다 적은 segment 크기에서도 압축의 효과가 나타나기 시작했다고 한다.
    - 첫 두 byte에 `timestamp`가 아닌 `sequenceId`를 사용하는 이유는 `timestamp`의 분포는 색인 비율에 영향을 받기 때문에 `sequencId`에 비해 분포의 안정성이 떨어지기 때문이다.


  ```java
  int i = 0;
  // 3byte의 sequenceId의 가장 아래쪽의 1byte를 할당한다.
  uuidBytes[i++] = (byte) sequenceId;
  // sequencId의 bit를 오른쪽으로 shift하여 3byte중 위쪽의 1byte만 남긴다.
  uuidBytes[i++] = (byte) (sequenceId >>> 16);
  ```

  - `timestamp`의 byte들을 뒤쪽으로 배치한다.
    - 각 byte가 일정 기간마다 변경되게 하여 prefix를 공유하게 함으로써 압축률을 높인다.

  ```java
  uuidBytes[i++] = (byte) (timestamp >>> 16); // changes every ~65 secs
  uuidBytes[i++] = (byte) (timestamp >>> 24); // changes every ~4.5h
  uuidBytes[i++] = (byte) (timestamp >>> 32); // changes every ~50 days
  uuidBytes[i++] = (byte) (timestamp >>> 40); // changes every 35 years
  ```

  - 뒤의 6 bytes는 MAC address로 채운다.

  ```java
  // MAC address를 가져오고
  byte[] macAddress = macAddress();
  // MAC address가 6bytes가 맞는지 확인한 후
  assert macAddress.length == 6;
  // MAC address 값으로 6bytes를 채운다.
  System.arraycopy(macAddress, 0, uuidBytes, i, macAddress.length);
  // i의 값을 6만큼 올린다.
  i += macAddress.length;
  ```

  - `timestamp`와 `sequenceId`의 남은 bytes들을 사용하여 마지막 3 bytes를 생성한다.

  ```java
  uuidBytes[i++] = (byte) (timestamp >>> 8);
  uuidBytes[i++] = (byte) (sequenceId >>> 8);
  uuidBytes[i++] = (byte) timestamp;
  ```



- 예시

  - UUID가 생성되는 과정을 예시와 함께 살펴볼 것이다.
  - `sequencId` 생성
    - Elasticsearch가 최초로 실행될 때, 103,484,266라는 난수가 생성됐다.
    - 이 난수에 1을 더한 103,484,267를 0xffffff와 AND 연산을 수행한다.
    - 103,484,267는 2진수로 변환하면 00000110 00101011 00001011 01101011이 되고, 0xffffff와 AND 연산을 수행하면 2,820,971이 된다.
  - `timestamp` 생성
    - `timestamp`는` lastTimestamp`와 `currentTimeMillis`중 더 큰 값으로 결정되는데, `lastTimestamp`는 최초 실행시 0으로 초기화된 상태이므로 `currentTimeMillis`값이 `timestamp`가 된다.
    - 이 값이 1709086673072라고 가정해보자.
  - UUID의 첫 두 개의 byte에 `sequencId`의 세 번째와 첫 번째 byte를 넣는다.
    - 2,820,971는 2진수로 변환하면 00101011 00001011 01101011이다.
    - 첫 번째와 세 번째 byte를 넣으면 UUID는 01101011 00101011이 된다.
    - UUID의 두 번째 byte를 `sequencId`의 세 번째 byte로 사용하므로 65,536(2**16)건의 문서를 색인할 때 마다 UUID의 두 번째 byte가 변경된다.
  - UUID의 세 번째 부터 여섯 번째 byte에 `timestamp`의 byte값 일부를 넣는다.
    - 1,709,098,431,248를 2진수로 변환하면 00000001 10001101 11101110 00110100 01110011 00010000이 된다.
    - UUID의 세 번째 byte에 `timestamp`의 뒤에서 세 번째 byte(`timestamp >>> 16`)를 넣는다.
    - 따라서 UUID의 세 번째 byte 값은 대략 65초(65536ms == 2**16)마다 변경된다.
    - UUID의 네 번째 byte에 `timestamp`의 뒤에서 네 번째 byte(`timestamp >>> 24`)를 넣는다.
    - 따라서 UUID의 네 번째 byte 값은 대략 4.6시간(16777216ms == 2**24)마다 변경된다.
    - UUID의 다섯 번째 byte에 `timestamp`의 뒤에서 다섯 번째 byte(`timestamp >>> 32`)를 넣는다.
    - 따라서 UUID의 다섯 번째 byte 값은 대략 50일(4294967296ms == 2**32)마다 변경된다.
    - UUID의 여섯 번째 byte에 `timestamp`의 뒤에서 여섯 번째 byte(`timestamp >>> 40`)를 넣는다.
    - 따라서 UUID의 여섯 번째 byte 값은 대략 35년(1099511627776ms == 2**40)마다 변경된다.
  - MAC address로 UUID의 일곱 번째부터 열두 번째 byte를 채운다.
  - 남은 byte로 UUID의 열 세 번째 부터 열 다섯 번째까지 채운다.
    - 남은 byte는 `sequencId`의 두 번째 byte와 `timestamp`의 마지막 두 개의 byte이다.

  ```
  # sequencId
  00101011 00001011 01101011
  
  # timestamp
  00000001 10001101 11101110 00110100 01110011 00010000
  
  # 결과 UUID
  01101011 00101011 00110100 11101110 10001101 00000001 ...<MAC address bytes>... 01110011 00001011 00010000
  ```







