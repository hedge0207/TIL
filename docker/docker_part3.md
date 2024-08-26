# Logging

- Docker container는 다양한 log를 남긴다.

  - 아래 명령어를 통해서 container의 log를 확인할 수 있다.
    - `--follow` 옵션을 주면 새로 추가되는 log도 지속적으로 출력한다.
    - `--details`: 보다 상세한 log를 보여준다.
    - `--since`: 특정 시점부터의 log를 보여준다.
    - `--until`: 특정 시점까지의 log를 보여준다.
    - `--tail`: 마지막 n개의 log를 보여준다.

  ```bash
  $ docker logs <container 식별자>
  ```

  - Docker logging driver(log drvier)
    - Docker v1.6에서 추가되었다.
    - Docker는 log를 확인할 수 있도록 다양한 logging mechanism을 지원하는데, 이를 logging driver라 부른다.
    - 기본적으로 Docker는 log를 JSON 형태로 저장하는 `json-file` logging driver를 사용한다.



## Logging driver

- 기본 logging driver 설정하기

  - 기본 logging driver를 설정하기 위해서는 Docker daemon의 설정을 변경해야한다.
    - `daemon.json` 파일을 아래와 같이 수정하면 기본 logging driver가 변경된다.
    - `daemon.json` 파일의 경로는 linux 기준 `/etc/docker/daemon.json`이다.
    - 주의할 점은 숫자나 boolean 값이라 할지라도 문자열로 묶어줘야 한다는 것이다.

  ```json
  {
    // logging driver는 json-file을 사용한다.
    "log-driver": "json-file",
    // logging driver와 관련된 상세 설정으로 driver의 종류에 따라 달라질 수 있다.
    "log-opts": {
      "max-size": "10m",
      "max-file": "3",	// 숫자라도 문자열로 묶어준다.
      "labels": "production_status",
      "env": "os,customer"
    }
  }
  ```

  - 위와 같이 변경한 후에는 Docker를 재시작해야 변경 사항이 적용된다.
    - 단, 이미 생성된 container 들에는 적용되지 않는다.
  - 아래 명령어를 통해 현재 기본값으로 설정된 logging driver를 확인할 수 있다.

  ```bash
  $ docker info --format '{{.LoggingDriver}}'
  ```



- Container 단위로 logging driver 설정하기

  - Container를 시작할 때, Docker daemon에 default로 설정된 logging driver와 다른 logging driver를 설정할 수 있다.
    - `--log-driver`와 `--log-opt <NAME>=<VALUE>` flag를 통해 설정할 수 있다.

  ```bash
  $ docker run --log-driver json-file
  ```

  - 아래 명령어를 통해 컨테이너에 설정된 logging driver를 확인할 수 있다.

  ```bash
  docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER 식별자>
  ```



- Delivery mode

  - Docker는 container에서 log driver로 log를 전달하는 두 가지 방식을 지원한다.
    - Direct, blocking 방식(기본값): Container가 log driver에 직접 전달하는 방식.
    - Non-blocking 방식: Container와 log driver 사이에 buffer를 두고 해당 buffer에 저장한 뒤 driver가 가져가는 방식.
  - Non-blocking 방식은 application이 logging back pressure로 인해 blocking되는 것을 방지한다.
    - Application은 STDERR이나 STDOUT의 흐름이 block 됐을 때, 예상치 못하게 fail될 수 있는데, Non-blocking 방식을 사용하면 이를 방지할 수 있다.
    - 단, 만일 buffer가 가득 찰 경우 새로운 log는 buffer에 추가되지 않고 삭제되게 된다.
    - log를 삭제하는 것이 application의 log-writing process를 block시키는 것 보다 낫기 때문이다.

  - Container를 실행할 때 어떤 방식을 사용할지 선택하는 것이 가능하다.
    - `--log-opt` flag에 값으로 설정하면 된다.
    - `max-buffer-size`를 통해 container와 log driver 사이에서 log를 저장하는데 사용되는 buffer의 size를 설정할 수 있다.

  ```bash
  $ docker run --log-opt mode=non-blocking --log-opt max-buffer-size=4m
  ```





# DinD DooD

- Docker achitecture

  > https://docs.docker.com/get-started/overview/

  - Docker는 client-server 구조를 사용한다.
    - Docker client가 빌드, 컨테이너 실행, 컨테이너 배포 등을 수행하는 Docker daemon와 통신한다.
    - Docker client와 daemon은 같은 system에서 실행될 수도 있고, 서로 다른 시스템이서 실행되어 원격으로 통신할 수도 있다.
    - Docker client와 daemon은 UNIX socket 혹은 network interface를 통해 REST API를 사용하여 통신한다.
  - Docker daemon
    - Docker daemon(`dockerd`)은 Docker API로 들어오는 요청을 처리한다.
    - Image, container, network, volume 등의 docker object들을 관리한다.
    - 또한 Docker service를 관리하기 위해서 다른 daemon들과도 상호작용한다.
  - Docker client(Docker CLI)
    - Docker client(`docker`)는 Docker와 상호작용하는 주요 방법이다.
    - Docker 명령어(e.g. `docker run`)를 입력하면, Docker client는 dockerd로 해당 명령을 전송한다.
    - 하나 이상의 Docker daemon과 통신할 수 있다.
  - Docker registries
    - Docker image를 저장하기 위한 저장소이다.
    - Docker Hub는 누구나 사용할 수 있는 공개 저장소이며, private registry도 존재한다.
  - Docker desktop
    - Windows, Mac, Linux 등에서 Docker를 보다 쉽게 사용할 수 있게 해주는 application이다.
    - Docker Client(`docker`)와 Docker daemon(`dockerd`), Docker compose 등을 모두 포함하고 있다.



## DooD

- DooD(Docker out of Docker)

  - Docker container 내부에서 host machine의 Docker daemon을 사용하는 방식이다.
    - DooD라는 용어 자체는 DinD처럼 널리 쓰이는 것은 아닌 듯 하고, DooD 방식 자체를 DinD의 하나로 보는 사람들도 있다.
  - `docker.sock` 파일을 bind-mount해서 사용한다.

  ```bash
  $ docker run -v /var/run/docker.sock:/var/run/docker.sock ...
  ```




- Docker container 내부에서 host의 Docker daemon에 요청 보내기(DooD)

  > Host machine에 Docker가 설치된 상태에서 진행한다.

  - Ubuntu image pull 받기

  ```bash
  $ docker pull ubunut:20.04
  ```

  - Dockerfile 생성하기
    - Docker daemon은 host machine의 것을 쓸 것이기에 docker cli(docker client)만 설치한다.
    - Docker는 보다 안전하게 docker package를 설치할 수 있도록 gpg key를 제공한다.
    - 따라서 gpg key를 받아와서 install시 사용해야한다.

  ```dockerfile
  FROM ubuntu:20.04
  
  # docker cli를 설치하는 데 필요한 package들을 설치한다.
  RUN apt-get update && apt-get install -y ca-certificates curl lsb-release gnupg
  
  # gpg key를 저장하기 위한 directory를 생성한다.
  RUN mkdir -p /etc/apt/keyrings
  
  # Docker 공식 gpg key를 받아와서  /etc/apt/keyrings/docker.gpg에 저장한다.
  # gpg --dearmor -o에서 -o는 결과를 file에 쓰겠다는 옵션이다.
  RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  
  # docker-ce-cli package를 받아올 repository를 설정한다.
  RUN echo \
    # `dpkg --print-architecture`를 통해 arch(architecture) 정보를 입력한다.
    "deb [arch=$(dpkg --print-architecture) \ 
    # 위에서 받아온 /etc/apt/keyrings/docker.gpg 파일을 signed-by에 넣어준다.
    signed-by=/etc/apt/keyrings/docker.gpg] \  
    https://download.docker.com/linux/ubuntu \ 
    # 위에서 설치한 lsb-release를 사용하여 `lsb_release -cs` 명령어를 통해 linux 배포판의 codename을 입력한다.
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
  
  RUN apt-get update && apt-get install -y docker-ce-cli
  ```

  - Docker client가 설치된 ubuntu container 실행하기
    - 아래 보이는 것과 같이 host machine의 `/var/run/docker.sock`를 container 내부에 bind mount 해줘야한다.
    - Ubuntu container 내부의 docker cli가 docker.sock을 통해서 host machine의 docker daemon에 요청을 보낸다.

  ```bash
  $ docker run -it --name dood-ubuntu -v /var/run/docker.sock:/var/run/docker.sock dood-ubuntu:latest /bin/bash
  ```

  - Docker 명령어 테스트 해보기
    - Container 내부에서 아래와 같이 명령어를 입력하면 host의 container들의 목록이 뜨는 것을 확인할 수 있다.

  ```bash
  $ docker ps
  ```



- DooD 사용시 `/var/run/docker.sock`에 대한 권한 문제가 생길 수 있는데, 아래와 같이 해결이 가능하다.

  - Host machine의 docker group id를 확인한다.

  ```bash
  $ cat /etc/group | grep docker
  ```

  - Docker image build시 아래와 같이 docker group을 추가해주고, container 내부의 user를 해당 group에 추가해준다.
    - 주의할 점은 docker group의 group id를 host machine의 docker group id와 동일하게 생성해야한다는 점이다.

  ```dockerfile
  RUN groupadd -g <host machine의 docker group id> docker
  
  RUN usermod -aG docker <container 내부 user>
  ```



## DinD

- DinD(Docker in Docker)

  > https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/

  - Docker container 내부에서 Docker를 실행시키는 방식이다.
  - 본래 Docker를 개발하는 개발자들이 보다 쉽게 Docker를 개발할 수 있게 하기 위해 개발되었다.
    - 그러나 많은 사람들이 CI pipeline을 위해 DinD 기능을 사용하기 시작했다.
    - 그러나 후술할 여러 문제들로 인해, DinD 방식을 Docker 개발이 아닌 CI를 위해 사용하는 것은 권장하지 않는다.
    - Jenkins 공식 문서에서도 DinD 방식을 사용하지만, 이는 이 방식이 가장 쉽고 직관적인 방식이어서 그런 것이지 DinD 방식을 권장해서는 아니다([출처](https://community.jenkins.io/t/what-is-the-purpose-of-docker-in-docker-when-using-a-dockerized-jenkins/1370/5)).
  - DinD 이전의 Docker 개발 방식
    - 개발
    - 개발이 완료된 새로운 version의 Docker를 이전 version의 Docker로 build한다.
    - Docker daemon을 정지시킨다.
    - 새로운 version의 Docker daemon을 실행한다.
    - Test를 수행한다.
    - 새로운 version의 Docker daemon을 정지시킨다.
    - 위 과정을 반복한다.
  - DinD가 도입된 후의 Docker 개발 방식
    - 개발
    - Build와 실행을 동시에 한다.
    - 반복한다.



- DinD 실행하기

  - Docker hub에서 `docker:dind` image를 pull 받는다.

  ```bash
  $ docker image pull docker:dind
  ```

  - `docker:dind` image를 아래와 같이 실행한다.
    - `--privileged`: DinD를 위해서는 privileged 옵션을 줘야한다.
    - `--env DOCKER_TLS_CERTDIR`: DinD를 위해 `--privileged` 옵션을 줬으므로, 보안을 위해 TLS를 사용해야 한다. 따라서 `DOCKER_TLS_CERTDIR` 환경 변수로 Docker TLS 인증서들의 root directory를 설정한다.
    - 다른 container에서 `docker-in-docker` container의 docker deamon을 사용할 수 있도록 client용 인증서를 호스트 머신에 복사한다.
    - 2376 port는 docker daemon과 통신을 위한 port이다.

  ```bash
  $ docker run \
  --name docker-in-docker \
  --privileged \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume /path/docker-certs:/certs/client \
  --publish 2376:2376 \
  docker:dind
  ```

  - Docker compose로 실행하기

  ```yaml
  version: '3.2'
  
  services:
    dind:
      image: docker:dind
      container_name: docker-in-docker
      privileged: true
      environment:
        - DOCKER_TLS_CERTDIR=/certs
      volumes:
        - ./certs:/certs/client
      ports:
        - 2376:2376
      restart: always
  ```

  - 확인하기

  ```bash
  $ docker exec -it docker-in-docker docker --version



- DinD 방식의 문제점

  - AppArmour나 SELinus 등의 LSM(Linux Security Modules)들이 내부 container와 외부 container 간에 충돌을 일으킬 수 있다.
  - Storage driver 관련 문제
    - 외부 Docker는 EXT4나 BTRFS 등의 normal filesystem에서 실행되는 반면, 내부 Docker는 AUFS, BTRFS 등의 copy-on-write system에서 실행된다.
    - 이들은 에러를 발생시킬 수 있는 수 많은 조합이 존재한다.
    - 예를 들어 AUFS 위에서 AUFS를 실행시킬 수는 없고, BTRFS 위에서 BTRFS를 실행시키면 처음에는 잘 동작하는 것 같지만, 중첩된 subvolume이 생성된다면, parent subvolume을 삭제할 수 없다.

  - Build cache와 관련된 문제
    - Docker 내부의 Docker에서 host에 위치한 image를 사용하려고 하는 사람들이 많다.
    - 그들 중 일부는 Docker image들이 모여있는 외부 Docker의 `/var/lib/docker` directory를 내부 Docker에 bind-mount하기도 한다.
    - 그러나 이는 container들 사이에 같은 data를 사용하여 data 손상이 발생할 수 있으므로 매우 위험한 행동이다.
    - 또한 만약 위 처럼 `/var/lib/docker`가 volume이 잡혀있는 상태에서 내부 container에서 build를 한다면, 이는 build cache에 지대한 영향을 끼치게 된다.





# Docker registry

- Docker image를 저장하고 공유할 수 있게 해주는 server side application이다.
  - Apache license 하에서 open source로 개발되었다.
  - Docker hub도 일종의 registry이며, private image를 저장할 수 있는 기능을 제공한다.
  - 주로 아래의 용도로 사용한다.
    - Image 저장소를 보다 엄격히 통제하기 위해서.
    - Image 공유 pipeline을 보다 완전히 통제하기 위해서.
    - Image 저장소를 내부 개발 workflow에 포함시키기 위해서.
  - Docker 1.6.0 version부터 사용이 가능하다.



- Docker registry 사용해보기

  - Docker hub에서 `registry` image를 pull 받는다.

  ```bash
  $ docker pull registry:latest
  ```

  - Pull 받은 `registry` image를 사용하여 container를 생성한다.
    - Registry가 생성된 서버에 문제가 생겨 registry containe가 정지되더라도, 바로 다시 실행햐야하므로 `--restart=always` 옵션을 준다.
    - `registry`는 기본적으로 5000번 port로 생성되는데, 만약 이 값을 바꾸고 싶으면 `-e REGISTRY_HTTP_ADDR=localhost:5001`와 같이 환경변수로 추가해주면 된다.

  ```bash
  $ docker run -d -p 5000:5000 --restart=always --name my-registry registry:latest
  ```

  - 위에서 생성한 registry에 저장할 테스트용 image를 pull한다.

  ```bash
  $ docker pull python:3.10.0
  ```

  - 이 이미지를 우리가 생성한 registry에 등록하기 위해 아래와 같이 이름을 변경한다.
    - `docker push`가 실행되면, image명에서 `/` 앞의 registry 주소(이 경우 `localhost:5000`)로 image가 push된다.
    - 따라서 image명을 아래와 같이 `<registry_domain>:<port>/<image_name>[:<port>]` 형식으로 지정한다.

  ```bash
  $ docker image tag python:3.10.0 localhost:5000/myfirstimage
  ```

  - 이 상태에서 image 목록을 확인하면 아래와 같다.
    - IMAGE ID가 같은 것에서 알 수 있듯, 두 image는 이름만 다른 같은 image이다.

  ```bash
  $ docker images
  REPOSITORY                    TAG       IMAGE ID       CREATED         SIZE
  python                        3.10.0    24gtea791238   19 months ago   917MB
  localhost:5000/myfirstimage   latest    24gtea791238   19 months ago   917MB
  ```

  - 새로운 tag를 붙인 image를 push한다.
    - 이렇게 push된 image는 `registry` container 내부의 `/var/lib/registry` directory에 저장된다.

  ```bash
  $ docker push localhost:5000/myfirstimage
  ```

  - 저장된 image를 pull 할 때도 동일한 image 이름을 사용한다.

  ```bash
  $ docker pull localhost:5000/myfirstimage
  ```
  
  - registry에 등록된 image들 확인하기
    - 명령어가 따로 있지는 않고, API를 호출해야한다.
  
  ```bash
  $ curl http://localhost:5000/v2/_catalog
  ```



- Registry에 등록된 image로 container 생성하기

  - 위에서 본 것과 같이 registry에 등록한 image를 pull 받아서 container를 생성해도 되고, 아래와 같이 pull 받지 않고 바로 생성해도 된다.
  - Test용 app을 생성한다.

  ```python
  import time
  import logging
  
  
  logger = logging.getLogger("simple_example")
  logger.setLevel(logging.DEBUG)
  
  sh = logging.StreamHandler()
  sh.setLevel(logging.DEBUG)
  
  formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s")
  sh.setFormatter(formatter)
  
  logger.addHandler(sh)
  
  
  try:
      while True:
          logger.info("Hello World!")
          time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
      logger.info("Bye!")
  ```

  - 위에서 생성한 app을 docker image로 build하기 위해 dockerfile을 생성한다.

  ```dockerfile
  FROM python:3.8.0
  
  COPY ./main.py /app/main.py
  WORKDIR /app
  
  ENTRYPOINT ["python", "main.py"]
  ```

  - Image를 build한다.

  ```bash
  $ docker build -t localhost:5000/test-image .
  ```

  - Image를 registry에 push한다.

  ```bash
  $ docker push localhost:5000/test-image
  ```

  - 이후 host에선 image를 삭제한다.

  ```bash
  $ docker rmi localhost:5000/test-image:latest
  ```

  - Docker registry에 등록한 test image로 바로 container를 생성한다.

  ```bash
  $ docker run localhost:5000/test-image
  ```

  - 수동으로 pull을 받지 않아도, 자동으로 위에서 upload한 `test-image`를 pull 받은 후 해당 image로 container를 생성한다.
    - Registry에 등록된 image를 바로 사용하는 것이 아니라, Docker hub와 마찬가지로 저장소에 있는 image를 pull을 통해 받아와서 실행하는 것이다.
    - 따라서 registry container가 종료되더라도 registry에 등록된 image로 실행시킨 container에는 영향을 미치지 않는다.



## Configuration

- 설정 방법
  - Docker container 생성시에 환경변수로 설정하는 방식
    - Configuration을 환경 변수를 선언하여 설정할 수 있다.
    - `REGISTRY_<variable>` 형식으로 선언하면 되며, `<variable>`에는 configuration option이 들어간다.
    - 만일 들여쓰기로 level이 구분될 경우 `_`를 넣으면 된다.
    - 예를 들어 `reporting.newrelic.verbose`의 값을 False로 설정하고 싶을 경우 `REGISTRY_REPORTING_NEWRELIC_VERBOSE=false`와 같이 설정하면 된다.
  - Configuration file을 직접 작성하는 방식
    - YAML 형식의 `config.yml`파일을 작성하여, `registry` container 내부의 `/etc/docker/registry/config.yml`에 bind mount한다.



- 주요 설정들

  > 전체 설정은 [Docker 공식 문서](https://docs.docker.com/registry/configuration/#list-of-configuration-options) 참고

  - `notifications`
    - Docker registry의 notification과 관련된 설정이며, `endpoints`리는 하나의 option만을 존재한다.
    - `threshold`가 3이고, `backoff`가 1s일 경우, 3번의 실패가 연속적으로 발생할 경우, 1초 동안 기다린 뒤 재시도한다.

  ```yaml
  notifications:
    events:
      includereferences: true
    endpoints:
      - name: alistener						# service의 이름을 설정한다.
        disabled: false						# 만일 false로 설정될 경우, service에 대한 notification이 비활성화된다.
        url: https://my.listener.com/event	# event를 전송할 url.
        headers: <http.Header>				# request와 함께 보낼 header를 설정한다.
        timeout: 1s							# ns, us, ms, s, m, h, 와 숫자의 조합으로 timeout을 설정한다.
        threshold: 10							# 몇 번의 실패를 실패로 볼지를 설정한다.
        backoff: 1s							# 실패 후 재실행까지 얼마를 기다릴지를 설정한다.
        ignoredmediatypes:					# 무시할 event들의 media type을 설정한다.
          - application/octet-stream
        ignore:
          mediatypes:							# ignoredmediatypes와 동일하다.
             - application/octet-stream
          actions:							# event를 전송하지 않을 action들을 지정한다.
             - pull
             
             
             
  # headers는 아래와 같이 작성하면 되며, 값은 반드시 array로 작성해야한다.
  headers:
    Authorization: [Bearer "qwer121t23t32gg34g4g43"]
  ```





## Notification

- Docker registry는 notification 기능을 지원한다.
  - Registry 내에서 event가 발생할 경우, 이에 대한 응답으로 webhook을 전송한다.
    - Manifest push와 pull, layer push와 pull이 event에 해당한다.
  - Event들은 registry 내부의 broadcast system이라는 queue에 쌓이며, queue에 쌓인 event들을 순차적으로 endpoint들로 전파한다.



- Endpoint
  - Notification은 HTTP request를 통해 endpoint로 전송된다.
    - Request를 받은 endpoint들이 200번대나 300번대의 응답을 반환하면, message가 성공적으로 전송된 것으로 간주하고, message를 폐기한다.
  - Registry 내에서 action이 발생할 경우, event로 전환되어 inmemory queue에 저장된다.
    - Event가 queue의 끝에 도달할 경우, endpoint로 전송될 http request가 생성된다.
  - Event들은 각 endpoint에 순차적으로 전송되지만, 순서가 보장되지는 않는다.



- Event

  - Event들은 JSON 형식으로 notification request의 body에 담겨서 전송된다.

  - Event의 field들
    - GO로 작성된 자료구조를 사용한다.

  | Field      | Type                    | Description                          |
  | ---------- | ----------------------- | ------------------------------------ |
  | id         | string                  | Event들을 고유하게 식별할 수 있는 값 |
  | timestamp  | Time                    | Event가 발생한 시간                  |
  | action     | string                  | Event를 발생시킨 action              |
  | target     | distribution.Descriptor | Event의 target                       |
  | length     | int                     | Content의 bytes 길이                 |
  | repository | string                  | repoitory명                          |
  | url        | string                  | Content에 대한 link                  |
  | tag        | string                  | Tag event의 tag                      |
  | request    | RequestRecord           | Event를 생성한 request               |
  | actor      | ActorRecord             | Event를 시작한 agent                 |
  | source     | SourceRecord            | Event를 생성한 registry node         |

  - 하나 이상의 event들은 envelope이라 불리는 구조로 전송된다.
    - 하나의 envelope으로 묶였다고 해서 해당 event들이 서로 관련이 있는 event라는 것은 아니다.
    - Envelope은 단순히 request 횟수를 줄이기  위해 event들을 묶어서 한 번에 보내는 것 뿐이다.

  ```json
  {
      "events":[
          //
      ]
  }
  ```




- Docker registry notification 활용

  - Notification을 받을 app을 실행한다.

  ```python
  from pydantic import BaseModel
  from typing import List, Any
  from fastapi import FastAPI
  import uvicorn
  
  
  class DockerRegistryEvent(BaseModel):
      events: List[Any]
  
  app = FastAPI()
  
  @app.post("/notifiaction")
  def get_event(event: DockerRegistryEvent):
      print(event)
  
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8017)
  ```

  - Registry configuration file을 아래와 같이 작성한다.
    - `notifications.endpoints.url`에 위에서 실행한 app의 url을 입력한다.

  ```yaml
  version: 0.1
  storage:
    filesystem:
      rootdirectory: /var/lib/registry
  http:
    addr: :5000
    headers:
      X-Content-Type-Options: [nosniff]
  notifications:
    events:
      includereferences: true
    endpoints:
      - name: alistener
        url: http://<app_host>:8017/notifiaction
        timeout: 1s
        threshold: 10
        backoff: 1s
  ```

  - registry를 실행시킬 Docker container를 실행한다(optional).
    - 위에서 작성한 config파일을 volume으로 설정한다.

  ```yaml
  version: '3.2'
  
  services:
    docker-node1:
      image: docker:dind
      container_name: docker-node1
      privileged: true
      volumes:
        - ./config.yml:/home/config.yml
      restart: always
  ```

  - Registry container를 실행한다.

  ```bash
  $ docker pull registry
  $ docker run -d -p 5000:5000 -v /home/config.yml:/etc/docker/registry/config.yml --name my-registry registry:latest
  ```

  - Docker registry에 push할 image를 생성한다.

  ```bash
  $ docker pull python:3.10.0
  $ docker image tag python:3.10.0 localhost:5000/my-python
  ```

  - 위에서 생성한 image를 registry에 push한다.
    - 여기까지 완료하면 맨 처음에 띄운 app의 `/notifiaction`로 요청이 들어오는 것을 확인할 수 있다.

  ```bash
  $ docker push localhost:5000/my-python
  ```

  - 현재 bug인지 의도된 것인지는 모르겠지만 ignore에 actions만 줄 경우 적용이 되지 않는다.

    > https://github.com/distribution/distribution/issues/2916

    - mediatypes를 반드시 함께 줘야한다.
  
  ```yaml
  ignore:
    mediatypes:
      - application/octet-stream
    actions:
      - pull
  ```



- Jenkins와 연동하기

  - Docker repository에 push가 발생할 때 마다 Jenkins pipeline에서 build가 이루어지도록 할 것이다.
  - Jenkins pipeline을 생성한다.
    - Build Triggers에서 `빌드를 원격으로 유발`을 선택하고 원하는 token 값을 입력한다.
  - Jenkins에 [`Build Authorization Token Root`](https://plugins.jenkins.io/build-token-root/) plugin을 설치한다.
    - 이 plugin을 설치하지 않을 경우 `<jenkins_url>/job/<job_name>/build?token=<token>` 형태로 요청을 보내야 trigger가 동작하는데, CSRF 문제로 403 Forbidden이 반환된다.
    - 이 plugin을 설치 후 `<jenkins_url>/buildByToken/build?job=<job_name>&token=<token>`로 요청을 보내면, 정상적으로 build가 trigger된다.
  - Docker registry 설정

  ```yaml
  version: 0.1
  storage:
    filesystem:
      rootdirectory: /var/lib/registry
  http:
    addr: :5000
    headers:
      X-Content-Type-Options: [nosniff]
  notifications:
    endpoints:
      - name: jenkins
        url: http://<jenkins_url>/buildByToken/build?job=<job_name>&token=<token>
        timeout: 1s
        threshold: 10
        backoff: 1s
        ignore:
          mediatypes:
             - application/octet-stream
          actions:
             - pull
  ```

  - 이제 Docker registry에 image를 push할 경우 Jenkins pipeline이 trggier되어 실행된다.





## Registry Security

- Insecure registry

  - 어떠한 보안 조치도 취하지 않은 Docker registry를 의미한다.
    - 당연하게도, CA에 의해 발행된 TLS 인증서를 사용하여 registry를 보호하는 것이 권장된다.
    - 그러나 사용하다보면, 테스트 등의 목적으로 보안을 전부 해제해야하는 경우도 있다.
  - `/etc/docker/daemon.json` 파일을 아래와 같이 수정한다.
    - 파일을 수정한 후 Docker를 재실행해야한다.

  ```json
  {
    "insecure-registries" : ["http://<registry_host>:<registry_port>"]
  }
  ```

  - Insecure registry에 접근하고자 하는 모든 host에서 위와 같은 작업을 해야한다.
    - 주의할 점은 접근하고자 하는 host의 ip가 아닌 registry가 위치한 ip를 입력해야한다는 점이다.





# Docker swarm

> https://docs.docker.com/

- Swarm이란
  - Docker engine에 포함되어 있는 cluster 관리 및 orchestration 기능이 이다.
  - Swarm은 swarm mode가 활성화 된 상태로 실행중인 Docker host들로 구성된다.
    - 각 Docker host들은 manager와 worker의 역할을 수행한다.
    - Docker swarm을 통해 관리되는 container들을 swarm service라 부른다.
  - Docker swarm의 대략적인 동작 방식
    - Swarm service를 생성할 때, 이상적인 상태를 정의힌다.
    - Docker swarm은 이 이상적인 상태를 유지하는 방식으로 동작한다.
  - Swarm으로 관리되지 않는 container를 standalone container라 부른다.
    - Swarm mode로 실행중인 Docker에서도 standalone container를 실행할 수 있다.
    - Standalone container와 swarm service의 가장 핵심적인 차이는 swarm service는 swarm manager만이 관리 하지만, standalone container는 아무 daemon에서나 실행될 수 있다는 것이다.



- Node
  - Swarm에 참여하고 있는 Docker engine을 의미한다.
  - Manager node
    - Task라 불리는 작업들의 unit을 worker 노드에게 전파하는 역할을 한다. 
    - Orchestration과 cluster 관리를 통해 이상적인 상태를 유지하는 역할을 한다.
    - Manager node는 orchestration task를 수행하기 위해서 단일 leader를 선출한다.
    - 기본적으로 manager node 또한 worker node의 역할을 수행하지만, 설정을 통해 manager task만 수행하도록 할 수 있다.
    - Manger node의 개수가 는다고 가용성이나 성능이 좋아지는 것은 아니며, 오히려 그 반대이다.
    - 홀수 N개 만큼의 manager node가 있을 경우 (N-1)/2 만큼의 manager node가 손실되어도 버틸 수 있다.
    - Docker 공식 문서에서는 Manager node의 개수가 최대 7개를 넘지 않도록 권고한다.
  - Worker node
    - Manager node가 전파한 task들을 수행하는 역할을 한다.
    - Manager node가 이상적인 상태를 유지할 수 있도록 worker node는 manager node에게 자신이 할당 받은 작업의 현재 상태를 알린다.



- Services와 tasks와 container
  - Service
    - Manager node 혹은 worker node에서 실행될 작업들을 의미한다.
    - Swarm system의 중심 구조이면서 사용자가 swarm과 상호작용하는데 가장 근본이 되는 요소이다.
    - Service를 생성할 때, 어떤 image를 사용하여 container를 생성할 것이고 해당 container가 어떤 명령어를 실행할지를 지정해줘야한다.
    - Replicated service model에서 swarm manager는 특정 수의 replica task들을 node들에게 뿌려준다.
    - Global service에서 swarm은 cluster 내의 모든 가용한 node들에게 하나의 task만을 실행하도록 한다.
    - Swarm manager는 service의 이상적인 상태를 받아 이상적인 상태를 실현하기 위해 replica task들을 node에서 실행시킨다.
  - Task
    - Docker container와 container 내에서 실행할 명령을 의미한다.
    - Manager node가 worker node들에게 task를 할당하면, task들은 다른 node로 이동할 수 없다.
    - 오직 할당 받은 node에서 실행되거나 실패될 뿐이다.
  - Container
    - Task는 container를 담을 수 있는 slot에 비유될 수 있다.
    - Container가 살아 있는 동안은 해당 task가 `running` 상태에 있다고 본다.
    - 그러나 container가 종료되면 task도 함께 종료된다.
  - 아래 그림은 service가 생성되는 과정을 보여준다.
  
  ![Services flow](docker_part3.assets/service-lifecycle.webp)



- Load balancing
  - Swarm manager는 ingress load balancing을 사용한다.
    - 이를 통해 service를 swarm 외부에서 접근할 수 있게 된다.
    - 또한 하나의 port로 service 내의 모든 task에 접근할 수 있게 된다.
  - Ingress network를 사용하기 위해서는 swarm node들 사이에 아래의 port들이 열려있어야한다.
    - `7946` TCP/UDP: container network discovery에 사용된다.
    - `4789` UDP: container의 ingress network에 사용된다.
  - Swarm manager는 service에 자동으로 PublishedPort를 할당할 수 있으며, 사용자가 수동으로 설정할 수도 있다.
    - `published`값을 설정하지 않을 경우 30000에서 32767 사이의 port를 자동으로 할당한다.
    - 아래와 같이 수동으로 설정할 수 있다.
    - 기존에는 `-p <PUBLISHED-PORT>:<CONTAINER-PORT>`와 같이 설정했으나, 아래와 같이 설정하는 것이 보다 직관적이고 유연성이 높으므로 아래와 같이 설정하는 것이 권장된다.
  
  ```bash
  $ docker service create \
    --name <SERVICE-NAME> \
    --publish published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
    <IMAGE>
  ```
  
  - Cloud load balancer 등의 외부 컴포넌트는 cluster에 속한 아무 node의 PublishedPort를 통해 service에 접근할 수 있다.
    - 해당 node가 task를 실행 중이 아니라도 접근할 수 있다.
    - 예를 들어 3개의 node가 있고, 아래와 같이 service를 실행하여 task가 3개의 node 중 2개에만 할당되었다고 할 때, task가 할당되지 않은 node로도 PublishedPort를 통해 service에 접근할 수 있다.
  
  - Swarm mode는 각 service마다 자동적으로 부여할 internal DNS component를 가지고 있다.
    - 이는 DNS entry에서 하나씩 빼서 부여하는 방식이다.
    - Swarm manager는 cluster 내의 service들에 request를 분산하기 위해서 service의 DNS name을 기반으로 internal load balancing를 사용한다.



- Docker swam 시작하기

  - Docker 1.12부터는 Docker에 docker swarm이 포함되어 별도의 설치 없이도, 도커만 설치되어 있다면 바로 사용이 가능하다.
  - ServerA에 Docker container 생성하기
    - `Docker:dind` image를 사용하여 Docker container를 생성한다.

  ```bash
  $ docker pull docker:dind
  $ docker run \
  --name docker-node1 \
  --privileged \
  --publish 2378:2377 \
  --publish 7947:7946 \
  docker:dind
  $ docker exec -it docker-node1 /bin/sh
  ```

  - Docker container 내부에서 Docker swarm을 실행한다.

    - 제대로 실행 되었다면 `docker node ls`를 입력했을 때 cluster에 속한 docker node들이 출력된다.

    - 혹은 `docker info` 명령어를 입력하여 `Server.Swarm` 값이 active로 설정되었는지를 확인하면 된다.

    - 또한 init시에 swarm에 다른 worker를 추가하려면 어떤 명령어를 입력해야 하는지도 함께 출력된다.

  ```bash
  $ docker swarm init
  $ docker node ls
  $ docker info
  ```

  - ServerB에 Docker container 생성하기
    - 위와 동일한 방식으로 ServerB에 Docker container를 생성한다.
  - ServerB에 새로 생성한 Docker를 Docker swarm에 추가하기
    - 아래 명령어를 입력하면 Docker Swarm에 추가된다.

  ```bash
  $ docker swarm join --token <ServerA의 docker swarm init시에 출력된 token> <host>:2378
  ```

  - 만일 ServerA에서 `docker swarm init` 실행시에 token을 확인하지 못했다면 아래 명령어를 입력하여 token을 확인할 수 있다.
    - Worker node용 token과 manager용 token이 따로 생성되므로, worker를 입력해줘야한다.fㄹ

  ```bash
  $ docker swarm join-token worker
  ```

  - 추가 됐는지 확인
    - ServerA의 Docker container 내부에서 아래 명령어를 입력한다(아래 명령어는 오직 Swarm manager에서만 사용이 가능하므로, ServerB에서는 확인이 불가능하다).
    - ServerA의 docker와 ServerB의 docker가 모두 뜬다면 성공적으로 swarm에 추가가 된 것이다.

  ```bash
  $ docker node ls
  ```



- Docker swarm 시작하기

  - `--task-history-limit`
    - Docker swarm은 기본적으로 이전의 작업 내역을 저장해둔다.
    - 예를 들어 service를 생성한 후 해당 service를 몇 번 update하면 이전 version의 container들이 쌓이게 된다.
    - 이 옵션은 몇 개의 내역을 쌓을지를 설정하는 값으로 기본 값은 5이다.
    - 만일 init시에 설정을 못 했더라도 추후 update를 통해 변경이 가능하다.

  ```bash
  $ docker swarm init [options]
  ```



- Node 목록 조회

  - ID 옆의 `*` 표시는 현재 명령을 실행한 node를 나타낸다.
  - Docker swarm 내에서 `HOSTNAME` 값은 중복이 가능하지만 ID 값은 중복될 수 없다.
  - AVAILABILITY
    - `Active`: 새로운 task를 할당 받을 수 있는 상태
    - `Pause`: 새로운 task를 할당 받지는 않지만 현재 실행중인 task는 구동중인 상태
    - `Drain`: 새로운 task도 할당 받지 않고, 실행 중인 task들도 모두 종료되는 상태
    - 단 이는 swarm service에 해당하는 사항으로, service가 아닌 standalone container의 경우 영향을 받지 않는다.
    - 즉, 예를 들어 node가 Drain 상태라고 하더라도 해당 Docker로 띄운 standalone container는 계속 실행된다.
  - MANAGER STATUS
    - manager node에만 표시된다.
    - `Leader`: Swarm 관리와 orchestration을 맡은 노드임을 의미한다. 
    - `Reachable`: 다른 매니저 노드들과 정상적으로 통신 가능한 노드임을 의미하며, 만일 leader node에 장애가 발생할 경우 이 상태값을 가진 node들 중에 새로운 leader를 선출한다.
    - `Unavailable`: Leader를 포함한 다른 매니저 노드들과 통신이 불가능한 상태임을 의미한다.

  ```bash
  $ docker node ls
  ID                           HOSTNAME       STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
  vpaqawacp368mhz27ugn12qw     42535425321b   Ready     Active                          24.0.2
  qgebfgjontqwmcvt4tibrevz *   35262352352q   Ready     Active         Leader           24.0.2
  ```



- 특정 노드 상세 조회

  - 특정 node에 대한 상세한 정보를 JSON 형식으로 출력한다.
    - `--pretty` option을 줄 경우 보다 보기 편한 형태로 출력한다.
  
  
  ```bash
  $ docker node inspect <node 식별자>
  ```



- Node의 type 변경하기

  - Worker node를 manager node로 변경하기
    - 복수의 node를 space로 구분하여 한 번에 변경할 수 있다.

  ```bash
  $ docker swarm promote <node 식별자> [node 식별자2]
  ```

  - Manager node를 worker node로 변경하기
    - 마찬가지로 복수의 node를 space로 구분하여 한 번에 변경할 수 있다.
    - 단, manager node가 하나 뿐일 경우 실행할 수 없다.

  ```bash
  $ docker swarm demote <node 식별자> [node 식별자2]
  ```



- Node update하기

  - Docker node 의 availability 변경하기

  ```bash
  $ docker node update --availability <상태> <node 식별자> 
  ```

  - Label 설정하기
    - Label은 "key=value" 형태로 부여하거나 key만 부여할 수도 있다.
    - Node에 부여된 label은 이후에 스케줄링에 사용된다.

  ```bash
  $ docker node update --label-add <(key=value) | key> <node 식별자>
  ```

  - Label 삭제하기

  ```bash
  $ docker node update --label-rm <(key=value) | key> <node 식별자>
  ```



- Cluster에서 node 제외시키기

  - Cluster에서 node를 제외시키는 절차
    - 만일 제외하려는 node가 manager node라면 먼저 worker node로 변경해준다.
    - 삭제할 노드의 availability를 drain으로 변경한다.
    - 삭제할 노드의 task들이 다른 node로 잘 옮겨졌는지 확인한다(`docker service ps`).
    - 잘 옮겨졌다면 해당 node와 cluster의 연결을 끊는다.
    - Manager node에서 해당 node를 삭제한다.
  - Node와 cluster의 연결 끊기
    - 제외시키려는 node에서 아래 명령어를 실행한다.
    - 아직 node list에는 보이지만, `down`이라고 표시된다.

  ```bash
  $ docker swarm leave
  ```

  - Cluster에서 node 제외시키기
    - Manager node에서 아래 명령어를 실행한다.

  ```bash
  $ docker node rm <node 식별자>
  ```

  - 만일 제외하려는 node가 manager node일 경우 매우 주의해서 제외시켜야한다.
    - Manager node를 강제로 제거하려 할 경우 cluster가 기능을 멈출 수 있다.
  
  - Cluster에서 모든 node가 제외되면 swarm mode가 종료된다.



- `task.db`
  - Docker swarm에서 실행되는 task들을 저장하기 위한 file이다.
    - `/var/lib/docker/swarm/worker`경로에서 확인할 수 있다.
  - Docker deamon이 restart될 때 간혹 이 file이 오염되는 경우가 있다.
    - 이 경우 Docker deamon을 정지하고 `task.db` file을 삭제한 후 다시 생성하면 된다고 하는데, 직접 테스트해보지는 않았다.
    - [Stackoverflow](https://stackoverflow.com/questions/50933171/docker-node-is-down-after-service-restart)와 [github issue](https://github.com/moby/moby/issues/34827#issuecomment-457678500)에서 이와 관련된 질문과 답변을 찾아볼 수 있다.
  - Docker swarm과 관련된 task들을 작성하는 file이기에 모종의 이유(disk 부족 등)로 file을 작성할 수 없게 될 경우, 해당 node는 swarm에서 이탈하게 된다.
    - Heatbeat가 실패하게 되어 `STATUS`는 `Down`이 되고, `MANAGER STATUS`는 `Unreachable`이 된다.
    - 이 경우 file 작성을 불가능하게 만든 원인을 제거하면 해결된다.





# Docker service

- Docker service 관련 명령어

  - Service 생성
    - Docker container를 생성할 때 사용하는 명령어를 대부분 공유한다.
    - `--volume` option은 사용할 수 없으며, volume 또는 bind bount를 추가하려면 `--mount` option을 사용해야한다.
    - `mount`시에는 모든 node에 mount하려는 source 파일이 있어야한다.
  
  ```bash
  $ docker service create [options] <image> [command] [args]
  
  # 예시
  $ docker service create \
    --name my-service \
    --replicas 3 \
    --mount type=volume,source=my-volume,destination=/path/in/container,volume-label="color=red",volume-label="shape=round" \
    my-image
  ```
  
  - Service 조회
  
  ```bash
  $ docker service ls
  ```
  
  - Service의 task 조회
    - Service에서 실행중인 task들의 목록을 보여준다.
    - Swarm manager가 유지해야 할 task의 상태(`DESIRED STATE`)와 현재 상태(`CURRENT STATE`)를 확인할 수 있으며 각 상태는 [Docker 공식 문서](https://docs.docker.com/engine/swarm/how-swarm-mode-works/swarm-task-states/?ref=seongjin.me)에서 확인할 수 있다.
  
  ```bash
  $ docker service ps <service>
  ```
  
  - Service 삭제
    - 삭제를 실행하면 service로 생성된 모든 container가 삭제된다.
    - 예를 들어 service를 update하거나 rollback하면 새로운 container가 생성되는데, service를 삭제하면, 이러한 container 들도 함께 삭제된다.
    - 정말 삭제할 것인지를 묻지 않으므로 신중하게 사용해야한다.
  
  ```bash
  $ docker service rm <service>
  ```
  
  - Service log 확인
    - Docker service 또는 service의 task를 확인하기 위해 사용한다.
  
  ```bash
  $ docker service logs <service | task> 
  ```
  
  - Service 상세 정보 확인
  
  ```bash
  $ docker service inspect <service>
  ```
  
  - Service update하기
    - 기존 task(container)를 정지시키고 변경 사항을 반영한 새로운 task(container)를 생성하는 방식으로 동작한다.
    - `--mount-add`/`--mount-rm`: service 생성시에 미처 추가하지 못한 volume 혹은 bind mount를 추가/삭제 할 수 있다(추가 방식은 create 할 때와 동일하며, 삭제시에는 target_path를 입력하면 된다).
    - `mount-add`시에는 모든 node에 mount하려는 source 파일이 있어야한다.
    - 이 외에도 publish할 port의 추가/삭제, network의 추가/삭제 등도 가능하다.
    - `--image` option을 통해 update에 사용할 image를 지정할 수 있다.
    - 기본적으로 task에 영향을 주지 않는 옵션은 task를 재생성하지 않는데, 예를 들어 `--update-parallelism`를 변경하더라도 이는 task에 영향을 주는 setting은 아니므로 task가 재생성되지는 않는다.
    - 그럼에도 task를 재생성 시키고자 한다면 `--force` flag를 주면 task가 무조건 재생성된다.
    - `--update-parallelism`: update를 동시에 실행할 최대 task의 개수를 설정한다(기본값은 0).
    - `--update-parallelism`를 적당한 값으로 주고, `--force` flag를 주면, 아무 변경 사항이 없더라도, `update` 명령어를 rolling restart에 사용할 수 있다.
    
  
  ```bash
  $ docker service update [options] <service>
  ```
  
  - Service rollback하기
    - Service를 이전 버전(마지막으로 `docker service update`를 실행한 이전 version)으로 되돌린다.
    - 특정 version을 지정할 수는 없고, 바로 직전 version으로 돌아가게 되는데, 직전 version에 대한 정보는 `docker service inspect` 명령어를 입력하여 확인할 수 있다(`PreviousSpec`을 확인하면 된다).
    - Rollback은 이전 상태로 돌아가는 명령어로, rollback 자체도 다른 상태로 넘어가는 명령어이다.
    - 따라서 rollback을 실행한 이후에 다른 상태 변화 없이 다시 rollback을 실행하면 rollback 이전의 상태로 다시 돌아갈 수 있다.
  
  ```bash
  $ docker service rollback [options] <service>
  ```
  
  - Service scale하기
    - `docker service update` 명령어를 통해서도 가능하다.
  
  ```bash
  $ docker service scale <service>=<replicas> [<service>=<replicas> ...]
  
  # 아래 두 명령어는 동일하게 동작한다.
  $ docker service scale frontend=50
  $ docker service update --replicas=50 frontend
  ```



- Label 설정

  - Service 실행시 label을 따로 설정하지 않으면 service의 container들은 자동으로 각 node에 고르게 분배되어 실행된다.
  - Node에 아래와 같이 label을 설정한다.
    - `key=value` 형태로 설정할 수 있으며, key만 넣을 수도 있다(key만 넣을 경우 value는 빈 문자열이 된다).
    - `--label-rm`을 통해 삭제가 가능하다.
  
  ```bash
  $ docker node update --label-add foo=bar <node ID>
  ```
  
    - node에 label이 잘 설정 됐는지 확인하기
      - `Spec.Labels`에서 확인할 수 있다.
  
  ```bash
  $ docker node inspect <node>
  ```
  
    - Service 생성시 아래와 같이 `--constraint` 옵션을 통해 task를 실행할 node를 설정할 수 있다.
      - `==`를 통해 배포할 node를 설정할 수 있고, `!=`를 통해 배포하지 않을 node를 설정할 수 있다.
      - Service의 label을 설정하는`--label` option이나 container의 label을 설정하는 `--container-label`이 아닌 `--constraint` option을 사용한다는 것에 주의해야 한다.
  
  ```bash
  $ docker service create --constraint node.labels.foo==bar <image>
  ```
  
  - Compose file에서는 아래와 같이 설정하면 된다.
  
  ```yaml
    version: '3.2'
  
    services:
      service_name:
  
      # ...
  
      deploy:
        placement:
          constraints:
            - node.labels.foo==bar
  ```
  
    - Service에 constraint가 잘 설정되었는지 확인
      - `Spec.TaskTemplate.Placement.Constraints`에서 확인할 수 있다.
  
  ```bash
  $ docker service inspect <service>
  ```
  
    - Service 실행시 node에 설정되지 않은 label을 설정할 경우 service는 생성되지만 task는 아무 node에도 할당되지 않은 상태가 된다.
      - 만약 service 생성시 label을 잘못 입력했다면 아래와 같이 constraint를 update해준다.
  
  ```bash
  # 기존 constraint를 삭제하고
  $ docker service update --constraint-rm node.labels.foo==bar
  
  # 새로운 constraint를 추가한다.
  $ docker service update --constraint-add node.labels.foo==baz
  ```
  
    - Task가 분배된 이후에 constraint를 변경할 경우, constraint에 맞게 task가 재분배된다.
      - **정확히는 재분배가 아니라 기존 task를 종료하고 새로운 task를 실행하는 것이다.**
      - 예를 들어 node1에 foo라는 label에 bar 값이 설정되어 있었고, node2에 foo라는 label에 baz라는 값이 설정되어 있다.
      - Service를 생성할 때 constraint를 bar로 설정하면 모든 task가 node1에 분배될 것이다.
      - 만일 추후에 아래와 같이 contraint를 update하면, 모든 task가 node2에서 재실행된다(node1의 모든 task가 종료되고, node2에서 새로운 task가 실행된다).
      - 단, 이 경우 기존 node1에 생성된 task(container)는 삭제되지는 않고 정지되기만 한다.
  
  ```bash
  $ docker service update --constraint-add node.labels.foo==baz
  ```



- 가급적 특정 node에만 task 할당하기

  - 위 예시에서 `--constraint` option을 통해 label을 설정할 경우, 해당 label이 설정된 node에만 task가 할당된다.
    - 따라서 만약 일치하는 label이 설정된 node가 없을 경우 task는 할당되지 않은 상태로 남게 된다.
  - `--placement-pref` option을 사용하면 label에 일치하는 node가 있을 경우 해당 node에 task를 할당하고, 없을 경우 아무 node에나 할당하도록 할 수 있다.
    - `--placement-pref` option은 `<strategy>=<arg>`의 형태로 설정한다.
    - 현재는 `spread` strategy만 사용할 수 있으며, `agr`에는 node에 설정한 label의 key를 입력하면 된다.
    - `spread`는 인자로 받은 label key를 가진 모든 node에 균등하게 task를 분배하고, 더 이상 조건에 맞는 node가 없을 경우 나머지 node에 균등하게 분배하는 방식이다.

  ```bash
  $ docker service create --replicas 3 --placement-pref spread=foo <image>
  ```

  - Label의 value가 아닌 key만을 지정하지만 분배는 label의 value에 따라 이루어진다.

    - 예를 들어 Docker swarm이 아래와 같이 구성되어 있다고 가정해보자.

    - datacenter=east와 같은 label을 가진 node가 3대 있다.
    - datacenter=west와 같은 label을 가진 node가 2대 있다.
    - datacenter=south와 같은 label을 가진 node가 1대 있다.
    - 이 경우 `replicas`가 9인 service를 아래와 같이 생성하면, task는 east라는 value를 가진 node group에 3개, west라는 value를 가진 node group에 3대, south라는 value를 가진 node group에 3대로 고르게 분배된다.
    - 그리고 east라는 value를 가진 node 3대에는 task가 1개씩 분배되고, west라는 value를 가진 node 2대 중 1대에는 2개의 task가, 나머지 1대의 node에는 1개의 task가 분배되며 south라는 value를 가진 node 1대에는 3개의 task가 분배된다.

  ```bash
  $ docker service create --replicas 9 --placement-pref spread=node.labels.datacenter <image>
  ```

  - 상기했듯 균등하게 분배하고 난 후 더 이상 조건에 맞는 node가 없을 경우 조건이 맞지 않는 node들에 균등하게 분배한다.
    - 예를 들어 `foo`라는 label을 가진 node 1대와, 갖지 않는 node 1대가 있다고 가정해보자.
    - Replica의 개수를 4로 설정하고, `--placement-pref`를 `node.labels.foo`로 설정하여 service를 생성할 경우, 4개의 task는 label을 가진 node와 갖지 않은 node에 각 2개씩 배치된다.
    - 즉 `--placement-pref`를 설정했다고 특정 label을 가진 node에 모두 task를 할당하는 것이 아니라, 특정 label을 가진 node에 최대한 균등하게 할당하고, 남는 task를 label을 갖지 않은 node에 다시 균등하게 할당한다.
  
  - Service update
    - `--placement-pref-add`를 통해 추가가 가능하고, `--placement-pref-rm`을 통해 삭제가 가능하다.

  ```bash
  $ docker service update --placement-pref-add node.labels.foo <service>
  $ docker service update --placement-pref-rm node.labels.foo <service>
  ```
  



- Image update와 rollback

  - `docker service rollback` 명령어는 Docker service를 마지막 `docker service update` 명령어를 실행하기 이전의 상태로 돌리는 명령어이다.
  - Image의 경우 image의 id가 아닌 image의 이름을 기반으로 rollback이 실행되기 때문에, update 전후에 image의 내용이 달라졌더라도 이름이 같으면 rollback이 예상대로 동작하지 않을 수 있다.
  - 예를 들어 아래와 같은 app을 만든다.

  ```python
  import time
  import logging
  
  
  logger = logging.getLogger("simple_example")
  logger.setLevel(logging.DEBUG)
  
  sh = logging.StreamHandler()
  sh.setLevel(logging.DEBUG)
  
  formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s")
  sh.setFormatter(formatter)
  
  logger.addHandler(sh)
  
  
  try:
      while True:
          logger.info("Foo")
          time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
      pass
  ```

  - 이를 Docker image로 build한다.
    - 생성시에 version을 명시하지 않았기 때문에 latest로 생성된다.

  ```bash
  $ docker build -t my-app .
  ```

  - 위에서 build한 image로 service를 생성한다.

  ```bash
  $ docker service create --replicas 2 --name my-service my-app
  ```

  - 의도한 대로 1초에 1번씩 "Foo"가 출력되는지 확인한다.

  ```bash
  $ docker logs <container_name>
  ```

  - App이 "Foo"가 아닌 "Bar"를 출력하도록 아래와 같이 app을 수정한다.

  ```python
  # ...
  try:
      while True:
          logger.info("Bar")
          time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
      pass
  ```

  - 수정한 app을 다시 build한다.
    - 마찬가지로 version을 명시하지 않았기 때문에 latest로 생성된다.

  ```bash
  $ docker build -t my-app .
  ```

  - 새로 build한 image로 service를 update한다.
    - image의 이름이 변경되지 않았으므로, docker service 입장에서는 변경 사항이 있는지 알 수 없고, 따라서 그냥 update를 실행하면 변경 사항이 없다고 판단하여 task들을 재실행 시키지 않는다.
    - 따라서 `--force` option을 주어 강제적으로 task들을 재시작 시킨다.

  ```bash
  $ docker service upcate --image my-app --force my-service
  ```

  - 의도한 대로 1초에 1번씩 "Bar"가 출력되는지 확인한다.

  ```bash
  $ docker logs <container_name>
  ```

  - 다시 "Foo"가 출력되도록 rollback을 시키려고 하는데, rollback 전에 `PreviousSpec`을 확인한다.
    - Service를 update하기 이전에 사용하던 image의 이름은 `my-app:latest`였고, update 후에 사용하는 image의 이름도 `my-app:latest`이다.
    - 두 image는 각기 "Foo", "Bar"를 출력하는, 다른 내용을 가진 image이지만 이름은 완전히 동일하다.
    - Rollback을 실행하면 `PreviousSpec.TaskTemplate.ContainerSpec.Image` 부분에 적혀 있는 image를 사용하여 task들을 재실행한다.
    - `PreviousSpec.TaskTemplate.ContainerSpec.Image` 부분을 확인해보면 `my-app:latest`라고 적혀 있는 것을 확인할 수 있다.
    - 따라서 rollback을 해도 `my-app:latest`라는 이름의 image를 찾아 task를 재실행하므로 "Foo"를 출력하는 상태로는 돌아갈 수 없다.

  ```bash
  $ docker inspect my-service
  ```

  - 결론
    - Service에서 사용중인 image의 tag와 update할 image의 tag는 다르게 설정하는 것이 좋다.
    - 두 image의 이름이 같을 경우 image를 update할 때도 `--force` option을 주어야 하며, 이전 image로 service를 되돌리는 rollback도 불가능하기 때문이다.
    - 만약 위 예시에서 update 전에 사용한 image의 이름과 update에 사용한 image의 이름을 각기 `my-app:1.0.0`, `my-app:2.0.0`과 같이 다르게 줬으면, update시에 `--force` option을 줄 필요도 없고, rollback도 예상대로 동작하게 된다.



- Volume 관리

  - Docker service를 생성할 때나, update할 때 volume을 추가하고, 제거할 수 있다.
    - `--mount-add`의 `type`이 volume일 경우 src에는 volume의 이름을 받고, bind일 경우 host의 경로를 받는다.
    - `--mount-rm`은 `type`이 volume일 때나 bind일 때나 모두 container 내부의 경로를 받는다.

  ```bash
  $ docker service update --mount-add type=bind,src=./test,dest=/app/test my-app
  $ docker service update --mount-rm /app/test my-app
  ```

  - Docker service의 volume 관리시에 유의해야 할 점은 `docker service update` 명령어는 기존 container를 정지 시키고 새로운 container를 생성한다는 점이다.
    - 따라서 만약 기존에 container 내에 없던 data를 대상으로 volume을 생성했다면 container 내에서 해당 data가 사라지게 된다.
    - 또한 container 내에 이미 있던 data를 대상으로 volume을 생성했다 하더라도, 변경 사항이 모두 초기화된다.
    - volume, bind-mount 모두 동일하다.
  - Volume을 service 단위로 설정하더라도 volume의 관리는 swarm을 구성하는 개별 node들이 한다.
    - 따라서 service를 제거하더라도 service에서 사용하던 volume은 제거되지 않으며, 이는 service를 생성하면서 함께 생성된 volume일 경우에도 마찬가지다.
    - 또한 같은 service를 구성하는 task라 하더라도 각기 다른 docker daemon에서 실행 중이라면 volume의 sync가 맞지 않을 수 있다.
    - 예를 들어 `--replicas`를 3으로 설정하고 volume을 설정하여 service를 생성했다고 가정해보자.
    - Task 2개는 A서버에, task 1개는 B서버에 할당이 됐다고 할 때, A서버에 할당된 task 2개는 같은 volume을 사용하므로 data의 sync가 맞지만, B 서버에 할당된 task는 다른 volume을 사용하므로 sync가 맞지 않게 된다.





# Docker image build시 anti-pattern

> http://jpetazzo.github.io/2021/11/30/docker-build-container-images-antipatterns/

- Big image

  - 큰 이미지 보다는 작은 이미지가 낫다.
    - 이미지가 작을 수록 build, push 그리고 pull을 보다 빠르게 실행할 수 있다.
    - 또한 공간도 더 적게 차지하며, network도 덜 사용한다.
  - 얼마나 커야 크다고 할 수 있는가?
    - 상대적으로 적은 수의 의존성을 가지고 있는 microservice의 경우 100MB 이상부터
    - Monoliths의 경우 1GB 이상부터 크다고 할 수 있다.
  - 여러 개의 app을 하나의 image로 build하거나, data를 image에 포함시키는 방식은 지양해야한다.
    - 여러 개의 app은 각각의 image로 생성하는 것이 나을 수 있다.
    - Data는 image에 포함시키기보다 volume으로 관리하는 것이 낫다.

  - 작으면 무조건 좋은가?
    - Image의 크기가 너무 작다면 필요한 tool들이 포함되어 있지 않을 수도 있다.
    - 물론, 상황에 따라 필요한 tool이 무엇인지는 달리질 수 있지만, image의 크기를 줄이겠다고 필수적인 tool들까지 설치하지 않는 것은 지양해야한다.



- Zip, tar 혹은 다른 종류의 archive들을 image에 포함시키는 경우
  - Image에 zip, tar 등의 archive를 포함시키는 것은 일반적으로 좋지 않은 생각이며, container 실행시에 이들을 unpack하는 것은 확실히 좋지 않은 생각이다.
  - Docker image는 registry에 저장될 때 이미 압축된 상태이다.
    - 따라서 압축된 file을 image에 포함시킨다고 해서 image의 용량을 덜 차지하지 않는다.
    - 또한 압축되지 않은 file을 image에 포함시킨다고 해서 image의 용량을 더 차지하는 것도 아니다.
  - Image에 archive를 포함시키고, container 실행시에 이를 unpack하는 것은 아래와 같은 단점들이 있다.
    - Unpack이 실행해야 하므로, 이미 unpack된 file들을 포함시켰을 때에 비해 CPU cycle과 시간을 낭비한다.
    - 압축된 file과 unpack된 file을 모두 container에 보관하므로 공간이 낭비된다.



- 동일한 base image로 생성할 image를 반복적으로 rebuilding하는 경우
  - 여러 app이 같은 base image를 사용하는 것은 흔한 일이다.
    - 여러 app에 공통으로 들어가지만, build하는 데 시간이 오래 걸리는 의존성들을 설치한 image를 base image로 사용하는 경우도 있을 수 있다.
  - 이런 공통 image들은 매번 build하기 보다는 registry에 등록하고 필요할 때 pull해서 사용하는 것이 낫다.
    - Image를 pull 하는 것이 build하는 것 보다 거의 항상 빠르기 때문이다.
    - 또한 registry에 등록하지 않고, 동일한 app을 각기 다른 여러 사람이 각자의 컴퓨터에서 build하다보면, 각 image에 사이에 차이가 생기는 상황이 발생할 수 있다.
    - 반면에 registry에 등록해 두고 registry에서 pull해서 사용한다면, 모든 사람이 동일한 image를 사용한다는 것이 보장된다.



- 거대한 monorepo의 root directory에서 build하는 경우

  > 이는 Buildkit을 사용하지 않을 경우에만 해당된다.

  - Dockerfile을 거대한 monorepo의 root directory에 두고 build할 경우 monorepo의 모든 file과 directory가 build context에 포함되게 된다.
    - 매 build마다 repoistory의 모든 file들을 묶어서 Docker server로 전송해야하므로 이는 매우 비효율적이다.

  ```
  # 아래와 같이 Dockerfile을 monorepo의 root에 둘 경우 매우 비효율적이다.
  monorepo
  ├── app1
  │   └── source...
  ├── app2
  │   └── source...
  ├── Dockerfile.app1
  └── Dockerfile.app2
  ```

  - 이 문제는 아래와 같은 방식으로 해결할 수 있다.
    - Monorepo 내에 있는 각 app directory에 Dockerfile을 작성한다.
    - 혹은 Buildkit을 사용한다.

  ```
  # 아래와 같이 변경해준다.
  monorepo
  ├── app1
  │   ├── Dockerfile
  │   └── source...
  └── app2
      ├── Dockerfile
      └── source...
  ```



- Buildkit을 사용하지 않는 것
  - Buildkit은 보다 효율적인 image build를 위해 Docker 23.0. 부터 추가된 builder이다.
    - 다양한 기능이 새롭게 추가되었다.
    - 사용 방법은 기존 builder와 완전히 동일하지만 보다 빠르고 효율적인 build가 가능하다.
  - Buildkit을 사용할 수 있다면, 사용하지 않을 이유가 없다.



- 변경사항이 있을 때 마다 rebuild를 해야하는 경우
  - Compile언어가 아닌 interpreter 언어에서 code가 약간 바뀌었다고 image를 rebuild하고 container를 다시 생성할 필요는 없다.
  - volume을 사용해서 변경된 부분만 container에 적용해주면 된다.
  - 물론 build에 시간이 오래 걸리지 않고, image의 크기가 크지 않다면, 변경 사항이 있을 때 마다 image를 rebuild해도 상관은 없다.





# Build context

- Build context

  - Docker server가 image를 빌드하기 위해 필요로 하는 file들을 의미한다.
  - Image를 빌드하기 위해 Docker client는 build context를 묶어서 tar acrchive로 만든 뒤 Docker server로 전송한다.
    - Buildkit을 사용하지 않을 경우, 기본적으로 Docker client는 working directory의 모든 file과 directory를 build context로 보고 이들을 묶어 Docker server로 전송한다.
    - Docker client는 image를 build할 때 마다 build context를 생성하여 Docker server로 전송하므로, 매 build마다 archive를 생성하고, 이를 저장하고, network를 통해 Docker server로 보내는 비용이 발생한다.
  - `docker build` 명령어를 실행하면 아래와 같은 image를 맨 첫 줄에서 확인할 수 있다.

  ```bash
  $ docker build .
  
  Sending build context to Docker daemon 45.3 MB Step 1: FROM ...
  ```

  - `.dockerignore`
    - Build context에서 제외시킬 file 혹은 directory들을 정의하는 file이다.
    - `.dockerignore`에 포함된 file 혹은 directory들은 build context에 포함되지 않는다.
    - 작성법은 `.gitignore` file과 거의 유사하다.





