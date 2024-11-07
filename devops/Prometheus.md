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



- JMX exporter 사용하여 Java application metric 수집하기

  > https://meetup.nhncloud.com/posts/237

  - [`jmx_exporter` repository](https://github.com/prometheus/jmx_exporter/releases)에서 JMX exporter를 다운 받는다.

    - Java agent와 HTTP server 두 가지 종류가 있는데, Java agent를 사용하는 것이 권장된다.

  - Java agent를 위한 설정 파일을 작성한다.

    > 전체 설정은 [링크](https://github.com/prometheus/jmx_exporter/tree/release-1.0.1/docs) 참조

    - [`jmx_exporter` repository](https://github.com/prometheus/jmx_exporter/tree/main/example_configs)에서 예시를 확인할 수 있다.
    - 가장 기본적인 형태는 아래와 같다.

  ```yaml
  rules:
  - pattern: ".*"
  ```

  - Java agent를 실행한다.
    - `-jar` 옵션에 metric을 수집할 jar file의 경로를 입력한다.

  ```bash
  $ java -javaagent:./jmx_prometheus_javaagent-1.0.1.jar=<port>:<path/to/config/file> -jar <path/to/jar/file>
  ```

  - HTTP server 실행을 위한 설정 파일 작성하기
    - Java agent와 달리 remote server에서 HTTP 요청을 통해 metric을 받아오기에 `hostPort` 또는 `jmxUrl` 둘 중 하나를 반드시 설정해야한다.
    - 가장 기본적인 형태는 아래와 같다.

  ```yaml
  hostPort: localhost:9999
  rules:
    - pattern: ".*"
  ```

  - HTTP server 실행하기

  ```bash
  $ java -jar jmx_prometheus_httpserver-1.0.1.jar <port> <path/to/config/file>
  ```

  - prometheus.yml 파일을 아래와 같이 작성한 후, Prometheus를 실행한다.
    - `<port>`에는 JMX exporter 실행시에 지정한 port를 입력한다.

  ```yaml
  global:
    scrape_interval: "5s"
    evaluation_interval: "5s"
  scrape_configs:
  - job_name: "jmx_exporter"
    static_configs:
    - targets:
      - "<jmx_exporter_host>:<jmx_exporter_port>"
  ```









