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







# DooD


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



- Services와 tasks
  - Service
    - Manager node 혹은 worker node에서 실행될 작업들을 의미한다.
    - Swarm system의 중심 구조이면서 사용자가 swarm과 상호작용하는데 가장 근본이 되는 요소이다.
    - Service를 생성할 때, 어떤 image를 사용하여 container를 생성할 것이고 해당 container가 어떤 명령어를 실행할지를 지정해줘야한다.
    - Replicated service model에서 swarm manager는 특정 수의 replica task들을 node들에게 뿌려준다.
    - Global service에서 swarm은 cluster 내의 모든 가용한 node들에게 하나의 task만을 실행하도록 한다.
  - Task
    - Docker container와 container 내에서 실행할 명령을 의미한다.
    - Manager node가 worker node들에게 task를 할당하면, task들은 다른 node로 이동할 수 없다.
    - 오직 할당 받은 node에서 실행되거나 실패될 뿐이다.



- Load balancing
  - Swarm manager는 ingress load balancing을 사용한다.
    - 이를 통해 service를 swarm 외부에서 접근할 수 있게 된다.
  - Swarm manager는 service에 자동으로 PublishedPort를 할당할 수 있으며, 사용자가 수종으로 설정할 수도 있다.
    - Port를 설정하지 않을 경우 30000에서 32767 사이의 port를 자동으로 할당한다.
  - Cloud load balancer 등의 외부 컴포넌트는 cluster에 속한 아무 node의 PublishedPort를 통해 service에 접근할 수 있다.
    - 해당 node가 task를 실행 중이 아니라도 접근할 수 있다.
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
    - Worker node용 token과 manager용 token이 따로 생성되므로, worker를 입력해줘야한다.

  ```bash
  $ docker swarm join-token worker
  ```

  - 추가 됐는지 확인
    - ServerA의 Docker container 내부에서 아래 명령어를 입력한다(아래 명령어는 오직 Swarm manager에서만 사용이 가능하므로, ServerB에서는 확인이 불가능하다).
    - ServerA의 docker와 ServerB의 docker가 모두 뜬다면 성공적으로 swarm에 추가가 된 것이다.

  ```bash
  $ docker node ls
  ```





## Swarm 관련 명령어

> https://seongjin.me/docker-swarm-introduction-nodes/

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
  - Docker swarm 내에서 HOSTNAME 값은 중복이 가능하지만 ID 값은 중복될 수 없다.
  - AVAILABILITY
    - Active: 새로운 task를 할당 받을 수 있는 상태
    - Pause: 새로운 task를 할당 받지는 않지만 현재 실행중인 task는 구동중인 상태
    - Drain: 새로운 task도 할당 받지 않고, 실행 중인 task들도 모두 종료되는 상태
    - 단 이는 swarm service에 해당하는 사항으로, service가 아닌 standalone container의 경우 영향을 받지 않는다.
    - 즉, 예를 들어 node가 Drain 상태라고 하더라도 해당 Docker로 띄운 standalone container는 계속 실행된다.
  - MANAGER STATUS
    - manager node에만 표시된다.
    - Leader: Swarm 관리와 orchestration을 맡은 노드임을 의미한다. 
    - Reachable: 다른 매니저 노드들과 정상적으로 통신 가능한 노드임을 의미하며, 만일 leader node에 장애가 발생할 경우 이 상태값을 가진 node들 중에 새로운 leader를 선출한다.
    - Unavailable: Leader를 포함한 다른 매니저 노드들과 통신이 불가능한 상태임을 의미한다.

  ```bash
  $ docker node ls
  ID                           HOSTNAME       STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
  vpaqawacp368mhz27ugn12qw     42535425321b   Ready     Active                          24.0.2
  qgebfgjontqwmcvt4tibrevz *   35262352352q   Ready     Active         Leader           24.0.2
  ```



- 특정 노드 상세 조회

  - 특정 node에 대한 상세한 정보를 JSON 형식으로 출력한다.

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
  $ docker node update --label-add <key=value | key> <node 식별자>
  ```

  - Label 삭제하기

  ```bash
  $ docker node update --label-rm <key=value | key> <node 식별자>
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
