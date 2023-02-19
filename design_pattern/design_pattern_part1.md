# Strategy Pattern

- 오리 시뮬레이션 게임, SimUduck

  - 오리 시뮬레이션 게임을 만들기 위해 아래와 같은 class들을 생성했다.
    - 모든 오리는 "quack"이라는 소리를 내며, 헤엄을 칠 수 있으므로 super class에 작성한다.
    - 오리의 종류별로 생김새는 다르므로, `display()` 메서드는 추상 메서드로 작성한다.

  ```python
  from abc import abstractmethod
  
  class Duck:
      def quack(self):
          print("quack quack")
      
      def swim(self):
          # 헤엄치는 code
      
      @abstractmethod
      def display(self):
          pass        
  
  
  class MallardDuck(Duck):
      def display(self):
          # MallardDuck의 생김새를 표현하는 code
          
          
  class RedheadDuck(Duck):
      def display(self):
          # RedheadDuck의 생김새를 표현하는 code
  ```

  - 오리에 날 수 있는 기능 추가하기.
    - 모든 오리가 날 수 있을 것이라 생각해 `Duck` class에 `fly()` 메서드를 추가한다.

  ```python
  class Duck:
      def quack(self):
          print("quack quack")
      
      def swim(self):
          # 헤엄치는 code
      
      def fly(self):
          # 나는 code
      
      @abstractmethod
      def display(self):
          pass
  ```

  - 문제 발생
    - `Duck`을 상속 받는 class 중 고무 오리를 표현한 `RubberDuck` class가 있었다.
    - 고무 오리는 날 수 없을 뿐더러 "quack" 소리를 내지도 않는다.
    - 이를 해결하기 위해 `RubberDuck` class의 메서드들을 아래와 같이 overide하여 작성한다.

  ```python
  class RubberDuck(Duck):
      def quack(self):
          print("quack quack")
      
      def swim(self):
          # 헤엄치는 code
      
      # 날 수 없으므로, 아무것도 하지 않는다.
      def fly(self):
          pass
      
      def display(self):
          # RubberDuck의 생김새를 표현하는 code
  ```

  - 새로운 문제 발생

    - 날 수 없고, "quack" 소리를 내지도 않는 나무 오리, 구리 오리, 황금 오리 등이 추가되기 시작한다.
    - 날 수 없고, "quack" 소리를 내지도 않는 무수히 많은 종류의 오리가 추가될 때 마다 메서드를 overide해야한다.

    - 해결 `fly()`와 `quack()` 메서드를 `Duck` super class에서 빼고 이를 interface로 작성한다.
    - 날 수 있고, "quack" 소리를 낼 수 있는 오리에게만 interface를 구현한다.

  ```python
  from abc import ABC, abstractmethod
  
  
  class Duck:
      def swim(self):
          # 수영하는 code
      
      @abstractmethod
      def display(self):
          pass
  
  
  class Quackable(ABC):
      @abstractmethod
      def quack(self):
          pass
  
  
  class Flyable(ABC):
      @abstractmethod
      def fly(self):
          pass
  ```

  - 이어지는 문제
    - Interface는 일반 class의 상속과는 달리, method를 상속받아서 그대로 사용할 수는 없고, 반드시 상속 받은 class에서 메서드를 구현해야 한다.
    - 만일 모든 `fly()`에 공통으로 들어가는 code가 있다면, 중복이 발생하게 된다.
    - 또, 만일 이 공통으로 들어가는 code가 변경된다면, interface를 구현한 모든 class를 찾아 일일이 바꿔줘야 한다.



- 모든 디자인 패턴의 기반이 되는 원리
  - 소프트웨어 개발에서 절대 바뀌지 않는 진리는 모든 소프트웨어는 바뀔 수 있다는 것이다.
  - 기반 원리
    - **상대적으로 변경이 일어날 것 같은 코드를 찾아 나머지 코드에 영향을 주지 않도록 캡슐화하여 바뀌지 않는 부분에 영향을 주지 않도록 따로 분리해야한다.**
    - 즉 바뀌는 부분은 따로 뽑아서 캡슐화하여, 나중에 바뀌지 않는 부분에 영향을 미치지 않고 그 부분만 고치거나 확장할 수 있도록 해야한다.



- Duck class에 적용하기

  - 변화하는 부분과 그대로 있는 부분을 분리하기
    - 변화하는 부분인 나는 행동과 꽥꽥 거리는 행동을 캡슐화하기 위해 모두 class로 만든다.
    - class들을 두 개의 집합으로 구분한다.
    - 하나는 나는 것과 관련된 부분, 다른 하나는 꽥꽥거리는 것과 관련된 부분이다.
    - 각 class 집합에는 각 행동을 구현한 것을 전부 집어넣는다.
    - 예를 들어 빽빽 거리는 행동을 구현하는 class를 만들고, 삑삑 거리는 행동을 구현하는 class를 만들고, 아무 것도 하지 않는 class를 만들어 꽥꽥거리는 것과 관련된 class 집합에 넣는다.
  - Class 집합을 디자인하기
    - 위에서 모든 문제의 원인이 오리의 행동과 관련된 유연성 때문이었으므로, 최대한 유연하게 만드는 것을 목표로한다.
    - 또한 Duck의 instance에 행동을 할당 할 수 있게 할 것이다.
    - 예를 들어 MallardDuck의 instance를 생성한 뒤에 특정 형식의 나는 행동으로 초기화하는 방식을 사용할 수 있을 것이다.
    - 또한 오리의 행동을 동적으로 바꾸는 것도 가능하도록 하기 위해서 Duck class에 행동과 관련된 setter 메서드를 추가해, 프로그램 실행 중에도 MallardDuck의 행동을 바꿀 수 있도록 한다.
  - **구현보다는 인터페이스에 맞춰서 프로그래밍한다.**
    - 각 행동은 인터페이스로 표현하고 이들 인터페이스를 사용해서 행동을 구현한다.
    - 나는 행동과 꽥꽥거리는 행동은 이제 Duck 클래스에서 구현하지 않는다.
    - 대신 특정 행동(삑삑 소래 내기)만을 목적으로 하는 클래스의 집합을 만든다.
    - 행동 인터페이스는 Duck 클래스가 아니라 행동 클래스에서 구현한다.
    - 예를 들어 `FlyBehavior`라는 interface를 만들고, 해당 interface를 구현하는 `FlyWithWings`, `FlyNoWay`라는 class를 만든 후, 각 class(`FlyWithWings`, `FlyNoWay`)에서 `fly` 메서드를 작성한다.

  - 인터페이스에 맞춰서 프로그래밍한다는 말은 상위 형식에 맞춰서 프로그래밍한다는 말이다.
    - 실제 실행 시에 쓰이는 객체가 코드에 고정되지 않도록 상위 형식(supertype)에 맞춰 프로그래밍해서 다형성을 활용해야한다는 의미이다.
    - 또 "상위 형식에 맞춰서 프로그래밍한다"는 원칙은 객체를 변수에 대입할 때 상위 형식을 구체적으로 구현한 형식이라면 어떤 객체든 넣을 수 있기 때문에, 변수를 선언할 때 보통 추상 클래스나 인터페이스 같은 상위 형식으로 선언해야한다는 의미이다. 이를 통해 변수를 선언하는 class에서 실제 객체의 형식을 몰라도 사용할 수 있게 된다.
  - 오리의 행동을 구현하기
    - `FlyBehavior`와 `QuackBehavior`라는 두 개의 인터페이스를 사용한다.

  ```python
  from abc import ABC, abstractmethod
  
  
  class FlyBehavior(ABC):
      @abstractmethod
      def fly(self):
          pass
  
  
  class FlyWithWings(FlyBehavior):
      def fly(self):
          # 나는 것과 관련된 행동
          
          
  class FlyNoWay(FlyBehavior):
      def fly(self):
          pass
  
  class QuackBehavior(ABC):
      @abstractmethod
      def quack(self):
          pass
      
      
  class Quack(QuackBehavior):
      def quack(self):
          # 꽥꽥 소리를 냄
      
      
  class Squeak(QuackBehavior):
      def quack(self):
          # 삑삑 소리를 냄
      
      
  class MuteQuack(QuackBehavior):
      def quack(self):
          # 아무 소리도 내지 않음
  ```



- 오리의 행동 통합하기

  - 가장 중요한 점은 나는 행동과 꽥꽥거리는 행동을 Duck class(혹은 그 sub class)에서 정의한 메서드를 써서 구현하지 않고 다른 클래스에 위임한다는 것이다.
  - 우선 Duck class에서 행동과 관련된 두 인터페이스의 인스턴스 변수를 추가한다.
    - 인터페이스의 인스턴스 변수를 설정하는 이유는 동적 타이핑을 지원하지 않는 언어들(대표적으로 Java)의 경우 인터페이스를 구현한 모든 class를 변수에 대입하기 위해서 해당 인터페이스를 type으로 설정해야 하기 때문이다.
    - 각 sub class 객체에서는 실행시에 이 변수에 특정 행동 형식(`FlyWithWings`, `MuteQuack` 등)의 레퍼런스를 다형적으로 설정한다.
  - `Duck` class에 `perform_fly()`와 `perform_quack()`이라는 메서드를 추가한다.
    - 나는 행동과 꽥꽥거리는 행동은 `FlyBehavior`와 `QuackBehavior` 인터페이스로 옮겨놨으므로, `Duck` class와 모든 subclass에서 `fly()`와 `quack()` 메서드를 제거한다.

  ```python
  class Duck:
      def __init__(self, ):
          self.fly_behavior = None
          self.quack_behavior = None
          
      def swim(self):
          # 수영하는 code
      
      @abstractmethod
      def display(self):
          pass
  
      def perform_fly(self):
          self.fly_behavior.fly()
      
      def perform_quack(self):
          self.quack_behavior.quack()
  ```

  - 실제 Duck 객체를 생성할 때, 행동 객체를 설정해준다.
    - 상속 받은 `perform_quack`, `perform_fly` 메서드를 실행할 때, 각기 실제 행동의 실행은 `Quack`, `FlyWithWings`에 위임된다.
    - 예시로 `MallardDuck`를 살펴보면 아래와 같다.

  ```python
  class MallardDuck(Duck):
      def __init__(self):
          self.fly_behavior = FlyWithWings()
          self.quack_behavior = Quack()
      
      def display(self):
          # display code
  ```

  - 참고
    - 특정 구현에 맞춰서 프로그래밍해선 안된다고 했지만, `MallardDuck` class를 보면 `self.fly_behavior = FlyWithWings()`과 같이 `FlyWithWings`라는구현되어 있는 구상 class의 인스턴스를 만들었다.
    - 이는 단순함을 위해 이렇게 한 것으로, 추후에 변경할 것이다.
    - 그러나 이 코드 역시 실행 시에 행동 class를 동적으로 변경하는 것이 가능하므로, 유연하기는 하다.



- 동적으로 행동 지정하기

  - Duck class에서 행동을 동적으로 지정하기 위한 method를 추가한다.

  ```python
  class Duck:
      # ...
      def set_fly_behavior(self, fb):
          self.fly_behavior = fb
      
      def set_quack_behavior(self, qb):
          self.quack_behavior = qb
  ```

  - 위에서 추가한 method를 사용해 behavior를 변경한다.

  ```python
  rubber_duck = RubberDuck()
  rubber_duck.set_fly_behavior(MuteQuack())
  ```



- 구성
  - 오리에는 `FlyBehavior`와 `QuackBehavior`가 있으며, 각각 나는 행동과 꽥꽥거리는 행동을 위임 받는다.
  - 이런 식으로 두 클래스를 합치는 것을 구성(composition)을 이용한다고 부른다.
    - 오리 class들은 행동을 상속받는 대신, 올바른 행동 객체로 구성되어 행동을 부여받는다.
    - 상속이 "A는 B다"로 표현된다면, 구성은 "A에는 B가 있다"로 표현된다.
  - **상속보다는 구성을 활용해야한다.**
    - 지금까지 봐 왔던 것 처럼, 구성을 활용해서 시스템을 만들면 유연성을 크게 향상시킬 수 있다.
    - 구성은 여러 디자인 패턴에서 사용된다.



- 지금까지 살펴본 디자인 패턴을 전략 패턴(Strategy pattern)이라 부른다.
  - 알고리즘군을 정의하고 캡슐화해서 각 알고리즘군을 수정해서 쓸 수 있게 해주는 패턴으로, 클라이언트로부터 알고리즘을 분리해서 독립적으로 변경할 수 있다.
  - 위 예시에서는 오리의 각 행동이 알고리즘군이라 할 수 있다.
    - 즉, `FlyBehavior`라는 알고리즘군과, `QuackBehavior`라는 알고리즘군이 있다.
  - 즉, "오리들의 다양한 행동을 전략 패턴으로 구현하고 있다"는 말은 아래와 같은 뜻이다.
    - 오리의 행동을 쉽게 확장하거나 변경할 수 있는 클래스들의 집합으로 캡슐화되어 있다.
    - 또한 필요시 실행중에도 확장과 변경이 가능하다.







# 디자인 원칙 모아보기

- 애플리케이션에서 달라지는 부분을 찾아내고, 달라지지 않는 부분과 분리한다.
- 구현보다는 인터페이스에 맞춰서 프로그래밍한다.
- 상속보다는 구성을 활용한다.

