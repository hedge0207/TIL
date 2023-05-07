# Compound pattern

- 복합 패턴
  - 여러 패턴을 함께 사용해서 다양한 디자인 문제을 해결하는 방법을 복합 패턴이라 부른다.
  - 패턴 몇 개를 결합한다고 해서 무조건 복합 패턴이 되는 것은 아니다.
    - 복합 패턴이라고 불리려면 여러 가지 문제의 일반적인 해결법을 제시해야 한다.



- 오리 시뮬레이션 게임에 다양한 패턴 적용하기

  - 오리 시뮬레이션 게임을 처음부터 다시 만들면서 몇 가지 기능을 추가 할 것이다.
  - Quackable 인터페이스와 이를 구현하는 구상 클래스를 만든다.

  ```python
  from abc import ABCMeta, abstractmethod
  
  
  class Quackable(metaclass=ABCMeta):
  
      @abstractmethod
      def quack(self):
          pass
  
  
  class MallardDuck(Quackable):
      def quack(self):
          print("Quack")
  
  
  class RedHeadDuck(Quackable):
      def quack(self):
          print("Quack")
  
  # 고무 오리는 일반 오리와 다른 소리를 낸다.
  class RubberDuck(Quackable):
      def quack(self):
          print("Squeak")
  
  # 사냥꾼이 사용하는 오리 호출기도 오리와 다른 소리를 낸다.
  class DuckCall(Quackable):
      def quack(self):
          print("Quck")
  ```

  - 오리 시뮬레이터 생성하기

  ```python
  class Simulator:
      def simulate(self):
          mallard_duck: Quackable = MallardDuck()
          red_head_duck: Quackable = RedHeadDuck()
          rubber_duck: Quackable = RubberDuck()
          duck_call: Quackable = DuckCall()
  
          self._simulate(mallard_duck)
          self._simulate(red_head_duck)
          self._simulate(rubber_duck)
          self._simulate(duck_call)
  
      # 다형성을 활용하여 어떤 Quackable이 전달되든 quack() 메서드를 호출할 수 있게 한다.
      def _simulate(self, duck: Quackable):
          duck.quack()
  
  
  simulator = Simulator()
  simulator.simulate()
  ```



- Adapter Pattern 적용하기

  - 거위 클래스 추가하기

  ```python
  class Goose:
      def honk(self):
          print("honk")
  ```

  - 거위용 adapter 생성하기

  ```python
  from quackable import Quackable
  from goose import Goose
  
  
  class GooseAdapter(Quackable):
      def __init__(self, goose: Goose):
          self.goose = goose
  
      
      def quack(self):
          self.goose.honk()
  ```

  - 시뮬레이터에 거위 추가하기

  ```python
  from goose import Goose
  from goose_adapter import GooseAdapter
  
  
  class Simulator:
      def simulate(self):
          # ... 기존 코드
          goose: Quackable = GooseAdapter(Goose())
  
          # ... 기존 코드
          self._simulate(goose)
  
      # 기존 코드
  ```



- Decorator Pattern 적용하기

  - 오리가 운 횟수를 세기 위해 decorator class를 생성한다.
    - 모든 오리 객체가 운 횟수를 구해야 하므로 `num_of_quack`은 class 변수로 생성한다.
    - `get_quacks()` 메서드는 class method로 선언한다.

  ```python
  from quackable import Quackable
  
  
  class QuackCounter(Quackable):
      num_of_quack = 0
  
      def __init__(self, duck: Quackable):
          self.duck = duck
  
      def quack(self):
          self.duck.quack()
          QuackCounter.num_of_quack += 1
  
      @classmethod
      def get_quacks(cls):
          return cls.num_of_quack
  ```

  - 모든 객체를 decorator로 감싸준다.
    - 오리가 운 횟수만 셀 것이므로 거위는 제외한다.

  ```python
  from quackable import Quackable, MallardDuck, RedHeadDuck, RubberDuck, DuckCall
  from goose import Goose
  from goose_adapter import GooseAdapter
  from quack_counter import QuackCounter
  
  
  class Simulator:
      def simulate(self):
          mallard_duck: Quackable = QuackCounter(MallardDuck())
          red_head_duck: Quackable = QuackCounter(RedHeadDuck())
          rubber_duck: Quackable = QuackCounter(RubberDuck())
          duck_call: Quackable = QuackCounter(DuckCall())
          goose: Quackable = GooseAdapter(Goose())	# 거위는 제외한다.
  
          # ...(기존 코드와 동일)
  
          print("number of quack: ", QuackCounter.get_quacks())
  
      # ...
  ```



- Abstract Factory Pattern 적용하기

  - 지금까지는 simualtor 안에서 각 오리 구상 class를 직접 생성했으나, 이 생성을 하나의 class에서 처리하고자 한다.
  - 이를 위해 추상 팩토리를 생성한다.

  ```python
  from abc import ABCMeta, abstractmethod
  
  from quackable import Quackable
  
  
  class AbstractDuckFactory(metaclass=ABCMeta):
      @abstractmethod
      def create_mallard_duck(self) -> Quackable:
          pass
  
      @abstractmethod
      def create_red_head_duck(self) -> Quackable:
          pass
  
      @abstractmethod
      def create_rubber_duck(self) -> Quackable:
          pass
  
      @abstractmethod
      def create_duck_call(self) -> Quackable:
          pass
  ```

  - 실제 사용할 factory class를 생성한다.
    - `AbstractDuckFactory`를 상속 받는다.

  ```python
  from quackable import Quackable, MallardDuck, RedHeadDuck, RubberDuck, DuckCall
  from quack_counter import QuackCounter
  
  
  class CountingDuckFactory(AbstractDuckFactory):
      def create_mallard_duck(self) -> Quackable:
          return QuackCounter(MallardDuck())
      
      def create_red_head_duck(self) -> Quackable:
          return QuackCounter(RedHeadDuck())
      
      def create_rubber_duck(self) -> Quackable:
          return QuackCounter(RubberDuck())
      
      def create_duck_call(self) -> Quackable:
          return QuackCounter(DuckCall())
  ```

  - 시뮬레이터를 수정한다.
    - `simulate()` 메서드는 이제 factory를 매개 변수로 받는다.

  ```python
  from quackable import Quackable, MallardDuck, RedHeadDuck, RubberDuck, DuckCall
  from goose import Goose
  from goose_adapter import GooseAdapter
  from quack_counter import QuackCounter
  from duck_factory import CountingDuckFactory
  
  
  class Simulator:
      def simulate(self, duck_factory):
          mallard_duck: Quackable = duck_factory.create_mallard_duck()
          red_head_duck: Quackable = duck_factory.create_red_head_duck()
          rubber_duck: Quackable = duck_factory.create_rubber_duck()
          duck_call: Quackable = duck_factory.create_duck_call()
          goose: Quackable = GooseAdapter(Goose())
  
          # ... 기존과 동일
  
      # ... 기존과 동일
  
  
  if __name__ == "__main__":
      simulator = Simulator()
      # factory를 생성하고
      duck_factory = CountingDuckFactory()
      # 인자로 넘긴다.
      simulator.simulate(duck_factory)
  ```



- Composite Pattern 적용하기

  - 지금까지는 오리를 개별적으로 관리했지만, 통합해서 관리하려 한다.
    - 이를 위해 객체들로 구성된 컬렉션을 개별 객체와 같은 방식으로 다룰 수 있게 해 주는 composite pattern을 적용한다.
    - Iterator Pattern도 추가로 적용한다.

  ```python
  from typing import List
  
  from quackable import Quackable
  
  
  class Flock(Quackable):
      # composite 객체와 leaf 원소에서 같은 인터페이스를 구현해야 한다.
      def __init__(self):
          self.quackers: List[Quackable] = []
  
      def add(self, qucker:Quackable):
          self.quackers.append(qucker)
      
      def quack(self):
          for quacker in self.quackers:
              quacker.quack()
  ```

  - 시뮬레이터를 수정한다.

  ```python
  from quackable import Quackable
  from goose import Goose
  from goose_adapter import GooseAdapter
  from quack_counter import QuackCounter
  from duck_factory import CountingDuckFactory
  from flock import Flock
  
  
  class Simulator:
      def simulate(self, duck_factory):
          red_head_duck: Quackable = duck_factory.create_red_head_duck()
          rubber_duck: Quackable = duck_factory.create_rubber_duck()
          duck_call: Quackable = duck_factory.create_duck_call()
          goose: Quackable = GooseAdapter(Goose())
  
          flock_of_ducks = Flock()
  
          flock_of_ducks.add(red_head_duck)        
          flock_of_ducks.add(rubber_duck)        
          flock_of_ducks.add(duck_call)        
          flock_of_ducks.add(goose)        
  
          flock_of_mallards = Flock()
  
          mallard_duck_one: Quackable = duck_factory.create_mallard_duck()
          mallard_duck_two: Quackable = duck_factory.create_mallard_duck()
          mallard_duck_three: Quackable = duck_factory.create_mallard_duck()
          mallard_duck_four: Quackable = duck_factory.create_mallard_duck()
          flock_of_mallards.add(mallard_duck_one)
          flock_of_mallards.add(mallard_duck_two)
          flock_of_mallards.add(mallard_duck_three)
          flock_of_mallards.add(mallard_duck_four)
          
          # flock_of_mallards을 flock_of_ducks에 추가한다.
          flock_of_ducks.add(flock_of_mallards)
  
          print("전체 오리 시뮬레이션")
          self._simulate(flock_of_ducks)
  
          print("물오리 시뮬레이션")
          self._simulate(flock_of_mallards)
  
          print("number of quack: ", QuackCounter.get_quacks())
  
      # 기존과 동일
  
  
  if __name__ == "__main__":
      simulator = Simulator()
      duck_factory = CountingDuckFactory()
      simulator.simulate(duck_factory)
  ```



- Observer Pattern 적용하기

  - 오리가 꽥꽥 소리를 낼 때마다 추적하는 기능을 넣고자 한다.
  - Observer를 위한 인터페이스 생성하기
    - 옵저버를 삭제하는 기능은 편의상 생략한다.
    - `Observer` interface는 추후에 정의한다.

  ```python
  from abc import ABCMeta, abstractmethod
  
  
  class QuackObervable(metaclass=ABCMeta):
      @abstractmethod
      def register_observer(self, observer: Observer):
          pass
  
      @ abstractmethod
      def notify_observer(self):
          pass
  ```

  - Quackable이 Obserer를 구현하도록 수정하기

  ```python
  from abc import abstractmethod
  
  from quack_observer import QuackObervable
  
  class Quackable(QuackObervable):
  
      @abstractmethod
      def quack(self):
          pass
  ```

  - Quackable을 구현하는 모든 구상 클래스에서 QuackObservable에 있는 메서드를 구현하도록 한다.
    - 등록 및 연락용 코드를 Observable 클래스에 캡슐화하고, 구성으로 QuackObservable에 포함시킨다.
    - 이를 통해 실제 코드는 한 군데만 작성하고, QuackObservalbe이 필요한 적업을 Observable 보조 클래스에 전부 위임하게 만들 수 있다.

  ```py
  class Observable(QuackObervable):
      def __init__(self, duck):
          self.observers: List[Observer] = []
          self.duck = duck
      
      def register(self, observer: Observer):
          self.observers.append(observer)
      
      def notify_observer(self):
          for observer in self.observers:
              observer.update(self.duck)
  ```

  - Observer 보조 객체를 모든 Quackable class에 넘겨준다.
    - 예시로 MallardDuck에만 추가하지만 모든 Quackable class(`Goose`, `QuackCOunter` 등)에 추가해야한다.

  ```python
  from quackable import Quackable
  from observer import Observable
  
  
  class MallardDuck(Quackable):
      def __init__(self):
          self.observable = Observable(self)
      
      def quack(self):
          print("Quack")
          # quack이 호출되면 Observer에게 신호를 보낸다.
          self.notify_observer()
  
      def register_observer(self, observer: Observer):
          self.observable.register_observer(observer)
      
      def notify_observer(self):
          self.observable.notify_observer()
  ```

  - `QuackCounter`를 아래와 같이 수정한다.

  ```python
  class QuackCounter(Quackable):
      # .. 기존 코드와 동일
      
      def register_observer(self, observer: Observer):
          self.duck.register_observer(observer)
      
      def notify_observer(self):
          self.duck.notify_observer()
  ```

  - `Flock`은 아래와 같이 변경한다.
    - 옵저버에 등록할 때 오리 무리 안에 있는 모든 Quakable 객체들을 일일이 옵저버에 등록해줘야한다.
    - Quackable 객체에서 알아서 옵저버에게 연락을 돌리므로 Flock은 아무 일도 하지 않아도 된다(Flock에서 개별 Quackable 객체의 `quack()` 메서드를 호출하면 자동으로 처리된다).

  ```python
  from typing import List
  
  from quackable import Quackable
  from observer import Observer
  
  
  class Flock(Quackable):
      def __init__(self):
          self.quackers: List[Quackable] = []
  
      def add(self, qucker:Quackable):
          self.quackers.append(qucker)
      
      def quack(self):
          for quacker in self.quackers:
              quacker.quack()
      
      def register_observer(self, observer: Observer):
          # quackers를 순회하면서 일일이 등록한다.
          # 만일 quacker가 또 다른 Flock 객체라면 재귀적으로 호출이 반복된다.
          for quacker in self.quackers:
              quacker.register_observer(observer)
      
      def notify_observer(self):
          pass
  ```

  - Observer class 만들기

  ```python
  class Observer(metaclass=ABCMeta):
      def update(self, duck: QuackObervable):
          pass
  
  
  class QuackLogist(Observer):
      def update(self, duck: QuackObervable):
          print("{}가 방금 소리 냈다.".format(duck.__class__.__name__))
  ```

  - 시뮬레이터 수정하기

  ```python
  from quackable import Quackable
  from goose import Goose
  from goose_adapter import GooseAdapter
  from quack_counter import QuackCounter
  from duck_factory import CountingDuckFactory
  from flock import Flock
  from observer import QuackLogist
  
  
  class Simulator:
      def simulate(self, duck_factory):
          # 기존 코드와 동일
  
          quack_logist = QuackLogist()
          flock_of_ducks.register_observer(quack_logist)
          self._simulate(flock_of_ducks)
  
          print("number of quack: ", QuackCounter.get_quacks())
  
      # 다형성을 활용하여 어떤 Quackable이 전달되든 quack() 메서드를 호출할 수 있게 한다.
      def _simulate(self, duck: Quackable):
          duck.quack()
  
  
  if __name__ == "__main__":
      simulator = Simulator()
      duck_factory = CountingDuckFactory()
      simulator.simulate(duck_factory)
  ```



## Model-View-Controller Pattern

- MVC Pattern
  - Model
    - 모든 데이터, 상태와 애플리케이션 로직이 들어있다.
    - 뷰와 컨트롤러에서 모델의 상태를 조작하거나 가져올 때 필요한 인터페이스를 제공하고, 모델이 자신의 상태 변화를 옵저버들에게 연락해주지만, 기본적으로 모델은 뷰와 컨트롤러에 별 관심이 없다.
  - View
    - 모델을 표현하는 방법을 제공한다.
    - 일반적으로 화면에 표시할 때 필요한 상태와 데이터는 모델에서 직접 가져온다.
    - 다만, 꼭 모델에게 요청해서 가져올 필요는 없고, 모델이 갱신 될 때, view도 함께 갱신시키는 방식을 사용해도 된다.
  - Controller
    - 사용자로부터 입력을 받는다.
    - 입력받은 내용이 모델에게 어떤 의미가 있는지 파악한다.
    - 컨트롤러에는 비즈니스 로직을 작성하지 않는다.



- 동작 과정

  - 사용자가 뷰에 접촉한다.
    - 사용자는 뷰에만 접촉할 수 있다.
    - 사용자가 뷰에서 뭔가를 하면 뷰는 무슨 일이 일어났는지 컨트롤러에게 알려준다.
    - 컨트롤러가 상황에 맞게 작업을 처리한다.

  - 컨트롤러가 모델에게 상태를 변경하라고 요청한다.
    - 컨트롤러는 사용자의 행동을 받아서 해석한다.
    - 사용자가 버튼을 클릭하면 컨트롤러는 그것이 무엇을 의미하는지 해석하고, 모델을 어떤 식으로 조작해야 하는지 결정한다.
  - 컨트롤러가 뷰를 변경해 달라고 요청할 수도 있다.
    - 컨트롤러는 뷰로부터 어떤 행동을 받았을 때, 그 행동의 결과로 뷰에게 뭔가를 바꿔 달라고 할 수도 있다.
    - 예를 들어 컨트롤러는 화면에 있는 어떤 버튼이나 메뉴를 활성화하거나 비활성화 할 수 있다.
  - 상태가 변경되면 모델이 뷰에게 그 사실을 알린다.
    - 사용자가 한 행동이나 내부적인 변화 등으로 모델에서 변경이 생길경우 모델은 뷰에게 상태가 변경되었다고 알린다.
  - 뷰가 모델에게 상태를 요청한다.
    - 뷰는 화면에 표시할 상태를 모델로부터 직접 가져온다.
    - 컨트롤러가 뷰에게 뭔가를 바꾸라고 요청할 때, 뷰는 모델에게 상태를 알려달라고 요청할 수도 있다.



- MVC에 사용되는 패턴들
  - Observer Pattern
    - 모델은 옵저버 패턴을 사용하여 상태가 바뀔 때 마다 뷰와 컨트롤러에게 연락한다.
    - 옵저버 패턴을 사용함으로써 모델을 뷰와 컨트롤러로부터 완전히 독립시킬 수 있다.
    - 한 모델에서 서로 다른 뷰를 사용할 수도 있고, 여러 개의 뷰를 동시에 사용할 수도 있게 된다.
  - Strategy Pattern
    - 뷰와 컨트롤러는 전략 패턴을 사용하여 부 객체를 여러 전략을 사용하여 설정할 수 있다.
    - 컨트롤러가 전략을 제공하고, 뷰는 애플리케이션의 겉모습에만 신경 쓰고, 인터페이스의 행동을 결정하는 일은 모두 컨트롤러에게 맡긴다.
    - 사용자가 요청한 내역을 처리하려고 모델과 얘기하는 일을 컨트롤러가 맡고 있으므로, 전략 패턴을 사용함으로써 뷰를 모델로부터 분리할 수 있다.
  - Composite Pattern
    - 뷰는 컴포지트 패턴을 사용하여 여러 단계로 겹쳐 있는 화면을 표현한다.
    - 컨트롤러가 뷰에게 화면을 갱신해달라고 요청하면 최상위 뷰 구성 요소에게만 화면을 갱신하라고 얘기하면 된다.
    - 나머지는 컴포지트 패턴이 알아서 처리해준다.



- MVC 패턴 적용해보기

  > Streamlit을 사용하여 타이머를 만드려고 했으나 변경 사항이 생길 때 마다 렌더링이 이루어지는 streamlit 특성 상 MVC 패턴 적용이 불가능하다.
  >
  > 추후 PyQt5를 사용하여 다시 해볼 것





# 다양한 디자인 패턴들

- 디자인 패턴의 정의
  - 특정 컨텍스트 내에서 주어진 문제의 해결책을 패턴이라 부른다.
    - 컨텍스트란 패턴이 적용되어야 하는 상황을 의미하며, 반복적으로 일어날 수 있는 상황이어야 한다.
    - 문제란 컨텍스트 내에서 이뤄야하는 목표를 의미한다.
    - 해결책은 제약조건 속에서 누가 적용해도 목표를 이룰 수 있는 일반적인 디자인을 의미한다.
  - 특정 디자인이 컨텍스트 내에서 주어진 문제를 해결하는 해결책이라 하더라도, 해당 컨텍스트가 반복적으로 발생하지 않는다면, 패턴이라 부를 수 없다.



- 디자인 패턴 분류

  > 모든 디자인 패턴들이 각 범주에 딱 떨어지게 분류되는 것은 아니다.
  >
  > 관점에 따라, 상황에 따라 다른 범주에 속할 수도 있다.

  - 생성(Creational) 패턴
    - 객체 인스턴스를 생성하는 패턴이다.
    - 클라이언트와 클라이언트가 생성해야 하는 객체 인스턴스 사이의 연결을 끊어준다.
    - 싱글톤, 팩토리 패턴 등이 이에 속한다.
  - 행동(Behavioral) 패턴
    - 클래스와 객체들이 상호작용하는 방법과 역할을 분담하는 방법을 다루는 패턴이다.
    - 옵저버, 상태, 전략 패턴등이 이에 속한다.
  - 구조(Structural)
    - 클래스와 객체를 더 큰 구조로 만들 수 있게 구상을 사용하는 패턴이다.
    - 어댑터, 데코레이터, 컴포지트 패턴 등이 이에 속한다.
  - 혹은 클래스를 다루는 패턴인지, 객체를 다루는 패턴인지에 따라 구분하기도 한다.
    - 클래스 패턴은 클래스 사이의 관계가 상속으로 어떻게 정의되는지를 다루는 패턴들로, 어댑터, 템플릿 메서드 등이 이에 속한다.
    - 객체 패턴은 객체 사이의 관계를 다루며, 객체 사이의 관계는 일반적으로 구성으로 정의 되는 패턴들로, 대부분의 패턴이 이에 속한다.



- 브리지 패턴
  - 



