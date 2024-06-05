# Nginx

- Nginx란
  - 동시접속 처리에 특화된 Web Server
    - 웹 서버에 대한 설명은 [WAS와 Web Sever](https://github.com/hedge0207/TIL/blob/master/CS/web_application_architecture.md#was%EC%99%80-web-server) 참고
  - Apache의 문제점을 보완하기 위해 등장했다.
    - Apache를 비롯한 기존의 웹 서버들은 1만개의 동시 연결을 처리하기 어렵다는 문제가 있었다
    - 이를 C10k(Concurrent 10,000 clients/connections)라 부른다.
    - Apache 웹 서버는 Process-Driven 방식으로 클라이언트로부터 요청이 올 때마다 Process 또는 Thread를 생성하여 처리한다.
    - 요청이 올 때마다 Thread가 생성되므로 시스템 자원이 고갈되는 문제가 발생한다.
  - Nginx는 Evemt-Driven 방식을 사용한다.
    - 싱글 스레드의 Event Loop가 계속 돌아가면서 Event Queue에 요청이 들어오면 Event Loop가 Thread Poll에 적절히 분배하여 비동기적으로 처리하도록 한다.
    - 따라서 많은 요청이 한 번에 오더라도 무리없이 처리할 수 있다.
  - 아직 Web Server 점유율은 Apache가 압도적이지만 Nginx도 꾸준히 성장하고 있다.



- UpStream과 DownStream
  - 데이터의 흐름을 강물에 비유한 것.
    - 지형의 고저차에 의해 상류와 하류가 결정되는 강물과 달리 데이터의 흐름에 따라 상류와 하류가 유동적으로 변동될 수 있다.
  - 구분
    - 데이터를 보내는 쪽을 UpStream, 데이터를 받는 쪽을 DownStream이라 한다.
    - 만일 서버로 부터 특정 데이터를 받아올 경우 데이터를 받아오는 클라이언트는 하류가 되고, 데이터를 보내주는 서버는 상류가 된다.



## 설치

## Docker로 설치

- Docker image 받기

  ```bash
  $ docker pull nginx
  ```



- 컨테이너 실행하기

  ```bash
  $ docker run <container 명> -p <외부포트>:<내부포트> <이미지명>
  ```



- Nginx Docker container 사용시 주의할 점

  - 사전지식
    - Docker network 내부에서 container에게 할당되는 IP는 container가 정지되면 할당 해제되고, 다시 실행되면 새로 할당된다.
    - 그러나 컨테이너 내부에서 DNS(docker service name)로 요청을 보내면 Docker가 service name에 해당하는 IP address로 바인딩해주기에 통신에는 영향이 없다.
    - 다만, Nginx container 사용시에는 문제가 생길 수 있다.
  - 아래와 같이 간단한 app을 생성한다.
    - `/ping`으로 요청을 보내면 "pong"을 반환하는 간단한 app이다.
    - 총 3개의 application을 container로 실행할 것이고, 각 container는 자신들의 port 번호를 router prefix로 사용한다.
    - 예를 들어 port가 8017이면 `localhost:8017/8017/ping`과 같이 요청을 보내야한다.

  ```python
  import os
  
  from fastapi import FastAPI, APIRouter
  import uvicorn
  
  PORT = int(os.environ.get("PORT", 8017))
  
  app = FastAPI()
  
  router = APIRouter(
      prefix=f"/{PORT}"
  )
  
  @router.get("/ping")
  def ping():
      return "pong"
  
  
  app.include_router(router)
  
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=PORT)
  ```

  - 위 app을 build하기 위한 Dockerfile을 작성한다.

  ```dockerfile
  FROM python:3.8.0
  
  COPY ./main.py /main.py
  COPY ./requirements.txt /requirements.txt
  
  RUN pip install -r requirements.txt
  
  ENTRYPOINT ["/bin/bash", "-c", "python -u main.py"]
  ```

  - 위 app을 build한다.

  ```bash
  $ docker build -t network-test .
  ```

  - Nginx configuraion file을 작성한다.
    - Docker service name으로 요청을 전송하도록 설정한다.

  ```nginx
  user  nginx;
  worker_processes  auto;
  
  error_log  /var/log/nginx/error.log warn;
  pid        /var/run/nginx.pid;
  
  events {
      worker_connections  4096;
  }
  
  http {
  
      server {
          listen       3015;
          listen  [::]:3015;
          server_name  localhost;
  
          location /8091 {
              proxy_pass http://network-container1:8091;
          }
  
          location /8092 {
              proxy_pass http://network-container2:8092;
          }
          
          location /8093 {
              proxy_pass http://network-container3:8093;
          }
      }
  }
  ```

  - Docker network를 생성한다.

  ```bash
  $ docker network create network-test
  ```

  - Docker compose file을 작성한다.

  ```yaml
  version: '3'
  
  services:
    network-container1:
      profiles: ["app"]
      container_name: network-container1
      image: network-test:latest
      environment:
        PORT: 8091
      networks:
        - network-test
    
    network-container2:
      profiles: ["app"]
      container_name: network-container2
      image: network-test:latest
      environment:
        PORT: 8092
      networks:
        - network-test
    
    network-container3:
      profiles: ["app"]
      container_name: network-container3
      image: network-test:latest
      environment:
        PORT: 8093
      networks:
        - network-test
    
    network-container:
      profiles: ["nginx"]
      container_name: network-container
      image: nginx:latest
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
      ports:
        - 3015:3015
      networks:
        - network-test
  
  # 위에서 생성한 network를 입력한다.
  networks:
    network-test:
      external:
        name: network-test
  ```

  - Container들을 실행시킨다.

  ```bash
  $ docker compose --profile app up -d
  $ docker compose --profile nginx up -d
  ```

  - Nginx로 요청을 보낸다.
    - 모두 정상적으로 응답이 온다.

  ```bash
  $ curl localhost:3015/8091/ping
  $ curl localhost:3015/8092/ping
  $ curl localhost:3015/8093/ping
  ```

  - `network-test` network를 확인해보면 각 container에 아래와 같이 IP가 할당된 것을 볼 수 있다.

  ```bash
  $ docker network inspect
  "Containers": {
      "3gwgre4h3434hw34hreh3eh34h3w44hw34h34h4w3hh43h34h43h43h34h4hh433": {
          "Name": "network-container1",
          "IPv4Address": "172.17.0.3/16",
      },
      "dsdg3232534246234tg443h34hw4h34534543yq3h34yh34y34t34t43t4g44453": {
          "Name": "network-container2",
          "IPv4Address": "172.17.0.2/16",
      },
      "grhytkj7k67i56j5656j56u56u8565867967i76i67u6u454565748484845yg12": {
          "Name": "network-container3",
          "IPv4Address": "172.17.0.4/16",
      }
  }
  ```

  - App container들을 정지 후 재실행 시킨다.

  ```bash
  $ docker compose --profile app stop
  $ docker compose --profile app start
  ```

  - 다시 `network-test` network를 확인해본다.
    - `network-container2`, `network-container3`의 IP가 변경된 것을 확인할 수 있다.

  ```bash
  $ docker network inspect
  "Containers": {
      "3gwgre4h3434hw34hreh3eh34h3w44hw34h34h4w3hh43h34h43h43h34h4hh433": {
          "Name": "network-container1",
          "IPv4Address": "172.17.0.3/16",
      },
      "dsdg3232534246234tg443h34hw4h34534543yq3h34yh34y34t34t43t4g44453": {
          "Name": "network-container2",
          "IPv4Address": "172.17.0.4/16",
      },
      "grhytkj7k67i56j5656j56u56u8565867967i76i67u6u454565748484845yg12": {
          "Name": "network-container3",
          "IPv4Address": "172.17.0.2/16",
      }
  }
  ```

  - 다시 Nginx로 요청을 보낸다.
    - IP가 변경되지 않은 `network-container1`으로 보내는 요청은 여전히 정상적으로 응답이 오는 반면, IP가 변경된 `network-container2`, `network-container3`로 보내눈 요청은 `502 Bad Gateway`가 응답으로 온다.

  ```bash
  $ curl localhost:3015/8091/ping		# "pong"
  $ curl localhost:3015/8092/ping		# 502 Bad GateWay
  $ curl localhost:3015/8093/ping		# 502 Bad GateWay
  ```

  - Nignx log를 확인해보면 아래와 같은 message를 확인할 수 있다.
    - `network-container2`(8092 port)로 요청을 보내면 변경된 IP인 172.17.0.4로 요청을 보내야 하는데, 기존 IP인 172.17.0.2로 요청을 보낸다.
    - `network-container3`도 마찬가지로 기존 IP로 요청을 보낸다.

  ```
  connect() failed (111: Connection refused) while connecting to upstream, request: "GET /8092/ping HTTP/1.1", upstream: "http://172.17.0.2:8092/8092/ping", host: "localhost:3015"
  connect() failed (111: Connection refused) while connecting to upstream, request: "GET /8093/ping HTTP/1.1", upstream: "http://172.17.0.4:8093/8093/ping", host: "localhost:3015"
  ```



- 해결방법

  - Nginx에는 hostname을 IP로 resolve해주는 name server를 설정하기 위한 `resolver`를 설정할 수 있다.
    - `resolver`는 `http`, `server`, `location` context에 작성이 가능하다.
    - `IP`에는 DNS 서버의 IP 주소를 지정하면 된다.
    - Docker 내부의 기본 DNS 서버는 일반적으로 127.0.0.11이며, container에서 `cat /etc/resolv.conf`로 확인이 가능하다.
    - `valid`에는 Nginx가 DNS 조회 결과를 캐시할 시간을 지정하며, 이 시간이 지나면 Nginx는 도메인 이름을 다시 조회하여 IP를 받아온다.	


  ```nginx
  resolver <IP> ipv4=on ipv6=off valid=30s;
  ```

  - Nginx 파일에 아래와 같이 resolver를 추가한다.
    - Docker 내부의 기본 DNS 서버 IP인 127.0.0.11를 입력한다.

  ```nginx
  user  nginx;
  worker_processes  auto;
  
  error_log  /var/log/nginx/error.log warn;
  pid        /var/run/nginx.pid;
  
  events {
      worker_connections  4096;
  }
  
  http {
      
      resolver 127.0.0.11 ipv4=on ipv6=off valid=30s;
  
      server {
          listen       3015;
          listen  [::]:3015;
          server_name  localhost;
  
          location /8091 {
              proxy_pass http://network-container1:8091;
          }
  
          location /8092 {
              proxy_pass http://network-container2:8092;
          }
          
          location /8093 {
              proxy_pass http://network-container3:8093;
          }
      }
  }
  ```

  - 이후에 `proxy_pass`에 URL을 위와 같이 문자열로 입력하는 것이 아니라, 변수에 할당한 후, 해당 변수를 설정해줘야 한다.

  ```nginx
  user  nginx;
  worker_processes  auto;
  
  error_log  /var/log/nginx/error.log warn;
  pid        /var/run/nginx.pid;
  
  events {
      worker_connections  4096;
  }
  
  http {
      
      resolver 127.0.0.11 ipv4=on ipv6=off valid=30s;
  
      server {
          listen       3015;
          listen  [::]:3015;
          server_name  localhost;
  
          location /8091 {
              set $network-container1 "http://network-container1:8091"
              proxy_pass $network-container1;
          }
  
          location /8092 {
              set $network-container2 "http://network-container2:8092"
              proxy_pass $network-container2;
          }
          
          location /8093 {
              set $network-container3 "http://network-container3:8093"
              proxy_pass $network-container3;
          }
      }
  }
  ```

  - `proxy_pass`에 변수를 설정해야 하는 이유

    > https://serverfault.com/questions/560632/some-nginx-reverse-proxy-configs-stops-working-once-a-day

    - `proxy_pass`에 변수가 아닌 static한 값을 줄 경우, Nginx가 conf 파일을 최초로 읽을 때 domain에 해당하는 IP를 resolve한다.
    - 반면에 변수는 변할 수 있는 값이므로, 매번 요청이 들어올 때 마다 `resolver`를 참조하여 domain에 해당하는 IP를 resolve한다.

  - 이제 다른 container들의 IP가 변경되더라도 Nginx는 `resolver`를 통해 domain에 해당하는 IP 값을 받아와서 정상적으로 동작하게 된다.

  - 예시에서는 Docker를 들었지만, IP가 동적으로 변경될 수 있는 service와 Nginx를 함께 사용할 경우 모두 적용할 수 있다.





## yum으로 설치

- 설치

  ```bash
  $ yum install nginx
  ```



- 명령어

  - 실행

  ```bash
  $ nginx
  ```

  - 실행중인지 확인

  ```bash
  $ ps -ef | grep nginx
  ```

  - 정지

  ```bash
  $ nginx -s stop
  ```

  - 재실행

  ```bash
  $ nginx -s reload
  ```



## Nginx 설정 파일

> 아래에 나온 설정들 보다 훨씬 다양한 설정들이 존재한다.

- nginx.conf

  - 위치는 설치 방식에 따라 다를 수 있으나 일반적으로 `/etc/nginx/conf`에 있다.
    - Nginx Docker image의 경우 `/etc/nginx`에 있다.
  
  - Nginx의 동작 방식을 설정해 놓은 파일이다.
  - root 권한이 있어야 수정이 가능하다.
  
  ```nginx
  user  nginx;
  worker_processes  auto;
  worker_rlimit_nofile 65535	
  error_log  /var/log/nginx/error.log notice;
  pid        /var/run/nginx.pid;
  
  events {
      worker_connections  1024;
  }
  
  http {
      include       /etc/nginx/mime.types;
      default_type  application/octet-stream;
      log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
      access_log  /var/log/nginx/access.log  main;
  
      sendfile        on;
      tcp_nopush      on;
  
      keepalive_timeout  65;	# 접속 시 커넥션 유지 시간을 설정한다.
      server_tokens off		# nginx 버전을 숨길지 여부를 정한다(일반적으로 보안을 위해서 숨긴다).
  
      #gzip  on;
  	# /etc/nginx/conf.d 디렉토리 아래 있는 .conf 파일을 모두 읽어 들인다.
      include /etc/nginx/conf.d/*.conf;
  }
  ```



- Top(Core block)

  - user
    - Nginx Worker Process의 user를 의미한다.
    - Woker Process의 권한을 설정할 때 이용한다.
  - worker_processes
    - 몇 개의 워커 프로세스를 실행할 것인지를 지정한다. 
    - 1 이상의 정수 혹은 auto로 설정이 가능하다(기본값은 1).
  - worker_rlimit_nofile
    - Worker process가 이용할 수 있는 최대 File Desciptor의 개수를 의미한다.
    - 일반적으로 worker_connections*2로 설정한다.
  - error_log
    - log를 남길 위치 및 로그 레벨을 설정한다.
    - `파일위치 레벨` 형식으로 작성한다.
  - pid
    - nginx master process PID를 저장할 파일 경로 지정

  ```nginx
  user  nginx;
  worker_processes  auto;
  worker_rlimit_nofile 65535	
  ```



- conf.d
  - nginx.conf 파일에서 include를 통해 읽어들일 설정들을 저장하는 디렉토리이다.
  - nginx.conf 파일에서 모든 설정을 관리하면 알아보기도 힘들고 지저분해질 수 있기에 이 디렉토리에 설정 파일들을 작성하고  include를 통해 가져와서 사용한다.



- Event Block

  - events 블록은 주로 네트워크 동작에 관련된 설정을 하는 영역이다.
  - worker_connections
    - 하나의 프로세스가 처리할 수 있는 커넥션의 수를 설정한다.
    - worker_rlimit_nofile보다 클 수 없다.
    - 최대 접속자 수는 `worker_processes * worker_connections`이다.

  ```nginx
  events {
      worker_connections  1024;
  }
  ```



- http Block Top

  - http 블록은 하위에 server 블록 및 location 블록을 갖는 루트 블록이다.
    - 여기서 선언된 값은 하위 블록에 상속된다.
    - nginx.conf와 같이 내부적으로 block이 나뉜다.
  - include
    - 읽어들일 파일을 지정한다.
  - index
    - Index page로 사용할 페이지를 지정한다.
  - default_type
    - Default MIME(Multipurpose Internet Mail Extensions)을 설정한다.
    - MIME는 이미지나 영성과 같은 파일을 text 형태로 전송하기 위한 인코딩/디코딩 기법을 의미한다.
    - 기본값은 text/plain이다.
  - log_format
    - HTTP, HTTPS 처리 Log의 format을 의미한다.
  - access_log
    - HTTP, HTTPS 처리 Log가 저장될 경로를 의미한다.
  - sendfile
    - Static File(이미지, 영상 등)을 전송할 때 sendfile() System Call의 사용 여부를 설정한다.
    - 기존의 read()/write() System Call에 비해 빠르다.
  - tcp_nopush
    - sendfile() System Call 이용시 TCP Socket에 TCP_CORK 설정 유무
    - TCP_CORK은 TCP Socket으로 Packet 전송시 Packet을 TCP Socket Buffer에 모았다가 한번에 보내도록 설정한다.
  - server_names_hash_bucket_size
    - Nginx에 등록할 수 있는 최대 server name의 개수
  - keepalive_timeout
    - 접속 시 커넥션 유지 시간을 설정한다.
    - 기본값은 75s이다.
  - server_tokens
    - nginx 버전을 숨길지 여부를 정한다(일반적으로 보안을 위해서 숨긴다).
  - client_max_body_size
    - Client Request의 최대 body size
  - client_body_buffer_size 
    - Client Request의 Body를 위한 Read Buffer의 크기
  - proxy_connect_timeout 
    - TCP Connection이 구축되는데 필요한 최대 대기 시간
  - proxy_send_timeout
    - Proxied Server에 Client의 Request를 전송하는데 필요한 최대 대기 시간
  - proxy_read_timeout 
    - Proxied Server로부터 Response를 수신하는데 필요한 최대 대기 시간
  - proxy_buffers
    - Proxied Server와의 Connection 한개당 이용하는 Read Buffer의 크기
    - `<Buffer의 개수> <각 Buffer의 크기>` 형식으로 입력한다.

  ```nginx
  http{
      include       /etc/nginx/mime.types;
      index		  index.html index.php;
      default_type  application/octet-stream;
      log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
      access_log  /var/log/nginx/access.log  main;
      sendfile        on;
      tcp_nopush 		on;
      server_names_hash_bucket_size 128;
      
      keepalive_timeout  65;	
      server_tokens off;
  }
  ```



- Nginx의 `access.log`와 `error.log`는 Nignx Docker image의 경우 `/var/log/nginx`에 저장된다.



##  Nginx SSL 인증서 설정

- SSL 인증서 설정

  - SSL 인증서 설정에는 아래와 같은 파일들이 필요하다.
    - 도메인 인증서
    - 개인키 파일
  - nginx.conf file에서 아래와 같이 추가해준다.

  ```nginx
  server {
      listener 443;
      server_name 도메인;
      
      ssl on;
      ssl_certificate			/도메인/인증서/경로;
      ssl_certificate_key 	/개인키/경로;
  }
  ```

  - 설정 후 nginx service를 재기동 해야한다.
    - nginx 설치 방식에 따라 재기동 명령어는 달라질 수 있다.

  ```bash
  $ systemctl restart nginx
  ```

  - 인증서를 교체해야 할 경우 인증서 file을 교체하고 nginx.conf을 변경한 뒤 nginx를 재실행하면 된다.









# 참고

- [나는 nginx 설정이 정말 싫다구요](https://juneyr.dev/nginx-basics)

- [nginx에 대한 정리](https://developer88.tistory.com/299)
- [Nginx Config](https://ssup2.github.io/theory_analysis/Nginx_Config/)
- http://nginx.org/en/docs/ngx_core_module.html

