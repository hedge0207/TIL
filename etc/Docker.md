# Docker

> http://www.pyrasis.com/docker.html

- Docker란 무엇인가

  - 모든 개발자가 Docker를 사용할 줄 알아야 하는 것은 아니다. 그러나 모든 개발자는 Docker에 대해서 이해하고 있어야 한다.
  - Linux 컨테이너를 만들고 사용할 수 있도록 하는 컨테이너화 기술.
    - 컨테이너: 애플리케이션을 환경에 구애 받지 않고 실행하는 기술
    - 예를 들어 gitlab을 우분투에 설치할 때와, CentOS에 설치할 때 명령어가 각기 다르다. 그러나 컨테이너 도구인 Docker를 사용하면 어느 환경이든 상관 없이 동일한 명령어로 gitlab을 실행할 수 있다.
  - 컨테이너를 Docker 이미지라는 파일로 저장하여 이 이미지 파일만 있다면 언제든 해당 이미지 파일에 저장된 환경을 세팅할 수 있게 된다.
      - 이미지 파일은 컨테이너를 조립할 수 있는 자재라고 생각하면 된다.
    - Go로 개발 중이다.



- 왜 도커를 사용해야 하는가
  - 서버에 배포를 할 때 개발 환경과 동일한 세팅을 서버에도 해주어야 한다.
    - 예를 들어 프론트는 Vue, 백은 Django, DB는 MySQL을 사용해 개발했다면 서버에도 이것들이 동작할 수 있도록 해주어야 한다.
    - 복잡한 서비스일 수록 서버 환경을 개발 환경과 동일하게 세팅하는 것에 오랜 시간과 노력이 들어가게 된다.
    - 또한 서버를 옮겨야 하는 경우에도 옮기려는 서버에 동일한 환경을 세팅해야 하는데 이전 서버를 세팅했던 개발자가 퇴직을 한 상황이고 메뉴얼도 존재하지 않는다면 곤란한 일이 발생하게 된다.
    - 이럴 때 도커를 사용하면 훨씬 편하게 세팅을 마칠 수 있다.
  - 한 서버에서 여러 서비스를 운영할 때 충돌이 발생할 수 있다.
    - 예를 들어 A 서비스는 Java7을 사용하고, B 서비스는 Java8을 사용한다면 서로 다른 버전 때문에 충돌이 발생할 수 있다.
  - 가상 환경을 사용하면 되는 것 아닌가?
    - 가상 환경은 서버의 자원을 분할하여 작동하게 된다.
    - 예를 들어 A, B라는 2개의 프로젝트를 각각 가상환경을 만들어서 실행할 경우 100이라는 한정적 자원을 A, B가 분할해서 사용하게 된다. 만일 C, D, E 등 새로운 프로젝트를 진행한다면 자원이 그만큼 분할되게 된다.
    - 또한 가상 환경은 불필요한 중복을 발생시킨다.
    - 예를 들어 A, B 프로젝트가 모두 파이썬으로 개발되었다고 할 때 A의 가상환경에도 파이썬이 설치되어야 하고, B의 가상환경에도 파이썬이 설치되어야 하므로 비효율적이다.
    - 컨테이너는 하드웨어를 가상화하는 가상 환경과 달리 커널을 공유하는 방식이기에 실행 속도가 빠르고, 성능 상의 손실이 거의 없다.







# Docker 사용해보기

- 다운로드 후 설치하기

  > https://www.docker.com/get-started

  - 경우에 따라 리눅스 커널을 설치해야 할 수 있는데 안내에 따라 설치하면 된다.
  - 설치 후 cmd 창에서 `docker --version`을 입력하여 제대로 설치 되었는지 확인한다.



- Docker에 mariaDB 설치하고 실행하기

  - mariaDB 이미지 받기
    - https://hub.docker.com/ 이 사이트에는 개발에 필요한 거의 모든 환경이 이미지 형태로 저장되어 있다.
    - pull 명령어는 우선 내 컴퓨터에서 mariadb라는 이름으로 저장되어 있는 이미지 파일을 찾는다.
    - 찾을 수 없을 경우 위 사이트에 등록된 이미지들 중 해당 이름으로 등록된 이미지를 다운 받게 된다.

  ```
  //docker pull ㅏ이미지명ㅓ:ㅏ태그명ㅓ 태그는 필수가 아니다. 
  
  docker pull mariadb
  ```

  - 컴퓨터에 다운 된 docker 이미지들 보기
    - 아래 명령어를 입력했을 때 mariadb가 나온다면 제대로 다운 받아진 것이다.

  ```
  docker images
  ```

  - 다운 받은 이미지로 컨테이너 생성하기
    - `create` 명령어는 다운 받은 이미지를 가지고 컨테이너를 만드는 명령어이다.
    - `--name`은 컨테이너의 이름을 설정하는 옵션이다.
    - `-p {호스트의 포트 번호}:{컨테이너의 포트 번호}`는 호스트와 컨테이너의 포트를 연결하는 옵션이다.
    - `-e`는 컨테이너 내의 환경변수를 설정하는 옵션이다. 

  ```
  //docker create ㅏ옵션ㅓ ㅏ이미지명ㅓ:ㅏ태그ㅓ
  //아래 명령어에서 "--name maria-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwer"까지는 옵션이고 "mariadb"는 이미지명, 태그는 없다.
  
  docker create --name maria-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwer mariadb
  ```

  - 컨테이너 실행하기
    - `start` 명령어는 `create` 명령어로 만든 컨테이너를 사용하겠다는 의미이다.

  ```
  //docker start ㅏ컨테이너명 또는 idㅓ
  
  docker attach maria-db
  ```

  - 컨테이너에 접속하기
    - `attach` 명령어는 컨테이너 내 CLI(Command line interface, 명령 줄 인터페이스)를 이용하는 명령어이다.
    - DB나 서버 같이 백그라운드에서 실행되는 컨테이너의 경우 입력은 할 수 없고 출력만 보이게 된다.
    - `ctrl+p+q`로 종료한다.

  ```
  //docker attach {컨테이너 id 또는 이름}
  
  docker attach maria-db
  ```

  - DB나 서버의 경우 아래와 같이 접속하면 된다.
    - `exec` 명령어는 container에 bin/bash를 실행시켜서 쉘을 띄우는데도 사용한다.
    - `docker exec maria-db /bin/bash` 입력 후(`ctrl+d` 혹은 `exit`로 종료)
    - `mysql -u root -p`를 입력해도 결과는 동일하다.
    - `-it`는 컨테이너로 들어갔을 때 bash로 CLI 입출력을 사용할 수 있도록 해 준다(`-i`.,`-t`를 따로 입력해도 된다).

  ```
  docker exec -it maria-db mysql -u root -p
  ```

  - `attach`와 `exec`의 차이
    - `attach`: 현재 실행중인 컨테이너에 접속하는 것. docker에서 컨테이너는 프로세스 개념으로 run이나 start로 컨테이너가 실행되면 /bin/bash를 실행하는 이미지도 있어 `attach`를 입력했을 때 바로 쉘 프롬포트가 나오는 경우도 있지만 그렇지 않은 경우도 있다. 또한 attach로 바로 쉘 프롬포트에 접속하게되면 /bin/bash로 실행된 1번 PID에 접속하게 되는 것이므로 해당 콘솔에서 나가게 되는 경우 해당 컨테이너는 중지된다.
    - `exec`: 현재 실행중인 컨테이너에 특정 쉘 스크립트를 실행하는 것이다. exec명령어로 DB에 접속하면 해당 컨테이너에 bash shell을 실행시켜 쉘 프롬포트가 화면에 나오게 된다.  또한 기존에 열려있던 PID1에 물리는 것이 아닌 별도의 프로세스를 생성하여 bash 를 실행한다. 따라서 해당 쉘 프롬포트에서 exit하게되도 그 컨테이너는 중지되지 않고 유지된다.
    - 이는 둘의 종료 명령어에서도 차이가 드러나는데 `ctrl+d` 혹은 `exit`는 컨테이너를 종료시키지만 `ctrl+p,q`는 컨테이너를 종료시키지 않는다.

  - 한번에 실행하고 싶을 경우 아래 명령어를 입력한다.
    - `run` 명령어는 `pull`,`create`,`start`,`attach`를 한번에 실행하는 것과 같다.
    - `-d`는 백그라운드에서 실행하겠다는 것이다.

  ```
  docker run --name maria-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 -d mariadb
  ```

  - 위 명령어를 입력했을 때 아래와 같은 에러가 발생할 수 있다.

    - `docker: Error response from daemon: Ports are not available: listen tcp 0.0.0.0:3306: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.`
    - 이미 port를 사용하고 있다는 것인데 `netstat -a -o` 명령어를 입력하면 실행중인 port를 확인할 수 있다.

    - 목록에서 PID 확인 후 작업관리자에서 PID로 프로세스를 찾아 실행을 중지하면 된다.
- 또한 permission 관련 오류가 발생하면 `sudo`를 모든 명령어 앞에 붙여주면 된다.
  
  - 이는 비단 docker에만 한정되는 것은 아니다.
  - 그 후 아래와 같이 sql문을 사용하여 DB를 조작하면 된다.
  - 굳이 mariaDB를 컴퓨터에 설치하지 않아도, docker에서 컨테이너만 실행하면 mariaDB를 실행할 수 있다.
  
  ```sql
  create database ㅏdb명ㅓ
  use ㅏdb명ㅓ
  ```



- 기본적인 docker 명령어

  - 위에서 다룬 것들은 따로 적지 않았다.
  - 동작중인 컨테이너 재시작

  ```
  docker restart ㅏ컨테이너 이름 혹은 idㅓ
  ```

  - 동작중인 컨테이너 보기

  ```
  docker ps
  ```

  - 컨테이너 삭제

  ```
  docker rm ㅏ컨테이너 이름 혹은 idㅓ
  ```

  - 모든 컨테이너 삭제

  ```
  docker rm `docker ps -a -q`
  ```

  - 이미지 삭제

  ```
  docker rmi ㅏ옵션ㅓ ㅏ이미지ㅓ  //해당 이미지를 사용중인 컨테이너가 있을 경우에도 강제로 삭제하고 싶으면 -f 옵션을 사용하면 된다.
  ```

  - 모든 컨테이너 중지

  ```
  docker stop $(docker ps -aq)
  ```

  - 사용하지 않는 모든 도커 요소(이미지, 컨테이너, 네트워크, 볼륨 등) 삭제

  ```
  docker system prune -a
  ```

  -  도커 파일로 이미지 생성

  ```
  docker build -t ㅏ이미지명ㅓ
  ```

  - 도커 컴포즈 실행

  ```
  docker-compose up  //백그라운드에서 돌도록 하려면 -d 옵션을 붙인다.
  ```





# 참고

- https://www.yalco.kr/36_docker/
- https://www.youtube.com/watch?v=hWPv9LMlme8&t=886s
- https://sukill.tistory.com/9
- https://sleepyeyes.tistory.com/68
- https://zgundam.tistory.com/132
- https://www.popit.kr/%EA%B0%9C%EB%B0%9C%EC%9E%90%EA%B0%80-%EC%B2%98%EC%9D%8C-docker-%EC%A0%91%ED%95%A0%EB%95%8C-%EC%98%A4%EB%8A%94-%EB%A9%98%EB%B6%95-%EB%AA%87%EA%B0%80%EC%A7%80/

