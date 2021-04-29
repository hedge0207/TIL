# 엘라스틱서치 모니터링

## Head

- Head
  - 클러스터의 상태를 모니터링 할 수 있는 모니터링 도구 중 하나.
  - 가장 큰 장점 중 하나는 샤드 배치 정보를 확인할 수 있다는 점이다.



- 설치하기
  - 기존에는 플러그인 방식을 사용했지만 ES6 이상부터는 보안상의 이유로 플러그인 방식을 사용하지 않는다.
  - https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm 에서 확장 프로그램을 추가하여 사용이 가능하다.



- Overview
  - 클러스터를 구성하는 노드들의 이름과 인덱스 이름, 인덱스를 구성하는 샤드와 인덱스에 저장된 문서의 건수를 살펴볼 수 있다.
  - 노드의 Info 버튼
    - Cluster Node Info는 해당 노드의 호스트명과 아이피 등의 여러 가지 설정을 확인 가능하다. 
    - Node Stats는 노드의 기본 정보와 클러스터에서 수행된 동작들의 통계 정보를 확인할 수 있다. 간단한 수치이기 때문에 특별히 유의미한 정보는 아니다.
  - 노드의 Actions 버튼
    - Shutdown 메뉴는 동작하지 않는다.
    - 프로세스의 종료는 가급적이면 시스템에 접근하여 실행하는 것이 로그나 클러스터 상태를 살피기에 좋다.
  - 인덱스의 Info 버튼
    - Index Status는 해당 인덱스의 문서 개수나 삭제된 문서 개수, 사이즈, 해당 인덱스를 대상으로 수행한 동작들의 통계 정보를 보여준다. 이 값도 단순한 수치이기 때문에 특별히 유의미한 정보는 아니다.
    - Index Metadata는 인덱스의 open/close 여부와 함께 인덱스를 구성하는 정보인 settings, mappings, aliases 정보를 보여준다. 해당 정보는 인덱스가 어떻게 구성되어 있는지 한 눈에 확인할 때 유용하다.
  - 인덱스의 Actions 버튼
    - New Alias, Refresh, Flush 등의 드롭다운 메뉴가 존재한다.
    - 인덱스 alias, refresh, forcemerge, close, delete 등 인덱스에 수행할 수 있는 다양한 작업을 진행 가능하다.



- Indices
  - 클러스터 내에 생성한 인덱스의 이름과 크기, 문서의 개수를 요약하여 보여준다.
  - Overview 탭에서도 확인 가능하지만 인덱스가 많아져 전체 인덱스를 한 눈에 확인하기 어려울 때 사용한다.



- Browser
  - 생성한 인덱스와 타입, 문서의 필드에 해당하는 내용들을 확인 가능하다.
  - 검색 API를 사용하지 않고도 인덱스내에 어떤 문서들이 어떤 타입으로 생성되어 있는지 하나씩 확인 가능하다.



- Structured Query
  - 특정 인덱스를 선택하여 간단하게 쿼리를 해볼 수 있는 탭이다.
  - 드롭다운 메뉴에서 항목들을 선택하고 Search 버튼을 누르면 원하는 검색 결과를 확인할 수 있다.'



- Any Request
  - Head에 연결시킨 클러스터에 쿼리를 요청할 수 있다.
  - Structured Query가 구조화된 검색 쿼리만 요청할 수 있는 반면, 다양한 요청을 전달할 수 있다.
  - 기본으로는 POST 메서드로 _search API를 호출하도록 되어 있다.
  - 하단의 Request를 클릭하면 정의한 사항들을 클러스터에 요청한다.





## X-Pack

- X-Pack
  - 베이직 라이선스로 활용할 수 있으며, 베이직 라이선스는 무료로 사용할 수 있다.
  - 6.3 이전 버전은 1년에 한 번 베이직 라이선스를 재활성화하기 위해 클러스터의 노드를 전부 삭제해야 한다.
  - 6.3 이후 버전부터 라이선스를 규칙적으로 갱신하지 않아도 모니터링 기능을 사용할 수 있다.



- 설치하기

  - Kibana를 설치해야 한다.

    - Kibana는 ES에 저장된 로그를 검색하거나 그래프 등으로 시각화할 때 사용하는 도구다.
    - 사실상 ES의 웹 UI와 같은 역할을 하는 도구라고 생각하면 된다.

    - 공식 홈페이지에서 다운로드 가능하다.



- 프로메테우스
  - 위의 두 가지 외에도 프로메테우스를 사용해서도 모니터링이 가능하다.
    - 오픈 소스 기반의 모니터링 시스템.
    - 데이터를 시간의 흐름대로 저장할 수 있는 시계열 데이터베이스의 일종.
    - 수집된 데이터를 바탕으로 임계치를 설정하고 경고 메세지를 받을 수 있는 오픈소스 모니터링 시스템이다.
    - ES 외에도 많은 시스템을 모니터링할 수 있게 해준다.
  - 컴포넌트 구성
    - 중앙에 TSDB(Time Series Data Base)의 역할을 하는 Prometheus Server가 존재한다.
    - 각종 지표들을 Exporter라는 컴포넌트를 통해서 가져올 수 있다.
    - Push Gateway를 통해서 입력할 수도 있다.
    - 각 항목에 대한 임계치를 설정하여 Alert Manager를 통해 경고 메시지를 받을 수도 있다.



# 클러스터 구축하기

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

- 클러스터의 할당 정보를 확인하는 API

  ```bash
  $ curl -XGET _cluster/allocation/explain
  ```

  

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
  $ curl -XPUT "localhost:9200/_flush/synced?pretty" -H 'Content-type:application/json'
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

  - 클러스터 그린 상태 확인
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
  $ curl -XPUT "localhost:9200/_cluster/reroute/retry_failed?pretty" -H 'Content-type:application/json'
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

  - 아무때나 샤드 재배치가 일어나는 것이 아니라 cluseter.routing.allocation.disk.threshold_enabled 설정(기본값은 true)에 의해 클러스터 내의 노드 중 한 대 이상의 디스크 사용량이 아래와 같이 설정한 임계치에 도달했을 때 동작하게 된다.
    - cluster.routing.allocation.disk.watermark.low: 특정 노드에서 임계치가 넘어가면 해당 노드에 더 이상 할당하지 않음. 새롭게 생성된 인덱스에 대해서는 적용되지 않음(기본값은 85%)
    - cluster.routing.allocation.disk.watermark.high: 임계치를 넘어선 노드를 대상으로 즉시 샤드 재할당 진행. 새로 생성된 인덱스에도 적용됨(기본값은 90%)
    - cluster.routing.allocation.disk.watermark.flood_stage: 전체 노드가 임계치를 넘어서면 인덱스를 read only 모드로 변경(기본값은 95%)
    - cluster.info.update.interval: 임계치 설정을 체크할 주기(기본값은 30s)

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

  



# 엘라스틱서치 설정하기

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



- JVM 설정 조정하기

  - 엘라스틱서치는 JAVA 애플리케이션이므로 JVM에서 실행한다.
  - 엘라스틱서치에 의해 사용하는 대부분 메모리는 힙이라고 부른다.
    - 기본 설정은 ES가 힙으로 초기에 256MB를 할당해서 1GB까지 확장한다.
    - 검색이나 색인 작업이 1GB 이상의 RAM이 필요하면, 작업이 실패하고 로그에서 OOM(Out of Memory) 에러를 보게 될 것이다.
    - 엘라스틱서치에 얼마만큼의 메모리를 사용할지 변경하기 위해 `ES_HEAP_SIZE` 환경변수를 사용할 수 있다.

  ```bash
  # heap을 늘린 후 elasticsearch를 실행한다.
  SET ES_HEAP_SIZE=500m & bin\elasticearch.bat
  ```



# 클러스터에 노드 추가하기

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







