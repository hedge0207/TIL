```
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

```