# Jenkins

- Jenkins Docker로 설치하기

  - Bridge network를 생성한다.
  
  ```bash
  $ docker network create jenkins
  ```
  
  - Jenkins node 내부에서 docker를 실행하기 위해 `docker:dind` image를 사용한다.
  
  ```bash
  $ docker image pull docker:dind
  ```

  - `docker:dind` image를 아래와 같이 실행한다.
    - `--privileged`: DinD를 위해서는 privileged 옵션을 줘야한다.
    - `--network`: 위에서 생성한 network를 입력한다.
    - `--network-alias`: 위에서 생성한 `jenkins` 네트워크 내부에서 `docker`라는 hostname을 사용한다.
    - `--env DOCKER_TLS_CERTDIR`: DinD를 위해 `--privileged` 옵션을 줬으므로, 보안을 위해 TLS를 사용해야 하므로, `DOCKER_TLS_CERTDIR` 환경 변수로 Docker TLS 인증서들의 root directory를 설정한다.
    - 다른 다른 container에서 `jenkins-docker` container의 docker deamon을 사용할 수 있도록 client용 인증서를 호스트 머신에 복사한다.
    - `jenkins-docker` container와 이후에 띄울 `jenkins` container가 데이터를 공유할 수 있도록 호스트 머신에 복사한다.
  
  ```bash
  $ docker run \
  --name jenkins-docker \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume /some/path/jenkins-docker-certs:/certs/client \
  --volume /some/path/jenkins_home:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind
  ```
  
  - Docker hub에서 Jenkins official image를 다운 받는다.
    - 아래 image에는 blue ocean이 설치되어 있지 않으므로, blue ocean을 사용하려면, jenkins instance 생성 후 설치하거나, image를 다시 빌드해서 사용해야한다.
  
  ```bash
  $ docker pull jenkins/jenkins
  ```
  
  - 위에서 받은 jenkins docker image를 custom한다.
    - Dockerfile을 아래와 같이 작성 후 build한다.
  
  ```dockerfile
  FROM jenkins/jenkins:2.401.1
  
  USER root
  
  RUN apt-get update && apt-get install -y lsb-release
  RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg
  RUN echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
  
  # docker cli를 설치한다.
  RUN apt-get update && apt-get install -y docker-ce-cli
  
  USER jenkins
  
  # plugin들을 설치한다.
  RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
  ```
  
  - Jenkins container를 실행한다.
    - `--network`에는 `jenkins-docker` container와 동일한 network로 묶이도록 위에서 생성한 network를 입력한다.
    - `jenkins-docker`의 docker deamon을 사용하기 위해 `DOCKER_HOST`, `DOCKER_CERT_PATH`, `DOCKER_TLS_VERIFY` 환경 변수를 설정한다.
    - `jenkins-docker`에서 설정한 것과 동일한 host machine의 경로로 volume을 설정한다.
    - 만일 volume permission 문제로 실행이 되지 않는다면 host 경로의 소유자를 `sudo chown 1000 <path>`를 통해 super user로 변경한다.
  
  
  ```bash
  $ docker run \
  --name jenkins-blueocean \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume /some/path/jenkins_home:/var/jenkins_home \
  --volume /some/path/jenkins-docker-certs:/certs/client:ro \
  <위에서 build한 jenkins image명>:<version>
  ```
  
  - 관리 page 접속하기
    - 관리 page 용 port(위의 경우 8080)로 `<host>:<port>`와 같이 접속하면 Getting Started page로 연결되고, administrator password를 입력하라고 나온다.
    - Administrator password는 docker를 실행시킬 때 log에 출력이 되며, 만일 이 때 보지 못했다면, `/var/jenkins_home/secrets/initialAdminPassword` 경로에서 확인하면 된다.
    - Jenkins 실행시 자동으로 관리자 권한을 가진 admin이라는 이름의 user를 생성하는데, 해당 user의 password도 administrator password를 사용하면 된다.
    - 그 후 설치할 plugin을 선택하는 화면이 나오는데, 그냥 건너 뛰거나 suggested pluin만 설치하면 된다.
    - 만일 이 때 설치하지 못 한 plugin이 있더라도 추후에 관리 page의 `Manage Jenkins` - `Plugins`에서 설치가 가능하다.
    - 만일 그냥 건너뛰지 않고 plugin을 설치했다면, Admin 계정을 생성하는 창이 나오고, 그 이후에는 URL을 설정하는 창이 나오는데 모두 설정하고 나면 관리 page로 이동된다.



- Jenkins pipeline 생성하기

  - Jenkins Pipline(Pipeline)이란
    - Jenkins에서 CD(Continuous delivery) pipeline을 구현하고 통합하는 플러그인들의 모음이다.
  - Docker, Docker Pipeline plugin을 설치한다.
    - `Manage Jenkins`> `Plugins` page에서 설치할 수 있다.
    - 설치후 Jenkins를 재실행해야한다.
  - 아래 내용을 `Jenkinsfile`에 입력한 후 git으로 관리중인 repository의 root directory에 저장한다.
  
  ```groovy
  pipeline {
      agent { docker { image 'python:3.8.0' } }
      stages {
          stage('build') {
              steps {
                  sh 'python --version'
              }
          }
      }
  }
  ```
  
    - `New Item`을 클릭한 후 `Multibranch Pipeline`을 선택한다.
      - `Branch Sources`에서 Add Source를 눌러 github credential 설정과 repository를 설정한다.
      - Credentials의 Username에는 github username입력하고, password에는 github access token을 입력하면 된다.
      - 그 후 Save를 누르면 자동으로 실행된다.
