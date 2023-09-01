# Dockerfile

- Dockerfile
  - Docker 상에서 작동시킬 컨테이너의 구성 정보를 기술하기 위한 파일.
  - Dockerfile로 Docker 이미지를 생성하면 Dockerfile에 작성된 구성 정보가 담긴 이미지가 생성된다.



- Dockerfile의 기본 구문

  - Dockerfile은 텍스트 형식의 파일로, 에디터 등을 사용하여 작성한다.
  - Dockerfile 이외의 파일명으로도 동작하며, 확장자는 필요 없다.
  - 주석은 `#`을 사용하여 작성한다.
  - 주요 명령어
    - 소문자로 작성해도 동작하지만 관례적으로 대문자로 통일하여 사용한다.

  | 명령       | 설명               |      | 명령       | 설명                       |
  | ---------- | ------------------ | ---- | ---------- | -------------------------- |
  | FROM(필수) | 베이스 이미지 지정 |      | VOLUEM     | 볼륨 마운트                |
  | RUN        | 명령 실행          |      | USER       | 사용자 지정                |
  | CMD        | 컨테이너 실행      |      | WORKDIR    | 작업 디렉토리              |
  | LABEL      | 라벨 설정          |      | ARG        | Dockerfile 내의 변수       |
  | EXPOSE     | 포트 익스포트      |      | ONBUILD    | 빌드 완료 후 실행되는 명령 |
  | ENV        | 환경변수           |      | STOPSIGNAL | 시스템 콜 시그널 설정      |
  | ADD        | 파일/디렉토리 추가 |      | HEATHCHECK | 컨테이너의 헬스 체크       |
  | COPY       | 파일 복사          |      | SHELL      | 기본 쉘 설정               |
  | ENTRYPOINT | 컨테이너 실행 명령 |      |            |                            |



- USER 명령어

  - Container를 실행시킬 user를 입력한다.
  - Dockerfile을 사용하여 이미지를 만들다보면 권한 문제가 발생할 때가 있다.
    - 예를 들어 `mkdir` 명령어를 사용하여 디렉터리를 생성해야 하는데 기본 사용자가 root 이외의 사용자로 설정되어 있어 생성이 불가능한 경우가 있다.
    - 이 때 `sudo`를 붙이거나 `su -`을 통해 root 사용자로 변경도 불가능하다.
    - 만일 가능하다고 해도 Docker는 기본적으로 Dockerfile에 작성된 매 명령을 수행할 때마다 이미지를 하나씩 생성하는 방식이다.
    - 따라서 이전 명령에서 `su -`를 통해 root 사용자로 변경 했어도 다음 명령에서는 다시 기본 사용자로 돌아오게 된다.
    - 반면에, USER 명령어를 통해 설정한 사용자는 모든 명령시에 자동으로 적용된다.

  - 예시
    - `elasticsearch:8.1.3` 이미지의 기본 사용자는 `elasticsearch`로 설정되어 있다.
    - `elasticsearch`라는 사용자는 modules 디렉터리에 쓰기 권한이 없어 폴더 생성이 불가능하다.
    - `USER` 명령어를 통해 root로 사용자를 변경한다.

  ```dockerfile
  # 문제
  FROM docker.elastic.co/elasticsearch/elasticsearch:8.1.3
  RUN mkdir -p /usr/share/elasticsearch/modules/test
  RUN mkdir -p /usr/share/elasticsearch/modules/test2
  
  # 예시
  FROM docker.elastic.co/elasticsearch/elasticsearch:8.1.3
  USER root
  RUN mkdir -p /usr/share/elasticsearch/modules/test
  RUN mkdir -p /usr/share/elasticsearch/modules/test2
  # elasticsearch:8.1.3 이미지의 경우 elasticsearch 사용자 이외의 사용자는 컨테이너 실행이 불가능하므로 다시 변경해준다.
  USER elasticsearch	
  ```




- FROM 명령어

  - Docker 컨테이너를 어떤 이미지로부터 생성할지 정의한다.
  - 다이제스트는 Docker Hub에 업로드하면 이미지에 자동으로 부여되는 식별자를 의미한다.
    - `docker image ls --digests ` 명령어를 통해 확인이 가능하다.

  ```dockerfile
  # 기본형
  FROM 이미지명
  # 태그를 생략할 경우 자동으로 latest 버전이 적용된다.
  FROM 이미지명:태그명
  # 다이제스트 사용
  FROM 이미지명@다이제스트
  ```



- ENV 명령어

  - Dockerfile 안에서 환경변수를 설정하고 싶을 때는 ENV 명령을 사용한다.
    - 리눅스 명령어 `export`에 해당한다.
  - `key value`형으로 지정
    - 단일 환경변수에 하나의 값을 지정한다.
    - 첫 번째 공백 앞을 key로 설정하면 그 이후는 모두 문자열로 취급한다.
  - `key=value`로 지정
    - 한 번에 여러 개의 값을 설정할 때 사용한다.
  
  ```dockerfile
  ENV [key] [value]
  ENV [key]=[value]
  ```



- ARG 명령

  - Dockerfile 안에서 사용할 변수를 정의할 때 사용한다.

  - ENV로 생성한 환경변수와 달리  Dockerfile 내에서만 사용이 가능하다.

  ```dockerfile
  ARG <변수명>[=기본값]
  ```



-  ADD 명령

  - 이미지에 호스트 상의 파일 및 디렉토리를 추가할 때 사용한다.

  ```dockerfile
  ADD <호스트의 파일 경로> <Docker 이미지의 파일 경로>
  ```



- COPY 명령

  - 이미지에 호스트상의 파일이나 디렉토리를 복사할 때 사용한다.

  ```dockerfile
  COPY <호스트의 파일 경로> <Docker 이미지의 파일 경로>
  ```



- WORKDIR 명령
  -  dockerfile에서 정의한 명령을 실행하기 위한 작업용 디렉토리를 지정할 때 사용한다.
    -  RUN, CMD, ADD, ENTRYPOINT, COPY 등의 명령을 실행하기 위한 적업용 디렉토리를 지정한다.
    - 지정한 디렉토리가 존재하지 않으면 새로 작성한다.



- RUN 명령어

  - FROM 명령에서 지정한 베이스 이미지에 대해 애플리케이션/미들웨어를 설치 및 설정하거나 환경 구축을 위한 명령을 실행할 떄 사용한다.
  - Shell 형식으로 기술
    - 명령의 지정을 쉘에서 실행하는 방식으로 기술하는 방법.
    - /bin/sh을 통해서 실행한다.
  
  ```dockerfile
  # elasticsearch에 노리 형태소 분석기를 설치하는 예시
  RUN bin/elsticsearch-plugin install analysis-nori
  ```
  
  - Exec 형식으로 기술
    - 실행하고 싶은 명령을  JSON  배열로 지정한다(따라서 반드시 쌍따옴표로 묶어야한다).
  
  ```dockerfile
  # elasticsearch에 노리 형태소 분석기를 설치하는 예시
  RUN ["bin/elasitcsearch-plugin", "-c", "install analysis-nori"]
  ```



- Shell 형식과 Exec 형식의 차이

  - 같은 Python script를 아래와 같이 Shell 형식으로 실행시키면

  ```dockerfile
  FROM python:3.8.0
  COPY ./main.py /main.py
  ENTRYPOINT python main.py
  ```

  - 아래와 같이 실행되지만
    - /bin/sh의 subprocess로 `python main.py`이 실행되는 것을 확인할 수 있다.
  
  
  ```bash
  UID          PID    PPID  C STIME TTY          TIME CMD
  root           1       0  0 04:37 ?        00:00:00 /bin/sh -c python main.py
  root           7       1  3 04:37 ?        00:00:00 python main.py
  ```

  - 아래와 같이 Exec 형식으로 실행시키면
  
  ```dockerfile
  FROM python:3.8.0
  COPY ./main.py /main.py
  ENTRYPOINT ["python", "main.py"]
  ```

  - 아래와 같이 실행된다.
  
  ```bash
  UID          PID    PPID  C STIME TTY          TIME CMD
  root           1       0  1 04:33 ?        00:00:00 python main.py
  ```
  
  - Exec 형식이 Docker에서 권장하는 방식이다.
  
  - Shell  형식으로 명령을 기술하면 /bin/sh에서 실행되지만, Exec 형식으로 기술하면 쉘을 경유하지 않고 직접 실행한다.
  
    - 따라서 Exec 형식으로 기술하면 명령 인수에 환경변수를 지정할 수 없다.
  
    - 단 쉘을 지정하면 환경 변수를 사용 가능하다.
  
  ```bash
  ENV foo bar
  
  # 아래와 같이 실행하면 exec 형식이라고 하더라도 환경 변수를 사용할 수 있다.
  ENTRYPOINT ["/bin/bash", "-c", "echo ${foo}"]
  ```





- CMD 명령어
  - RUN 명령은 이미지를 작성하기 위해 실행하는 명령을 기술하는 반면 CMD 명령은 이미지를 바탕으로 생성된 컨테이너 안에서 실행할 명령을 기술한다.
  - 하나의  CMD 명령만을 기술할 수 있으며 복수의 명령을 작성하면 마지막 명령만 적용된다.
  - Exec  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - Shell  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - ENTRYPOINT 명령의 파라미터로 기술
    - ENTRYPOINT 명령의 인수로 CMD 명령을 사용할 수 있다.



- ENTRYPOINT 명령어
  - 데몬 실행
  - ENTRYPOINT 명령에서 지정한 명령은 `docker run` 명령을 실행했을 때 실행된다.
  - Exec  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - Shell  형식으로 기술
    - RUN 명령의 구문과 동일하다
  - CMD  명령과의 차이
    - `docker run` 명령 실행 시의 동작에 차이가 있다.
    -  CMD 명령의 경우는 컨테이너 시작 시에 실행하고 싶은 명령을 정의해도 `docker run` 명령 실행 시에 인수로 새로운 명령을 지정한 경우 이것을 우선 실행한다.
    - 반면 ENTRYPOINT 에서 지정한 명령은 반드시 컨테이너에서 실행되는데, 실행 시에 명령 인수를 지정하고 싶을 때는 CMD 명령과 조합하여 사용한다.
    - ENTRYPOINT 명령으로는 실행하고 싶은 명령 자체를 지정하고 CMD 명령으로는 그 명령의 인수를 지정하면, 컨테이너를 실행했을 때의 기본 작동을 결정할 수 있다.



- ONBUILD 명령
  - 빌드 완료 후, 다음 빌드에서 실행할 명령을 이미지 안에 설정하기 위한 명령이다.
    - ONBUILD 명령이 포함된 이미지를 빌드한다.
    - 빌드된 이미지를 베이스 이미지로 하여 다른 이미지를 빌드한다.
    - 이 때 ONBUILD에서 지정한 명령을 실행한다.



- Dockerfile의 빌드와 이미지 레이어 구조

  - Docker 이미지 만들기

  ```bash
  $ docker build -t [생성할 이미지명]:[태그명] [Dockerfile의 위치]
  ```

  - 이미지 레이어 구조
    - Dockerfile을 빌드하여 Docker 이미지를 작성하면 Dockerfile의 명령별로 이미지를 작성한다.
    - 작성된 여러 개의 이미지는 레이어 구조로 되어 있다.
    - 즉 이전 명령으로 생성된 이미지 파일 위에 다음 명령으로 생성된 이미지가 덮이는 형식이다.
  - Docker image에 Python 설치하기
  
  ```dockerfile
  RUN yum update -y && \
   yum install -y wget && \
   # Python 설치 파일 다운
   wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz && \
   # Python 설치(압축 해제)
   tar xzf Python-3.7.3.tgz && \
   # Python configuration 변경
   cd Python-3.7.3 && \
   ./configure --enable-optimizations
  ```





- 멀티스테이지 빌드
  - 제품 환경에 필요한 것들만 빌드하기
    - 애플리케이션 개발 시에 개발 환경에서 사용한 라이브러리나 개발 지원 툴 등이 제품 환경에서 모두 사용되는 것은 아니다.
    - 제품 환경에서는 애플리케이션을 실행하기 위한 최소한의 실행 모듈만 배치하는 것이 리소스 관리나 보안 관점에서 볼 때 바람직하다.
  - Docker 파일 작성하기
    - Dockerfile 을 작성할 때 개발용과 제품용 2가지 이미지를 생성하도록 작성한다.
    - 예시는 p.165 참고





# Docker Compose

- Docker Compose
  - 여러 개의 Docker 컨테이너를 모아서 관리하기 위한 툴
  - docker-compose.yml 파일에 컨테이너의 구성 정보를 정의하여 동일 호스트상의 여러 컨테이너를 일괄적으로 관리한다.
    - 애플리케이션의 의존관계를 모아서 설정하는 것이 가낭흐다.
    - 이 정의를 바탕으로  docker-compose 명령을 실행하면 여러 개의 컨테이너를 모아서 시작하거나 정지할 수 있다.
    - 또한 컨테이너의 구성정보를 YAML 형식의 파일로 관리할 수 있으므로 지속적 배포도 용이하다.
    - YAML은 구조화된 데이터를 표현하기 위한 데이터 포맷이다.



## docker-compose.yml 파일의 구성

- 맨 앞에는 docker-compose의 버전을 지정한다.
  - 버전에 따라 기술할 수 있는 항목이 다르므로 주의해야 한다.



- image

  - Docker 컨테이너의 바탕이 되는 베이스 이미지를 지정한다.
  - 이미지명 또는 이미지 ID 중 하나를 지정한다.
  - 베이스 이미지가 로컬 환경에 있으면 그것을 사용하고, 없으면 Docker Hub에서 자동으로 다운로드한다.
    - 태그를 지정하지 않을 경우 자동으로 latest태그가 붙은 이미지를 다운로드한다.

  ```yaml
  elasticsearch:
    image: elasticsearch
  ```



- build

  - 이미지의 작성을 Dockerfile에 기술하고 그것을 자동으로 빌드하여 베이스 이미지로 지정할 때는 build를 지정한다.
  - build에는 docker-compose.yml이 있는 디렉토리를 기준으로 Dockerfile의 경로를 지정한다.
    - Dockerfile은 작성하지 않아도 자동으로 해당 경로의  Dockerfile이라는 이름의 파일을 찾아서 빌드한다.

  ```yaml
  elasticsearch:
    # dockerfile이 현재 디렉토리에 있을 경우
    build: .
  ```

  - Dockerfile의 파일명이 Dockerfile이 아닐 경우에는 context에 경로를. dockerfile에 Dockerfile이름을 넣는다.

  ```yaml
  elasticsearch:
    build: 
      # /data 경로에 있는 my-dockerfile이라는 이름의 Dockerfile로 빌드를 하려는 경우
      context: /data
      dockerfile: my-dockerfile
  ```

  - args로 인수를 지정하는 것도 가능하다.
    - bool 타입을 사용할 경우에는 따옴표로 둘러싸야 한다.
    - Docker Compose를 실행하는 머신 위에서만 유효하다.

  ```yaml
  elasticsearch:
    # dockerfile이 현재 디렉토리에 있을 경우
    build:
      args:
        va1:1
        va2:"true"
        va3:foo
  ```



- command/entrypoint

  - 컨테이너 안에서 작동하는 명령 지정
    - 베이스 이미지에 이미 명령이 지정되어 있을 경우 이미지의 명령을 덮어쓴다.
  - entrypoint는 명령을 나열하는 것도 가능하다.

  ```yaml
  command: 명령어
  
  entrypoint:
    - 명령어1
    - 명령어2
  ```



- links

  - 다른 컨테이너에 대한 링크 기능을 사용하여 연결할 때 사용한다.

  ```yaml
  links:
    - 컨테이너1
    - 컨테이너2
  ```



- ports/expose

  - 컨테이너 간 통신에 사용한다.
  - 컨테이너가 공개하는 포트는 ports로 지정한다.
    - `호스트 머신의 포트 번호 : 컨테이너의 포트 번호` 형식으로 지정하거나 컨테이너의 포트 번호만 지정한다.
    - 컨테이너의 포트 번호만 지정할 경우 호스트 머신의 포트는 랜덤한 값으로 설정된다.

  ``` yaml
  ports:
    - 호스트 머신의 포트 번호 : 컨테이너의 포트 번호
    - 컨테이너의 포트 번호
  ```

  - expose는 호스트 머신에 대한 포트를 공개하지 않고 링크 기능을 사용하여 연결하는 컨테이너에게만 포트를 공개할 때 사용한다.

  ``` yaml
  expose:
    - 컨테이너의 포트 번호1
    - 컨테이너의 포트 번호2
  ```



- depends_on

  - 여러 서비스의 의존관계를 정의할 때 사용한다.
    - 예를 들어 Kibana를 실행하기전에 ES를 먼저 실행시키고자 한다면 Kibana가 ES를 의존하도록 설정할 수 있다.
  - 주의할 점은 컨테이너의 시작 순서만 제어할 뿐 컨테이너상의 애플리케이션이 이용 가능해질 때까지 기다리는 것은 아니라는 것이다.

  ```yaml
  depends_on:
    - 컨테이너1
    - 컨테이너2
  ```



- environment/emv_file

  - 컨테이너 안의 환경변수를 지정할 때 사용한다.
    - `.env` 파일이라고 생각하면 된다.
  - YAML 배열 형식 또는 해시 형식 중 하나로 변수를 지정한다.
  
  ```yaml
  # 배열 형식
  environmnet:
    - FOO = bar
    - VAL
  
  # 해시 형식
  environmnet:
    FOO: bar
    VAL:
  ```
  
  - 설정하고자 하는 환경변수가 많을 때는 env_file을 지정한다.
  
  ```yaml
  env_file: <env 파일 경로>
  ```



- container_name/label

  - 컨테이너의 이름 또는 라벨을 붙일 때 사용한다.

  ```yaml
  container_name: 컨테이너이름
  ```

  - 컨테이너 라벨은 YAML 배열 형식 또는 해시 형식 중 하나로 지정 가능하다.



- volumes/volumes_from

  - 컨테이너에 볼륨을 마운트할 때 사용한다.
    - 호스트 측에서 마운트할 경로를 지정하려면 `호스트의 디렉토리 경로:컨테이너의 디렉토리 경로`

  ```yaml
  volumes:
    - <마운트할 경로>
    - <호스트의 디렉토리 경로>:<컨테이너의 디렉토리 경로>
  ```

  - 볼륨 지정 뒤에 ro를 지정하면 볼륨을 읽기 전용으로 마운트할 수 있다.

  ```yaml
  volumes:
    - <호스트의 디렉토리 경로>:<컨테이너의 디렉토리 경로>/:ro
  ```

  - 다른 컨테이너로부터 모든 볼륨을 마운트할 때는 volumes_from에 컨테이너명을 지정한다.

  ```yaml
  volumes_from:
    - 컨테이너명
  ```



- network

  - 컨테이너 사이의 통신에 사용할 network를 지정한다.

  - 만일 지정해주지 않을 경우 `<compose 파일의 위치>_default` 라는 이름으로 network이 생성되고 compose 파일에 선언된 모든 컨테이너가 연결된다.

  - default로 생성하기
    - default로 생성하면 각 container별로 network을 지정해주지 않아도 default에 설정된 network에 연결된다.

  ```yaml
  version: "3.9"
  
  services:
    proxy:
      build: ./proxy
    app:
      build: ./app
    db:
      image: postgres
  
  networks:
    default:
      driver: custom-driver
  ```

  - custom network 생성하기
    - 네트워크를 생성하고 각 컨테이너에 네트워크를 지정해준다.

  ```yaml
  version: "3.9"
  
  services:
    proxy:
      build: ./proxy
      networks:
        - frontend
    app:
      build: ./app
      networks:
        - frontend
        - backend
    db:
      image: postgres
      networks:
        - backend
  
  networks:
    frontend:
      # Use a custom driver
      driver: custom-driver-1
    backend:
      # Use a custom driver which takes special options
      driver: custom-driver-2
      driver_opts:
        foo: "1"
        bar: "2"
  ```

  - 이미 생성된 네트워크 사용하기
    - 아래와 같이 `external`로 외부 network를 불러온다.

  ```yaml
  version: '3.2'
  
  services:
    other_app:
      build: ./other_app
  
  networks:
    default:
      external:
        name: backend
  ```



## 명령어

- `docker-compose` 명령
  - `docker-compose` 명령은  docker-compose.yml을 저장한 디렉토리에서 실행된다.
  - 만일 현재 디렉토리 이외의 장소에 docker-compose.yml을 놓아 둔 경우 `-f` 옵션으로 파일 경로를 지정해야 한다.
    - 그 외에도 Docker Compose 파일을 docker-compose.yml 이외의 이름으로 설정한 경우에도 `-f` 옵션으로 Docker Compose  파일을 지정해 줘야 한다.
  - 서브 명령 다음에 컨테이너명을 지정하면 해당 컨테이너만 조작이 가능하다.



- Docker Compose의 버전 확인

  - Docker for Mac, Docker for Windows에 미리 설치되어 있다.

  ```bash
  $ docker-compose -v(--version)
  ```



- docker-compose에 정의된 컨테이너 생성 후 시작하기

  - `-d`: 백그라운드에서 실행한다.
  - `--no-deps`: 링크 서비스를 시작하지 않는다.
  - `--build`: 도커 컨테이너 시작시에 Dockerfile을 빌드한다.
  - `--no-build`: 이미지를 빌드하지 않는다.
  - `-t(--timeout)`: 컨테이너의 타임아웃을 초로 지정(기본 10초)한다.

  ```bash
  $ docker-compose up [옵션] [서비스명 .] 
  
  # 이름이 docker-compose.yml(yaml)이 아닌 파일로 실행
  $ docker-compose -f <파일명> up
  ```



- 여러 컨테이너 확인

  - 컨테이너 상태 확인
    - `-q`: 컨테이너 ID 확인

  ```bash
  $ docker-compose ps 
  ```

  - 컨테이너 로그 확인

  ```bash
  $ docker-compose logs
  ```



- 특정 컨테이너에서 명령 실행

  - 실행 중인 컨테이너에서 임의의 명령 실행

  ```bash
  $ docker-compose run <컨테이너 명> <명령>
  # docker-compose run es1 /bin/bash
  ```



- 여러 컨테이너 시작/정지/재시작

  - 특정 컨테이너만 조작하고 싶을 경우 뒤에 컨테이너명을 지정하면 된다.

  ```bash
  # 시작
  $ docker-compose start
  # 정지
  $ docker-compose stop
  # 재시작
  $ dockcer-compose restart
  ```



- 여러 컨테이너 일시 정지/재개

  ```bash
  # 일시 정지
  $ docker-compose pause
  # 재개
  $ docker-compose unpause
  ```



- 구성 확인

  - 공개용 포트 확인
    - `--protocol=proto`: 프로토콜, tcp 또는 udp
    - `--index=index`: 컨테이너의 인덱스 수

  ```bash
  $ docker-compose port [옵션] <서비스명> <프라이빗 포트 번호>
  ```

  - compose의 구성 확인

  ```bash
  $ docker-compose config
  ```



- 여러 컨테이너 강제 정지/삭제

  - `kill` 명령을 사용하면 컨테이너에 시그널을 송신할 수 있다.
    - 시그널이란 프로세스 간의 연락을 주고 받기 위한 장치로 리눅스 커널에 내장되어 있다.
    - 실행 중인 프로새스의 처리를 멈추고 다른 프로세스를 처리하고 싶은 경우나 프로세스를 강제 종료시키고자 할 때 사용한다.
  - 시그널 목록
    - `SIGHUP`: 프로그램 재시작
    - `SIGINT`: 키보드로 인터럽트, `ctrl+c`로 송신할 수 있다.
    - `SIGQUIT`: 키보드에 의한 중지, `ctrl+\`로 송신할 수 있다.
    - `SIGTERM`: 프로세스 정상 종료
    - `SIGKILL`: 프로세스 강제 종료
    - `SIGSTOP`: 프로세스 일시 정지
    - 지원하는 시그널의 종류는 `kill -l`명령으로 확인 가능하다.

  ```bash
  # 정지
  $ docker-compose kill
  # 예시, 컨테이너에게 SIGINT를 송신
  $ docker-compose kill -s SIGINT 
  # 삭제
  $ docker-compose rm
  ```



- 여러 리소스의 일괄 삭제

  - docker-compose에 정의된 컨테이너를 일괄 정지 후 삭제시킨다.
  - `--rmi all`: compose에 정의된 모든 이미지 삭제
  - `--rmi local`: 커스텀 태그가 없는 이미지만 삭제
  - `-v, --volumes`: Compose 정의 파일의 데이터 볼륨을 삭제

  ```bash
  $ docker-compose down
  ```



# Manage application data

- Docker는 컨테이너 내부에 데이터를 저장한다.
  - 컨테이너가 삭제될 경우 데이터도 함께 삭제된다.
    - 따라서 컨테이너가 삭제되더라도 데이터를 남겨야 하는 경우 컨테이너의 외부에 데이터를 저장할 방법이 필요하다.
  - 또한 다른 프로세스(호스트 혹은 다른 컨테이너)에서 컨테이너 내부의 데이터에 접근하기도 번거롭다.
  - 따라서 컨테이너 이외의 장소에 데이터를 저장할 방법이 필요하다.
  - Docker는 크게 아래 3가지 방식을 제공한다.
    - Volumes
    - Bind mounts
    - tmpfs mounts
  - 위 방식 중 어떤 방식을 사용하더라도 컨테이너 내부에서는 차이가 없다.



- Docker 컨테이너 내부의 데이터를 외부에 저장하는 방법.

  - bind mount
    - data를 host의 filesystem 내부의 어느 곳에든 저장하는 방식이다.
    - container의 데이터를 임의의 host 경로에 저장
  
  - volume
    - data를 host의 filesystem중 docker가 관리하고 있는 영역에 저장하는 방식이다.
    - container의 데이터를 host의 `/var/lib/docker/volume`이라는 경로에 저장
    - 해당 경로는 docker를 설치할 때 지정된 docker의 root 경로(`/var/lib/docker`)로, 볼륨 외에도 이미지, 컨테이너 관련된 정보들이 저장되어 있다.
  
  - tmpfs
    - host의 메모리에 저장
    - 파일로 저장하는 것이 아니라 메모리에 저장하는 것이므로 영구적인 방법은 아니다.
  - bind mount와 volume의 차이
    - volume은 오직 해당 volume을 사용하는 컨테이너에서만 접근이 가능하지만 bind mount 된 데이터는 다른 컨테이너 또는 호스트에서도 접근이 가능하다.
    - 즉 Non-docker process는 volume을 수정할 수 없다.
    - 바인드 마운트를 사용하면 호스트 시스템의 파일 또는 디렉터리가 컨테이너에 마운트 된다.
    - 바인드 마운트는 양방향으로 마운트되지만(즉, 호스트의 변경 사항이 컨테이너에도 반영되고 그 반대도 마찬가지), volume의 경우 호스트의 변화가 컨테이너 내부에는 반영되지 않는다.
  
  ![](docker_part2.assets/volume_vs_bindmount.png)
  
  - 공식문서에서는 volume을 사용하는 것을 추천한다.
    - 백업이나 이동이 쉽다.
    - docker CLI 명령어로 볼륨을 관리할 수 있다(`docker volume ~`).
    - 볼륨은 리눅스, 윈도우 컨테이너에서 모두 동작한다.
    - 컨테이너간에 볼륨을 안전하게 공유할 수 있다.
    - 볼륨드라이버를 사용하면 볼륨의 내용을 암호화하거나 다른 기능을 추가할 수 있다.
    - 새로운 볼륨은 컨테이너로 내용을 미리 채울 수 있다.



- 볼륨 내부의 데이터 유무에 따른 차이

  - 빈 볼륨을 컨테이너 내부의 디렉토리에 마운트 할 경우
    - 컨테이너 내부의 디렉토리가 비어 있던 볼륨에 복사된다.

  - 컨테이너 내부의 디렉토리에 바인드 마운트하거나 비어 있지 않은 볼륨을 마운트할 경우
    - 기존에 컨테이너 내부에 존재하던 디렉토리가 가려지게 된다.
    - 그렇다고 삭제되거나 대체되는 것은 아니며, 마운트를 해제할 경우 다시 보이게 된다.



## Volumes

> https://docs.docker.com/storage/volumes/

- volume을 사용해야 하는 경우
  - 여러 컨테이너들이 데이터를 공유해야 하는 경우
    - 여러 컨테이너는 동시에 같은 volume에 마운트 할 수 있다.
    - 다를 컨테이너에 연결된 하나의 볼륨에서 읽기, 쓰기 모두 동시에 처리 가능하다.
  - 마운트 하려는 디렉토리 혹은 파일이 호스트의 filesystem에 있는지 확신하기 어려울 경우
    - volume은 host의 filesystem 중에서도 docker가 관리하는 영역에 생성되므로 호스트의 filesystem에 마운트할 파일 혹은 폴더가 실제로 존재한다는 것이 보장된다.
  - data를 local(host의 filesystem)이 아닌 cloud나 remote 호스트에 저장해야 할 경우
  - data를 백업하거나 복원하거나 다른 host로 옮겨야 할 경우
  - 높은 수준의 I/O가 발생하는 작업을 해야 할 경우



- 관련 명령어

  - 볼륨 생성하기

  ```bash
  $ docker create volume <볼륨 이름>
  ```

  - volume 목록 보기

  ```bash
  $ docker volume ls
  ```

  - 특정  volume 상세 정보 보기

  ```bash
  $ docker volume inspect <볼륨 이름>
  ```

  - volume 마운트하기
    - `-v` 옵션 또는 `--mount` 옵션 사용

  ```bash
  $ docker run -v <볼륨 이름>:<컨테이너 경로> <이미지 이름>
  
  $ docker run --mount type=volume,source=<호스트 경로>,target=<도커 경로>
  ```

  - volume 삭제
    - cp를 통해 볼륨을 다른 디렉터리에 복제해도 rm 명령을 사용하면 **복제 된 volume도 삭제된다.**

  ``` bash
  $ docker volume rm <볼륨 이름>
  ```

  - 사용하지 않는 볼륨 일괄 삭제

  ```bash
  $ docker volume prune
  ```



- `-v(--volume)`와 `--mount`
  - 원래 독립형 컨테이너에서는 `-v`가 사용되었고, Docker cluster인 Swarm Mode의 Service에서는 `--mount`가 사용되었다.
    - 그러나 docker 17.06부터 독립형 컨테이너에서도 `--mount`의 사용이 가능해졌다.
    - 반면 Service에서는 오직 `--mount`만 사용이 가능하다.
  - `--mount`
    - key=value 쌍으로 설정한다.
    - source, target(혹은 destination, dst), type, readonly 등의 옵션을 지정 가능하다.
    - type에 volume, bind, tmpfs를 사용 가능하다.
    - readonly 옵션을 줄 경우 readonly 상태로 마운트된다.
  - `-v`로 설정한다고 volume이 되는 것이 아니며, `--mount`로 설정한다고 bind mount가 되는 것이 아니다.
    - 두 설정은 단지 설정 format이 다른 것일 뿐 `-v`로도 bind mount가 가능하고 `--mount`로도 volume을 설정하는 것이 가능하다.
    - 예를 들어 `-v <volume>:<container_path>`와 같이 설정하면 volume이 설정되는 것이고, `-v <host_path>:<container_path>`와 같이 설정하면 bind mount가 되는 것이다.



- docker volume의 기본 경로 변경하기

  - docker data root directory 자체를 변경하는 방법
    - 아래 [Data Root Directory 변경] 부분 참고
  - 지정한 경로에 volume  생성하기
    - `--driver local`의 의미는 local, 즉 호스트에 저장하겠다는 의미이다.
    - local이 아닌 다른 옵션을 주면 외부 호스트에 저장이 가능하다.
    - 이후 run  명령이나 docker-compose 파일에서 아래에서 생성한 volume 이름을 적어주면 된다.

  ```bash
  $ docker volume create --driver local --opt type=none --opt device=<호스트 경로> --opt o=bind <volume 이름>
  ```

  - `docker run` 명령어와 함께 생성하기

  ```bash
  $ docker run --mount type=volume dst=<컨테이너 내부 경로> \
     volume-driver=local volume-opt=type=none volume-opt=o=bind volume-opt=device=<호스트 경로> \
     <컨테이너 이름>
  ```

  - docker-compose.yml 에서 설정 변경하기

  ```yaml
  services:
    <컨테이너명>:
      (...)
      volumes:
        - <volume 이름>:<컨테이너 내부 경로>
    (...)
    volumes:
      <volume 이름>:
        driver:local,
        driver_opts:
          type: none
          o: bind
          device: <호스트 경로>
  
  
  # 예시
  version: '2.2'
  
  services:
    es:
      (...)
      volumes:
        - es_data:/usr/share/elasticsearch/data
    (...)
    volumes:
      es_data:
        driver:local,
        driver_opts:
          type: none
          o: bind
          device: /home/es/data/docker_volumes/es
  ```



## Bind mounts

> https://docs.docker.com/storage/bind-mounts/

- bind mounts를 사용해야 하는 경우
  - 설정 파일을 호스트와 컨테이너가 공유해야 하는 경우
  - 소스코드를 호스트와 컨테이너가 공유해야 하는 경우



- bind mount

  - volume과 달리 다른 컨테이너나 호스트도 파일의 내용에 접근이 가능하다.
  - 마운트하기
    - `-v` 옵션 또는 `--mount` 옵션 사용

  ```bash
  $ docker run -v <호스트 경로>:<컨테이너 경로> <이미지이름>
  
  $ docker run --mount type=bind,source=<호스트 경로>,target=<도커 경로>
  ```



## tmpfs

> https://docs.docker.com/storage/tmpfs/

- tmpfs를 사용해야 하는 경우
  - 보안상의 이유 등으로 데이터를 호스트나 컨테이너에 일시적으로 저장하고자 할 경우.



# Docker health check

- health check
  - Docker container를 생성한 후 container가 제대로 실행되었는지 확인할 수 있는 기능이다.
  - Dockerfile, docker-compose file, `create` 명령어, `run` 명령어 등에서 사용 가능하다.



- `create`, `run` 명령어와 함께 사용하기

  - 둘 다 동일한 방식으로 사용한다.

  - 옵션들

    - `--health-cmd`: health check에 사용할 명령어를 설정한다.

    - `--health-interval`: 각 check 사이의 기간을 설정한다.
    - `--health-retries`: 실패했을 경우 재시도할 횟수를 설정한다.
    - `--health-start-period`: 실패 후 다음 시도까지의 시간을 설정한다.
    - `--heath-timeout`: 명령어의 실행이 완료될 기한을 설정한다.

  ```bash
  $ docker <run | create> [options]
  
  # e.g.
  $ docker run --health-cmd curl localhost:9200 --health-retries 3 --health-timeout 10
  ```



- dockerfile에서 사용하기

  - 옵션들
    - `--interval`
    - `--timeout`
    - `--start-period`
    - `--retries`

  ```dockerfile
  # HEALTHCHECK를 할 경우
  HEALTHCHECK [options] CMD command
  
  # e.g.
  HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1
  
  # 하지 않을 경우
  HEALTHCHECK NONE
  ```

  - 기본적으로 `HEALTHCHECK`를 작성하지 않으면 실행되지 않는데 굳이 `HEALTHCHECK NONE`과 같이 명시해주는 이유
    - Base image를 기반으로 새로운 image를 만들었을 때 base image에 health check가 포함되어 있다면 health check가 실행되게 된다.
    - 따라서 만일 health check가 포함된 base image로 새로운 이미지를 만들었을 때, health check를 원치 않는다면 위와 같이 명시적으로 작성해줘야 한다.



- docker-compose에서 사용하기

  - 옵션은 다른 방식들과 동일하다.

  ```yaml
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost"]
    interval: 1m30s
    timeout: 10s
    retries: 3
    start_period: 40s
  ```

  - `depends_on`과 함께 사용하기
    - `depends_on`에는 `condition`이라는 문법을 사용 가능하다.
    - 의존하는 container가 `condition`에 설정된 상태가 되면 해당 container를 생성하도록 하기 위해 사용한다.
    - `condition`에 설정 가능한 값은 아래와 같다.
    - `service_started`: 의존하는 container가 생성만 되면 생성을 시작한다.
    - `service_healthy`: 의존하는 container의 health check가 성공하면 생성을 시작한다.
    - `service_compledted_successfully`: 의존하는 container가 완전히 동작하면 생성을 시작한다.

  ```yaml
  # web container는 elasticsearch container의 health check가 성공하고, db가 온전히 동작하면, 생성이 시작된다.
  services:
    web:
      build: .
      depends_on:
        db:
          condition: service_healthy
        redis:
          condition: service_started
    elasticsearch:
      image: elasticsearch
      healthcheck:
        test: ["CMD", "curl", "localhost:9200"]
        interval: 1m30s
        timeout: 10s
        retries: 3
        start_period: 40s
    db:
      image: postgres
  ```





# etc

## Docker Volume 사용시 ownership 문제

- 문제
  - Docker volume 사용시 container 내부에서 volume으로 설정된 file 혹은 directory(이하 file)의 소유권은, host에서 해당 container를 실행시킨 사람의 uid, gid로 설정된다.
  - 일부 docker image들은 내부적으로 기본 사용자만 특정 file에 접근하도록 설정되어 있다.
  - 만일 이러한 file에 volume을 설정할 경우 해당 file의 소유권은 host에서 container를 실행시킨 user의 id와 group id로 설정된다.
  - 따라서 docker image 상에서 기본 사용자로는 permission 문제로 해당 file에 접근할 수 없게 된다.



- 예시

  - Elasticsearch에서 제공하는 logstash image는 `logstash`를 기본 사용자로 하고, logstash 실행시 file 작성이 필요할 경우 `logstash`가 소유하고 있는 file에 작성한다.
    - 아래와 같이 logstash가 file을 작성하는 data folder는 소유 유저가 `logstash`, 소유 그룹이 `root`로 설정되어 있다.

  ```bash
  # docker container
  $ ls -l
  # ...
  drwxrwsr-x 1 logstash root  4096 Jan 28  2022 data
  # ...
  ```

  - 그런데 위 file에 아래와 같이 volume을 설정할 경우 경우 

  ```yaml
  version: '3.2'
  
  services:
    logstash:
      # ...
      volumes:
        - ./data:/usr/share/logstash/data
  	# ...
  ```

  - 소유권이 container를 실행시킨 host user(아래의 경우 foo)의 user id와 group id가 된다.

  ```bash
  # host machine
  $ id
  uid=1022(foo) gid=1022(foo) groups=1022(foo)
  
  # docker container
  $ ls -l
  # ...
  drwxrwsr-x 1 1022 1022  4096 Jan 28  2022 data
  # ...
  ```

  - 따라서 `logstash` user는 `1022`라는 uid를 가진 user가 소유한 `data` folder에 쓰기 권한이 사라져 file을 쓸 수 없게 되고, 문제가 발생한다.



- 해결

  - 불가능한 방식들
    - 가장 깔끔한 방식은 docker에서 volume을 설정할 때 소유권을 함께 설정하는 기능을 제공하는 것이겠으나, 그런 기능을 지원하지 않는다.
    - 그렇다고 아래와 같이 docker image를 build할 때 미리 file을 생성해놓고 해당 file의 소유권을 변경해줘도, 결국 container 실행시 volume이 설정되면서 소유권이 덮어씌워지게 된다.

  ```dockerfile
  FROM docker.elastic.co/logstash/logstash:7.17.0
  # folder를 생성하고
  RUN mkdir /usr/share/data/main
  # 소유권을 변경해도
  RUN chmod logstash:root /usr/share/data/main
  
  # 결국 container 실행시 volume이 설정되면 host의 user 정보로 소유권이 설정된다.
  ```

  - 해결 방법
    - 아래와 같이 image 내의 기본 user(아래 예시의 경우 `logstash`)의 uid를 host user의 uid와 맞춰준다.
    - 상기했듯, container 내부의 소유권은 host user의 uid, guid로 설정되므로, container 내부의 기본 user의 uid만 host user의 uid로 변경해주면 file에 접근이 가능해진다.
    - 주의할 점은 build 과정에서 build process가 기본 user로 실행되고 있으므로 `usermod` 명령어가 실행이 안 될 수 있다.
    - 따라서 uid 변경 전에 임시로 다른 user로 변경하는 과정이 필요하다.

  ```dockerfile
  FROM docker.elastic.co/logstash/logstash:7.17.0
  # 임시로 root로 변경하고
  USER root
  # 기본 user의 uid 변경 후
  RUN usermod -u 1012 logstash
  # 다시 기본 user로 변경한다.
  USER logstash
  ```



## sudo 없이 docker 명령어 실행

- docker 명령어는 기본적으로 root 권한으로 실행해야 한다.

  - 따라서 root가 아닌 user로 명령어를 실행하려면 항상 명령어 앞에 sudo를 입력해야한다.

  - 아래 과정을 거치면 sudo를 입력하지 않고도 docker 명령어 실행이 가능하다.



- sudo 없이 docker 명령어 실행

  - docker group이 있는지 확인

  ```bash
  $ cat /etc/group | grep docker
  ```

  - 만일 docker group이 없다면 docker group 생성

  ```bash
  $ sudo groupadd docker
  ```

  - docker group에 사용자 추가
    - `-a`는 그룹에 사용자를 추가하는 옵션이다.
    - `-G`는 그룹을 지정하는 옵션이다.

  ```bash
  $ sudo usermod -aG docker <사용자 id>
  ```

  - 사용자에서 로그아웃 한 후 다시 로그인한다.
    - ubuntu의 경우 `exit`

  ```bash
  $ logout
  ```

  - group에 추가됐는지 확인한다.

  ```bash
  $ groups
  ```

  - 만일 추가되지 않았다면 아래 명령어를 통해 재로그인 한다.

  ```bash
  $ su <사용자 id>
  ```

  

  

  

  



## docker 컨테이너 내부에서 docker 명령어 사용

- `/var/run/docker.sock`파일을 볼륨을 잡아 컨테이너 내부의 동일 경로에 생성해 주면 된다.

  ```
  /var/run/docker.sock:/var/run/docker.sock
  ```



## docker-entrypoint-initdb.d

- `docker-entrypoint-initdb.d`
  - DB 이미지들 중에는 컨테이너를 생성할 때 일련의 작업(DB 생성, table 생성, data 추가 등)이 자동으로 실행되도록 `docker-entrypoint-initdb.d`라는 폴더를 생성해주는 것들이 있다.
  - 컨테이너 내부의 `docker-entrypoint-initdb.d` 폴더에 volume을 설정하면 컨테이너가 최초로 실행될 때 `docker-entrypoint-initdb.d` 폴더 내부의 파일이 실행된다.



- 주의사항
  - 만일 컨테이너에 이미 volume이 존재한다면 `docker-entrypoint-initdb.d`에 실행할 파일을 넣어도 실행이 되지 않는다.
  - 따라서 반드시 volume을 삭제한 후에 실행해야 한다.



## Data Root Directory 변경

- 기존 Docker Data Root 경로의 용량이 부족할 경우, 혹은 기본 경로가 아닌 다른 곳에 저장을 해야 할 경우 아래 두 가지 방식으로 Root Directory를 변경 가능하다.
  - dockerd에 `--data-root` 옵션 추가(이전 버전에서는 `-g`를 사용했다)
  - daemon.json에 "data-root" 추가



- 기존 데이터 복사하기

  - 변경하고자 하는 경로에 디렉토리를 생성한 후 기존 docker 데이터를 생성한 디렉토리에 옮긴다.
  - 복사 전에 구동중인 Docker 데몬을 종료한다.

  ```bash
  # 새로운 디렉토리 생성
  $ mkdir data
  # Docker 데몬 종료
  $ systemctl stop docker.servic
  # 데이터 복사
  $ cp -R /var/lib/docker data
  ```



- `--data-root` 옵션 추가하기

  - docker.service 파일에 아래 내용을 추가한다.
    - CentOS의 경우 `/usr/lib/systemd/system/docker.service` 경로에 있다.

  ```bash
  ExecStart=/usr/bin/dockerd --data-root <복사할 디렉터리> -H fd:// --containerd=/run/containerd/containerd.sock
  ```

  - docker 데몬 재실행하기

  ```bash
  $ systemctl daemon-reload
  $ systemctl start docker.service
  ```



- daemon.json에 "data-root" 추가

  - daemon.json 파일에 아래 내용을 추가한다.
    - CentOS의 경우 `/etc/docker/daemon.json ` 경로에 있다.

  ```bash
  {
      "data-root": "<복사할 디렉터리>"
  }
  ```



- 변경 되었는지 확인하기

  ```bash
  $ docker info | grep -i "docker root dir"
  ```






## Docker Container Timezone 설정

- Docker Container Timezone 설정

  - 기본적으로 UTC로 설정되어 우리나라보다 9시간 느리다.
    - 따라서 시간에 따른 로그를 출력해야 하거나 정확한 시간이 필요한 경우 아래와 같이 timezone을 변경해 줘야 한다.
  - `TZ`라는 환경 변수를 통해 설정이 가능하다.
    - 어떤 방식으로든 환경 변수로 넘겨주기만 하면 된다.
  - `Dockerfile`에서 설정하기

  ```dockerfile
  ENV TZ=Asia/Seoul
  ```

  - 컨테이너를 실행할 때 설정하기

  ```bash
  $ docker run -e TZ=Asia/Seoul
  ```

  - docker-compose에서 설정하기

  ```yaml
  version: '3'
  
  services:
    some-container:
      environment:
        - TZ=Asia/Seoul
  ```





## 컨테이너 생성시 sql문 자동 실행

- 아래와 같이 실행시킬 sql 파일을  `/docker-entrypoint-initdb.d/`에 볼륨을 잡으면 자동으로 실행된다.

  - 꼭 sql 파일이 아니어도 되며, sql문이 작성된 sh 파일도 가능하다.
  
  ```yaml
  version: '3'
  
  services:
    postgresql:
      container_name: postgressql
      image: postgres:latest
      environment:
        - POSTGRES_PASSWORD=my_password
        - TZ=Asia/Seoul
      volumes:
        - ./create_table.sql:/docker-entrypoint-initdb.d/create_table.sql
  ```
  
  - 주의
    - 이미 데이터가 존재 할 경우 실행되지 않는다.



## Container 상태 보기

- 아래 명령어를 통해 모든 컨테이너의 상태를 볼 수 있다.

  ```bash
  $ docker stats [옵션1] [옵션2] [...]
  ```



- 결과

  - `NET I/O`
    - 컨테이너가 네트워크 인터페이스를 통해 주고 받은 데이터의 양
  - `BLOCK I/O`
    - 컨테이너가 disk에서 읽고 쓴(read and write) 데이터의 양

  ```bash
  CONTAINER ID   NAME           CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O         PIDS
  34ac359a659b   container1     0.00%     41.64MiB / 125.6GiB   0.03%     392kB / 15.1MB    0B / 0B           49
  d71698367f39   container2     0.23%     227.7MiB / 125.6GiB   0.18%     168MB / 68.7MB    8.19kB / 0B       62
  d62202653708   container3	  0.19%     59.24MiB / 125.6GiB   0.05%     27.7MB / 11MB     4.1kB / 8.19kB    13
  4b6e5264a8f2   container4	  0.54%     368.5MiB / 125.6GiB   0.29%     2.98GB / 4.09GB   4.1kB / 0B        19
  ```



- 옵션
  - `--all`, `-a`
    - 모든 컨테이너의 상태를 보여준다.
    - 기본값은 실행 중인 컨테이너의 상태만 보여준다.
  - `--format`
    - Go 템플릿을 통해 format을 설정할 수 있다.
  - `--no-stream`
    - 명령어 실행 시점의 상태를 보여준다.
    - 기본값은 지속적으로 변화하는 상태를 보여준다.
  - `--no-trunc`
    - 결과를 잘라내지 않고 전부 보여준다.





# 참고

- https://boying-blog.tistory.com/31

- https://carpfish.tistory.com/entry/Docker-Data-Root-Directory-%EA%B2%BD%EB%A1%9C-%EB%B3%80%EA%B2%BD
