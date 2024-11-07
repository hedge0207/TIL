- Prometheus
  - Metric 수집, monitoring, alert 기능 등을 제공하는 툴이다.
  - Grafana와의 차이
    - Grafana와 겹치는 기능이 많지만, 서로 강점을 보이는 기능이 있다.
    - Grafana의 경우 metric 수집 기능은 제공하지 않는 데 반해 Prometheus는 metric 수집 기능을 제공한다.
    - 반면에 data visualization 기능은 Grafana가 더 풍푸하게 제공한다.
    - 일반적으로 Prometheus는 metric 수집에 사용하며, Prometheus를 통해 수집된 metric의 monitoring 및 alerting에는 Grafana를 사용한다.



- Docker로 설치하기

  > prom/prometheus:v2.54.1 로 실행한다.

  - Docker image를 다운 받는다.

  ```bash
  $ docker pull prom/prometheus
  ```

  - `docker run` 명령어로 실행하기

  ```bash
  $ docker run -p <port>:9090 prom/prometheus[:<tag>] --name <container_name>
  ```

  - 설정 파일과 Prometheus data를 bind-mount하기

  ```bash
  $ docker run \
      -p 9090:9090 \
      -v </path/to/prometheus.yml>:/etc/prometheus/prometheus.yml \
      -v </path/to/bind-mount>:/prometheus \
      prom/prometheus[:<tag>]
      --name <container_name>
  ```

  - docker compose file 작성하기

  ```yaml
  services:
    prometheus:
      image: prom/prometheus[:<tag>]
      container_name: <container_name>
      ports:
       - <port>:9090
  ```

  

  