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



- elasticsearch container network

  - elasticsearch 공식 이미지로 컨테이너를 생성하면 elasticsearch.yml의 network는 아래와 같이 설정된다.
    - 0.0.0.0으로 설정하면, 클라이언트의 요청, 클러스터 내부의 다른 노드와의 통신에는 elasticsearch docker container에 할당된 IP를 사용하고, 내부에서는 localhost(127.0.0.1)로 통신이 가능해진다.

  ```yaml
  network.host: 0.0.0.0
  ```
  
  - 만일 한 서버에 여러 대의 node로 cluster를 구성하고자 하면 반드시 같은 network로 묶어줘야한다.
    - 위에서 말한 것 처럼 클러스터 내부의 다른 노드와의 통신에는 elasticsearch docker container에 할당된 IP를 사용하는데, 같은 네트워크에 속하지 않을 경우 해당 IP에 접근이 불가능하기 때문이다.



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
  



- 각기 다른 서버에 설치된 node들로 클러스터 구성하기(with docker)

  - 가장 중요한 설정은 `network.publish_host`이다.
    - 만일 이 값을 따로 설정해주지 않을 경우 `network.host`의 기본 값은 0.0.0.0으로 설정된다.
    - `network.host`는 내부 및 클라이언트의 요청 처리에 사용할 `network.bind_host`와 `network.pulbish_host`를 동시에 설정한다.
    - 따라서 다른 node와 통신할 때 사용하는  `network.pulbish_host` 값은 docker container의 IP(정확히는 IP의 host)값이 설정된다.
    - 그런데 docker container의 IP는 같은 docker network에 속한 것이 아니면 접근이 불가능하다.
    - 한 서버에서, 다른 서버에 있는 docker network에 접근하는 것은 불가능하므로, 다른 서버에 있는 node가 접근할 수 있도록 docker network의 host가 아닌,서버의 host를 설정하고 port를 열어줘야한다.
  - master node 생성하기
    - `network.host`가 아닌 `network.publish_host`로 설정해줘야 한다.
    - 그러나 docker container 내부에서는 docker network의 ip를 host로 사용하므로, `network.bind_host` 값에 서버의 host는 할당할 수 없다.
    - 따라서 `network.publish_host`만 따로 설정해줘야한다.

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
        # 다른 node와 통신할 host를 입력한다.
        - network.publish_host=<서버의 host>
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
        - discovery.seed_hosts=192.168.0.242:9300
        - bootstrap.memory_lock=true
        # 역시 마찬가지로 다른 서버의 node와 통신하기 위한 host를 입력한다.
        - network.publish_host=192.168.0.231
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

  

