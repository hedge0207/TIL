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

  - 관람객의 소지품을 표현할 Bag class를 구현한다.
    - 관람객은 초대장, 표, 현금 중 하나를 가지고 있어야 공연 관람이 가능하므로 이 셋을 instance 변수로 추가하고, 관련 메서드들을 추가한다.
    - 이벤트에 당첨된 관람객의 가방 안에는 현금과 초대장이 들어있지만 당첨되지 않은 관람객의 가방 안에는 초대장이 들어있지 않을 것이다.
    - 따라서 Bag instance의 상태는 현금과 초대장을 함께 보관하거나 초대장 없이 현금만 보관하는 두 가지 중 하나일 것이다.
    - Bag instance를 생성하는 시점에 이 제약을 강제할 수 있도록 생성자를 구현한다.

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
      
      def has_ticket(self):
          return self.ticket is not None
      
      def set_ticket(self, ticket:Ticket):
          self.ticket = ticket
          
      def minus_amount(self, amount: int):
          self.amount -= amount
      
      def plus_amount(self, amount:int):
          self.amount += amount
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
          return ticket.pop()
      
      def minus_amount(self, amount):
          self.amount -= amount
      
      def plust_amount(self, amount):
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

  ```py
  class Theater:
      def __init__(self, ticket_seller: TicketSeller):
          self.ticket_seller = ticket_seller
      
      def enter(self, audience: Audience):
          if audience.getBag().has_invitation():
              ticket = self.ticket_seller.get_ticket_office().get_ticket()
              audience.get_bag().set_ticket(ticket)
          else:
              ticket = self.ticket_seller.get_ticket_office().get_ticket()
              audience.get_bag().minus_amount(ticket.get_fee())
              ticket_seller.get_ticket_office().plus_amount(ticket.get_fee())
              audience.get_bag().set_ticket(ticket)
  ```

  - 이 간단한 프로그램에는 정상적으로 동작하지만, 몇 가지 문제점이 있다.



- 예상을 빗나가는 코드
  - `Theater` class의 `enter` method는 아래와 같은 일을 한다.
    - 관람객의 가방을 열어 초대장이 있는지 확인한다.
    - 초대장이 있으면 매표소에 보관 중인 티켓을 관람객의 가방 안으로 옮긴다.
    - 초대장이 없으면 관람객의 가방에서 티켓 가격 만큼의 현금을 꺼내 매표소에 추가한 후 매표소에 보관 중인 티켓을 관람객의 가방 안으로 옮긴다.
  - 문제는 관람객과 판매원이 극장의 통제를 받는 수동적인 존재라는 것이다.
    - 극장은 관객의 가방을 마음대로 열어볼 수 있고, 안의 내용물을 가져갈 수도 있다.
    - 또한 극장은 매표소에 보관 중인 티켓과 현금에도 접근할 수 있다.
    - 무엇보다 티켓을 꺼내 관람객의 가방에 넣고, 관람객에게 받은 돈을 매표소에 적립하는 일을 판매원이 아닌 극장이 수행한다는 점이다.
  - 위 코드는 코드를 처음 읽는 사람이 예상한 방향과 다르게 동작한다. 
    - 이는 `Theater` class에 너무 많은 역할이 몰려 있어 다른 클래스들은 역할을 잃어버렸기 때문이다.



- 변경에 취약한 코드

  - 위 코드의 가장 큰 문제는 변경에 취약하다는 것이다.

    - 위 코드는 관람개이 현금과 초대장을 보관하기 위해 항상 가방을 들고 다닌다고 가정한다.
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