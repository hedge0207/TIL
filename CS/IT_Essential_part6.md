# 프로그래밍 언어

- 저급 언어와 고급 언어
  - 저급 언어: 컴퓨터가 이해하기 쉬운 언어, 기계어
  - 고급 언어:인간이 이해하기 쉬운 언어, 기계어로 바꾸는 과정 필요



- 기계어와 어셈블리어
  - 기계어
    - CPU가 해독할 수 있는 언어
    - 비트 단위로 표현하기 때문에 0과 1로만 표현
  - 어셈블리어
    - 각 명령어에 대해 사람이 알아보기 쉬운 니모닉 기호(연상 기호)를 정해 사람이 좀 더 쉽게 컴퓨터의 행동을 제어할 수 있도록 한 것



- Python, Java, C의 차이

  - Python-Java
    - Python: 동적 타이핑을 지향(변수는 고정된 값을 갖지 않는다)
    - Java: 정적 타이핑을 지향(변수를 선언할 때 타입을 정해줘야 한다)

  - Python-C
    - Python은 객체 지향 언어
    - C는 절차 지향 언어: 입력된 순서에 따라 프로그램을 실행한다.
  - Java-C
    - Java는 객체 지향 언어
    - C는 절차 지향 언어: 입력된 순서에 따라 프로그램을 실행한다.



## 절차적 프로그래밍 언어

- 주의사항
  - 아래의 언어별 구분은 절대적인 것이 아니다.
  - 예컨데 객체지향 프로그래밍 언어이면서 스크립트 언어일 수 있다.



- 개념
  - 특정 작업을 수행하기 위한 프로그램을 작성할 때 프로시저, 루틴으로 구성이 되거 프로그래밍 하는 프로그래밍 패러다임
    - 루틴은 할 일에 대한 순서가 정해져 있으며, 그것이 변하지 않는다는 것을 의미한다.
    - 프로시저란 순서를 의미한다.
    - 즉, 프로그래머가 정의한 루틴을 위에서 아래의 순서로 실행하는 것을 절차적 프로그래밍이라 한다.
  - 명령형 프로그래밍이라고도 불린다.



- 특징
  - 크게 복잡하지 않고 유지보수가 쉽다.
  - 순차적으로 진행되기에 프로그램의 흐름을 파악하기 쉽다.



- 종류
  - 알골(ALGOL)
    - 알고리즘의 연구 개발에 이용하기 위한 목적으로 생성
    - 절차형 언어로는 최초로 재귀호출이 가능
    - 이후 언어의 발전에 큰 영향을 미침
  - C 언어
    - 유닉스 운영 체제에서 사용하기 위해 개발한 프로그래밍 언어
    - 유닉스 시스템의 바탕은 모두 C로 작성
    - 수 많은 운영체제의 커널 또한 C로 작성
  - 베이직(BASIC)
    - 교육용으로 개발된 언어
    - 다양한 종류가 존재(다른 종류 사이의 소스코드는 호환되지 않음)
  - 포트란(FORTRAN)
    - 과학 계산에 필수적인 벡터, 행렬 계산 등이 내장되어 있는 과학 기술 전문 언어
    - 산술 기호, 삼각 함수, 대수합수 등과 같은 수학 함수들 사용 가능

## 객체지향 프로그래밍 언어

- 개념
  - 컴퓨터 프로그램을 명령의 목록으로 보는 시각에서 벗어나 여러 개의 독립된 단위인 객체들을 중심으로 하는 프로그래밍 패러다임
  - 객체 지향 프로그래밍은 프로그램을 유연하고 변경이 용이하게 만들기 때문에 대규모 소프트웨어 개발에 많이 사용된다.



- 특징
  - 클래스에 하나의 문제 해결을 위한 데이터르 모아 놓음으로써 응집력을 강화.
  - 클래스 간에 독립적으로 디자인함으로써 결합력을 약하게 할 수 있다.



- 기능
  - 자료 추상화
    - 불필요한 정보는 숨기고 중요한 정보만 표현함으로써 프로그램을 간단하게 만든다.
  - 상속
    - 새로운 클래스가 기존 클래스의 자료와 연산을 이용할 수 있게 하는 기능
    - 상속을 받는 자식 클래스를 생성함으로써 기존의 클래스는 변경하지 않고도 프로그램의 요구에 맞추어 클래스 수정 가능.
    - 클래스 간의 종속 관게를 형성함으로써 객체를 조직화
  - 다중 상속
    - 2개 이상의 클래스로부터 상속을 받을 수 있게 하는 기능.
    - 클래스들의 상속 관계에 혼란을 줄 수 있음
    - 모든 객체 지향 언어에서 지원하는 것은 아니다(JAVA는 미지원)
  - 다형성
    - 어떤 한 요소에 여러 개념을 넣어 놓는 기법
    - 일반적으로 오버라이딩이나 오버로딩을 의미
    - 다형 개념을 통해서 프로그램 안 객체 간의 관계를 조직적으로 표현
  - 동적 바인딩
    - 실행 시간 중에 일어나거나 실행 과정에서 변경될 수 있는 바인딩.
    - 프로그램의 한 개체나 기호를 실행 과정에 여러 속성이나 연산에 바인딩 함으로써 다형 개념을 실현



- 종류
  - C++
    - C 언어에 객체 지향 프로그래밍을 지원
    - C 언어에 대해 상위 호환성을 갖는 언어
    - 직접 신경써야 하는 것들이 많은 언어이기 때문에 개발이 어려움
  - C#
    - 마이크로소프트에서 개발한 객체 지향 프로그래밍 언어
    - 자바와 달리 불완전 코드와 같은 기술을 통하여 플랫폼 간 상호 운용성 확보
  - JAVA
    - 가전 제품 내에 탑재해 동작하는 프로그램을 위해 개발
    - 가장 큰 특징은 컴파일된 코드(.class)가 플랫폼 독립적
    - 자바 컴파일러는 자바 언어로 작성된 프로그램을 바이트코드라는 특수한 바이너리 형태로 변환

## 스크립트 언어

- 개념
  - 소스코드를 컴파일하지 않고도 실행할 수 있는 프로그래밍 언어.
  - 응용 프로그램과 독립하여 사용하고, 일반적으로 응용 프로그램의 언어와 다른 언어로 사용되어 최종 사용자가 응용 프로그램의 동작을 사용자의 요구에 맞게 수행할 수 있도록 해준다.



- 특징
  - 일반적으로 빠르게 배우고 쉽게 작성할 수 있다.
  - 다른 언어들에 비해 상대적으로 단순한 구문과 의미를 내포한다.
  - 보통 스크립트 언어로 작성된 코드는 시작에서 끝날 때까지 실행되며, 시작점(Entry Point)이 따로 명시되어 있지 않다.



- 종류

  - PHP

    - 동적 웹 페이지를 만들기 위해 개발
    - 범용 프로그래밍 언어로도 사용

  - 펄(Perl)

    - 인터프리터 방식(소스 코드를 바로 실행하는 방식)
    - 실용성을 모토로, 다른 언어에서 뛰어난 기능을 많이 도입

    - 강력한 문자열 처리 기능이 특징

  - Python

    - 라이브러리가 풍부하며 다영한 플랫폼에서 사용 가능
    - 들여쓰기를 사용하여 블록을 구분하는 문법 사용

  - JavaScript

    - 객체 기반의 스크립트 프로그래밍 언어
    - 웹 브라우저에서 주로 사용된다.



## 선언형 언어

- 개념
  - 해법을 정의하기 보다는 문제를 설명하는 언어.
  - 선언형 언어는 무엇을 할 것인지에 중점을 두고 있다.



- 유형
  - 함수형 언어
    - 자료 처리를 수학적 함수의 계산으로 취급
    - 상태와 가변 데이터를 멀리하는 프로그래밍 패러다임
    - 함수의 출력값은 그 함수에 입력된 인수에만 의존하므로 인수 x에 같은 값을 넣고 함수 f를 호출하면 항상 f(x)라는 결과가 나온다(순수함수).
  - 논리형 언어
    - 논리 문장을 이용하여 프로그램을 표현하고 계산을 수행하는 개념에 기반.
    - 대부분의 논리 문장들은 절대 문절 형태로 존재



- 기능
  - 함수형 언어
    - 순수 함수: 어느 순간에 호출해도 동일한 값을 반환(부작용이 없는 함수).
    - 익명 함수: 이름이 없는 함수, 람다식이라고도 불린다.
    - 고계함수: 함수를 또 하나의 값으로 간주하여 함수의 인자 혹은 반환값으로 사용할 수 있는 함수
  - 논리형 언어
    - 사실: 객체와 객체 간의 관계에 대한 논리적 사실을 포함하고 있는 문장
    - 규칙: 목표점에 이르는 원인 규명 과정은 지식 데이터베이스로부터 새로운 논리를 찾는 과정
    - 질문: 추론 규칙이 참인지 거짓인지 확인하기 위한 문장



- 종류
  - 함수형 언어
    - 허스켈(Haskell)
    - 리스프(LISP)
  - 논리형 언어
    - 프롤로그(Prolog)
  - 특수분야 언어
    - SQL



# UI

- UI(User Interface)
  - 넓은 의미에서 사용자와 시스템 사이에서 의사소통 할 수 있도록 고안된 물리적 혹은 가상의 매개체이다.
  - 좁은 의미에서는 정보기기나 소프트웨어의 화면 등에서 사람들이 접하게 되는 화면이다.



- UX(User eXperience)
  - 제품과 서비스 등을 사용자가 직/간접적으로 경험하면서 느끼고 생각하는 총체적 경험.
  - UI는 UX에 포함되는 개념이다.



- UI 유형
  - CLI(Command Line Interface)
    - 정적인 테스트 기반 인터페이스
    - 명령어를 텍스트로 입력하여 조작하는 사용자 인터페이스
  - GUI(Graphical User Interface)
    - 그래픽 반응 기반 인터페이스
    - 그래픽 환경을 기반으로 한 마우스나 전자펜을 이용하는 사용자 인터페이스
  - NUI(Natrural User Interface)
    - 직관적 사용자 반응 기반 인터페이스
    - 사용자가 가진 셩험을 기반으로 키보드나 마우스 없이 신체 부위를 이용하는 사용자 인터페이스(터치, 음성 등)
  - OUI(Organic User Interface)
    - 유기적 상호작용 기반 인터페이스
    - 입력장치가 곧 출력장치가 되고, 현실에 존재하는 모든 사물이 입출력장치로 변화 할 수 있는 사용자 인터페이스



- UI 분야
  - 물리적 제어 분야: 정보 제공과 기능 전달을 위한 하드웨어 기반
  - 디자인적 분야: 콘텐츠의 정확하고 상세한 표현과 전체적 구성
  - 기능적 분야: 사용자의 편의성에 맞춰 쉽고 간편하게 사용 가능



- UI 설계 원칙
  - 직관성
    - 누구나 쉽게 이해하고, 쉽게 사용 가능해야 함.
    - 쉬운 사용성, 일관성
  - 유효성
    - 정확하고 완벽하게 사용자의 목표가 달성될 수 있어야 함
    - 쉬운 오류 처리 및 복구
  - 학습성
    - 초보와 숙련자 모두가 쉽게 배우고 사용할 수 있게 제작해야 함
    - 쉽게 학습, 쉽게 기억
  - 유연성
    - 사용자의 인터랙션(입출력 장치를 매개로 디지털 시스템과 사람이 주고받는 일련의 의사소통 과정)을 최대한 포용하고, 실수를 방지할 수 있도록 제작
    - 오류 예방, 실수 포용, 오류 감지



- UI 개발을 위한 주요 기법

  - 3C 분석
    - 고객(Customer), 자사(Company), 경쟁사(Competitor)를 비교, 분석.
    - 자사를 어떻게 차별화할지 분석하는 기법

  - SWOT 분석
    - Strength(강점), Weakness(약점), Opportunity(기회), Threat(위협) 요인을 규정.
    - 기업 내부의 환경과 외부 환경을 분석
  - 시나리오 플래닝
    - 불확실성이 높은 상황 변화를 사전에 예측하고 다양한 시나리오를 설계하는 방법.
    - 불확실성을 제거하는 전략.
  - 사용성 테스트
    - 사용자가 직접 제품을 사용하면서 미리 작성된 시나리오에 맞추어 과제를 수행.
    - 과제 수행 후 질문에 답하도록 한다.
  - 워크숍
    - 소규모 인원으로 특정 문제나 과제에 대한 새로운 지식, 기술, 아이데어, 방법들을 서로 교환하고 검토.



- UI 설계 프로세스
  - 문제 정의
    - 시스템의 목적을 수립
    - 해결해야 할 문제 정의
  - 사용자 모델 정의
    - 사용자의 특성 파악
    - 소트프웨어와 이를 통해 수행할 작업에 대한 이해도를 바탕으로 초보자, 중급자, 숙련자로 분류
  - 작업 분석
    - 사용자 특징 세분화
  - 컴퓨터 오브젝트 및 기능 정의
    - 분석한 작업을 어떤 UI를 통해 표현할 것인지 정의
  - 사용자 인터페이스 정의
    - 작업자가 예측한 대로 동작하도록 사용자 인터페이스를 정의
    - 오브젝트(키보드, 마우스 등)를 선택
  - 디자인 평가
    - 설계한 UI가 분석한 작업에 맞게 설계가 되었는지, 사용자의 능력이나 지식에 적합한지, 쉽고 쓰기 편한지 등을 평가
    - GOMS, 휴리스틱 등의 사용자 공학의 평가 방법론 사용
    - GOMS: Goals, Operators, Methods, Selection rules의 약자로, 사용자가 서비스를 사용하면서 배우고, 이해하고, 사용하는지에 대해 평가하는 방법이다.
    - 휴리스틱: 경험에 기반하여 문제를 해결 또는 학습하거나 발견하는 기법.  





# 소프트웨어의 이해

- 소프트웨어
  - 정의 컴퓨터 시스템을 효율적으로 운영하기 위해 개발된 프로그램의 총칭.
  - 소프트웨어의 구성 요소: source code, 산출물(자료구조, DB, 테스트 결과 등), 매뉴얼



- 소프트웨어의 분류

  - 정보 관리 소프트웨어

    - 정보 제공 및 관리 소프트웨어
    - DB에 자료를 저장 후 검색을 통해 사용자가 원하는 형태로 정보를 제공
    - 예시: 인터넷 뱅킹, 대학의 종합정보 시스템 등

  - 제어 소프트웨어

    - 각종 센서를 이용하거나 기기들의 동작을 제어하는 소프트웨어
    - 예시: 교통 신호 제어, 의료 기기 제어, 공장 장비 제어 등

  - 임베디드 소프트웨어

    - 장비나 기기에 내장된 형태의 소프트웨어

    - 예시: 가전제품내의 소프트웨어, 각종 공정 제어 시스템 내의 소프트웨어



- 소프트웨어의 특징
  - 제조가 아닌 개발
    - 제조: 정해진 틀에 맞춰 일정하게 생산하는 것, 많은 인력이 필요하고 능력별 결과물 차이가 근소함
    - 개발: 개인의 능력에 따라 결과물 차이가 매우 크다.
  - 소모가 아닌 품질 저하
    - 하드웨어: 오래 사용하면 부품이 닳고, 고장 발생 빈도가 높어지고, 기능도 저하된다.
    - 소프트웨어: 오래 사용해도 닳지 않고, 고장 발생 빈도 낮고, 기능도 동일하다.



- 소프트웨어 개발의 문제점
  - 아래 내용은 단순히 몇 십년 전에 개발된 테트리스와 현재 개발중인 다른 게임들을 비교해보면 차이를 확연히 알 수 있다.
  - 새로운 소프트웨어에 대한 사용자 요구가 증가하고 있으나 소프트웨어 개발의 발전 속도가 이를 따라가지 못함
  - 소프트웨어 개발에도 관리가 필요
    - 비용 관리, 일정 관리, 개발자 관리
    - PMBOK를 활용한 적극적인 프로젝트 관리가 필요하다.
    - PMBOK(Project Management Body Of Knowledge): 프로젝트 관리 협회에서 발간하는 프로젝트 관리를 위한 일련의 표준 용어 및 지침.
  - 개발 과정이 복잡해지고 있다.
  - 참여 인력이 많아지고 있다.
  - 개발 기간이 길어지고 있다.



- 소프트웨어 공학

  - 정의: 품질 좋은 소프트웨어를 경제적으로 개발하기 위해 계획을 세우고, 개발하며, 유지 및 관리하는 과정에서 공학, 과학, 수학적 원리와 방법을 적용하여 필요한 이론과 기술 및 도구들에 관해 연구하는 학문.

  - 목표: 개발 과정에서의 생산성 향상과 고품질 소프트웨어 생산을 통한 사용자의 만족도 향상.
  - 특성: 정해진 기간, 주어진 비용이라는 제약사항 내에서 개발을 해야 한다. 따라서 효율성을 향상시키려는 노력이 필요







# 소프트웨어 개발 생명 주기(SDLC, System Development Life Cycle)

- 폭포수 모델(Waterfall Model): S/W개발을 단계적으로 정의한 체계이며 대표적인 선형 순차적 모델이다. 가장 오래되고 널리 사용되고 있다.
  - 단계
    - 계획: 사용자의 문제 정의 및 전체 시스템이 갖춰야 할 기본 기능과 성능 요건을 파악
    - 요구분석: 사용자의 문제를 구체적으로 이해
    - 설계: 소프트웨어의 구조를 명확히 밝혀 구현을 준비하는 단계
    - 구현: 프로그래밍을 하는 단계
    - 테스트: 소프트웨어를 테스트하는 단계
    - 유지보수: 소프트웨어를 발전시키는 단계
  - 장점
    - 관리 용이
    - 체계적 문서화 가능
    - 요구사항 변화가 적은 프로젝트에 적합
  - 단점
    - 각 단계는 앞 단계가 완료되어야 수행 가능
    - 각 단계의 결과물이 완벽해야 다음 단계에 오류를 넘겨주지 않는다.
    - 사용자가 중간에 가시적인 결과를 볼 수 없다.



- 프로토타입 모델(Prototyping Model)
  - 점진적으로 시스템을 개발해 나가는 접근 방식, 진화적 프로세스 모델의 대표적 모델이다.
  - 프로토타입을 만들어 고객과 사용자가 함께 평가한 후 개발될 소프트웨어의 요구사항을 정제하여 보다 완전한 요구명세서를 완성하는 방식
  - 빠른 설계-프로토타입 제작-사용자에게 평가를 받음-사용자가 바라던 것이 아닐 경우 요구 사항 재정의, 맞을 경우 본격적인 개발 시작
  - 장점
    - 사용자 요구가 충분히 반영된다.
    - 프로토타입 사용을 통한 새로운 요구사항 발견
    - 프로토타입 사용을 통한 완성품 예측 가능
  - 단점
    - 인력 및 자원 산정의 어려움
    - 프로토타입 과정에 대한 통제 및 관리의 어려움
    - 불명확한 개발 범위로 인한 개발 종료 시점 및 목표의 불확실성



- 나선형 모델(Spiral Model)
  - 프로토타입 모델에 위험 분석을 더한 모델
  - 요구사항 분석 및 계획 수립 - 위험 분석 - 개발 및 검증 - 사용자 평가 순으로 반복
  - 위험 분석 단계에서 요구사항의 빈번한 변경, 경험이 부족한 팀원, 팀워크가 부족한 협업, 프로젝트 관리의 부족 등의 위험 요소를 분석한다.
  - 장점
    - 위험 요소 감소와 이를 통한 프로젝트 중단 확률 감소
    - 사용자의 요구가 충분히 반영되는 개발 과정
  - 단점
    - 반복적 개발에 의한 프로젝트 기간 연장의 가능성
    - 반복 회수 증가에 따른 프로젝트 관리의 어려움
    - 위험 전문가 필요에 따른 부담



- 통합 프로세스(UP) 모델
  - 개발의 모든 단계를 무자르듯 자르는 것이 아니라 모든 단계들이 유기적으로 연결되어 있다는 것을 인지하고 동시에 진행하는 방식
  - 단계
    - 도입 단계: 요구사항 분석 및 문제 정의
    - 구체화 단계: 설계
    - 구축 단계: 프로그래밍
    - 전이 단계: 테스트, 배포, 운영 등
    - 도입/구체화/구축/전이 단계의 공통 작업



# Agile

- 애자일 프로세스 모델

  - agile: 날렵한, 민첩한
  - 정의: 고객의 요구에 민첩하게 대응하고 그때 그때 주어지는 문제를 풀어나가는 방법론, 반복적인 개발을 통한 잦은 출시를 목표로 한다. 고객과의 협업이 핵심 가치
  - 기본 가치
    - 프로세스와 도구 중심이 아닌, 개개인과의 상호 소통 중시
    - 문서 중심이 아닌, 실행 가능한 소프트웨어 중시
    - 계약과 협상 중심이 아닌, 고객과의 협력 중시
    - 계획 중심이 아닌, 변화에 대한 민첩한 대응 중시

  - 단계(아래 과정을 반복한다)
    - 설계
    - 개발
    - 테스트
    - 데모 출시
  - 스크럼 개발 프로세스
    - 소프트웨어 개발보다는 팀의 개선과 프로젝트 관리를 위한 애자일 방법론
    - 구체적인 프로세스를 명확하게 제시하지 않음
    - 개발 팀(조직)을 운영하는 효율적인 운영 방식(지침)
    - 일일 회의를 통한 팀원들 간의 신속한 협조와 조율이 가능하다.
    - 다른 개발 방법론에 비해 단순하고 실천 지향적이다.
    - 프로젝트 진행 현황 공유를 통해 신속하게 목표와 결과를 추정 가능하고 목표에 맞는 변화를 시도 가능하다.
  - XP(eXtreme Programming)
    - 의사소통, 피드백, 단순함, 용기, 존중에 가치를 두고 있는 애자일 방법론
    - 고객의 참여, 짧은 개발 과정의 반복을 극대화하는 방법
  - 단순하게 둘 다 애자일 방법론이라는 공통점이 있고 스크럼은 팀에, XP는 고객에 더 중점을 둔다고 생각하면 된다.



- XP의 5가지 가치와 12가지 원리
  - 5가지 가치
    - 용기: 자신감 있게 개발하고, 피드백을 수용, 리팩토링.
    - 단순성: 필요한 것만 개발.
    - 의사소통: 개발자, 관리자, 고객 사이의 원활한 소통
    - 피드백: 빠른 피드백
    - 존중: 팀원 사이의 존중
  - 12가지 원리
    - Pair programming: 개발자 두 명이 짝을 이뤄 개발.
    - Collective Ownership: 코드는 공동으로 소유하며, 누구든지 언제라도 수정 가능.
    - Continuous Integration: 매일 여러 번씩 소프트웨어를 통합하고 빌드한다.
    - Planning process: 고객의 요구를 정의하고, 개발자가 필요한 것과, 어떤 부분에서 지연될 수 있는지를 고객에게 알려줘야 한다.
    - Small release: 작은 시스템을 먼저 만들고, 짧은 주기로 업데이트 한다.
    - Metaphor: 고객과 개발자 사이의 원활한 의사소통을 위해 공통의 이름 체계와 시스템 서술서를 만든다.
    - Simple design: 가장 단순한 시스템을 설계한다.
    - TDD: 테스트 코드를 먼저 작성하고, 테스트를 통과할 수 있도록 코드를 작성한다.
    - Refactoring
    - 40-Hour Work: 개발자가 피곤으로 실수하지 않도록 주 40시간 이상 근무해선 안된다.
    - Coding Standard: 효과적인 공동 작업을 위해 모든 코드에 대한 코딩 표준을 정의해야 한다.
    - On Site Customer: 개발자들의 질문에 즉각 대답해 줄 수 있는 고객을 프로젝트에 풀 타임으로 상주시켜야 한다.



- Lean 개발 방법론
  - 도요타 생산 시스템의 기법을 소프트웨어에 적용한 방법론
  - 정의: 프로젝트를 수행할 때 발생할 수 있는 모든 낭비를 제거하는 기법
  - 7가지 개발 원칙
    - 낭비의 제거: 불필요한 코드나 불분명한 요구사항, 느린 커뮤니케이션, 관료적 습관 등 상품의 가치에 영향을 미치지 않는 모든 것을 제거
    - 품질 내재화
    - 배움 증폭: 프로젝트 진행 기간에도 학습할 필요가 있음
    - 늦은 결정: 중요한 문제에 대한 의사 결정을 최대한 미룸
    - 빠른 인도: 최대한 빨리 결과물을 제공, 고객이 요구사항을 변경할 시간을 주지 않음, 고객이 결점을 발견할 수 있는 시간 제공
    - 사람 존중
    - 전체를 최적화: 모든 프로세스를 최적화
  - 일본 업계에 등장한 품질 관리론
    - 생산이 아닌 유지 보수에 초점을 맞췄다.
    - 점차 발전하여 유지 보수가 쉬운 생산 과정을 만드는 것으로 이어졌다.
  - 5S원칙
    - Lean의 토대가 되는 원칙으로 원래 TPM의 원칙이었다.
    - 정리(Seiri, 조직 혹은 체계화): 적절한 명명법 과 같은 방법을 통해 무엇이 어디에 있는지 알아야 한다.
    - 정돈(Seiton, 단정함 혹은 체계화): 코드는 누구나 예상하는 위치에 있어야 한다,
    - 청소(Seiso, 정리 또는 광내기): 불필요한 코드는 주석으로 남겨두지 말고 제거한다.
    - 청결(Seiketsu, 표준화): 그룹 내에서 동의한 표준화된 방식으로 작업 공간을 정리한다. 
    - 생활화(Shutsuke, 규율): 관례를 따르고, 자기 코드를 자주 되돌아보고, 기꺼이 변경하는 것을 생활화한다.





# 소프트웨어 개발 단계

## 프로세스

- 프로제스
  - 정의: 일이 처리되는 과정이나 공정, 주어진 일을 해결하기 위한 목적으로 그 순서가 정해져 수행되는 일련의 절차
  - 목적: 이전에 얻은 노하우를 바탕으로 시행착오를 감소시켜 빠르게 개발하기 위함, 가이드 역할



- 소프트웨어 프로세스의 정의

  - 작업(task):SW를 개발할 때 일을 수행하는 작은 단위
  - 작업(task) 순서의 집합+제약 조건(일정, 예산, 자원)을 포함하는 일련의 활동(activity)

  - 좁은 의미의 소프트웨어 개발 프로세스
    - SW 제품을 개발할 때 필요한 절차, 과정, 구조
    - 사용자의 요구사항을 SW시스템으로 구현하기 위한 일련의 활동
  - 넓은 의미의 소프트웨어 개발 프로세스
    - 절차, 구조, 방법, 도구, 참여자까지 모두 포함
    - SW개발 목적을 이루는데 필요한 통합적 수단



- 소프트웨어 프로세스 모델
  - 정의
    - SW를 어떻게 개발할 것인가에 대한 전체적인 흐름을 체계화한 개념
    - 공장에서 제품을 생산하듯이 소프트웨어 개발의 전 과정을 하나의 프로세스로 정의한다.
    - 주어진 예산과 자원으로 개발하고 관리하는 방법을 구체적으로 정의한다.
  - 특징
    - 개발 계획 수립부터 최종 폐기때까지의 전 과정을 다룬다.
    - 순차적인 단계로 이루어진다.
  - 목적
    - 궁극적으로 고품질의 소프트웨어 제품 생산을 목적으로 한다.
  - 역할
    - 프로젝트에 대한 전체적인 기본 골격을 세워준다.
    - 일정 계획을 수립할 수 있다.
    - 개발 비용을 포함한 여러 자원을 산정하고 분배할 수 있음
    - 참여자 간에 의사소통의 기준이 될 수 있다.
    - 용어의 표준화를 가능케 한다.
    - 개발 진행 상황을 명확히 파악 가능하다.
    - 각 단계 별로 생성되는 문서를 포함한 산출물을 활용하여 검토할 수 있게 해준다.



## 소프트웨어 개발 계획(무엇을 만들 것인가)

- 소프트웨어 개발 계획
  - 소프트웨어 개발에 필요한 비용, 기간, 자원에 대한 계획을 세우는 것
  - 계획 없는 소프트웨어 개발은 일정 지연, 비용 초과, 품질 저하, 유지보수 비용 증가 등의 문제가 발생할 수 있다.



- 문제의 정의
  - 무엇을 개발할 것인가를 결정
  - 개발의 범위를 결정
  - 프로젝트의 초기 타당성과 초기 계획을 작성할 수 있는 기초로 활용



- 타당성 분석
  - 경제적 타당성(투자 효율성, 시장성, 이 소프트웨어가 과연 팔릴지에 대한 고민)
  - 기술적 타당성(구현 가능성, 하드웨어 성능, 개발자의 기술력)
  - 법적 타당성(개발용 소프트웨어와 도구의 사용에 대한 법적 문제 검토, 지적 소유권과 프로그램 보호범에 대한 검토)



- 개발비 산정
  - 소프트웨어 개발 비용 예측은 개발자의 능력에 따라 생산성의 차이가 난다.
  - 다양한 개발 프로세스로 인한 표준화/자동화가 어렵다.
  - 위와 같은 이유들 때문에 명확한 개발비 산출이 어렵다.



- 소프트웨어 개발 비용에 영향을 주는 요소
  - 프로그래머의 자질: 초급 프로그래머와 고급 프로그래머의 생산성 차이
  - 소프트웨어 복잡도: 복잡도가 증가할 수록 개발 비용도 증가
    - 소프트웨어 크기: 크기가 증가하면 참여 인원이 증가하고 개발 기간도 길어지고 복잡도도 증가한다.
  - 가용 기간: 개발 가능한 기간, 관리자들의 잘못된 생각으로 인력/자원의 증가가 개발 기간을 단축시킨다고 생각한다.
    - 브룩스의 법칙: 지연되는 프로젝트에 인력을 더 투입하면 오히려 더 늦어진다는 이론. 3명이서 개발을 할 때에는 3명이서만 의사소통을 하면 되지만 한 명이 더 추가되면 4명이서 의사소통을 해야 하므로 의사소통의 복잡도가 증가하게 된다.
  - 요구되는 신뢰도 수준: 높은 신뢰도의 소프트웨어 개발은 개발 비용을 증가시킨다.
  - 기술 수준: 고급 언어를 사용할 경우 생산성이 증가한다.



- 개발비 산정 기법
  - 하향식 산정 기법
    - 전문가 판단 기법
    - 경험이 많은 전문가가 개발 비용을 산정
    - 짧은 시간에 개발비를 산정하거나 입찰에 응해야 하는 경우 많이 사용
    - 수학적 계산 방법보다 경험에만 의존할 경우 부정확 할 수 있음
    - 델파이 기법(전문가 합의법): 어떤 문제의 해결과 관계된 미래 추이의 예측을 위해 전문가 패널을 구성하여 수회 이상 설문하는 정성적 분석 기법

  - 상향식 산정 기법
    - 세부 작업 단위별로 비용 산정한 후 전체 비용 합산
    - 원시 코드라인 수(LOC) 기법: 원시 코드 라인 수의 비관치, 낙관치, 중간치를 측정 후 예측치를 구해 비용 산정
    - 개발 단계별 노력(effort per task) 기법: 생명주기의 각 단계별로 노력을 산정
  - 수학적 산정 기법
    - 상향식 비용 산정 기법의 하나
    - 경험적 추정 기법 또는 실험적 추정 기법
    - COCOMO 방법: SW 규모를 예측한 후 각 비용 산정 공식에 대입하여 비용 산정
    - Putnam 방법: 소프트웨어 생명 주기의 전 과정에 사용될 노력의 분포를 가정해준다.
    - 기능 점수(FP) 방법: 기능 점수를 구한 후 이를 이용해 비용 산정



- 일정 계획
  - 작업 순서, 소작업 개발 기간과 순서 등을 정한다.
  - 작업 분할 구조도(WBS, Work Breakdown Structure)
    - 프로젝트 목표를 달성하기 위해 필요한 활동과 업무를 세분화
    - 프로젝트 구성 요소들을 계층 구조로 분류
  - PERT/CPM
    - WBS의 작업 순서, 소요 기간 등을 네트워크 형태의 그래프로 표현
    - 어떤 작업이 중요한지, 일정에 여유가 있는 작업은 어떤 것인지 찾아내 중점 관리 해야 하는 작업을 명확히 하는데 사용
  - 간트 차트(Gantt chart)
    - 프로젝트 일정 관리를 위한 바 형태의 도구
  - WBS로 분석->PERT/CPM로 시각화->간트 차트로 정리



- 위험 관리 절차
  - 위험 요소 식별/위험 분석
    - 위험 요소가 발생할 가능성과 영향력을 판단
    - 과거 프로젝트의 데이터와 위험을 분석한 경험이 많은 개발자에 의존
  - 위험 계획 수립
    - 위험을 처리하는 위험 대응 방안 수립
  - 위험 감사
    - 식별된 위험 요소의 발생 확률과 변화 등을 관리
    - 예측한 위험의 실제 발생 여부 확인



- 요구 사항과 요구 분석 명세서

  - 고객 만족을 위한 분석 과정
    - 적시성
    - 유연성
    - 통합
  - 고객 만족의 개발 조건
    - 고품질
    - 정해진 기간
    - 주어진 예산
  - 요구사항: 사용자와 개발자 간에 합의한 개발 범위에서 시스템이 제공해야 하는 기능
  - 요구 분석 명세서: 개발 초기에 사용자의 요구 사항(비기능 요구 사항 포함)을 추출하여 정리한 문서
  - 요구 분석 절차
    - 자료 수집: 현행 시스템 파악, 실무 담당자 인터뷰
    - 요구 사항 도출: 수집한 자료를 바탕으로 요구 사항 도출
    - 문서화: 요구 분석 명세서 작성
    - 검증: 요구 분석 명세서 검토: 모순 사항, 빠뜨린 사항 등 점검

  - 요구 사항의 범위
    - 기능적 요구 사항
    - 비기능적 요구 사항: 품질, 제약 사항
    - 사용자 요구사항
    - 시스템 요구 사항
  - 품질
    - 신뢰성: 소프트웨어가 고장 없이 동작하는 것
    - 신뢰도 측정: 고장 간 평균 시간(MTBF)과 이용 가능성(가용성)을 척도로 사용
    - MTBF=MTTF+MTTR
    - MTBF(Mean TIme Between Failure, 고장 간 평균 시간): 고장에서 다음 고장까지의 평균 시간
    - MTTF(Mean Time To Failure, 평균 실패 시간): 수리한 후 다음 고장까지의 평균 시간
    - MTTR(Mean Time To Repair, 평균 수리 시간): 고장 발생 시점에서 수리 시까지의 평균 시간
    - 이용 가능성 = MTTF/(MTTF+MTTR)*100%
    - 이용 가능성: 주어진 시점에서 프로그램이 요구에 따라 작동되고 있을 가능성 
  - 성능
    - 사용자가 시스템에 어떤 요구를 했을 때 해당 기능을 정상적으로 수행하는 것은 물로 사용자가 원하는 조건(응답 시간, 데이터의 처리량 등)을 만족시키는 것
    - 보안성: 인증을 받지 않은 사람이 시스템에 접근하는 것을 막아 시스템과 데이터를 보호
    - 안전성: 작동하는 모든 시스템이 소프트웨어 오류로 인해 인명 피해가 발생하지 않아야 함
    - 사용성: 소프트웨어를 사용할 때 혼란스러워하거나 사용하는 순간에 고민하지 않게 하는 편의성



- 보안 취약성 식별
  - 보안 취약성의 개념
    - 정보 시스템이 불법적인 사용자의 접근을 허용할 수 있는 위협.
    - 정보 시스템의 정상적인 서비스를 방해하는 행위.
    - 정보 시스템에서 관리하는 중요 데이터의 유출, 변조, 삭제에 대한 위협
  - 침투 테스트
    - 정찰: 목표 애플리케이션에 관련된 정보를 수집
    - 탐색: 애플리케이션을 검사하여 보안 위협에 관련된 상세 정보를 확인
    - 접근 권한 획득: 애플리케이션의 허점을 찾아내어 악성 코드를 삽입하여 데이터에 접근할 수 는 권한을 획득 후 이를 이용한 공격을 수행
    - 엑세스 유지: 애플리케이션 내에 접근 권한을 계속 유지하여 다수의 공격 테스트 수행
    - 추적 방지: 공격자는 자신의 흔적을 남기지 않도록 로그, 수집된 데이터 등의 접근 이력을 모두 제거
  - 취약성 공격
    - 보안 버그나 잘못된 설정 등 결함을 공격하여 공격자가 원하는 결과를 얻기위한 코드, 프로그램, 스크립트 또는 이를 이용하는 행위를 의미한다.
    - 취약성 공격의 목표는 대상 시스템을 장악하여 정보를 빼내거나 혹은 다른 용도로 악용하기 위함이다.
    - 기존 취약점 공격과는 달리 피해 시스템의 중요 데이터를 암호화하여 인질로 삼고 금전을 요구하는 랜섬웨어도 취약점 공격을 통해 권한을 획득하는 것이다.
  - 취약성에 따른 공격 기법
    - 서비스 거부(DoS): 무의미한 서비스 요청 등의 반복을 통해 특정 시스템의 가용자원을 소모시켜 서비스 가용성을 저하사키는 공격 기법
    - 코드 실행: 응용 프로그램이 적절한 입력 유효성 검사 없이 쉘 명령을 실행하는 취약점을 이용하여 공격자가 원하는 임의 코드가 실행되도록 하는 공격 기법
    - 버퍼 오버플로우: 정해진 메모리의 범위를 넘치게 해서 원래의 리턴 주소를 변경시켜 임의의 프로그램이나 함수를 실행시키는 해킹 기법
    - 정보 수집: 공격 전 서버 또는 시스템의 취약점, 네트워크 경로, 방화벽 설치 유무를 알아내고 정보를 수집하는 공격 기법
    - 권한 상승: 악성프로그램 설치 후 데이터 조회, 변경, 삭제 등을 통한 권한 상승으로 루트 권한을 획득하는 공격 기법
    - SQL 인젝션: 데이터베이스와 연동된 웹 애플리케이션에서 공격자가 입력 폼 및 URL 입력란에 SQL문을 삽입하여 DB로부터 정보를 열람할 수 있는 공격 기법
    - 크로스 사이트 스크립팅(XSS): 공격자가 게시판에 악성 스크립트를 작성, 삽입하여 사용자가 그것을 보았을 때 이벤트 발생을 통해 사용자의 쿠기 정보, 개인 정보 등을 특정 사이트로 전송하는 공격기법
    - 사이트 간 요청 위조 공격(CSRF): 웹 사이트 취약점 공격의 하나로, 사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위를 특정 웹 사이트에 요청하게 하는 공격기법
    - 디렉터리 접근: HTTP 기반의 공격으로 액세스가 제한된 디렉터리에 접근하여, 서버의 루트 디렉터리에서 외부 명령을 실행하여 파일, 웹소스 등을 강제로 내려 받을 수 있는 공격기법
  - 시큐어 코딩
    - 소프트웨어 개발 과정에서 개발자의 실수, 논리적 오류 등으로 인해 SW에 내포될 수 있는 보안 취약점을 최소화.
    - 안전한 SW를 개발하기 위한 일련의 활동





- 소프트웨어 개발에서의 모델
  - SW 개발에 여러 관점의 모델을 사용, UML 다이어그램 등을 이용하여 표현
  - 모델링 언어: 애매모호한 표현 등의 문제점을 해결하기 위해 모델링을 할 때 사용하는 기호, 표기법, 도구
  - 개발 방법론에 따른 모델링 언어
    - 구조적 방법론: DFD(Data Flow Diagram), DD(Data Dictionary), 프로세스 명세
    - 정보공학 방법론: DB 설계 시 표현은 ERD(Entity Relationship Diagram)
    - 객체 지향 방법론: UML(유스케이스 다이어그램) 표기법
  - 장점
    - 개발될 소프트웨어에 대한 이해도 향상
    - 이해 당사자 간의 의사소통 향상
    - 유지보수 용이
  - 단점
    - 과도한 문서 작업으로 인한 일정 지연 가능성
    - 형식적인 산출물로 전락할 가능성





## 소프트웨어 설계(어떻게 만들 것인가)/구현/테스트

### 설계

- 설계의 종류
  - 상위 설계
    - 아키텍처(구조) 설계: 시스템의 전체적인 구조
    - 데이터 설계: 시스템에 필요한 정보를 자료구조와 데이터베이스 설계에 반영
    - 시스템 분할: 전체 시스템을 여러 개의 서브 시스템으로 나눈다.
    - 인터페이스 정의: 시스템 구조와 서브 시스템들 사이의 인터페이스가 명확히 정의
    - UI 설계: 사용자가 익숙하고 편리하게 사용할 수 있도록 사용자 인터페이스 설계
  - 하위 설계
    - 각 모듈의 실제적인 내부를 알고리즘(Pseudo-code) 형태로 표현
    - 인터페이스에 대한 설명, 자료구조, 변수 등에 대한 상세한 정보를 작성



- 아키텍처 정의
  - 구성 요소
  - 구성 요소들 사이의 관계
  - 구성 요소들이 외부에 드러내는 속성
  - 구성 요소들과 주변 환경 사이의 관계
  - 구성 요소들이 제공하는 인터페이스
  - 구성 요소들의 협력 및 조립 방법



- 소프트웨어의 아키텍처
  - 소프트웨어의 전체적인 구조
  - 소프트웨어를 이루고 있는 여러 구성 요소
  - 구성 요소들의 인터페이스 간의 상호작용을 정의
  - 시스템 설계와 개발 시 적용되는 원칙과 지침



- 아키텍처 품질 속성
  - 시스템 품질 속성: 가용성, 변질 용이성, 성능, 보안성, 사용성, 테스트 용이성 등
  - 비즈니스 품질 속성: 시장 적시성, 비용과 이익, 예상 시스템 수명, 목표 시장, 신규 발매 일정 또는 공개 일정, 기존 시스템과의 통합
  - 개념적 무결성: 일관성
  - 정확성과 완전성: 사용자가 요구 하는 기능을 충족시키는 정도
  - 개발 용이성(구축 가능성): 정해진 기간 내에 완성하고, 개발 과정 중에 쉽게 변경가능 



- 아키텍처 구축 절차
  - 요구 사항 분석: 기능적, 비기능적 요구 사항 분류 및 명세
  - 아키텍처 분석
  - 아키텍처 설계: 관점 정의, 아키텍처 스타일 선택, 후보 아키텍처 도출
  - 검증 및 승인: 아키텍처 평가, 아키텍처 상세화(반복), 아키텍처 승인



- 아키텍처 모델
  - 데이터 중심형 모델
    - repository model
    - 주요 데이터를 repository 에서 중앙 관리
    - repository 와 여기에 접근하는 서브 시스템으로 구성
    - 데이터가 한 곳에 모여 있기에 데이터를 모순되지 않고 일관성 있게 관리 가능
    - 새로운 서브시스템 추가 용이
    - repository의 병목 현상 발생 가능
    - 서브 시스템과 repository  사이의 강한 결합으로 repository 변경 시 서브 시스템에 영향을 준다.
  - Client-Server 모델
    - 네트워크를 이용하는 분산 시스템 형태
    - 데이터와 처리 기능을 클라이언트와 서버에 분할하여 사용
    - 분산 아키텍처에 유용
    - 서버: 클라이언트(서브시스템)에 서비스 제공
    - 클라이언트: 서버가 제공하는 서비스를 요청(호출) 하는 서브 시스템
  - Layering 모델
    - 기능을 몇 개의 계층으로 나누어 배치
    - 구성: 하위 계층은 서버, 상위 계층은 클라이언트 역할
  - MVC(Model View Controller) 모델
    - 중앙 데이터 구조
    - 같은 모델의 서브 시스템에 대하여 여러 뷰 서브 시스템을 필요로 하는 시스템에 적합
    - 장점: 데이터를 화면에 표현 하는 디자인(V)과 로직(M)을 분리함으로써 느슨한 결함 가능, 구조 변경 요청 시 수정 용이
    - 단점: 기본 기능 설계로 인한 클래스 수의 증라로 복잡도 증가, 속도가 중요한 프로젝트에 부적합



- 디자인 패턴
  - 자주 사용하는 설계 형태를 정형화해서 이를 유형별로 설계 템플릿을 만들어둔 것
  - 많은 개발자들이 경험상 체득한 설계 지식을 검증하고 이를 추상화하여 일반화한 템플릿
  - 장점
    - 개발자 간의 원활한 의사소통
    - 소프트웨어 구조 파악 용이
    - 재사용을 통한 개발 시간 단축
    - 설계 변경 요청에 대한 유연한 대처
  - 단점
    - 객체지향 설계/구현 위주
    - 초기 투자 비용 부담
  - GoF(Gang of Fours) 디자인 패턴
    - Creational Pattern: 객체를 생성하는데 관련된 패턴들, 객체가 생성되는 과정의 유연성을 증가시키고 코드 유지를 쉽게 한다.
    - Structural Pattern: 프로그램 구조에 관련된 패턴들, 프로그램 내의 자료구조나 인터페이스 구조 등 프로그램의 구조를 설계하는데 활용할 수 있는 패턴들
    - Behavioral Pattern: 반복적으로 사용되는 객체들의 상호작용을 패턴화 해놓은 것들

- 재사용
  - 재사용의 개념
    - 목표 시스템의 개발 시간 및 비영 절감을 위하여 검증된 기능을 파악하고 재구성하여 시스템에 응용하기 위한 최적화 작업
    - 기존의 소프트웨어 또는 소프트웨어 지식을 활용하여 새로운 소프트웨어를 구축하는 작업이다.
  - 재사용의 유형
    - 함수와 객체 재사용: 클래스나 함수 단위로 구현한 소스 코드를 재사용
    - 컴포넌트 재사용: 컴포넌트 단위로 재사용, 컴포넌트의 인터페이스를 통해 통신
    - 애플리케이션 재사용: 공통기능 제공 애플리케이션과 기능을 공유하여 재사용
    - 프레임워크, 라이브러리, 아키텍처 등이 재사용 사례이다.
  - 코드 재사용
    - 프로그램의 일부 또는 전부를 이후의 다른 프로그램을 만들 때 사용하는 기법이다.
    - 코딩 작업에 소비하는 시간과 에너지를 절약하는 전형적인 기법이다.
    - 프로그램 이전 버전에서 시작해 다음 버전을 개발하는 작업도 코드 재사용에 속한다.
    - 기존 프로그램에서 코드를 일부 또는 전체를 추출하여 새로운 프로그램에 복사할 경우 중복 코드로 인한 문제가 발생할 수 있다.
  - 재사용 프로그래밍 기법
    - 객체지향 프로그래밍: 객체 단위로 재사용이 이루어지도록 설계.
    - 제네릭 프로그래밍: 하나의 값이 여러 데이터 타입을 가질 수 있음, 이를 통해 재사용성을 높일 수 있다.
    - 자동 프로그래밍: 사용자가 설정 변수에 근거한 프로그램 생성.
    - 메타 프로그래밍: 런타임에 수행해야 할 작업의 일부를 컴파일 타임 동안 수행하는 프로그램.



### 모듈화

- 모듈화
  - 정의
    - 소프트웨어 개발에서 큰 문제를 작은 단위로 나누는 것
    - 프로그램의 효율적 관리를 위해 시스템을 분해하고 추상화함으로써 소프트워에어의 성능을 향상시키거나 시스템의 수정 및 재사용, 유지 관리를 쉽게 하는 기법.
  - 모듈
    - 프로그램을 구성하는 구성 요소의 일부로, 관련된 함수난 변수 또는 클래스를 모아 놓은 파일.
    - 모듈은 다른 프로그램에서 불러와서 사용할 수 있다.
  - 목적
    - 프로그램 개발 시 생산성과 최적화, 관리에 용이하게 기능 단위로 분할하는 기법.
    - 프로그램을 구성하는 데이터와 함수들을 묶어서 모듈을 형성한다.
  - 특징
    - 다른 것들과 구별되는 독립적인 기능
    - 독립적으로 컴파일
    - 유일한 이름을 지님
    - 모듈에서 또 다른 모듈을 호출
    - 다른 프로그램에서도 모듈을 호출
  - 모듈화의 원리
    - 정보 은닉: 어렵거나 변경 가능성이 있는 모듈을 타 모듈로부터 은폐
    - 분할 정복: 복잡한 문제를 분해, 모듈 단위로 문제 해결
    - 데이터 추상화: 각 모듈 자료 구조를 액세스하고 수정하는 함수 내에 자료 구조의 표현 내역을 은폐
    - 모듈 독립성: 낮은 결합도와 높은 응집도를 가진다.
  - 모듈 개수 및 비용간의 상관관계
    - 모듈의 크기가 너무 작아 모듈 개수가 많아지면 모듈 간 통합 비용이 많이 발생한다.
    - 모듈의 크기가 너무 크면 모듈 간의 통합 비용이 줄어드는 대신 모듈 당 개발 비용이 상승한다.
  - 모둘화 측정 지표
    - 결합도와 응집도로 모듈화 적정성을 측정한다.
    - 좋은 모듈화란 용도에 맞게 잘 구분된 기능을 가진 모듈들로 세분화하는 것이다.
    - 개별 모듈은 독립적으로 주어진 역할 만을 수행하며, 타 모듈에 의존성이 높지 않아야 한다.



- 모듈화의 유형
  - 설계 측면
    - 모듈: 설계 시 연관 기능을 한 부분에 모아 놓고 라이브러리 형태로 사용
    - 컴포넌트: 바이너리 형태의 재사용 가능한 형태, 인터페이스에 의해 로직을 수행할 수 있는 모듈 단위
    - 서비스: 기존 컴포넌트보다는 느슨한 결합(다른 클래스를 직접적으로 사용하는 클래스의 의존성을 줄여 코드 재사용성과 유연성을 높인 기법) 형태의 기능을 제공하는 모듈 단위.
  - 구현 측면
    - 매크로: 프로그램의 반복되는 부분을 특정 이름을 부여하고 실행할 수 있도록 하는 기법
    - 함수: 프로그램 구현 시 커다른 프로그램의 일부 코드로 특정한 작업을 수행하고 상대적으로 다른 코드에 비해 독립적인 모듈
    - 인라인: 프로그램 구현 시 반복되는 부분을 특정 이름을 부여하여 실행할 수 있도록 하는 프로그램 기법



- 응집도

  - 정의
    - 모듈 내부에 존재하는 구성 요소들 사이의 밀접한 정도
    - 예를 들어 계산기라는 하나의 모듈 내에 덧셈 함수, 뺄셈 함수 등이 있는 것은 응집도가 높은 것이지만, 다른 국가의 시간을 출력하는 기능이 들어간다면 응집도가 낮은 모듈이라 할 수 있다.
    - 정보 은닉 개념의 확장 개념으로, 하나의 모듈은 하나의 기능을 수행하는 것을 의마한다.
    - 높을 수록 바람직한 설계라고 할 수 있다.
- 특징
  - 유사기능 영역구성: 클래스 목적에 부합하는 같은 기능영역의 함수들로 구성
  - 단일 책임할당: 함수의 개수가 상대적으로 적고 오로지 자신만이 할 수 있는 책임을 할당받는다.
  - 함수 간 상호협력: 하나의 함수에 많은 기능을 넣지 않고 다른 함수와 협력
  - 유형(낮은 응집도 순)
    - 우연적 응집: 모듈 내부의 각 구성요소들이 연관이 없을 경우.
    - 논리적 응집: 유사한 성격을 갖거나 특정 형태로 분류되는 처리 요소들이 한 모듈에서 처리되는 경우
    - 시간적 응집: 연관된 기능이라기보다는 특정 시간에 처리되어야 하는 활동들을 한 모듈에서 처리할 경우
    - 절차적 응집: 모듈이 다수의 관련 기능을 가질 때 모듈 안의 구성요소들이 그 기능을 순차적으로 수행할 경우
    - 통신적 응집: 동일한 입력과 출력을 사용하여 다른 기능을 수행하는 활동들이 모여 있을 경우
    - 순차적 응집: 모듈 내에서 한 활동으로부터 나온 출력값을 다른 활동이 사용할 경우
    - 기능적 응집: 모듈 내부의 모든 기능이 단일한 목적을 위해 수행되는 경우



- 결합도
  - 정의
    - 모듈과 모듈 사이의 관계에서 관련된 정도
    - 모듈 내부가 아닌 외부의 모듈과의 연관도 또는 모듈간의 상호 의존성이다.
    - 낮을 수록 바람직한 설계라고 할 수 있다.
  - 특징
    - 모듈 연관성 없음: 서로 다른 상위 모듈에 의해 호출되어 처리상 연관성이 없는 다른 기능을 수행
    - 인터페이스 의존성: 자료전달이 인터페이스를 통과하여 인터페이스 복잡성에 의존적
    - 복잡성 감소: 낮은 결합도를 통해 복잡성 감소
    - 파급효과 최소화: 에러 발생 시 오류가 전파되어 다른 오류의 원인이 되는 파급효과를 최소화
  - 유형(높은 결합도 순)
    - 내용 결합도: 다른 모듈 내부에 있는 변수나 기능을 다른 모듈에서 사용하는 경우
    - 공통 결합도: 파라미터가 아닌 모듈 밖에 선언되어 있는 전역 변수를 참조하고 전역 변수를 갱신하는 식으로 상호 작용하는 경우
    - 외부 결합도: 모듈이 다수의 관련 기능을 가질 때 모듈 안의 구성요소들이 그 기능을 순차적으로 수행할 경우
    - 제어 결합도: 단순 처리할 대상인 값만 전달되는 게 아니라 어떻게 처리를 해야 한다는 제어 요소가 전달되는 경우
    - 스탬프 결합도: 모듈 간의 인터페이스로 배열이나 객체, 구조 등이 전달되는 경우
    - 자료 결합도: 모듈 간의 인터페이스로 전달되는 파라미터를 통해서만 모듈 간의 상호작용이 일어나는 경우



- 형태
  - 용도가 비슷한 것끼리 묶어놓은 라이브러리 함수, 그래픽 함수 등
  - 추상화된 자료 등
- 장점
  - 분할정복의 원리가 적용
  - 용이성 증대
  - 성능 향상
  - 복잡도 감소
  - 유지보수 용이
  - 오류로 인한 파급 효과를 최소화
  - 설계 및 코드를 재사용
  - 기능의 분리가 가능하고 인터페이스가 단순해진다.



- 방법론
  - 프로세스 지향 방법
    - 처리순서를 구조화하는 방법
    - 대표적인 모델 기법: DFD(Data Flow Design)
    - 기능이 중심(우선)이 되고 그 기능을 수행하는 데 필요한 데이터가 참조되는 형태로 구성
    - 프로세스와 데이터의 분리
    - 실세계를 컴퓨터 처리 방식으로 표현
    - 함수 중심(우선) 으로 모듈 구성
  - 데이터 지향 방법
    - 시스템이 취급하는 데이터에 관심
    - 즉 데이터가 중심(우선)이 되어 데이터를 구조화
    - 대표적인 SW 개발 방법론: 정보 공학 방법론
    - DB 설계를 위한 대표적 모델 표기법: E-R(Entity-Relationship) 다이어그램
  - 위 두 방법의 문제점
    - 변경이 미치는 영향이 크다: 프로세스와 데이터를 별개의 것으로 파악하기 때문
    - 프로그램의 복잡도 증가: 함수와 데어타가 분리되어 있기 때문
    - 프로그램 변경 시 프로그램 구조 파악 필요: 프로그래머는 프로그램의 구조와 영향을 미치는 곳도 파악해야 함
    - 재사용의 어려움: 프로세스와 데이터가 분리된 구조 때문
  - 객체 지향 방법
    - 위 문제점을 해결하기 위해 고안
    - 기능이나 데이터 대신 객체가 중심이 되어 개발
    - 데이터를 가장 먼저 찾고 그 데이터를 조작하는 메서드를 찾아 그 둘을 객체라는 이름으로 묶어 그 객체를 중심으로 모듈을 구성
    - 실세계를 사람이 생각하는 방식으로 표현한다.
    - 임의로 데이터에 접근할 수 없다.
    - 시스템은 객체들의 모임이다.
    - 요구 사항 변경에 유연한 대처가 가능하다.
    - 확장성과 재사용성이 높아진다.
    - 추상화를 통해 생산성과 품질이 향상된다.



### 구현

- 프로그래밍 언어 선정
- 코딩 규칙 설정: 높은 가독성,  간결하고 명확한 코딩, 개발 시간의 단축



### 테스트

- 테스트의 정의
  - IEEE(I Triple): 테스트는 시스템이 명시된 요구를 잘 만족하는지, 즉 예상된 결과와 실제 결과가 어떤 차이를 보이는지 수동이나 자동으로 검사하고 평가하는 작업
  - Zoha Manna: 테스트는 시스템의 명세까지 완벽하게 옳다고 확신할 수 없고, 테스트 시스템 그 자체가 맞다고 증명할 수 없기 때문에 프로그램을 완전히 테스트 할 수 없다.
  - Dahl, Dijkstra, Hoare: 테스트는 결함이 있음을 보여줄 뿐, 결함이 없음을 증명할 수는 없다.



- 결함과 오류
  - 오류: 소프트웨어 개발자에 의해 만들어지는 실수로 결함의 원인이다.
  - 결함: 오류의 결과로 고장의 원인이다.
  - 고장, 실패, 문제, 장애: 시스템이 요구 사항대로 작동하지 않는 것



- 소프트웨어 테스트
  - 소프트웨어 내에 존재하지만 드러나지 않고 숨어 있는 오류를 발견할 목적
  - 개발 과정에서 생성되는 문서나 프로그램에 있는 오류를 여러 기술을 이용해 검출하는 작업
  - 오류를 찾아내 정상적으로 실행될 수 있도록 하는 정도지 완전히 오류를 없앨 수는 없다.



- 테스트의 목표
  - 좁은 의미
    - 원시 코드 속에 남아 있는 오류를 발견하는 것
    - 결함이 생기는 것을 예방하는 것
  - 넓은 의미
    - 고객의 요구를 만족시키는지 확인하는 것
    - 고객이 사용하기에 충분한 소프트웨어라는 것을 보여주는 것
    - 소프트웨어의 신뢰성을 높이기 위한 작업



- 테스트의 분류
  - 시각에 따른 테스트
    - 확인 테스트: 각 단계에서 개발자의 시각으로 테스트, 설계도 대로 만들었는지 테스트
    - 검증 테스트: 사용자 요구 사항대로 만들었는지 테스트, 사용자의 시각에서 테스트
  - 사용 목적에 따른 테스트
    - 운영 목적 적합성 테스트
    - 수정 용이성 테스트
    - 운영 지원 용이성 테스트
  - 프로그램 실행 여부에 따른 테스트
    - 정적 테스트: 프로그램을 실행시키지 않고 코드리뷰를 통해 오류를 찾는 방법
    - 동적 테스트: 프로그램을 실행하면서 오류를 찾는 방법





# 소프트웨어 품질

- 소프트웨어 품질
  - 정의: 사용자의 요구와 부합되는 정도
  - 개발자 관점에서의 좋은 소프트웨어
    - 결함 없는 프로그램
    - 요구 분석 명세서대로 만든 소프트웨어



- 품질 목표
  - 정확성: 요구 분석 명세서와 일치하는 정도
  - 신뢰성: 기능이 정확하고 일관성 있는 정도
  - 효율성: 최소의 시간과 저장 용량을 사용
  - 무결성: 허가 받은 사용자만 사용 가능
  - 접근 사용성: 사용자가 쉽게 사용 가능
  - 유지보수 용이성: 쉽게 변경할 수 있는 정도
  - 테스트 용이성: 쉽고 철저하게 테스트
  - 유연성: 새로운 기능의 추가 및 변경의 용이성
  - 이식성: 다른 하드웨어 환경에서 운영할 수 있게 변경이 용이
  - 재사용성: 시스템의 일부나 전체를 다른 애플리케이션에서 사용할 수 있는가
  - 상호운영성: 다른 소프트웨어와의 연계 및 결합하여 정보를 교환할 수 있는 정도



- 품질 특성
  - McCall: 제품 수정, 제품 변환, 제품 운영에 중점을 두고 품질을 정의
  - Gravin: 성능, 특성품질, 신뢰성, 일치성, 내구성, 서비스, 미적 감각, 지각적 부분에 중점을 두고 품질을 정의
  - Boehm: 이식성, 신뢰성, 효율성, 인간공학성, 테스트성, 이해성, 변경성 등에 중접을 두고 품질을 정의  



- 품질 평가 표준 모델
  - 제품 품질 특성 평가
    - 완성된 제품에 대한 평가
    - 각종 표준 기구에서 제시하는 모델을 소프트웨어 품질 평가에 사용
  - 프로세스 품질 평가
    - 소프트웨어 제품의 개발 프로세스 평가
    - 소프트웨어 개발 과정의 각 단계마다 평가
  - CMMI(Capability Marturity Model Integration)
    - 프로세스 품질 평가에 사용하는 모델
    - 기업에 표준 프로세스를 만들 수 있는 지침을 제시한다.
    - C(Capability, 능력): 개발 목표(주어진 기간, 정해진 비용, 품질)를 달성할 수 있는 힘
    - M(Maturity, 성숙도): 책임감 있는 조직으로서 개발 과정에서 객관적이고 정량적인 근거에 따라 프로세스가 측정되고 지속적인 개선이 이루어지는 조직인가 평가
    - M(Model, 모델): 프로세스를 감사(audit)하는 의미로 사용
    - I(Integration, 통합): 소프트웨어 개발 생명주기의 각 단계를 통합한 모델
  - SPICE(ISO 15504) 모델
    - 소프트웨어 프로세스 평가를 위한 프레임워크 제공
    - 정보 시스템 분야에 특화된 품질 표준이자 일종의 규격 역할



# 프로젝트 관리

- 프로젝트
  - 정의: 유일한 제품이나 서비스를 만들기 위해 일정한 기간을 정해놓고 수행하는 작업
  - 특징
    - 한시성: 일의 시작과 끝이 명확히 정해져 있다.
    - 유일성: 기간이 종료되어 만들어 내는 인도물을 유일하다
    - 참여자의 일시성: 참여 인력은 프로젝트 시작과 동시에 참여하고, 종료되면 해체된다.
    - 한정성: 프로젝트가 종료되면 사용된 자원은 원래의 위치로 돌아가던가 없앤다.



- PMBOK의 5가지 프로세스 그룹
  - 시작(intiating) 그룹: 범위 관리 착수 및 프로젝트를 구성하는 단계 정의 및 승인
  - 기획(planning) 그룹: 프로젝트 목표 설정 및 목표 달성을 위한 활동 계획과 예싼, 인력, 자원 등의 계획 수립
  - 실행(executing) 그룹: 핵심 프로세스는 프로젝트 계획을 실행하는 것
  - 통제(controlling) 그룹: 계획 대비 목표의 진척 상황을 주기적으로 감시하고 성과를 측정
  - 종료(closing) 그룹: 프로젝트 종료: 관리의 종료(구성원 평가), 계약 종료



- PMBOK의 (프로젝트 관리)9가지 관점
  - 통합: 프로젝트 헌장, 범위 진술서, 계획을 수립한다. 프로젝트 변화를 지시하고 관리하며 모니터하고 통제한다.
  - 범위: 기획, 정의, 작업분류체계(WBS) 작성, 비준 및 통제.
  - 시간: 정의, 연결, 자원 및 기간 추정, 일정 관리
  - 비용: 자원 기획, 비용 추정, 예산 및 통제
  - 인적 자원: 인적 자원 계획, 인력 충원, 인력 개발 및 프로젝트 팀 관리.
  - 통신: 커뮤니케이션 계획, 정보 제공, 성과 보고, 이해관계자 관리.
  - 위험: 리스크 계획 및 확인, 리스크 분석(양적, 질적), 리스크 대응(활동) 계획 및 리스크 모니터링 및 통제.
  - 조달: 획득 및 계약 계획, 판매자 대응 및 선택, 계약관리 및 계약 종료



- 정보시스템 감리
  - 정의: 감리발주자 및 피감리인의 이해관계로부터 독립된 자가 정보시스템의 효율성을 향상시키고 안전성을 확보하기 위하여 제3자적 관점에서 정보시스템의 구축 및 운영 등에 관한 사항을 종합적으로 점검하고 문제점을 개선하도록 하는 것.
    - 전자정부법에서 해당 내용에 대해 다루고 있다.
    - 소프트웨어의 개발 국한된 것이 아닌 소프트웨어 운영, 하드웨어를 포함한 전반적인 사항을 점검한다.
  - 목적
    - 정보시스템의 효과성 확보: 사전에 설정된 목표를 달성했는지 여부
    - 정보시스템의 효율성 확보: 응답 시간이 적절한가, 최대 처리량이 얼마인가, 자원 이용도는 얼마인가
    - 정보시스템 안정성 확보: 무결성, 가용성, 기밀성
    - 법적 요건의 준수 확인: 업무와 관련된 기준, 규정, 정보화사업 추진과 관련된 규정 등
  - 감리 대상
    - 정보시스템의 구축 및 운영 전반
    - DB 구축사업
    - 운영사업
    - 유지 보수 사업
    - ISP 사업(인터넷 서비스 제공 사업)
    - ITA 사업(정보 기술 아키텍처 사업) 등
