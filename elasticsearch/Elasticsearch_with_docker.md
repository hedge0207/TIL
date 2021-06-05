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

  - Kibana 실행하기
    - ES와 연결하기위해 envirenment 값으로 `ELASTICSEARCH_HOSTS=http://<ES 컨테이너명>:9200`을 준다.

  ```bash
  $ docker run --name kib01-test --net <네트워크명> -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://<ES 컨테이너명 >:9200" <이미지명>
  ```

  