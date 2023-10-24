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
  
  
  



