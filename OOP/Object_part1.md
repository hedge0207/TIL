# 객체, 설계

- 티켓 판매 애플리케이션 구현하기.

  - 상황
    - 추첨을 통해 선정된 관람객에게 공연을 무료로 관람할 수 있는 초대장을 발송하려 한다.
    - 문제는 이벤트에 당첨된 관람객과 그렇지 않은 관람객을 다른 방식으로 입장시켜야 한다는 것이다.
    - 이벤트에 당첨된 관람객은 초대장을 티켓으로 교환한 후 입장하고, 이벤트에 당첨되지 않은 관람객은 티켓을 구매한 후 입장해야한다.
    - 따라서 관람객을 입장시키기 전에 이벤트 당첨 여부를 확인해야하고, 이벤트 당첨자가 아닌 경우에는 티켓을 판매한 후에 입장시켜야한다.
  - 초대장 구현하기
    - `when` instance 변수에는 공연을 관람할 수 있는 초대 일자를 저장된다.

  ```python
  class Invitation:
      def __init__(self):
          self.when: date = None
  ```

  - 표 구현하기

  ```python
  class Ticket:
      def __init__(self):
          self.fee: int = None
          
      def get_fee(self) -> int:
          return self.fee
  ```

  - 관람객의 소지품을 표현할 `Bag` class를 구현한다.
    - 관람객은 초대장, 표, 현금 중 하나를 가지고 있어야 공연 관람이 가능하므로 이 셋을 instance 변수로 추가하고, 관련 메서드들을 추가한다.
    - 이벤트에 당첨된 관람객의 가방 안에는 현금과 초대장이 들어있지만 당첨되지 않은 관람객의 가방 안에는 초대장이 들어있지 않을 것이다.
    - 따라서 `Bag` instance의 상태는 현금과 초대장을 함께 보관하거나 초대장 없이 현금만 보관하는 두 가지 중 하나일 것이다.
    - `Bag` instance를 생성하는 시점에 이 제약을 강제할 수 있도록 생성자를 구현한다.

  ```python
  class Bag:
      def __init__(self, amount=None, invitation: Invitation=None):
          if amount is None and invitation is None:
              raise Exception()
          
          self.amount = amount
          self.invitation = invitation
          self.ticket: Ticket = None
          
      def has_invitation(self):
          return self.invitation is not None
      
      def has_ticket(self):
          return self.ticket is not None
      
      def set_ticket(self, ticket:Ticket):
          self.ticket = ticket
          
      def minus_amount(self, amount: int):
          self.amount -= amount
  ```
  
  - 관람객을 구현한다.
  
  ```python
  class Audience:
      def __init__(self, bag: Bag=None):
          self.bag = bag
      
      def get_Bag(self) -> Bag:
          return self.bag
  ```
  
  - 매표소를 구현한다.
  
  ```python
  class TicketOffice:
      def __init__(self, amount, tickets:list[Ticket]):
          self.amount = amount
          self.tickets = tickets
      
      def get_ticket(self) -> Ticket:
          return self.tickets.pop()
      
      def plus_amount(self, amount):
          self.amount += amount
  ```
  
  - 판매원을 구현한다.
  
  ```python
  class TicketSeller:
      def __init__(self, ticket_office:TicketOffice):
          self.ticket_office = ticket_office
      
      def get_ticket_office(self) -> TicketOffice:
          return self.ticket_office
  ```
  
  - 극장을 구현한다.
  
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
  
  - 이 간단한 프로그램은 정상적으로 동작하지만, 몇 가지 문제점이 있다.



- 이해하기 어려운 코드
  - `Theater`의 `enter` 메서드는 아래와 같은 일을 한다.
    - 관람객의 가방을 열어 초대장이 있는지 확인한다.
    - 초대장이 있으면 매표소에 보관 중인 티켓을 관람객의 가방 안으로 옮긴다.
    - 초대장이 없으면 관람객의 가방에서 티켓 가격 만큼의 현금을 꺼내 매표소에 추가한 후 매표소에 보관 중인 티켓을 관람객의 가방 안으로 옮긴다.
  - 위 코드의 문제는 `Audience`와 `TicketSeller`가 `Theater`의 통제를 받는 수동적인 존재라는 것이다.
    - 극장은 관객의 가방을 마음대로 열어볼 수 있고, 안의 내용물을 가져갈 수도 있다.
    - 또한 극장은 매표소에 보관 중인 티켓과 현금에도 접근할 수 있다.
    - 무엇보다 티켓을 꺼내 관람객의 가방에 넣고, 관람객에게 받은 돈을 매표소에 적립하는 일을 판매원이 아닌 극장이 수행한다는 점이다.
  - 위 코드는 코드를 처음 읽는 사람이 예상한 방향과 다르게 동작한다. 
    - 이는 `Theater` 클래스에 너무 많은 역할이 몰려 있어 다른 클래스들은 역할을 잃어버렸기 때문이다.
    - 이로 인해 코드를 이해하기 힘들어진다.



- 변경에 취약한 코드

  - 위 코드의 가장 큰 문제는 변경에 취약하다는 것이다.

    - 위 코드는 관람객이 현금과 초대장을 보관하기 위해 항상 가방을 들고 다닌다고 가정한다.
    - 또한 판매원이 매표소에서만 티켓을 판매한다고 가정한다.
    - 만약 관람객이 가방을 들고 있지 않을 경우, `Audience` 클래스에서 `Bag`을 제거해야함은 물론 `Audience`의 `Bag`에 직접 접근하는 `Theater`의 `enter` 메서드도 수정해야한다. 

  - 한 클래스가 다른 클래스의 내부에 대해 더 많이 알면 알수록 클래스를 수정하기 어려워진다.

    - 위 코드에서 `Theater`는 관램객이 가방을 들고 있고, 판매원이 매표소에서만 티켓을 판매한다는 지나치게 세부적인 사실에 의존해서 동작한다.
    - 따라서 `Theater`가 의존하는 클래스의 변경 사항이 `Theater`에도 영향을 미치게 된다.

  - 의존성 문제

    - 결국 변경에 취약하다는 문제는 객체 사이의 의존성과 관련된 문제다.
    - 의존성은 변경에 대한 영향을 암시하며, 의존성이라는 말 속에는 어떤 객체가 변경될 때 그 객체에게 의존하는 다른 객체도 함꼐 변경될 수 있다는 사실에 내포돼 있다.

    - 그렇다고 객체 사이의 의존성을 완전히 없애는 것이 정답은 아니다.
    - 객체지향 설계는 서로 의존하면서 협력하는 개체들의 공동체를 구축하는 것이다.
    - 따라서 애플리케이션의 기능을 구현하는 데 필요한 최소한의 의존성만 유지하고 불필요한 의존성을 제거하는 데 목표를 둬야 한다.

  - 결합도(coupling)

    - 객체 사이의 의존성이 과한 경우를 가리켜 결합도가 높다고 한다.
    - 반대로 객체들이 합리적인 수준으로 의존할 경우에는 결합도가 낮다고 말한다.
    - 결합도는 의존성과 관련되어 있기에 결합도 역시 변경과 관련이 있다.
    - 두 객체 사이의 결합도가 높을수록 함께 변경될 확률도 높아지기에 변경이 어려워진다.
    - 따라서 설계의 목표는 객체 사이의 결합도를 낮추는 것이어야 한다.



- 설계 개선하기

  - 위 코드의 문제를 해결하는 방법은 `Theater`가 `Audience`와 `TicketSeller`에 관해 너무 세세한 부분까지 알지 못하도록 정보를 차단하는 것이다.
    - 다시 말해 `Audience`와 `TicketSeller`를 자율적인 객체로 만들면 되는 것이다.
  - `Theater.enter()`에서 `TicketOffice`에 접근하는 모든 코드를 `TicketSeller` 내부로 숨긴다.
    - `TicketSeller`에 `sell_to` 메서드를 추가하고 `Theater`에 있던 로직을 이 메서드로 옮긴다.
    - 외부에서는 `TicketSeller`의 `TicketOffice` 인스턴스에 접근할 수 없도록 변경한다.
    - 이처럼 개념적이나 물리적으로 객체 내부의 세부적인 사항을 감추는 것을 **캡슐화**라고 부른다.
    - 이제 `Theater`는 `TicketSeller` 내부에 `TicketOffice`가 있다는 것을 알지 못한다.
    - 단지 `ticket_seller`가 `sell_to` **메시지를 이해하고 응답할 수 있다는 사실만 알고 있을 뿐**이다.
    - 즉, 이제 `Theater`는 `TicketSeller`의 **인터페이스**에만 의존한다.

  ```python
  class TicketSeller:
      def __init__(self, ticket_office:TicketOffice):
          # 외부에서 TicketOffice에 접근할 수 없도록 private으로 선언한다.
          self._ticket_office = ticket_office
          
      # TicketOffice를 반환하던 get_ticket_office 메서드를 삭제한다.
      # def get_ticket_office(self) -> TicketOffice:
      #    return self.ticket_office
      
      def sell_to(self, audience: Audience):
          if audience.getBag().has_invitation():
              ticket = self._ticket_office().get_ticket()
              audience.get_bag().set_ticket(ticket)
          else:
              ticket = self._ticket_office.get_ticket()
              audience.get_bag().minus_amount(ticket.get_fee())
              self._ticket_office.plus_amount(ticket.get_fee())
              audience.get_bag().set_ticket(ticket)
              
              
  class Theater:
      def __init__(self, ticket_seller: TicketSeller):
          self.ticket_seller = ticket_seller
      
      def enter(self, audience: Audience):
          self.ticket_seller.sell_to(audience)
  ```
  
  - `Audience` 캡슐화
    - `TicketSeller`는 `Audience`의 `get_bag` 메서드를 호출해서 `Audience`내부의 `Bag` 인스턴스에 직접 접근하므로, `Audience`는 아직 자율적인 객체가 아니다.
    - `Bag`에 접근하는 모든 로직을 `Audience` 내부로 감춘다.
    - 이를 통해 `TicketSeller`도 `Audience`의 구현이 아닌 인터페이스에만 의존하게 된다.
  
  ```python
  class Audience:
      def __init__(self, bag: Bag=None):
          # 외부에서 Bag에 접근할 수 없도록 private으로 선언한다.
          self._bag = bag
      
      # 원래 있던 get_bag 메서드는 삭제한다.
      # def get_Bag(self) -> Bag:
      #    return self.bag
      
      # 기존에 TicketSeller에서 Audience를 통해서 Bag에 직접 접근하는 부분을 Audience 내부로 옮겨온다.
      def buy(self, ticket: Ticket) -> int:
          if self._bag.has_invitation():
              self._bag.set_ticket(ticket)
              return 0
          else:
              self._bag.set_ticket(ticket)
              self._bag.minus_amount(ticket.get_fee())
              return ticket.get_fee()
          
          
  class TicketSeller:
      def __init__(self, ticket_office:TicketOffice):
          self._ticket_office = ticket_office
      
      def sell_to(self, audience: Audience):
          self._ticket_office.plus_amount(audience.buy(self._ticket_office.get_ticket()))
  ```
  
  - 응집도(cohesion)
    - 위에서는 객체의 자율성을 높이는 방식으로 코드를 개선했다.
    - 객체의 자율성이 높아질수록 결합도는 낮아지고, 응집도가 높아진다.
    - 객체가 밀접하게 연관된 작업만을 수행하고 연관성 없는 작업은 다른 객체에게 위임한다면, 객체의 응집도가 높다고 할 수 있다.
    - 객체의 응집도를 높이기 위해서는 객체 스스로 자신의 데이터를 책임져야한다.



- 절차지향과 객체지향
  - 절차적 프로그래밍
    - 수정 전의 코드에서는 `Theater`의 `enter` 메서드 안에서 `Audience`와 `TicketSeller`로부터 `Bag`과 `TicketOffice`를 가져와 관람객을 입장시키는 절차를 구현했다.
    - `Audience`, `TicketSeller`, `Bag`, `TicketOffice`는 관람객을 입장시키는 데 필요한 정보를 제공하고, 모든 처리는 `Theater.enter` 메서드 안에 존재했었다.
    - 이 관점에서 `Theater.enter`는 프로세스며, 다른 class들은 데이터다.
    - 이처럼 프로세스와 데이터를 별도의 모듈에 위치시키는 방식을 절차적 프로그래밍이라고 부른다.
    - 만약 코드에서 데이터와 데이터를 사용하는 프로세스가 별도의 객체에 위치하고 있다면 절차적 프로그래밍 방식을 따르고 있을 확률이 높다.
  - 절차적 프로그래밍의 문제
    - 절차적 프로그래밍의 세계에서는 `Theater`를 제외한 모든 클래스가 수동적인 객체일 뿐이었다.
    - 절차적 프로그래밍은 우리의 예상을 너무나도 쉽게 벗어나기 때문에 코드를 읽는 사람과 원활하게 의사소통하지 못한다.
    - 절차적 프로그래밍에서는 데이터의 변경으로 인한 영향을 지역적으로 고립시키기 어렵다.
    - 예를 들어 `Audience`와 `TicketSeller`의 내부 구현을 변경하려면 `Theater`의 `enter` 메서드를 함께 변경해야한다.
    - 이처럼 절차적 프로그래밍은 변경하기 어려운 코드를 양산하는 경향이 있다.
  - 객체 지향 프로그래밍
    - 수정 후의 코드처럼 자신의 데이터를 스스로 처리하도록 하여 데이터와 프로세스가 동일한 모듈 내에 위치하도록 하는 프로그래밍 방식을 객체 지향 프로그래밍이라고 부른다.
    - 절차적 프로그래밍에 비해 변경의 여파가 작다.



- 책임의 이동(Shift of Responsibility)
  - 두 방식 간의 근본적인 차이를 만드는 것은 책임의 이동이다.
    - 변경하기 전 절차적 프로그래밍에 가까운 코드에서는 책임이 `Theater`에 집중되어 있었다.
    - 반면, 변경 후 객체지향 설계에서는 각 객체가 분할된 책임을 스스로 처리했다.
    - 이처럼 집중된 책임을 여러 곳으로 이동시키는 것을 책임의 이동이라 한다.
  - 객체지향 설계에서는 각 객체에 책임이 적절하게 분배된다.
    - 따라서 각 객체는 자신을 스스로 책임진다.
    - 객체지향 애플리케이션은 스스로 책임을 수행하는 자율적인 객체들의 공동체를 구성함으로써 완성된다.
  - 적절한 객체에 적절한 책임을 할당하면 이해하기 쉬운 구조와 읽기 쉬운 코드를 얻을 수 있다.



- 추가로 개선하기

  - `Bag`은 아직도 `Audience`에게 끌려다니는 수동적인 객체에 머물러 있으므로, `Bag`을 자율적은 객체로 변경한다.
    - 방식은 위에서 했던 것과 동일하다.
  
  
  ```python
  class Bag:
      def __init__(self, amount=None, invitation: Invitation=None):
          if not amount and not invitation:
              raise Exception()
          
          self._amount = amount
          self._invitation = invitation
          self._ticket: Ticket = None
      
      def _has_invitation(self):
          return self._invitation is not None
      
      def _set_ticket(self, ticket:Ticket):
          self._ticket = ticket
          
      def _minus_amount(self, amount: int):
          self._amount -= amount
      
      def hold(self, ticket:Ticket):
          if self._has_invitation():
              self._set_ticket(ticket)
              return 0
          else:
              self._set_ticket(ticket)
              self._minus_amount(ticket.get_fee())
              return ticket.get_fee()
  ```

  - 이에 맞춰 `Audience`도 `Bag`의 구현이 아닌 인터페이스에 의존하도록 수정한다.
  
  ```python
  class Audience:
      def __init__(self, bag: Bag=None):
          self._bag = bag
      
      def buy(self, ticket: Ticket) -> int:
          return self._bag.hold(ticket)
  ```

  - `TicketOffice` 역시 아직까지는 자율적인 객체라고 할 수 없으므로, `TicketOffice`도 변경한다.
  
  ```python
  class TicketOffice:
      def __init__(self, amount, tickets:list[Ticket]):
          self.amount = amount
          self.tickets = tickets
      
      def _get_ticket(self) -> Ticket:
          return self.tickets.pop()
      
      def _plus_amount(self, amount):
          self.amount += amount
      
      def sell_ticket_to(self, audience: Audience):
          self._plus_amount(audience.buy(self._get_ticket()))
  ```

  - `TicketSeller`도 이에 맞게 수정한다.
  
  ```py
  class TicketSeller:
      def __init__(self, ticket_office:TicketOffice):
          self._ticket_office = ticket_office
      
      def sell_to(self, audience: Audience):
          self._ticket_office.sell_ticket_to(audience)



- 훌륭한 설계는 적절한 트레이드오프의 결과물이다.
  - 추가 개선의 결과 `TicketOffice`와 `Audience` 사이에 새로운 의존성이 생겨났다.
    - 변경 전에는 새로운 의존성이 추가되었으므로, `TicketOffice`와 `Audience`의 결합도가 높아지게 됐다.
    - `TicketOffice`의 자율성은 높아졌지만, 전체 설계의 관점에서는 결합도가 상승했다.
  - 설계는 트레이드오프의 산물이다.
    - 어떤 기능을 설계하는 방법은 한 가지 이상일 수 있다.
    - 동일한 기능을 한 가지 이상의 방법으로 설계할 수 있기 때문에 결국 설계는 트레이드오프의 산물이다.
    - 모든 사람들을 만족시킬 수 있는 설계를 만드는 것은 불가능에 가깝다.



- 의인화(anthropomorphism)
  - 현실 세계에서 가방이나 극장 등은 자율적인 존재가 아닌, 관객에 의해 통제되는 수동적인 존재이다.
  - 그러나 객체지향의 세계에서는 현실 세계에서 수동적인 존재라 하더라도, 자율적인 존재로 취급하는 것이 가능하다.
  - 이와 같이 현실 세계의 존재를 능동적이고 자율적인 존재로 소프트웨어 객체를 설계하는 것을 의인화라고 한다.



- 객체지향 설계

  > 설계란 코드를 배치하는 것이다[Metz]

  - 설계와 코드 작성
    - 설계가 코드 작성보다 높은 차원의 행위라고 생각하는 사람도 있지만, 설계를 구현과 떨어트려서 이야기하는 것은 불가능하다.
    - 설계는 코드를 작성하는 매 순간 코드를 어떻게 배치할 것인지 결정하는 과정에서 나온다.
    - 설계는 코드 작성의 일부이며 코드를 작성하지 않고서는 검증할 수 없다.
  - 좋은 설계
    - 오늘 요구하는 기능을 온전히 수행하면서 내일의 변경을 매끄럽게 수용할 수 있는 설계다.
    - 변경을 수용할 수 있는 설계가 중요한 이유는 요구사항이 항상 변경되기 때문이며, 코드가 변경될 때 버그가 추가될 가능성이 높기 때문이다.
  - 객체지향 설계
    - 객체지향 프로그래밍은 의존성을 효율적으로 통제할 수 있는 다양한 방법을 제공함으로써 요구사항 변경에 좀 더 수월하게 대응할 수 있는 가능성을 높여준다.
    - 객체지향은 사람들이 세상에 대해 예상하는 방식대로 객체가 행동하리라는 것을 보장함으로써 코드를 좀 더 쉽게 이해할 수 있게 한다.
    - 코드가 이해하기 쉬울수록 변경하기도 쉬워진다.
  - 훌륭한 객체지향 설계란 협력하는 객체 사이의 의존성을 적절하게 관리하는 설계다.
    - 객체들이 협력하는 과정 속에서 객체들은 다른 객체에 의존하게 된다.
    - 메시지를 전송하기 위해 필요한 지식들이 두 객체를 결합시키고 이 결합이 객체 사이의 의존성을 만든다.
    - 이렇게 생성된 의존성을 잘 관리하여 변경이 용이한 설계가 진정한 객체지향 설계다.





# 객체지향 프로그래밍

- 영화 예매 시스템의 할인 기능 요구사항

  - 할인액을 결정하는 두 가지 규칙이 존재하는데, 하나는 할인 조건이라 부르고 다른 하나는 할인 정책이라 부른다.
    - 할인 조건은 다수의 조건을 지정하거나 혼합하는 것이 가능하지만, 할인 정책은 하나의 정책만 할당할 수 있다.
    - 할인 정책은 1인을 기준으로 책정된다.
  - 할인 조건은 가격의 할인 여부를 결정하며 순서 조건과 기간 조건의 두 종류로 나눌 수 있다.
    - 순서 조건은 상영 순번을 이용해 할인 여부를 결정하는 규칙이다(e.g. 순번이 3번일 경우 매일 3번째로 사양되는 영화를 예매한 사용자들에게 할인 혜택 제공).
    - 기간 조건은 영화 상영 시작 시간을 이용해 할인 여부를 결정하며, 요일, 시작 시간, 종료 시간의 세 부분으로 구성된다.
  - 할인 정책은 할인 요금을 결정하며, 할인 정책에는 금액 할인 정책과 비율할인 정책이 있다.
    - 금액 할인 정책은 예매 요금에서 일정 금액을 할인해주는 방식이다.
    - 비율 할인 정책은 정가에서 일정 비율의 요금을 할인해 주는 방식이다.

  - 할인을 적용하기 위해서는 할인 조건과 할인 적책을 함께 조합해서 사용한다.
    - 먼저 사용자의 예매 정보가 할인 조건 중 하나라도 만족하는지 검사한다.
    - 할인 조건을 만족할 경우 할인 정책을 이용해 할인 요금을 계산한다.
    - 할인 정책은 적용돼 있지만 할인 조건을 만족하지 못하는 경우나 아예 할인 정책이 적용돼 있지 않은 경우에는 요금을 할인하지 않는다.



- 협력, 객체, 클래스
  - 객체지향은 클래스가 아닌 객체에 초점을 맞춰야한다.
    - 어떤 클래스가 필요한지를 고민하기 전에 어떤 객체들이 필요한지 고민해야한다.
    - 클래스는 공통적인 상태와 행동을 공유하는 객체들을 추상화한 것이다.
    - 따라서 클래스의 윤곽을 잡기 위해서는 어떤 객체들이 어떤 상태와 행동을 가지는지를 먼저 결정해야한다.
    - 객체를 중심에 두는 접근 방법은 설계를 단순하고 깔끔하게 만든다.
  - 객체를 독립적인 존재가 아니라 기능을 구현하기 위해 협력하는 공동체의 일원으로 봐야 한다.
    - 객체는 다른 객체에게 도움을 주거나 의존하면서 살아가는 협력적인 존재다.
    - 객체를 협력하는 공동체의 일원으로 바라보는 것은 설계를 유연하고 확장 가능하게 만든다.
  - 객체의 모양과 윤곽이 잡히면 공통된 특성과 상태를 가진 객체들을 타입으로 분류하고 이 타입을 기반으로 클래스를 구현해야한다.
    - 훌륭한 협력이 훌륭한 객체를 낳고, 훌령한 객체가 훌륭한 클래스를 낳는다.



- 도메인의 구조를 따르는 프로그램 구조
  - 도메인(domain)
    - 소프트웨어는 사용자가 가진 어떤 문제를 해결하기 위해 만들어진다.
    - 문제를 해결하기 위해 사용자가 프로그램을 사용하는 분야를 도메인이라 부른다.
  - 객체지향과 도메인
    - 객체지향 패러다임이 강력한 이유는 요구사항을 분석하는 초기 단계부터 프로그램을 구현하는 마지막 단계까지 객체라는 동일한 추상화 기법을 사용할 수 있기 때문이다.
    - 요구사항과 프로그램을 객체라는 동일한 관점에서 바라볼 수 있기 때문에 도메인을 구성하는 개념들이 프로그램의 객체와 클래스로 매끄럽게 연결될 수 있다.
    - 일반적으로 클래스의 이름은 대응되는 도메인 개념의 이름과 동일하거나 유사하게 지어야 한다.
    - 클래스 사이의 관계도 최대한 도메인 개념 사이에 맺어진 관계와 유사하게 만들어서 프로그램의 구조를 이해하고 예상하기 쉽게 만들어야 한다.



- 클래스 구현하기
  - 클래스를 구현할 때 가장 중요한 것은 클래스의 경계를 구분 짓는 것이다.
    - 클래스는 내부와 외부로 구분되며 훌륭한 클래스를 설계하기 위한 핵심은 어떤 부분을 외부에 공개하고 어떤 부분을 감출지를 결정하는 것이다.
    - 클래스와 내부와 외부를 구분해야 하는 이유는 **경계의 명확성이 객체의 자율성을 보장**하기 때문이다.
    - 또한 이를 통해 프로그래머에게 구현의 자유를 제공하기 때문이다.
  - 자율적인 객체
    - 객체는 상태와 행동을 함께 가지는 복합적인 존재이면서, 스스로 판단하고 행동하는 자율적인 존재이다.
    - 객체지향 이전의 패러다임과 달리 객체지향에서는 객체라는 단위 안에 데이터와 기능을 한 덩어리로 묶는다.
    - 이처럼 데이터와 기능을 객체 내부로 함께 묶는 것을 캡슐화라고 부른다.
    - 대부분의 객체지향 프로그래밍 언어들은 캡슐화에서 한 걸음 더 나아가서 접근 제어(access control) 매커니즘을 함께 제공한다.
    - **객체 내부에 대한 접근을 통제하는 이유는 객체를 자율적인 존재로 만들기 위해**서다.
    - 객체지향의 핵심은 자율적인 객체들의 공동체를 구성하는 것이며, 객체가 자율적이기 위해서는 외부의 간섭을 최소화해야 한다.
    - 외부에서는 객체가 어떤 상태에 놓여 있는지, 어떤 생각을 하고 있는지 알아서는 안 되며, 결정에 직접 개입하려고 해도 안 된다.
    - 캡슐화와 접근 제어는 객체를 외부에서 접근 가능한 퍼블릭 인터페이스와 내부에서만 접근 가능한 구현으로 나눈다.
    - 이 인터페이스와 구현의 분리 원칙은 객체지향 프로그램을 만들기 위해 따라야 하는 핵심 원칙이다.
  - 프로그래머의 자유
    - 프로그래머의 역할을 클래스 작성자(class creator)와 클라이언트 프로그래머(client programmer)로 구분하는 것이 유용하다.
    - 클래스 작성자는 새로운 데이터 타입을 프로그램에 추가하고, 클라이언트 프로그래머는 클래스 작성자가 추가한 데이터 타입을 사용한다.
    - 클래스 작성자는 클라이언트 프로그래머에게 필요한 부분만 공개하고 나머지는 숨겨야하는데, 이를 구현 은닉(implementation hiding)이라 부른다.
    - 구현 은닉은 두 종류의 프로그래머 모두에게 유용한 개념이다.
    - 이를 통해 클래스 작성자는 클라이언트 프로그래머에 대한 영향을 걱정하지 않고도 내부 구현을 마음대로 변경할 수 있다.
    - 클라이언트 프로그래머는 내부의 구현은 모른채 인터페이스만 알아도 클래스를 사용할 수 있다.



- 협력하는 객체들의 공동체를 구현한다.

  - 먼저 상영 클래스를 구현한다.
    - 인스턴스 변수는 모두 private으로, 메서드는 모두 public으로 선언한다.

  ```python
  from datetime import datetime
  
  
  class Screening:
      def __init__(self, movie: Movie, sequence: int, when_screened: datetime):
          self._movie = movie
          self._sequence = sequence
          self._when_screened = when_screened
  
      def get_start_time(self):
          return self._when_screened
  
      def is_sequence(self, sequence: int):
          return self._sequence == sequence
  
      def get_movie_fee(self):
          return self._movie.get_fee()
  
      def _calculate_fee(self, audience_count: int):
          return self._movie.calculate_movie_fee(self).times(audience_count)
  
      def reserve(self, customer: Customer, audience_count: int):
          return Reservation(customer, self, self.calculate_fee(audience_count), audience_count)
  ```

  - `Money` 클래스를 구현한다.
    - 굳이 int를 사용하지 않고 `Money` 클래스를 따로 구현한 이유는 저장하는 값이 금액과 관련되어 있다는 의미를 보다 분명히 전달하고, 금액과 관련된 로직이 서로 다른 곳에 중복되어 구현되는 것을 막기 위해서다.

  ```python
  class Money:
      def __init__(self, amount):
          self._amount = amount
  
      @classmethod
      def wons(self, amount) -> Self:
          return Money(amount)
  
      def plus(self, amount: Self) -> Self:
          return Money(self._amount + amount._amount)
  
      def minus(self, amount: Self) -> Self:
          return Money(self._amount - amount._amount)
  
      def times(self, percent: int) -> Self:
          return Money(self._amount * percent)
  
      def is_lt(self, other: Self) -> bool:
          return self._amount < other._amount
  
      def is_gte(self, other: Self) -> bool:
          return self._amount >= other._amount
  ```

  - `Reservation` 클래스를 구현한다.

  ```python
  class Reservation:
      def __init__(self, customer: Customer, screening: Screening, fee: Money, audience_count: int):
          self.customer = customer
          self.screening = screening
          self.fee = fee
          self.audience_count = audience_count
  ```

  - 협력(Collaboration)
    - 영화를 예매하기 위해 각 인스턴스들은 서로의 메서드를 호출하며 상호작용한다.
    - 이처럼 시스템의 어떤 기능을 구현하기 위해 객체들 사이에 이뤄지는 상호작용을 협력이라고 부른다.
    - 객체지향 프로그램을 작성할 때는 먼저 협력의 관점에서 어떤 객체가 필요한지를 결정하고, 객체들의 공통 상태와 행위를 구현하기 위해 클래스를 작성한다.
  - 협력의 방식
    - 객체는 다른 객체의 엔터페이스에 공개된 행동을 수행하도록 요청 할 수 있다.
    - 요청을 받은 객체는 자율적인 방법에 따라 요청을 처리한 후 응답한다.
    - 객체가 다른 객체와 상호작용 할 수 있는 유일한 방법은 메시지를 전송하는 것이다.
    - 다른 객체에게 요청이 도착할 때 해당 객체가 메시지를 수신했다고 이야기한다.
    - 메시지를 수신한 객체는 스스로의 결정에 따라 자율적으로 메시지를 처리할 방법을 결정한다.
  - 메서드와 메시지
    - 수신된 메시지를 처리하기 위한 자신만의 방법을 메서드라 부른다.
    - 메시지와 메서드를 구분하는 것은 매우 중요하며, 이를 구분하는 것에서 다형성의 개념이 출발한다.
    - 위에서 `Screening`이 `Movie`의 `calculate_movie_fee` '메서드를 호출한다'는 표현 보다는 '메시지를 전송한다'는 표현이 더 적절한 표현이다.
    - 사실 `Screening`은 `Movie`의 내부에 `caclulate_movie_fee` 메서드가 있는지조차 알지 못한다.
    - 단지 `Movie`가 `calculate_movie_fee`라는 메시지에 응답할 수 있다고 믿고 메시지를 전송할 뿐이다.



- 할인 요금을 구하기 위한 협력

  - `DiscountCondition`을 구현한다.
    - 할인 조건을 구현하기 위한 클래스이다.
    - 여러 할인 조건들은 공유하는 코드가 생길 수 밖에 없으므로, 중복 코드를 제거하기 위해 부모 클래스를 생성한다.
    - 부모 클래스는 직접 생성할 일이 없으므로 인터페이스로 구현한다.

  ```python
  class DiscountCondition(metaclass=ABCMeta):
      @abstractmethod
      def is_satisfied_by(self, screening: Screening) -> bool:
          ...
  
  
  class SequenceCondition(DiscountCondition):
      def __init__(self, sequence: int):
          self._sequence = sequence
  
      def is_satisfied_by(self, screening: Screening) -> bool:
          return screening.is_sequence(self._sequence)
  
  
  class PeriodCondition(DiscountCondition):
      def __init__(self, day_of_week: int, start_time: time, end_time: time):
          self.day_of_week = day_of_week
          self.start_time = start_time
          self.end_time = end_time
  
      def is_satisfied_by(self, screening: Screening) -> bool:
          return screening.get_start_time().weekday() == self.day_of_week and \
                 self.start_time <= screening.get_start_time() and \
                 self.end_time >= screening.get_start_time()
  ```

  - `DiscountPolicy` 클래스를 구현한다.
    - 할인 정책은 금액 할인과 비율 할인으로 구분되는데, 두 방식은 계산하는 방식만 다를 뿐 대부분이 유사하다.
    - 따라서 할인 조건을 구현할 때와 마찬가지로, 두 정책의 부모 클래스를 생성할 것이다.

  ```python
  class DiscountPolicy:
  
      def __init__(self, conditions: list[DiscountCondition]):
          self.conditions = conditions
  
      @abstractmethod
      def get_discount_amount(self, screening: Screening) -> Money:
          ...
  
      def calculate_discount_amount(self, screening: Screening):
          for condition in self.conditions:
              if condition.is_satisfied_by(screening):
                  return self.get_discount_amount(screening)
  
          return Money.wons(0)
  
  
  class AmountDiscountPolicy(DiscountPolicy):
  
      def __init__(self, discount_amount: Money, conditions: list[DiscountCondition]):
          super().__init__(conditions)
          self.discount_amount = discount_amount
  
      def get_discount_amount(self, screening: Screening) -> Money:
          return self.discount_amount
  
  
  class PercentDiscountPolicy(DiscountPolicy):
  
      def __init__(self, percent: float, conditions: list[DiscountCondition]):
          super().__init__(conditions)
          self.percent = percent
  
      def get_discount_amount(self, screening: Screening) -> Money:
          return screening.get_movie_fee().times(self.percent)
  ```

  - `Movie` 클래스를 구현한다.
    - `calculate_movie_fee` 메서드는 `_discount_policy`에 `caculate_discount_amount` 메시지를 전송해 할인 요금을 반환 받는다.	

  ```python
  class Movie:
      def __init__(self, title: str, running_time: time, fee: Money, discount_policy: DiscountPolicy):
          self._title = title
          self._running_time = running_time
          self._fee = fee
          self._discount_policy = discount_policy
  
      def get_fee(self) -> Money:
          return self._fee
  
      def calculate_movie_fee(self, screening: Screening):
          return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))
  ```



- 상속과 다형성
  - 컴파일 시간 의존성과 실행 시간 의존성
    - 