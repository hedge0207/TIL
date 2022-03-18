# Loggin Configuration

> https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html
>
> https://www.elastic.co/guide/en/elasticsearch/reference/current/logging.html

- Elasticsearch의 log와 관련된 설정은 대부분 `config/log4j2.properties`파일에 설정해준다.

  - 단, 로그 파일을 저장할 위치는 예외적으로 `config/elasticsearch.yml`파일에서 한다.

  ```yaml
  # elasticsearch.yml
  # 아래와 같이 설정하거나
  path:
      logs: /var/log/elasticsearch
  
  # 아래와 같이 설정한다.
  path.logs: /var/log/elasticsearch
  ```



- `log4j2.properties`

  - 파일 이름이 `log4j2.properties`인 이유는 Elasticsearch가 로깅에 Apache Log4j2를 사용하기 때문이다.

    - 즉 `log4j2.properties`는 정확히 말해서 ES 자체설정이라기 보다 ES가 사용하는 Apache Log4j2와 관련된 설정이다.

  - ES는 4개의 프로퍼티를 expose한다.

    - `${sys:es.logs.base_path}`: log파일의 위치, `config/elasticsearch.yml`에 설정해준 `path.logs` 값으로 설정된다.
    - `${sys:es.logs.cluster_name}`: 클러스터명, 
    - `${sys:es.logs.node_name}`: 노드명
    - `${sys:file.separator}`: `/`

    - 예를 들어 `path.logs`를 /var/log/elasticsearch로 설정하고 클러스터명이  my_cluster면 `${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}.log`는 /var/log/elasticsearch/my_cluster.log가 된다.

  - 설정 예시

  ```properties
  # RollingFile 또는 Console 등을 선택 가능하다. RollingFile은 파일로 저장하는 것이고 Console은 stdout을 출력한다.
  appender.rolling.type = RollingFile 
  appender.rolling.name = rolling
  # 로그를 저장할 파일 이름을 지정한다.
  appender.rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.json 
  # 로그 파일의 레이아웃을 선택한다.
  appender.rolling.layout.type = ESJsonLayout 
  appender.rolling.layout.type_name = server 
  # 롤링된 로그 파일의 형식을 선택한다.
  appender.rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.json.gz
  appender.rolling.policies.type = Policies
  # 시간 기반의 롤링 방식을 사용.
  appender.rolling.policies.time.type = TimeBasedTriggeringPolicy 
  # 매일 로그를 롤링한다.
  appender.rolling.policies.time.interval = 1 
  appender.rolling.policies.time.modulate = true 
  # 용량 기반의 롤링 방식도 사용한다.
  appender.rolling.policies.size.type = SizeBasedTriggeringPolicy 
  # 로그 파일의 크기가 256MB가 넘으면 롤링한다.
  appender.rolling.policies.size.size = 256MB 
  appender.rolling.strategy.type = DefaultRolloverStrategy
  appender.rolling.strategy.fileIndex = nomax
  # 로그를 롤링할 때 delete action을 사용한다.
  appender.rolling.strategy.action.type = Delete 
  appender.rolling.strategy.action.basepath = ${sys:es.logs.base_path}
  # 로그 파일의 패턴이 일치할 때만 로그를 삭제한다.
  appender.rolling.strategy.action.condition.type = IfFileName 
  appender.rolling.strategy.action.condition.glob = ${sys:es.logs.cluster_name}-* 
  appender.rolling.strategy.action.condition.nested_condition.type = IfAccumulatedFileSize 
  appender.rolling.strategy.action.condition.nested_condition.exceeds = 2GB 



- Log rolling(Log rotation)
  - 로그파일을 갱신하는 작업을 말한다.
  - 로그 파일은 지속적인 관리가 필요하다.
    - 예를 들어 `app.log`라는 로그 파일에 로그를 계속 저장한다면, 언젠가는 로그 파일의 크기가 지나치게 커지게 될 것이다.
    - 따라서 일정 기간, 혹은 로그 파일의 크기가 일정 이상이 되면 로그 파일을 분리하는 작업을 해주는데 이를 Log rotation 혹은 Log rolling이라 한다.
    - `app.log`에 저장하다 다음 날이 되면 `app.log.yyyy-MM-dd`등으로 저장하는 것이 로그 롤링의 예시이다.



# Slow Log

- 개요
  - ES를 사용하다보면 모든 검색, 색인 로그가 아닌 일정 시간 이상 걸린 검색, 색인 로그만 보고 싶을 때가 있다.
    - Slow Log를 사용하면 검색 또는 색인 시에 속도에  따라 각기 다른 로그를 남길 수 있다.
    - 예를 들어 일정 시간 이상이 소요됐을 때만 로그를 남기거나, 일정 시간 이상이 소요됐으면 WARN으로 남기는 것도 가능하다.
  - 인덱스 단위로 설정해줘야 한다.
    - 기존에는 모든 클러스터에 일괄적용이 가능했으나 Elasticsearch 5 이상부터는 인덱스 단위로 설정해야 한다.



- 구성

  - 크게 search-query, search-fetch, indexing의 세 개로 나눌 수 있다.
  - search-query는 query 검색 시에 속도 별 로그를 남기는 것이다.
    - `index.search.slowlog.threshold.query.<level>: <시간>`
  - search-fetch는 fetch 검색 시에 속도 별 로그를 남기는 것이다.
    - `index.search.slowlog.threshold.fetch.<level>: <시간>`
  - indexing은 indexing시에 속도 별 로그를 남기는 것이다.
    - `index.indexing.slowlog.threshold.index.<level>: <시간>`

  - \<level>과 <시간>
    - level은 `info`, `warn`, `debug`, `trace`가 있다.
    - 시간은 s 혹은 ms로 시간을 표기한다. 
  - 예시
    - `index.indexing.slowlog.threshold.index.info: 1ms`
    - 색인에 1ms 이상이 걸리면 info로 로그를 남기겠다.



- 설정 방법

  - 인덱스 단위로 설정해준다.
    - 동적으로 적용되며, 클러스터를 재시작하거나 재인덱싱을 필요로하지 않는다.
    - 와일드 카드(`*`)를 사용해 이름이 유사한 인덱스에 동시 설정이 가능하다.
  - 예시

  ```bash
  PUT /test-index/_settings
  {
    "index.search.slowlog.threshold.query.warn": "2s",
    "index.search.slowlog.threshold.query.info": "1s",
    "index.search.slowlog.threshold.query.debug": "1s",
    "index.search.slowlog.threshold.query.trace": "10s",
    
    "index.search.slowlog.threshold.fetch.warn": "1s",
    "index.search.slowlog.threshold.fetch.info": "0ms",
    "index.search.slowlog.threshold.fetch.debug": "500ms",
    "index.search.slowlog.threshold.fetch.trace": "30ms",
    
    "index.indexing.slowlog.threshold.index.warn": "0s",
    "index.indexing.slowlog.threshold.index.info": "0ms",
    "index.indexing.slowlog.threshold.index.debug": "0s",
    "index.indexing.slowlog.threshold.index.trace": "0ms",
    "index.indexing.slowlog.source": "1000"
  }
  ```



- 테스트

  - 아래에서 search-fetch에 소요되는 시간이 0ms이상이면 info로 로그가 뜨도록 설정했으므로 어떤 fetch 검색을 해도 info로 로그가 뜨게 된다.
  - 로그의 형태는 운영체제에 따라 다른데 docker로 ES를 띄워서 사용할 경우 stdout으로 출력된다.

  ```bash
  # 인덱스 생성
  PUT test-index
  
  # 설정 변경
  {
    "index.search.slowlog.threshold.fetch.info": "0ms",
  }
  
  # 데이터 삽입
  PUT test-index/_doc/1
  {
    "name":"oeht",
    "age":27
  }
  
  
  GET test-index/_search
  {
    "query": {
      "match_all": {}
    }
  }
  
  
  $ docker logs <ES 컨테이너명>
  # log
  {"type": "index_search_slowlog", "timestamp": "2021-10-27T08:38:06,872Z", "level": "INFO", "component": "i.s.s.fetch", "cluster.name": "single-node", "node.name": "single-node", "message": "[test-index][0]", "took": "352.4micros", "took_millis": "0", "total_hits": "4 hits", "types": "[]", "stats": "[]", "search_type": "QUERY_THEN_FETCH", "total_shards": "1", "source": "{\"query\":{\"match_all\":{\"boost\":1.0}}}", "cluster.uuid": "KE5yvoK7QTi9kmc1XbOpiQ", "node.id": "TexkAspeRVGjARhS3TdXsQ"  }
  ```

  - Json형식으로 볼 경우
    - 시간과 level, index 이름, node 이름, 검색이 이루어진 shards, 쿼리식(`source`) 등을 볼 수 있다.

  ```json
  {
      "type": "index_search_slowlog",
      "timestamp": "2021-10-27T08:38:06,872Z",
      "level": "INFO",
      "component": "i.s.s.fetch",
      "cluster.name": "single-node",
      "node.name": "single-node",
      "message": "[test-index][0]",
      "took": "352.4micros",
      "took_millis": "0",
      "total_hits": "4 hits",
      "types": "[]",
      "stats": "[]",
      "search_type": "QUERY_THEN_FETCH",
      "total_shards": "1",
      "source": "{\"query\":{\"match_all\":{\"boost\":1.0}}}",
      "cluster.uuid": "KE5yvoK7QTi9kmc1XbOpiQ",
      "node.id": "TexkAspeRVGjARhS3TdXsQ"
  }
  ```



- File로 저장하기

  - ES 공식 이미지로 Docker Container를 생성했을 경우 slowlog를 파일로 저장하지 않고 stdout으로 출력한다.
    - slowlog뿐 아니라 gc를 제외한 대부분의 로그를 파일로 저장하지 않는다.
    - 로그의 type이 운영체제마다 다른데 Docker를 제외한 대부분의 경우에는 File로 저장한다.

  - 파일로 저장되도록 수정하기

  ```properties
  # 기존
  ######## Search slowlog JSON ####################
  appender.index_search_slowlog_rolling.type = Console	# 콘솔로 출력하게 설정되어 있다.
  appender.index_search_slowlog_rolling.name = index_search_slowlog_rolling
  appender.index_search_slowlog_rolling.layout.type = ESJsonLayout
  appender.index_search_slowlog_rolling.layout.type_name = index_search_slowlog
  appender.index_search_slowlog_rolling.layout.esmessagefields=message,took,took_millis,total_hits,types,stats,search_type,total_shards,source,id
  
  #################################################
  
  
  # 파일로 저장하도록 수정
  ######## Search slowlog JSON ####################
  appender.index_search_slowlog_rolling.type = RollingFile	# 파일로 저장하도록 수정한다.
  appender.index_search_slowlog_rolling.name = index_search_slowlog_rolling
  appender.index_search_slowlog_rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs\
    .cluster_name}_index_search_slowlog.json
  appender.index_search_slowlog_rolling.layout.type = ESJsonLayout
  appender.index_search_slowlog_rolling.layout.type_name = index_search_slowlog
  appender.index_search_slowlog_rolling.layout.esmessagefields=message,took,took_millis,total_hits,types,stats,search_type,total_shards,source,id
  
  appender.index_search_slowlog_rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs\
    .cluster_name}_index_search_slowlog-%i.json.gz
  appender.index_search_slowlog_rolling.policies.type = Policies
  appender.index_search_slowlog_rolling.policies.size.type = SizeBasedTriggeringPolicy
  appender.index_search_slowlog_rolling.policies.size.size = 1GB
  appender.index_search_slowlog_rolling.strategy.type = DefaultRolloverStrategy
  appender.index_search_slowlog_rolling.strategy.max = 4
  #################################################
  ```

  - `.log` 파일로 저장하기
    - 위 설정은 json파일로 저장하도록 설정한 것이고 `.log` 파일로 저장하는 것도 가능하다.
    - 둘 중 하나를 선택해야 하는 것은 아니고, 둘 다 사용이 가능하다.

  ```properties
  # json 파일로 저장
  ######## Search slowlog JSON ####################
  appender.index_search_slowlog_rolling.type = RollingFile
  appender.index_search_slowlog_rolling.name = index_search_slowlog_rolling
  appender.index_search_slowlog_rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs\
    .cluster_name}_index_search_slowlog.json
  appender.index_search_slowlog_rolling.layout.type = ESJsonLayout
  appender.index_search_slowlog_rolling.layout.type_name = index_search_slowlog
  appender.index_search_slowlog_rolling.layout.esmessagefields=message,took,took_millis,total_hits,types,stats,search_type,total_shards,source,id
  
  appender.index_search_slowlog_rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs\
    .cluster_name}_index_search_slowlog-%i.json.gz
  appender.index_search_slowlog_rolling.policies.type = Policies
  appender.index_search_slowlog_rolling.policies.size.type = SizeBasedTriggeringPolicy
  appender.index_search_slowlog_rolling.policies.size.size = 1GB
  appender.index_search_slowlog_rolling.strategy.type = DefaultRolloverStrategy
  appender.index_search_slowlog_rolling.strategy.max = 4
  #################################################
  # .log 파일에 저장
  ######## Search slowlog -  old style pattern ####
  appender.index_search_slowlog_rolling_old.type = RollingFile
  appender.index_search_slowlog_rolling_old.name = index_search_slowlog_rolling_old
  appender.index_search_slowlog_rolling_old.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}\
    _index_search_slowlog.log
  appender.index_search_slowlog_rolling_old.layout.type = PatternLayout
  appender.index_search_slowlog_rolling_old.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name]%marker %m%n
  
  appender.index_search_slowlog_rolling_old.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}\
    _index_search_slowlog-%i.log.gz
  appender.index_search_slowlog_rolling_old.policies.type = Policies
  appender.index_search_slowlog_rolling_old.policies.size.type = SizeBasedTriggeringPolicy
  appender.index_search_slowlog_rolling_old.policies.size.size = 1GB
  appender.index_search_slowlog_rolling_old.strategy.type = DefaultRolloverStrategy
  appender.index_search_slowlog_rolling_old.strategy.max = 4
  #################################################
  ```





# Metricbeat

- Metricbeat

  - Metric을 수집할 수 있도록 해주는 ELK Stack 중 하나이다.
  - module과 Ouput을 지정 가능하다.
    - module은 수집 할 metric의 종류, output에는 metric을 저장 할 곳을 지정하면 된다.
    - Elasticsearch Metric뿐 아니라 다양한 Metric을 수집할 수 있다.
  - 수집 할 수 있는 metric의 종류(module의 종류)

  > https://www.elastic.co/guide/en/beats/metricbeat/7.15/metricbeat-modules.html



- Metricbeat으로  Elasticsearch metric 수집하기(linux, docker 기준)

  - metricbeat 설치

  ```bash
  $ curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.14.0-linux-x86_64.tar.gz
  $ tar xzvf metricbeat-7.14.0-linux-x86_64.tar.gz
  ```

  - `metricbeat.yml` 파일 수정
    - 위에서 압축을 푼 폴더 내부에 있는 `metricbeat.yml` 파일을 아래와 같이 수정한다.

  ```yaml
  # (...)
  # ================================== Outputs ===================================
  
  # Configure what output to use when sending the data collected by the beat.
  
  # ---------------------------- Elasticsearch Output ----------------------------
  output.elasticsearch:
    # Array of hosts to connect to.
    hosts: ["192.168.0.242:9204"]
    # (...)
  setup.kibana:
    host: "192.168.0.242:5604"
  # (...)
  ```

  - elasticsearch module을 활성화한다.

  ```bash
  $ ./metricbeat modules enable elasticsearch
  ```

  - 활성화된 module list 보기
  
  ```bash
  $ ./metricbeat modules list
  ```
  
  - `modules.d` 폴더 내부의 `elasticsearch.yml` 파일을 아래와 같이 수정한다.
    - `modules.d` 폴더에는 각 모듈의 설정 파일이 저장되어 있다.
    - 활성화 되지 않은 모듈의 설정 파일은 suffix로 `.disable`가 붙어있다.
    - `metricsets`에 입력된 값들을 수집하겠다는 의미이며, 전부 수집하지 않아도 된다면, 필요한 것만 입력하면 된다.
  
  ```yaml
  - module: elasticsearch
    metricsets:
      - ccr
      - cluster_stats
      - enrich
      - node
      - node_stats
      - index
      - index_recovery
      - index_summary
      - shard
      - ml_job
      - pending_tasks
    period: 10s
    hosts: ["http://localhost:9200"]
    #username: "user"
    #password: "secret"
  ```
  
  - ES에서 수집 가능한 metric 목록
  
  > https://www.elastic.co/guide/en/beats/metricbeat/7.15/metricbeat-module-elasticsearch.html
  
  - setup하기
    - `metricbeat.yml`에서 `setup.kibana`에 설정해준대로 setup된다.
  
  
  ```bash
  $ ./metricbeat setup
  ```
  
  - 실행하기
    - `-e` 옵션을 주면 log를 터미널에 출력해준다.
    - 주지 않을 경우 `/usr/share/metricbeat/logs`에 log 파일이 생성된다.
  
  
  ```bash
  $ ./metricbeat -e
  ```
  
  - 여기까지 실행하면 Elasticsearch에 `metricbeat-<버전>-<날짜>-000001` 형식으로 인덱스가 생성 된 것을 확인 가능하다.



- docker container로 실행하기

  - 이미지를 받는다.

  > https://www.docker.elastic.co/r/beats

  - docker container 실행하기

  ```yaml
  version: '3.2'
  
  services:
    metricbeat:
      image: <위에서 받은 image>
      user: root
      environment:
        ELASTICSEARCH_HOSTS: http://<elasticsearch_host:port>
        KIBANA_HOST: http://<kibana_host:port>
      networks:
        - <elasticsearch_network>
  
  volumes:
    data01:
      driver: local
  ```



# ILM(Index Lifecycle Management)

- Index lif cycle
  - Hot
    - 인덱스에 지속적으로 쓰기 및 검색 요청이 들어오는 상태
  - Warm
    - 쓰기 요청은 더 이상 들어오지 않지만, 지속적으로 검색 요청이 들어오는 상태
  - Cold
    - 쓰기 요청이 더 이상 들어오지 않고 검색도 빈번히 일어나는 것도 아닌 상태.
    - 아직은 검색할 필요는 있지만, 빠른 속도로 검색 될 필요는 없는 데이터들이 저장되어 있다.
  - Forzen
    - 쓰기 요청이 더 이상 들어오지 않고 검색도 거의 들어오지 않는 상태.
    - 아직은 검색할 필요는 있지만, 매우 느린 속도로 검색 되도 상관 없는 데이터들이 저장되어 있다.
  - Delete
    - index가 더 이상 필요 없어 안전하게 삭제된 상태.





# Data streams

## 개요

- Data stream
  - 여러 인덱스를 하나로 묶어 하나의 인덱스처럼 사용할 수 있게 해주는 기능
  - logs, events, metrics 같이 지속적으로 생산되는 데이터를 관리하는 데 도움을 준다.
  - data stream은 data stream에 저장된 데이터에 거의 변경이 일어나지 않는다고 가정하고 만들어졌다.
    - 따라서 update, delete 요청을 보낼 수 없다.
    - `update by query`, `delete by query`로는 update, delete가 가능하다.



- ILM(Index Lifecycle Management)
  - 인덱스의 lifecycle을 관리할 수 있게 도와주는 기능
  - Data stream의 backing index들을 관리하는 데도 사용된다.



- backing index

  - data stream의 데이터를 저장하고 있는 인덱스들이다.
    - 자동으로 생성되며 hidden 인덱스이다.
    - 검색 및 색인 요청은 backing indices에 직접 하는 것이 아니라 data stream을 통해서 간접적으로 한다.

  - Read & write requests
    - Read requests의 경우에는 data stream 내의 모든 backing indices를 대상으로 보낸다.
    - Write requests의 경우에는 data stream 내의 가장 최신(가장 최근에 생성된) backing index(이를 write index라 부른다)를 대상으로 보낸다.
    - 가장 최근에 생성된 인덱스가 아닌 다른 backing index를 지정해서 write request를 보내도, doc이 추가되지 않는다.
  - convention
    - data stream의 이름, 생성된 날짜, 0으로 패딩 된 6자리 숫자가 인덱스명에 들어간다.

  ```bash
  .ds-<data stream 명>-<yyyy.MM.dd>-<6자리 숫자>
  ```



## 생성하기

- 순서
  - ILM을 생성한다.
  - component template을 생성한다(Optional).
    - index template을 보다 원활히 생성하기 위해 사용하는 것이므로 필수적인 단계는 아니다.
  - index template을 생성한다.
    - 데이터 스트림을 사용하기 위해서는 index template을 먼저 생성해야 한다.
    - backing indices는 index template에 정의한 mapping, setting에 따라 생성된다.
    - data stream에 색인되는 모든 문서는 `@timestamp` 필드가 있어야 한다.
    - `@timestamp` 필드는  `date`, 혹은 `date_nanos` 타입으로 정의되어야 한다.
    - data stream에 사용할 index template에 따로 `@timestamp` 필드를 정의하지 않을 경우 ES는 자동으로 `@timestamp` 필드를 생성하고 date type으로 mapping한다.
  - data stream을 생성한다.
  - data stream의 보안을 설정한다.



- ILM 생성하기

  - Kibana로 생성하기
    - `Stack Management` → `Index Lifecycle Policies`에서 `Create policy`를 통해 생성 가능하다.
  - api를 통해서도 생성이 가능하다.
    - `PUT _ilm/policy/<policy 명>`으로 생성이 가능하다.
    - `hot`만 required이며 나머지는 optional이다.

  ```json
  PUT _ilm/policy/my-lifecycle-policy
  {
    "policy": {
      "phases": {
        "hot": {
          "actions": {
            "rollover": {
              "max_primary_shard_size": "50gb"
            }
          }
        },
        "warm": {
          "min_age": "30d",
          "actions": {
            "shrink": {
              "number_of_shards": 1
            },
            "forcemerge": {
              "max_num_segments": 1
            }
          }
        },
        "cold": {
          "min_age": "60d",
          "actions": {
            "searchable_snapshot": {
              "snapshot_repository": "found-snapshots"
            }
          }
        },
        "frozen": {
          "min_age": "90d",
          "actions": {
            "searchable_snapshot": {
              "snapshot_repository": "found-snapshots"
            }
          }
        },
        "delete": {
          "min_age": "735d",
          "actions": {
            "delete": {}
          }
        }
      }
    }
  }
  ```



- component template 생성하기

  - index template을 구성하기 위해서 component template을 생성한다.
  - component template에도 date 혹은 date_nanos 필드로 매핑된 `@timestamp` 필드가 필요하다.
    - 만일 정의하지 않으면 ES가 자동으로 date 타입으로 `@timestamp` 필드를 생성한다.

  - Kibana로 생성하기
    - `Stack Management` → `Index Management` → `Component Template`에서 `Create component template`을 통해 생성 가능하다.

  - api로 생성하기
    - `PUT _component_template/<component template 명>`으로 생성한다.

  ```json
  // mappings를 정의하는 component template 생성
  PUT _component_template/my-mappings
  {
    "template": {
      "mappings": {
        "properties": {
          "@timestamp": {
            "type": "date",
            "format": "date_optional_time||epoch_millis"
          },
          "message": {
            "type": "wildcard"
          }
        }
      }
    },
    "_meta": {
      "description": "Mappings for @timestamp and message fields",
      "my-custom-meta-field": "More arbitrary metadata"
    }
  }
  
  // settings를 정의하는 component template 생성
  PUT _component_template/my-settings
  {
    "template": {
      "settings": {
        "index.lifecycle.name": "my-lifecycle-policy"
      }
    },
    "_meta": {
      "description": "Settings for ILM",
      "my-custom-meta-field": "More arbitrary metadata"
    }
  }
  ```



- index template 생성하기

  - Kibana로 생성하기
    - `Stack Management`  → `Index Management` → `Index Templates`에서 `Create template`을 통해 생성 가능하다.
  - api로 생성하기

  ```json
  PUT _index_template/my-index-template
  {
    // data stream 이름
    "index_patterns": ["my-data-stream*"],
    "data_stream": { },
    // component template에서 정의한 이름
    "composed_of": [ "my-mappings", "my-settings" ],
    "priority": 500,
    "_meta": {
      "description": "Template for my time series data",
      "my-custom-meta-field": "More arbitrary metadata"
    }
  }
  ```

  - component template을 작성하지 않았을 경우 아래와 같이 생성한다.

  ```json
  PUT /_index_template/template_1
  {
    // data stream 이름
    "index_patterns" : ["my-data-stream*"],
    "data_stream": {}
    "priority" : 1,
    "template": {
      "settings" : {
        "number_of_shards" : 2,
        "index.lifecycle.name": "my-lifecycle-policy"
      }
    }
  }
  ```



- data stream 생성하기

  - index template에서 정의한 `index_pattenrs`와 일치하는 index명으로 index 요청을 보내면 자동으로 data stream이 생성된다.

  ```json
  POST my-data-stream/_doc
  {
    "@timestamp": "2099-05-06T16:21:15.000Z",
    "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
  }
  ```

  - 수동으로 생성하고자 한다면 아래와 같이 하면 된다.
    - `PUT _data_stream/my-data-stream`
    - index template에서 정의한 `index_pattenrs`와 일치하는 datastream명으로 위 요청을 보낸다.



- Data stream 조회 삭제

  - 조회

  ```bash
  GET _data_stream/<data stream 이름>
  ```

  - 삭제

  ```bash
  DELETE _data_stream/<data stream 이름>
  ```






# Search template

- search template
  - 검색 양식을 미리 생성한 후 해당 검색 양식에 값을 넘겨서 검색식을 완성할 수 있게 해주는 기능.
  - 검색식 때문에 코드가 지저분해지는 등 검색식 관리가 힘들 때 활용할 수 있는 기능이다.
  - 또한 검색식을 ES 내부에 저장하기에 검색식이 외부에 노출되지 않는다는 장점이 있다.



- 생성하기

  - search template을 생성하고 수정하기 위해서는 `_script` API를 사용한다.
    - requests의 `source` 부분에 search API 사용되는 reqeust body를 넣는다.
    - Mustache 값으로 각 쿼리의 검색 값을 표시한다(즉 함수의 파라미터를 선언해주는 부분이라 보면 된다).
  - ES는 search template을  cluster state에 [mustache scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html)로 저장한다.

  - 예시
    - 아래 예시는 `my-search-template`라는 search template을 생성하는 예시이다.

  ```json
  PUT _scripts/my-search-template
  {
    "script": {
      "lang": "mustache",
      "source": {
        "query": {
          "match": {
            "message": "{{query_string}}"
          }
        },
        "from": "{{from}}",
        "size": "{{size}}"
      },
      "params": {
        "query_string": "My query string"
      }
    }
  }
  ```



- 유효성 검증하기

  - `_render` API를 통해 search template을 검색식으로 변환할 수 있다.
    - GET/POST 모두 사용 가능하며 template_id를 path parameter로 넘길 수도 있다(`POST _render/template/my-search-template`).
    - `params`에는 key-value 쌍의 값을 받는다.

  ```json
  POST _render/template
  {
    "id": "my-search-template",
    "params": {
      "query_string": "hello world",
      "from": 20,
      "size": 10
    }
  }
  ```

  - output

  ```json
  {
    "template_output": {
      "query": {
        "match": {
          "message": "hello world"
        }
      },
      "from": "20",
      "size": "10"
    }
  }
  ```

  - `source`는 템플릿 생성 전에 임시로 템플릿을 렌더링하면 어떤 모습이 될지를 확인하기 위해 사용한다. 
    - search API 사용되는 reqeust body를 넣는다.
    - `template_id`가 없을 경우 `source`는 required field가 된다.
    - 이미 템플릿이 있는 상태에서 `source` 파라미터를 주면 기존 템플릿은 무시되고 source에 정의 된 내용만 렌더링된다.

  ```json
  GET _render/template
  {
    "id": "my-search-template",
    "params": {
      "query_string": "hello world",
      "from": 20,
      "size": 10
    },
    "source": {
      "sort":{
        "@timestamp":"desc"
      }
    }
  }
  ```

  - ouput

  ```json
  {
    "template_output" : {
      "sort" : {
        "@timestamp" : "desc"
      }
    }
  }
  ```



- 기본값 설정하기

  - 아래와 같은 형식으로 기본 값을 설정할 수 있다.

  ```bash
  {{my-var}}{{^my-var}}default value{{/my-var}}
  ```

  - 예시

  ```json
  POST _render/template
  {
    "source": {
      "query": {
        "match": {
          "message": "{{query_string}}"
        }
      },
      "from": "{{from}}{{^from}}0{{/from}}",
      "size": "{{size}}{{^size}}10{{/size}}"
    },
    "params": {
      "query_string": "hello world"
    }
  }
  ```



- URL 인코딩하기

  - `{{@url}}`을 통해 URL이라는 것을 표시한다.

  ```json
  POST _render/template
  {
    "source": {
      "query": {
        "term": {
          "url.full": "{{#url}}{{host}}/{{page}}{{/url}}"
        }
      }
    },
    "params": {
      "host": "http://example.com",
      "page": "hello-world"
    }
  }
  ```



- 여러 개의 값을 하나의 문자열로 묶기

  - `{{@join}}`을 활용하여 list형의 값을 하나의 문자열로 이어서 받을 수 있다.
    - 기본적으로 `,`로 구분한다.

  ```json
  POST _render/template
  {
    "source": {
      "query": {
        "match": {
          "user.group.emails": "{{#join}}emails{{/join}}"
        }
      }
    },
    "params": {
      "emails": [ "user1@example.com", "user_one@example.com" ]
    }
  }
  ```

  - 구분자를 `,`가 아닌 다른 것으로 직접 지정하는 것도 가능하다.
    - `{{#join delimiter='||'}}`와 같이 구분자를 `||`로 지정이 가능하다.

  ```json
  POST _render/template
  {
    "source": {
      "query": {
        "range": {
          "user.effective.date": {
            "gte": "{{date.min}}",
            "lte": "{{date.max}}",
            "format": "{{#join delimiter='||'}}date.formats{{/join delimiter='||'}}"
  	      }
        }
      }
    },
    "params": {
      "date": {
        "min": "2098",
        "max": "06/05/2099",
        "formats": ["dd/MM/yyyy", "yyyy"]
      }
    }
  }
  ```

  - output

  ```json
  {
    "template_output": {
      "query": {
        "range": {
          "user.effective.date": {
            "gte": "2098",
            "lte": "06/05/2099",
            "format": "dd/MM/yyyy||yyyy"
          }
        }
      }
    }
  }
  ```



- Json으로 변환하기

  - json 표현식으로도 변환이 가능하다.

  ```json
  POST _render/template
  {
    "source": "{ \"query\": {{#toJson}}my_query{{/toJson}} }",
    "params": {
      "my_query": {
        "match_all": { }
      }
    }
  }
  ```

  - output

  ```json
  {
    "template_output" : {
      "query" : {
        "match_all" : { }
      }
    }
  }
  ```



- 검색 템플릿 조회하기

  - 개별 템플릿 조회하기
    - 아래와 같이 GET 메서드와  template_id를 활용하여 조회가 가능하다.

  ```bash
  GET _scripts/my-search-template
  ```

  - 모든 template 조회하기
    - cluster state에 저장되므로 아래와 같이 조회한다.

  ```bash
  GET _cluster/state/metadata?pretty&filter_path=metadata.stored_scripts
  ```



- 검색 템플릿 삭제하기

  - DELETE 메서드와 template_id를 활용하여 삭제한다.

  ```bash
  DELETE _scripts/my-search-template
  ```



- 검색하기

  - `_search/template` API를 활용하여 검색이 가능하다.
    - 아래와 같이 template id를 지정하고 mustache로 정의한 값들을 params에 넣어서 검색한다.
    - 응답값은 일반적인 검색과 같다.

  ```json
  GET my-index/_search/template
  {
    "id": "my-search-template",
    "params": {
      "query_string": "hello world",
      "from": 0,
      "size": 10
    }
  }
  ```

  - [다중 템플릿 검색](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-search-template.html)
    - `_msearch/template` API를 활용하여 검색한다.
    - 단일 검색을 두 번 수행하는 것 보다 오버헤드가 적고 속도가 빠를 수 있다.

  ```json
  GET my-index/_msearch/template
  { }
  { "id": "my-search-template", "params": { "query_string": "hello world", "from": 0, "size": 10 }}
  { }
  { "id": "my-other-search-template", "params": { "query_type": "match_all" }}
  ```



- 조건문 활용하기

  - 아래와 같은 형식으로 조건문을 사용 가능하다.

  ```bash
  {{#condition}}content{{/condition}}
  ```

  - 예시

  ```json
  POST _render/template
  {
    "source": "{ \"query\": { \"bool\": { \"filter\": [ {{#year_scope}} { \"range\": { \"@timestamp\": { \"gte\": \"now-1y/d\", \"lt\": \"now/d\" } } }, {{/year_scope}} { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
    "params": {
      "year_scope": true,
      "user_id": "kimchy"
    }
  }
  ```

  - `year_scope`값이 true면

  ```json
  {
    "template_output" : {
      "query" : {
        "bool" : {
          "filter" : [
            {
              "range" : {
                "@timestamp" : {
                  "gte" : "now-1y/d",
                  "lt" : "now/d"
                }
              }
            },
            {
              "term" : {
                "user.id" : "kimchy"
              }
            }
          ]
        }
      }
    }
  }
  ```

  - `year_scope`값이 false면

  ```json
  {
    "template_output" : {
      "query" : {
        "bool" : {
          "filter" : [
            {
              "term" : {
                "user.id" : "kimchy"
              }
            }
          ]
        }
      }
    }
  }
  ```

  - if - else도 활용이 가능하다.

  ```bash
  {{#condition}}if content{{/condition}}{{^condition}}else content{{/condition}}
  ```

  - 예시

  ```json
  POST _render/template
  {
    "source": "{ \"query\": { \"bool\": { \"filter\": [ { \"range\": { \"@timestamp\": { \"gte\": {{#year_scope}} \"now-1y/d\" {{/year_scope}} {{^year_scope}} \"now-1d/d\" {{/year_scope}} , \"lt\": \"now/d\" }}}, { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
    "params": {
      "year_scope": true,
      "user_id": "kimchy"
    }
  }
  ```

