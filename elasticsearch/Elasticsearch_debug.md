- 아래와 같이 Elasticsearch debugging용 container를 생성하기 위한 Dockerfile을 작성한다.

  - Elasticsearch에 Gradle wrapper가 포함되어 있어 Gradle은 설치하지 않아도 된다.

  ```dockerfile
  FROM ubuntu:22.04
  
  ENV DEBIAN_FRONTEND=noninteractive
  
  RUN ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime
  
  RUN apt-get update
  
  RUN apt-get install curl -y openjdk-17-jdk -y git
  
  RUN groupadd -g 999 es
  
  RUN useradd -r -u 999 -g es es
  
  RUN chmod 777 /home
  
  USER es
  
  WORKDIR /home
  
  RUN git clone https://github.com/elastic/elasticsearch.git
  
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

  ```bash
  $ cd /home/elasticssearch
  $ ./gradlew run
  ```

  - 실행 해봤으나 아래와 같은 error가 발생하면서 build에 실패한다.

  ```bash
  process was found dead while waiting for ports files, node{::runTask-0}
  ```

  - 아래 문서 참고해서 다시 시도해볼것

  > https://github.com/elastic/elasticsearch/blob/main/TESTING.asciidoc
  >
  > https://github.com/elastic/elasticsearch/blob/main/CONTRIBUTING.md

  