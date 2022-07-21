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



- http server block



# 참고

- [나는 nginx 설정이 정말 싫다구요](https://juneyr.dev/nginx-basics)

- [nginx에 대한 정리](https://developer88.tistory.com/299)
- [Nginx Config](https://ssup2.github.io/theory_analysis/Nginx_Config/)
- http://nginx.org/en/docs/ngx_core_module.html

