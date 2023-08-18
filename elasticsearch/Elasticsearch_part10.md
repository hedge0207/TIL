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

  ```json
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

  ```json
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

























