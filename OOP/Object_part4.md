# 메시지와 인터페이스

- 객체지향 애플리케이션의 가장 중요한 재료는 클래스가 아니라 객체들이 주고 받는 메시지다.
  - 클래스 사이의 정적인 관계에서 메시지 사이의 동적인 흐름으로 초점을 전환해야한다.
  - 애플리케이션은 클래스로 구성되지만 메시지를 통해 정의된다.



- 협력과 메시지

  - 클라이언트-서버 모델
    - 협력은 어떤 객체가 다른 객체에게 무언가를 요청할 때 시작된다.
    - 객체가 다른 객체에게 접근할 수 있는 유일한 방법은 메시지를 전송하는 것 뿐이다.
    - 객체는 자신의 희망을 메시지라는 형태로 전송하고 메시지를 수신한 객체는 요청을 적절히 처리한 후 응답한다.
    - 두 객체 사이의 관계를 설명하기 위해 사용하는 전통적인 메타포는 클라이언트-서버 모델이다.
    - 협력 안에서 메시지를 전송하는 객체를 클라이언트, 메시지를 수신하는 객체를 서버라 부르며, 협력은 클라이언트가 서버의 서비스를 요청하는 단방향 상호작용이다.
    - 협력의 관점에서 객체는 객체가 수신하는 메시지의 집합과 외부의 객체에게 전송하는 메시지의 집합이라는 두 종류의 메시지 집합으로 구성된다.
    - 대부분의 사람들은 객체가 수신하는 메시지의 집합에만 초점을 맞추지만 협력에 적합한 객체를 설계하기 위해서는 외부에 전송하는 메시지의 집합도 함께 고려하는 것이 바람직하다.
  - 메시지와 메시지 전송
    - 한 객체가 다른 객체에게 도움을 요청하는 것을 메시지 전송 또는 메시지 패싱이라 부른다.
    - 이 때 메시지를 전송하는 객체를 메시지 전송자라고 부르고, 메시지를 수신하는 객체를 메시지 수신자라고 부른다.
    - 메시지는 오퍼레이션명과 인자로 구성되며 메시지 전송은 여기에 미시지 수신자를 추가한 것이다.
    - 예를 들어 `is_satisfied_by(screening)`은 오퍼레이션명(`is_satisfied_by`)과 인자(`screening`)으로 구성된 메시지이며, `condition.is_satisfied_by(screening)`는 메시지 수신자(`condition`)가 추가된 메시지 전송이다.
  - 메시지와 메서드
    - 메시지를 수신했을 때 실제로 실행되는 함수 또는 프로시저를 메서드라고 부른다.
    - 메시지를 수신했을 때 실제로 어떤 코드가 실행되는지는 메시지 수신자의 실제 타입이 무엇인가에 달려 있다.
    - 기술적인 관점에서 객체 사이의 메시지 전송은 전통적인 방식의 함수 호출이나 프로시저 호출과는 다르다.
    - 전통적인 방식의 개발자는 어떤 코드가 실행될지를 정확하게 알고 있는 상황에서 함수 호출이나 프로시저 구문을 작성한다.
    - 즉 코드의 의미가 컴파일 시점과 실행 시점에 동일하다.
    - 반면에 객체는 메시지와 메서드라는 서로 다른 개념을 실행 시점에 연결해야 하기에 컴파일 시점과 실행 시점의 의미가 달라질 수 있다.
    - 메시지와 메서드의 구분은 메시지 전송자와 수신자가 느슨하게 결합될 수 있게 한다.
    - 메시지 전송자는 자신이 어떤 메시지를 전송해야 하는지만 알면 되며 수신자에 대해 몰라도 된다.
    - 메시지 수신자 역시 전송자에 대해 알 필요가 없으며, 단지 메시지가 도착했다는 사실만 알면 된다.
    - 메시지 수신자는 메시지를 처리하기 위해 필요한 메서드를 결정할 수 있는 자율권을 누린다.
    - 실행 시점에 메시지와 메서드를 바인딩하는 메커니즘은 두 객체 사이의 결합도를 낮춤으로써 유연하고 확장 가능한 코드를 작성할 수 있게 만든다.
  - 퍼블릭 인터페이스와 오퍼레이션
    - 객체는 안과 밖을 구분하는 뚜렷한 경계를 가진다.
    - 외부에서 볼 때 객체의 안쪽은 미지의 영역이며, 외부의 객체는 오직 객체가 공개하는 메시지를 통해서만 객체와 상호작용할 수 있다.
    - 이처럼 객체가 의사소통을 위해 외부에 공개하는 메시지의 집합을 퍼블릭 인터페이스라고 부른다.
    - 프로그래밍 언어적 관점에서 퍼블릭 인터페이스에 포함된 메시지를 오퍼레이션이라 부른다.
    - 오퍼레이션은 수행 가능한 어떤 행동에 대한 추상화이며, 흔히 오퍼레이션이라 부를 때는 내부의 구현 코드는 제외하고 단순히 메시지와 관련된 시그니처를 가리키는 경우가 대부분이다.
    - 그에 비해 메시지를 수신했을 때 실제로 실행되는 코드는 메서드라고 부른다.
    - 예를 들어 `DiscountDondition` interface에 정의 된 `is_satisfied_by`는 오퍼레이션에 해당하고, `SequenceCondition`과 `PeriodCondition`의 `is_satisfied_by`는 실제 구현을 포함하기에 메서드라고 부른다.
    - 객체가 메시지를 전송하면 런타임 시스템은 메시지 전송을 오퍼레이션 호출로 해석하고, 메시지를 수신한 객체의 실제 타입을 기반으로 적절한 메서드를 찾아 실행한다.
    - 따라서 퍼블릭 인터페이스와 메시지의 관점에서 보면 '메서드 호출' 보다는 '오퍼레이션 호출'이라는 용어를 사용하는 것이 더 적절하다.

  - 시그니처
    - 오퍼레이션(또는 메서드)의 이름과 파라미터 항목을 합쳐서 시그니처라고 부른다(일부 언어에서는 반환 타입까지 시그니처에 포함되기도 한다).
    - 오퍼레이션은 실행 코드 없이 시그니처만을 정의한 것이다.
    - 메서드는 시그니처에 구현을 더한 것이다.
    - 일반적으로 메시지를 수신하면 오퍼레이션의 시그니처와 동일한 메서드가 실행된다.
    - 하나의 오퍼레이션에 오직 하나의 메서드만 존재하는 경우 굳이 둘을 구분할 필요가 없다.
    - 그러나 다형성을 위해서는 하나의 오퍼레이션에 대해 다양한 메서드를 구현해야한다.
    - 따라서 오퍼레이션의 관점에서 다형성이란 동일한 오퍼레이션 호출에 대해 서로 다른 메서드들이 실행되는 것이라고 정의할 수 있다.



- 인터페이스와 설계 품질
  - 좋은 인터페이스는 최소한의 인터페이스와 추상적인 인터페이스라는 조건을 만족해야한다.
    - 최소한의 인터페이스는 꼭 필요한 오퍼레이션만을 인터페이스에 포함한다.
    - 추상적인 인터페이스는 어떻게 수행하는지가 아니라 무엇을 하는지를 표현한다.
  - 위 조건을 만족시키는 가장 좋은 방법은 책임 주도 설계 방법을 따르는 것이다.
    - 책임 주도 설계는 메시지를 먼저 선택함으로써 협력과는 무관한 오퍼레이션이 인터페이스에 스며드는 것을 방지하여 인터페이스는 최소한의 오퍼레이션만 포함하게 된다.
    - 또한 메시지가 객체를 선택하게 함으로써 클라이언트의 의도를 메시지에 표현할 수 있게 하여 추상적인 오퍼레이션이 인터페이스에 자연스럽게 스며들게 된다.
  - 퍼블릭 인터페이스의 품질에 영향을 미치는 대표적인 원칙과 기법들은 아래와 같은 것들이 있다.
    - 디미터 법칙
    - 묻지 말고 시켜라
    - 의도를 드러내는 인터페이스
    - 명령-쿼리 분리



- 디미터 법칙(Law of Demeter)

  - 객체의 내부 구조에 강하게 결합되지 않도록 협력 경로를 제한하라는 법칙이다.
    - 낯선 자에게 말하지 말라
    - 오직 인접한 이웃하고만 말하라.
  - 디미터 법칙을 따르게 위해서는 클래스가 특정한 조건을 만족하는 대상에게만 메시지를 전송하도록 프로그래밍해야 한다.
    - 모든 클래스 C와 C에 구현된 모든 메서드 M에 대해서, M이 메시지를 전송할 수 있는 모든 객체는 다음에 서술된 클래스의 인스턴스여야 한다(이때 M에 의해 생성된 객체나 M이 호출하는 메서드에 의해 생성된 객체, 전역 변수로 선언된 객체는 모두 M의 인자로 간주한다).
    - M의 인자로 전달된 클래스(C 자체를 포함) 또는 C의 인스턴스 변수의 클래스
  - 결국 쉽게 말해 아래 조건을 만족하는 인스턴스에만 메시지를 전송하도록 프로그래밍해야 한다.
    - this 객체
    - 메서드의 매개 변수
    - this의 속성
    - this의 속성인 컬렉션의 요소
    - 메서드 내에서 생성된 지역 객체
  - 부끄럼타는 코드(shy code)
    - 디미터 법칙을 따르면 부끄럼타는 코드를 작성할 수 있다.
    - 부끄럼 타는 코드란 불필요한 어떤 것도 다른 객체에게 보여주지 않으며, 다른 객체의 구현에 의존하지 않는 코드를 의미한다.
    - 디미터 법칙을 따르는 코드는 메시지 수진자의 내부 구조가 전송자에게 노출되지 않으며, 메시지 전송자는 수신자의 내부 구현에 결합되지 않는다.
    - 따라서 클라이언트와 서버 사이에 낮은 결합도를 유지할 수 있다.
  - 디미터 법칙과 캡슐화
    - 디미터 법칙은 캡슐화를 다른 관점에서 표현한 것이다.
    - 디미터 법칙이 가치 있는 이유는 캡슐화를 위해 따라야 하는 구체적인 지침을 제공하기 때문이다.
    - 캡슐화가 클래스 내부 구현을 감춰야한다는 사실을 강조한다면 디미터 법칙은 협력하는 클래스의 캡슐화를 지키기 위해 접근해야 하는 요소를 제한한다.
  - 기차 충돌(train wreck)
    - 아래 코드는 디미터 법칙을 위반하는 코드의 전형적인 모습을 표현한 것이다.
    - 메시지 전송자가 수신자의 내부 구조에 대해 물어보고 반환받은 요소에 대해 연쇄적으로 메시지를 전송한다.
    - 이러한 코드를 기차 충돌이라 부르는데 여러 대의 기차가 한 줄로 늘어서 충돌한 것 처럼 보이기 때문이다.
    - 클래스의 내부 구현이 외부로 노출됐을 때 나타나는 전형적인 형태로 메시지 전송자는 메시지 수신자의 내부 정보를 자세히 알게 된다.
    - 따라서 수신자의 캡슐화는 무너지고, 전송자가 수신자의 내부 구현에 강하게 결합된다.

  ```python
  screening.get_movie().caclulate_fee()
  ```

  - 무비판적으로 디미터 법칙을 수용하면 인터페이스 관점에서 객체의 응집도가 낮아질 수 있다.



- 묻지 말고 시켜라(Tell, Don't Ask)

  - 디미터 법칙은 훌륭한 메시지는 객체의 상태에 관해 묻지 말고 원하는 것을 시켜야 한다는 사실을 강조한다.
    - 묻지 말고 시켜라는 이런 스타일의 메시지 작성을 장려하는 원칙을 가리키는 용어다.
    - 메시지 전송자는 메시지 수신자의 상태를 기반으로 결정을 내린 후 메시지 수신자의 상태를 바꿔서는 안 된다.
    - 객체의 외부에서 해당 객체의 상태를 기반으로 결정을 내리는 것은 객체의 캡슐화를 위반한다.

  - 묻지 말고 시켜라 원칙을 따르면 밀접하게 연관된 정보와 행동을 함께 가지는 객체를 만들 수 있다.
    - 객체지향의 기본은 변경될 확률이 높은 정보와 행동을 하나의 단위로 통합하는 것이다.
    - 묻지 말고 시켜라 원칙을 따르면 객체의 정보를 이용하는 행동을 객체의 외부가 아닌 내부에 위치시키기 때문에 자연스럽게 정보와 행동을 동일한 클래스 안에 두게 된다.
    - 이 원칙을 따를 경우 자연스럽게 정보 전문가에게 책임을 할당하게 되고 응집도 높은 클래스를 얻을 확률이 높아진다.
  - 묻지 말고 시켜라 원칙과 디미터 법칙은 훌륭한 인터페이스를 제공하기 위해 포함해야 하는 오퍼레이션에 대한 힌트를 제공한다.
    - 내부의 상태를 묻는 오퍼레이션을 인터페이스에 포함시키고 있다면 더 나은 방법은 없는지 고민해야한다.
    - 내부의 상태를 이용해 어떤 결정을 내리는 로직이 객체 외부에 존재한다면 객체가 책임져야 하는 행동이 객체 외부로 누수된 것이다.
    - 상태를 묻는 오퍼레이션을 행동을 요청하는 오퍼레이션으로 대체하여 인터페이스를 향상시켜야 한다.
    - 하지만 단순하게 객체에게 묻지 않고 시킨다고 해서 모든 문제가 해결되는 것은 아니다.
    - 여기에 더해서 객체가 어떻게 작업을 수행하는지를 노출해서는 안 된다.



- 의도를 드러내는 인터페이스(Intention Revealing Interface)

  - 메서드의 이름을 짓는 방법
    - 켄트 벡은 메서드를 명명하는 두 가지 방법을 설명했다.
    - 첫 번째 방법은 메서드가 작업을 어떻게 수행하는지를 나타내도록 이름을 짓는 것이다.
    - 두 번째 방법은 메서드가 무엇을 수행하는지를 나타내도록 이름을 짓는 것이다.
    - 결론부터 말하면, 두 방법 중 후자가 더 나은 방법이다.
    - 전자의 경우 메서드의 내부 구현을 설명하는 이름으로, 협력을 설계하기 시작하는 이른 시기부터 클래스의 내부 구현에 관해 고민하게 한다.
    - 반면에 후자의 경우 객체가 협력 안에서 수행하는 책임에 관해 고민하도록 해준다.
  - 메서드가 작업을 어떻게 수행하는지 나타내도록 명명하기
    - 아래와 같이 메서드가 작업을 어떻게 수행하는지 나타내도록 명명하는 것은 좋지 않은 방법이다.
    - 첫 번째 이유는 메서드에 대해 제대로 커뮤니케이션 하지 못한다는 것이다.
    - 클라이언트의 관점에서는 아래 두 메서드 모두 할인 조건을 판단하는 동일한 작업을 수행함에도, 이름이 다르기에 두 메서드의 내부 구현을 정확히 모른다면 두 메서드가 동일한 작업을 수행한다는 사실을 알기 힘들다.
    - 두 번째 이유는 메서드 수준에서 캡슐화를 위반한다는 것이다.
    - 이 메서드들은 클라이언트로 하여금 협력하는 객체의 종류를 알도록 강요한다.
    - 즉, `PeriodCondtion`를 사용하는 코드를 `SequenceCondition`를 사용하는 코드로 변경하려면 단순히 참조하는 객체를 변경하는 것뿐만 아니라 호출하는 메서드를 변경해야한다.
    - 만약 할인 여부를 판단하는 방법이 변경된다면 메서드의 이름 역시 변경해야 하며, 이는 메시지를 전송하는 클라이언트의 코드도 함께 변경해야 한다는 것을 의미한다.

  ```python
  class PeriodCondtion:
      def is_satisfied_by_period(self, screening: Screening):
          ...
          
          
  class SequenceCondition:
      def is_satisfied_by_sequence(self, screening: Screening):
          ...
  ```

  - 메서드가 무엇을 하는지 나타내도록 명명하기
    - 메서드의 구현이 한 가지인 경우에는 무엇을 하는지를 드러내는 이름을 짓는 것이 어려울 수도 있다.
    - 그러나 무엇을 하는지 드러내는 이름은 코드를 이해하기 쉽게 만들뿐만 아니라 유연한 코드를 만들게 해준다.
    - 이 방식은 객체가 협력 안에서 수행하는 책임에 관해 고민하도록 한다.
    - 이를 통해 외부의 객체가 메시지를 전송하는 목적을 먼저 생각하도록 만들며, 결과적으로 협력하는 클라이언트의 의도에 부합하도록 메서드의 이름을 짓게 된다.
    - 메서드가 무엇읗 하느냐에 초점을 맞추면 클라이언트의 관점에서 동일한 작업을 하는 메서드들을 하나의 타입 계층으로 묶을 수 있는 가능성이 커 진다.
    - 그 결과 다양한 타입의 객체가 참여할 수 있는 유연한 협력을 얻게 된다.

  ```python
  class DiscountCondition(ABC):
      @abstractmethod
      def is_satisfied_by(self, screening: Screening):
          ... 
  
  
  class PeriodCondtion(DiscountCondition):
      def is_satisfied_by(self, screening: Screening):
          ...
          
          
  class SequenceCondition(DiscountCondition):
      def is_satisfied_by(self, screening: Screening):
          ...
  ```

  - 의도를 드러내는 선택자(Intention Revealing Selector)
    - 어떻게 하느냐가 아니라 무엇을 하느냐에 따라 메서드의 이름을 짓는 패턴을 의도를 드러내는 선택자라고 부른다.
    - 켄트 벡은 메서드에 의도를 드러낼 수 있는 이름을 붙이기 위해 다음과 같이 생각할 것을 조언한다,
    - 매우 다른 두 번째 구현을 상상하고, 해당 메서드에 동일한 메서드를 붙인다고 상상한다.
    - 이렇게 하면 가능한 한 가장 추상적인 이름을 메서드에 붙이게 될 것이다.
  - 의도를 드러내는 인터페이스는 의도를 드러내는 선택자를 인터페이스 레벨로 확장한 것이다.
    - 에릭 에반스가 켄트 벡의 의도를 드러내는 선택자를 확장하여 제시했다.
    - 구현과 관련된 모든 정보를 캡슐화하고 객체의 퍼블릭 인터페이스에는 협력과 관련된 의도만을 표현해야 한다.
    - 타입 이름, 메서드 이름, 인자 이름이 모두 결합되어 의도를 드러내는 인터페이스를 형성한다.
    - 퍼블릭 인터페이스에는 관계와 규칙을 실행하는 방법이 아닌 이벤트와 규칙 그 자체만 명시한다.



- 함께 모으기

  - 디미터 법칙을 위반하는 티켓 판매 도메인
    - 디미터 법칙에 따르면 인자로 전달된 `audience`와 인스턴스 변수인 `ticket_seller`에게 메시지를 전송하는 것은 문제가 없다.
    - 문제는 `Theater`가 `audience`와 `ticket_seller` 내부에 포함된 객체에도 직접 접근하여 디미터 법칙을 위반한다는 것이다.

  ```python
  class Theater:
      def __init__(self, ticket_seller: TicketSeller):
          self.ticket_seller = ticket_seller
      
      def enter(self, audience: Audience):
          if audience.get_bag().has_invitation():
              ticket = self.ticket_seller.get_ticket_office().get_ticket()
              audience.get_bag().set_ticket(ticket)
          else:
              ticket = self.ticket_seller.get_ticket_office().get_ticket()
              audience.get_bag().minus_amount(ticket.get_fee())
              self.ticket_seller.get_ticket_office().plus_amount(ticket.get_fee())
              audience.get_bag().set_ticket(ticket)
  ```

  - 근본적으로 디미터 법칙을 위반하는 설계는 인터페이스와 구현 분리 원칙을 위반한다.
    -  `Audience`가 `Bag`을 포함한다는 사실은 `Audience`의 내부 구현에 속하며 `Audience`는 자신의 내부 구현을 자유롭게 변경할 수 있어야 한다.
    - 그러나 퍼블릭 인터페이스에 `get_bag`을 포함시키는 순간 객체의 구현이 퍼블릭 인터페이스를 통해 외부로 새어나가게 된다.
    - 따라서 디미터 법칙을 위반하는 것은 클라이언트에게 구현을 노출한다는 것을 의미하며, 그 결과 작은 변경에도 쉽게 무너지는 불안정한 코드를 얻게 된다.
  - 디미터 법칙을 위반한 코드는 사용하기도 어렵다.
    - 클라이언트 객체의 개발자는 `Audience`의 퍼블릭 인터페이스뿐만 아니라 `Audience`의 내부 구현까지 알고 있어야 하기 때문이다.
    - `TicketSeller`의 경우 그 정도가 더 심한데, `Theater`는 `TicketSeller`가 `get_ticket_office` 메시지를 수신할 수 있다는 사실뿐만 아니라 내부에 `TicketOffice`를 포함하고 있다는 사실도 알아야 한다. 또한 `Theater`는 반환된 `TicketOffice`가 `get_ticket` 메시지를 수신할 수 있으며, 이 메서드가 반환하는 `Ticket`인스턴스가 `get_fee` 메시지를 이해할 수 있다는 사실도 알고 있어야한다.
  - `Theater`에 묻지 말고 시켜라 적용하기
    - 디미터 법칙을 위반한 코드를 수정하는 일반적인 방법은 내부 구조를 묻는 대신 `Audience`와 `TicketSeller`가 직접 자신의 책임을 수행하도록 시키는 것이다.
    - 즉, `Audience`와 `TicketSeller`는 묻지 말고 시켜라 스타일을 따르는 퍼블릭 인터페이스를 가져야 한다.

  ```python
  class TicketSeller:
      def __init__(self, ticket_office: TicketOffice):
          self.ticket_office = ticket_office
      
      def get_ticket_office(self) -> TicketOffice:
          return self.ticket_office
          
      def set_ticket(self, audience: Audience):
          if audience.get_bag().has_invitation():
              ticket = self.ticket_office.get_ticket()
              audience.get_bag().set_ticket(ticket)
          else:
              ticket = self.ticket_office.get_ticket()
              audience.get_bag().minus_amount(ticket.get_fee())
              self.ticket_office.plus_amount(ticket.get_fee())
              audience.get_bag().set_ticket(ticket)
              
              
  class Theater:
      def __init__(self, ticket_seller: TicketSeller):
          self.ticket_seller = ticket_seller
      
      def enter(self, audience: Audience):
          self.ticket_seller.set_ticket(audience)
  ```

  - `TicketSeller`에 묻지 말고 시켜라 적용하기
    - 마찬가지로 `Audience`가 `Ticket`을 보유하도록 만들어 `TicketSeller`가 묻지 않고 시킬 수 있도록 한다.
  
  ```python
  class Audience:
      def __init__(self, bag: Bag=None):
          self.bag = bag
      
      def get_bag(self) -> Bag:
          return self.bag
      
      def set_ticket(self, ticket: Ticket):
          if self.bag.has_invitation():
              self.bag.set_ticket(ticket)
              return 0
          else:
              self.bag.set_ticket(ticket)
              self.bag.minus_amount(ticket.get_fee())
              return ticket.get_fee()
  
  
  class TicketSeller:
      def __init__(self, ticket_office: TicketOffice):
          self.ticket_office = ticket_office
      
      def get_ticket_office(self) -> TicketOffice:
          return self.ticket_office
          
      def set_ticket(self, audience: Audience):
          self.ticket_office.plus_amount(audience.set_ticket(self.ticket_office.get_ticket()))
  ```
  
  - `Audience`에 묻지 말고 시켜라 적용하기
    - `Audience`는 `Bag`에게 원하는 일을 시키기 전에 `has_invitation` 메서드를 이용하여 초대권이 있는지를 확인하므로 디미터 법칙을 위반한다.
  
  ```python
  class Bag:
      def __init__(self, amount=None, invitation: Invitation=None):
          if not amount and not invitation:
              raise Exception()
          
          self.amount = amount
          self.invitation = invitation
          self.ticket: Ticket = None
          
      def has_invitation(self):
          return self.invitation is not None
      
      def set_ticket(self, ticket: Ticket):
          if self.has_invitation():
              self.ticket = ticket
              return 0
          else:
              self.ticket = ticket
              self.minus_amount(ticket.get_fee())
              return ticket.get_fee()
          
      def minus_amount(self, amount: int):
          self.amount -= amount
          
          
  class Audience:
      def __init__(self, bag: Bag=None):
          self.bag = bag
      
      def set_ticket(self, ticket: Ticket):
          return self.bag.set_ticket(ticket)
  ```
  
  - 디미터 법칙과 묻지 말고 시켜라 원칙에 따라 리팩터링한 후에 `Audience`는 자신의 상태를 스스로 관리하고 결정하는 자율적인 객체가 됐다.
    - 두 원칙을 따르면 자연스럽게 자율적인 객체로 구성된 유연한 협력을 얻게 된다.
    - 구현이 객체의 퍼블릭 인터페이스에 노출되지 않기 때문에 객체 사이의 결합도는 낮아진다.
    - 책임이 잘못된 곳에 할당될 가능성이 낮아지기 때문에 객체의 응집도 역시 높아진다.



