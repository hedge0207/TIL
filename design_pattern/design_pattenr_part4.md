# State Pattern

- 최첨단 뽑기 기계

  - 뽑기 기계에는 아래와 같이 네 종류의 상태가 있다.
    - 동전 없음
    - 동전 있음
    - 알맹이 판매
    - 알맹이 매진

  - 이 시스템에서 일어날 수 있는 행동들은 아래와 같다.
    - 동전 투입
    - 동전 반환
    - 손잡이 돌림
    - 알맹이 내보냄
  - 기계 역할을 하는 클래스를 만든다.

  ```python
  class GumballMachine:
      # 각 상태를 저장할 변수를 선언한다.
      SOLD_OUT = 0
      NO_QUARTER = 1
      HAS_QUARTER = 2
      SOLD = 3
  
      def __init__(self, count):
          self.state = self.SOLD_OUT
          # 캡슐의 개수를 저장하기 위한 변수
          self.count = count
          # 캡슐 개수가 0보다 크면 동전이 들어오길 기다리는 상태가 된다.
          if count > 0:
              self.state = self.NO_QUARTER
  
      def insert_quarter(self):
          if self.state == self.HAS_QUARTER:
              print("이미 동전이 들어가 있습니다.")
          elif self.state == self.NO_QUARTER:
              self.state = self.HAS_QUARTER
              print("동전을 넣으셨습니다.")
          elif self.state == self.SOLD_OUT:
              print("남아 있는 캡슐이 없습니다. 다음에 이용해주세요.")
          elif self.state == self.SOLD:
              print("캡슐을 내보내고 있습니다.")
  
      def eject_quarter(self):
          if self.state == self.HAS_QUARTER:
              self.state = self.NO_QUARTER
              print("동전이 반환됩니다.")
          elif self.state == self.NO_QUARTER:
              print("반환 할 동전이 없습니다.")
          elif self.state == self.SOLD_OUT:
              print("반환할 동전이 없습니다. 동전이 반환되지 않습니다.")
          elif self.state == self.SOLD:
              print("이미 캡슐을 뽑으셨습니다.")
      
      # 손잡이를 돌리는 메서드
      def turn_crank(self):
          if self.state == self.SOLD:
              print("손잡이는 한 번만 돌려주세요")
          elif self.state == self.NO_QUARTER:
              print("먼저 동전을 넣어주세요")
          elif self.state == self.SOLD_OUT:
              print("매진되었습니다.")
          elif self.state == self.HAS_QUARTER:
              print("손잡이를 돌리셨습니다.")
              self.state = self.SOLD
              self.dispense()
  
      # 캡슐을 내보내는 메서드
      def dispense(self):
          if self.state == self.SOLD:
              print("캡슐을 내보내고 있습니다.")
              self.count -= 1
              if self.count == 0:
                  print("이제 남은 알맹이가 없습니다.")
                  self.state = self.SOLD_OUT
              else:
                  self.state = self.NO_QUARTER
          # 아래의 세 경우는 오류가 나는 상황이다.
          elif self.state == self.NO_QUARTER:
              print("먼저 동전을 넣어주세요")
          elif self.state == self.SOLD_OUT:
              print("매진되었습니다.")
          elif self.state == self.HAS_QUARTER:
              print("알맹이를 내보낼 수 없습니다.")
  ```

  - 기능 추가 요청이 들어왔다.
    - 10번에 한 번 꼴로 손잡이를 돌릴 때 알맹이 2개가 나오도록 코드를 고쳐야한다.
    - 이제 기존에 선언했던 상태 변수에 알맹이 2개가 나오는 당첨 상태를 추가해야한다.
    - 그리고 모든 메서드에 조건문 분기를 추가해야한다.
    - 이 방식은 확장성이 매우 떨어지므로 리팩터링을 하기로 한다.



- 새로운 디자인 구상하기

  - 상태 객체들을 별도로 생성해서 어떤 행동이 발생하면 상태 객체에서 필요한 작업을 처리하도록 한다.

    - 우선 뽑기 기계와 관련된 모든 행동에 관한 메서드가 들어있는 State 인터페이스를 정의한다.
    - 그 다음 기계의 모든 상태를 대상으로 상태 클래스를 구현하는데, 기계가 어떤 상태에 있다면, 그 상태에 해당하는 상태 클래스가 모든 작업을 책임진다.

    - 마지막으로 조건문을 모두 없애고 상태 클래스에 모든 작업을 위임한다.
    - 뽑기 기계는 구성을 활용하여 각 상태 객체를 가지고 있는다.

  - State 인터페이스 구현하기

  ```python
  from abc import ABCMeta, abstractmethod
  
  
  class State(metaclass=ABCMeta):
      
      @abstractmethod
      def insert_quarter(self):
          pass
  
      @abstractmethod
      def eject_quarter(self):
          pass
  
      @abstractmethod
      def turn_crank(self):
          pass
  
      @abstractmethod
      def dispense(self):
          pass
  ```

  - `NoQuarterState` 생성하기
    - 다른 상태 클래스들도 마찬가지 방법으로 생성한다.

  ```python
  class NoQuarterState(State):
      
      def __init__(self, gumball_machine):
          self.gumball_machine = gumball_machine
      
      def insert_quarter(self):
          print("동전을 넣으셨습니다.")
          self.gumball_machine.set_state(self.gumball_machine.get_has_quarter_state())
      
      def eject_quarter(self):
          print("반환 할 동전이 없습니다.")
      
      def turn_crank(self):
          print("먼저 동전을 넣어주세요.")
      
      def dispense(self):
          print("먼저 동전을 넣어주세요.")
  ```

  - 뽑기 기계 class 수정하기

  ```python
  from state import State, HasQuarterState, NoQuarterState, SoldState, SoldOutState
  
  
  class GumballMachine:
      def __init__(self, num_gumballs):
          # 구성을 활용하여 각 상태에 대한 정보를 가지고 있는다.
          self.has_quarter_state:State = HasQuarterState()
          self.no_quarter_state:State = NoQuarterState()
          self.sold_state: State = SoldState()
          self.sold_out_state: State = SoldOutState()
  
          self.count = num_gumballs
          if self.count > 0:
              self.state = self.no_quarter_state
          else:
              self.state = self.sold_out_state
      
      def insert_quarter(self):
          self.state.insert_quarter()
      
      def eject_quarter(self):
          self.state.eject_quarter()
      
      def turn_crank(self):
          self.state.turn_crank()
          self.state.dispense()
      
      def set_state(self, state: State):
          self.state = state
      
      def release_ball(self):
          print("캡슐을 내보내고 있습니다.")
          
          if self.count > 0:
              self.count -= 1
      
      # 각 상태 객체를 위한 getter 메서드들(get_quarter_state() 등)
  ```

  - 변경 사항
    - 각 상태의 행동을 별개의 클래스로 분리.
    - if문을 전부 제거
    - 각 상태는 변경에는 닫혀있게 되었고, `GumballMachine` 클래스는 새로운 상태 클래스를 추가하는 확장에는 열려있게 되었다.
    - 훨씬 이해가 쉬운 상태가 되었다.
  - 생각해볼 거리
    - 위 코드상으로 각 State마다 중복되는 코드가 다수 존재하고, 특히 각 상태별 부적절한 행동에 대한 대응은 거의 유사할 것이다.
    - 따라서, `State`를 인터페이스로 정의하는 대신 추상 클래스로 정의하고, 부적절한 행동에 대한 예외처리를 기본 동작으로 추가해도 될 것이다(Composite pattern에서 `MenuComponent`에 이 방식을 적용했었다). 



- 상태 패턴

  - 정의
    - 객체의 내부 상태가 바뀜에 따라 객체의 행동을 바꿀 수 있다.
    - 마치 객체의 클래스가 바뀌는 것과 같은 결과를 얻을 수 있다(클라이언트 입장에선 지금 사용하는 객체의 행동이 완전히 달라지면 마치 그 객체가 다른 클래스로부터 남들어진 객체처럼 느껴진다. 그러나 사실은 다른 클래스로 변한 것이 아니라 구성으로 여러 상태 객체를 바꿔가면서 사용하는 것이다).
  - 클래스 다이어그램
    - Context가 `request()` 메서드를 호출하면 그 작업은 상태 객체에게 맡가젼디(`state.handle()`)
    - 구상 상태 클래스는 원하는 만큼 만들 수 있다.

  ![image-20230423161204091](design_pattenr_part4.assets/image-20230423161204091.png)

  - 전략 패턴과의 관계
    - 전략 패턴과 거의 유사한 다이어그램을 가지고 있다.
    - 그러나 둘 사이에는 용도의 차이가 존재한다.
    - 상태 패턴을 사용할 때는 상태 객체의 일련의 행동이 캡슐화 되고, 상황에 따라 Context 객체에서 여러 상태 중 한 객체게 모든 행동을 맡기게 된다.
    - 클라이언트는 상태 객체를 몰라도 된다.
    - 반면에 전략 패턴의 경우 일반적으로 클라이언트가 Context 객체에게 어떤 전략을 사용할지를 지정해준다.
    - 전략 패턴은 주로 실행시에 전략 객체를 변경할 수 있는 유연성을 제공하는 용도로 사용한다.
    - 일반적으로 전략패턴은 서브클래스를 만드는 방법을 대신해서 유연성을 극대화하는 용도로 쓰인다.
    - 상속을 사용하여 클래스를 정의하다 보면 행동을 변경해야 할 때 마음대로 변경하기가 힘들다.
    - 하지만 전략 패턴을 사용하면 구성으로 행동을 정의하는 객체를 유연하게 변경할 수 있다.
  - 상태의 변경은 누가 주도해야하는가?
    - 현재 코드상으로는 현재 상태에 의해서 다음 상태가 결정된다.
    - 예를 들어 `NoQuarterState` 상태일 때,`GumballMachine`의 `insert_qurater()`메서드가 호출되면  `NoQuarterState`의 `insert_quarter()` 메서드가 호출되고, 그 안에서 `GumballMachine` 클래스의 `get_has_quarter_state()` 메서드가 호출되어 상태가 `HasQuarterState`로 변경되게 된다.
    - 즉 `insert_quarter()`가 호출 될 때 상태가 `NoQuarterState`였으므로 다음 상태가 `HasQuarterState`로 변경되는 것이다.
    - 그러나 State가 아니라 Context에서 상태 흐름을 결정하도록 해도 된다.
    - 그러나 상태 전환이 동적으로 결정된다면 State 클래스에서 처리하는 것이 좋다.
    - 예를 들어 `NoQurater`로 전환할지, 아니면  `SoldOut`으로 전환할 지는 남아 있는 캡슐의 양에 따라 동적으로 결정된다.
    - 이럴 때는 State class에서 처리하는 것이 좋다.
    - 반면에 상태 전환 코드를 State 클래스에서 관리하면, 상태 클래스 사이에 의존성이 생기는 단점이 있다.
    - 따라서 위 코드에서도 `set_state()` 메서드를 호출할 때, 구상 State 클래스를 쓰는 대신, getter 메서드를 사용하여 의존성을 최소화하려했다.

  - 클라이언트가 State 객체와 직접 연락하는 경우가 있는가?
    - 그럴 일은 없다.
    - 클라이언트는 Context만을 조작하며, 클라이언트는 Context의 상태를 직접 바꿀 수 없다(전략 패턴과의 차이).
    - 상태를 관리하는 일은 전적으로 Context가 책임져야한다.
  - 만약 여러 개의 Context instance를 생성했다면, 각 instance들이 State 객체를 공유할 수 있는가?
    - 가능하며, 실제로 그렇게 해야 하는 경우도 있다.
    - 상태 객체 내에 자체 상태를 보관하지 않아야한다는 조건만 만족하면 상관 없다.
    - 상태 객체 내에 자체 상태를 보관하려면 각 Context마다 유일한 객체가 필요하기 때문이다.
    - 일반적으로 상태를 공유할 때는 각 상태를 정적 인스턴스 변수에 할당하는 방법을 사용한다.
    - 상태 객체에서 Context에 있는 메서드 또는 인스턴스 변수를 사용해야한다면 `handle()` 메서드에 Context의 레퍼런스도 전달해야한다.



- 보너스 캡슐 기능 추가하기

  - `WinnerState` 클래스를 생성한다.

  ```python
  class WinnerState(State):
      def __init__(self, gumball_machine):
          self.gumball_machine = gumball_machine
      
      # 부적절
      def insert_quarter(self):
          print("캡슐을 내보내고 있습니다.")
      
      # 부적절
      def eject_quarter(self):
          print("이미 캡슐을 뽑으셨습니다.")
      
      # 부적절
      def turn_crank(self):
          print("이미 손잡이를 돌리셨습니다.")
      
      def dispense(self):
          self.gumball_machine.release_ball()
          if self.gumball_machine.get_count() == 0:
              self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())
          else:
              print("축하드립니다. 캡슐을 하나 더 드리겠습니다.")
              self.gumball_machine.release_ball()
              if self.gumball_machine.get_count > 0:
                  self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())
              else:
                  print("캡슐이 모두 떨어졌습니다.")
                  self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())
  ```

  - `HasQuarterState` 클래스의 `turn_crank()` 메서드를 아래와 같이 변경한다.
    - 10%의 확률로 당첨 여부를 결정해서 뽑기 기계의 상태를 `WinnerState`로 전환하는 기능을 추가한다.

  ```python
  import random
  
  class HasQuarterState(State):
      def __init__(self, gumball_machine):
          self.gumball_machine = gumball_machine
      
      def turn_crank(self):
          print("손잡이를 돌리셨습니다.")
          winner = random.choices([True, False], weights=[0.1, 0.9])[0]
  
          if winner and self.gumball_machine.get_count() > 1:
              self.gumball_machine.set_state(self.gumball_machine.get_winner_state())
          else:
              self.gumball_machine.set_state(self.gumball_machine.get_sold_state())
  ```

  - `GumballMachine` class를 아래와 같이 수정한다.

  ```python
  class GumballMachine:
      def __init__(self, num_gumballs):
          # winner_state 추가
          self.winner_state: State = WinnerState()
  ```

  
