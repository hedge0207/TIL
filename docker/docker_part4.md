# Docker Stack

- Docker Stack
  - Docker Swarm을 관리하기 위한 툴이다.
  - Docker Compose가 여러 개의 container로 구성된 애플리케이션을 관리하기 위한 도구라면, Docker Stack은 여러 개의 애플리케이션을 관리하기 위한 도구라고 보면 된다.
    - 더 직관적으로는, Docker compose는 container 들을 관리하는 도구이고, Docker Stack은 service들을 관리하는 도구이다.
    - Docker Compose는 개발에는 적합하지만, 운영 환경에서는 적합하지 않을 수 있다.
    - 예를 들어 Docker Compose는 `docker compose` 명령이 실행되는 순간에만 container의 상태가 올바른지 확인한다.
    - 반면에, Docker Stack은 이상적인 서비스 상태가 무엇인지 알고 있으며, 이상적인 상태와 현재 상태가 다를 경우 조치가 가능하다.
    - Docker Compose는 기본 네트워크로 bridge를 사용하지만, Docker Stack은 기본 네트워크로 Overlay를 사용한다.
  - Stack을 배포하면 stack file에 정의된 service들이 배포된다.
    - 해당 service들은 다시 container를 생성한다.
    - 결국 stack이 service를 생성하고 service가 container를 생성하는 구조이다.



- Test 환경 구성

  - Docker network 생성

  ```bash
  $ docker network create dind
  ```

  - DinD container 생성
    - Swarm을 구성하기 위한 dind container 2개와 image를 공유하기 위한 Docker registry 1개를 생성한다.
    - 위에서 생성한 Docker network를 사용한다.

  ```yaml
  version: '3.2'
  
  services:
    dind1:
      image: docker:dind
      container_name: dind1
      privileged: true
      environment:
        - DOCKER_TLS_CERTDIR=/certs
      networks:
        - dind
    
    dind2:
      image: docker:dind
      container_name: dind2
      privileged: true
      environment:
        - DOCKER_TLS_CERTDIR=/certs
      networks:
        - dind
    
    registry:
      image: registry:latest
      container_name: docker-registry
      networks:
        - dind
  
  networks:
    dind:
      name: dind
      external: true
  ```

  - dind1 container에서 swarm mode를 시작한다.

  ```bash
  $ docker swarm init
  ```

  - dind2 container를 swarm node로 합류시킨다.

  ```bash
  $ docker swarm join --token <token> dind1:2377
  ```

  - dind1 container에서 swarm이 잘 구성되었는지 확인한다.

  ```bash
  $ docker node ls
  ```



- Stack 관련 명령어

  - `config`
    - 최종 config file 확인하기 위해 사용한다.
    - `--compose-file` 옵션 뒤에 yaml file을 입력하면 된다.

  ```bash
  $ docker stack config --compose-file docker-compose.yml
  ```

  - `deploy`
    - 새로운 stack을 배포하거나, 기존 stack을 update하기 위해 사용한다.

  ```bash
  $ docker stack deploy --compose-file docker-compose.yml <stack_name>
  ```

  - `ls`
    - Stack 들의 목록을 확인하기 위해 사용한다.

  ```bash
  $ docker stack ls
  ```

  - `ps`
    - Stack 내의 task들의 목록을 확인하기 위해 사용한다.
    - `--filter` 혹은 `-f` 옵션을 사용하여 filtering이 가능하다.

  ```bash
  $ docker stack ps <stack_name>
  ```

  - `services`
    - Stack에 속한 service들의 목록을 확인하기 위해 사용한다.
    - `--filter` 혹은 `-f` 옵션을 사용하여 filtering이 가능하다.

  ```bash
  $ docker stack services <stack_name>
  ```

  - `rm`
    - Stack을 삭제하기 위해 사용한다.
    - Stack을 삭제하면 해당 stack은 물론이고 stack이 생성한 service, container가 모두 삭제된다.
  
  ```bash
  $ docker stack rm <stack> [stack2 ...]
  ```
  





# Docker volume과 권한, 소유자, 소유 그룹

- Docker container 내에서의 uid와 gid

  > https://medium.com/@mccode/understanding-how-uid-and-gid-work-in-docker-containers-c37a01d01cf

  - 아무런 option을 주지 않을 경우 container 내의 모든 process는 root로 실행된다.
  - Linux kernel은 모든 process를 실행할 때 프로세스를 실행한 user의 uid와 gid를 검사한다.
    - User name과 group name이 아닌 uid와 gid를 사용한다는 것이 중요하다.
  - Docker container 역시 kernel을 가지고 있으므로 container 내부에서 process 실행시 uid와 gid를 검사한다.



- Container 실행시 user 설정하는 방법

  - Docker run 명령어 실행시 container 내의 default user를 설정할 수 있다.

  ```bash
  $ docker run --user=[ user | user:group | uid | uid:gid | user:gid | uid:group ]
  ```

  - Docker compose file의 service 아래에 아래와 같이 설정할 수 있다.

  ```yaml
  services:
    test:
      user: [ user | user:group | uid | uid:gid | user:gid | uid:group ]
  ```

  - 만약 존재하지 않는 user name을 옵션으로 줘서 container를 실행하려 할 경우 아래와 같은 error가 발생한다.

  ```bash
  $ docker run -it --name my-ubuntu --user foo ubuntu:20.04 /bin/bash
  # docker: Error response from daemon: unable to find user foo: no matching entries in passwd file.
  ```

  - 반면에 존재하지 않는 uid를 줄 경우 error가 발생하지 않는다.
    - 다만 container에 attach할 경우 `I have no name!`이라는 user name이 보이게 된다.

  ```bash
  $ docker run -it --name my-ubuntu --user 1010 ubuntu:20.04 /bin/bash
  ```



- Bind-mount volume의 소유자

  - Docker compose file

  ```yaml
  version: '3.2'
  
  
  services:
    ubuntu:
      user: 1200:1200
      container_name: my_ubuntu
      image: ubuntu:20.04
      volumes:
        - ./dir:/home/dir
      command: "/bin/bash"
      tty: true
  ```

  - Container 내부의 file 소유자
    - Container 내부에는 서는 bind mount 대상인 file의 유무와 무관하게 host에 있는 file의 소유자, 그룹이 소유자와 소유 그룹이 된다.
    - 예를 들어 host에서 foo라는 사용자가 dir을 만들었다면 container 내부에 `/home/dir`이 원래 있었는지와 무관하게 container 내부의 `/home/dir`의 소유자, 소유 그룹은 foo와 foo의 그룹이 된다.
  - Host machine의 file 소유자
    - Bind mount를 통해 volume을 설정하더라도 소유자는 변경되지 않는다.
    - 예를 들어 위에서 `dir`을 foo라는 사용자가 만들었다면, bind mount를 하더라도 해당 file의 소유자는 foo이다.
    - Host machine에 없는 file을 대상으로 bind mount할 경우 Docker가 해당 file을 생성하는데, 이 때는 root 권한으로 생성된다.



- 기본 umask 설정

  - 예를 들어 아래와 같이 5초 마다 umask 값을 출력하는 python code가 있다고 가정해보자.

  ```python
  # main.py
  
  import os
  import time
  
  try:
      while True:
          os.system("umask")
          time.sleep(5)
  except (KeyboardInterrupt, SystemExit):
      logger.info("Bye!")
  ```

  - Dockerfile을 아래와 같이 설정한다.
    - `.bashrc`은 user의 home directory에 생성되므로, user 추가시 `-m` option을 줘야한다.


  ```dockerfile
FROM python:3.8.0

RUN useradd -m -u 1005 foo

USER foo

# .bashrc에 umask 0002 명령어를 추가한다.
RUN echo "umask 0002" >> ~/.bashrc

COPY ./main.py /main.py

ENTRYPOINT ["python", "main.py"]
  ```

  - 위 예시의 경우 0002를 출격할 것 같지만, 0002를 출력한다. 즉, 의도한 대로 동작하지 않는다.
    - 반면에 `docker exec -it <container> /bin/bash`와 같이 입력하여 직접 `python main.py`를 실행시키면 0002가 제대로 출력된다.

  - 아래와 같이 dockefile을 작성한다.
    - `umask 0002`와 python script 실행이 한 세션에서 실행될 수 있도록 한다.

  ```dockerfile
FROM python:3.8.0

RUN useradd -m -u 1005 foo

USER foo

COPY ./main.py /main.py

ENTRYPOINT ["/bin/bash", "-c", "umask 0002 && python main.py"]
  ```



- Dockerfile에서 `COPY` 명령어 실행시 소유권과 권한을 아래와 같이 설정할 수 있다.

  - 설정하지 않을 경우 기본적으로 소유권은 root,  file의 권한은 334, directory의 권한은 755로 설정된다.\
  - 단 `--chown`와 `--chmod` 옵션은 linux container에만 적용되며, windows container에는 적용되지 않는다.

  ```bash
  COPY [--chown=<user>:<group>] [--chmod=<perms>] <src> <dest>
  COPY [--chown=<user>:<group>] [--chmod=<perms>] ["<src>" "<dest>"]
  ```



- Docker compose options
  - tty:true로 주면 docker run 실행시에 -t option을 준 것과 동일하다.
  - stdin_open:true로 주면 docker run 실행시에 -i option을 준 것과 동일하다.



# etc

- Orphan container

  - Docker를 사용하다보면 `Found orphan containers ([<container_name>]) for this project.`과 같은 warning이 발생할 때가 있다.
    - Warning이므로 container를 실행하는 데는 아무런 문제는 없다.
  - Orphan container warning이 발생하는 원인은 아래와 같다.
    - Docker compose는 각 project를 구분하기 위해서 project name을  사용한다.
    - Project name은 project 내의 container와 다른 resource들(e.g. docker network)을 고유하게 식별하기 위한 identifier를 생성하기 위해 사용된다.
    - 예를 들어 project name이 `foo`이고, 두 개의 service `db`와 `app`이 있을 때, docker-compose.yml 파일에서 각 service의 container name을 설정해주지 않았다면  Compose는 `foo-db-1`과 `foo-app-1`이라는 두 개의 container를 생성할 것이다.
    - Orphan container warning은 같은 project name을 가진 container가 docker-compose.yml 파일에는 정의되어 있지 않을 때 발생한다.
    - 대부분의 문제는 project name의 default 값이 docker-compose.yml 파일이 위치한 directory name이라 발생한다.
  - 상황1. 기존 docker-compose.yml을 수정했을 경우
    - 처음 orphan service를 정의하고 container를 실행하면 project name은 default 값인 docker-compose.yml 파일이 위치한 directory name으로 설정된다.
    - 이 때, `orphan` container를 삭제하지 않은 상태에서, docker-compose.yml 파일을 변경한 후 다시 실행하면, 같은 project name을 가진 `orphan`이라는 container는 생성되어 있는데, 해당 container가 docker-compose.yml 파일에는 정의되어 있지 않으므로 orphan container warning이 발생한다.

  ```yaml
  # 기존 docker-compose.yml 파일이 아래와 같을 때, docker compose up으로 container를 생성하고
  services:
    orphan:
      container_name: orphan
      image: hello-world:lates
      
  
  # 이후에 아래와 같이 변경하여 다시 docker compose up으로 container를 생성하면 orphan이라는 orphan container가 있다는 warning이 발생한다.
  services:
    new:
      container_name: new
      image: hello-world:lates
  ```

  - 상황2. 동일한 directory에서 복수의 docker-compose.yml 파일을 사용할 경우
    - 같은 directory에 아래와 같이 두 개의 docker-compose.yml 파일이 있다고 가정해보자.
    - 마찬가지로 project name은 default 값인 두 개의 docker-compose.yml 파일이 위치한 directory name으로 설정된다.
    - 이 때, `docker-compose up`을 실행하여 docker-compose.yml에 정의된 container를 실행하고, `docker-compose -f docker-compose.bar.yml up`을 통해 docker-compose.bar.yml에 정의된 container를 실행하면 같은 project name으로 생성된 `foo` container가 있으나 `docker-compose.bar.yml` 파일에는 정의되어 있지 않으므로 orphan container warning이 발생한다.

  ```yaml
  # docker-compose.yml
  services:
    foo:
      container_name: foo
      image: hello-world:lates
      
  # docker-compose.bar.yml
  services:
    bar:
      container_name: bar
      image: hello-world:lates
  ```

  - Orphan container의 생성을 방지하는 방법
    - 대부분의 문제는 project name의 default 값인 directory name을 사용할 때 발생한다.
    - 따라서 default 값을 사용하지 않도록 project name을 설정하면 된다.
    - `docker compose` 명령어 실행시 아래와 같이 `-p` 옵션을 주어서 project name을 설정할 수 있다.
    - 혹은 `COMPOSE_PROJECT_NAME` 환경 변수를 설정하는 방법도 있다.

  ```bash
  $ docker compose -p foo up
  $ docker compose -f docker-compose.bar.yml -p bar up
  ```

  - 아래와 같이 docker-compose.yml 파일의 top level에 `name`을 설정할 수도 있다.

  ```yaml
  name: foo
  
  services:
    foo:
      container_name: foo
      image: hello-world:latest
  ```



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





# alpine image

- alpine image의 경우 일반 image에 비해 size가 작긴 하지만, 경우에 따라 성능에 상당한 차이가 있을 수 있다.

  > https://superuser.com/questions/1219609/why-is-the-alpine-docker-image-over-50-slower-than-the-ubuntu-image

  - 예를 들어 `python:3.8.0` image와 `python:3.8.0-alpine` image의 경우 size는 `python:3.8.0-alpine`이 훨씬 작지만, 성능은 `python:3.8.0`이 보다 뛰어나다.
  - 이러한 차이가 나는 이유는 두 image가 서로 다른 방식으로 구현되었기 때문이다.

