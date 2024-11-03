# Node의 역할

- Node의 역할 13가지

  - master-eligible(m)
    - 클러스터의 상태를 변경
    - 클러스터의 상태를 모든 노드에 게시
    - 전역 클러스터 상태를 유지
    - 샤드에 대한 할당과 클러스터 상태 변화 게시
  - Data 관련 role 6가지
    - data(d)
    - data_content(s)
    - data_hot(h)
    - data_warm(w)
    - data_cold(c)
    - data_frozen(f)
  - ingest(i)
    - ingest pipeline 기능을 사용하기 위해서는 클러스터 내에 적어도 하나 이상의 ingest 역할을 하는 노드가 필요하다.
    - master, data 역할을 같이 수행하지 않는 것이 좋다.
    - 색인 전에 데이터를 전처리하기 위해 사용한다.
  - machine_learning(l)
    - xpack에서 제공하는 머신러닝 기능을 사용하기 위한 노드
    - basic에서는 사용이 불가능하다.
  - remote_cluster_client(r)
    - 다른 클러스터에 연결되어 해당 클러스트의 원격 노드 역할을 수행하는 노드
  - transform(t)
    - 색인된 데이터로부터 데이터의 pivot이나 latest 정보를 별도 데이터로 변환해서 transform index로 저장한다.
  - voting_only(v)
    - 마스터 노드를 선출하는 역할만 하는 노드
    - 주의할 점은 role 설정시 아래와 같이 master를 함께 줘야 한다는 것이다.
    - 마스터 노드 역할을 동시에 줘야하지만, 마스터 노드로 선출되지 않는다.
    - 마스터 노드 선출시 tiebreaker 역할을 한다.

  ```yaml
  node.roles: [master, voting_only]
  ```

  - coordinating node(-)
    - 설정해준 역할과 무관하게 모든 노드가 수행하는 역할이다.
    - `node.rules`에 빈 리스트를 주면 순수 coordinating node가 된다.
    - 주로 search reqeust를 받거나 bulk indexing request를 받는 역할을 한다.



- Single node
  - 단일 node라는 의미도 있지만 node의 역할 측면에서 보면 node의 모든 역할을 수행할 수 있는 node를 의미한다.
    - Node에 아무 역할을 지정해주지 않으면 기본적으로 모든 역할을 하는 single node로 동작한다.
  - Cluster의 규모가 작을 때는 node 별로 역할을 나누기 보다 single node로 동작하게 하는 것이 유리할 수 있다.
    - 장애가 발생했을 때 다른 node가 대신할 수 있어야 하기 때문이다.
    - 일반적으로 3대 이하의 소규모 cluster를 구축한다면 모든 Elasticsearch node를 single node로 동작시키는 것이 좋다.



- Coordinator node

  - 기본적으로 모든 node는 coordinator의 역할을 수행한다.
  - 그럼에도 coordinator의 역할만 하는 node를 두는 것이 권장된다.
    - Coordinator node가 검색 요청을 받으면 cluster에 존재하는 모든 data node에게 검색을 요청한다.
    - 각 data node들이 검색을 수행하고 그 결과를 다시 coordinator node에게 전달한다.
    - Coordinator node는 모든 data node들로부터 검색 결과를 받을 때 까지 대기하다가 모든 data node로부터 검색 결과가 반환 되면 이들을 하나로 병합해서 사용자에게 전달한다.
    - 각 data node에게 전달 받은 data를 하나로 합치는 작업은 memory를 많이 필요로한다.
    - 따라서 coordinator node가 master나 data node 등 다른 역할도 함께 수행할 경우 문제가 발생할 가능성이 높아진다.
    - 또한 aggregation과 같이 매우 많은 resource를 필요로 하는 기능도 있다.
    - 따라서 자칫 무리한 작업을 실행하여 resource의 한계에 도달할 경우 시스템 전체에 장애가 발생할 수도 있다.
    - 그러므로 coordinator node를 별도로 구축하면 해당 node는 data node의 역할은 하지 않을 수 있으므로 부하가 훨씬 감소하게 된다.
  - Master node도 마찬가지 이유로 따로 분리할 수 있다면 data node와 분리하는 것이 좋다.
    - Master node는 data node나 coordinator node와 달리 많은 resource를 필요로 하지 않으므로 상대적으로 떨어지는 사양을 가진 장비에 master node를 실행하고, 보다 높은 사양을 가진 장비에 data node를 실행하는 식으로 운영이 가능하다.



- Data role
  - Data노드는 기본적으로 아래와 같은 역할을 수행한다.
    - 문서의 색인 및 저장
    - 문서의 검색 및 분석
    - 코디네이팅
  - data_content
    - 일반적으로, 제품의 카탈로그나 기사의 archive 같은 상대적으로 영속적으로 저장해야 하고 다른 tier로 옮길 필요가 없는 data를을 저장한다.
    - 시간이 오래 지나더라도 빠른 속도로 검색이 가능해야하는 data를 저장하는 용도로 사용한다.
    - 일반적으로 query 성능을 위해 최적화되므로, 복잡한 검색이나 aggregation도 빠르게 수행할 수 있다.
    - Indexing도 수행하긴 하지만, 일반적으로 log나 metric 같은 time series data를 빠르게 수집하지는 못한다.
    - Data stream의 일부가 아닌 index나 system index들은 자동으로 content tier를 할당 받는다.
  - data_hot
    - 검색이 빈번하게 이루어지고, 최신 데이터를 저장해야하는 노드에 지정하는 tier다.
    - log, metrics 등의 time series 데이터들에 주로 사용한다.
    - Hot tier에 있는 node들은 색인과 검색이 모두 빨라야하므로 보다 많은 hardware resource와 SSD 등의 보다 빠른 저장소를 필요로한다.
    - Data stream을 통해 생성된 index들은 자동으로 hot tier로 할당된다.
  - data_warm
    - time series 데이터를 유지하고 있는 노드로 업데이트와 검색이 빈번하지 않게 이루어지는 경우에 사용한다.
    - 일반적으로 지난 1주 정도의 data를 저장하고 검색하는 용도로 사용한다.
  - data_cold
    - 업데이트와 검색이 매우 드물게 이루어지는 경우에 사용한다.
    - 이 tier에 속한 data들은 빠른 검색 보다는 저장에 보다 적은 비용을 사용하도록 최적화된다.
    - Cold tier의 이점을 최대한 누리기 위해서는 searchable snapshot의 fully mounted index를 사용해야한다.
    - 이를 사용하지 않아도 hardware resource를 덜 사용하긴 하지만, warm tier에 비해서 disk space가 줄지는 않는다.
  - data_frozen
    - 업데이트와 검색이 아예 이루어지지 않거나 거의 이루어지는 경우 사용한다.
    - Cold tier와 마찬가지로 frozen tier의 이점을 최대로 누리기 위해선 searchable snapshot의 partially mounted index를 사용해야한다.
  - Data tier 개념을 노드에 적용한 것은 각 tier별로 hardware 스펙을 동일하게 하게 맞추도록 하려는 의도이다.
    - 같은 tier의 data node 끼리는 hardware 스펙을 동일하게 맞춰주는 것이 좋다. 
    - 각기 다를 경우 병목 현상으로 색인, 검색 시에 성능에 문제가 생길 수 있다.
  - Index에 data tier를 설정하면, 해당 tier에 맞는 노드로 인덱스의 shard가 할당된다.



- 기본 할당 정책

  - `index.routing.allocation.include._tier_preference`
    - elasticsearch.yml 파일의 위 부분에 설정된대로 index를 tier에 할당한다.
    - 기본값은 content이기에, `data_content` role을 맡은 shard가 있을 경우 shard를 이 node에 먼저 할당한다.
    - 여러 개의 tier를 설정할 수 없으며, 앞에서부터 해당 tier의 node가 있는지 확인하고 있을 경우 할당한다.
    - 없을 경우 다음으로 설정된 tier의 node에 할당한다.
    - 예를 들어 아래와 같이 설정한 경우 `data_warm`으로 설정된 node가 있는지를 먼저 보고 없으면, `data_cold`로 설정된 node가 있는지를 확인후 있으면 해당 node에 할당한다.

  ```yaml
  index.routing.allocation.include._tier_preference: data_warm,data_cold
  ```

  - Data stream을 통해 생성된 index의 경우 위 설정의 영향을 받지 않으며, 무조건 hot tier에 할당된다.



- Index 생성시에 tier 설정하기

  - 아래와 같이 index 생성시에 설정이 가능하다.

  ```json
  PUT test
  {
    "settings": {
      "index.routing.allocation.include._tier_preference": "data_warm"
    }
  }
  ```

  - 위 설정이 elasticsearch.yml에 설정된 값보다 우선한다.





# ILM(Index Lifecycle Management)

- Docker compose를 통해 아래와 같이 테스트용 cluster를 구성한다.

  - Elasticsearch의 node는 홀수로 설정하는 것이 좋지만 테스트를 위한 cluster이므로 아래에서는 짝수로 설정했다.
  - 각 노드마다 data_hot, data_warm, data_cold, data_content tier를 부여한다.

  ```yaml
  version: '3.2'
  
  services:
    node1:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node1
      environment:
        - node.name=node1
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_hot]
        - discovery.seed_hosts=node2,node3,node4
        - cluster.initial_master_nodes=node1,node2,node3,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      ports: 
        - 9205:9200
      restart: always
      networks:
        - elastic
  
    node2:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node2
      environment:
        - node.name=node2
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_warm]
        - discovery.seed_hosts=node1,node3,node4
        - cluster.initial_master_nodes=node1,node2,node3,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      networks:
        - elastic
  
    node3:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node3
      environment:
        - node.name=node3
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_cold]
        - discovery.seed_hosts=node1,node2,node4
        - cluster.initial_master_nodes=node1,node2,node3,,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      networks:
        - elastic
    
    node4:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node4
      environment:
        - node.name=node4
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_content]
        - discovery.seed_hosts=node1,node2,node3
        - cluster.initial_master_nodes=node1,node2,node3,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      networks:
        - elastic
  
    kibana:
      image: docker.elastic.co/kibana/kibana:8.6.0
      container_name: kibana
      ports:
        - "5605:5601"
      environment:
        ELASTICSEARCH_URL: http://node1:9200
        ELASTICSEARCH_HOSTS: http://node1:9200
      networks:
        - elastic
      depends_on:
        - node1
  
  networks:
    elastic:
      driver: bridge
  ```





## ILM을 사용하지 않고 tier를 수동으로 이동시키기

- Test용 index를 생성한다.

  - 당일에 색인된 data들은 data_hot, 지난 일주일의 data는 data_warm, 그 이상은 data_cold에 저장할 것이다.
  - 아래와 같이 일별로 index를 생성한다.

  ```json
  PUT test-20230713
  {
    "settings": {
      "number_of_replicas": 0, 
      "index.routing.allocation.include._tier_preference": "data_hot"
    }
  }
  
  PUT test-20230706
  {
    "settings": {
      "number_of_replicas": 0, 
      "index.routing.allocation.include._tier_preference": "data_warm"
    }
  }
  
  PUT test-20230701
  {
    "settings": {
      "number_of_replicas": 0, 
      "index.routing.allocation.include._tier_preference": "data_cold"
    }
  }
  ```



- 각 shard들의 할당 상태를 확인한다.

  - 요청

  ```http
  GET _cat/shards/test*?v&h=i,n&s=i:desc
  ```

  - 응답
    - 위에서 설정한 대로 할당 된 것을 확인할 수 있다.

  ```json
  i             n
  test-20230713 node1
  test-20230706 node2
  test-20230701 node3
  ```



- Tier를 이동시키기

  - `test-20230713` index를 warm tier로, `test-20230706` index를 cold tier로 이동시킬 것이다.

  ```json
  PUT test-20230713/_settings
  {
    "index.routing.allocation.include._tier_preference": "data_warm"
  }
  
  PUT test-20230706/_settings
  {
    "index.routing.allocation.include._tier_preference": "data_cold"
  }
  ```

  - 다시 확인해보면

  ```http
  GET _cat/shards/test*?v&h=i,n&s=i:desc
  ```

  - 잘 옮겨진 것을 확인할 수 있다.

  ```json
  i             n
  test-20230713 node1
  test-20230706 node2
  test-20230701 node3
  ```





## ILM을 사용하여 tier를 자동으로 이동시키기

- Index의 lifecycle을 관리할 수 있게 해주는 기능이다.
  - Index의 lifecycle은 아래와 같다.
    - hot
    - warm
    - cold
    - frozen
    - delete
  - 아래와 같은 방법으로 설정이 가능하다.
    - `_ilm` API를 사용하여 설정.
    - Kibana의 `Stack Management-Data-Index Lifecycle Policies`에서 UI를 통해 설정하는 방법.



### Action

- Action
  - Lifecycle의 각 phase마다 실행할 동작들이다.
  - 각 phase마다 실행할 수 있는 action이 다르다.



- Rollover

  > hot phase에서만 사용할 수 있다.

  - 특정 조건이 충족됐을 때, 기존 index를 새로운 index로 roll over한다.
  - Data stream과 index alias을 대상으로 사용할 수 있다.
  - Alias를 대상으로 할 경우 반드시 아래의 조건을 충족해야한다.
    - Index name은 반드시 `*^.\*-\d+$*` pattern과 일치해야한다.
    - `index.lifecycle.rollover_alias` 옵션에 alias를 입력해야한다.
    - Index가 반드시 write index여야한다(alias 설정시 `is_write_index`  옵션을 true로 줘야한다).



- Migrate

  > warm, cold phase에서 사용할 수 있다.

  - warn, cold phase에서 아무 action을 설정하지 않을 경우, 자동으로 migrate action이 설정된다.
  - Index를 다른 data tier로 이동시키는 action이다.
    - `index.routing.allocation.include._tier_preference`을 자동으로 변경시키는 방식으로 동작한다.



- Delete

  > delete phase에서만 사용할 수 있다.

  - Index를 영구적으로 삭제하는 action이다.



### ILM 사용하기

- ILM policy 생성 및 수정하기

  - `_meta`
    - Policy에 대한 meta data를 설정할 수 있다.
    - 여기에 설정한 정보는 policy 정보를 확인할 때 함께 노출된다.
  - `phases`
    - Phase를 설정한다.
    - 각 phase에는 `min_age`와 `actions`를 설정한다.
    - `actions`에 들어갈 수 있는 값은 각 phase마다 다르며, [공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-actions.html)에서 확인할 수 있으며, 
  - Update API는 따로 존재하지 않는다.
    - 아래 API를 통해서 생성고 수정을 모두 실행한다.
    - 이미 존재하는 `policy_id`로 요청을 보낼 경우 policy의 version이 올라가게 된다.
  - 예시

  ```json
  PUT _ilm/policy/my-ilm-policy
  {
    "policy": {
      "phases": {
        "hot": {
          "actions": {
            "rollover": {
              "max_age": "10s"
            }
          }
        },
        "warm": {
          "min_age": "20s",
          "actions": {}
        },
        "cold": {
          "min_age": "30s",
          "actions": {}
        },
        "delete": {
          "min_age": "40s",
          "actions": {
            "delete": {}
          }
        }
      }
    }
  }
  ```

  - warm과 cold phase의 경우 action을 설정해주지 않아도 자동으로 migrage action이 추가된다.



- ILM policy 조회 및 삭제하기

  - ILM policy 모두 가져오기

  ```json
  GET _ilm/policy
  ```

  - 특정 ILM policy 가져오기

  ```json
  GET _ilm/policy/<policy_id>
  ```

  - ILM policy 삭제하기

  ```json
  DELETE _ilm/policy/<policy_id>
  ```



- 관련 설정

  - 실행할 action이 있는지 확인하는 주기 변경하기
    - 기본적으로 ILM은 10분마다 실행할 action이 있는지를 확인한다.
    - 우리는 예시에서 10분보다 작은 간격을 설정했으므로, action을 확인하는 간격을 변경해줘야한다.
    - `indices.lifecycle.poll_interval` 설정을 변경해준다.

  ```json
  PUT _cluster/settings
  {
    "transient": {
      "indices.lifecycle.poll_interval": "5s" 
    }
  }
  ```

  - 문서가 없어도 action을 실행하도록 설정
    - ILM은 색인된 문서가 있어야 action을 실행한다.
    - `indices.lifecycle.rollover.only_if_has_documents` 값을 false로 변경해야 문서가 없어도 action을 실행한다.

  ```json
  PUT _cluster/settings
  {
    "transient": {
      "indices.lifecycle.rollover.only_if_has_documents": false
    }
  }
  ```



- Index에 ILM policy를 적용하기

  - Index template을 생성한다.

  ```json
  PUT _index_template/my-template
  {
    "index_patterns": [
      "my-index-*"
    ],
    "template": {
      "settings": {
        "number_of_replicas": 0,
        "index.lifecycle.name": "my-ilm",
        "index.lifecycle.rollover_alias": "my-alias",
        "index.routing.allocation.include._tier_preference": "data_hot"
      }
    }
  }
  ```

  - 위에서 생성한 template으로 index를 생성한다.

  ```http
  PUT my-index-000001
  {
    "aliases": {
      "my-alias": {
        "is_write_index": true
      }
    }
  }
  ```

  - 잘 적용되었는지 확인한다.

  ```http
  GET my-alias/_ilm/explain
  ```

  - 다음과 같이 동작한다(`indices.lifecycle.poll_interval`이 매우 작은 값이라 바로 적용된다고 가정)
    - 첫 index가 생성된지 10초가 지나면 rollover가 실행되어 두 번째 index가 생성된다.
    - 첫 index가 생성된지 20초가 지나면, 두 번째 index에 rollover가 실행되어 세 번째 index가 생성되고, 첫 번째 index가 hot에서 warm으로 tier가 변경된다(shard의 할당 위치가 다른 노드로 변경된다).
    - 첫 index가 생성된지 30초가 지나면, 세 번째 index에 rollover가 실행되어 네 번째 index가 생성되고, 첫 번째 index는 warm에서 cold로, 두 번째 index는 hot에서 warm으로 tier가 변경된다.
    - 첫 index가 생성된지 40초가 지나면, 네 번째 index에 rollover가 실행되어 다섯 번째 index가 생성되고, 두 번째 index는 warm에서 cold로, 세 번째 index는 hot에서 warm으로 tier가 변경되며, 첫 번째 index는 삭제된다.





# Sniffing

> https://www.elastic.co/kr/blog/elasticsearch-sniffing-best-practices-what-when-why-how

- Sniffing이란

  > Sniff는 "코를 킁킁 거리며 냄새를 맡다", "코를 훌쩍이다" 등의 뜻을 가지고 있다.

  - Elasticsearch와 application 사이의 연결은 대부분의 경우에 Elasticsearch client를 통해서 이루어진다.
    - Python을 예로 들면 `elasticsearch package`를 사용한다.
    - Elasticsearch는 Elasticsearch와 application 사이의 연결을 최적화하는 다양한 방식을 제공하며, sniffing 역시 그 중 하나다.
  - Elasticsearch는 분산 시스템이다.
    - 여러 node에 data를 분산하여 저장하는 것의 장점은 고가용성뿐이 아니다.
    - 여러 노드에 shard가 분산되어 저장되어 거대한 단일 노드에 검색하는 것 보다 훨씬 빠른 검색이 가능하게 해준다.
  - Client와 Elasticsearch 사이의 연결과 관련된 가장 일반적인 설정 방식은 cluster의 노드들 중 하나의 node의 URL만 입력하는 것이다.
    - 이는 가장 간단한 방법이긴 하지만, 단점도 있다.
    - 가장 중요한 단점은 client에서 보내는 모든 요청이 URL을 통해 설정된 하나의 coordination node로만 향한다는 것이다.
    - 이는 해당 node에 부하가 가해지도록 하고, 전체 성능에 영향을 주게 된다.
    - 이를 해결하는 방법은 모든 node의 URL을 입력하여 각 node에 돌아가면서 요청이 전달되도록 하는 것이다.
    - 문제는 이 방식을 사용하기 위해서는 node 중 하나라도 내려가선 안 된다는 것이다.
    - Sniffing을 사용할 경우 한 node가 내려가더라도 요청이 나머지 node에 고르게 전달되도록 할 수 있다.
  - Sniffing
    - Sniffing을 활성화하면 client는 `_nodes/_all/http` endpoint를 호출한다.
    - 위 endpoint는 cluster에 속한 각 node들의 IP 주소가 포함된 정보를 반환한다.
    - Client는 이 정보를 가지고 connection pool을 update하여 cluster에 속한 node의 정보와 connection pool을 동기화한다.
    - 단, 모든 node에 대한 정보를 가져온다고 해서, master_only node에게도 요청을 보내는 것은 아니다.



- Sniffing은 양날의 검이다.

  - 아래와 같은 경우에 문제가 생길 수 있다.
    - Elasticsearch cluster가 자신만의 network를 사용할 경우.
    - Elasticsearch cluster가 load balancer 뒤에 있을 경우.
    - Cloud provider를 사용하는 경우.
    - Elasticsearch client가 `_nodes` API에 접근할 수 있는 권한(monitoring_user)이 없을 경우.
  - 앞의 세 경우는 모두 `_nodes/_all/http`가 반환하는 IP address로는 node에 접근할 수 없기 때문이다.
    - 예를 들어 Docker를 사용하여 cluster를 구성하는 경우를 생각해보자(첫 번째 경우에 해당).
    - Docker container 내부에서는 host machie과는 다른 network를 사용하여 통신이 이루어진다.
    - 아래와 같이 Python client에서 확인해보면 `_nodes/_all/http` endpoint에 해당하는 `nodes.info()` 요청을 보냈을 때, 각 node에 담겨온 `publish_address`의 정보가 host mahcine의 address와 다른 것을 확인할 수 있다.
    - 단 7.17 version 기준으로 `_nodes/_all/http`의 반환값으로 `bound_address` 값이 함께 넘어오는데 client가 이 값을 사용하는지는 확인이 필요하다.

  ```python
  from elasticsearch import Elasticsearch
  
  # 10.11.12.13는 host machine의 IP
  es_client = Elasticsearch("http://10.11.12.13:9200", sniff_on_start=True)
  node_info = es_client.nodes.info(node_id="_all", metric="http")
  print(json.dumps(node_info, indent="\t"))
  ```

  - 단 첫 번째 경우는 `http.publish_host`를 설정함으로써 해결할 수 있다.
    - `http.publish_host`에 host machine의 host를 입력하면,  `_nodes/_all/http`의 반환값에 `http.publish_host`에 설정된 host가 함께 반환된다.
    - 공식 client 7.0 version 이상부터는  `_nodes/_all/http`의 반환값에 `http.publish_host`에 설정된 host가 함께 반환될 경우, 이 host를 가지고 sniffing을 실행한다.



- Sniffing 사용 방법
  - 시작시에 sniffing하기
    - Client가 initialize 될 때 단 한 번만 sniffing을 실행하는 방식이다.
  - Connection이 실패할 경우 sniffing하기
    - Node에 요청이 실패했을 경우에만 sniffing을 실행한다.
    - 즉, node가 내려가거나 node와의 connection이 끊어졌을 경우에 sniffing을 실행한다.
  - 일정 간격을 두고 sniffing하기
    - 일정 간격을 두고 sniffing을 실행하는 방식이다.
    - Cluster에 노드가 빈번히 추가되거나 제거되는 경우에 유용한데, 시작시에만 sniffing을 하거나 connection이 실패했을 경우에만 sniffing을 할 경우 cluster에 node가 추가되어도 알지 못하기 때문이다.
  - Custom한 방식으로 sniffing하기
    - 사용자가 원하는 방식으로 sniffing하는 방법이다.



- Elasticsearch Python client의 sniffing

  > https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/config.html

  - Elasticsearch Python client도 sniffing과 관련된 다양한 옵션을 제공한다.
  - `sniff_on_start`(bool, default:False)
    - Client가 instantiation될 때 단 한 번만 sniffing을 실행하는 방식이다.
  - `sniff_before_requests`(bool, default:False)
    - Elasticsearch에 request를 보내기 전에 sniffing을 실행하는 방식이다.
  - `sniff_on_node_failure`(bool, default:False)
    - Connection이 실패했을 경우 sniffing을 실행하는 방식이다.
  - `sniff_on_connection_fail`(deprecate 될 예정)
    - Connection이 실패했을 경우 sniffing을 실행하는 방식이다.
    - `sniff_on_node_failure`로 대체된다.
  - `sniff_timeout`(float)
    - 8 version부터는 기본값이 0이며, 그 전 version에서는 0.2이다.
    - Sniffing을 위해  `_nodes/_all/http`을 보낼 때의 timeout을 설정한다.
    - `sniff_on_start`이 설정됐을 경우, 첫 sniffing은 이 값을 무시한다.
  - `sniffer_timeout`(float)
    - 8 version에서 deprecated 예정이며, `min_delay_between_sniffing`로 대체될 예정이다.
    - sniffing과 sniffing 사이의 시간 간격을 설정한다.
  - `sniffed_node_callback`
    - 기본적으로 master_only 역할을 가진 node는 사용되지 않는다.
    - 만일, 추가적으로 사용하지 않을 node를 설정하고자 한다면 `sniffed_node_callback`에 관련 logic을 구현한 함수를 넣어주면 된다.

  ```python
  from typing import Optional, Dict, Any
  from elastic_transport import NodeConfig
  from elasticsearch import Elasticsearch
  
  
  def filter_master_eligible_nodes(
      node_info: Dict[str, Any],
      node_config: NodeConfig
  ) -> Optional[NodeConfig]:
      # 예를 들어 이 callback은 node eligible한 모든 node를 요청 대상 node에서 제외시킨다.
      if "master" in node_info.get("roles", ()):
          return None
      return node_config
  
  client = Elasticsearch(
      "https://localhost:9200",
      sniffed_node_callback=filter_master_eligible_nodes
  )
  ```






# Snapshot

- Snapshot
  - Elasticsearch cluster의 backup이다.
  - 아래와 같은 경우 사용한다.
    - Cluster의 중단 없이 cluster를 backup하기 위해서.
    - Data를 복원하기 위해서.
    - Cluster 간에 data를 전송하기 위해서.
    - Cold, frozen data tier에서 searchable snapshot을 사용하여 저장 비용을 절감하기 위해서.
  - Snapshot repository
    - Snapshot은 snapshot repository라 불리는 저장소에 저장된다.
    - 따라서 snapshot 기능을 사용하기 위해서는 먼저 cluster에 snapshot repository를 지정해야한다.
    - AWS S3, Google Cloud Storage, Microsoft Azure를 포함하여 다양한 option을 제공한다.
  - Repository는 Elasticsearch version간에 호환되지 않을 수도 있다.
    - 이전 version의 elasticsearch에서 snapshot을 생성하고, elasticsearch를 update하더라도, 기존의 snapshot을 그대로 사용할 수 있다.
    - 그러나, 만약 update된 elasticsearch에서 repository에 수정을 가하면, 그 때부터는 이전 version의 elasticsearch에서 사용할 수 없을 수도 있다.
    - 따라서 여러 cluster가 하나의 repository를 공유해야한다면 repository를 공유하는 모든 cluster들의 elasticsearch version이 같아야한다.



- Snapshot에는 아래와 같은 정보들이 포함된다.
  - Cluster state
    - Persistent cluster settings(transient cluster settings는 저장되지 않는다).
    - Index template
    - Legacy index template
    - Ingest pipeline
    - ILM policy
    - Feature state(Elasticsearch의 설정 정보를 저장하거나, security나 kibana 등의 특정 기능을 위한 index 혹은 data stream을 의미한다).
  - Data stream
  - Regular Index



- Snapshot을 생성하기 위한 조건
  - Master node가 있는 실행 중인 cluster가 있어야한다.
  - Snapshot repository가 등록되어 있어야한다.
  - Cluster의 global metadata가 readable해야한다.
  - 만약 snapshot에 index를 포함시킬 것이라면, index와 index의 metadata도 readable해야한다.



- Snapshot의 동작 방식
  - Index를 backup하는 방식
    - Index의 segment를 복사해서 snapshot repository에 저장한다.
    - Segment는 수정할 수 없기 때문에, repository의 마지막 snapshot 생성 이후에 새로 생긴 segment들만 copy한다.
    - 각각의 segment는 논리적으로 분리되어 있기 때문에, 한 snapshot을 삭제하더라도, 다른 snapshot에 저장된 segment는 삭제되지 않는다.
  - Snapshot과 shard 할당
    - Snapshot은 primary shard에 저장된 segment들을 복사한다.
    - Snapshot 생성을 시작하면, Elasticsearch는 접근 가능한 primary shard의 segment들을 즉시 복제한다.
    - 만약 shard가 시작 중이거나 재할당 중이라면, Elasticsearch는 이를 기다렸다 완료되면 복제한다.
    - 만약 하나 이상의 primary shard를 사용할 수 없는 상태라면, snapshot은 생성되지 않는다.
    - Snapshot을 생성하는 중에는, Elasticsearch는 shard를 이동시키지 않고, snapshot 생성이 완료되면 shard를 이동시킨다.
  - Snapshot은 특정 시점의 cluster를 보여주지 않는다.
    - Snapshot은 시작 시간과 종료 시간을 포함하고 있다.
    - Snapshot은 이 시작 시간과 종료 시간 사이의 어떤 시점의 shard의 data 상태만 보여줄 뿐이다.



- 고려사항
  - 각 snapshot은 repository 내에서 고유한 이름을 가지므로, 이미 존재하는 이름으로는 snapshot을 생성할 수 없다.
  - Snapshot에는 자동으로 중복 제거가 실행되므로, snapshot을 빈번하게 생성해도 storage overhead가 크게 증가하지는 않는다.
  - 각각의 snapshot은 논리적으로 구분되므로, 하나의 snapshot을 삭제하더라도 다른 snapshot에는 영향을 주지 않는다.
  - Snapshot을 생성하는 중에는 일시적으로 shard의 할당이 정지된다.
  - Snapshot을 생성하더라도 indexing을 포함한 다른 요청들이 block되지는 않지만, snapshot의 생성이 시작된 이후의 변경사항들은 반영되지 않는다.
  - `snapshot.max_concurrent_operation` 설정을 변경하여 동시에 생성 가능한 snapshot의 최대 개수를 변경할 수 있다.
  - 만일 snapshot에 data stream을 포함할 경우, data stream의 backing index들과 metadata도 snapshot에 저장된다.



- Repository 등록하기

  > Kibana를 통해서도 등록 가능하다.

  - 아래와 같이 `_snapshot` API를 사용하여 repository를 등록할 수 있다.
    - Shared file system respositroy로 사용하기 위해 `type`을 `fs`로 준다.
    - `elasticsearch.yml`파일의 `path.repo`에 설정해준 경로를 넣어준다.
    - 아래와 같이 모든 경로를 넣어줘도 되고, 넣지 않을 경우, `path.repo`에 설정한 경로부터 상대경로로 설정된다.

  ```json
  // PUT _snapshot/<repository>
  {
    "type": "<type>",
    "settings": {
      "location": "<path.repo에 설정한 경로를 기반으로 한 경로>"
    }
  }
  ```

  - 예시

  ```json
  // PUT _snapshot/my-fs-repo
  {
    "type": "fs",
    "settings": {
      "location": "/usr/share/elasticsearch/snapshots/my_snapshot"
      // "location": "my_snapshot" 과 같이 주는 것과 완전히 같다.
    }
  }
  ```

  - 하나의 snapshot repository를 여러 cluster에 등록 할 경우, 오직 한 곳에서만 작성이 가능하고, 나머지 cluster에서는 읽기만 가능하다.



- Repository 목록 조회

  - `_cat` API를 통해 전체 repository들을 확인할 수 있다.

  ```http
  GET _cat/repositories
  ```



- Repository에서 참조되지 않는 데이터 일괄 삭제하기

  - 시간이 지남에 따라 respository에는 어느 snapshot도 참조하지 않는 data들이 쌓이기 시작한다.
    - 이들이 repository의 성능에 악영향을 미치는 것은 아니지만, 용량을 차지하고 있기는 하므로, 삭제시키는 것이 좋다.
  - 아래 API를 통해 참조되지 않는 data를 일괄 삭제할 수 있다.

  ```http
  POST _snapshot/<repository>/_cleanup
  ```

  - Snapshot을 삭제할 때 이 endpoint도 자동으로 호출된다.
    - 따라서 만일 주기적으로 snapshot을 삭제한다면, 굳이 이 endpoint를 호출할 필요는 없다.



- Repository 삭제하기

  - Repository를 삭제하더라도, repository에 저장되어 있던 snapshot들은 삭제되지 않는다.

  ```http
  DELETE _snapshot/<repository>
  ```

  

  



- SLM(Snapshot Lifecycle Management)

  - Snapshot을 자동으로 관리해주는 기능이다.
    - 설정된 일정에 따라 snapshot을 자동으로 생성할 수 있다.
    - 설정한 기간이 지난 snapshot들을 자동으로 삭제할 수 있다.

  - SLM Policy 생성하기

  ```json
  // PUT _slm/policy/<snapshot>
  {
    // snapshot을 생성할 schedule을 설정한다.
    "schedule": "0 30 1 * * ?",
    // snapshot의 이름을 설정한다.
    "name": "<nightly-snap-{now/d}>", 
    // snapshot을 저장할 repository를 설정한다.
    "repository": "my_repository",
    "config": {
      // data stream을 포함한 모든 종류의 index들을 snapshot에 저장한다.
      "indices": "*",
      // cluster state를 snapshot에 포함시킨다.
      "include_global_state": true    
    },
    "retention": {
      "expire_after": "30d",	// 30일 동안 snapshot을 저장한다.
      "min_count": 5,			// 보유 기간과 상관 없이 최소 5개의 snapshot을 저장한다.
      "max_count": 50			// 보유 기간과 상관 없이 최대 50개의 snapshot을 저장한다.
    }
  }
  ```

  - SLM Policy를 수동으로 실행하기
    - Snapshot을 즉시 생성하기 위해서 SLM policy를 수동으로 실행할 수도 있다.

  ```http
  POST _slm/policy/<snapshot>/_execute
  ```

  - SLM retention
    - SLM snapshot retension은 policy에 설정된 snapshot schedule과 별개로 실행되는 cluster 수준의 task이다.
    - SLM retention task를 언제 실행할지는 아래와 같이 설정할 수 있다.

  ```json
  // PUT _cluster/settings
  {
    "persistent" : {
      "slm.retention_schedule" : "0 30 1 * * ?"
    }
  }
  ```

  - SLM snapshot retention 바로 실행시키기
    - SLM policy와 마찬가지로 바로 실행시키는 것도 가능하다.

  ```http
  POST _slm/_execute_retention
  ```



- SLM을 사용하지 않고 수동으로 관리하기

  - Snapshot 생성하기
    - Snapshot 이름은 [date math](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#api-date-math-index-names)를 지원한다.


  ```HTTP
  PUT _snapshot/<repository>/<my_snapshot_{now/d}>
  ```

  - Snapshot을 삭제하기

  ```http
  DELETE _snapshot/<repository>/<snapshot>
  ```



- Snapshot monitoring하기

  - 현재 실행중인 snapshot들 받아오기

  ```http
  GET _snapshot/<repository>/_current
  ```

  - Snapshout의 상태 받아오기

  ```http
  GET _snapshot/_status
  ```

  - SLM의 실행 기록 받아오기

  ```http
  GET _slm/stats
  ```

  - 특정 SLM policy의 실행 기록 가져오기

  ```http
  GET _slm/policy/<slm_policy>
  ```



- Snapshot 정보 확인하기

  - 사용 가능한 전체 snapshot 목록 확인하기

  ```http
  GET _sanpshot
  ```

  - 특정 repository에 저장된 snapshot 목록 받아오기
    - `<snapshot>`에 `*` 또는 `_all`을 입력하면 전체 목록을 받아올 수 있다.
    - `verbose` query parameter를 false로 주어 간략한 정보만 받아올 수 있다.

  ```http
  GET _snapshot/<repository>/<snapshot>[?query_params]
  ```



- Snapshot 복원하기

  - 아래에서는 API를 통해서 했지만, Kibana를 통해서도 가능하다.

  ```http
  POST _snapshot/<repository>/<snapshot>/_restore
  {
    "indices": "index_1,index_2",
    "ignore_unavailable": true,
    "include_global_state": false,
    "rename_pattern": "index_(.+)",
    "rename_replacement": "restored_index_$1",
    "include_aliases": false
  }
  ```

  - `indices`
    - 복원할 index들과 data stream들을 array 형태로 입력한다.
    - 아무 값도 주지 않으면 snapshot에 저장된 모든 index와 data stream이 복원된다.
    - 단, sysrem index와 system data stream은 복원되지 않는데, 이는 `feature_state` 값을 true로 줘야한다.
  - `ignore_unavailable`
    - `indices`에 설정해준 index나 data stream 들이 snapshot에 없을 경우 예외를 발생시킬지 여부를 설정한다.
    - false(기본값)로 줄 경우 없을 경우 예외가 발생한다.
  - `include_global_state` 
    - Cluster state도 함께 복원할지 여부를 결정하며, 기본값은 false이다.
    - Data stream의 경우 복원시에 index template이 필요한데, index template은 cluster state에 포함되어 있는 값이다.
    - 따라서 data stream을 복원하려면 이 값을 true로 주거나, index template을 새로 생성해야한다(index template이 없어도 data stream이 복원은 된다).
  - `feature_state`
    - 복원시킬 feature state의 목록을 입력한다.
    - Feature state도 cluster state에 포함된 값이므로, `include_global_state`가 true로 설정되어 있다면 feature state도 복원된다.
    - 만약 `include_global_state`가 false로 설정되어 있다면, feature state도 복원시키지 않는다.
    - 만약 이 값을 `["none"]`으로 줄 경우 `include_global_state`값이 true라고 하더라도 feature state는 복원되지 않는다.
  - `rename_pattern`
    - 복원된 index와 data stream에 적용할 rename pattern을 설정한다.
    - `rename_pattern`과 일치하는 index와 data stream은 `rename_replacement` 값에 따라 rename된다.
    - 위 예시의 경우 만약 snapshot에 `index_(.+)`에 mathcing되는 index나 data stream이 있을 경우, `restore_index_$1` 형식으로 rename된다.



- 복원하려는 index나 data stream과 동일한 이름으로 생성된 index 또는 data stream이 있다면 복원되지 않는다.
  - 삭제 후 복원하기
    - 이미 존재하는 index나 data stream을 삭제하고 snapshot에 있는 index나 data stream을 복원하는 방식이다.
    - 이미 존재하는 index 혹은 data stream을 수동으로 삭제한 후 restroe API를 통해 snapshot에 있는 data를 복원한다.
  - 복원시 rename하기
    - 복원시에 `rename_pattern`과 `rename_replacement` 옵션을 줘서 복원시에 rename을 해준다.
    - Data stream을 rename할 경우 data stream의 backing index들도 rename된다.
    - Index template의 경우, 생성시에 설정한 `index_patterns`에 data stream의 이름을 맞춰줘야 하기에 결국 기존 index나 data stream을 삭제하고 reindex를 해줘야한다.



- Snapshot 삭제하기

  - 생성 중인 snapshot을 삭제할 경우 생성이 취소된다.

  ```http
  DELETE _snapshot/<repository>/<snapshot>
  ```





## 실습

- Snapshot test를 위한 cluster 구성

  - Docker를 사용해 elasticsearch cluster를 구성하기 위해 docker-compose.yml 파일을 아래와 같이 작성한다.
  - Test에서는 snapshot repository 중 shared file system repository를 사용할 것인데, 이를 위해서는 몇 가지 설정을 해줘야한다.
    - `path.repo`에 snapshot을 저장할 directory를 지정한다.
    - Snapshot을 생성하려는 위치에 volume을 설정한다(필수).

  ```yaml
  version: '3.2'
  
  services:
    node1:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node1
      environment:
        - node.name=node1
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_hot,data_content]
        - discovery.seed_hosts=node2,node3,node4
        - cluster.initial_master_nodes=node1,node2,node3,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
        - path.repo=/usr/share/elasticsearch/snapshots
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - snapshots:/usr/share/elasticsearch/snapshots
      ports: 
        - 9205:9200
      restart: always
      networks:
        - elastic
  
    node2:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node2
      environment:
        - node.name=node2
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_warm]
        - discovery.seed_hosts=node1,node3,node4
        - cluster.initial_master_nodes=node1,node2,node3,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
        - path.repo=/usr/share/elasticsearch/snapshots
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - snapshots:/usr/share/elasticsearch/snapshots
      restart: always
      networks:
        - elastic
  
    node3:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node3
      environment:
        - node.name=node3
        - cluster.name=es-docker-cluster
        - node.roles=[master,data_cold,ingest]
        - discovery.seed_hosts=node1,node2,node4
        - cluster.initial_master_nodes=node1,node2,node3,,node4
        - bootstrap.memory_lock=true
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        - xpack.security.enabled=false
        - xpack.security.enrollment.enabled=false
        - path.repo=/usr/share/elasticsearch/snapshots
      ulimits:
        memlock:
          soft: -1
          hard: -1
      volumes:
        - snapshots:/usr/share/elasticsearch/snapshots
      restart: always
      networks:
        - elastic
  
    kibana:
      image: docker.elastic.co/kibana/kibana:8.6.0
      container_name: kibana
      ports:
        - "5605:5601"
      environment:
        ELASTICSEARCH_URL: http://node1:9200
        ELASTICSEARCH_HOSTS: http://node1:9200
      networks:
        - elastic
      depends_on:
        - node1
  
  volumes:
    snapshots:
      driver: local
  
  networks:
    elastic:
      driver: bridge
  ```



- Snapshot에 담길 data들 생성하기

  - Persistent cluster settings 변경하기
    - 위에서 생성한 node 중 `node3`에는 shard가 할당되지 않도록 아래와 같이 설정을 변경한다.

  ```http
  PUT _cluster/settings
  {
    "transient": {
      "indices.lifecycle.poll_interval": "10s",
      "indices.lifecycle.rollover.only_if_has_documents": false
    }
  }
  ```
  
  - Regular index 생성하기
  
  ```http
  PUT my-index/_doc/1
  {
    "foo":"bar"
  }
  ```
  
  - ILM policy 생성하기
  
  ```http
  PUT _ilm/policy/my-ilm-policy
  {
    "policy": {
      "phases": {
        "hot": {
          "actions": {
            "rollover": {
              "max_age": "30s"
            }
          }
        },
        "warm": {
          "min_age": "1m",
          "actions": {}
        },
        "cold": {
          "min_age": "2m",
          "actions": {}
        },
        "delete": {
          "min_age": "3m",
          "actions": {
            "delete": {}
          }
        }
      }
    }
  }
  ```
  
  - Index template 생성하기
  
  ```http
  PUT _index_template/my-template
  {
    "index_patterns": [
      "my-data-stream*"
    ],
    "data_stream": {},
    "template": {
      "settings": {
        "number_of_replicas": 0,
        "index.lifecycle.name": "my-ilm-policy",
        "index.routing.allocation.include._tier_preference": "data_hot"
      },
      "mappings": {
        "properties": {
          "@timestamp": {
            "type": "date"
          },
          "message": {
            "type": "text"
          }
        }
      }
    }
  }
  ```
  
  - Data stream 생성하기
  
  ```http
  PUT _data_stream/my-data-stream
  ```
  
  - Data stream에 data 색인
  
  ```http
  POST my-data-stream/_doc
  {
    "@timestamp": "2099-05-06T16:21:15.000Z",
    "message": "hello world!"
  }
  ```
  
  - `docker-compose.yml`에 kibana도 함께 생성하도록 설정했으므로 kibana에 관한 feature state도 생성될 것이다.



- Snapshot 생성하기

  - Repository 등록하기

  ```http
  PUT _snapshot/my_fs_backup
  {
    "type": "fs",
    "settings": {
      "location": "/usr/share/elasticsearch/snapshots/my_snapshot"
    }
  }
  ```

  - Snapshot 생성하기

  ```http
  PUT _snapshot/my_fs_backup/my_snapshot
  ```

  - 잘 생성 됐는지 확인하기

  ```http
  GET _snapshot/my_fs_backup/my_snapshot
  ```



- Snapshot restore하기

  - Docker compose를 통해 생성한 모든 container를 삭제한다.
    - Snapshot을 저장하는 repository 외에는 volume 설정을 하지 않았기에, container를 삭제하면 data가 모두 삭제된다.

  ```bash
  $ docker compose down
  $ docker compose up
  ```

  - 이전에 등록했던 repoistory의 경로로 repository를 다시 등록해준다.

  ```http
  PUT _snapshot/my_fs_backup
  {
    "type": "fs",
    "settings": {
      "location": "/usr/share/elasticsearch/snapshots/my_snapshot"
    }
  }
  ```

  - 이전에 생성한 snapshot이 있는지 확인

  ```http
  GET _snapshot/my_fs_backup/my_snapshot
  ```

  - Snapshot을 통해 복원하기
    - Regular index와 data stream 모두 `my-*` 형식으로 생성했으므로 `indices`에도 아래와 같이 넣어준다.
    - 우선은 test를 위해 `include_global_state` 값을 false로 준다.

  ```http
  POST _snapshot/<repository>/<snapshot>/_restore
  {
    "indices": "my-*",
    "ignore_unavailable": true,
    "include_global_state": false,
    "rename_pattern": "my-*",
    "rename_replacement": "restored_my_index_"
  }
  ```

  - 확인하기
    - 아래와 같이 index와 data stream은 복원된 것을 확인할 수 있다.
    - 그러나 `_cluster/settings`, `_index_template/my-*`, `_ilm/policy/my-*` 등을 통해 확인해보면 cluster settings, index template, ILM policy 등은 복원되지 않은 것을 확인할 수 있다.

  ```json
  // _cat/indices
  restored_my_index_index                             
  .ds-restored_my_index_data-stream-2023.07.17-000001
  ```

  - `include_global_state`를 true로 주고 다시 복원하기
    - 기존에 복원한 것과 동일한 이름으로 rename할 수 는 없으므로 `rename_replacement`를 아래와 같이 변경한다.

  ```http
  POST _snapshot/<repository>/<snapshot>/_restore
  {
    "indices": "my-*",
    "ignore_unavailable": true,
    "include_global_state": true,
    "rename_pattern": "my-*",
    "rename_replacement": "restored_my_index_2_"
  }
  ```

  - 위에서 복원되지 않았던 값들이 전부 복원된 것을 확인할 수 있다.



- Data stream과 index template

  - 우리가 위에서 index template을 생성할 때, `index_patterns`를 `"my-data-stream*"`으로 줬다.
  - 그러나, 복원시에 rename을 하면서 data stream의 이름이 `restored_my_index_2_data`로 변경되어, 더 이상 index template을 적용받지 못하게 된다.
    - 아래와 같이 복원된 data stream을 확인해보면 template이 적용되어 있지 않다는 것을 확인할 수 있다.

  ```http
  GET _data_stream/restored_my_index_2_data-stream
  {
    "data_streams": [
      {
        "name": "restored_my_index_2_data-stream",
        "timestamp_field": {
          "name": "@timestamp"
        },
        "indices": [
          {
            "index_name": ".ds-restored_my_index_2_data-stream-2023.07.17-000001",
            "index_uuid": "VzRqKpUNTb22J2txnq516Q"
          }
        ],
        "generation": 1,
        "status": "GREEN",
        "hidden": false,
        "system": false,
        "allow_custom_routing": false,
        "replicated": false
      }
    ]
  }
  ```

  - 해결 방법
    - 두 가지 해결 방법이 있다.
    - 복원 전에 `index_patterns`값에 `restored_my_index_2_data-stream`를 포함시킨 index template을 생성하고 복원한다.
    - 복원 된 index template의 `index_patterns`에 맞는 data stream을 생성 후, 해당 data stream에 복원된 data stream을 재색인한다.
    - 아래 예시에서는 두 번째 방법을 적용해 볼 것이다.
  - Index template의 `index_patterns`에 맞는 data stream 생성하기

  ```http
  PUT _data_stream/my-data-stream
  ```

  - 위 data stream에 복원된 data stream의 data를 재색인한다.
    - Data stream을 재색인 할 때는 `op_type`을 create로 줘야한다.

  ```http
  POST _reindex
  {
    "source": {
      "index":"restored_my_index_2_data-stream"
    },
    "dest": {
      "index": "my-data-stream",
      "op_type": "create"
    }
  }
  ```







# Bootstrap check

- Bootstrap check
  - Elasticsearch가 실행될 때 Elasticsearch와 system이 Elasticsearch를 안정적으로 실행할 수 있도록 설정되어 있는지를 확인하는 작업이다.
    - 만약 이상한 점이 발견되면 개발 모드에서는 warning log를 남기기만 한다.
    - 그러나 운영 모드에서는 이상한 점이 발견될 경우 Elasticsearch를 실행시키지 않는다.
  - Bootstrap check를 하는 이유
    - 이전 version에서는 Elasticsearch의 중요 설정들을 설정하지 않은 경우, warning으로 log를 남겼다.
    - 그러나 이 log를 놓치는 사용자들이 많았고, 이런 상황을 방지하기 위해 Elasticsearch는 최초 실행시에 bootstrap check를 실행한다.
  - 개발 모드와 운영 모드
    - 기본적으로 Elasticsearch는 IP주소를 loopback으로 설정한다.
    - `network.host`값이 loopback 주소로 설정되거나 `discovery.type`이 `single-node`일 경우 Elasticsearch가 개발 모드로 실행된다.
    - 개발 모드로 실행되면 bootstrap check에 실패해도 Elasticsearch가 실행된다.
    - 반면에 둘 다 아닐 경우 운영 모드로 실행된다.



- Bootstrap check 과정

  > Bootstrap을 실행하는 code는 [github](https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/bootstrap/BootstrapChecks.java)에서 볼 수 있다.

  - Heap size check
    - JVM의 기본 힙 크기(`-Xms`)와 최대 힙 크기(`-Xmx`)의 값이 같은지 확인한다.
    - Elasticsearch는 많은 memory를 사용하기 때문에 처음부터 기본 힙 크기(`-Xms`)와 최대 힙 크기(`-Xmx`)의 값을 같게 설정하는 것이 좋다.
    - 운영 중에 힙 크기 조정이 발생할 경우 시스템이 일시 정지할 위험이 있기 때문이다.
    - 또한 이는 Memory Lock과도 관련이 있는데, Elasticsearch는 swapping을 최소화하기 위해 전체 힙 메모리에 대해 Memory Lock을 숭행하는데, 두 기본 힙 크기와 최대 힙 크기가 다를 경우 기본 힙 크기만큼만 Memory Lock 대상으로 잡는다.
    - 따라서 나중에 늘어난 힙 크기만큼의 메모리는 swapping의 대상이 될 수 있다.
  - File descriptor check
    - Elasticsearch가 사용할 file descriptor가 충분히 있는지 검사한다.
    - Linux에서는 소켓, 시스템 콜 등 모든 것이 file로 처리된다.
    - 따라서 file을 처리하는 데 사용되는 file descriptor의 수가 매우 중요한 요소이다.
    - Elasticsearch는 통신도 많이 발생하고 I/O도 많이 사용하며, 특히 Lucene의 경우 inverted index를 구성하는  정보를 모두 file로 처리하기 땜누에 더더욱 많은 수의 file descriptor를 필요로한다.
  - Memory Lock check
    - Elasitcsearch에 할당된 heap memory의 Memory Lock 여부를 검사한다.
    - JVM은 memory 관리를 위해 주기적으로 garbage collection을 수행한다.
    - 이 과정에서 메모리를 확보하기 위해 불필요하 객체를 찾게 되고, 이러한 객체들을 힙 영역에서 제거함으로써 메모리를 확보한다.
    - Garbage collection이 수행될 경우 모든 heap memory를 검사해야하는데, 이 때 heap을 구성하는 memory page 조각 중 단 하나라도 swap-out 되어 있다면 이를 memory에 다시 올리는 swap-in 작업을 반드시 해야한다.
    - 이러한 swap-in, swap-out 작업은 JVM 기반 application에 큰 부담을 주기에, Elasticsearch는 swapping을 최대한 사용하지 않는 것을 권장하며, heap에 할당된 memory는 swapping의 대상이 되지 않도록 Memory Lock을 이용해 잠그도록 안내한다.
    - `bootstrap.memory_lock` option이 enable 되었을 때만 검사한다.
  - Maximum numbeor of threads check
    - Elasticsearch process가 생성할 수 있는 최대 thread 수를 검사한다.
    - 대량의 요청을 빠르게 처리하기 위해 내부를 기능별로 나눠 여러 단계의 모듈로 구성되어 있다.
    - 각 모듈은 queue와 thread pool을 가지고 있기 때문에 요청에 대한 throughput을 조절하면서 탄력적으로 처리하는 것이 가능하다.
    - 모듈 내부에는 Thread Pool Excecuter가 있어 많은 수의 thread를 생성하고 관리한다.
    - Thread Pool Exceutor가 여유롭게 thread를 생성할 수 있도록 Elasticsearch가 최소 4096개 이상의 thread를 생성할 수 있도록 설정하는 것이 좋다.
    - `/etc/security/limits.conf` file에서 `nproc`(max number of processes) 값을 설정하여 변경할 수 있다.
  - Max file size check
    - Elasticsearch가 생성할 수 있는 최대 file 크기가 충분한지(unlimited) 검사한다.
    - Segment file과 translog file은 상황에 따라 매우 커질 수도 있다.
    - 따라서 Elasticsearch를 안정적으로 운영하기 위해서는 최대 파일 크기를 무제한으로 설정하는 것이 좋다.
    - `/etc/security/limits.conf` file에서 `fsize`값을 `unlimited`로 설정하면 된다.
  - Maximum size virtual memory check
    - Elasticsearch process가 무한한 address space를 가지고 있는지 확인한다.
    - Elasticsearch와 Lucene은 index를 효율적으로 관리하기 위해 mmap을 사용하여 memory를 mapping한다.
    - mmap을 사용하면 JVM을 통하지 않고도 linux kernel로 직접 SystemCall을 실행할 수 있어 고성능 Java application에서 많이 사용한다.
    - mmap은 kernel 수준의 memory를 직접 할당 받아 application의 가상 memory 주소에 mapping해서 동작하기 때문에 가상 memory 크기에 제한이 없는 것이 좋다.
    - Elasticsearch에서는 mmap을 효율적으로 활용하기 위해 application의 가상 memory를 무제한으로 설정하도록 한다.
    - `/etc/security/limits.conf` file에 `<user> - as unlimited`를 추가하면 된다.
  - Maximum map count check
    - Elasticsearch process가 최소 262,144 개의 memory-mapped area를 가질 수 있는지 검사한다.
    - mmap을 효율적으로 사용하기 위해서 Elasticsearch는 또한 많은 memory-mapped areas를 생성할 수 있어야한다.
    - [Store module](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-store.html) 중 `mmapfs` 또는 `hybridfs`를 사용할 때만 check하면 된다.
  - Client JVM check
    - Elasticsearch가 Server JVM으로 실행되는지를 확인한다.
    - JVM은 server에서 동작하는 program을 위한 Server JVM과 client에서 동작하는 program을 위한 Client JVM으로 나뉘어져 있다.
    - Server JVM은 고성능 처리를 위해 최적화 되어 있고, Client JVM은 빠른 실행과 적은 memory 사용에 최적화 되어 있다.
    - Elasticsearch는 고성능으로 동작해야 하기 때문에 Server JVM에서 실행해야한다.
  - Use serial collector check
    - Elasticsearch가 serail collector를 사용하여 GC를 수행하는지 검사한다.
    - JVM을 위한 다양한 garbage collector가 있는데, serial collector는 예전 version의 JVM에서 사용되던 garbage collector로 극히 작은 heap이나 single logical CPU등에 맞는 garbage collector였다.
    - Elasticsearch는 많은 양의 memory와 CPU를 사용하므로 serial collector와는 맞지 않으므로 사용해선 안 된다.
    - Elasticsearch는 G1GC를 사용한다.
  - System call filter check
    - System call filter(seccomp 등)가 설치되어 있고, 활성화 되어 있는지 검사한다.
    - 운영체제들은 보안을 위해 user mod와 kernel mode로 메모리 공간을 분리해서 관리하며, 각 memory 간의 data 공유를 위해 system call을 이용해 통신을 수행한다.
    - Linux의 경우 user mode에서 kernel mode로 접근하는 system call을 제한하는 방식으로 Sandbox를 구현하고 있으며, 임의 코드 공격을 막기 위한 목적으로 System Call Filter를 제공한다.
  - OnError and OnOutOfMemoryError check
    - `-XX:OnError="<명령어>"`, `-XX:OnOutOfMemoryError="<명령어>"` flag가 설정되었는지 확인한다.
    - JVM 실행시 `-XX:OnError="<명령어>"`, `-XX:OnOutOfMemoryError="<명령어>"` flag가 있다.
    - Application에서 error가 발생하거나 OOM error가 발생할 경우 지정한 명령어나 script가 실행되도록 지원하는 flag이다.
    - 다만, Elasticsearch는 system call filter를 사용하는데, 위 두 옵션은 system call filter를 사용하는 application에서는 사용할 수 없다.
    - 따라서 두 flag가 설정되어 있으면 이 단계를 통과할 수 없다.
  - Early-access check
    - JVM의 release version을 사용하고 있는지 확인한다.
    - JDK는 test 목적으로 다음 version의 release snapshot을 미리 제공한다.
    - 다음 버전의 기능을 미리 사용할 수 있다는 장점이 있지만, 안정화 된 것은 아니기에 실제 서비스에 적용하는 것은 부적절하다.
  - All permission check
    - Bootstrap 중에 사용된 보안 정책이 Elasticsearch에게 `java.security.AllPermission`을 주지는 않았는지 확인한다.
    - Java로 작성된 application은 운영체제의 resource를 사용하기 위해 security manager를 통해 필요한 권한을 선택적으로 부여 받는다.
    - 이 중 모든 권한을 부여하는 `java.security.AllPermission` 옵션도 있는데, 이는 매우 위험할 수 있다.
    - 모든 권한을 부여 받은 채로 실행되는 것은 security manager를 비활성화 하는 것과 마찬가지다.
  - Discovery configuration check
    - Bootstrap check가 기본 값으로 설정되어 있지는 않은지 확인한다.
    - 기본적으로 discovery 관련 설정을 하지 않았을 경우 Elasticsearch는 최초로 실행될 때, 같은 host에서 실행 중인 다른 node들을 탐색하고, 수 초 내에 선출 된 master를 찾지 못하면, 발견한 node들로 cluster를 구성한다.
    - 이는 개발 환경에서 별 다른 설정 없이 cluster를 간편하게 구성할 수 있게 해주지만, 운영 환경에서 이렇게 사용하는 것은 위험할 수 있다.
    - `discovery.seed_hosts`, `discovery.seed_providers`, `cluster.inital_master_node` 셋 중 하나라도 설정 되어 있어야한다.







# Elasticsearch thread pool

- Thread Pool의 종류

  > 전체 목록은 [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-threadpool.html) 참고

  - `generic`
    - Background node discovery 등의 일반적인 동작에 사용된다.
    - Thread pool type은 scaling이다.
  - `search`
    - Shard level의 검색 및 count에 사용되며(즉, query phase에 사용), 이 연산은 `search_worker` thread pool에 offload(위임) 된다.
    - Fetch phase를 비롯한 검색과 관련된 작업들에도 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 `int(node.processors*3) / 2) + 1`이고 queue size의 기본값은 1000이다.
  - `search_worker`
    - 같은 shard 내에 있는 여러 segment에 걸쳐서 동시에 실행되는 무거운 count/search 작업에 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 `int(node.processors*3) / 2) + 1`이고 queue size의 기본값은 무제한이다.
  - `search_throttled`
    - count/search/suggest/get 등에 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 1이고, queue_size의 기본값은 100이다.
  - `search_coordination`
    - 검색과 관련된 가벼운 조정에 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 `node.processors / 2`이고 queue size의 기본값은 1000이다.
  - `get`
    - Get을 수행하는 데 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 `int(node.processors*3) / 2) + 1`이고 queue size의 기본값은 1000이다.
  - `analyze`
    - Analyze request를 수행하는 데 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 1, queue size의 기본값은 16이다.
  - `write`
    - 단일 문서의 index/delete/update, ingest processor의 수행, 그리고 bulk를 수행하는 데 사용된다.
    - Thread pool의 type은 fixed이며, 기본값은 `node.processors`이며 queue size의 기본값은 10000이다.
    - Thread pool의 최대 크기는 `1 + node.processors`이다.



- Node가 얼마 만큼의 thread pool을 사용하게 할지 설정할 수 있다.

  - Thread pool 설정은 static 설정으로, 변경하려면 Elasticsearch를 재실행해야 한다.
  - `elasticsearch.yml` 파일을 통해 thread pool의 개수를 조정할 수 있다.

  ```yaml
  thread_pool:
      write:
          size: 30
  ```

  - 아래와 같이 queue_size도 설정할 수 있다.
    - `queue_size`가 가득차게 되면, 이후에 오는 요청은 거부된다.

  ```yaml
  thread_pool:
      write:
          size: 30
          queue_size: 1000
  ```

  - 아래와 같이 scaling도 가능하다.
    - Thread pool의 크기가 dynamic하게 변경된다.
    - 부하와 `core`, `max`에 의해 동적으로 변경된다.
    - `keep_alive`는 thread pool에 있는 thread가 수행하는 작업이 없을 때 얼마나 thread pool에 남아있을지를 설정하는 값이다.

  ```yaml
  thread_pool:
      warmer:
          core: 1
          max: 8
          keep_alive: 2m
  ```

  - Processor의 개수 조정하기
    - Processor의 개수는 자동으로 탐지되며, thread pool 설정은 이 값을 기반으로 자동으로 설정된다.
    - 아래와 같이 processor의 개수를 조정할 수 있다.
    - 단, 실제 processor 이상의 값은 설정할 수 없다.
    - 부동 소수점도 설정 가능하다.
    - 특수한 상황이 아니면 수정하지 않는 것이 권장된다.

  ```yaml
  node.processors: 2
  ```

  - Processor의 개수를 조정하는 것이 유용한 경우
    - 만약 여러 개의 Elasticsearch instance를 하나의 host에서 실행해야 한다고 가정해보자.
    - 단, Elasticsearch가 CPU의 일부만 사용하고 있는 것 처럼 실행하고자 한다.
    - 이 때, `node.processors`를 조정하면 CPU의 일부만 사용하는 것 처럼 실행할 수 있다.



- Thread pool 확인하기

  - 아래와 같이 thread pool을 확인할 수 있다.

  ```http
  GET /_cat/thread_pool
  ```

  - Path parameter
    - 쉼표로 분리된 thread pool의 이름들을 입력하면 해당 thread pool만 확인이 가능하다.

  ```http
  GET /_cat/thread_pool/<thread_pool_A>[,<thread_pool_B>,...]
  ```

  - Query parameter
    - `format`: JSON, YAML 등의 format을 지정할 수 있다.
    - `h`: 특정 column만 지정해서 확인이 가능하다.
    - `help`: `_cat/thread_pool`을 통해 확인할 수 있는 정보들을 확인할 수 있다.
    - `v`: 응답에 head를 포함시킨다.
    - `s`: 정렬한다.
  - `_nodes`를 통해서도 thread pool에 관한 정보를 확인할 수 있다.

  ```http
  GET _nodes/thread_pool
  ```



















