# 검색 엔진 개요

- 검색 엔진(search engine)의 정의
  - 웹에 존재하는 많은 양의 정보 중에서 사용자가 원하는 정보만을 여러 웹 사이트나 웹 페이지 등에서 검색해주는 시스템이나 프로그램을 통틀어 검색 엔진이라 부른다.
  - 검색 엔진은 사용자가 원하는 정보를 웹에서 찾는데 걸리는 시간을 최소화할 수 있게 도와준다.



- 검색 엔진 현황
  - 국내의 검색 엔진
    - 와이즈넛, 코난테크놀로지, 솔트룩스의 3파전 양상
    - 와이즈넛이 가장 유명하지만 그렇다고 기술력이 가장 뛰어난 업체라는 것은 아니다.
  - 오픈소스 검색 엔진
    - 루신, 솔라, 엘라스틱서치 등이 대표적인 오픈소스 검색엔진이다.
    - 솔라와 엘라스틱서치는 모두 루씬을 기반으로 만들어졌다.
  - 검색 엔진은 협업 없이는 만드는 것이 불가능에 가깝다.
    - 검색 엔진은 기본적으로 형태소 분석기, 색인, 검색 기능이 존재해야 한다.
    - 색인, 검색 기능은 혼자 구현할 수 있겠으나 형태소 분석은 혼자 개발하는 것이 불가능하다.
    - 전문적으로 국내의 형태소를 배운 사람과의 협업이 필수적이다.
    - 따라서 개발할 엄두를 내기 힘들며 다른 오픈소스에 비해 검색 엔진 오픈소스는 수가 부족하다.



- 검색 엔진의 구동 원리
  - 형태소 분석기

    > https://aiopen.etri.re.kr/demo_nlu.php
    >
    > https://www.shineware.co.kr/products/komoran/

    - 검색 엔진의 필수적인 3 가지 기능(형태소 분석, 색인, 검색) 중 가장 어려운 것이 형태소 분석기이다.
    - 사전을 기반으로 만든다고 하더라도 사전을 전부 순회하며 찾는다면 시간이 오래 걸릴 것이다.
    - 또한 신조어는 찾을 수 없는 문제가 발생한다.

  - 색인

    - 형태소 분석기를 돌린 결과를 토대로 데이터를 빠르게 찾기 위해서 색인을 활용해야 한다.
    - 색인을 쓰지 않으면, 모든 데이터를 일일히 찾는 엔진이 될 것이다.
    - 일반적으로 색인은 단어와 레코드 주소를 Key, Value로 묶어서 저장하는 구조를 가진다. 이를 역 색인(Inverted Indexing)이라 부른다.

  - 검색

    - 검색은 사용자으 질의(Query)를 분석하여 원하는 결과를 찾아주는 데 여기서 형태소 분석기를 마찬가지로 활용하게 된다.



- 역색인

  - 역색인은 키워드들에 문서들의 PK(또는 주소, 파일명 등)와 같은 값등을 매핑하여 저장하는 기술이다.
    - 역색인 작업의 장점은 매우 빨리 찾을 수 있다는 것이다.
    - 기존보다 추가적인 작업과 메모리가 필요하게 되지만, 검색은 매우 빠른 속도로 처리가 된다.
  - 다음과 같이 dictionary 구조로 저장되어 있는 데이터(문서)가 있다.

  ```python
  data1 = {1:"사과의 효능에 대해서 알아봅시다."}
  data2 = {2:"사과의 효능과 유통기한에 대해서 알아봅시다."}
  data3 = {3:"제가 가장 좋아하는 과일은 사과입니다."}
  ```

  - 위 data들의 value에 형태소 분석을 수행하면 각 value의 형태소들이 추출된다.
    - 일반적으로 검색엔진은 불필요한 품사를 제외한 명사등만 추출한다(명사만 추출된다고 가정).
    - data1: 사과, 효능
    - data2: 사과, 효능, 유통기한
    - data3: 사과, 과일
  - 검색 엔진은 위 결과를 토대로 역색인 작업을 하게 된다.

  | 키워드   | 문서 번호 |
  | -------- | --------- |
  | 사과     | 1, 2, 3   |
  | 효능     | 1, 2      |
  | 유통기한 | 2         |
  | 과일     | 3         |

  - "사과 효능"을 검색했을 경우
    - 사과가 포함된 문서 1,2,3을 가져오고
    - 유통기한이 포함된 문서 1, 2를 가져온다.
    - 마지막으로 둘의 교집합인 1, 2를 출력해준다.

  - AND가 아닌 OR 처리가 필요하다면 다음과 같은 처리를 하면 된다.
    - "사과 효능"을 검색할 경우
    - 1번 문서에는 사과, 효능이 모두 일치한다 - 2개가 일치
    - 2번 문서도 사과, 효능이 모두 일치한다 - 2개가 일치
    - 3번 문서는 사과만 일치한다 - 1개만 일치
    - 이제 문서별로 일치도가 높은 순으로 정렬(1,2,3) 후 사용자에게 출력한다.





# 엘라스틱 서치 개요

- 엘라스틱 서치란
  - 오픈 소스 검색 엔진
  - 역사
    - 2004년 샤이 배논이 요리 공부를 시작한 아내를 위해 레시피 검색 프로그램을 만드려 함.
    - 아파치 루씬을 적용하려던 중 루씬이 가진 한계를 보완하기 위해 새로운 검색엔진을 만들기 위한 프로젝트를 시작, Compass라는 이름의 오픈소스 검색 엔진을 개발함.
    - 2010년 Compass에서 Elasticsearch라고 이름을 바꾸고 프로젝트를 오픈소스로 공개.
    - 2012년에 창시자 샤이 배논과 함께 스티븐 셔르만, 우리 보네스 그리고 아파치 루씬 커미터인 사이먼 윌너 4인이 네델란드 암스텔담에서 회사를 설립 설립.
    - 현재는 주 본사인 네덜란드 암스테르담과 캘리포니아 마운틴 뷰를 비롯한 전 세계에 직원들이 분포되어 있다.
    -  Logstash, Kibana와 함께 사용 되면서 한동안 ELK Stack (Elasticsearch, Logstash, Kibana) 이라고 널리 알려지게 된 Elastic은 2013년에 Logstash, Kibana 프로젝트를 정식으로 흡수.
    - 2015년에는 회사명을 Elasticsearch 에서 Elastic으로 변경 하고, ELK Stack 대신 제품명을 Elastic Stack이라고 정식으로 명명하면서 모니터링, 클라우드 서비스, 머신러닝 등의 기능을 계속해서 개발, 확장 하고 있다.
    - 창시자인 샤이 배논은 트위터와 공식 아이디로 kimchy 를 사용하고 있는데, 2000년대 초반 한국에서 생활한 적이 있어 김치를 좋아한다고도 이야기 하고 있고, 또 Kimchy는 샤이 배논의 어머니 성씨이기도 하다.
    - 샤이 배논은 동양 문화에 관심이 많으며 Elasticsearch 첫 로고는 소나무 분재였고 샤이 배논의 블로그에는 지금도 용(竜) 한자가 메인 로고로 있다.



- 엘라스틱 서치를 사용해야하는 이유
  - 엘라스틱 서치가 최고의 솔루션이다라는 환상에서 벗어나는 것이 좋다.
    - 물론 상용 검색엔진을 비용, 기술적 문제로 다루기 힘든 사람에게는 최고의 선택이 될 수 있을 것이다.
  - 데이터베이스 대용으로 사용 가능하다.
    - NoSQL처럼 사용 가능하다.
  - 대량의 비정형 데이터 보관 및 검색 가능
    - 기존 데이터베이스로 처리하기 어려운 대량의 비정형 데이터 검색이 가능하며, 전문 검색(Full-Text Search)과 구조 검색 모두를 지원한다.
    - 기본적으로는 검색엔진이지만 MongoDB나 Hbase처럼 대용량 스토리지로 사용도 가능하다.
  - 통계 분석
    - 비정형 로그 데이터를 수집하고 한 곳에 모아서 통계 분석이 가능하다.
    - 키바나(엘라스틱 스택의 하나)를 이용하면 시각화 또한 가능하다.
  - 멀티 테넌시(Multi-tenancy)
    - 엘라스틱서치에서 인덱스는 관계형 DB의 데이터베이스와 같은 개념임에도 불구하고, 서로 다른 인덱스에서도 검색할 필드명만 같으면 여러 개의 인덱스를 한번에 조회할 수 있다.
  - Schemaless
    - 엘라스틱 서치는 JSON 구조를 사용하여 기존의 RDMS와 같은 엄격한 구조를 적용하지 않는다.
    - 비정형 데이터는 비구조적이며, 스키마가 다이나믹하게 변할 수 있다.
    - 전통적인 관계형 구조로 구성할 경우 프로젝트 막바지에 모든 스키마를 변경하고, 데이터를 다시 구성하는 문제에 봉착할 수 있는데 JSON 구조는 이런 문제들을 사전에 막을 수 있다.
  - 문서지향
    - 여러 계층의 데이터를 JSON 형식의 구조화된 문서로 인덱스에 저장 가능하다. 
    - 계층 구조로 문서도 한 번의 쿼리로 쉽게 조회 가능하다.
  - 데이터 공간을 절약할 수 있다.
    - 컬럼을 동적으로 정의하여, 필요한 데이터만 넣게 되어 데이터 공간 및 CPU 사용량, 네트워크 트래픽도 줄일 수 있는 효과를 볼 수 있다.
    - 컬럼이 동적으로 정의되지 않을 경우, 예를 들어 데이터 a, b, c가 있을 때, c만 color라는 컬럼을 가진다면, a, b는 굳이 color에 null이라는 데이터를 추가해줘야 한다. 
  - 검색 능력
    - 기본적인 검색 기능뿐만 아니라 Full-text search(전문 검색 엔진)라는 강력한 기능을 탑재하고 있다.
    - Full-text search: 모든 데이터를 역파일 색인 구조로 저장하여 가공된 텍스트를 검색하는 것.
  - 분석
    - 엘라스틱서치를 탑재한 사이트에 접속하는 사람들의 OS가 무엇인지, 혹은 어느 나라에서 접속했는지 등을 알고 싶을 때 엘라스틱의 분석 기능을 사용하면 편리하게 알 수 있다.
  - 풍부한 API와 REST 지원
    - Python, Java, C#, JS 등 20개의 프로그래밍 언어를 지원한다.
    - 기본적으로 Elasticsearch는 REST API를 제공하여 REST API를 사용하는 모든 언어에서 HTTP 형식으로 사용할 수 있다.
  - 쉬운 작동, 쉬운 확장
    - single node instance로 작동을 하며, 수백개의 스케일 아웃을 쉽게 할 수 있다.
    - Elasticsearch는 대부분의 빅데이터 플랫폼들이 그러하듯 Vertical Scaling보다 Horizontal Scaling을 사용한다.
    - Vertical Scaling(수직 스케일링)은 단순히 말하자면 기존의 하드웨어를 보다 높은 사양으로 업그레이드하는 것을 말한다. 스케일업(Scale-up)이라고도 한다.
    - Horizontal Scaling(수평 스케일링)은 장비를 추가해서 확장하는 방식을 말한다. 스케일아웃(Scale-out)이라고도 한다.
  - Near real-time(근접 실시간)
    - 검색 엔진은 기본적으로 형태소를 분석하고 색인을 해야 하는 다른 DBMS보다 오래 걸린다.
    - 엘라스틱 역시 데이터를 삽입한 순간 약 몇 초 정도는 이 단계를 지나며 그 후 검색을 할 수 있다.
  - Lightning-fast(빠른 속도)
    - 엘라스틱 서치는 루씬을 기반으로 만들어졌기에 단어 입력 후 문서를 찾는 속도가 다른 NoSQL들에 비해 매우 빠르다.
  - Fault-tolerant(내고장성)
    - 노드 실패시 replicate된 다른 노드에서 데이터를 가져오며, 네트워크 실패 시 다른 마스터 복제본으로 선택한다.



- DB의 SQL과 엘라스틱 서치
  - DB의 SQL로도 데이터 검색이 가능하다.
  - 그럼에도 검색 엔진이 필요한 이유는 다음과 같다.
    - RDBMS는 단순 텍스트 매칭에 대한 검색만을 제공한다(MySQL 최신 버전에서는 n-gram 기반의 Full-text 검색을 지원하지만, 한글 검색은 아직 많이 빈약하다).
    - 텍스트를 여러 단어로 변형하거나 텍스트의 특질을 이용한 동의어나 유의어를 활용한 검색이 가능
    - 엘라스틱 서치 등의 검색엔진에서는 RDBMS에서는 불가능한 비정형 데이터의 색인과 검색이 가능
    - 엘라스틱 서치 등의 검색엔진에서는 형태소 분석을 통한 자연어 처리가 가능
    - 역색인 지원으로 매우 빠른 검색이 가능
  - RDBMS와 엘라스틱서치의 가장 큰 차이 중 하나는 데이터를 CRUD하는 방식이다.
    - RDBMS의 경우 DB를 서버와 연결하여 SQL을 날리는 방식을 사용한다.
    - 엘라스틱서치의 경우 RESTful API라는 방식을 이용한다.
    - 또한 엘라스틱서치의 POST 즉, 데이터 삽입의 경우에는 관계형 데이터베이스와 약간 다른 특성을 갖고 있는데, 스키마가 미리 정의되어 있지 않더라도, **자동으로 필드를 생성하고 저장**한다는 점이다. 이러한 특성은 큰 유연성을 제공하지만 선호되는 방법은 아니다.



- 엘라스틱서치의 약점
  - 실시간(Real Time) 처리는 불가능하다.
    - 엘라스틱서치의 데이터 색인의 특징 때문에 엘라스틱서치의 색인된 데이터는 1초 뒤에나 검색이 가능하다. 
    - 색인된 데이터가 내부적으로 커밋(Commit)과 플러시(Flush)와 같은 과정을 거치기 때문. 
    - 그래서 엘라스틱서치 공식 홈페이지에서도 NRT(Near Real Time)라는 표현을 쓴다.
  - 트랜잭션(Transaction) 롤백(Rollback) 등의 기능을 제공하지 않는다.
    - 분산 시스템 구성의 특징 때문에, 시스템적으로 비용 소모가 큰 롤백, 트랜잭션을 지원하지 않는다. 
    - 그러므로 데이터 관리에 유의해야 한다.
  - 진정한 의미의 업데이트(Update)를 지원하지 않는다.
    - 업데이트 명령이 존재는 한다.
    - 그러나 실제로는 데이터를 삭제했다가 다시 만드는 과정으로 업데이트된다. 
    - 이러한 특성은 나중에 불변성(Immutable)이라는 이점을 제공하기도 한다.



- 엘라스틱서치 기본 개념
  - 클러스터
    - 엘라스틱서치에서 가장 큰 시스템 단위
    - 최소 하나 이상의 노드로 이루어진 노드들의 집합
    - 서로 다른 클러스터는 데이터의 접근, 교환을 할 수 없는 독립적인 시스템으로 유지된다.
    - 여러 대의 서버가 하나의 클러스터를 구성할 수 있고, 한 서버에 여러 개의 클러스터가 존재할 수도 있다.
  - 노드
    - 엘라스틱서치를 구성하는 하나의 단위 프로세스
    - 역할에 따라 Master-eilgible, Data, Ingest, Tribe 노드로 구분할 수 있다.
    - Master-eilgible node: 클러스터를 제어하는 마스터 노드로 선택할 수 있는 노드
    - Master node: 인덱스 생성과 삭제, 클러스터 노드들의 추적과 관리, 데이터 입력 시 어느 샤드에 할당할 것인지를 결정하는 등의 역할을 수행한다.
    - Data node: 데이터와 관련된 CRUD 작업과 관련 있는 노드로, CPU, 메모리 등 자원을 많이 소모하므로 모니터링이 필요하며, master 노드와 분리되는 것이 좋다.
    - Ingest node: 데이터를 변환하는 등 사전 처리 파이프라인을 실행하는 역할을 한다.
    - Coordination only node: Master-eilgible node, Data node의 역할을 대신하는 노드로 대규모 클러스터에서 큰 이점이 있다.
  - 인덱스
    - RDBMS의 database에 대응하는 개념.
    - 엘라스틱서치에만 존재하는 개념은 아니며, 분산 데이터베이스 시스템에도 존재하는 개념이다.
  - 샤딩(sharding)
    - 데이터를 분산해서 저장하는 방법
    - 엘라스틱서치에서 스케일 아웃을 위해 index를 여러 shard로 쪼갠 것.
    - 기본적으로 1개가 존재하며, 검색 성능 향상을 위해 클러스터의 샤드 개수를 조장하는 튜닝을 하기도 한다.
  - 복제본(replica)
    - 또 다른 형태의 shard.
    - 노드를 손실했을 경우 데이터의 신뢰성을 위해 샤드들을 복제하는 것.
    - 따라서 shard와 replica는 서로 다른 노드에 저장해야 한다.



- DB와 엘라스틱 서치의 용어 비교

  | DB           | 엘라스틱서치 |
  | ------------ | ------------ |
  | 데이터베이스 | 인덱스       |
  | 파티션       | 샤드         |
  | 테이블       | 타입         |
  | 행           | 문서         |
  | 열           | 필드         |
  | 스키마       | 매핑         |
  | SQL          | Query DSL    |




# 데이터 처리

## CRUD

- 도큐먼트에 접근
  - 엘라스틱서치는 단일 도큐먼트별로 고유한 URL을 갖는다.
  - `http://<호스트>:<포트>/<인덱스>/_doc/<도큐먼트id>`



- 삽입(POST)

  - PUT 메서드로도 추가가 가능하다.
    - 둘의 차이는 POST의 경우 도큐먼트id를 입력하지 않아도 자동으로 생성하지만 PUT은 자동으로 생성하지 않는다는 것이다.
  - office라는 인덱스에 도큐먼트id가 1인 데이터를 입력하는 예시

  ```json
  POST office/_doc/1
  {
      "nickname":"Theo",
      "message":"안녕하세요!"
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 1,
      "result": "created", // 새로 생성한 것이므로 created로 뜨지만, 수정할 경우 updated라고 뜬다.
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 0,
      "_primary_term": 1
  }
  ```

  - 실수로 기존 도큐먼트가 덮어씌워지는 것을 방지하기 위해 입력 명령어에 `_doc` 대신 `_create`를 사용해서 새로운 도큐먼트의 입력만 허용하는 것이 가능하다.
    - 이 경우 이미 있는 도큐먼트id를 추가하려 할 경우 오류가 발생한다.
    - 이미 위에서 도큐먼트id가 1인 도큐먼트를 추가했으므로 아래 예시는 오류가 발생한다. 

  ```json
  POST office/_create/1
  
  {
      "nickname":"Theo",
      "message":"안녕하세요!"
  }
  ```



- 조회

  - 도큐먼트id가 1인 도큐먼트를 조회하는 예시

  ```json
  GET office/_doc/1
  ```

  - 응답
    - 문서의 내용은 `_source` 항목에 나타난다.

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
          "nickname": "Theo",
          "message": "안녕하세요!"
      }
  }
  ```



- 삭제

  - 도큐먼트 또는 인덱스 단위의 삭제가 가능하다.
    - 도큐먼트를 삭제하면 `"result":"deleted"`가 반환된다.
    - 도큐먼트는 삭제되었지만 인덱스는 남아있는 경우, 삭제된 도큐먼트를 조회하려하면 `"found":false`가 반환된다.
    - 삭제된 인덱스의 도큐먼트를 조회하려고 할 경우(혹은 애초에 생성된 적 없는 도큐먼트를 조회할 경우) 에러가 반환된다.

  - 도큐먼트를 삭제하는 경우

  ```json
  DELETE office/_doc/1
  ```

  - 도큐먼트 삭제의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "deleted",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 삭제된 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 삭제된 도큐먼트를 조회했을 경우의 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "found": false
  }
  ```

  - 인덱스를 삭제

  ```json
  DELETE office
  ```

  - 인덱스 삭제의 응답

  ```json
  {
      "acknowledged": true
  }
  ```

  - 삭제된 인덱스의 도큐먼트를 조회

  ```json
  GET office/_doc/1
  ```

  - 응답

  ```json
  {
      "error": {
          "root_cause": [
              {
                  "type": "index_not_found_exception",
                  "reason": "no such index [office]",
                  "resource.type": "index_expression",
                  "resource.id": "office",
                  "index_uuid": "_na_",
                  "index": "office"
              }
          ],
          "type": "index_not_found_exception",
          "reason": "no such index [office]",
          "resource.type": "index_expression",
          "resource.id": "office",
          "index_uuid": "_na_",
          "index": "office"
      },
      "status": 404
  }
  ```



- 수정

  - 위에서 삭제한 데이터를 다시 생성했다고 가정
  - 수정 요청

  ```json
  PUT office/_doc/1
  
  {
      "nickname":"Oeht",
      "message":"!요세하녕안"
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "result": "updated",
      "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
      },
      "_seq_no": 1,
      "_primary_term": 1
  }
  ```

  - 수정할 때 특정 필드를 뺄 경우 해당 필드가 빠진 채로 수정된다.
    - POST 메서드로도 수정이 가능한데 POST 메서드를 사용해도 마찬가지다.

  ```json
  // 요청
  PUT office/_doc/1
  
  {
      "nickname":"Theo"
  }
  
  // 응답
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "1",
      "_version": 2,
      "_seq_no": 9,
      "_primary_term": 1,
      "found": true,
      "_source": {
          // message 필드가 사라졌다.
          "nickname": "Theo"
      }
  }
  ```

  - `_update`
    - `_update`를 활용하면 일부 필드만 수정하는 것이 가능하다.
    - 업데이트 할 내용에 `"doc"`이라는 지정자를 사용한다.

  ```json
  // 도큐먼트id가 2인 새로운 도큐먼트를 생성했다고 가정
  PUT office/_update/2
  
  {
      "doc":{
          "message":"반갑습니다.!"
      }
  }
  ```

  - 응답

  ```json
  {
      "_index": "office",
      "_type": "_doc",
      "_id": "2",
      "_version": 2,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
          "nickname": "Oeht",
          "message": "반갑습니다!"
      }
  }
  ```



## 벌크 API

- `_bulk`

  - 복수의 요청을 한 번에 전송할 때 사용한다.
    - 동작을 따로따로 수행하는 것 보다 속도가 훨씬 빠르다.
    - 대량의 데이터를 입력할 때는 반드시 `_bulk` API를 사용해야 불필요한 오버헤드가 없다.
  - 형식
    - index, create, update, delete의 동작이 가능하다.
    - delete를 제외하고는 명령문과 데이터문을 한 줄씩 순서대로 입력한다.
    - delete는 내용 입력이 필요 없기 때문에 명령문만 있다.
    - `_bulk`의 명령문과 데이터문은 반드시 한 줄 안에 입력이 되어야 하며 줄바꿈을 허용하지 않는다.

  - 예시

  ```json
  POST _bulk
  {"index":{"_index":"learning", "_id":"1"}} // 생성
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}} // 생성
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}} // 삭제
  {"create":{"_index":"learning", "_id":"3"}} // 생성
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}} // 수정
  {"doc":{"field":"deep learning"}}
  ```

  - 응답

  ```json
  {
    "took" : 1152,
    "errors" : false,
    "items" : [
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 0,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 1,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "delete" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 2,
          "result" : "deleted",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 2,
          "_primary_term" : 1,
          "status" : 200
        }
      },
      {
        "create" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "3",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 3,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "update" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 2,
          "result" : "updated",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 4,
          "_primary_term" : 1,
          "status" : 200
        }
      }
    ]
  }
  ```

  - 인덱스명이 모두 동일할 경우에는 아래와 같이 하는 것도 가능하다.

  ```json
  POST learning/_bulk
  
  {"index":{"_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_id":"2"}}
  {"create":{"_id":"3"}}
  {"field":"docker"}
  {"update":{"_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```



- json 파일에 실행할 명령을 저장하고 curl 며영으로 실행시킬 수 있다.

  - bulk.json 파일

  ```json
  {"index":{"_index":"learning", "_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}}
  {"create":{"_index":"learning", "_id":"3"}}
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```

  - 명령어
    - 파일 이름 앞에는 @를 입력한다.

  ```bash
  $ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
  ```





# 참고

https://needjarvis.tistory.com/167?category=704321

https://esbook.kimjmin.net/

https://velog.io/@jakeseo_me/%EC%97%98%EB%9D%BC%EC%8A%A4%ED%8B%B1%EC%84%9C%EC%B9%98-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0-2-DB%EB%A7%8C-%EC%9E%88%EC%9C%BC%EB%A9%B4-%EB%90%98%EB%8A%94%EB%8D%B0-%EC%99%9C-%EA%B5%B3%EC%9D%B4-%EA%B2%80%EC%83%89%EC%97%94%EC%A7%84