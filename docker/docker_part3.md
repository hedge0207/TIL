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

  - 기본 logging driver를 설정하기 위해서는 Docker daemin의 설정을 변경해야한다.
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

