

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





## 색인이 실행 과정

- Elasticsearch

  - 아래와 같이 Elasticsearch에 색인 요청을 보낸다.

  ```json
  // POST test/_doc
  {
      "foo":"bar"
  }
  ```

  - `RestIndexAction.prepareRequest()` method가 호출되어 색인를 위한 request를 생성한다.
    - `server.src.main.java.org.elasticsearch.rest.document.RestIndexAction`

  ```java
  @Override
  public RestChannelConsumer prepareRequest(final RestRequest request, final NodeClient client) throws IOException {
      if (request.getRestApiVersion() == RestApiVersion.V_7) {
          request.param("type"); // consume and ignore the type
      }
  	// IndexRequest를 생성하고, params들을 추가한다.
      IndexRequest indexRequest = new IndexRequest(request.param("index"));
      indexRequest.id(request.param("id"));
      indexRequest.routing(request.param("routing"));
      // (...)
  	
      // 생성한 request를 인자로 넘겨 NodeClient의 index 메서드를 실행한다.
      return channel -> client.index(
          indexRequest,
          new RestToXContentListener<>(channel, DocWriteResponse::status, r -> r.getLocation(indexRequest.routing()))
      );
  }
  ```

  - `AbstractClient.index()` method가 호출되어 색인을 실행한다.
    - `server.src.main.java.org.elasticsearch.client.internal.support.AbstractClient`
    - `NodeClient`는 `AbstractClient`를 상속한 client이다.
    - `index()` method는 `TransportIndexAction.TYPE`을 추가하여 `execute()` method를 호출한다.
    - `execute()` method는 `NodeClient.doExecute()` method를 호출한다.

  ```java
  @Override
  public void index(final IndexRequest request, final ActionListener<DocWriteResponse> listener) {
      // NodeClient의 execute 메서드를 실행한다.
      execute(TransportIndexAction.TYPE, request, listener);
  }
  
  @Override
  public final <Request extends ActionRequest, Response extends ActionResponse> void execute(
      ActionType<Response> action,
      Request request,
      ActionListener<Response> listener
  ) {
      try {
          doExecute(action, request, listener);
      } catch (Exception e) {
          assert false : new AssertionError(e);
          listener.onFailure(e);
      }
  }
  ```

  - `NodeClient.doExecute()` method가 호출되고, `deExecute()`는 다시 `executeLocally()` method를 호출한다.
    - `server.src.main.java.org.elasticsearch.client.internal.node.NodeClient`
    - `executeLocally()` method는 이전 단계에서 받아온 action(이 경우에는 `indices:data/write/index`)과 request, listener를 가지고 `TaskManager.registerAndExecute()` method를 호출하여 task manager에 task를 등록하고, 등록한 task를 실행한다.
    - `transportAction()` method는 action에 해당하는 TransPortAction instance(이 경우에는 `TransportIndexAction`)를 반환한다.

  ```java
  @Override
  public <Request extends ActionRequest, Response extends ActionResponse> void doExecute(
      ActionType<Response> action,
      Request request,
      ActionListener<Response> listener
  ) {
      try {
          executeLocally(action, request, listener);
      } catch (TaskCancelledException | IllegalArgumentException | IllegalStateException e) {
          listener.onFailure(e);
      }
  }
  
  public <Request extends ActionRequest, Response extends ActionResponse> Task executeLocally(
          ActionType<Response> action,
          Request request,
          ActionListener<Response> listener
  ) {
      return taskManager.registerAndExecute(
          "transport",
          transportAction(action),
          request,
          localConnection,
          ActionListener.assertOnce(listener)
      );
  }
  ```

  - `TaskManager.registerAndExecute()` method는 task를 등록하고, 실행한다.

    - `server.src.main.java.org.elasticsearch.tasks.TaskManager`

    - `TransportIndexAction.execute()` method를 호출하여 task를 실행한다.

  ```java
  public <Request extends ActionRequest, Response extends ActionResponse> Task registerAndExecute(
      String type,
      TransportAction<Request, Response> action,
      Request request,
      Transport.Connection localConnection,
      ActionListener<Response> taskListener
  ) {
      // (...)
  
      try (var ignored = threadPool.getThreadContext().newTraceContext()) {
          final Task task;
          try {
              // 받아온 정보로 task를 등록하고
              task = register(type, action.actionName, request);
          } catch (TaskCancelledException e) {
              Releasables.close(unregisterChildNode);
              throw e;
          }
          // TransportIndexAction의 execute method를 호출하여 task를 실행한다.
          // 색인 결과를 처리할 listener를 생성하여 execute() 호출시 함께 넘긴다.
          action.execute(task, request, new ActionListener<>() {
              @Override
              public void onResponse(Response response) {
                  try {
                      release();
                  } finally {
                      taskListener.onResponse(response);
                  }
              }
  
              @Override
              public void onFailure(Exception e) {
                  try {
                      if (request.getParentTask().isSet()) {
                          cancelChildLocal(request.getParentTask(), request.getRequestId(), e.toString());
                      }
                      release();
                  } finally {
                      taskListener.onFailure(e);
                  }
              }
  
              @Override
              public String toString() {
                  return this.getClass().getName() + "{" + taskListener + "}{" + task + "}";
              }
  
              private void release() {
                  Releasables.close(unregisterChildNode, () -> unregister(task));
              }
          });
          return task;
      }
  }
  ```

  - `TransportAction.execute()`는 다시 sub class의 `RequestFilterChain.proceed()` method를 호출한다.
    - `server.src.main.java.org.elasticsearch.action.support.TransportAction`
    - `execute()` method에서는 전달 받은 request에 대한 validation을 수행하고, 이상 없이면 이후의 process를 실행한다.
    - `action.doExecute()`를 호출하는 데, 이 때 action은 `TransportIndexAction`이다.

  ```java
  public final void execute(Task task, Request request, ActionListener<Response> listener) {
      // 유효성 검사
      final ActionRequestValidationException validationException;
      try {
          validationException = request.validate();
      } catch (Exception e) {
          assert false : new AssertionError("validating of request [" + request + "] threw exception", e);
          logger.warn("validating of request [" + request + "] threw exception", e);
          listener.onFailure(e);
          return;
      }
      if (validationException != null) {
          listener.onFailure(validationException);
          return;
      }
      
      // (...)
      
      requestFilterChain.proceed(task, actionName, request, ActionListener.runBefore(listener, releaseRef::close));
  }
  
  
  // RequestFilterChain class
  @Override
  public void proceed(Task task, String actionName, Request request, ActionListener<Response> listener) {
      int i = index.getAndIncrement();
      try {
          if (i < this.action.filters.length) {
              this.action.filters[i].apply(task, actionName, request, listener, this);
          } else if (i == this.action.filters.length) {
              try (releaseRef) {
                  // action의 doExecute method를 실행한다.
                  this.action.doExecute(task, request, listener);
              }
          } else {
              listener.onFailure(new IllegalStateException("proceed was called too many times"));
          }
      } catch (Exception e) {
          logger.trace("Error during transport action execution.", e);
          listener.onFailure(e);
      }
  }
  ```

  - `TransportSingleItemBulkWriteAction.doExecute()`
    - `server.src.main.java.org.elasticsearch/action/bulk.TransportSingleItemBulkWriteAction`
    - `TransportIndexAction`는 `TransportSingleItemBulkWriteAction`를 상속 받는다.
    - 위 예시에서 `this.action.doExecute()`를 호출하면 `TransportSingleItemBulkWriteAction.doExeucte()` method가 실행된다.
    - `doExeucte()` method는 단일 문서 색인용으로 생성된 request를 bulk request format으로 변경하고, `TransportBulkAction.execute()`를 호출한다.
    - 결국 Elasticsearch에서는 단 건 색인도 bulk로 처리되는 것이다.

  ```java
  @Override
  protected void doExecute(Task task, final Request request, final ActionListener<Response> listener) {
      bulkAction.execute(task, toSingleItemBulkRequest(request), TransportBulkAction.unwrappingSingleItemBulkResponse(listener));
  }
  ```

  - `TransportAction.doInternalExecute()`
    - `TransportBulkAction`이 상속 받은 `TransportAction`의 `execute()` method가 다시 실행된다.
    - `execute()` method는 다시 `RequestFilterChain.proceed()` method를 호출하고, `proceed()` method는 이번에는 `TransportBulkAction.doExecute()` method를 호출한다.
  - `TransportBulkAction.doExecute()`
    - `server.src.main.java.org.elasticsearch.action.bulk.TransportBulkAction`
    - `doExecute()` method는 `ensureClusterStateThenForkAndExecute()` method를, `ensureClusterStateThenForkAndExecute()` method는 `forkAndExecute()` method를, `forkAndExecute()` method는 다시 `doInternalExecute()` method를 호출한다.
    - 최종적으로는 `createMissingIndicesAndIndexData()` 메서드가 호출된다.

  ```java
  protected void doInternalExecute(Task task, BulkRequest bulkRequest, String executorName, ActionListener<BulkResponse> listener) {
      // (...)
  
      // Bulk를 시작하기 전에 index를 먼저 생성한다.
      // 1 단계: bulkRequest에 담겨있는 모든 index 정보를 수집한다.
      final Map<String, ReducedRequestInfo> indices = bulkRequest.requests.stream()
          // 삭제 요청일 때는 index를 생성해선 안 되므로 그 부분에 대한 처리를 해준다.
          .filter(
          request -> request.opType() != DocWriteRequest.OpType.DELETE
          || request.versionType() == VersionType.EXTERNAL
          || request.versionType() == VersionType.EXTERNAL_GTE
      )
          .collect(
          Collectors.toMap(
              DocWriteRequest::index,
              request -> ReducedRequestInfo.of(request.isRequireAlias(), request.isRequireDataStream()),
              (existing, updated) -> ReducedRequestInfo.of(
                  existing.isRequireAlias || updated.isRequireAlias,
                  existing.isRequireDataStream || updated.isRequireDataStream
              )
          )
      );
  
      // 2 단계: 현재 존재하지 않는 index들을 filtering한다.
      final Map<String, IndexNotFoundException> indicesThatCannotBeCreated = new HashMap<>();
      final ClusterState state = clusterService.state();
      Map<String, Boolean> indicesToAutoCreate = indices.entrySet()
          .stream()
          .filter(entry -> indexNameExpressionResolver.hasIndexAbstraction(entry.getKey(), state) == false)
          .filter(entry -> entry.getValue().isRequireAlias == false)
          .collect(Collectors.toMap(Map.Entry::getKey, entry -> entry.getValue().isRequireDataStream));
  
      // 3 단계: bulk 전에 roll over 되어야 하는 data stream들을 수집한다.
      Set<String> dataStreamsToBeRolledOver = featureService.clusterHasFeature(state, LazyRolloverAction.DATA_STREAM_LAZY_ROLLOVER)
          ? indices.keySet().stream().filter(target -> {
          DataStream dataStream = state.metadata().dataStreams().get(target);
          return dataStream != null && dataStream.rolloverOnWrite();
      }).collect(Collectors.toSet())
          : Set.of();
  
      // Step 4: 생성해야 하는 index들을 생성하고, bulk를 실행한다.
      createMissingIndicesAndIndexData(
          task,
          bulkRequest,
          executorName,
          listener,
          indicesToAutoCreate,
          dataStreamsToBeRolledOver,
          indicesThatCannotBeCreated,
          startTime
      );
  }
  ```

  - `TransportBulkAction.createMissingIndicesAndIndexData()`
    - 먼저 생성해야 할 index가 있는지와 roll over해야 할 data stream이 없는지 확인한다.
    - 만약 없다면 바로 `executeBulk()` method를 호출하여 bulk를 계속 진행하고, 있다면 index 생성, roll over를 모두 마치고 bulk를 계속한다.

  ```java
  protected void createMissingIndicesAndIndexData(
      Task task,
      BulkRequest bulkRequest,
      String executorName,
      ActionListener<BulkResponse> listener,
      Map<String, Boolean> indicesToAutoCreate,
      Set<String> dataStreamsToBeRolledOver,
      Map<String, IndexNotFoundException> indicesThatCannotBeCreated,
      long startTime
  ) {
      final AtomicArray<BulkItemResponse> responses = new AtomicArray<>(bulkRequest.requests.size());
      // 만약 생성해야 할 index가 없고, roll over해야 할 data stream이 없다면
      if (indicesToAutoCreate.isEmpty() && dataStreamsToBeRolledOver.isEmpty()) {
          // 바로 bulk를 실행한다.
          executeBulk(task, bulkRequest, startTime, listener, executorName, responses, indicesThatCannotBeCreated);
          return;
      }
      // 만약 아니라면 index를 생성하고, data stream을 roll over한 후에 bulk를 실행한다.
      Runnable executeBulkRunnable = () -> threadPool.executor(executorName).execute(new ActionRunnable<>(listener) {
          @Override
          protected void doRun() {
              executeBulk(task, bulkRequest, startTime, listener, executorName, responses, indicesThatCannotBeCreated);
          }
      });
      try (RefCountingRunnable refs = new RefCountingRunnable(executeBulkRunnable)) {
          for (Map.Entry<String, Boolean> indexEntry : indicesToAutoCreate.entrySet()) {
              final String index = indexEntry.getKey();
              // index를 생성한다.
              createIndex(index, indexEntry.getValue(), bulkRequest.timeout(), ActionListener.releaseAfter(new ActionListener<>() {
                  // ...
              }, refs.acquire()));
          }
          for (String dataStream : dataStreamsToBeRolledOver) {
              // roll over를 실행한다.
              lazyRolloverDataStream(dataStream, bulkRequest.timeout(), ActionListener.releaseAfter(new ActionListener<>() {
  				// ...
          }
      }
  }
  ```

  - `TransportBulkAction.executeBulk()`
    - `executeBulk()` method는 `BulkOperation`의 instance를 생성한 후 해당 instance의 `run()` method를 실행한다.

  ```java
  void executeBulk(
      Task task,
      BulkRequest bulkRequest,
      long startTimeNanos,
      ActionListener<BulkResponse> listener,
      String executorName,
      AtomicArray<BulkItemResponse> responses,
      Map<String, IndexNotFoundException> indicesThatCannotBeCreated
  ) {
      new BulkOperation(
          task,
          threadPool,
          executorName,
          clusterService,
          bulkRequest,
          client,
          responses,
          indicesThatCannotBeCreated,
          indexNameExpressionResolver,
          relativeTimeProvider,
          startTimeNanos,
          listener
      ).run();
  }
  ```

  - `ActionRunnable`
    - `server.src.main.java.org.elasticsearch.action.ActionRunnable`
    - `BulkOperation`은 `ActionRunnable`을 상속 받고 `BulkOperation.run()`을 호출하면 `ActionRunnable.run()`이 실행된다.
    - `run()` method는 `ActionRunnable`의 인스턴스를 생성하여 반환하는데, 이 경우 `ActionRunnable`을 상속한 `BulkOperation` instacne가 생성된다.

  ```java
  public static <T> ActionRunnable<T> run(ActionListener<T> listener, CheckedRunnable<Exception> runnable) {
      return new ActionRunnable<>(listener) {
          @Override
          protected void doRun() throws Exception {
              runnable.run();
              listener.onResponse(null);
          }
      };
  }
  ```

  - `BulkOperation`
    - `server.src.main.java.org.elasticsearch.action.bulk.BulkOperation`
    - `doRun()` method가 실행되면 `executeBulkRequestsByShard()` method를 호출한다.
    - `executeBulkRequestsByShard()` method는 `executeBulkShardRequest()`메서드를 호출한다.
    - `executeBulkShardRequest()`메서드는 `NodeClient.executeLocally()` method를 호출한다. 

  ```java
  @Override
  protected void doRun() {
      assert bulkRequest != null;
      final ClusterState clusterState = observer.setAndGetObservedState();
      if (handleBlockExceptions(clusterState)) {
          return;
      }
      Map<ShardId, List<BulkItemRequest>> requestsByShard = groupRequestsByShards(clusterState);
      executeBulkRequestsByShard(requestsByShard, clusterState);
  }
  
  private void executeBulkRequestsByShard(Map<ShardId, List<BulkItemRequest>> requestsByShard, ClusterState clusterState) {
      if (requestsByShard.isEmpty()) {
          listener.onResponse(
              new BulkResponse(responses.toArray(new BulkItemResponse[responses.length()]), buildTookInMillis(startTimeNanos))
          );
          return;
      }
  
      // 색인 요청을 받은 node의 node ID를 받아온다.
      String nodeId = clusterService.localNode().getId();
      Runnable onBulkItemsComplete = () -> {
          listener.onResponse(
              new BulkResponse(responses.toArray(new BulkItemResponse[responses.length()]), buildTookInMillis(startTimeNanos))
          );
          bulkRequest = null;
      };
  
      try (RefCountingRunnable bulkItemRequestCompleteRefCount = new RefCountingRunnable(onBulkItemsComplete)) {
          for (Map.Entry<ShardId, List<BulkItemRequest>> entry : requestsByShard.entrySet()) {
              // 색인을 실행할 shard의 ID를 받아온다.
              final ShardId shardId = entry.getKey();
              final List<BulkItemRequest> requests = entry.getValue();
  			
              // shard의 ID를 추가하여 bulk request를 재구성한다.
              BulkShardRequest bulkShardRequest = new BulkShardRequest(
                  shardId,
                  bulkRequest.getRefreshPolicy(),
                  requests.toArray(new BulkItemRequest[0])
              );
              bulkShardRequest.waitForActiveShards(bulkRequest.waitForActiveShards());
              bulkShardRequest.timeout(bulkRequest.timeout());
              bulkShardRequest.routedBasedOnClusterVersion(clusterState.version());
              if (task != null) {
                  bulkShardRequest.setParentTask(nodeId, task.getId());
              }
              // executeBulkShardRequest method를 호출하여 벌크를 계속 진행한다.
              executeBulkShardRequest(bulkShardRequest, bulkItemRequestCompleteRefCount.acquire());
          }
      }
  }
  
  private void executeBulkShardRequest(BulkShardRequest bulkShardRequest, Releasable releaseOnFinish) {
      // 여기서 client는 BulkOperation의 property로 NodeClient class의 instance이다.
      // 이번에도 첫 번째 인자로 Action의 type을 넘기는데, 이번에는 TransportShardBulkAction.TYPE을 넘긴다.
      client.executeLocally(TransportShardBulkAction.TYPE, bulkShardRequest, new ActionListener<>() {
          @Override
          public void onResponse(BulkShardResponse bulkShardResponse) {
              for (BulkItemResponse bulkItemResponse : bulkShardResponse.getResponses()) {
                  // we may have no response if item failed
                  if (bulkItemResponse.getResponse() != null) {
                      bulkItemResponse.getResponse().setShardInfo(bulkShardResponse.getShardInfo());
                  }
                  responses.set(bulkItemResponse.getItemId(), bulkItemResponse);
              }
              releaseOnFinish.close();
          }
  
          @Override
          public void onFailure(Exception e) {
              // create failures for all relevant requests
              for (BulkItemRequest request : bulkShardRequest.items()) {
                  final String indexName = request.index();
                  DocWriteRequest<?> docWriteRequest = request.request();
                  BulkItemResponse.Failure failure = new BulkItemResponse.Failure(indexName, docWriteRequest.id(), e);
                  responses.set(request.id(), BulkItemResponse.failure(request.id(), docWriteRequest.opType(), failure));
              }
              releaseOnFinish.close();
          }
      });
  }
  ```

  - `NodeClient`
    - `executeLocally()` method는 `TaskManager.registerAndExecute()` method를 호출한다.
    - 이 때, 위에서 받아온 action 정보(`TransportShardBulkAction.TYPE`)를 가지고 이번에는 `TransportShardBulkAction`을 인자로 넘긴다.
    - `TaskManager.registerAndExecute()` method는 task를 등록하고, 인자로 받은 action(`TransportShardBulkAction`)의 `execute()` method를 호출한다.
    - `execute()` 메서드가 호출되면, `TransportShardBulkAction`가 상속 받은 `TransportAction.execute()`가 실행된다.
    - `TransportAction.execute()`가 실행되면서 sub class인 `RequestFilterChain`의 `proceed()` method를 호출한다.
    - `RequestFilterChain.proceed()` method가 호출되면서 `doExecute()` method가 호출된다.
    - `TransportShardBulkAction`은 `TransportWriteAction`을 상속 받고, `TransportWriteAction`은 `TransportReplicationAction`을 상속 받는다.
    - 앞의 두 class에 `doExecute()` method가 없으므로, `TransportReplicationAction.doExecute()` 메서드가 호출된다.
  - `TransportReplicationAction`
    - `server.src.main.java.org.elasticsearch.action.support.replication.TransportReplicationAction`
    - `doExecute()` method는 `runReroutePhase()` 메서드를 호출한다.
    - `runReroutePhase()` 메서드가 호출되면 `TransportReplicationAction`의 sub class인 `ReroutePhase`의 인스턴스를 생성하고, `ReroutePhase.run()` 메서드를 호출한다.
    - `ReroutePhase`는 `AbstractRunnable`을 상속받는데, `ReroutePhase`에는 `run()` method가 없어 `AbstractRunnable.run()` 메서드가 실행된다.
    - `AbstractRunnable.run()` method가 실행되면서, `ReroutePhase.doRun()` method를 호출한다.
    - `ReroutePhase.doRun()` method는 `performRemoteAction` method를 호출한다.
    - `performRemoteAction()` method는 `performAction()` method를 호출한다.
    - `performAction()` method는 다시 `TransportService.sendRequest()` method를 호출한다.
    - `TransportService.sendRequest()`는 마지막 인자로 `TransportResponseHandler`의 instance를 받는다.

  ```java
  private void performAction(
      final DiscoveryNode node,
      final String action,
      final boolean isPrimaryAction,
      final TransportRequest requestToPerform
  ) {
      // TransportResponseHandler의 instance를 인자로 받는다.
      transportService.sendRequest(node, action, requestToPerform, transportOptions, new TransportResponseHandler<Response>() {
  
          @Override
          public Response read(StreamInput in) throws IOException {
              return newResponseInstance(in);
          }
  
          @Override
          public Executor executor() {
              return TransportResponseHandler.TRANSPORT_WORKER;
          }
  
          @Override
          public void handleResponse(Response response) {
              finishOnSuccess(response);
          }
  
          @Override
          public void handleException(TransportException exp) {
              // ...
          }
      });
  }
  ```

  - `TransportService.sendRequest()`
    - `server.src.main.java.org.elasticsearch.transport.TransportService`
    - `TransportService.sendRequest()`는 overloading된 다른 `sendrequest()`를 호출한다.
    - `sendrequest()`는 `asyncSender.sendRequest()` method를 호출하고, 그 결과 `sendRequestInternal()` method가 호출된다.
    - `sendRequestInternal()`는 인자로 받은 `Transport.Connection` instance의 `sendRequest()` method를 호출한다.
    - 그 결과 `sendLocalRequest()` method가 호출된다.

  ```java
  volatile DiscoveryNode localNode = null;
      private final Transport.Connection localNodeConnection = new Transport.Connection() {
          @Override
          public DiscoveryNode getNode() {
              return localNode;
          }
  
          @Override
          public TransportVersion getTransportVersion() {
              return TransportVersion.current();
          }
  
          @Override
          public void sendRequest(long requestId, String action, TransportRequest request, TransportRequestOptions options) {
              sendLocalRequest(requestId, action, request, options);
          }
          // ...
      };
  
  // ...
  
  public final <T extends TransportResponse> void sendRequest(
      final DiscoveryNode node,
      final String action,
      final TransportRequest request,
      final TransportRequestOptions options,
      TransportResponseHandler<T> handler
  ) {
      // connector는 만약 색인 대상 node가 local node면 localNode attribute를 반환하고, 아니라면 ConnectionManager.getConnection()를 통해 connection을 받아온다.
      final Transport.Connection connection = getConnectionOrFail(node, action, handler);
      if (connection != null) {
          // overloading된 다른 sendRequest method가 실행된다.
          sendRequest(connection, action, request, options, handler);
      }
  }
  ```

  - `TransportService.sendLocalRequest()`
    - `sendLocalRequest`는 `Executor.execute()` method를 호출한다.
    - `Executor.execute()` method는 `AbstractRunnable` instance를 생성한다.
    - `AbstractRunnable` instance를 생성할 때, `doRun()` method를 구현하는데, `doRun()`는 `RequestHandlerRegistry.processMessageReceived` method를 실행한다.

  ```java
  private void sendLocalRequest(long requestId, final String action, final TransportRequest request, TransportRequestOptions options) {
      final DirectResponseChannel channel = new DirectResponseChannel(localNode, action, requestId, this);
      try {
          onRequestSent(localNode, requestId, action, request, options);
          onRequestReceived(requestId, action);
          @SuppressWarnings("unchecked")
          // registry를 가져온다.
          final RequestHandlerRegistry<TransportRequest> reg = (RequestHandlerRegistry<TransportRequest>) getRequestHandler(action);
          
          // ...
          // executor를 가져온다.
          final Executor executor = reg.getExecutor();
          if (reg == null) {
             // ...
          } else {
              boolean success = false;
              request.mustIncRef();
              try {
                  // AbstractRunnable instance를 생성한다.
                  executor.execute(threadPool.getThreadContext().preserveContextWithTracing(new AbstractRunnable() {
                      @Override
                      protected void doRun() throws Exception {
                          reg.processMessageReceived(request, channel);
                      }
                      // ...
                  }));
                  success = true;
              } finally {
                  if (success == false) {
                      request.decRef();
                  }
              }
          }
      // ...
  }
  ```

  - `RequestHandlerRegistry`
    - `server.src.main.java.org.elasticsearch.transport.RequestHandlerRegistry`
    - `RequestHandlerRegistry.processMessageReceived()`는 `ProfileSecuredRequestHandler.messageReceived()`를 호출한다.
    - `ProfileSecuredRequestHandler.messageReceived()`는 다시 `getReceiveRunnable()` method를 통해 생성한 `AbstractRunnable` instance의 `run()` method를 호출한다.
    - `AbstractRunnable.run()`이 호출되면 `doRun()` method를 실행한다.
    - `getReceiveRunnable()` method를 통해 `AbstractRunnable` instance를 생성할 때, `doRun` method를 설정해주는 데, 이 때 `doRun` method가 실행되면 `TransportReplicationAction.handlePrimaryRequest`를 실행하도록 설정된다.
    - `TransportReplicationAction.handlePrimaryRequest`가 실행되는 이유는 `TransportReplicationAction` instance가 초기화 될 때, `TransportService`의 instance에 `registerRequestHandler()` method를 통해 여러 action들을 등록해주는데, `handlePrimaryRequest` method가 그 때 등록되기 때문이다.

  - `TransportReplicationAction`
    - `handlePrimaryRequest()` method가 실행되면 `AsyncPrimaryAction`의 instance를 생성하고, `AsyncPrimaryAction.run()` method를 실행한다.
    - `AsyncPrimaryAction.run()` method는 `AsyncPrimaryAction.doRun()` method를 실행한다.
    - `AsyncPrimaryAction.doRun()` method는 `AsyncPrimaryAction.runWithPrimaryShardReference` method를 실행한다.
    - `AsyncPrimaryAction.runWithPrimaryShardReference` method는 `ReplicationOperation` instance를 생성하고, 해당 instance의 `execute()` method를 실행한다.
  - `ReplicationOperation`
    - `server.src.main.java.org.elasticsearch.action.support.replication.ReplicationOperation`
    - `ReplicationOperation.execute()` method는 `TransportAction`의 서브 클래스인 `PrimaryShardReference`의 `perform()` method를 호출한다.
    - `PrimaryShardReference.perform`은 다시 `TransportWriteAction.shardOperationOnPrimary()` method를 호출한다.
  - `TransportShardBulkAction`
    - `TransportWriteAction.shardOperationOnPrimary()` method는 `TransportShardBulkAction.dispatchedShardOperationOnPrimary()` method를 호출한다.
    -  `TransportShardBulkAction.dispatchedShardOperationOnPrimary()` 는 다시 `performOnPrimary()` method를 호출한다.
    -  `performOnPrimary()`는 `ActionRunnable` instance를 생성한 뒤 해당 instance의 `run` method를 실행한다.
    - `ActionRunnable.run()`은 `ActionRunnable.doRun()` method를 실행하고, `doRun()` method는 `executeBulkItemRequest()` method를 실행한다.
    - `executeBulkItemRequest()` method는 실행되면서 `IndexShard.applyIndexOperationOnPrimary()` method를 실행한다.

  ```java
  public static void performOnPrimary(
      BulkShardRequest request,
      IndexShard primary,
      UpdateHelper updateHelper,
      LongSupplier nowInMillisSupplier,
      MappingUpdatePerformer mappingUpdater,
      Consumer<ActionListener<Void>> waitForMappingUpdate,
      ActionListener<PrimaryResult<BulkShardRequest, BulkShardResponse>> listener,
      ThreadPool threadPool,
      String executorName,
      @Nullable PostWriteRefresh postWriteRefresh,
      @Nullable Consumer<Runnable> postWriteAction,
      DocumentParsingProvider documentParsingProvider
  ) {
      // ActionRunnable instance를 생성한다.
      new ActionRunnable<>(listener) {
  
          private final Executor executor = threadPool.executor(executorName);
  
          private final BulkPrimaryExecutionContext context = new BulkPrimaryExecutionContext(request, primary);
  
          final long startBulkTime = System.nanoTime();
  		
          // ActionRunnable instance의 doRun() method를 설정한다.
          @Override
          protected void doRun() throws Exception {
              // 실행할 operation이 더 남아있지 않을 때 까지 operation을 실행하다.
              while (context.hasMoreOperationsToExecute()) {
                  // executeBulkItemRequest method를 호출하여 색인을 진행한다.
                  if (executeBulkItemRequest(
                      context,
                      updateHelper,
                      nowInMillisSupplier,
                      mappingUpdater,
                      waitForMappingUpdate,
  
                      ActionListener.wrap(v -> executor.execute(this), this::onRejection),
                      documentParsingProvider
                  ) == false) {
                      // We are waiting for a mapping update on another thread, that will invoke this action again once its done
                      // so we just break out here.
                      return;
                  }
                  assert context.isInitial(); // either completed and moved to next or reset
              }
              primary.getBulkOperationListener().afterBulk(request.totalSizeInBytes(), System.nanoTime() - startBulkTime);
              // We're done, there's no more operations to execute so we resolve the wrapped listener
              finishRequest();
          }
          // ...
      }.run();	// 실행한다.
  }
  ```

  - `IndexShard`
    - `server.src.main.java.org.elasticsearch.index.shard.IndexShard`
    - `applyIndexOperationOnPrimary()` method는 실행되면서 `applyIndexOperation` method를 호출한다.
    - `applyIndexOperation()` method는 실행되면서 `index()` method를 호출한다.
    - `index()` method가 실행되면서, 인자로 받은 `InternalEngine` instance의 `index()` method를 실행한다.

  ```java
  private Engine.IndexResult index(Engine engine, Engine.Index index) throws IOException {
          try {
              final Engine.IndexResult result;
              final Engine.Index preIndex = indexingOperationListeners.preIndex(shardId, index);
              try {
                  // ...
                  // Engine.index() method를 실행한다.
                  result = engine.index(preIndex);
                  // ...
          } finally {
              active.set(true);
          }
      }
  ```

  - `InternalEngine`
    - `server.src.main.java.org.elasticsearch.index.engine.InternalEngine`
    - `index()` method는 실행되면서 `indexIntoLucene()` method를 호출한다.
    - `indexIntoLucene()`method가 실행되면서 `addDocs()` method를 호출한다.
    - `addDocs()` method는 색인하려는 문서의 숫자에 따라 Lucene의 `IndexWriter.addDocuments()` 혹은 `IndexWriter.addDocument()` 중 하나의 method를 실행한다.











