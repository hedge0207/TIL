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
    - `--env DOCKER_TLS_CERTDIR`: DinD를 위해 `--privileged` 옵션을 줬으므로, 보안을 위해 TLS를 사용해야 한다. 따라서 `DOCKER_TLS_CERTDIR` 환경 변수로 Docker TLS 인증서들의 root directory를 설정한다.
    - 다른 container에서 `jenkins-docker` container의 docker deamon을 사용할 수 있도록 client용 인증서를 호스트 머신에 복사한다.
    - `jenkins-docker` container와 이후에 띄울 `jenkins` container가 데이터를 공유할 수 있도록 호스트 머신에 복사한다.
    - 2376 port는 docker daemon과 통신을 위한 port이다.
  
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
    - 아래 image는 Docker client만 설치된 상태로, 위에서 생성한 `jenkins-docker`의 Docker daemon으로 요청을 보낸다.
  
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



- Jenkins Pipeline 생성해보기

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





# Jenkins Pipeline

- Jenkins Pipeline(Pipeline, P를 대문자로 써야 한다)
  - CD pipeline을 구현하고 통합하는데 도움을 주는 plugin들의 모음이다.
  - 여러 종류의 tool들을 지원하며, Pipeline DSL syntax를 사용한다.
  - Jenkins Pipeline은 Jenkinsfile이라 불리는 text file로 정의된다.
    - Jenkinsfile은 프로젝트의 source control repository에 작성한다.
  - Jenkinsfile을 프로젝트의 source control repository에 함께 작성함으로써 아래와 같은 이점을 누릴 수 있다.
    - 모든 branch와 pull request에 대해서 Pipeline build process를 자동으로 생성할 수 있다.
    - Pipeline의 변경 이력을 추적할 수 있다.
    - 프로젝트를 진행하는 모든 팀원이 확인하고 편집할 수 있다.
  - Jenkinsfile은 Declarative와 Scripted라는 두 종류의 syntax로 작성할 수 있다.
    - Declarative Pipeline이 Scripted Pipeline보다 최근에 나온 방식이다.
    - Declarative Pipeline이보다 풍부한 기능을 제공하며, 읽고 쓰기도 더 쉽다.



- Pipeline과 관련된 개념들
  - Pipeline
    - CD pipeline을 사용자가 정의한 model이다.
    - Pipeline의 code는 build하고 test하고, 배포하는 전체 build process를 정의한다.
  - Node
    - Pipeline을 실행하는 machine을 의미한다.
  - Stage
    - 전체 Pipeline에서 실행되는 task들을 정의하는 부분이다.
  - Step
    - 하나의 task를 의미한다.
    - 각 단계에서 무엇을 해야 하는지 Jenkins에게 알려주는 역할을 한다.



- Pipeline overview

  - Declarative Pipeline

  ```groovy
  pipeline {
      agent any 
      stages {
          // Build를 위한 stage를 정의한다.
          stage('Build') { 
              steps {
                  // 
              }
          }
          // Test를 위한 stage를 정의한다.
          stage('Test') { 
              steps {
                  // 
              }
          }
          // Deploy를 위한 stage를 정의한다.
          stage('Deploy') { 
              steps {
                  // 
              }
          }
      }
  }
  ```

  - Scripted Pipeline
    - Scripted Pipeline에서는 `node ` block이 최상단에 위치한 것을 볼 수 있다.
    - Scripted Pipeline 방식에서 `node` block이 필수적인 것은 아니지만, Pipeline에서 수행할 작업을 `node` block에 넣으면 아래와 같이 동작한다.
    - Jenkins queue에 step들을 추가하는 방식으로 step들을 스케쥴링하며, node의 executor가 수행하는 작업이 없을 경우, step들이 수행된다.

  ```groovy
  node {  
      stage('Build') { 
          // 
      }
      stage('Test') { 
          // 
      }
      stage('Deploy') { 
          // 
      }
  }
  ```



- Pipeline(Jenkinsfile)은 세 가지 방법으로 정의할 수 있다.
  - Blue Ocean을 사용하는 방법
    - Pipeline을 간편하게 구성할 수 있도록 해주는 Blue Ocean plugin을 사용하는 방식이다.
  - Classic UI를 사용하는 방법
    - 본래 Jenkins에서 제공하는 UI를 사용하는 방식이다.
  - SCM을 사용하는 방법
    - Jenkinsfile을 수동으로 작성하는 방식이다.
    - UI를 사용해서 구성하기 힘든, 복잡한 Pipeline을 구성할 때 사용한다.



## Jenkinsfile

> 아래 내용은 이미 source code를 저장할 repository와 Jenkins Pipeline이 생성되었다고 가정한다.

- Jenkinsfile 개요

  - Jenkinsfile의 기본 구조는 아래와 같다.
    - 꼭 아래와 같이 많은 stage들이 있어야 하는 것은 아니지만, 아래와 같은 구조가 가장 기본적인 형태이다.
    - 각각의 keyword(`agent`, `stages` 등)을 directive라고 부른다.

  ```groovy
  pipeline {
      agent any
  
      stages {
          stage('Build') {
              steps {
                  echo 'Building..'
              }
          }
          stage('Test') {
              steps {
                  echo 'Testing..'
              }
          }
          stage('Deploy') {
              steps {
                  echo 'Deploying....'
              }
          }
      }
  }
  ```

  - `agent`
    - 필수 값으로 Jenkins가 Pipeline을 위한 executor와 workspace를 할당하도록 하는 역할을 한다.
    - 또한 source repository를 check하고 이후의 stage들이 실행될 수 있도록 해준다.
    - 필수 값이므로 설정하지 않았을 경우 Pipeline이 동작하지 않는다.
    - 위 예시에서와 같이 최상단에만 설정해도 되고, 각 stage마다 설정해줄 수도 있는데, 최상단에는 반드시 설정되어야한다.
    - 각 stage마다 다르게 설정할 경우 각 stage가 각기 다른 agent로 실행된다.
  - Build stage
    - 일반적으로 source code가 모여서 컴파일되고 패키징 되는 단계이다.
    - Jenkinsfile은 Mavne, Gradle 등의 build tool을 대체하는 것은 아니다.

  - Test stage
    - 자동화된 테스트를 수행하는 단계이다.
  - Deploy stage
    - 배포를 실행하는 단계이다.
    - 이전의 stage들이 성공적으로 완료되었을 때만 실행된다.



- Jenkinsfile에서 사용할 수 있는 환경 변수들

  - Jenkins Pipeline에서 `env`라는 global variable을 통해 환경 변수에 접근할 수 있다.
    - Jenkinsfile의 어디서나 사용이 가능하다.
  - 기본적으로 아래와 같은 환경 변수들이 설정되어 있다.
    - `BUILD_ID`, `BUILD_NUMBER`, `BUILD_TAG`, `BUILD_URL`, JENKINS_URL, `JAVA_HOME`
    - 전체 목록은 `${YOUR_JENKINS_URL}/pipeline-syntax/globals#env`에서 확인할 수 있다.

  ```groovy
  pipeline {
      agent any
      stages {
          stage('Example') {
              steps {
                  echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
              }
          }
      }
  }
  ```

  - Jenkinsfile 내에서 환경 변수를 설정하는 것도 가능하다.
    - `environment` directive를 통해 설정할 수 있다.
    - Scripted Pipeline에서는 `withEnv`를 사용한다.
    - 환경 변수는 자신이 설정된 범위 내에서만 유효한데, 예를 들어 최상단서 설정된 `CC`의 경우 Pipeline의 모든 곳에서 사용할 수 있지만, Example stage에서 설정된 `DEBUG_FLAG`는 Example stage에서만 사용할 수 있다.

  ```groovy
  pipeline {
      agent any
      environment { 
          CC = 'clang'
      }
      stages {
          stage('Example') {
              environment { 
                  DEBUG_FLAGS = '-g'
              }
              steps {
                  sh 'printenv'
              }
          }
      }
  }
  ```

  - 환경 변수를 동적으로 설정하기
    - Shell script를 사용하여 run time에 환경변수가 동적으로 설정되도록 할 수 있다.

  ```groovy
  pipeline {
      agent any 
      environment {
          // Using returnStdout
          CC = """${sh(
                  returnStdout: true,
                  script: 'echo "clang"'
              )}""" 
          // Using returnStatus
          EXIT_STATUS = """${sh(
                  returnStatus: true,
                  script: 'exit 1'
              )}"""
      }
      stages {
          stage('Example') {
              environment {
                  DEBUG_FLAGS = '-g'
              }
              steps {
                  sh 'printenv'
              }
          }
      }
  }
  ```



- Credential 관리하기

  - Jenkins에는 credential을 관리하는 기능이 있다.
    - Jenkinsfile은 source repository에서 관리되기에 사용자 이름이나 비밀번호 등이 노출될 수 있다.
    - 따라서 이러한 내용들을 Jenkins의 credential로 따로 빼고 Jenkinsfile에서 이 credentail에 접근하여 값을 가져오는 방식으로 작성해야한다.
  - `credentials()` 메서드를 사용하여 credential에 접근할 수 있다.
    - `environment` directive에서 사용할 수 있다.
    - 당연하게도 `enviroment` directive가 작성된 범위 내에서만 사용이 가능하다.
    - 만일 Pipeline 상에서 credential 정보를 노출해야 하는 경우(e.g. 아래 예시에서 `echo AWS+ACCESS_KEY_ID`가 실행될 경우) "\****"으로 표기된다.

  ```groovy
  pipeline {
      agent {
          // 
      }
      environment {
          AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
          AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
      }
  }
  ```

  - 만일 credentail을 생성할 때 종류를 `Username with password`로 설정했을 경우 세 개의 환경 변수를 사용할 수 있다.
    - 사용자가 지정한 환경 변수 외에 `_USR`, `_PSW` suffix가 붙은 환경 변수가 자동으로 생성된다.
    - 예를 들어 아래와 같이 선언했을 때, 따로 선언하지 않아도 자동으로 `BITBUCKET_COMMON_CREDS`, `BITBUCKET_COMMON_CREDS_USR`, `BITBUCKET_COMMON_CREDS_PSW`라는 세 개의 환경 변수가 생성된다.

  ```groovy
  environment {
      BITBUCKET_COMMON_CREDS = credentials('jenkins-bitbucket-common-creds')
  }
  ```

  - Text뿐 아니라 file도 지정 가능하다.
    - GPG 파일과 같이 binary 형식의 file이나, Jenkinsfile에 직접 입력하기에 너무 긴 내용을 file로 관리할 수 있다.

  ```groovy
  pipeline {
      agent {
          //
      }
      environment {
          MY_KUBECONFIG = credentials('my-kubeconfig')
      }
      stages {
          stage('Example stage 1') {
              steps {
                  sh("kubectl --kubeconfig $MY_KUBECONFIG get pods")
              }
          }
      }
  }
  ```

  - Text나 file 외에도 다양한 종류의 crential에 접근하는 것이 가능하다.
    - 더 자세한 정보는 [공식 문서](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#handling-credentials) 참고



- 문자열 보간법

  - Jenkinsfile은 Groovy와 동일한 문자열 보간법 규칙을 사용한다.
    - Groovy는 string을 선언할 때 작은 따옴표와 큰 따옴표 모두를 지원한다.
    - 그러나 문자열 보간법은 오직 큰 따옴표만 사용할 수 있으며, 아래와 같이 `$` 기호를 사용한다.

  ```groovy
  def username = 'Jenkins'
  echo 'Hello Mr. ${username}'
  echo "I said, Hello Mr. ${username}"
  ```

  - Credentials에는 절대 문자열 보간법을 사용해선 안된다.
    - 문자열 보간법 대신 작은 따옴표를 사용해서 linux에서 환경 변수를 참조하는 방식을 사용해야 한다.

  ```groovy
  // 아래와 같이 보간법을 사용하면 안된다.
  sh("curl -u ${EXAMPLE_CREDS_USR}:${EXAMPLE_CREDS_PSW} https://example.com/")
  
  // 아래와 같이 참조해야한다.
  sh('curl -u $EXAMPLE_CREDS_USR:$EXAMPLE_CREDS_PSW https://example.com/')
  ```

  - 또한 보간법 사용시 아래와 같은 경우도 주의해야한다.
    - 보간법을 잘 못 사용할 경우 SQL injection과 같은 문제가 발생할 수 있다.

  ```groovy
  // 예를 들어 아래 Pipeline이 실행되면 hello; ls \가 echo되는 것이 아니라 hello가 echo 된 후 전체 파일 list가 출력된다.
  pipeline {
    agent any
    parameters {
      string(name: 'STATEMENT', defaultValue: 'hello; ls /', description: 'What should I say?')
    }
    stages {
      stage('Example') {
        steps {
          /* WRONG! */
          sh("echo ${STATEMENT}")
        }
      }
    }
  }
  
  // 따라서 위와 같은 경우를 방지하기 위해서, 보간법을 사용하지 말고 아래와 같이 작성해야한다.
  pipeline {
    agent any
    parameters {
      string(name: 'STATEMENT', defaultValue: 'hello; ls /', description: 'What should I say?')
    }
    stages {
      stage('Example') {
        steps {
          /* CORRECT */
          sh('echo ${STATEMENT}')
        }
      }
    }
  }
  ```



- Parameter

  - Declarative Pipeline은 `parameter` directive를 통해 run time에 parameter를 설정할 수 있다.
    - Scripted Pipeline에서는 `properties` step에서 설정한다.
  - 예시
    - 아래와 같이 `params`를 통해 접근할 수 있다.

  ```groovy
  pipeline {
      agent any
      parameters {
          string(name: 'Greeting', defaultValue: 'Hello', description: 'How should I greet the world?')
      }
      stages {
          stage('Example') {
              steps {
                  echo "${params.Greeting} World!"
              }
          }
      }
  }
  ```



- 실패 처리하기

  - Declarative Pipeline은 다양한 failure handling 방식을 제공한다.
    - Scripted Pipeline의 경우 Groovy의 try/catch/finally semantic을 사용한다.
  - `post` sectin에 아래와 같은 것들을 정의할 수 있다.
    - `always`, `unstable`, `success`, `failure`, `changed`
  - 예시

  ```groovy
  pipeline {
      agent any
      stages {
          stage('Test') {
              steps {
                  sh 'make check'
              }
          }
      }
      post {
          always {
              junit '**/target/*.xml'
          }
          failure {
              mail to: team@example.com, subject: 'The Pipeline failed :('
          }
      }
  }
  ```



- 병렬 실행하기

  - `parallel` step을 사용하여 여러 개의 작업을 동시에 실행할 수 있다.
  - 예시

  ```groovy
  stage('Test') {
      parallel linux: {
          node('linux') {
              checkout scm
              try {
                  unstash 'app'
                  sh 'make check'
              }
              finally {
                  junit '**/target/*.xml'
              }
          }
      },
      windows: {
          node('windows') {
              /* .. snip .. */
          }
      }
  }
  ```










# Blue Ocean

- Blue Ocean
  - UI상으로 Jenkinsfile을 작성할 수 있도록 도와주는 plugin이다.
  - 더 이상 기능 상의 업데이트는 없을 예정이다.





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





# Jenkins + Docker swarm  + Docker registry로 Continuous Deploy pipeline 구성

- ServerA에 Docker Container 생성하기

  - `daemon.json` 파일을 아래와 같이 작성한다.
    - Test용으로 사용할 것이므로 Docker registry를 insercure repository로 사용한다.

  ```json
  {
      "insecure-registries" : ["http://<ServerA_host>:5000"]
  }
  ```

  - Docker daemon으로 사용하기 위한 Docker container를 생성한다.
    - 2376 port는 docker daemon과 통신을 위한 port, 5000은 docker registry를 위한 port, 8021은 우리가 띄울 app을 위한 port, 2377은 docker swam에서 사용할 port이다.

  ```bash
  docker run \
  --name docker-node1 \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume <host_path>:/certs/client \
  --volume <host_path>:/etc/docker/daemon.json \
  --volume <host_path>:/var/jenkins_home \
  --publish 2376:2376 --publish 5000:5000 --publish 8021:8021 --publish 2378:2377 \
  docker:dind
  ```

  - `docker-node1` container 내부에서 Docker registry 생성하기

  ```bash
  $ docker pull registry
  $ docker run -d -p 5000:5000 --name reg registry:latest
  ```



- Jenkins container 생성하기

  - Jenkins container에 사용할 image를 cutstom한다.
    - Blueocean은 예시에서는 사용하지 않지만, 추후에 사용할 수도 있으므로 함께 설치한다.


  ```dockerfile
  FROM jenkins/jenkins:latest
  
  USER root
  
  RUN apt-get update && apt-get install -y lsb-release
  RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg
  RUN echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
  RUN apt-get update && apt-get install -y docker-ce-cli
  
  USER jenkins
  
  RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
  ```

  - Jenkins container를 생성한다.
    - `path1`에는 `docker-node1`에서 `/certs/client`와 bind mount한 host의 path를 입력한다.
    - `path2`에는 `docker-node1`에서 `/var/jenkins_home`과 bind mount한 host의 path를 입력한다.
    - `path2`의 경우 `sudo chown 1000 <path2>`와 같이 소유자를 변경해줘야한다.

  ```bash
  $ docker run \
  --name jenkins \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 49999:50000 \
  --volume <path1>:/certs/client:ro \
  --volume <path2>:/var/jenkins_home \
  jenkins-blueocean:latest
  ```

  - 필요한 plugin들을 다운 받는다.
    - 초기 화면에서 suggested pluin을 설치한다.
    - `Build Authorization Token Root` plugin을 설치한다.



- ServerB에 Docker container를 생성한다.

  - `docker:dind` image를 받고

  ```bash
  $ docker pull docker:dind
  ```

  - `daemon.json` 파일을 작성한다.

  ```json
  {
      "insecure-registries" : ["http://<ServerA_host>:5000"]
  }
  ```

  - Container를 생성한다.
    - ServerA에 띄운 Docker container와는 달리 외부에서 daemon에 접근할 일도 없고, Docker registry도 ServerA의 것을 사용할 것이므로 port는 app에서 사용할 port만 열어주면 된다.

  ```bash
  $ docker run \
  --name docker-node2 \
  --privileged \
  --publish 8021:8021 \
  -v ./daemon.json:/etc/docker/daemon.json \
  docker:dind
  ```



- Application 생성하기

  - 아래와 같이 같단한 application을 생성한다.
    - App을 실행하기 위한 requirements 파일도 생성한다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  @app.get("/")
  def hello_world():
      return "Hello World!"
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8021)
  ```

  - App을 build하기 위한 Dockerfile을 작성한다.

  ```dockerfile
  FROM python:3.8.0
  
  COPY . /app
  WORKDIR /app
  
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  CMD ["python", "main.py"]
  ```

  - Jenkinsfile을 작성한다.

  ```groovy
  pipeline {
      agent any
  
      stages {
          stage('Build') {
              steps {
                  sh 'docker build -t <ServerA_host>:5000/app .'
                  sh 'docker push <ServerA_host>:5000/app'
              }
          }
          stage('Deploy') {
              steps {
                  sh 'docker service create --name app --replicas=2 --publish=8021:8021 <ServerA_host>:5000/app'
              }
          }
      }
  }
  ```

  - 만일 bind mount가 필요하다면 위 jenkinsfile에서 service를 생성하는 부분을 아래와 같이 수정하거나, service를 update해주면 된다.
    - 이 경우에는 ServerA의 Docker container와 ServerB의 docker container에 저장된다.

  ```bash
  $ docker service create --name app --replicas=2 --mount type=bind,source=<container 내부 경로>,destination=<host 경로> --publish=8021:8021 <ServerA_host>:5000/app
  
  # 혹은 아래와 같이 service를 update한다.
  docker service update --mount type=bind,source=<container 내부 경로>,destination=<host 경로> app
  ```

  - 전체 디렉터리 구조는 아래와 같다.

  ```
  app
  ├── main.py
  ├── requirements.txt
  ├── Jenkinsfile
  └── Dockerfile
  ```

  - 위 directory를 github에 push한다.



- Jenkins pipeline을 생성한다.
  - `FirstPipeline`이라는 이름으로 Pipeline을 생성한다.
  - Github 연동
    - Pipeline의 Definition을 `Pipeline script from SCM`으로 변경하고 SCM에서 `Git`을 설정한다.
    - 위에서 app을 push했던 github repository의 url과 Credientials를 입력한다.
    - `Branch to build`에 branch를 설정한다.
  - Github과 연동할 경우 build시에 pull을 받지 않아도 자동으로 실행된다.



- Docker swarm 생성하기

  - ServerA의 Docker container 내부에서 아래 명령어를 실행한다.

  ```bash
  $ docker swarm init
  ```

  - ServerB의 Docker container 내부에서 아래 명령어를 실행한다.

  ```bash
  $ docker swarm join --token <token> <ServerA_host>:2378
  ```

  - 잘 연결되었는지 확인한다.
    - ServerA의 Docker container에서 아래 명령어를 실행한다.
    - 만일 두 개의 node가 보인다면 성공한것이다.

  ```bash
  $ docker node ls
  ```



- Jenkins에 접속해서 build를 실행하면 ServerA와 ServerB 모두 app container가 생성된 것을 확인할 수 있다.

  - 만일 bind mount 혹은 volume이 필요하다면 jenkinsfile 내에서 Docker service를 아래와 같이 생성하거나, service를 update해주면 된다.

  ```bash
  $ docker service create --name app --replicas=2 --mount type=bind,source=/data,destination=/app/files # ...
  ```











