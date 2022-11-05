# Elasitcsearch monitroing

- Elasticsearch는 자체적으로 monitoring 기능을 지원한다.
  - Kibana에서 monitoring을 사용하면 자동으로 monitoring 데이터가 쌓이는데 이는 ES 내부의 monitoring 기능을 사용하는 것이다.
  - 아래와 같은 것들을 모니터링 할 수 있다.
    - cluster
    - node
    - index
  - 기본적으로 `_cat` API로 요청을 보냈을 때 응답으로 오는 데이터들이 포함되어 있다.
    - 다만, 모두 포함 된 것은 아니다.
  - 한 클러스터 뿐 아니라 다른 클러스터에서 monitoring 데이터를 가져오는 것도 가능하다.



- monitoring data 저장하기

  - 아래와 같이 클러스터 설정만 변경해주면 된다.

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-settings.html
  >
  > https://www.elastic.co/guide/en/elasticsearch/reference/current/collecting-monitoring-data.html

  ```bash
  PUT _cluster/settings
  {
    "persistent": {
      "xpack.monitoring.collection.enabled": true
    }
  }
  ```



- 자체적으로 지원하는 모니터링 기능 외에도 metricbeat, filebeat 등을 사용 가능하다.
