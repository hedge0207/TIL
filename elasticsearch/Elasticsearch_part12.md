# 구현

## Exact Match 구현

- Test용 data 색인





- 정확히 동일한 검색어가 정확히 동일한 순서로 나와야 하는 기능을 구현해야 하는 경우 아래의 방법들을 사용할 수 있다.

  - 만일 검색 대상 field의 값이 단어 2~3개로 짧을 경우, keyword field를 대상으로 검색하거나 term query를 사용하여 검색하면 된다.
    - 이 두 방식의 공통점은 analyzing하지 않은 text를 대상으로 검색한다는 점이다.








# Elasticsearch shard allocation

> Part2의 샤드 배치 방식 변경에 넣을 것

- Elasticsearch는 shard가 어떤 노드에 할당될지를 설정할 수 있는 다양한 설정 값들을 제공한다. 
  - 특정 index의 shard가 어떤 node에 할당될지를 설정할 수 있는 [index level](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html)의 설정값들이 있다.
  - [Cluster level](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#cluster-shard-allocation-filtering)에서 어떻게 할당할지를 설정할 수 있는 설정값들이 있다.



## Index level

- Index level에서 shard 할당 설정하기

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html#shard-allocation-filtering

  - Node의 속성값을 기반으로 특정 index의 shard가 어떤 노드에 할당될지를 설정할 수 있다.
    - ILM에서 사용하는 data tier에 따라 shard를 재할당하는 방식도 이 설정값을 기반으로 하는 방식이다.
    - Custom한 속성값을 사용할 수도 있고, Elasticsearch에 내장되어 있는 속성값들을 사용할 수도 있다.
  - Index level에서 shard 할당 방식을 설정한다해도 예상과 다르게 동작할 수 있다.
    - Index level 설정은 cluster level 설정과 결합하여 동작한다.
    - Primary shard와 replica shard가 같은 node에 있을 수 없다는 것 같은 shard 할당의 기본적인 제약을 무시하면서 동작하지는 않는다.



- Custom 속성값 작성하기

  - 각 node의 `elasticsearch.yml` 파일에 아래와 같이 `node.attr.<custom_attribute>: <attribute>` 형식으로 작성한다.

  ```yaml
  node.attr.my_attr: foo
  ```

  - 만일 Docker compose를 사용해 cluster를 구성한다면, 아래와 같이 하면 된다.

  ```yaml
  version: '3.2'
  
  
  services:
    node1:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node1
      environment:
        - node.name=node1
        - node.attr.my_attr=foo
        # ...
  
    node2:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node2
      environment:
        - node.name=node2
        - node.attr.my_attr=bar
        # ...
  
    node3:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.6.0
      container_name: node3
      environment:
        - node.name=node3
        - node.attr.my_attr=baz
        # ...
  ```

  - `_cat/nodeattrs` API를 통해 attribute가 제대로 설정되었는지 확인할 수 있다.

  ```http
  GET _cat/nodeattrs
  ```

  - 그 후 index를 생성할 때 `settings.index.routing.allocation.include.<custom_attribute>`에 attribute를 입력하면, 해당 attribute에 해당하는 node에 할당된다.
    - 아래의 경우 node1이나 2에 할당되게 된다.

  ```json
  // PUT test
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "my_attr":"foo,bar"
                      }
                  }
              }
          }
      }
  }
  ```

  - 만일 `node.attr.<custom_attribute>`에 설정해준 적 없는 값을 줄 경우 어떤 node에도 할당되지 않는다.

  ```json
  // 아래의 경우나
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "qwe":"foo"
                      }
                  }
              }
          }
      }
  }
  
  // 아래의 경우에는 아무 곳에도 할당되지 않는다.
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "my_attr":"qwe"
                      }
                  }
              }
          }
      }
  }
  ```



- 위에서는 include를 사용했지만 include 외에 exclude, require를 사용하는 것도 가능하다.
  - `settings.index.routing.allocation.include.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`이나 `attr2`로 설정된 node 들 중 한 곳에 할당된다.
  - `settings.index.routing.allocation.require.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`과 `attr2`가 모두 설정된 node에만 할당된다.
  - `settings.index.routing.allocation.include.<custom_attribute>:<attr1, attr2>`의 경우 `attr1`과 `attr2`가 모두 설정되지 않은 node에만 할당된다.



- 내장 속성 사용하기

  - 아래의 bulit-in attribute들을 사용할 수 있다.
    - `_name`: node의 이름
    - `_host_ip` : node의 host ip
    - `_publish_ip` : node의 publish ip
    - `_ip`: `_host_ip` 혹은 `_publish_ip`
    - `_host`: node의 hostname
    - `_id`: node의 id
    - `_tier`: node의 data tier
  - 예를 들어 아래 index의 shard는 node1이라는 이름을 가진 node에 할당된다.

  ```json
  {
      "settings": {
          "index":{
              "routing":{
                  "allocation":{
                      "include":{
                          "_name":"node1"
                      }
                  }
              }
          }
      }
  }
  ```



- 아래와 같이 index 생성 후에 변경하는 것도 가능하다.

  - 변경 사항은 바로 반영된다.
  - 그러나 이는 매우 무거운 작업이므로 빈번히 사용하는 것은 권장되지 않는다.

  ```json
  // PUT test/_settings
  {
    "index.routing.allocation.include._name": "node2"
  }
  ```



- Replica shard 역시 설정을 공유한다.

  - 따라서 아래와 같이 attribute의 값을 하나만 줄 경우 replica의 할당이 이루어지지 않을 수 있다.
    - 아래에서는 `_name`라는 built-in attribute의 값으로 `node1`이라는 하나의 값만을 줬다.
    - Primary와 replica는 이 값을 공유하므로 primary와 replica 모두 `node1`에 할당하려 할 것이다.
    - 그런데 `node1`에 primary가 할당되면, replica는 primary와 같은 node에 할당될 수 없으므로, unassigned 상태가 된다.

  ```json
  PUT test
  {
      "settings": {
          "index": {
              "routing": {
                  "allocation": {
                      "include": {
                          "_name": "node1"
                      }
                  }
              }
          }
      }
  }
  ```

  - 이를 `_cluster/allocation/explain` API를 통해 미할당된 이유를 확인해보면 아래와 같다.
    - `node2`와 `node3`의 my_attr 값은 각각 bar와 baz인데 index의 my_attr값은 foo이므로 node2, node3에는 할당할 수 없고, `node1`에는 이미 primary shard가 할당되어 있으므로 할당할 수 없다는 설명을 확인할 수 있다.

  ```json
  // _cluster/allocation/explain
  {
    // ...
    "index": "test",
    // ...
    "primary": false,
    "current_state": "unassigned",
    // ...
    "node_allocation_decisions": [
      {
        // ...
        "node_name": "node3",
        // ...
        "node_attributes": {
          // ...
          "my_attr": "baz",
          // ...
        },
        // ...
        "deciders": [
          {
            "decider": "filter",
            "decision": "NO",
            "explanation": """node does not match index setting [index.routing.allocation.include] filters [_name:"node1"]"""
          }
        ]
      },
      {
        // ...
        "node_name": "node2",
        // ...
        "node_attributes": {
          "my_attr": "bar",
          // ...
        },
        // ...
        "deciders": [
          {
            "decider": "filter",
            "decision": "NO",
            "explanation": """node does not match index setting [index.routing.allocation.include] filters [_name:"node1"]"""
          }
        ]
      },
      {
        // ...
        "node_name": "node1",
        // ...
        "node_attributes": {
          // ...
          "my_attr": "foo"
        },
        // ...
        "deciders": [
          {
            "decider": "same_shard",
            "decision": "NO",
            "explanation": "a copy of this shard is already allocated to this node [[test][0], node[bDGjyx9-RTGnb54PVlGxFQ], [P], s[STARTED], a[id=S1dC8DYGScqaUMt_BJ296Q], failed_attempts[0]]"
          }
        ]
      }
    ]
  }
  ```

  - 따라서 replica shard의 할당도 고려하여 아래와 같이 복수의 attribute 값을 설정해야한다.

  ```json
  PUT test
  {
      "settings": {
          "index": {
              "routing": {
                  "allocation": {
                      "include": {
                          "_name": "node1,node2"
                      }
                  }
              }
          }
      }
  }
  ```



