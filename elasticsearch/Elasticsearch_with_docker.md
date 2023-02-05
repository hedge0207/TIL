# Docker로 ES, Kibana 설치하기

- image 받기

  > 아래 사이트에서 지원하는 버전 목록을 확인 가능하다.
  >
  > https://www.docker.elastic.co/

  - Elasticsearch image 받기

  ```bash
  $ docker pull docker.elaistc.co/elasticsearch/elasticsearch:<버전>
  ```

  - Kibana image 받기

  ```bash
  $ docker pull docker.elastic.co/kibana/kibana:<버전>
  ```



- 네트워크 생성

  - elasticsearch와 kibana를 연결할 네트워크를 생성한다.
  - 이루 ES와 Kibana를 실행할 때 아래에서 지정해준 네트워크명을 옵션으로 준다.

  ```bash
  $ docker network create <네트워크명>
  ```



- 실행

  - ES 실행하기
    - 단일 노드만 생성할 것이기에, envirenment 값으로 `discovery.type=single-node`을 준다.

  ```bash
  $ docker run --name <컨테이너명> --net <네트워크명> -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" <이미지명>
  ```
  
  - Kibana 실행하기
    - ES와 연결하기위해 envirenment 값으로 `ELASTICSEARCH_HOSTS=http://<ES 컨테이너명>:9200`을 준다.
  
  ```bash
  $ docker run --name kib01-test --net <네트워크명> -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://<ES 컨테이너명 >:9200" <이미지명>






# elasticsearch single node

- single-node로 띄우기

  - 아래와 같이 주면 `discovery.type=single-node`를 주지 않고도 single-node로 띄울 수 있다.

  ```yaml
  version: "3.2"
  
  services:
    es:
      image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
      environment:
        - node.name=test-node
        - cluster.name=test
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
        - cluster.initial_master_nodes=test-node
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports:
        - 9200:9200
        - 9300:9300
  ```

  - `discovery.type=single-node`를 명시적으로 주는 것 과의 차이
    - `discovery.type=single-node`를 명시적으로 주면 다른 node와 cluster를 구성할 수 없다.
    - 그러나 위와 같이 node를 생성하면, 추후에 다른 node와 cluster를 구성할 수 있다.
    - 즉, 둘의 차이는 오직 single-node로만 cluster를 구성할 것인지, 일단 single node로 구성하되, 추후에 다른 node와 clustering을 할 가능성을 남겨 두는지이다.
    - 얼핏 보면 추후에 다른 node와 clustering도 할 수 있는 위 방식이 더 효율적으로 보이지만, 사실 두 방식은 용도가 다르다.
    - `discovery.type=single-node`를 명시적으로 주는 방식은 주로 test용으로 사용된다.
    - 설정에 따라서 각기 독립적인 cluster를 구성해야 하는 두 node가 하나의 cluster로 묶이는 상황이 발생할 수 있다.
    - 그런데 이 때 한 노드에 `discovery.type=single-node` 설정을 줬다면, 두 노드는 절대 하나의 cluster에 묶일 수 없게 되어, 보다 간단한 설정으로 test가 가능해진다.



## Docker-compose로 설치하기

- docker-compose.yml 파일에 아래와 같이 작성

  - `environment`에는 elasticsearch.yml에 있는 모든 설정을 적용 가능하다.
  - 4 대의 노드와 1 대의 kibana를 설치
  
  ```yaml
  version: '3.2'
  
  services:
    node1:
      build: .
      container_name: node1
      environment:
        - node.name=node1
        - node.master=true
        - node.data=false
        - node.ingest=false
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node2,node3,node4
        - cluster.initial_master_nodes=node1
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - data01:/usr/share/elasticsearch/data
      ports: 
        - 9200:9200
      restart: always
      networks:
        - elastic
  
    node2:
      build: .
      container_name: node2
      environment:
        - node.name=node2
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node1,node3,node4
        - cluster.initial_master_nodes=node1
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - data02:/usr/share/elasticsearch/data
      restart: always
      networks:
        - elastic
  
    node3:
      build: .
      container_name: node3
      environment:
        - node.name=node3
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node1,node2,node4
        - cluster.initial_master_nodes=node1
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - data03:/usr/share/elasticsearch/data
      restart: always
      networks:
        - elastic
  
    node4:
      build: .
      container_name: node4
      environment:
        - node.name=node4
        - cluster.name=es-docker-cluster
        - discovery.seed_hosts=node1,node2,node3
        - cluster.initial_master_nodes=node1
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - data04:/usr/share/elasticsearch/data
      restart: always
      networks:
        - elastic
  
    kibana:
      image: docker.elastic.co/kibana/kibana:7.5.2
      container_name: theo_kibana
      ports:
        - "5603:5601"
      environment:
        ELASTICSEARCH_URL: http://<ES 호스트>:<ES 포트>
        ELASTICSEARCH_HOSTS: http://<ES 호스트>:<ES 포트>
      networks:
        - elastic
      depends_on:
        - node1
  
  volumes:
    data01:
      driver: local
    data02:
      driver: local
    data03:
      driver: local
    data04:
      driver: local
  
  networks:
    elastic:
      driver: bridge
  ```




- single node로 구성하는 방법

  - single node일 때 추가해야 할 옵션
    - `discovery.type=single-node`
  - single node일 때 제거해야 할 옵션
    - `cluster.initial_master_nodes`
    - `discovery.seed_hosts`
    - `network.publish_host`

  ```yaml
  version: '3.2'
  
  services:
    single-node:
      build: .
      container_name: single-node
      environment:
        - node.name=single-node
        - cluster.name=single-node
        - discovery.type=single-node
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports: 
        - 9204:9200
      restart: always
      networks:
        - elastic
  
    kibana:
      image: kibana:7.14.0
      container_name: single-node-kibana
      ports:
        - "5604:5601"
      environment:
        ELASTICSEARCH_URL: http://192.168.0.237:9204
        ELASTICSEARCH_HOSTS: http://192.168.0.237:9204
      networks:
        - elastic
      depends_on:
        - single-node
  
  networks:
    elastic:
      driver: bridge
  ```
  





## 각기 다른 서버에 설치된 node들로 클러스터 구성하기

- 가장 중요한 설정은 `network.publish_host`이다.
  - 따로 설정해주지 않을 경우 `network.host`의 기본 값은 `_local_`으로 설정된다.
    - `_local_`일 경우 루프백(127.0.0.1)으로 설정된다.
  - `network.host`는 내부 및 클라이언트의 요청 처리에 사용할 `network.bind_host`와 `network.pulbish_host`를 동시에 설정한다.
  - 따라서 다른 node와 통신할 때 사용하는  `network.pulbish_host` 값은 docker container의 IP(정확히는 IP의 host)값이 설정된다.
  - 그런데 docker container의 IP는 같은 docker network에 속한 것이 아니면 접근이 불가능하다.
  - 한 서버에서, 다른 서버에 있는 docker network에 접근하는 것은 불가능하므로, 다른 서버에 있는 node가 접근할 수 있도록 docker network의 host가 아닌, 서버의 host를 설정하고 port를 열어줘야한다.



- 클러스터 구성하기

  - `network.host`가 아닌 `network.publish_host`로 설정해줘야 한다.
    - docker container 내부에서는 docker network의 ip를 host로 사용하므로, `network.bind_host` 값에 서버의 host는 할당할 수 없다.
    - 따라서 `network.publish_host`만 따로 설정해줘야한다.

  - 마스터 노드 생성하기
  
  ```yaml
  version: '3.2'
  
  services:
    master-node:
      build: .
      container_name: master-node
      environment:
        - node.name=master-node
        # cluster name을 설정한다.
        - cluster.name=my-cluster
        - bootstrap.memory_lock=true
        # cluster가 구성될 때 master node가 될 node의 이름을 적어준다.
        - cluster.initial_master_nodes=master-node
        # 현재 서버의 host를 입력한다.
        - network.publish_host=<현재 서버의 host>
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      # 다른 노드와 통신을 위한 port를 열어준다.
      # 내부 port인 9300은 elasticsearch.yml의 transport.port 값으로, 다른 노드와 통신을 위한 tcp port이다. 
      ports:
        - 9300:9300
  ```

  - 다른 서버의 노드 생성하기
  
  ```yaml
  version: '3.2'
  
  services:
    other-node:
      build: .
      container_name: other-node
      environment:
        - node.name=other-node
        # 위에서 설정한 cluster명과 동일하게 설정한다.
        - cluster.name=my-cluster
        # 합류할 cluster의 내의 node ip를 적어준다.
        - discovery.seed_hosts=<합류할 node의 host>:9300
        - bootstrap.memory_lock=true
        # 역시 마찬가지로 다른 서버의 node와 통신하기 위한 host를 입력한다.
        - network.publish_host=<현재 서버의 host>
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      # 다른 노드와 통신을 위한 port를 열어준다.
      ports:
        - 9300:9300
      restart: always
  ```




- 주의사항

  > 아래 내용은 docker로 띄울 때 국한된 것이다.

  - 만일 기본 포트인 9300이 아닌 다른 포트를 사용할 경우 `transport.port` 값을 반드시 설정해줘야한다.
    - `transport.port` 값은 `transport.publish_port`와 `transport.bind_port`에 동시에 적용된다.
    -  `transport.publish_port`와 `transport.bind_port`를 개별적으로 적용하는 것도 가능하다.
    - 외부 port(`:` 왼쪽의 port)를 9300이 아닌 port로 했을 경우, `transport.publish_port`를, 내부 port(`:` 오른쪽의 port)를 변경했을 경우 `transport.bind_port`를 수정한다.
  
  - Docker로 생성한 두 개의 노드가 통신하는 과정은 다음과 같다.
    - `discovery.seed_hosts`에 설정된 ip(아래의 경우 `<master node의 ip>:9301`)로 handshake 요청을 보낸다.
    - `handshake`이 완료 되면 `network.publish_host`에 설정된 host + `transport.port`에 설정된 port를 응답으로 보낸다.
    - 응답으로 받은 ip로 클러스터 구성을 위한 요청을 보낸다.
    - 따라서 만일 `transport.port` 값을 설정해주지 않아 기본값인 9300으로 설정되었다면 `discovery.seed_hosts`에 다른 port를 입력했더라도 handshake 이후의 통신이 불가능해진다.
  
  - 노드 A
    - 아래와 같이 기본 port가 아닌 port를 사용한다면 `transport.port`를 반드시 설정해줘야한다.
  
  ```yaml
  version: '3.2'
  
  services:
    node_A:
      image: elasticsearch:8.1.3
      container_name: node_A
      environment:
        - node.name=node_A
        - cluster.name=remote-cluster
        - bootstrap.memory_lock=true
        - cluster.initial_master_nodes=node_A
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        # node A가 handshake 이후에 응답으로 보내는 ip는 아래 두 개의 값이 조합되어 생성된다.
        - network.publish_host=<현재 node의 host>
        - transport.port=9301
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      ports:
        - 9301:9301
      networks:
        - elasticsearch_elastic
  ```
  
  - 노드 B
  
  ```yaml
  version: '3.2'
  
  services:
    node231:
      image: theo_elasticsearch:8.1.3
      container_name: node231
      environment:
        - node.name=node231
        - cluster.name=remote-cluster
        # handshake은 아래에서 설정한 ip로 이루어지고, handshake이 완료되면 node A는 응답으로 ip를 보낸다.
        - discovery.seed_hosts=<master node의 ip>:9301
        - bootstrap.memory_lock=true
        - network.publish_host=<현재 node의 ip>
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports:
        - 9300:9300
      restart: always
  ```






# Security 활성화 한 상태로 생성하기

- docker-compose로 띄우기

  - `setup` 컨테이너를 생성하여 CA와 certs를 먼저 생성한다.
    - 생성한 CA와 certs를 volume을 사용하여 다른 컨테이너들에 복사한다.
    - setup 컨테이너는 setup이 끝나면 종료된다.
  - 환경 변수 파일 작성하기
    - `.env`파일을 작성한다.
    - 파일명은 정확히 `.env`로 작성하고, `docker-compose.yml`파일과 같은 디렉터리에 위치해야한다.

  ```env
  # Password for the 'elastic' user (at least 6 characters)
  ELASTIC_PASSWORD=qweasd
  
  # Password for the 'kibana_system' user (at least 6 characters)
  KIBANA_PASSWORD=qweasd
  
  # Version of Elastic products
  STACK_VERSION=8.1.3
  
  # Set the cluster name
  CLUSTER_NAME=docker-cluster
  
  # Set to 'basic' or 'trial' to automatically start the 30-day trial
  LICENSE=basic
  #LICENSE=trial
  
  # Port to expose Elasticsearch HTTP API to the host
  ES_PORT=9215
  #ES_PORT=127.0.0.1:9200
  
  # Port to expose Kibana to the host
  KIBANA_PORT=5615
  #KIBANA_PORT=80
  
  # Increase or decrease based on the available host memory (in bytes)
  MEM_LIMIT=1073741824
  
  # Project namespace (defaults to the current folder name if not set)
  #COMPOSE_PROJECT_NAME=myproject
  ```

  - docker-compose 파일 작성하기

  ```yaml
  version: "2.2"
  
  services:
    setup:
      image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs
      user: "0"
      command: >
        bash -c '
          if [ x${ELASTIC_PASSWORD} == x ]; then
            echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
            exit 1;
          elif [ x${KIBANA_PASSWORD} == x ]; then
            echo "Set the KIBANA_PASSWORD environment variable in the .env file";
            exit 1;
          fi;
          if [ ! -f config/certs/ca.zip ]; then
            echo "Creating CA";
            bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
            unzip config/certs/ca.zip -d config/certs;
          fi;
          
          # instances.yml에 각 node의 dns와 ip정보를 입력한다.
          # instances.yml을 바탕으로 certs를 생성한다.
          if [ ! -f config/certs/certs.zip ]; then
            echo "Creating certs";
            echo -ne \
            "instances:\n"\
            "  - name: es01\n"\
            "    dns:\n"\
            "      - es01\n"\
            "      - localhost\n"\
            "    ip:\n"\
            "      - 127.0.0.1\n"\
            "  - name: es02\n"\
            "    dns:\n"\
            "      - es02\n"\
            "      - localhost\n"\
            "    ip:\n"\
            "      - 127.0.0.1\n"\
            "  - name: es03\n"\
            "    dns:\n"\
            "      - es03\n"\
            "      - localhost\n"\
            "    ip:\n"\
            "      - 127.0.0.1\n"\
            > config/certs/instances.yml;
            bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
            unzip config/certs/certs.zip -d config/certs;
          fi;
          echo "Setting file permissions"
          chown -R root:root config/certs;
          find . -type d -exec chmod 750 \{\} \;;
          find . -type f -exec chmod 640 \{\} \;;
          echo "Waiting for Elasticsearch availability";
          until curl -s --cacert config/certs/ca/ca.crt https://es01:9200 | grep -q "missing authentication credentials"; do sleep 30; done;
          echo "Setting kibana_system password";
          until curl -s -X POST --cacert config/certs/ca/ca.crt -u elastic:${ELASTIC_PASSWORD} -H "Content-Type: application/json" https://es01:9200/_security/user/kibana_system/_password -d "{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do sleep 10; done;
          echo "All done!";
        '
      healthcheck:
        test: ["CMD-SHELL", "[ -f config/certs/es01/es01.crt ]"]
        interval: 1s
        timeout: 5s
        retries: 120
  
    es01:
      depends_on:
        setup:
          condition: service_healthy
      image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs
      ports:
        - ${ES_PORT}:9200
      environment:
        - node.name=es01
        - cluster.name=${CLUSTER_NAME}
        - cluster.initial_master_nodes=es01,es02,es03
        - discovery.seed_hosts=es02,es03
        - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
        - bootstrap.memory_lock=true
        - xpack.security.enabled=true
        - xpack.security.http.ssl.enabled=true
        - xpack.security.http.ssl.key=certs/es01/es01.key
        - xpack.security.http.ssl.certificate=certs/es01/es01.crt
        - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.http.ssl.verification_mode=certificate
        - xpack.security.transport.ssl.enabled=true
        - xpack.security.transport.ssl.key=certs/es01/es01.key
        - xpack.security.transport.ssl.certificate=certs/es01/es01.crt
        - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.transport.ssl.verification_mode=certificate
        - xpack.license.self_generated.type=${LICENSE}
      mem_limit: ${MEM_LIMIT}
      ulimits:
        memlock:
          soft: -1
          hard: -1
      healthcheck:
        test:
          [
            "CMD-SHELL",
            "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
          ]
        interval: 10s
        timeout: 10s
        retries: 120
  
    es02:
      depends_on:
        - es01
      image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs
      environment:
        - node.name=es02
        - cluster.name=${CLUSTER_NAME}
        - cluster.initial_master_nodes=es01,es02,es03
        - discovery.seed_hosts=es01,es03
        - bootstrap.memory_lock=true
        - xpack.security.enabled=true
        - xpack.security.http.ssl.enabled=true
        - xpack.security.http.ssl.key=certs/es02/es02.key
        - xpack.security.http.ssl.certificate=certs/es02/es02.crt
        - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.http.ssl.verification_mode=certificate
        - xpack.security.transport.ssl.enabled=true
        - xpack.security.transport.ssl.key=certs/es02/es02.key
        - xpack.security.transport.ssl.certificate=certs/es02/es02.crt
        - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.transport.ssl.verification_mode=certificate
        - xpack.license.self_generated.type=${LICENSE}
      mem_limit: ${MEM_LIMIT}
      ulimits:
        memlock:
          soft: -1
          hard: -1
      healthcheck:
        test:
          [
            "CMD-SHELL",
            "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
          ]
        interval: 10s
        timeout: 10s
        retries: 120
  
    es03:
      depends_on:
        - es02
      image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs
      environment:
        - node.name=es03
        - cluster.name=${CLUSTER_NAME}
        - cluster.initial_master_nodes=es01,es02,es03
        - discovery.seed_hosts=es01,es02
        - bootstrap.memory_lock=true
        - xpack.security.enabled=true
        - xpack.security.http.ssl.enabled=true
        - xpack.security.http.ssl.key=certs/es03/es03.key
        - xpack.security.http.ssl.certificate=certs/es03/es03.crt
        - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.http.ssl.verification_mode=certificate
        - xpack.security.transport.ssl.enabled=true
        - xpack.security.transport.ssl.key=certs/es03/es03.key
        - xpack.security.transport.ssl.certificate=certs/es03/es03.crt
        - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
        - xpack.security.transport.ssl.verification_mode=certificate
        - xpack.license.self_generated.type=${LICENSE}
      mem_limit: ${MEM_LIMIT}
      ulimits:
        memlock:
          soft: -1
          hard: -1
      healthcheck:
        test:
          [
            "CMD-SHELL",
            "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
          ]
        interval: 10s
        timeout: 10s
        retries: 120
  
    kibana:
      depends_on:
        es01:
          condition: service_healthy
        es02:
          condition: service_healthy
        es03:
          condition: service_healthy
      image: kibana:${STACK_VERSION}
      volumes:
        - ./certs:/usr/share/kibana/config/certs
      ports:
        - ${KIBANA_PORT}:5601
      environment:
        - SERVERNAME=kibana
        - ELASTICSEARCH_HOSTS=https://es01:9200
        - ELASTICSEARCH_USERNAME=kibana_system
        - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
        - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=config/certs/ca/ca.crt
      mem_limit: ${MEM_LIMIT}
      healthcheck:
        test:
          [
            "CMD-SHELL",
            "curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'",
          ]
        interval: 10s
        timeout: 10s
        retries: 120
  ```



## 각기 다른 서버에 설치된 node들로 클러스터 구성하기

- CA와 certificates 생성하기

  - CA와 certificates 생성을 위해서 노드를 생성한다.
    - master node로 사용할 node에 해도 되고, 새로운 노드를 하나 더 생성한 후 CA와 certs를 생성한 뒤 삭제해도 된다.

  ```yaml
  version: '3.2'
  
  services:
    single-node:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.1.3
      container_name: master-node
      environment:
        - node.name=master-node
        - cluster.name=my-cluster
        - cluster.initial_master_nodes=master-node
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - ELASTIC_PASSWORD=qweasd
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      ports:
        - 9200:9200
        - 9300:9300
  ```

  - CA 생성
    - 컨테이너 내부에서 아래 명령어를 실행한다.
    - 실행하면 `ca.crt` 파일과 `ca.key` 파일이 생성되는데, 이는 certificate를 생성할 때 사용한다.

  ```bash
  $ bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
  $ unzip config/certs/ca.zip -d config/certs;
  ```

  - certificate를 silent mdoe로 생성하기 위해 yaml 파일을 작성한다.
    - slient mode로 생성하지 않을 경우 건너뛰어도 된다.

  ```bash
  $ echo -ne \
  "instances:\n"\
  "  - name: master-node\n"\
  "    dns:\n"\
  "      - localhost\n"\
  "    ip:\n"\
  "      - <master node를 띄울 host machine의 ip>\n"\
  "  - name: other-node\n"\
  "    dns:\n"\
  "      - localhost\n"\
  "    ip:\n"\
  "      - <다른 node를 띄울 host machine의 ip>\n"\
  > config/certs/instances.yml;
  ```

  - certificate 생성하기
    - 아래 명령어를 실행하면 `master-node.crt/key`, `other-node.crt/key` 파일이 생성된다.

  ```bash
  $ bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
  $ unzip config/certs/certs.zip -d config/certs
  ```



- 노드 생성하기

  - master node 띄우기
    - 위에서 생성한 CA와 certificates를 컨테이너 밖으로 가져온 후 해당 file들을 master node와 다른 노드에 복사한다.
    - `network.publish_host`를 설정하고 아래와 같이 node와 통신을 위한 port 값을 기본값인 9300이 아닌 다른 값으로 설정해줬으면 `transport.port`도 설정해준다.

  ```yaml
  version: '3.2'
  
  services:
    single-node:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.1.3
      container_name: master-node
      environment:
        - node.name=master-node
        - cluster.name=my-cluster
        - cluster.initial_master_nodes=master-node
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - network.publish_host=<host machine의 ip>
        - transport.port=9310
        - ELASTIC_PASSWORD=qweasd
        - xpack.security.enabled=true
        - xpack.security.http.ssl.enabled=true
        - xpack.security.http.ssl.key=certs-tmp/master-node.key
        - xpack.security.http.ssl.certificate=certs-tmp/master-node.crt
        - xpack.security.http.ssl.certificate_authorities=certs-tmp/ca.crt
        - xpack.security.http.ssl.verification_mode=certificate
        - xpack.security.transport.ssl.enabled=true
        - xpack.security.transport.ssl.key=certs-tmp/master-node.key
        - xpack.security.transport.ssl.certificate=certs-tmp/master-node.crt
        - xpack.security.transport.ssl.certificate_authorities=certs-tmp/ca.crt
        - xpack.security.transport.ssl.verification_mode=certificate
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs-tmp
      ports:
        - 9210:9200
        - 9310:9310
  ```

  - 다른 node 띄우기
    - 마찬가지로 위에서 생성한 CA와 certificates를 노드에 복사한다.
    - `discovery.seed_hosts`에 다른 node들의 url을 입력한다.

  ```yaml
  version: '3.2'
  
  services:
    single-node:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.1.3
      container_name: other-node
      environment:
        - node.name=other-node
        - cluster.name=my-cluster
        - discovery.seed_hosts=<master node를 띄운 host machine의 ip>:9310
        - bootstrap.memory_lock=true
        - network.publish_host=<host machine의 ip>
        - xpack.security.enabled=true
        - xpack.security.http.ssl.enabled=true
        - xpack.security.http.ssl.key=certs-tmp/other-node.key
        - xpack.security.http.ssl.certificate=certs-tmp/other-node.crt
        - xpack.security.http.ssl.certificate_authorities=certs-tmp/ca.crt
        - xpack.security.http.ssl.verification_mode=certificate
        - xpack.security.transport.ssl.enabled=true
        - xpack.security.transport.ssl.key=certs-tmp/other-node.key
        - xpack.security.transport.ssl.certificate=certs-tmp/other-node.crt
        - xpack.security.transport.ssl.certificate_authorities=certs-tmp/ca.crt
        - xpack.security.transport.ssl.verification_mode=certificate
      volumes:
        - ./certs:/usr/share/elasticsearch/config/certs-tmp
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      ports:
        - 9210:9200
        - 9300:9300
  ```



- 연결 테스트

  - 제대로 연결이 되었는지 테스트한다.

  ```bash
  $ curl https://<master-node의 ip>:9210/_cat/nodes --cacert <path>/master-node.crt -u elastic
  ```



- kibana 연결하기

  - `kibana_system` user의 password를 설정한다.
    - `kibana_system`은 kibana가 elasticsearch와 통신하기 위해 사용하는 user이다.

  ```bash
  # 방법1
  $ curl -s -X POST --cacert <ca.crt 파일의 경로> -u elastic:<elastic user의 password> -H "Content-Type: application/json" https://<es url>/_security/user/kibana_system/_password -d "{\"password\":\"<설정할 password>\"}"
  
  # 방법2
  $ bin/elasticsearch-reset-password -u kibana_system
  ```

  - kibana container 생성

  ```yaml
  kibana:
      image: docker.elastic.co/kibana/kibana:8.1.3
      container_name: es8-kibana
      environment:
        - ELASTICSEARCH_HOSTS=https://<elasticsearch host>:<port>
        - ELASTICSEARCH_USERNAME=kibana_system
        - ELASTICSEARCH_PASSWORD=<위에서 설정한 passowrd>
        - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=config/certs-tmp/ca.crt
      restart: always
      volumes:
        - ./certs:/usr/share/kibana/config/certs-tmp
      ports:
        - "5602:5601"
  ```





# Error

- `vm.max_map_count is too low` error

  - elasticsearch 실행 시 아래와 같은 error가 발생할 때가 있다.

  ```
  ERROR: [1] bootstrap checks failed 
  [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
  ```

  - 원인

    - elasticsearch는 index들을 저장하기 위해 mmapfs 디렉터리를 사용한다.
    - mmapfs을 사용하여 index를 저장할 때, mmap을 이용한 많은 수의 메모리 매핑이 발생한다.
    - 운영체제에서 mmap 값은 65530으로 제한되어 있다.

    - elasticsearch는 bootstrap 과정에서 mmap 수가 262,144 이하면 실행되지 않도록 설정 되어 있다.

  - `vm.max_map_count` 값을 수정하는 방법
    - 영구적으로 수정하는 방법이 있고, 일시적으로 수정하는 방법이 있다.

  ```bash
  # 일시적 변경(재부팅시 초기화)
  $ sysctl -w vm.max_map_count=262144
  
  # 영구적 수정
  $ vi /etc/sysctl.conf
  # 아래 내용을 추가 혹은 수정한다.
  vm.max_map_count=262144
  ```

  - 변경 확인

  ```bash
  $ sysctl vm.max_map_count
  ```

