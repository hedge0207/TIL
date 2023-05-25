

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

  - Elasticsearch 실행하기
    - elasticsearch를 clone 받은 directory에서 아래 명령어를 수행한다.
    - 이 때 9200, 9300 port를 사용 중인 process가 있을 경우 error가 발생한다.
    - 만일 실패할 경우 `./gradlew clean`을 수행한 후 다시 실행한다.

  ```bash
  $ ./gradlew :run
  ```

  - 정상적으로 실행 됐는지 확인하기

  ```bash
  $ curl -u elastic:password localhost:9200
  ```

  

