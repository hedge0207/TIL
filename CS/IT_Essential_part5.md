# Load Balancing algorithm

> https://www.designgurus.io/course-play/grokking-system-design-fundamentals/doc/641db0dec48b4f7de900fd04

- Round Robin
  - 가용한 server에 request를 순차적으로 분산하는 방식이다.
    - 가장 단순한 load balancing algorithm 중 하나이다.
  - 장점
    - 구현이 쉽다.
    - Server들의 처리 능력이 비슷할 경우 잘 동작한다.
  - 단점
    - Server들의 처리 능력이 각기 다를 경우 잘 동작하지 않을 수 있다.
    - Server health나 response time에 대해서는 고려하지 않는다.



- Least Connections
  - Request가 들어왔을 때 활성화된 connection이 가장 적은 server로 요청을 보내는 방식이다.
    - 예를 들어 A, B 두 개의 server가 있다고 가정하자.
    - 새로운 request가 들어왔을 때, A에는 2개의 connection이, B에는 1개의 connection이 연결되어 있다.
    - 이 경우 connection이 가장 적은 B에 새로운 request를 전달한다.
  - 장점
    - Server마다 처리 능력이 다를 때 사용하기 좋다.
    - Request를 처리하는 데 걸리는 시간이 다양할 때 보다 효과적으로 부하를 분산할 수 있다.
  - 단점
    - 각 server마다 활성화된 connection의 수를 추적해야한다.
    - Server health나 상태를 고려하지 않는다.



- Weighted Round Robin
  - Round Robin algorithm을 확장한 것으로 각 서버의 처리 능력에 따라 server마다 다른 가중치를 부여하고, 이 가중치에 비례하여 request를 분산한다.
  - 장점
    - 구현이 쉽다.
    - 각 server의 각기 다른 처리량을 고려한다.
  - 단점
    - 가중치를 수동으로 할당하고 관리해야한다.
    - Server health나 response time을 고려하지 않는다.



- Weighted Least Connection
  - 할당된 가중치에 따라 활성 연결 비율이 가장 낮은 server로 request를 전달한다.
    - Least Connection과 Weighted Round Robin을 결합한 방식이다.
  - 장점
    - Server의 처리량과 활성 연결의 수를 모두 고려하므로, 부하 분산이 효율적으로 이루어진다.
    - 할당된 가중치에 따라 활성 연결 비율이 가장 낮은 server로 request를 전달한다.
  - 단점
    - 활성화된 connection 수와 가중치를 모두 추적해야한다.
    - Server health나 response time을 고려하지 않는다.



- IP Hash
  - Source IP 주소 혹은 destination IP 주소를 기반으로 어떤 server로 보낼지 결정한다.
    - 이 방식은 session 지속성(persistence)를 유지한다.
    - 즉 특정 IP에서 온 request는 같은 server로 전송된다.
  - 장점
    - Session 지속성을 유지할 수 있으므로, 특정 client와 특정 server가 반복적으로 연결되어야 하는 경우 유용하다.
    - Hash 함수만 잘 구현한다면 부하를 고르게 분산할 수 있다.
  - 단점
    - 적은 수의 client가 많은 수의 요청을 보내는 상황에서는 부하가 잘 분산되지 않을 수 있다.
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.



- Least Response Time

  - 응답 시간이 가장 짧고, 활성화된 connection의 개수가 가장 적은 server로 request를 전달한다.
    - 가장 빨리 응답을 줄 수 있는 server에 우선 순위를 주기에 사용자 경험을 최적화하는데 도움을 준다.
  - 장점
    - Server의 response time을 고려하여 사용자 경험을 향상시킬 수 있다.
    - 활성 connection과 response time을 모두 고려하므로 효율적인 부하 분산이 가능하다.

  - 단점
    - Server의 response time을 추적하고 monitoring해야한다.
    - Server health나 server 마다 각기 다른 처리 능력을 고려하지 않는다.



- Random
  - 무선적으로 아무 server에나 request를 전송한다.
    - 모든 server가 비슷한 처리 능력을 가지고 있고 session persistence가 필요하지 않을 때 유용하다.
  - 장점
    - 구현이 쉽다.
    - Server들의 처리 능력이 비슷할 경우 잘 동작한다.
  - 단점
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.
    - Session persistence가 요구되는 경우 사용할 수 없다.



- Least Bandwidth

  - Request가 들어왔을 때, 가장 가장 적은 대역폭을 사용하는 server로 request를 전달한다.

  - 장점
    - Network 대역폭을 고려하므로, network 자원을 관리하는 데 도움을 준다.
    - Server들이 각기 다른 대역폭을 가지고 있을 때 유용하다.
  - 단점
    - Server의 대역폭을 추적하고 monitoring해야한다.
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.



- Custom Load
  - 특정 요구사항이나 조건에 따라 직접 구현한 load balancing algorithm을 사용하는 방식이다.
    - Server health, 위치, 처리 능력 등을 고려할 수 있다.
  - 장점
    - 커스터마이징이 가능하므로 특정 use case에 맞는 부하 분산이 가능하다.
    - 여러 요소를 고려하여 구현할 수 있다.
  - 단점
    - 직접 개발하고 유지보수 해야 하므로 시간이 많이 든다.
    - 성능 최적화를 위해 많은 광범위한 test가 필요하다.





# Shorts

- Type system

  - 모든 프로그래밍 언어는 어떤 category에 속한 object가 어떤 작업을 할 수 있고, 어떤 category가 어떻게 처리될지를 형식화하는 type system을 가지고 있다.
  - Dynamic Typing
    - Type checking을 run time에 수행하고, 변수의 type이 변경되는 것을 허용하는 방식을 말한다.
    - 대표적으로 Python이 있는데, 아래 코드는 절대 error가 발생하지 않는다.

  ```python
  # 1과 "foo"를 더하는 것은 불가능하지만, 해당 코드는 실행되지 않으므로 에러가 발생하지 않는다.
  if False:
      1 + "foo"
  ```

  - Static Typing
    - Type checking을 compile time에 수행하고, 일반적으로 변수의 type 변경이 불가능하다.
    - 대표적으로는 Java가 있는데, 아래 코드는 compile time에 error가 발생한다.

  ```java
  String foo;
  foo = 1;
  ```



- duck typing

  > if it walks like a duck and it quacks like a duck, then it must be a duck
  >
  > 만일 어떤 것이 오리 처럼 걷고 오리처럼 꽥꽥거린다면, 그것은 오리일 것이다.

  - Duck test에서 개념을 따 왔다.
  - 동적 타이핑 언어 및 다형성과 관련된 개념이다.
  - 객체의 type보다 해당 객체에 정의되어 있는 method 혹은 attribute가 더 중요하다는 개념이다.
    - 객체에 이미 존재하는 메서드를 호출하기 위해, 객체가 해당 메서드를 갖는 타입인지 확인하지 말고, 해당 메서드를 가지고 있다면 해당 타입으로 간주하라는 것이다.

  - 예시

  ```python
  class Duck:
      def fly(self):
          print("fly with wings")
  
          
  class Plane:
      def fly(self):
          print("fly with fuel")
          
          
  class Ostrich:
      def walk(self):
          print("walking")
  
          
  def fly_duck(duck):
      duck.fly()
  
  # Ostrich는 fly라는 메서드를 가지고 있지 않기에 error가 발생한다.
  for obj in [Duck(), Plane(), Ostrich()]:
      obj.fly()
  ```

  - 코드가 특정 type에 강하게 결합되지 않게 해준다는 장점이 있지만, 문제가 생길 경우 디버깅이 어려워진다는 단점이 있다.
  - Duck typing 덕분에 Python에서는 interface를 구현해야 하는 번거로움이 많이 줄어들었다.
    - Interface가 하는 역할을 duck typing이 해주고 있는 것이다.
    - 물론 그렇다고 Python에서 interface 자체가 쓸모 없다는 것은 아니다.





- Call by value, Call by reference, Call by sharing

  > https://en.wikipedia.org/wiki/Evaluation_strategy

  - 평가 전략(Evaluation Strategy)

    - 프로그래밍 언어에서 평가 전략이란 표현식을 평가하는 규칙들의 집합이다.
    - 그러나 주로 parameter 전달 전략(Parameter-passing strategy)의 개념을 가리킨다.
    - Parameter-passing strategy란 function에 전달되는 각 parameter의 값의 종류를 정의하고, 함수 호출시의 parameter를 평가할지 여부를 결정하고, 만약 평가한다면, 평가 순서를 결정하는 전략을 의미한다.

  - Parameter와 argument

    - Parameter(매개변수, 형식 매개변수(formal parameter))란 함수에 정의된 매개변수를 의미한다.
    - Argument(인자, 실인자(actual parameter))란 함수에 전달하는 값을 의미한다.
    - Parameter는 함수 선언부에 정의되고, argument는 함수 호출부에서 사용된다.

  ```python
  def f(a):	# 함수에 정의된 매개변수 a는 parameter
      return a
  
  f(1)		# 함수에 실제로 넘어가는 값인 1은 argument
  ```

  - Call by value
    - Argument 표현식의 평가된 값이 함수 내에서 일치하는 변수에 binding된다.
    - 주로 새로운 메모리에 값을 복사하는 방식으로 이루어진다.
    - 즉, 먼저 argument 표현식을 평가한다.
    - `f(1)`에서 argument 표현식에 해당하는 `1`이라는 표현식을 평가하면 `1`이라는 값을 얻게 된다.
    - 이 평가된 값을 함수 내에서 일치하는 변수인 `a`에 binding한다.
    - 이 때, 주로 1이라는 값을 복사하여 새로운 메모리 영역에 생성하는 방식을 사용한다.
    - 따라서 함수 내에서 값이 변경되어도 원본 값은 변경되지 않는다.
  - Call by reference
    - Parameter가 argument의 reference에 bound된다.
    - 이는 function이 argument로 사용된 변수를 변경할 수 있다는 것을 의미한다.
    - 이 방식은 프로그래머가 함수 호출의 영향을 추적하기 힘들게 만들고, 사소한 버그를 유발할 수도 있다.
  - Call by sharing(call by object, call by object-sharing)
    - Caller와 callee가 object를 공유하는 것이다.
    - 값이 원시 타입이 아니라 객체에 기반하고 있음을 표현하기 위해 주로 사용한다.
    - Callee에게 전달 된 값이 변경된다는 점에서 call by value와 다르고, 주소가 아닌 object를 공유한다는 점에서 call by reference와는 다르다.
    - Immutable object의 경우 call by value와 실질적인 차이가 존재하지 않는다.

  - Python과 Java, Javascript등의 언어는 Call by sharing 방식을 사용한다.

    - 그러나 일반적으로 call by sharing이라는 용어를 사용하지는 않는다.
    - Python community에서는 이를 call by assignment라 부른다.



- 도메인 로직(domain logic, 비즈니스 로직(Business logic))

  > https://velog.io/@eddy_song/domain-logic
  >
  > https://enterprisecraftsmanship.com/posts/what-is-domain-logic/

  - Problem space와 solution space
    - 하나의 프로젝트는 크게 problem space와 solution space라는 두 개의 영역으로 나눠진다.
    - Problem space는 일반적으로 domain 혹은 problem domain, core domain이라 부르며, software를 통해 해결하고자 하는 현실의 문제들을 의미한다.
    - Solution space는 business logic, business rules, domain logic, domain knowledge라 부르며, problem domain을 해결하기 위한 방안들을 의미한다.

  - 비즈니스 혹은 도메인
    - 소프트웨어 공학에서 비즈니스 혹은 도메인이라는 말은 소프트웨어가 해결하고자 하는 현실의 문제를 가리킨다.
    - 즉 소프트웨어의 존재 이유이다.
  - 도메인 로직
    - 소프트웨어가 해결하고자 하는 현실 문제를 해결하는 데 직접적으로 관련된 로직을 의미한다.
    - Software는 도메인 로직으로만 구성되지 않는다.
    - 개발을 하다 보면 다양한 코드를 작성하게 되며, 이들이 모두 domain model을 작성하는 것과 관련되지는 않는다.
    - 대부분의 경우 domain model을 DB 등의 data store, 외부 서비스, 사용자와 연결하기위해 많은 코드를 작성하게 된다.
    - 따라서 domain model과 직접적으로 관련된 코드와 그렇지 않은 코드를 구분하는 것은 쉽지 않다.
  - 애플리케이션 서비스 로직
    - 비즈니스 로직과 구분되는 현실 문제 해결에 직접적으로 관여하지 않는 로직을 의미한다.
    - 애플리케이션 서비스 로직은 애플리케이션 서비스 계층에서 결정들을 조율하고 의사결정 결과를 반영하는 등의 역할을 한다.
  - 도메인 로직과 애플리케이션 서비스 로직의 구분
    - 어떤 코드가 비즈니스에 대한 의사결정을 하고 있는가로 구분한다.

  - 왜 구분해야 하는가
    - 관심사의 분리를 가능하게 해준다.
    - 이를 통해 도메인과 관련된 로직에 보다 집중할 수 있게 된다.

  - 예시
    - 아래 코드는 application service layer를 보여준다.
    - 실제 비즈니스 로직은 atm 객체에서 처리하고 application service는 비즈니스에 관한 의사 결정 결과를 조율하고 반영하는 역할을 한다.
    - 비즈니스와 직접적으로 관련된 코드만 보고 싶다면 atm만 확인하면 된다.
    - 즉 아래와 같이 계층을 구분함으로써 코드를 보다 쉽게 읽을 수 있게 되고, 도메인 로직에 집중할 수 있게 된다.

  ```python
  class Bank:
      def __init__(self):
          self.atm = ATM()
          self.payment_gateway = None
          self.repository = None
  	
      # take_money 메서드 자체는 아무런 의사 결정을 하지 않는다.
      def take_money(amount):
          # 돈을 출금할 수 있는지에 대한 의사 결정은 atm 객체의 can_take_money 메서드를 통해 이루어진다.
          if self.atm.can_take_money(amount):
              # 수수료를 포함한 금액이 얼마인지에 대한 의사 결정 역시 atm 객체에서 이루어진다.
              amount_with_commision = self.amount.calculate_amount_with_commision(amount)
              
              self.payment_gateway.charge_payment(amount_with_commision)
              self.repository.save(self.atm)
          else:
              return "Not enough meney to withdraw"
  ```




- TTY
  - TTY의 기원
    - 1830년대에 와이어를 통해 message를 주고 받을 수 있는 teleprinter(전신인자기)가 개발되었다.
    - 기존에는 전송자가 모스 부호 입력하고, 수신자가 모스 부호를 받는 형식이었지만, teleprinter는 전송자가 문자를 입력하면 이를 모스 부호로 변환하여 전달하고, 수신자 측에 모스 부호로 도착하면 이를 다시 문자로 변환하여 수신자에게 출력해주었다.
    - 이후 개량을 거쳐 1908년 Teletypewriter가 발명되었다.
    - 컴퓨터가 개량되면서, 컴퓨터에도 입출력 장치가 필요하게 되었고, 컴퓨터에도 teletypewriter가 입출력장치로 사용되기 시작했다.
    - Teletypewriter은 시간이 흐르면서 teletype으로 줄여서 불리기 시작했고, 결국 현재는 TTY로 줄여서 부른다.
  - PTY(Pseudo-TeletYpes)
    - TTY는 Unix 계열 운영체제에서 software화 되었는데, 이를 물리적인 TTY와 구분하기 위해서 PTY라고 부른다.
    - Software로서의 TTY 역시 그냥 TTY라고 부르기도 한다.
    - Terminal과 동의어로 쓰인다.
  - PTS(Pseudo Terminal Slave)
    - `ssh` 등으로 서버에서 원격으로 접속했을 때 열리는 TTY이다.



- Loopback, localhost, 0.0.0.0

  > https://velog.io/@lky9303/127.0.0.1-%EA%B3%BC-localhost%EC%9D%98-%EC%B0%A8%EC%9D%B4

  - 네트워크 통신이란 인터넷 상에 존재하는 호스트와 서로 패킷을 주고 받는 것이다.
  - Loopback
    - 자신의 local PC을 서버로 만들고, local PC 내에서 요청을 보내고 응답을 받을 수 있는 것이다.
    - 127.0.0.1로 표현하며, 만약 목적지 IP 주소를 127.0.0.1로 설정하면 이는 패킷을 외부로 전송하지 않고 자신에게 전송한다.
    - 즉 자신이 송신한 패킷을 자신이 수신하게 된다.
    - 자기 자신을 가리키는 주소라고 보면 된다.
  - localhost
    - 127.0.0.1이 ip주소라면 localhost는 domain name이라고 보면 된다.
    - www.naver.com이라는 domain name이 DNS를 통해서 IP 주소로 변환되듯이, localhost가 127.0.0.1이라는 ip주소로 변환되는 것이다.
    - 그러나 localhost가 항상 127.0.0.1을 가리키는 것은 아닐 수 있다.
    - 정확히는 localhost는 OS hosts 파일의 redirect rule에 정의된 ip로 변환된다.
    - 따라서 OS host file의 redirect rule에서 localhost의 redirecting IP 값을 다르게 입력했다면, 127.0.0.1이 아닌 설정된 IP로 변환된다.
    - Ubuntu의 경우 `/etc/hosts`에서 확인할 수 있다.
  - 0.0.0.0
    - 지정한 IP 주소가 없다는 것이며, 내 컴퓨터에 연결된 모든 IPv4 address를 의미한다.



- NAS(Network-Attached Storage)
  - 컴퓨터 네트워크에 연결된 file-level의 컴퓨터 기억 장치
    - File-level이란 file storage를 의미한다.
    - 네트워크로 연결된 기기들 사이에 data를 공유할 수 있게 해주는 기술이다.
  - NAS와 클라우드는 다르다.
    - 클라우드는 네트워크 전체에서 확장 가능한 resource들을 추상화하고 공유하는 것이다.





- 방어적 프로그래밍(Defensive programming)
  - 예상치 못한 입력에도 소프트웨어가 계속적 기능 수행을 보장할 수 있도록 고안된 방어적 설계의 한 형태.



- DT(Digital Transformation, DX)
  - DT와 DX 모두 디지털 전환을 의미한다.
    - DT는 digital transformation의 약어이며, DX는 Digital의 D와 Transformation의 의미를 갖고 있는 X로 만들어진 합성어이다.
    - 둘 다 의미는 같다.
  - 디지털 전환
    - 기업 및 조직이 디지털 기술과 도구를 활용하여 비즈니스 모델과 프로세스를 혁신하는 과정이다.
    - 요즘에는 SI라는 말 보다는 DT, DX라는 용어를 더 선호한다.