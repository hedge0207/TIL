# 클러스터 구축하기

- 클러스터 이름 명시하기
  - 엘라스틱서치의 주 설정 파일은 config 디렉터리의 `elasticsearch.yml`이다.
  - `elasticsearch.yml`의 `cluster.name`을 주석 해제 후 변경한다.
    - 이후 엘라스틱서치를 정지하고 재실행한다.
    - 만일 데이터를 색인 한 후 클러스터명을 변경했다면 엘라스틱서치를 재시작했을 때 기존에 색인한 데이터가 사라져 있을 수도 있다.
    - 클러스터명을 다시 되돌리면 색인한 데이터도 다시 돌아온다.



- 자세한 로깅 명시하기
  - 엘라스틱서치의 로그를 봐야 한다면 logs 디렉터리를 확인하면 된다.
    - 엘라스틱서치 로그 엔트리는 세 가지 파일 형태로 구성된다
    - 메인 로그(클러스터명.log 파일): 엘라스틱서치가 동작 중일 때 무슨 일이 일어났는지에 대한 일반적인 정보를 담고 있다.
    - 느린 검색 로그(클러스터명_index_search_slowlog.log 파일): 쿼리가 너무 느리게 실행될 때(쿼리가 0.5초 넘게 걸릴 경우) 엘라스틱서치가 로그를 남기는 곳이다.
    - 느린 색인 로그(클러스터명_index_indexing_slowlog.log 파일): 느린 검색 로그와 유사하지만 기본으로 색인 작업이 0.5초 이상 걸리면 로그를 남긴다.
  - 로깅 옵션을 변경하려면 elasticsearch.yml과 같은 위치에 있는 logginh.yml 파일을 수정하면 된다.



- heap 메모리 설정하기

  - heap 메모리
    - Java로 만든 애플리케이션은 기본적으로 JVM이라는 가상 머신 위에서 동작하는데 OS는 JVM이 사용할 수 있도록 일정 크기의 메모리를 할당해준다.
    - 이 메모리 영역을 힙 메모리라고 부른다.
    - JVM은 힙 메모리 영역을 데이터를 저장하는 용도로 사용한다.
  - 엘라스틱서치는 JAVA 애플리케이션이므로 JVM에서 실행한다.
    - 따라서 ES 역시 heap 메모리를 사용한다.
    - 기본값은 1GB이다.
    - 검색이나 색인 작업이 1GB 이상의 RAM이 필요하면, 작업이 실패하고 로그에서 OOM(Out of Memory) 에러를 보게 될 것이다.
  - 엘라스틱서치에 얼마만큼의 메모리를 사용할지 변경하기 위해 `ES_HEAP_SIZE` 환경변수를 사용할 수 있다.
  
  ```bash
  # heap을 늘린 후 elasticsearch를 실행한다.
  SET ES_HEAP_SIZE=500m & bin\elasticearch.bat
  ```



## elasticsearch.yml

- elaisticsearch.yml
  - ES를 구성하기 위해 기본이 되는 환경 설정 파일.
    - 대부분의 설정이 주석으로 처리되어 있다.
    - 해당 설정에 대한 간략한 설명이 주석으로 제공된다.



- Cluster 영역

  ```txt
  # ---------------------------------- Cluster -----------------------------------
  #
  # Use a descriptive name for your cluster:
  #
  #cluster.name: my-application
  ```

  - 클러스터 전체에 적용 되는 설정
  - 클러스터의 이름을 설정할 수 있다.
  - 클러스터를 구성할 때는 클러스터를 구성할 노드들이 모두 동일한 클러스터 이름을 사용해야 한다.
  - 클러스터 이름을 변경하려면 클러스터 내의 모든 노드를 재시작해야 하기 때문에 처음부터 신중하게 설정해야 한다.
  - 기본값은 주석 처리 상태로 프로세스를 시작하면 elasticsearch라는 이름으로 자동 설정된다.



- Node 영역

  ```txt
  # ------------------------------------ Node ------------------------------------
  #
  # Use a descriptive name for the node:
  #
  #node.name: node-1
  #
  # Add custom attributes to the node:
  #
  #node.attr.rack: r1
  ```

  - 해당 노드에만 적용되는 설정.
  - 노드의 이름을 설정할 수 있으며 노드의 이름은 클러스터 내에서 유일해야 한다.
  - ES에는 `${HOSTNAME}`이라는 노드의 호스트명을 인식할 수 있는 변숫값을 미리 정의해 놓았기에 `node.name: ${HOSTNAME}`과 같이 설정하면 자동으로 노드의 이름이 호스트명과 같아져 다른 노드들과 겹치지 않게 설정할 수 있다.
  - 노드 이름은 운영 중에는 변경이 불가능하며, 변경하려면 노드를 재시작해야 한다.
  - 주석 처리된 상태로 시작하면 ES가 랜덤한 문자열을 만들어 자동으로 설정한다.
  - `node.attr.rack`은 각 노드에 설정할 수 있는 커스텀 항목으로, 사용자가 정의된 rack 값을 통해 HA 구성과 같이 샤드를 분배할 수 있는 기능이다.



- Paths 영역

  ```ㅅㅌㅅ
  # ----------------------------------- Paths ------------------------------------
  #
  # Path to directory where to store the data (separate multiple locations by comma):
  #
  #path.data: /path/to/data
  #
  # Path to log files:
  #
  #path.logs: /path/to/logs
  ```

  - 데이터와 로그의 저장 위치와 관련된 설정이다.
  - Paths 영역은 반드시 설정되어야 하는 값들이기 때문에 elasticsearch.yml의 기본값들 중에서 유일하게 주석 처리가 없는 영역이다. 이 항목들의 설정값이 없으면 애플리케이션이 실행되지 않는다.
  - `path.data`는 노드가 가지고 있을 문서들을 저장할 경로를 설정하는 항목이다. 
    - 색인이 완료된 문서들은 세그먼트 파일로 저장되는데 이 파일들이 위치하게 될 경로이다. 
    - 콤마로 구분하여 여러 개의 경로를 지정할 수 있는데, 이 경우 세그먼트가 두 개의 경로에 나뉘어 저장된다. 
    - 즉, 어떤 문서는 경로1에 저장되고, 어떤 문서는 경로2가 저장된다.
  - `path.logs`는 ES에서 발생하는 로그를 저장할 경로를 설정하는 항목이다.



- Memory 영역

  ```txt
  # ----------------------------------- Memory -----------------------------------
  #
  # Lock the memory on startup:
  #
  #bootstrap.memory_lock: true
  #
  # Make sure that the heap size is set to about half the memory available
  # on the system and that the owner of the process is allowed to use this
  # limit.
  #
  # Elasticsearch performs poorly when the system is swapping the memory.
  ```

  - ES 프로세스에 할당되는 메모리 영역을 어떻게 관리할 것인지 간략하게 설정할 수 있다.
  - `bootstrap.memory_lock: true`는 시스템의 스왑 메모리 영역을 사용하지 않도록 하는 설정이다(ES 권고 사항).
    - 이 설정을 통해 스왑 영역을 사용하지 않으면 성능을 보장할 수 있지만, 시스템의 메모리가 부족한 경우에는 Out Of Memory 에러를 일으켜 노드의 장애로 이어질 수 있다. 
    - 대부분의 경우에는 큰 문제가 없지만, JVM 힙 메모리의 용량이 시스템 메모리 용량의 절반 이상이 된다면 Out Of Memory 에러를 일으킬 수 있기에 주의해야 한다.
    - 또한 이 설정을 사용하기 위해서는 elasticsearch.yml 뿐만 아니라 OS의 /etc/security/limits.conf 파일도 수정해야 한다.



- Network 영역

  ```txt
  # ---------------------------------- Network -----------------------------------
  #
  # Set the bind address to a specific IP (IPv4 or IPv6):
  #
  #network.host: 192.168.0.1
  #
  # Set a custom port for HTTP:
  #
  #http.port: 9200
  #
  # For more information, consult the network module documentation.
  ```

  - ES 애플리케이션이 외부와 통신할 때 사용하게 될 IP 주소를 설정하는 항목.
    - 외부와의 통신뿐 아니라 노드간의 통신에도 Network 영역에서 설정한 값들을 바탕으로 동작한다.
  - `http.port`는 애플리케이션이 사용하게 될 포트 번호를 설정한다.
  - `network.host` 설정은 애플리케이션이 사용하게 될 IP 주소를 설정한다.
    - 다양한 IP를 애플리케이션에 사용할 수 있다.
    - 외부에 노출하지 않고 서버 내부에서만 사용할 수 있는 127.0.0.1과 같은 로컬 IP를 사용할 수도 있고, 외부와의 통신을 가능하게 하기 위해 서버에서 사용하고 있는 IP를 사용할 수도 있다.
    - 만약 두 가지를 모두 사용하고자 한다면 0.0.0.0의 IP 주소를 사용할 수도 있다.
    - 내부적으로 `network.host` 설정은 `network.bind_host`와 `network.publish_host` 두 개로 나눌 수 있다.
    - ``network.host` 를 설정하면 내부적으로는 두 설정 값이 같은 값으로 설정되지만 두 설정을 따로 쓸 수도 있다.
    - `network.bind_host`는 클라이언트의 요청을 처리하기 위한 IP, `network.publish_host`는 클러스터 내부의 노드 간의 통신에 사용하기 위한 IP이다.



- Discovery 영역

  ```txt
  # --------------------------------- Discovery ----------------------------------
  #
  # Pass an initial list of hosts to perform discovery when this node is started:
  # The default list of hosts is ["127.0.0.1", "[::1]"]
  #
  #discovery.seed_hosts: ["host1", "host2"]
  #
  # Bootstrap the cluster using an initial set of master-eligible nodes:
  #
  #cluster.initial_master_nodes: ["node-1", "node-2"]
  #
  # For more information, consult the discovery and cluster formation module documentation.
  ```

  - 노드 간의 클러스터링을 위해 필요한 설정.
  - `discovery.seed_hosts`는 클러스터링을 위한 다른 노드들의 정보를 나열한다.
    - 배열 형식으로 설정할 수 있기 때문에 한 대만 해도 되고, 두 대 이상을 나열해도 된다.
  - `cluster.initial_master_nodes`는 마스터 노드들을 설정한다.



- Gateway 영역

  ```txt
  # ---------------------------------- Gateway -----------------------------------
  #
  # Block initial recovery after a full cluster restart until N nodes are started:
  #
  #gateway.recover_after_nodes: 3
  #
  # For more information, consult the gateway module documentation.
  ```

  - 클러스터 복구와 관련된 내용들을 포함한다.
  - `gateway.recover_after_nodes` 설정은 클러스터 내의 노드를 전부 재시작할 때 최소 몇 개의 노드가 정상적인 상태일 때 복구를 시작할 것인지 설정한다.
    - ES의 버전 업그레이드를 진행하거나 전체 노드 장애로 인해 클러스터 내의 모든 노드를 다시 시작해야 할 때가 있는데 이런 작업을 Full Cluster Restart라고 부러며, 이렇게 재시작한 노드들은 순차적으로 다시 클러스터링을 진행한다.
    - 클러스터링을 시작하면 클러스터 내의 인덱스 데이터들을 복구하기 시작하는데, 이 때 사용자가 지정한 노드의 수만큼 클러스터에 노드들이 복귀하였을 때부터 인덱스 데이터에 대한 복구를 시작할 수 있게 할 수 있는 설정이다.
    - 이 설정은 다시 `gateway.recover_after_master_nodes`와 `gateway.recover_after_data_nodes` 노드로 나뉘어, master와 data role을 부여한 노드의 복귀 수를 별도로 지정할 수 있다.



- Various 영역

  ```txt
  # ---------------------------------- Various -----------------------------------
  #
  # Require explicit names when deleting indices:
  #
  #action.destructive_requires_name: true
  ```

  - `action.destructive_requires_name`는 클러스터에 저장되어 있는 인덱스를 _all이나 wildcard 표현식으로 삭제할 수 없도록 막는 설정이다.
  - 인덱스를 삭제할 때 사용자의 실수에 의해 전체 인덱스나 많은 인덱스가 한 번에 삭제되지 못하게 하는 대표적인 방법이다.



- 노드의 역할 정의

  - 하나의 노드는 복수의 역할을 수행할 수 있다.
    - 어떤 역할을 수행하게 할지 설정이 가능하다.
    - 기본 값은 전부 TRUE로 되어 있어 기본적으로 하나의 노드는 모든 역할을 수행할 수 있도록 설정 되어있다.

  | 노드 역할       | 항목        | 기본 설정값 |
  | --------------- | ----------- | ----------- |
  | 마스터 노드     | node.master | TRUE        |
  | 데이터 노드     | node.data   | TRUE        |
  | 인제스트 노드   | node.ingest | TRUE        |
  | 코디네이트 노드 | 설정 없음   | TRUE        |

  - 마스터 노드로만 사용하도록 설정하기
    - 아래와 같이 설정 된 노드는 마스터 노드가 될 수 있는 자격을 부여받은 노드로 클러스터에 합류한다.
    - 마스터 노드에 장애가 발생해서 클러스터로부터 분리될 경우, 마스터가 될 수 있는 자격을 부여받은 노드들 중 하나가 새로운 마스터가 된다.

  ```txt
  node.master: true
  node.data: false
  node.ingest: false
  ```

  - 세 값을 모두 false로 줄 경우
    - 코디네이트 노드가 된다.
    - 코디네이트 노드를 별도로 분리하는 이유는 사용자의 데이터 노드 중 한 대가 코디네이트 노드의 역할과 데이터 노드의 역할을 동시에 할 경우 해당 노드의 사용량이 높아질 수 있기 때문이다.
  - 향후 확장성을 위해 마스터 노드와 데이터 노드는 가급적 분리해서 구축하는 것이 좋다.





## jvm.options

- jvm.options
  - ES는 자바로 만들어진 애플리케이션이기에 힙 메모리, GC 방식과 같은 JVM 관련 설정이 필요하다.
  - 이 설정은 ES 애플리케이션의 성능에 결정적 역할을 하기 때문에 어떤 항목들을 설정할 수 있는지 알고 이해해 두어야 한다.



- JVM에서 사용할 힙 메모리 크기 설정

  ```txt
  ################################################################
  ## IMPORTANT: JVM heap size
  ################################################################
  ##
  (...중략...)
  ##
  ## -Xms4g
  ## -Xmx4g
  ```

  - JVM은 데이터를 저장하기 위해 힙 메모리라는 공간을 필요로 한다.
  - `Xms`로 최솟값을, `Xmx`로 최댓값을 설정한다.
    - 둘을 같은 값으로 설정하지 않으면 실행 시에는 Xms에 설정된 최솟값 정도의 크기만 확보했다가 요청이 늘어나서 더 많은 힙 메모리가 필요해지는 경우 Xmx에 설정된 최댓값 크기까지 메모리를 요청하게 된다.
    - 중간에 메모리의 요청이 추가로 일어나면 성능이 낮아질 수밖에 없기 때문에 두 값을 같은 값으로 설정하도록 권고한다.



- GC(Garage Collection) 관련 설정

  ```txt
  ## GC configuration
  8-13:-XX:+UseConcMarkSweepGC
  8-13:-XX:CMSInitiatingOccupancyFraction=75
  8-13:-XX:+UseCMSInitiatingOccupancyOnly
  
  ## G1GC Configuration
  # NOTE: G1 GC is only supported on JDK version 10 or later
  # to use G1GC, uncomment the next two lines and update the version on the
  # following three lines to your version of the JDK
  # 10-13:-XX:-UseConcMarkSweepGC
  # 10-13:-XX:-UseCMSInitiatingOccupancyOnly
  14-:-XX:+UseG1GC
  ```

  - `8-13:-XX:+UseConcMarkSweepGC`
    - CMS라는 GC 방식을 사용한다는 설정이다.
    - CMS는 ES가 기본으로 사용하는 GC 방식이며 특별한 경우가 아니라면 다른 방식으로 바꾸지 않아도 된다.
  - `8-13:-XX:CMSInitiatingOccupancyFraction=75`
    - CMS GC를 사용할 경우 힙 메모리 사용량이 어느 정도가 되면 old GC를 수행할 것인지 설정한다.
    - 75%가 기본값으로, 확보된 힙 메모리의 사용량이 75%가 되면 old GC를 진행한다는 의미이다.
    - old GC가 발생하면 **Stop-the-world** 현상에 의해 ES 프로세스가 잠시 응답 불가 상태가 되기 때문에 주의해서 설정해야 한다.
    - 이 값을 낮게 설정하면 old GC가 자주 발생하고, 높게 설정하면 한 번의 old GC 수행 시간이 길어진다.
  - `8-13:-XX:+UseCMSInitiatingOccupancyOnly`
    - old GC를 수행할 때, GC 통계 데이터를 근거로 하지 않고 ,`8-13:-XX:CMSInitiatingOccupancyFraction=75`의 설정만을 기준으로 old GC를 수행한다는 의미이다.
  - `G1GC Configuration`
    - CMS GC가 아닌 G1 GC에 대한 설정이다.
    - G1 GC를 적용하면 다양한 이슈가 발생할 수 있기 때문에 반드시 테스트해보고 진행해야 한다.



- 힙 메모리와 GC 방식 설정
  - 힙 메모리와 GC 방식에 대한 설정은 성능에 많은 영향을 주기 때문에 정확하게 이해하고 수정해야 한다.
    - 특히 힙 메모리 설정과 관련해서 ES 공식 문서에서는 가능한 한 32GB를 넘지 않게 설정할 것, 전체 메모리의 절반 정도를 힙 메모리로 설정할 것 등을 권고하고 있다.
  - 힙 메모리가 가능한 32GB를 넘지 않도록 권고하는 이유
    - JVM은 연산을 위한 데이터들을 저장하기 위한 공간으로 힙 메모리를 사용한다.
    - 이 때 힙 메모리에 저장되는 데이터들을 오브젝트라 부르고, 이 오브젝트에 접근하기 위한 메모리상의 주소를 OOP(Ordinaty Object Pointer)라는 구조체에 저장한다.
    - 각각의 OOP는 시스템 아키텍처에 따라 32 비트 혹은 64 비트의 주소 공간을 가리킬 수 있는데, 32비트라면 최대 4GB까지의 주소 공간을 가리킬 수 있는 반면 64 비트는 이론상 16EB까지의 주소 공간을 가리킬 수 있다.
    - 하지만 64 비트의 경우 32비트보다 더 넓은 주소 공간을 가리키기 위해 더 많은 연산과 더 많은 메모리 공간을 필요로 하기 때문에 성능 측면에서는 32 비트보다 떨어질 수밖에 없다.
    - 그래서 JVM은 시스템 아키텍처가 64 비트라고 하더라도 확보해야 할 힙 메모리 영역이 4GB보다 작다면 32 비트 기반의 OOP를 사용해서 성능을 확보한다.
    - 문제는 힙 메모리 영역이 4GB보다 클 경우에 발생한다. 32비트의 주소 공간을 사용하는 OOP로는 4GB 이상의 메모리 영역을 가리킬 수 없기 때문이다.
    - 그렇다고 64비트 기반의 OOP를 사용하게 되면 급작스럽게 성능 저하가 발생할 수 있기 때문에 JVM은 Compressed OOP를 통해 32비트 기반의 OOP를 사용하되 4GB 이상의 영역을 가리킬 수 있도록 구현했다.
    - Compressed OOP는 Native OOP에 비해 8배 더 많은 주소 공간을 표시할 수 있게 되고, 이에 따라 기존 4GB에서 32GB까지 힙 메모리 영역이 증가한다.
    - 그렇기에 힙 메모리 할당을 32GB 미만으로 하게 되면 32비트 기반의 OOP를 계속 사용할 수 있게 되고 성능 저하를 피할 수 있게 된다.
  - 전체 메모리의 절반 정로를 힙 메모리로 할당하도록 권고하는 이유
    - ES는 색인된 데이터를 세그먼트라는 물리적인 파일로 저장한다.
    - 파일로 저장하기 때문에 I/O가 발생할 수밖에 없는 구조이다.
    - I/O 작업은 시스템 전체로 봤을 때 가장 느린 작업이기 때문에 빈번한 I/O 작업이 발생한다면 시스템 성능이 떨어진다.
    - OS에서는 이런 성능 저하를 막기 위해 파일의 모든 내용을 메모리에 저장해 놓는 페이지 캐시 기법을 사용한다.
    - 하지만 페이지 캐시는 애플리케이션들이 사용하지 않는 미사용 메모리를 활용해서 동작하기 때문에 페이지 캐시를 최대한 활용하기 위해서는 애플리케이션이 사용하는 메모리를 줄이는 것이 좋다.
    - 특히 ES와 같이 빈번한 I/O 작업이 발생해야 하는 경우 가급적 많은 메모리를 페이지 캐시로 활용해서 I/O 작업이 모두 메모리에서 끝날 수 있도록 하는 것이 성능 확보에 도움이 된다.
    - 이런 이유로 인해 공식 문서에서는 물리 메모리의 절반 정도를 힙 메모리로 할당할 것을 권고한다.
    - 굳이 많은 양의 힙 메모리가 필요하지 않다면 절반 이하로 설정해도 된다.





# 클러스터 운영하기

- 클러스터 상태 확인하기

  - 아래 명령어를 통해 현재 클러스터 정보를 확인할 수 있다.
    - cat API는 JSON을 반환하지 않는다.

  ```bash
  $ curl 'localhost:9200/_cat/shards?v'
  ```

  - 새로운 노드를 추가한 적이 없으므로 오직 하나의 노드만 존재한다.
    - 샤드는 primary 샤드와 replica 샤드가 존재하는데 노드는 한 개만 존재하므로 replica 샤드는 할당되지 못한 상태이다(UNASSIGNED).
    - 미할당 레플리카는 클러스터의 상태를 yellow로 만든다.
    - yellow는 primary 샤드들은 할당되었으나 모든 레플리카가 할당된 것은 아니라는 것을 의미한다.
    - primary 샤드가 할당되지 않았다면, 클러스터는 red 상태가 된다.
    - 모든 샤드가 할당되었다면 클러스터는 green이 된다.



- 두 번째 노드 생성하기
  - 방법
    - `elasticsearch.yml` 파일에 `node.max_local_storage_nodes: 생성할 노드 수` 코드를 추가한다(`:`와 생성할 노드 수 사이에 공백이 있어야 한다).
    - 엘라스틱서치가 실행 중인 상태에서 다른 터미널에서 엘라스틱서치를 실행한다.
    - 이렇게 하면 같은 머신에 다른 ES 인스턴스를 시작하게 된다.
    - 현업에서는 추가적인 프로세싱 파워의 이득을 얻기 위해 다른 머신에 새로운 노드를 시작한다.
    - 혹은 그냥 엘라스틱서치 폴더를 복사해서 각자 실행시키면 된다.
  - 두 번째 노드는 멀티캐스트로 첫 번째 노드를 찾아서 클러스터에 합류하게 된다.
    - 첫 번째 노드는 클러스터의 마스터 노드다.
    - 즉 어떤 노드가 클러스터에 있고 샤드가 어디에 있는지 같은 정보를 유지하는 역할을 하는데, 이 정보를 클러스터 상태라고 부르고 다른 노드에도 복제 된다.
    - 마스터 노드가 내려가면 다른 노드가 마스터 노드가 된다.
  - 이제 추가한 노드에 레플리카가 할당되어 클러스터가 green으로 변경된 것을 확인 가능하다.



## 버전 업그레이드

- ES는 새로운 버전이 빠르게 공개된다.
  - 새로운 버전이 나올 때마다 새로운 기능들이 추가되고, 이전 버전의 버그도 수정되기 때문에 운영중인 ES의 버전에 치명적인 버그가 포함되어 있다거나, 꼭 필요한 새로운 기능이 추가되엇다면 운영 중인 클러스터의 버전을 업그레이드해야 한다.
  - 또한 꼭 업그레이드 할 때 뿐만 아니라, elasticsearch.yml 파일이나 jvm.options 파일을 수정할 때에도 재시작을 해줘야 한다.



- ES의 버전 업그레이드 방법은 두 가지가 있다.
  - Full Cluster Restart: 모든 노드를 동시에 재시작하는 방식, 다운 타임이 발생하지만 빠르게 버전을 업그레이드할 수 있다.
  - Rolling Restart: 노드를 순차적으로 한 대씩 재시작하는 방식, 다운타임은 없지만 노드의 개수에 따라서 업그레이드에 소요되는 시간이 길어질 수 있다.



- Rolling Restart의 순서

  - 클러스터 내 샤드 할당 기능 비활성화
    - ES 클러스터는 특정 노드가 정상적으로 동작하지 않을 경우 문제 노드의 샤드들을 다른 노드로 재할당한다.
    - 업데이트를 위해서는 노드가 잠시 동작을 멈추면서 클러스터에서 제외되는데, 그러면 클러스터가 업데이트 하려는 노드의 샤드들을 다른 노드로 재할당하게 된다.
    - 업데이트를 위해 노드 내부의 샤드들을 다른 노드로 이동시키는 것은 네트워크 비용이나 디스크 I/O 비용 측면에서 큰 낭비다.
    - 따라서 노드가 멈추더라도 재할당을 하지 않도록 설정을 변경해줘야 한다.
    - 아래와 같이 설정을 완료하고 노드를 정지하면, 정지된 노드의 샤드들은 다른 샤드로 재할당되지 않고 unassigned 상태가 된다.

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.allocation.enable":"none"
  	}
  }'
  ```

  - 프라이머리 샤드와 레플리카 샤드 데이터 동기화
    - 프라이머리 샤드와 레플리카 샤드 간의 데이터를 동일하게 맞춰줘야 한다.
    - 두 샤드가 가지고 있는 문서가 완벽히 동일해야 클러스터에서 노드가 제외되더라도 데이터의 정합성을 보장할 수 있기 때문이다.

  ```bash
  $ curl -XPUT "localhost:9200/_flush/synced?pretty"
  ```

  - 노드 한 대 버전 업그레이드 이후 클러스터 합류 확인
    - 업그레이드를 위해 노드가 정지되면, 클러스터에서 제외된다.
    - 업그레이드가 완료된 후 노드가 다시 클러스터에 합류하는지 확인한다.
  - 클러스터 내 샤드 할당 기능 활성화
    - 샤드 할당 기능을 활성화하여 unassigned 상태인 샤드들이 업그레이드한 노드에 할당될 수 있도록 한다.
    - null은 기본 설정으로 되돌리겠다는 의미이다.

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.allocation.enable":null
  	}
  }'
  ```

  - 클러스터 그린 상태(모든 샤드가 할당 된 상태) 확인
  - 위 과정 반복



## 샤드 배치 방식 변경

- 샤드의 배치 방식을 변경해야 하는 경우
  - ES는 기본적으로 자동으로 샤드를 배치한다.
  - 그러나 아래 예시와 같은 경우 배치 방식을 변경해야 한다.
    - 특정 노드에 장애가 발생하여 파생된 unassigned 샤드들에 대한 재할당 작업이 5회 이상 실패
    - 일정 기간이 지난 오래된 인덱스의 샤드를 특정 노드에 강제로 배치해야 할 경우



- reroute

  - 샤드 하나하나를 특정 노드에 배치할 때 사용하는 방법
  - 샤드 이동, 샤드 이동 취소, 레플리카 샤드의 특정 노드 할당이 가능하다.
  - 샤드 이동은 인덱스 내에 정상적으로 운영 중인 샤드를 다른 노드로 이동할 때 사용한다.
  - ES는 노드마다 균등하게 샤드를 배치하기에 수작업으로 샤드를 하나 이동하면 균형을 맞추기 위해 자동으로 다른 샤드 하나를 이동시킨다.
  - 샤드 이동(move) 명령

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/reroute?pretty" -H 'Content-type:application/json' -d '
  {
  	# list 형태로, 여러 명령을 동시에 실행하는 것이 가능하다.
  	"command":[
  		{
              "move":{
                  "index":"인덱스명",
                  "shard":샤드 번호,
                  "from_node":"이동할 샤드가 현재 배치되어 있는 노드명",
                  "to_node":"이동할 샤드가 배치될 노드명"
  		    }
  	    }
  	]
  }'
  ```

  - 이동 취소(cancel) 명령

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/reroute?pretty" -H 'Content-type:application/json' -d '
  {
  	"command":[
  		{
              "cancel":{
                  "index":"인덱스명",  # 이동 작업을 취소할 대상 샤드의 인덱스명
                  "shard":샤드 번호,	 # 이동 작업을 취소할 대상 샤드의 번호
                  "node":"이동 작읍을 취소할 대상 샤드가 포함된 노드의 이름",
  		    }
  	    }
  	]
  }'
  ```

  - 레플리카 샤드 배치(allocate_replica) 명령
    - 이미 배치된 레플리카 샤드에는 사용할 수 없다(unassigned 상태인 레플리카 샤드에만 사용이 가능하다).

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/reroute?pretty" -H 'Content-type:application/json' -d '
  {
  	"command":[
  		{
              "allocate_replica":{
                  "index":"인덱스명",  # 레플리카 샤드를 배치할 대상 샤드가 속한 인덱스 이름
                  "shard":샤드 번호,	 # 레플리카 샤드를 배치할 대상 샤드의 번호
                  "node":"레플리카 샤드를 배치할 노드의 이름",
  		    }
  	    }
  	]
  }'
  ```

  - 미할당 상태인 모든 샤드 할당하기
    - 샤드 배치가 모두 자동으로 이루어진다.
    - 특정 노드에 배치하고자 한다면 `allocate_replica` 명령을 사용하여 하나씩 배치해야 한다.

  ```bash
  $ curl -XPOST "localhost:9200/_cluster/reroute?retry_failed?pretty" -H 'Content-type:application/json'
  ```



- allocation

  - 클러스터 전체에 적용되는 재배치 방식을 설정.
    - reroute는 인덱스의 특정 샤드를 대상으로 하는 재배치
    - 위에서 살펴본 Rolling Restart 방식에서 일시적으로 모든 샤드의 재할당을 중지하는 것이 allocation을 활용한 것이다.

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		# 옵션에 아래 5개 중 하나를 넣으면 된다.
  		# all, primaries, new_primaries, none, null
  		"cluster.routing.allocation.enable":"옵션" # null은 예외적으로 따옴표로 감싸지 않는다.
  	}
  }'
  ```

  - all(기본값)
    - 모든 샤드의 배치를 허용하며 노드 간 샤드 배치가 진행된다.
    - 클러스터에 새로운 노드가 증설되면 기존 노드들이 가지고 있던 샤드들을 프라이머리와 레플리카 구분 없이 나눠준다.
    - 노드 한 대가 클러스터에서 제외됐을 경우, 프라이머리와 레플리카 샤드를 남은 노드에 배치한다.
  - primaries
    - all과 유사하지만 배치의 대상이 되는 샤드가 프라이머리 샤드로 한정된다.
    - 레플리카 샤드는 한번 배차된 이후에는 노드가 증설되더라도 재배치되지 않는다.
  - new_primaries
    - 새롭게 추가 되는 인덱스의 프라이머리 샤드만 재배치한다.
    - 새롭게 투입된 노드들에 기존 인덱스들의 샤드가 재배치되지 않으며, 투입 이후 새롭게 추가되는 인덱스의 프라이머리 샤드만 배치된다.
  - none
    - 모든 샤드의 배치 작업을 비활성화 시킨다.
  - null
    - 옵션을 초깃값으로 재설정할 때 사용한다.
    - 주로 none 옵션으로 배치 작업을 비활성화했을 때 이를 다시 활성화시키는 용도로 사용한다.
  - 장애 상황에서 샤드를 복구할 때 노드당 몇 개의 샤드를 동시에 복구할 것인지 설정할 수도 있다.
    - 기본값은 2이다.
    - 너무 많은 샤드를 동시에 복구하면 노드에 부하를 줄 수 있기 떄문에 클러스터의 성능을 고려해서 설정하는 것이 좋다.

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.allocation.node_concurrent_recoveries":샤드의 수
  	}
  }'
  ```



- rebalance

  - 클러스터 내의 샤드가 배치된 후에 특정 노드에 샤드가 많다거나 배치가 고르지 않을 때의 동작과 관련된 설정이다.
    - allocation은 노드가 증설되거나 클러스터에서 노드가 이탈했을 때의 동작과 관련된 설정이다.

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.rebalance.enable":"옵션"
  	}
  }'
  ```

  - 옵션

  | 옵션      | 설명                                             |
  | --------- | ------------------------------------------------ |
  | all       | 프라이머리 샤드와 레플리카 샤드 전부 재배치 허용 |
  | primaries | 프라이머리 샤드만 재배치 허용                    |
  | replicas  | 레플리카 샤드만 재배치 허용                      |
  | none      | 모든 샤드의 재배치 비활성화                      |
  | null      | 설정을 초기화하여 Default인 all로 설정           |

  - 아무때나 샤드 재배치가 일어나는 것이 아니라 `cluseter.routing.allocation.disk.threshold_enabled` 설정(기본값은 true)에 의해 클러스터 내의 노드 중 한 대 이상의 디스크 사용량이 아래와 같이 설정한 임계치에 도달했을 때 동작하게 된다.
    - `cluster.routing.allocation.disk.watermark.low`: 특정 노드에서 임계치가 넘어가면 해당 노드에 더 이상 할당하지 않음. 새롭게 생성된 인덱스에 대해서는 적용되지 않음(기본값은 85%)
    - `cluster.routing.allocation.disk.watermark.high`: 임계치를 넘어선 노드를 대상으로 즉시 샤드 재할당 진행. 새로 생성된 인덱스에도 적용됨(기본값은 90%)
    - `cluster.routing.allocation.disk.watermark.flood_stage`: 전체 노드가 임계치를 넘어서면 인덱스를 read only 모드로 변경(기본값은 95%)
    - `cluster.info.update.interval`: 임계치 설정을 체크할 주기(기본값은 30s)

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.allocation.disk.watermark.low":"n%",
  		"cluster.routing.allocation.disk.watermark.high":"n%",
  		"cluster.routing.allocation.disk.watermark.flood_stage":"n%",
  		"cluster.info.update.interval":"ns" # ns 또는 nm
  	}
  }'
  ```

  - read only 모드가 되었을 때, 쓰기 작업이 가능하도록 변경해주는 curl
    - 인덱스 단위로도 읽기 전용 모드를 해제 가능하다.
    - 그러나 읽기 전용 모드는 flood_stage에 의해 다수의 인덱스에 설정되므로 가능한 아래 코드와 같이 `_all`을 통해 모든 인덱스에 동시 적용하는 것이 좋다.
  
  ```bash
  $ curl -XPUT "localhost:9200/_all/_settings?pretty" -H 'Content-type:application/json' -d'{
  "index.block.read_only_allow_delete":null
  }'
  ```



- filtering

  - 특정 조건에 맞는 샤드를 특정 노드에 배치하는 작업.
  - 조건
    - `"cluster.routing.allocation.include.[속성]":"[값]"`: 설정이 정의된 하나 이상의 노드에 샤드를 할당.
    - `"cluster.routing.allocation.require.[속성]":"[값]"`: 설정이 정의된 노드에만 샤드를 할당.
    - `"cluster.routing.allocation.exclude.[속성]":"[값]"`: 설정이 정의된 노드로부터 샤드를 제외. Rolling Restart시 안정성을 위해 작업 대상 노드의 샤드를 강제로 다른 노드로 옮기는 용도로 주로 사용한다. 만일 제외하려는 설정이 클러스터의 안정성을 유지하기 위한 최소한의 룰에 위배된다면 제외되지 않는다(예를 들어 3개의 노드 중 2개의 노드를 제외하여 모든 샤드가 남은 하나의 노드에만 할당되는 경우 제외되지 않는다).
  - 속성

  | 속성  | 설명                                            |
  | ----- | ----------------------------------------------- |
  | _name | 노드의 이름(`,`로 구분하여 여러 노드 설정 가능) |
  | _ip   | 노드의 IP                                       |
  | _host | 노드의 호스트명                                 |

  - 예시
    - node02 라는 이름의 노드를 샤드 배치에서 제외하는 curl

  ```bash
  $ curl -XPUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d '
  {
  	"persistent":{
  		"cluster.routing.allocation.exclude._name":"node02"
  	}
  }'
  ```



## 클러스터와 인덱스의 설정 변경

### 클러스터 설정 변경

- 클러스터 API를 통해 클러스터 설정을 변경할 수 있다.

  - `_cluster/settings`와 같이 `_cluster`가 붙은 API를 클러스터 API라 부른다.
  - 현재 클러스터에 적용된 설정 확인

  ```bash
  $ curl -XGET "localhost:9200/_cluster/settings?pretty"
  ```

  - 응답

  ```json
  {
    "persistent" : { },
    "transient" : { }
  }
  ```



- cluster 설정
  - persistent
    - 영구히 적용되는 설정.
    - 아무 값이 없을 경우 항목의 기본값이 자동으로 적용된다.
    - 클러스터를 재시작해도 유지된다.
  - transient
    - 클러스터가 운영 중인 동안에만 적용되는 설정.
    - 아무 값이 없을 경우 항목의 기본값이 자동으로 적용된다.
    - 클러스터를 재시작하면 초기화된다.

  - elasticsearch.yml
    - 기본적인 설정은 elasticsearch.yml에도 설정할 수 있다. 
    - 각기 다른 설정을 적용할 경우 우선순위는 `transient > persistent > elasticsearch.yml` 순이다.
    - 또한 persistent, transient와 달리 elasticsearch.yml에서는 클러스터 전체가 아닌 노드별로 다르게 설정할 수 있는 항목들을 설정 가능하다.
    - 따라서 노드별로 다르게 설정해야 하거나 변경되지 않고 클러스터에 공통으로 필요한 사항은 elasticsearch.yml에 설정하는 것이 좋다.



- 클러스터 설정 예시

  - persistent는 elasticsearch.yml 보다 우선순위가 높기 때문에 elasticsearch.yml 파일에서 `discovery.zen.minimum_master_nodes` 설정을 2로 줬다고 하더라도 아래 요청을 보내면 동적으로 변경이 가능하다.

  ```bash
  $ curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-type:application/json' -d'
  {
  	"persistent":{
  		"cluster.routing.allocation.disk.watermark.low":"90%",
  		"discovery.zen.minimum_master_nodes":1
  	},
  	"transient":{
  		"cluster.routing.allocation.enable":"primaries"
  	}
  }
  ```



- 클러스터의 미할당 샤드를 확인하는 클러스터 API

  - `explain`을 사용한다.
    - 더 자세한 내용은 master node의 로그를 확인해보면 된다.

  ```bash
  $ curl -XGET _cluster/allocation/explain?pretty
  ```

  - 위에서 살펴본 샤드 reroute의 `retry_failed` 옵션과 함께 유용하게 사요된다.

  

### 인덱스 설정 변경

- 인덱스 API를 사용한다.

  - 아래와 같이 `인덱스명/_settings` endpoint를 사용하여 조회 및 수정이 가능하다.
    - `인덱스명`에 `_all` 지시자를 넣으면 모든 인덱스를 대상으로 수정이 가능하다.
    - 와일드카드와 같은 정규식을 사용하는 것도 가능하다(`user*`를 넣으면 user로 시작하는 모든 인덱스가 대상이 된다.)
  - 조회

  ```bash
  $ -XGET "localhost:9200/인덱스명/_settings"
  ```

  - 수정
    - 아래 curl은 레플리카 샤드의 수를 0개로 줄이는 요청이다.

  ```bash
  $ -XPUT "localhost:9200/인덱스명/_settings" -H 'Content-type:application/json' -d'
  {
  	"index.number_of_replicas":0
  }
  ```



- 자주 사용되는 인덱스 API

  - open/close
    - 인덱스를 사용 가능/불가능한 상태로 만드는 API
    - close 상태일 경우 색인과 검색이 모두 불가능해진다.

  ```bash
  # close
  $ curl -XPOST "localhost:9200/인덱스명/_close" -H 'Content-type:application/json' -d'
  
  # open
  $ curl -XPOST "localhost:9200/인덱스명/_open" -H 'Content-type:application/json' -d'
  ```

  - aliases
    - 인덱스에 별칭을 부여하는 API
    - 인덱스의 이름뿐만 아니라 별칭으로도 인덱스에 접근할 수 있게 된다.
    - 배열에 넣거나 패턴 매칭을 통해 여러 인덱스에 하나의 alias를 설정할 수 있다.
    - 주의할 점은 단일 인덱스에 설정된 alias는 별칭을 통해 색인과 검색이 모두 가능하지만, 여러 인덱스에 설정된 하나의 alias의 경우 별칭을 통해서는 검색만 가능하다는 점이다.
    - 또한 여러 개의 인덱스에 하나의 alias를 설정한 경우 인덱스가 하나라도 close 상태라면 alias를 통핸 검색 요청이 불가능해진다.

  ```bash
  # 하나의 인덱스에만 alias를 설정
  $ curl -XPOST "localhost:9200/_aliases" -H 'Content-type:application/json' -d'
  {
  	"actions":[
  		# alias를 설정할 인덱스와 alias의 이름을 입력한다.
  		# remove를 통해 제거가 가능하다.
  		{"add":{"index":"test1","alias":"alias1"}}
  	]
  }
  
  # 여러 개의 인덱스에 alias를 설정
  $ curl -XPOST "localhost:9200/_aliases" -H 'Content-type:application/json' -d'
  {
  	"actions":[
  		{"add":{"index":["test2","test3"],"alias":"alias2"}}
  		# 패턴 매칭 사용(test로 시작하는 모든 인덱스에 적용)
  		# {"add":{"index":["test*"],"alias":"alias2"}}
  	]
  }
  ```

  - rollover
    - 인덱스에 특정 조건을 설정하여 해당 조건을 만족하면 인덱스를 새로 만들고, 새롭게 생성된 인덱스로 요청을 받는 API
    - aliases API를 통해 별칭 설정이 반드시 필요한  API이다.
    - 예를 들어 index01이라는 인덱스에 aliases API로 user라는 별칭을 붙이고 user를 통해 인덱스에 접근하고 있었다고 가정했을 때, index01 인덱스에 많은 문서가 색인되는 등의 이유로 인덱스를 하나 더 생성해야 한다면 rollover API를 통해서 index02라는 인덱스를 생성하고 user라는 별칭이 가리키는 인덱스를 index02로 변경한다. 이렇게 함으로써 사용자는 user라는 별칭을 계속 사용하여 색인과 검색이 가능해진다.
    - `dry_run` 옵션을 통해 모의 실행이 가능하다. 이 경우 실제 변경이 적용되지는 않고, 변경이 적용되면 어떻게 되는지를 보여준다.

  ```bash
  # index01이라는 인덱스에 user라는 별칭 설정
  $ curl -XPOST "localhost:9200/index01/_aliases" -H 'Content-type:application/json' -d'
  {
  	"aliases":{"user":{}}
  }
  
  # rollover API를 호출하고 조건을 설정한다.
  $ curl -XPOST "localhost:9200/user/_rollover?pretty" -H 'Content-type:application/json' -d'
  {
  	# 생성된 지 7일이 지나거나, 문서의 수가 2개 이상이거나, 인덱스의 크기(프라이머리 샤드 기준)가 5GB가 넘으면 롤오버한다.
  	"contitions":{
  		"max_age":"7d",
  		"max_docs":2,
  		"max_size":"5gb"
  	}
  }
  
  # 새로 생성될 index의 이름(new_index)을 아래와 같이 직접 지정해주는 것이 가능하다.
  $ curl -XPOST "localhost:9200/user/_rollover/new_index?pretty" -H 'Content-type:application/json' -d'
  {
  	...
  }
  
  # dry_run 적용
  $ curl -XPOST "localhost:9200/user/_rollover?dry_run&pretty" -H 'Content-type:application/json' -d'
  {
  	...
  }
  ```

  - refresh API
    - `refresh_interval` 설정은 메모리 버퍼 캐시에 있는 문서들을 세그먼트로 저장해주는 주기를 의미한다.
    - refresh API는 `refresh_interval`에서 설정한 주기를 기다리지 않고 바로 메모리 버퍼 캐시에 있는 문서들을 세그먼트로 저장해준다.

  ```bash
  $ curl -XPOST "localhost:9200/인덱스명/_refresh?pretty" -H 'Content-type:application/json'
  ```

  - forcemerge API
    - 샤드를 구성하는 세그먼트를 강제로 병합하는 API.
    - `max_num_segments` 옵션으로 샤드 내 세그먼트들을 몇 개의 세그먼트로 병합할 것인지 설정한다.
    - 병합의 대상이 되는 세그먼트들은 샤드의 개수에 비례해서 증가하고 떄어 따라서 많은 양의 디스크 I/O 작업을 일으킨다.
    - 따라서 너무 많은 세그먼트를 대상으로 forcemerge API 작업을 진행하면 성능 저하를 일으킬 수 있다.
    - 또한 계속 문서의 색인이 일어나고 있는 인덱스라면 세그먼트에 대한 변경 작업이 계속되기 때문에 forcemerge 작업을 하지 않는 것이 좋다.

  ```bash
  $ curl -XPOST "localhost:9200/인덱스명/_forcemerge?max_num_segments=10&pretty" -H 'Content-type:application/json'
  ```

  - reindex API
    - 인덱스를 복제하는 API
    - 인덱스의 analyzer 변경이나 클러스터의 마이그레이션 등 인덱스를 마이그레이션해야 할 경우 사용한다.
    - 클러스터 내부가 아닌 클러스터 사이에 데이터 마이그레이션에도 사용할 수 있다.
    - 목적지 클러스터의 elasticsearch.yml 파일에서 `reindex.remote.whitelist:"호스트:9200,127.0.0.*:9200`과 같이 원본 클러스터의 주소를 whitelist에 설정해주면 되는데, 도메인이나 IP를 기준으로 예시처럼 와일드카드 패턴 매칭도 지원한다.

  ```bash
  # 클러스태 내 reindex
  $ curl -XPOST "localhost:9200/인덱스명/_reindex?pretty" -H 'Content-type:application/json' -d'
  {
  	"source":{
  		"index":"test"	# 원본 인덱스
  	},
  	"dest":{
  		"index":"new_index"	# 목적지 인덱스
  	}
  }
  
  # 클러스터 간 reindex(목적지 클러스터에서 수행)
  $ curl -XPOST "localhost:9200/인덱스명/_reindex?pretty" -H 'Content-type:application/json' -d'
  {
  	"source":{
  		"remote":{
  			"host":"http://example/com:9200"
  		},
  		"index":"test"
  	},
  	"dest":{
  		"index":"dest_test"	# 목적지 인덱스
  	}
  }
  ```

  

## 템플릿 활용하기

- 템플릿 API

  - 엘라스틱서치는 템플릿 API를 통해 특정 패턴의 이름을 가진 인덱스에 설정이 자동 반영되도록 하는 인터페이스를 제공한다.
  - 템플릿 API를 통해 정의할 수 있는 항목들

  | 항목     | 설명                |
  | -------- | ------------------- |
  | settings | 인덱스의 설정값     |
  | mappings | 인덱스의 매핑 정보  |
  | aliases  | 인덱스의 alias 정보 |



- 템플릿 생성하기

  - 아래와 같이 템플릿을 생성한 후 test1이라는 인덱스를 생성하면, 아래 템플릿이 적용되어 생성된다.

  ```bash
  $ curl -XPUT "localhost:9200/_template/my_template?pretty" -H 'Content-type:application/json' -d'
  {
  	"index_patterns":["test*"],
  	"order":1,
  	"settings":{
  		"number_of_shards":3,
  		"number_of_replicas":1
  	},
  	"mappings":{
  		"_doc":{
  			"properties":{
  				"test":{
  					"type":"text"
  				}
  			}
  		}
  	},
  	"aliases":{
  		"alias_test":{} # alias_test라는 별칭을 붙인다.
  	}
  }'
  ```

  - my_template이라는 이름으로 템플릿을 생성한다.
  - `index_patterns`에는 정규식이 사용 가능하다.
  - `order`
    - `index_patterns`에서 설정한 패턴이 겹치는 다른 템플릿이 존재한다면 어떤 템플릿을 적용할지 결정하는 역할을 한다.
    - 숫자가 높을 수록 우선순위가 높다.
    - 만일 A 템플릿에는 존재하는데 B 템플릿에는 존재하지 않는 설정이 있다면, A 템플릿이 우선 순위가 높다 하더라도, 해당 설정에 한해서는 B 템플릿이 적용된다.



- template 정보 확인하기

  - 모든 템플릿 확인하기

  ```bash
  $ curl -XPUT "localhost:9200/_cat/template?pretty"
  ```

  - 특정 템플릿 확인하기

  ```bash
  $ curl -XPUT "localhost:9200/_template/my_template?pretty"
  ```







