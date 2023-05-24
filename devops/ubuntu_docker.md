# Docker로 Ubuntu 실행하기

- Docker Container 실행하기

  - 원하는 ubuntu images를 pull 받는다.

  ```bash
  $ docker pull <ubuntu_image>:[version]
  ```

  - Ubuntu container를 실행한다.

  ```bash
  $ docker run -d --name ubuntu -p 22:22 -it --privileged ubuntu:latest
  ```

  - Container에 접속하기
    - Windows 환경에서 GitBash를 사용할 경우 아래와 같이 `winpty`를 붙여줘야한다.

  ```bash
  $ [winpty] docker exec -it ubuntu bash
  ```



- 필수 package 설치하기

  - 먼저 `apt-get`을 update한다.

  ```bash
  $ apt-get update
  ```

  - vim editor 설치하기

  ```bash
  $ apt install vim
  ```

  - git 설치하기

  ```bash
  $ apt install git
  ```

  - curl 설치하기

  ```bash
  $ apt install curl
  ```

  

