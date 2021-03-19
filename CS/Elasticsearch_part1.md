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
    - 어떤 문서를 ES에 입력하면 해당 문서는 우선 메모리 공간에 저장된다.
    - 그리고 1초 후에 샤드라는 ES 데이터 저장 공간에 저장되고 이후에는 쿼리를 통해서 해당 문서를 검색할 수 있게 된다.
    - 준 실시간성은 `refresh_interval`이라는 파라미터로 설정할 수 있다.
  - Lightning-fast(빠른 속도)
    - 엘라스틱 서치는 루씬을 기반으로 만들어졌기에 단어 입력 후 문서를 찾는 속도가 다른 NoSQL들에 비해 매우 빠르다.
  - Fault-tolerant(내고장성)
    - 노드 실패시 replicate된 다른 노드에서 데이터를 가져오며, 네트워크 실패 시 다른 마스터 복제본으로 선택한다.



- 일반적인 일래스틱서치 사용 사례

  - 일레스틱서치를 기본 백엔드로 사용
    - 전통적으로 검색엔진은 빠른 연관 검색 기능을 제공하기 위해 안정된 데이터 저장소 위에 배포한다.
    - 과거에는 검색엔진이 내구성 있는 저장소(durable storage)나 통계 같은 필요한 기능들을 제공하지 않았기 때문이다.
    - 일래스틱서치는 내구성 있는 저장소와 통계, 데이터 저장소에서 기대하는 다른 많은 기능을 제공하는 최신 검색엔진 중 하나다.
  - 기존 시스템에 엘라스틱서치 추가하기
    - 엘라스틱서치를 데이터 저장소로서는 사용하지 않고 오직 검색기능만을 위해서 사용
    - 기존의 데이터베이스와 엘라스틱서치를 동기화해서 사용한다.

  - 기존 시스템의 배게엔드로 일레스틱서치 사용하기
    - 일래스틱서치는 오픈소스이고 쉬운 HTTP 인터페이스를 제공하기에 큰 에코시스템을 가지고 있다.
    - 일래스특서치에 읽고 쓸 수 있는 도구들이 이미 이용 가능해서, 원하는 방식으로 동작하도록 도구를 설정하는 것 외에는 별도의 개발이 필요가 없다.



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



## 주요 기능

- 관련 결과 보장
  - 관련성 점수(relevancy score)
    - 특정 키워드가 포함 된 데이터들 중 정말 해당 키워드와 관련 있는 데이터를 가져오기 위해 관련성 점수를 계산한다.
    - 관련성 점수는 검색 조건과 일치하는 각각의 데이터에 할당된 점수이고 데이터가 얼마나 조건과 관련성이 있는지를 나타낸다.
  - 기본적으로 문서의 관련성을 평가하는 알고리즘은 **tf-idf**이다.
    - tf-idf는 단어 빈도, 역 문서 빈도를 나타내며, 관련성 점수에 영향을 주는 두 요소다.
    - 단어 빈도(term frequency): 데이터에서 찾고자 하는 단어가 많이 나올수록 높은 점수를 준다.
    - 역 문서 빈도(inverse document frequency): 다른 데이터들에서 흔치 않은 단어면 높은 가중치를 준다.
    - 예를 들어 사과 축제를 찾는다면 상대적으로 흔하지 않은 단어인 축제가 가중치가 높다.



- 완전 일치를 뛰어넘은 검색

  - 오타 처리
    - 정확히 일치하는 것만 찾는 대신 변형된 것들을 찾게 할 수 있다.
    - 퍼지(fuzzy) 질의를 사용하면 바나나에 대한 데이터를 찾을 때 바나너로도 검색할 수 있다.
  - 파생어 지원
    - 분석(analysis)을 사용하면 일래스틱서치가 사과라는 키워드를 검색할 때 apple, apples를 포함하여 검색하도록 할 수 있다.
  - 통계 사용
    - 사용자가 무엇을 검색할지 모를 때, 몇 가지 방법으로 도울 수 있다. 그 중 하나가 집계(aggregation)이다.
    - 집계는 질의의 결과로 수치들을 얻는 방법이다.
    - 얼마나 많은 주제가 범주별로 나뉘는지 또는 범주별로 좋아요와 공유의 숫자가 얼마인지와 같은 수치들을 얻을 수 있다.

  - 제안 제공
    - 사용자가 키워드를 입력할 때 인기 있는 검색 결과를 찾도록 도울 수 있다.
    - 와일드카드, 정규표현식 같은 특별한 질의 형태를 사용해서 입력했을 때 인기 있는 결과를 보여줄 수도 있다.



## 엘라스틱서치의 데이터 구조

- 엘라스틱서치 기본 개념
  - 클러스터
    - 여러 대의 컴퓨터 혹은 구성 요소들을 논리적으로 결합하여 전체를 하나의 컴퓨터 혹은 구성 요소처럼 사용할 수 있게 해주는 기술.
    - 엘라스틱서치에서 가장 큰 시스템 단위
    - 최소 하나 이상의 노드로 이루어진 노드들의 집합
    - 서로 다른 클러스터는 데이터의 접근, 교환을 할 수 없는 독립적인 시스템으로 유지된다.
    - 여러 대의 서버가 하나의 클러스터를 구성할 수 있고, 한 서버에 여러 개의 클러스터가 존재할 수도 있다.
    - 클러스터로 구성하면 높은 수준의 안정성을 얻을 수 있고 부하를 분산시킬 수 있다.
  - 노드
    - 엘라스틱서치를 구성하는 하나의 단위 프로세스
    - 역할에 따라 Master-eilgible, Data, Ingest, Tribe 노드로 구분할 수 있다.
    - Master-eilgible node: 클러스터를 제어하는 마스터 노드로 선택할 수 있는 노드
    - Master node: 인덱스 생성과 삭제, 클러스터 노드들의 추적과 관리, 데이터 입력 시 어느 샤드에 할당할 것인지를 결정하는 등의 역할을 수행한다.
    - Data node: 데이터와 관련된 CRUD 작업과 관련 있는 노드로, CPU, 메모리 등 자원을 많이 소모하므로 모니터링이 필요하며, master 노드와 분리되는 것이 좋다.
    - Ingest node: 데이터를 변환하는 등 사전 처리 파이프라인을 실행하는 역할을 한다.
    - Coordination only node: Master-eilgible node, Data node의 역할을 대신하는 노드로 대규모 클러스터에서 큰 이점이 있다.
    - 모든 노드는 매시 형태(모든 구성 요소가 논리적으로 연결되어 있어 다른 노드들과 직접적으로 통신할 수 있는 네트워크 형태)로 요청을 주고 받기 때문에 이떤 노드에서도 색인/검색 작업을 처리할 수 있으며 
    - 마스터 역할을 하는 서버만 요청을 처리할 수 있는 RDBMS와 달리 어떤 노드에서도 색인/검색 작업이 가능하기에 노드들 간의 부하 분산을 구현할 수 있다.
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



- 논리 배치와 물리 배치
  - 논리 배치
    - 검색 애플리케이션이 무엇을 알아야 하는가(즉, 검색 요청을 보내는 쪽에서 무엇을 알아야 하는가)
    - 색인과 검색을 위해 사용하는 단위는 문서이고, RDBMS의 행과 유사하다.
    - 타입은 테이블이 행을 포함하는 것과 유사하게 문서를 포함한다.
    - 마지막으로 하나 혹은 그 이상의 타입이 하나의 색인(index)에 존재한다.
    - 색인은 가장 큰 컨테이너이며 SQL 세계의 DB와 유사하다.
  - 물리 배치
    - 엘라스틱서치가 뒷단에서 어떻게 데이터를 다루는가(즉, 검색 요청을 받는 쪽은엘 어떻게 데이터를 다루는가)
    - 엘라스틱서치는 각 색인을 샤드로 나눈다.
    - 샤드는 클러스터를 구성하는 서버 간에 이동할 수 있다.
    - 보통 애플리케이션(프론트)은 서버의 개수와 무관하게 엘레스틱서치와 동작하기에 이것에 대해서 상관하지 않는다.
    - 그러나 클러스터를 관리할 때는 물리적으로 배치하는 방식이 성능과 확장성 가용성을 결정하기 때문에 관심을 가진다.



### 논리 배치

- 문서

  - 엘라스틱서치는 문서 기반이다.
    - 색인과 검색하는 데이터의 가장 작은 단위가 문서라는 것을 의미한다.
  - 문서는 독립적이다.
    - 필드(name)와 값(Elasticsearch Denver)을 가지고 있다.
    - 필드는 문서를 구성하기 위한 속성이라고 할 수 있다. 
    - 일반적으로 데이터베이스의 컬럼과 비교할 수 있으나 컬럼이 정적(static)인 데이터 타입인 반면, 필드는 좀 더 동적(dynamic)인 데이터 타입이다.
    - 문서는 보통 JSON 형식으로 표현한다.

  ```json
  {
      "name":"Theo",
      "department":"TA",
      "information":"developer"
  }
  ```

  - 문서는 계층을 가질 수 있다.
    - 즉 문서 안에 또 다른 문서가 존재할 수 있다.
    - 관계형 데이터베이스의 행과의 차이점이다.

  ```json
  {
      "name":"Theo",
      "department":"TA",
      // infromation이라는 문서 안에 또 다른 문서가 들어간다.
      "information":{
      	"email":"theo09@gmail.com",
          "phone": "010-1234-5678"
      }
  }
  ```

  - 유연한 구조를 가진다.
    - 문서는 미리 정의한 스키마에 의존하지 않는다.
    - 예를 들어 기존의 데이터에 필요 없는 값을 생략하거나, 새로운 값을 추가할 수 있다.

  ```json
  {
      "name":"Theo",
      "gender":"male"
  }
  ```

  - 하나의 문서가 값의 배열을 포함할 수 있다..

  ```json
  {
      "name":"Theo",
      "department":"TA",
      "colleague":["kim","lee"]
  }
  ```

  - 매핑 타입
    - 필드의 추가와 생략은 자유롭지만, 각 필드의 타입은 중요하다.
    - 일래스틱서치는 모든 필드와 타입, 그리고 다른 설정에 대한 매핑을 보관하고 있다.
    - 매핑(Mapping)은 문서의 필드와 필드의 속성을 정의하고 그에 따른 색인 방법을 정의하는 프로세스이다. 
    - 따라서 때로는 일래스틱서치에서 타입은 매핑 타입으로 불린다.



- 타입(7.0 버전부터 사라졌다)
  - 테이블이 행에 대한 컨테이너인 것과 같이 타입은 문서에 대한 논리적인 컨테이너다.
  - 각 타입에서 필드의 정의는 매핑이라고 부른다.
    - 예를 들어 위 예시에서 name은 stirng이지만 colleague는 list이다.
  - 일레스틱서치는 스키마가 존재하지 않는다.
    - 그럼에도 문서가 타입에 속하고 각 타입은 스키마와 같은 매핑을 포함하는가
    - 매핑은 타입에서 지금까지 색인한 모든 문서의 모든 필드를 포함한다.
    - 하지만 모든 문서가 모든 필드를 가질 필요는 없다.
    - 또한 새로운 문서가 매핑에 존재하지 않는 필드와 함께 색인하면, 일래스틱서치는 자동으로 새로운 필드를 매핑에 추가한다.예를 들어 값이 7이면,  long 타입을 가정한다.
    - 일래스틱서치가 새로운 필드의 타입을 잘못 추측할 수도 있다. 예를 들어, 7을 색인한 후에. "Hi"를 색인하면 "Hi"는 string이지 long이 아니므로 실패할 것이다.
    - 데이터의 색인을 만들기 전에 매핑을 정의하면 위와 같은 실패를 방지할 수 있다.
  - 매핑 타입은 문서를 논리적으로만 나눈다.
    - 물리적으로 같은 색인의 문서는 해당 문서가 속해 있는 매핑 타입에 관련 없이 디스크에 쓰인다.



- 색인
  - 매핑 타입의 컨테이너
    - 관계형 데이터베이스의 데이터베이스와 같이 독립적인 문서 덩어리아다.
  - 각각의 색인은 디스크에 같은 파일 집합으로 저장한다.
    - 모든 매핑 타입의 모든 필드를 저장하고, 고유의 설정을 한다.



### 물리 배치

- 노드와 샤드
  - 어떻게 데이터가 물리적으로 배치되는지 이해하는 것은 결국 어떻게 일래스틱서치가 확장하는지 이해하는 것이다.
  - 클러스터 내부에 노드들이 존재하며 각 노드 내부에 샤드들이 존재한다.
  - 샤드는 인덱스에 속한 문서들이 분산되어 저장된다.



- 색인의 생성과 검색
  - 색인의 생성
    - 문서 ID의 해시값을 기반으로 주 샤드 중 하나를 선택하고, 해당 주 샤드에 문서를 색인한다.
    - 그 후 해당 문서는 주 샤드의 모든 복제(replica)에 색인된다.
  - 색인 검색
    - 색인을 검색할 때 일래스틱서치는 해당 색인의 전체 샤드를 찾는다.
    - 일래스틱서치는 검색하려는 색인의 주 샤드와 레플리카 샤드로 검색 경로를 분리한다.
    - 즉, 레플리카를 검색 성능과 고장 감내(fault tolerance)에 유용하게 사용한다.



- 주 샤드(Primary shard)와 레플리카 샤드(replica shard)
  - 하나의 샤드는 하나의 루씬 색인이다.
    - 루씬 색인은 역 색인을 포함하는 파일들의 모음이다.
    - 역 색인은 일래스틱서치가 전체 문서를 찾아보지 않고도 하나의 단어를 포함하는 문서를 찾도록 해주는 구조다.
  - 일래스틱서치 색인과 루씬 색인
    - 일래스틱서치 색인은 샤드라는 청크로 나뉜다.
    - 하나의 색인은 하나의 루씬 색인이기에 일래스틱서치 색인은 여러 개의 루씬 색인으로 구성된다.
    - 일래스틱서치가 데이터를 색인하기 위한 핵심 라이브러리로 아파치 루씬을 사용하기에 루씬 색인이라 부른다.
    - 색인은 일레스틱서치 색인을 의미하며, 샤드 내부의 세부를 살펴볼 때는 루씬 색인이라 부른다.
  - 레플리카 샤드는 주 샤드의 정확한 복사본이다.
    - 레플리카는 검색을 위해 사용하거나 본래의 주 샤드를 잃어버렸을 때 새로운 주 샤드가 될 수 있다.
    - 일래스틱서치 색인은 하나 이상의 주 샤드와 0개 이상의 레플리카 샤드로 구성된다.



- 클러스터에 샤드 분산하기
  - 가장 단순한 일레스틱서치 클러스터는 하나의 노드를 가진다.
  - 같은 클러스터에서 더 많은 노드를 추가할수록 기존 샤드는 모든 노드에 균등하게 저장된다.
  - 클러스터에 노드를 추가하는 방법으로 확장하는 것을 수평적 확장이라 부른다.
    - 노드를 추가하면 요청이 분산되어 모든 노드가 일을 공유한다.



- 분산 색인과 검색
  - 색인
    - 색인 요청을 받은 일래스틱서치 노드는 우선 문서를 색인할 샤드를 선택한다.
    - 기본적으로 문서는 샤드에 골고루 분산된다.
    - 각 문서가 색인 될 샤드는 문서의 문자열로 이루어진 ID를 해싱해서 결정한다.
    - 각 샤드는 동등하게 새로운 문서를 받을 기회와 함께 동등한 해시 범위를 갖는다.
    - 대상 샤드가 결정되면 현재 노드는 샤드를 소유한 노드로 문서를 전달한다.
    - 해당 샤드의 복제 샤드에 색인 작업을 진행한다.
    - 색인 명령은 모든 가능한 레플리카가 문서를 색인한 후 색인에 성공했다는 결과값을 반환한다.
  - 검색
    - 검색 요청을 받은 노드는 모든 샤드에 요청을 전달한다.
    - 라운드 로빈을 사용해서, 일래스틱서치는 이용 가능한 주 혹은 레플리카 샤드를 선택하고 검색 요청을 전달한다.
    - 일래스틱서치는 샤드들로부터 결과를 모아서, 하나의 응답으로 집계 후에 클라이언트 애플리케이션에 응답을 전달한다.



## settings와 mappings

- settings와 mappings

  - 모든 인덱스는 settings와 mappings라는 두 개의 정보 단위를 가지고 있다.
  - 두 정보는 아래 명령어로 확인이 가능하다.

  ```bash
  $ curl 'localhost:9200/인덱스명?pretty'
  ```

  - 응답

  ```json
  {
    "company" : {
      "aliases" : { },
      "mappings" : {
        "properties" : {
          "age" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "name" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          }
        }
      },
      "settings" : {
        "index" : {
          "routing" : {
            "allocation" : {
              "include" : {
                "_tier_preference" : "data_content"
              }
            }
          },
          "number_of_shards" : "1",
          "provided_name" : "company",
          "creation_date" : "1615954842889",
          "number_of_replicas" : "1",
          "uuid" : "1pzaio30TyWjj73m80dBQA",
          "version" : {
            "created" : "7110299"
          }
        }
      }
    }
  }
  ```

  - settings 또는 mappings 정보만 따로 보고싶으면 아래와 같이 인덱스명 뒤에 보고자 하는 정보를 추가할 수 있다.

  ```bash
  $ curl 'localhost:9200/인덱스명/_settings?pretty'
  $ curl 'localhost:9200/인덱스명/_mappings?pretty'
  ```



- settings

  - 샤드의 수, 레플리카 샤드의 수, `refresh_interval`, 애널라이저, 토크나이저, 토큰 필터 등의 설정이 존재한다.

  - 샤드의 수는 인덱스를 처음 생성할 때 한 번 지정하면 바꿀 수 없지만 레플리카 샤드의 수는 동적으로 변경이 가능하다.

  ```bash
  # 레플리카 샤드의 수를 2개로 변경하는 명령어
  # 인덱스명 뒤에 _settings API로 접근해서 변경할 설정을 입력하면 변경이 가능하다.
  $ curl -XPUT 'localhost:9200/인덱스명/_settings?pretty' -H 'Content-Type: application/json' -d '{"number_of_replicas":2}'
  ```

  - `refresh_interval`: ES에서 세그먼트가 만들어지는 리프레시 타임을 설정하는 값으로 기본 값은 1초(1s)이다. 동적으로 변경이 가능하다.

  ```bash
  # refresh_interval을 30초로 변경하는 명령어
  $ curl -XPUT 'localhost:9200/company/_settings?pretty' -H 'Content-Type: application/json' -d '{"number_of_replicas":3}'
  ```



- mappings

  - ES는 동적 매핑을 지원하기에 미리 정의하지 않아도 인덱스에 도큐먼트를 새로 추가하면 자동으로 매핑이 생성된다.

  ```bash
  $ curl -XPUT 'localhost:9200/recipes/_doc/1' -H 'Content-Type: application/json' -d '{
  "name":"pasta",
  "author":"Theo",
  "created_date":"2018-10-24T00:00:00",
  "pages":3
  }'
  ```

  - recipes 엔덱스의 매핑 확인

  ```bash
  $ curl 'localhost:9200/recipes/_mappings?pretty'
  ```

  - 응답
    - 인덱스의 매핑에서 필드들은 `properties` 항목 아래 지정된다.
    - 매핑을 따로 설정해 준 적이 없음에도 각 필드의 매핑이 자동으로 생성된 것을 확인 가능하다.

  ```json
  {
    "recipes" : {
      "mappings" : {
        "properties" : {
          "author" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "created_date" : {
            "type" : "date"
          },
          "name" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "pages" : {
            "type" : "long"
          }
        }
      }
    }
  }
  ```

  - 매핑 미리 정의하기
    - 미리 먼저 인덱스의 매핑을 정의해 놓으면 정의해 놓은 매핑에 맞추어 데이터가 입력된다.
    - 매핑을 미리 만들 경우 미리 만들어진 매핑에 필드를 추가하는 것은 가능하지만 이미 만들어진 필드를 삭제하거나 필드의 타입 및 설정  값을 변경하는 것은 불가능하다.

  ```bash
  $ curl -XPUT 'localhost:9200/인덱스명' -H 'Content-Type: application/json' -d '{
  "mappings":{
  "properties":{
  "필드명":{
  "type":"필드 타입"
  ...필드 설정
  }
  }
  }
  }'
  ```

  - 미리 정의 된 매핑에 필드 추가하기
    - 당연히 기존 필드명과 추가할 필드명이 같으면 오류가 발생한다.

  ```bash
  $ curl -XPUT 'localhost:9200/인덱스명/_mapping' -H 'Content-Type: application/json' -d '{
    "properties":{
      "필드명":{
        "type":"필드 타입"
        ...필드 설정
      }
    }
  }'
  ```

  - 인덱스에 기존 매핑에 정의되지 않은 필드를 지닌 도큐먼트가 입력되면 필드가 자동으로 추가 된다.
    - 기존에 없던 rating 필드를 추가

  ```bash
  $ curl -XPUT 'localhost:9200/recipes/_doc/2' -H 'Content-Type: application/json' -d '{
  "rating":4
  }'
  ```

  - 확인

  ```json
  $ curl 'localhost:9200/recipes/_mappings?pretty'
  ```

  - 응답
    - rating 필드가 새로 추가 된 것을 확인 가능하다.

  ```json
  {
    "recipes" : {
      "mappings" : {
        "properties" : {
          "author" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "created_date" : {
            "type" : "date"
          },
          "name" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "pages" : {
            "type" : "long"
          },
          "rating" : {
            "type" : "long"
          }
        }
      }
    }
  }
  ```



### mappings의 type

- ES에서 선언 가능한 문자열 타입에는 text, keyword 두 가지가 있다.
  - 2.X 버전 이전에는 string이라는 하나의 타입만 있었고 텍스트 분석 여부, 즉 애널라이저 적용을 할 것인지 아닌지를 구분하는 설정이 있었다.
  - 5.0 버전부터는 텍스트 분석의 적용 여부를 text 타입과 keyword 타입으로 구분한다.
  - 인덱스를 생성할 때 매핑에 필드를 미리 정의하지 않으면 동적 문자열 필드가 생성될 때 text 필드와 keyword 필드가 다중 필드로 함께 생성된다.



- text
  - 입력된 문자열을 텀 단위로 쪼개어 역 색인 구조를 만든다.
  - 보통은 풀택스트 검색에 사용할 문자열 필드들을 text 타입으로 지정한다.
  - text 필드에는 아래와 같은 옵션들을 설정 가능하다.
    - `"analyzer" : "애널라이저명"`:  색인에 사용할 애널라이저를 입력하며 디폴트로는 standard 애널라이저를 사용한다. 토크나이저, 토큰필터들을 따로 지정할 수가 없으며 필요하다면 사용자 정의 애널라이저를 settings에 정의 해 두고 사용한다.
    - `"search_analyzer" : "애널라이저명"`: 기본적으로 text필드는 match 쿼리로 검색을 할 때 색인에 사용한 동일한 애널라이저로 검색 쿼리를 분석하는데, `search_analyzer`를 지정하면 검색시에는 색인에 사용한 애널라이저가 아닌 다른 애널라이저를 사용한다. 보통 NGram 방식으로 색인을 했을 때는 지정 해 주는 것이 바람직하다.
    - `"index" : <true | false>`: 디폴트는 true이고, false로 설정하면 해당 필드는 역 색인을 만들지 않아 검색이 불가능해진다.
    - `"boost" : 숫자 값`: 디폴트는 1이다. 값이 1 보다 높으면 풀텍스트 검색 시 해당 필드 스코어 점수에 가중치를 부여하고, 1 보다 낮은 값을 입력하면 가중치가 내려간다.
    - `"fielddata" : <true | false>`: 디폴트는 false이고, true로 설정하면 해당 필드의 색인된 텀들을 가지고 집계 또는 정렬이 가능하다. 이 설정은 동적으로 변경하는 것이 가능하다.



- keyword
  - 입력된 문자열을 하나의 토큰으로 저장한다.
    - text 타입에 keyword 애널라이저를 적용한 것과 동일하다
  - 보통은 집계 또는 정렬에 사용할 문자열 필드를 keyword 타입으로 지정한다.
  - keyword 필드에는 다음과 같은 옵션들을 설정할 수 있다.
    - `index`,`boost` 옵션은 text와 동일하다.
    - `"doc_values" : <true | false>`: 디폴트는 true이며, keyword 값들은 기본적으로 집계나 정렬에 메모리를 소모하지 않기 위해 값들을 doc_values라고 하는 별도의 열 기반 저장소를 만들어 저장하는데, 이 값을 false로 하면 doc_values에 값을 저장하지 않아 집계나 정렬이 불가능해진다.
    - `"ignore_above" : 자연수`: 디폴트는 2,147,483,647이며 다이나믹 매핑으로 생성되면 256으로 설정된다. 설정된 길이 이상의 문자열은 색인을 하지 않아 검색이나 집계가 불가능하다. `_source`에는 남아있기 때문에 다른 필드 값을 쿼리해서 나온 결과로 가져오는 것은 가능하다.
    - `"normalizer" : 노멀라이저명`: keyword 필드는 애널라이저를 사용하지 않는 대신 노멀라이저의 적용이 가능하다. 노멀라이저는 애널라이저와 유사하게 settings에서 정의하며 토크나이저는 적용할 수 없고 캐릭터 필드와 토큰 필터만 적용해서 사용이 가능하다.



- 숫자

  - ES는 JAVA에서 기본으로 사용되는 숫자 타입들을 지원한다.
  - 또한 half_float, scaled_float과 같이 ES에서만 사요외는 타입들도 존재한다.
  - 종류
    - JAVA에서 사용되는 숫자 타입들: long, integer, short, byte, double, float
    - ES에서만 지원하는 숫자 타입들: half_float, scaled_float

  - 사용 가능한 옵션들
    - `"index"`, `"doc_values"`, `"boost"` 등의 옵션들은 text, keyword 필드의 옵션들과 동일하다.
    - `"cource": <true | false>`: 디폴트는 true이며, 숫자 필드들은 기본적으로 숫자로 이해될 수 잇는 값들은 숫자로 변경해서 저장한다. 이를 false로 설정하면 정확한 타입으로 입력되지 않으면 오류가 발생한다. 
    - `"null_value": 숫자값`: 필드값이 입력되지 않거나 null인 경우 해당 필드의 디폴트 값을 지정한다. 
    - `"ignore_malformed": <true | false>`: 디폴트는 false로, 기본적으로 숫자 필드에 숫자가 아닌 불린 값이 들어오면 ES는 오류를 반환하는데, true로 설정하면 숫자가 아닌 값이 들어와도 도큐먼트를 정상적으로 저장한다. 해당 필드의 값은 `_source`에만 저장되고 겁색이나 집계에는 무시된다.
    - `"scaling_fator": 10의 배수`: scaled_float을 사용하려면 필수로 지정해야 하는 옵션으로 소수점 몇 자리까지 저장할지를 지정한다. 12.345라는 값을 저장하는 경우 `scaling_fator:10`과 같이 설정하면 실제로는 12.3이 저장되고, `scaling_fator:100`과 같이 설정했으면 12.34가 저장된다.

  - 전처리된 데이터가 아니면 항상 `_source`의 값은 변경되지 않는다.
    - `"cource": true`로 "4.5"라는 숫자가 integer 필드에 정상적으로 저장 되어도 `_source`의 값은 그대로 "4.5"이다.
    - `"null_value"`를 설정해도 역시 마찬가지로 `_source`에는 여전히 null로 표시된다.
  - `_source`에 저장된 값과 필드에 저장된 값이 다를 수 있다.
    - 예를 들어 byte 타입을 가진 필드에 4.5를 저장하는 경우에 byte는 오직 정수만을 저장하므로 4가 들어가게 된다.
    - 그러나 `_source`에는 4.5로 값이 들어가 있다.
    - 이 때 집계를 위해 3보다 크고 4.1보다 작은 값을 검색하면 4.5는 4.1보다 큼에도 필드에는 4로 저장되어 있으므로 검색이 되게 된다.
    - 이러한 이유로 숫자 필드를 동적으로 생성하는 것은 매우 위험하다.



- 날짜

  - ES에서 날짜 타입은 ISO8601 형식을 따라 입력한다.
    - "2021-03-18"
    - "2021-03-18T10:08:40"
    - "2021-03-18T10:08:40+09:00"
    - "2021-03-18T10:08:40.428Z"
    - ISO8601 형식을 따르지 않을 경우 text,keyword로 저장된다.
  - ISO8601외에도 long 타입 정수인 epoch_millis 형태의 입력도 가능하다.
    - epoch_millis는 1970-01-01 00:00:00부터의 시간을 밀리초 단위로 카운트 한 값이다.
    - 필드가 date 형으로 정의 된 이후에는 long 타입의 정수를 입력하면 날짜 형태로 저장이 가능하다.
    - epoch_millis외에도 epoch_second의 사용이 가능하다.
    - 사실 날짜 필드는 내부에서는 모두 long 형태의 epoch_millis로 저장한다.
  - 그 외에 사용 가능한 포맷들
    - 매핑의 format 형식만 지정 해 놓으면 지정된 어떤 형식으로도 색인 및 쿼리가 가능하다.
    - basic_date, strict_date_time과 같이 미리 정의 된 포맷들
    -  [joda.time.format](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html) 심볼을 사용하여 지정 가능하다.
    - 정의된 포맷들은  [Elastic 홈페이지의 공식 도큐먼트](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats)에서 볼 수 있으며 joda 심볼 기호들은 다음과 같다.

  | 심볼 | 의미                 | 예시) 2019-09-12T17:13:07.428+09.00 |
  | ---- | -------------------- | ----------------------------------- |
  | yyyy | 년도                 | 2019                                |
  | MM   | 월-숫자              | 09                                  |
  | MMM  | 월-문자(3자리)       | Sep                                 |
  | MMMM | 월-문자(전체)        | September                           |
  | dd   | 일                   | 12                                  |
  | a    | 오전/오후            | PM                                  |
  | HH   | 시각(0~23)           | 17                                  |
  | kk   | 시각(01-24)          | 17                                  |
  | hh   | 시각(01-12)          | 05                                  |
  | h    | 시각(1-12)           | 5                                   |
  | mm   | 분(00~59)            | 13                                  |
  | m    | 분(0~59)             | 13                                  |
  | ss   | 초(00~59)            | 07                                  |
  | s    | 초(0~59)             | 7                                   |
  | SSS  | 밀리초               | 428                                 |
  | Z    | 타임존               | +0900/+09:00                        |
  | e    | 요일(숫자 1:월~7:일) | 4                                   |
  | E    | 요일(텍스트)         | Thu                                 |

  - 사용 가능한 옵션들
    - `"doc_values"`, `"index"`, `"null_value"`, `"ignore_malformed"` 옵션들은 문자열, 숫자 필드와 기능이 동일하다.
    - `"format": "문자열 || 문자열..."`: 입력 가능한 날짜 형식을 ||로 구분해서 입력한다.



- 불리언
  - true, false 두 가지 값을 갖는 필드 타입이다.
  - "true"와 같이 문자열로 입력되어도 boolean으로 해석되어 저장된다.
  - 불리언 필드를 사용할 때는 일반적으로 term 쿼리를 이용해서 검색을 한다.
  - 사용 가능한 옵션들
    - `"doc_values"`, `"index"` 옵션들은 문자열, 숫자 필드와 기능이 동일하다.
    - `"null_value": true|false`: 필드가 존재하지 않거나 값이 null일 때 디폴트 값을 지정한다. 지정하지 않으면 불리언 필드가 없가나 값이 null인 경우 존재하지 않는 것으로 처리되어 true/false 모두 쿼리나 집계에 나타나지 않는다.



- Object와 Nested

  - JSON에서는 한 필드 안에 하위 필드를 넣는 object, 즉 객체 타입의 값을 사용할 수 있다.
    - 보통은 한 요소가 여러 하위 정보를 가지고 있는 경우 object 타입 형태로 사용한다.
  - object 필드를 선언할 때는 다음과 같이 `"properties"`를 입력하고 그 아래에 하위 필드 이름과 타입을 지정한다.

  ```bash
  $ curl -XPUT 'localhost:9200/movies?pretty' -H 'Content-Type: application/json' -d '{
    "mappings": {
      "properties": {
        "characters": {
          "properties": {
            "name": {
              "type": "text"
            },
            "age": {
              "type": "byte"
            },
            "side": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
  ```

  - object 필드를 쿼리로 검색하거나 집계를 할 때는 `.`를 이용해서 하위 필드에 접근한다.

  ```bash
  $ curl "http://localhost:9200/movie/_search" -H 'Content-Type: application/json' -d'{  "query": {    "match": { "characters.name": "Iron Man" }}}'
  ```

  - Nested
    - 만약에 object 타입 필드에 있는 여러 개의 object 값들이 서로 다른 역 색인 구조를 갖도록 하려면 nested 타입으로 지정해야 한다.
    - nested 타입으로 지정하려면 매핑이 다음과 같이 `"type":"nested"`를 명시한다.
    - 다른 부분은 object와 동일하다.

  ```bash
  curl -XPUT "http://localhost:9200/movie" -H 'Content-Type: application/json' -d'{
  "mappings":{    
    "properties":{      
      "characters":{        
        "type": "nested",        
          "properties": {          
            "name": {            
              "type": "text"          
            },          
            "side": {            
              "type": "keyword"          
            }        
          }      
        }    
      }   
    }
  }'
  ```

  - nested 필드를 검색 할 때는 반드시 nested 쿼리를 써야 한다. 
    - nested 쿼리 안에는 path 라는 옵션으로 nested로 정의된 필드를 먼저 명시하고 그 안에 다시 쿼리를 넣어서 입력한다.
    - nested 쿼리로 검색하면 nested 필드의 내부에 있는 값 들을 모두 별개의 도큐먼트로 취급한다.
    - object 필드 값들은 실제로 하나의 도큐먼트 안에 전부 포함되어 있다.
    - nested 필드 값들은 내부적으로 별도의 도큐먼트로 분리되어 저장되며 쿼리 결과에서 상위 도큐먼트와 합쳐져서 보여지게 된다.



- Geo
  - 위치 정보를 저장할 수 있는 Geo Point와 Geo Shape 같은 타입들이 있다.
  - Geo Point
    - 위도(latitude)와 경도(longitude) 두 개의 실수 값을 가지고 지도 위의 한 점을 나타내는 값이다.
  - Geo point는 다음과 같이 다양한 방법으로 입력이 가능하다.
  - 추후 추가







# Elaistcsearch 설치하고 실행하기

> https://www.elastic.co/kr/downloads/elasticsearch



- tar 파일로 설치하기

  - 위 사이트에서 tar 파일을 다운 받은 후 압축을 푼다.

  - 압축을 풀면 아래와 같은 디렉터리가 생성된다.

    - bin: ES 실행을 위한 바이너리 파일들이 모여 있는 디렉터리.
    - config: 환결 설정을 위한 파일들이 모여 있는 디렉터리.
    - lib: ES 실행을 위한 외부 라이브러리들이 모여 있는 디렉터리, 확장자가 jar 형태인 자바 라이브러리 파일들이 모여 있으며 ES의 기본이 되는 루씬 라이브러리도 여기에 포함되어 있다.

    - logs: 디폴트 로그 저장 디렉터리.
    - modules: ES를 구성하고 있는 모듈들이 모여 있는 디렉터리.
    - plugins: 설치한 플러그인을 구성하고 있는 파일들이 모여 있는 디렉터리.

  - 이 외에도 RPM, DEB로도 설치가 가능하다.



- 실행하기

  - bin/elasticsearch.bat 파일을 실행하여 실행이 가능하다.
  - 아래 명령어를 통해서도 실행이 가능하다.

  ```bash
  # bin 디렉토리에서
  $ ./elasticsearch.bat
  ```

  - `-d` 옵션을 붙여서 데몬 형태로 실행하는 방법

    - 위 명령어는 포어그라운드 형태로 실행시킨 것으로, 터미널에서 다른 입력을 하지 못하는 상태이다.

    - `-d` 옵션은 백그라운드에서 동작하게 해준다.

  ```bash
  $ ./elasticsearch.bat -d
  ```

  





# 데이터 처리

## 새로운 데이터 색인

- 문서 색인

  - 일레스틱서치에서 문서의 URI

  ```
  http://연결할 일레스틱 서치 노드의 호스트명:연결할 포트/색인명/타입명/문서id
  ```

  - 문서 색인 요청
    - `-X` 옵션은 request시 사용할 메소드의 종류를 기술한다. 메소드와 띄어 써도 되지만 붙여 써도 된다.
    - `-XGET`의 경우 생략이 가능하다.
    - 파라미터로 들어간 `pretty` 또는 `pretty-true`는 JSON  응답을 더 보기 좋게 해준다.
    - `-H` 옵션은 header를 지정한다.
    - `-d` 옵션은 body를 지정한다.

  ```bash
  $ curl -XPUT 'localhost:9200/company/colleague/1?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Theo",
  "age":"28"
  }'
  ```

  - 응답
    - 응답은 색인, 타입, 색인한 문서의 ID를 포함한다.

  ```json
  {
    "_index" : "company",
    "_type" : "colleague",
    "_id" : "1",
    "_version" : 1,
    "result" : "created",
    "_shards" : {
      "total" : 2,
      "successful" : 1,
      "failed" : 0
    },
    "_seq_no" : 0,
    "_primary_term" : 1
  }
  ```



- 색인 생성과 매핑 이해하기

  - curl 명령은 색인과 매핑타입을 자동으로 생성한다.
    - 위 예시에서 company라는 색인과 colleague라는 매핑 타입을 생성한 적이 없음에도 자동으로 생성되었다.
    - 수동으로 생성하는 것도 가능하다.
  - 색인을 수동으로 생성하기

  ```bash
  $ curl -XPUT 'localhost:9200/new-index'
  ```

  - 수동 생성의 응답

  ```json
  {
    "acknowledged" : true,
    "shards_acknowledged" : true,
    "index" : "test-index"
  }
  ```

  - 매핑 확인
    - 매핑을 보기 위해 url에 `_mapping`을 추가한다.
    - ES 6.x 이상의 경우 아래와 같이 `include_type_name=true` 또는 `include_type_name`을 파라미터로 넣어야 한다.

  ```bash
  $ curl 'localhost:9200/company/_mapping/colleague?include_type_name&pretty'
  ```

  - 응답
    - 색인 명, 타입, 프로퍼티 목록, 프로퍼티 옵션 등의 데이터가 응답으로 넘어 온다.

  ```json
  {
    "company" : {
      "mappings" : {
        "colleague" : {
          "properties" : {
            "age" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        }
      }
    }
  }
  ```



## 데이터 검색

- 검색하기

  - 검색을 위해 데이터를 더 추가

  ```bash
  $ curl -XPUT 'localhost:9200/company/colleague/2?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Kim",
  "age":"26"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/3?pretty' -H 'Content-Type: application/json' -d '{
  "name":"Lee",
  "age":"27"
  }'
  $ curl -XPUT 'localhost:9200/company/colleague/4?pretty' -H 'Content-Type: application/json' -d '{
  "name":"An",
  "age":"27"
  }'
  ```

  - 데이터 검색하기
    - `q`파라미터는 검색할 내용이 들어간다.
    - 특정 필드에서만 찾고자 할 때는 `q=name:Kim`과 같이 작성하면 된다.
    - 아래와 같이 필드를 지정해주지 않을 경우 `_all`이라는 모든 필드의 내용을 색인하는 필드가 자동으로 들어가게 된다.
    - `_source` 파라미터는 특정 필드만 반환되도록 한다(유사한 파라미터로 `stored_fileds`가 있다).
    - `size` 파라미터는 일치하는 데이터들 중 반환할 데이터의 수를 지정한다(기본값은 10이다).

  ```json
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 어디를 검색할지 설정하기

  - 다수의 타입에서 검색하기
    - url에서 타입을 콤마로 구분하여 검색하면 된다.
    - ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/colleague, department/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 모든 타입에서 검색하기
    - 타입을 지정하지 않고 검색하면 된다.
    - 역시 ES 6.X 부터 매핑 타입이 사라짐에 따라 쓸 일이 없는 기능이 되었다.

  ```bash
  $ curl "localhost:9200/company/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 다수의 색인을 검색하기
    - url에서 인덱스를 콤마로 구분하여 검색하면 된다.
    - 만일 검색하려는 색인이 없는 경우 에러가 발생하는데 에러를 무시하려면 `ignore_unavailable` 플래그를 주면 된다.

  ```bash
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty"
  
  # 없는 인덱스도 포함해서 검색하기
  $ curl "localhost:9200/company,fruits/_search?q=Kim&_source=name&size=1&pretty&ignore_unavailable"
  ```

  - 모든 색인을 검색하기
    - url의 색인이 올 자리에 `_all`을 입력하거나 아예 색인을 빼면 모든 색인에서 검색한다.

  ```bash
  $ curl "localhost:9200/_all/_search?q=Kim&_source=name&size=1&pretty"
  
  $ curl "localhost:9200/_search?q=Kim&_source=name&size=1&pretty"
  ```



- 응답 내용

  - 요청

  ```bash
  $ curl "localhost:9200/company/colleague/_search?q=Kim&_source=name&size=1&pretty"
  ```

  - 응답

  ```json
  {
    // 요청이 얼마나 걸렸으며, 타임아웃이 발생했는가
    "took" : 1,
    "timed_out" : false,
    // 몇 개의 샤드에 질의 했는가
    "_shards" : {
    "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      // 일치하는 모든 문서에 대한 통계
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      // 결과 배열
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim"
          }
        }
      ]
    }
  }
  ```

  - 시간
    - `took` 필드는 ES가 요청을 처리하는 데 얼마나 걸렸는지 말해준다(단위는 밀리 초).
    - `timed_out` 필드는 검색이 타임아웃 되었는지 보여준다.
    - 기본적으로 검색은 절대로 타임아웃이 되지 않지만, 요청을 보낼 때`timeout` 파라미터를 함께 보내면 한계를 명시할 수 있다.
    - `$ curl "localhost:9200/_search?q=Kim&timeout=3s"`와 같이 작성할 경우 3초가 지나면 타임아웃이 발생하고 `timed_out`필드의 값은 true가 된다.
    - 타임아웃이 발생할 경우 타임아웃될 때까지의 결과만 반환된다.
  - 샤드
    - 총 몇 개의 샤드에 질의 했고 성공한 것과 스킵한 것, 실패한 것에 대한 정보를 반환한다.
    - 만일 특정 노드가 이용 불가 상태라 해당 노드의 샤드를 검색하지 못했다면 질의에 실패한 것이 된다.
  - 히트 통계
    - `total`은 전체 문서 중 일치하는 문서 수를 나타낸다.
    - `total`은 `size`를 몇으로 줬는지와 무관하게 일치하는 모든 문서의 수를 표시해주므로 total과 실제 반환 받은 문서의 수가 다를 수 있다.
    - `max_score`는 일치하는 문서들 중 최고 점수를 볼 수 있다.
  - 결과 문서
    - 히트 배열에 담겨 있다.
    - 일치하는 각 문서의 색인, 타입, ID, 점수 등의 정보를 보여준다.



- 쿼리로 검색하기

  - 지금까지는 URI 요청으로 검색했다.
    - 간단한 검색에는 좋지만 복잡한 검색에는 적절치 못한 방법이다.
  - `query_string` 쿼리 타입으로 검색하기
    - 쿼리스트링 타입의 쿼리를 실행하는 명령문이다.
    - `default_field`는 검색을 실행할 필드를 특정하기 위해 사용한다.
    - `default_operator`는 검색할 단어들이 모두 일치하는 문서를 찾을 지, 하나라도 일치하는 문서를 찾을지를 설정한다(기본값은 OR로 하나라도 일치하는 문서는 모두 찾는다).
    - 위 두 옵션(`default_field`, `default_operator`)을 다음과 같이 쿼리 스트링 자체에 설정하는 것도 가능하다.
    - `"query":"name:Kim AND name:Lee"`

  ```bash
  $ curl 'localhost:9200/company/colleague/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
      "query_string":{
        "query":"Kim",
        "default_field":"name",
        "default_operator":"AND"
      }
    }
  }'
  ```

  - 응답

  ```json
  {
    "took" : 1,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      "hits" : [
        {
          "_index" : "company",
          "_type" : "colleague",
          "_id" : "2",
          "_score" : 0.6931471,
          "_source" : {
            "name" : "Kim",
            "age" : "26"
          }
        }
      ]
    }
  }
  ```



- 필터 사용(ES 6.X 부터 사용 불가)

  - 필터는 결과에 점수를 반환하지 않는다.
    - 쿼리는 결과와 함께 각 결과의 점수를 반환한다.
    - 필터는 오직 키워드가 일치하는지만 판단하여 일치하는 값들을 반환한다.
  - 필터 검색

  ```bash
  $ curl 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d '{
    "query":{
    	"filtered":{
    	  "filter":{
      	"term" :{
            "name":"Kim"
          }
    	  }
    	}    
    }
  }'
  ```



- ID로 문서 가져오기

  - 검색은 준실시간인데 반해 문서 ID로 문서를 찾는 것은 실시간이다.
  - 특정 문서를 가져오려면 문서가 속한 색인과 타입, 그리고 ID를 알아야 한다.
    - 그러나 타입은 현재 사라졌기 때문에 type 자리에 `_doc`을 입력하여 검색한다.
    - 타입을 입력해도 검색은 되지만 경고문이 뜬다.

  ```json
  // _doc 사용
  $ curl 'localhost:9200/company/_doc/1?pretty'
  
  // 타입 사용
  $ curl 'localhost:9200/company/colleague/1?pretty'
  ```

  - 응답
    - 만일 찾는 문서가 존재하지 않으면 아래 `found`는 false가 된다.

  ```json
  {
    "_index" : "company",
    "_type" : "_doc",
    "_id" : "1",
    "_version" : 5,
    "_seq_no" : 5,
    "_primary_term" : 1,
    "found" : true,
    "_source" : {
      "name" : "Theo",
      "age" : "28"
    }
  }
  ```





## CRUD

- 도큐먼트에 접근
  - 엘라스틱서치는 단일 도큐먼트별로 고유한 URL을 갖는다.
  - `http://<호스트>:<포트>/<인덱스명>/_doc/<도큐먼트id>`



- 삽입(PUT)

  - POST 메서드로도 추가가 가능하다.
    - 둘의 차이는 POST의 경우 도큐먼트id를 입력하지 않아도 자동으로 생성하지만 PUT은 자동으로 생성하지 않는다는 것이다.
  - office라는 인덱스에 도큐먼트id가 1인 데이터를 입력하는 예시

  ```json
  PUT office/_doc/1
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
  PUT office/_create/1
  
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
  POST office/_doc/1
  
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
  POST office/_doc/1
  
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
  POST office/_update/2
  
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