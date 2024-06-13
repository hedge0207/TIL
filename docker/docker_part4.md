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
