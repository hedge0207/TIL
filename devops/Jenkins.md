# Jenkins tutorial

- Jenkins Docker로 설치하기

  - Host machine의 docker deamon을 사용하지 않고 docker container 내부에 docker container를 띄우는 방식(DinD)을 사용한다.
    - 따라서 Docker를 실행하기 위한 container와 Jenkins container 2개의 container를 생성해야한다.
    - Jenkins container에서 실행되는 docker 명령어는 Docker를 실행하기 위한 container에서 실행되며, Jenkins container에서 새로운 image나 container 생성시 Docker를 실행하기 위한 container 내부에 생성된다.
  
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



- Jenkins pipeline 생성해보기

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
      - Credentials의 username에는 github username입력하고, password에는 github access token을 입력하면 된다.
      - 그 후 Save를 누르면 자동으로 실행된다.
    - 실행하면 위에서 입력한대로 python version이 출력되는 것을 확인할 수 있다.





# Jenkins로 application 관리하기

- 배포용 applicaction 생성하기

  - 배포할 application을 생성한다.

  ```python
  # main.py
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  @app.get("/")
  def hello_world():
      return "Hello World!"
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0")
  ```

  - Application을 실행하기 위한 requirements 파일을 작성한다.

  ```bash
  $ pip freeze > requirements.txt
  ```

  - Application을 build하기 위한 Dockerfile을 작성한다.

  ```dockerfile
  FROM python:3.8.0
  
  RUN mkdir /app
  COPY . /app
  WORKDIR /app
  
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  CMD ["python", "main.py"]
  ```

  - 배포를 위한 Jenkinsfile을 작성한다.
    - 먼저 위에서 작성한 Dockerfile을 기반으로 application을 build한다.
    - 그 후 build한 image로 container를 생성한다.

  ```groovy
  pipeline {
      agent any
      stages {
          stage('build') {
              steps {
                  sh 'docker build -t jenkins-test-app .'
              }
          }
          stage('deploy') {
              steps {
                  sh 'docker run -d -p 8000:8000 --name jenkins-test-app jenkins-test-app'
              }
          }
      }
  }
  ```

  - 최종 directory는 아래와 같다.

  ```
  app
  ├── main.py
  ├── requirements.txt
  ├── Dockerfile
  ├── Jenkinsfile
  └── README.md
  ```

  - 위 directory를 github에 push한다.



- 기존에 띄웠던 `jenkins-docker` container 수정하기

  - 외부에서 `jenkins-docker` container 내부에 생성되는 application container에 접근하기 위해 port를 publish해야한다.
    - 기존과 동일하게 하되, `--publish 8000:8000`를 추가한다.

  ```sh
  $ docker run \
  --name jenkins-docker \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume /some/path/jenkins-docker-certs:/certs/client \
  --volume /some/path/jenkins_home:/var/jenkins_home \
  --publish 2376:2376 \
  --publish 8000:8000
  docker:dind
  ```

  - Jenkins container는 수정할 필요가 없다.



- Jenkins pipeline을 구성한 후 실행하면 `jenkins-docker` container 내부에  `jenkins-test-app` container가 생성된 것을 확인할 수 있다.

  - `jenkins-docker` container 내부로 접속하기

  ```bash
  $ docker exec -it jenkins-docer /bin/sh
  ```

  - Application container가 생성 되었는지 확인

  ```bash
  $ docker ps
  ```

  - 생성된 application container에 요청을 보내본다.

  ```bash
  $ curl <host>:8000
  ```



- Github repository에 Push가 발생할 때 마다 자동으로 배포하기
  - Jenkins에 `Multibranch Scan Webhook Trigger` plugin을 설치한다.
    - 위에서 사용한 multi branch pipeline은 기본적으로 webhook trigger를 지원하지 않기에, plugin을 설치해야한다.
    - `Manage Jenkins` - `Plugins`에서 `Multibranch Scan Webhook Trigger`을 찾아 설치한다.
  - 기존 pipeline에 webhook 관련 설정을 추가한다.
    - 이제 pipeline 설정으로 이동하면, `Scan Repository Triggers`에 이전에는 없던 `Scan by webhook`이 생겼을 것이다.
    - `Scan by webhook`을 체크하면, `Trigger token`을 입력해야하는데, 원하는 형식으로 token 값을 입력한다(e.g. my-token)
  - Github repository에서 webhook을 설정한다.
    - Github repository의 `Settings`  > `Webhooks`로 이동하여 `Add webhook`을 클릭한다.
    - `Payload URL`에는 `http://<Jenkins url>/multibranch-webhook-trigger/invoke?token=<위에서 설정한 trigger token>`을 입력한다.
    - `Content type`은 `application/json`으로 설정한다.















