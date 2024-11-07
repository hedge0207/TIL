- Grafana
  - 모니터링 기능을 제공하는 오픈 소스 플랫폼이다.
    - 시각화, 알림, query 등의 다양한 기능을 제공한다.
    - 주로 Prometheus와 같은 time series database나  Elasticsearch 등의 logging 기능이 있는 tool과 함께 사용한다.
  - [체험 페이지](https://play.grafana.org/)에서 미리 사용해 볼 수 있다.



- Docker로 설치하기

  > grafana/grafana-oss:11.2.0로 진행
  >
  > 초기 접속 정보는 admin/admin 이다.

  - Grafana Docker image를 받아온다.
    - `grafana/grafana-enterprise`와 `grafana/grafana-oss` 두 가지 버전이 있다.
    - Enterprise 버전이 OSS(Open Source Software) 버전의 기능을 모두 포함하여 더 많은 기능을 포함하고 있다.
    - 아래에서는 OSS 버전을 사용한다.

  ```bash
  # OSS 버전
  $ docker pull grafana/grafana-oss
  
  # Enterprise 버전
  $ docker pull grafana/grafana-enterprise
  ```

  - `docker run` 명령어로 실행하기

  ```bash
  $ docker run -p <port>:3000 --name <container_name> grafana/grafana-oss[:<tag>]
  ```

  - Grafana plugin을 설치해야 한다면 아래와 같이 `GF_INSTALL_PLUGINS` 환경 변수를 주면 된다.

  ```bash
  $ docker run -d -p 3000:3000 --name=grafana \
    -e "GF_INSTALL_PLUGINS=grafana-clock-panel, grafana-simple-json-datasource" \
    grafana/grafana-enterprise
  ```

  - docker-compose 파일 작성하기

  ```yaml
  services:
    grafana:
      image: grafana/grafana-oss:<tag>
      container_name: <container_name>
      ports:
       - <port>:3000
  ```

  - Grafana plugin을 설치해야 한다면 역시 마찬가지로 `GF_INSTALL_PLUGINS` 환경 변수를 설정하면 된다.

  ```yaml
  services:
    grafana:
      image: grafana/grafana-oss:<tag>
      container_name: <container_name>
      environment:
       - GF_INSTALL_PLUGINS=grafana-clock-panel
      ports:
       - <port>:3000
  ```



