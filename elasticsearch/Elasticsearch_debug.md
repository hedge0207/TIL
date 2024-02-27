# Debug Elasticsearch

## Container 준비

- Elasticsearch debugging용 Docker container 생성하기

  - Ubuntu image를 pull 받는다.

  ```bash
  $ docker pull ubuntu:22.04
  ```

  - Dockerfile을 작성한다.

    - Elasticsearch에 Gradle wrapper가 포함되어 있어 Gradle은 설치하지 않아도 된다.

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

  - Elasticsearch를 clone 받은 directory로 이동 후 `gradlew run`을 실행한다.
    - 최초 실행시 자동으로 gradle을 설치한다.


  ```bash
  $ cd elasticssearch
  $ ./gradlew run
  ```

  - 만일 root user로 실행할 경우 아래와 같은 error가 발생하므로 반드시 일반 user로 실행해야한다.

  ```bash
  process was found dead while waiting for ports files, node{::runTask-0}
  ```

  - 아래와 같은 message가 출력되면 정상적으로 실행된 것이다.

  ```bash
  [2024-02-27T14:50:35,167][INFO ][o.e.h.AbstractHttpServerTransport] [runTask-0] publish_address {127.0.0.1:9200}, bound_addresses {[::1]:9200}, {127.0.0.1:9200}
  [2024-02-27T14:50:35,169][INFO ][o.e.n.Node               ] [runTask-0] started
  ```

  - 정상적으로 동작하는지 확인하기
    - Elasticsearch 8부터는 security 기능이 자동으로 활성화 된 상태이기 때문에 `-u` option으로 user와 password를 입력해야한다.
    - 기본 user/password는 elastic/password이다.

  ```bash
  $ curl -u elastic:password localhost:9200
  
  ```





## UUID 생성 과정

- Elasticsearch의 UUID가 생성되는 과정은 에서 확인 할 수 있다.

  - 편의를 위해 하나로 묶으면 아래와 같다.

  ```java
  package org.example;
  
  import java.net.NetworkInterface;
  import java.net.SocketException;
  import java.util.Base64;
  import java.security.SecureRandom;
  import java.util.Enumeration;
  import java.util.concurrent.atomic.AtomicInteger;
  /**
   * These are essentially flake ids but we use 6 (not 8) bytes for timestamp, and use 3 (not 2) bytes for sequence number. We also reorder
   * bytes in a way that does not make ids sort in order anymore, but is more friendly to the way that the Lucene terms dictionary is
   * structured.
   * For more information about flake ids, check out
   * https://archive.fo/2015.07.08-082503/http://www.boundary.com/blog/2012/01/flake-a-decentralized-k-ordered-unique-id-generator-in-erlang/
   */
  
  class MacAddressProvider {
  
      private static byte[] getMacAddress() throws SocketException {
          Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
          if (en != null) {
              while (en.hasMoreElements()) {
                  NetworkInterface nint = en.nextElement();
                  if (!nint.isLoopback()) {
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
  
          if (!isValidAddress(address)) {
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
  
  class SecureRandomHolder {
      // class loading is atomic - this is a lazy & safe singleton to be used by this package
      public static final SecureRandom INSTANCE = new SecureRandom();
  }
  
  class TimeBasedUUIDGenerator {
  
      // We only use bottom 3 bytes for the sequence number.  Paranoia: init with random int so that if JVM/OS/machine goes down, clock slips
      // backwards, and JVM comes back up, we are less likely to be on the same sequenceNumber at the same time:
      private final AtomicInteger sequenceNumber = new AtomicInteger(SecureRandomHolder.INSTANCE.nextInt());
  
      // Used to ensure clock moves forward:
      private long lastTimestamp;
  
      private static final byte[] SECURE_MUNGED_ADDRESS = MacAddressProvider.getSecureMungedAddress();
  
      static {
          assert SECURE_MUNGED_ADDRESS.length == 6;
      }
  
      // protected for testing
      protected long currentTimeMillis() {
          return System.currentTimeMillis();
      }
  
      // protected for testing
      protected byte[] macAddress() {
          return SECURE_MUNGED_ADDRESS;
      }
  
      public String getBase64UUID() {
          final int sequenceId = sequenceNumber.incrementAndGet() & 0xffffff;
          long timestamp = currentTimeMillis();
  
          synchronized (this) {
              // Don't let timestamp go backwards, at least "on our watch" (while this JVM is running).  We are still vulnerable if we are
              // shut down, clock goes backwards, and we restart... for this we randomize the sequenceNumber on init to decrease chance of
              // collision:
              timestamp = Math.max(lastTimestamp, timestamp);
  
              if (sequenceId == 0) {
                  // Always force the clock to increment whenever sequence number is 0, in case we have a long time-slip backwards:
                  timestamp++;
              }
  
              lastTimestamp = timestamp;
          }
  
          final byte[] uuidBytes = new byte[15];
          int i = 0;
  
          // We have auto-generated ids, which are usually used for append-only workloads.
          // So we try to optimize the order of bytes for indexing speed (by having quite
          // unique bytes close to the beginning of the ids so that sorting is fast) and
          // compression (by making sure we share common prefixes between enough ids),
          // but not necessarily for lookup speed (by having the leading bytes identify
          // segments whenever possible)
  
          // Blocks in the block tree have between 25 and 48 terms. So all prefixes that
          // are shared by ~30 terms should be well compressed. I first tried putting the
          // two lower bytes of the sequence id in the beginning of the id, but compression
          // is only triggered when you have at least 30*2^16 ~= 2M documents in a segment,
          // which is already quite large. So instead, we are putting the 1st and 3rd byte
          // of the sequence number so that compression starts to be triggered with smaller
          // segment sizes and still gives pretty good indexing speed. We use the sequenceId
          // rather than the timestamp because the distribution of the timestamp depends too
          // much on the indexing rate, so it is less reliable.
  
          uuidBytes[i++] = (byte) sequenceId;
          // changes every 65k docs, so potentially every second if you have a steady indexing rate
          uuidBytes[i++] = (byte) (sequenceId >>> 16);
  
          // Now we start focusing on compression and put bytes that should not change too often.
          uuidBytes[i++] = (byte) (timestamp >>> 16); // changes every ~65 secs
          uuidBytes[i++] = (byte) (timestamp >>> 24); // changes every ~4.5h
          uuidBytes[i++] = (byte) (timestamp >>> 32); // changes every ~50 days
          uuidBytes[i++] = (byte) (timestamp >>> 40); // changes every 35 years
          byte[] macAddress = macAddress();
          assert macAddress.length == 6;
          System.arraycopy(macAddress, 0, uuidBytes, i, macAddress.length);
          i += macAddress.length;
  
          // Finally we put the remaining bytes, which will likely not be compressed at all.
          uuidBytes[i++] = (byte) (timestamp >>> 8);
          uuidBytes[i++] = (byte) (sequenceId >>> 8);
          uuidBytes[i++] = (byte) timestamp;
  
          assert i == uuidBytes.length;
  
          return Base64.getUrlEncoder().withoutPadding().encodeToString(uuidBytes);
      }
  }
  
  
  class Main {
      public static void main(String[] args) {
          TimeBasedUUIDGenerator uuidGenerator = new TimeBasedUUIDGenerator();
          for (int i = 0; i < 10; i++) {
              System.out.println(uuidGenerator.getBase64UUID());
          }
      }
  }
  ```

  



