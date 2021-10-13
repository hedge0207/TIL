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



## Docker-compose로 설치하기

- docker-compose.yml 파일에 아래와 같이 작성

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
  node1:
      build: .
      container_name: node1
      environment:
        - node.name=node1
        - cluster.name=es-docker-cluster
        - discovery.type=single-node
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - data01:/usr/share/elasticsearch/data
      ports: 
        - 9201:9200
      restart: always
      networks:
        - elastic
  
    kibana:
      image: kibana:7.14.0
      container_name: theo_kibana
      ports:
        - "5603:5601"
      environment:
        ELASTICSEARCH_URL: http://192.168.0.237:9201
        ELASTICSEARCH_HOSTS: http://192.168.0.237:9201
      networks:
        - elastic
      depends_on:
        - node1
  ```

  

