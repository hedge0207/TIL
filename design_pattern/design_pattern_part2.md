# Factory Pattern

- 최첨단 피자 코드 만들기

  - 피자 생성 코드
    - 여기서의 `Pizza`는 인터페이스가 아닌 구상 클래스이다.

  ```python
  # 구상 클래스
  class Pizza:
      ...
  
  def order_pizza():
      pizza = Pizza()
      
      pizza.prepare()
      pizza.bake()
      pizza.cut()
      pizza.box()
      return pizza
  ```
  
  - Pizza의 종류가 하나만 있는 것은 아니므로, 피자의 종류마다 다른 처리를 해줘야 한다.
    - `type_` parameter로 피자의 종류를 받는다.
    - 이제 `Pizza`를 추상 클래스를 생성하고, 이를 구현하는 `CheesePizza`등의 여러 구상 클래스를 생성한다.
    - `type_`을 바탕으로 어떤 구상 클래스의 인스턴스를 생성할지를 결정한다.
  
  ```python
  from abc import ABC
  
  # 추상 클래스
  class Pizza(ABC):
      ...
  
  # 구상 클래스들
  class CheesePizza(Pizza):
      ...
  
  class GreekPizza(Pizza):
      ...
  
  class PepperoniPizza(Pizza):
      ...
  
  def order_pizza(type_):
      pizza = None
      if type_ == "cheese":
          pizza = CheesePizza()
      elif type_ == "greek":
          pizza = GreekPizza()
      elif type_ == "Pepperoni":
          pizza = PepperoniPizza()
      
      pizza.prepare()
      pizza.bake()
      pizza.cut()
      pizza.box()
      return pizza
  ```
  
  - 신메뉴를 추가해야 한다.
    - `GreekPizza`를 제외하고 `VeggiePizza`와 `ClamPizza`가 추가되어야 한다.
  
  ```py
  def order_pizza(type_):
      if type_ == "cheese":
          pizza = CheesePizza()
      # elif type_ == "greek":
      #     pizza = GreekPizza()
      elif type_ == "pepperoni":
          pizza = PepperoniPizza()
      elif type_ == "veggie":
          pizza = VeggiePizza()
      elif type_ == "clam":
          pizza = ClamPizza()
      
      pizza.prepare()
      pizza.bake()
      pizza.cut()
      pizza.box()
      return pizza
  ```
  
  - 문제점
    - `type_`을 가지고 분기를 줘서 인스턴스를 생성할 구상 클래스를 바꾸는 부분은 변화에 닫혀 있지 않다.
    - 피자가 추가, 삭제 될 때 마다 지속적으로 변경이 필요하다.
    - 또한 "구현에 의존하지 말고 인터페이스에 의존해야한다"는 디자인 원칙에 위반된다.
  
  - 바뀌는 부분(`type_`을 가지고 인스턴스를 생성할 구상 클래스를 분기하는 부분)을 확인했으니, 캡슐화를 할 차례다.
    - 즉, 이 코드의 경우 인스턴스를 생성하는 부분을 캡슐화해야 한다.



- 팩토리(Factory)

  - 객체 생성을 처리하는 클래스를 팩토리라 부른다.
    - 클라이언트로부터 요청을 받아 새로운 객체를 생성하고 반환하는 역할을 한다.
    - 위 예시를 기반으로 설명하면 다음과 같다.
    - Factory를 생성하고, 클라이언트인 `order_pizza()` 메서드가 실행될 때 마다 `Pizza` 인터페이스를 구현한 구상 클래스를 생성하고, 이를 반환해준다.
    - 클라이언트인 `order_pizza()`는 factory로부터 구상 클래스를 전달받아 `Pizza` 인터페이스에 구현된 `prepare()`, `bake()` 등의 메서드만 실행시킨다.
  - 결국 문제를 다른 객체에 떠넘기는 것 아닌가?
    - 위 예시에서는 `order_pizza()`만 살펴봤지만, `show_ingredients()` 등 pizza 인스턴스가 필요한 수 많은 클라이언트가 있을 수 있다.
    - 만일 객체의 생서을 factory 한 곳에 위임해서 처리하지 않고 각 클라이언트가 객체의 생성을 관리한다면, 수정사항이 있을 때 마다 모든 클라이언트 코드를 다 변경해줘야한다.
    - 아래 예시에서 `Pizza`의 종류가 추가되거나 삭제되면 두 개의 클라이언트 코드를 모두 수정해야한다.

  ````python
  def order_pizza(type_):
      if type_ == "cheese":
          pizza = CheesePizza()
      elif type_ == "pepperoni":
          pizza = PepperoniPizza()
      elif type_ == "veggie":
          pizza = VeggiePizza()
      elif type_ == "clam":
          pizza = ClamPizza()
      
      pizza.prepare()
      pizza.bake()
      pizza.cut()
      pizza.box()
      return pizza
  
  def show_ingredients(type_):
      if type_ == "cheese":
          pizza = CheesePizza()
      elif type_ == "pepperoni":
          pizza = PepperoniPizza()
      elif type_ == "veggie":
          pizza = VeggiePizza()
      elif type_ == "clam":
          pizza = ClamPizza()
      
      print(pizza.dough)
      print(pizza.cheeze)
  ````



- Factory 적용하기

  - 객체 생성 팩토리 만들기

  ```python
  class SimplePizzaFactory:
      
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = CheesePizza()
          elif type_ == "pepperoni":
              pizza = PepperoniPizza()
          elif type_ == "veggie":
              pizza = VeggiePizza()
          elif type_ == "clam":
              pizza = ClamPizza()
          return pizza
  ```

  - 클라이언트 코드 수정하기

  ```python
  class PizzaStore:
      
      def __init__(self, factory):
          factory = factory
      
      # client code
      def order_pizza(self, type_):
          pizza = factory.create_pizza(type_)
          
          pizza.prepare()
          pizza.bake()
          pizza.cut()
          pizza.box()
          return pizza
      
  pizza_store = PizzaStore(SimplePizzaFactory())
  pizza = pizza_store.order_pizza()
  ```

  - 이점
    - `order_pizza()`는 더 이상 구상 클래스에 의존하지 않는다.
    - 새로운 피자의 추가, 삭제가 일어날 때에도 모든 클라이언트의 코드를 변경하는 것이 아니라 factory의 코드만 변경하면 된다.

  - Simple factory란 디자인 패턴이라기 보다는 프로그래밍에서 자주 쓰이는 관용구에 가깝다.
    - 워낙 자주 쓰이다 보니 simple factory를 factory pattern이라 부르는 사람들도 있다.
    - 그럼에도 simple factory는 정확히는 패턴은 아니다.
  - Static factory란
    - 정적 메서드를 사용하여 객체를 생성하는 factory를 의미한다.
    - Java에서 static 메서드는 해당 메서드가 포함된 클래스의 인스턴스를 생성하지 않아도 실행시킬 수 있는 메서드를 의미한다.
    - 정적 메서드를 사용하는 이유는 객체 생성을 위해 factory 클래스의 인스턴스를 만들지 않아도 돼서 보다 간편하게 객체를 생성할 수 있기 때문이다.
    - 다만, 서브클래스를 만들어 객체를 생성하는 메서드의 행동을 변경할 수 없다는 단점이 있다.

  ```python
  class StaticPizzaFactory:
      
      @staticmethod
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = CheesePizza()
          elif type_ == "pepperoni":
              pizza = PepperoniPizza()
          elif type_ == "veggie":
              pizza = VeggiePizza()
          elif type_ == "clam":
              pizza = ClamPizza()
          return pizza
  
  
  class PizzaStore:
      
      def order_pizza(self, type_):
          pizza = StaticPizzaFactory.create_pizza(type_)
          
          pizza.prepare()
          pizza.bake()
          pizza.cut()
          pizza.box()
          return pizza
      
  pizza_store = PizzaStore()
  pizza = pizza_store.order_pizza()
  ```



- 다양한 팩토리 만들기

  - 피자 가게가 성장하면서 각 지역마다 지점을 내기로 했다.
    - 각 지역의 특성을 반영한 다양한 스타일의 피자를 출시하려 한다.
  - 각 피자 스타일별로 factory를 하나씩 생성하기로 한다.
    - 본사에서는 각 지역 스타일에 맞는 피자를 생성해주는 factory만 구현해준다.
    - 그리고 모든 지점에서 동일한 과정을 거쳐 피자를 만들게 하기 위해서 `PizzaStore`를 참고하여 각 지점마다 `PizzaStore` 클래스를 만들도록했다.  
  
  ```python
  class NYPizzaFactory:
      
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = NYStyleCheesePizza()
          elif type_ == "pepperoni":
              pizza = NYStylePepperoniPizza()
          elif type_ == "veggie":
              pizza = NYStyleVeggiePizza()
          elif type_ == "clam":
              pizza = NYStyleClamPizza()
          return pizza
  
  class ChicagoPizzaFactory:
      
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = ChicagoStyleCheesePizza()
          elif type_ == "pepperoni":
              pizza = ChicagoStylePepperoniPizza()
          elif type_ == "veggie":
              pizza = ChicagoStyleVeggiePizza()
          elif type_ == "clam":
              pizza = ChicagoStyleClamPizza()
          return pizza
  
  
  ny_store = NYPizzaStore(NYPizzaFactory())
  pizza = ny_store.order_pizza()
  
  chicago_store = ChicagoPizzaStore(ChicagoPizzaFactory())
  pizza = chicago_store.order_pizza()
  ```
  
  - 위 방식의 문제
    - 각 지점마다 Pizza를 생성하는 팩토리를 제대로 쓰긴 하는데, 정작 그 factory가 생성하는 instance로 피자를 생성하는 로직이 담긴 `PizzaStore`를 지점마다 구현하다보니 지점 사이에 차이가 생기게 된다.
    - 즉 지점마다 다른 조리법, 다른 포장 상자 등을 사용하기 시작한다.
    - 이는 `PizzaStore`와 pizza factory가 서로 분리되어 있기 때문에 발생하는 것이다.
    - 따라서 유연성을 잃지 않으면서 이 둘을 하나로 묶어줄 방법이 필요하다.
  
  -  `create_pizza` 코드를 factory가 아닌 `PizzaStore` 클래스로 다시 넣는다.
    - 다만, 단순히 넣기만 하는 것이 아니라, 이를 추상 메서드로 선언하고, `PizzaStore`도 추상 클래스로 변경한다.
    - 아래와 같이 하위 클래스에 객체 생성을 위임하도록 하는 메서드를 팩토리 메서드라 한다.
  
  ```python
  from abc import *
  
  
  class PizzaStore(metaclass=ABCMeta):
      
      def order_pizza(self, type_):
          pizza = self.create_pizza(type_)
          
          pizza.prepare()
          pizza.bake()
          pizza.cut()
          pizza.box()
          
          return pizza
      
      @abstractmethod
      def create_pizza(self, type_):
          pass
  ```
  
  - 각 스타일별 서브 클래스를 생성한다.
    - `create_pizza()` 메서드는 추상 메서드로 선언했으므로, 서브 클래스들은 반드시 이 메서드를 구현해야한다. 
  
  ```python
  class NYStylePizzaStore(PizzaStore):
      
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = NYStyleCheesePizza()
          elif type_ == "pepperoni":
              pizza = NYStylePepperoniPizza()
          elif type_ == "veggie":
              pizza = NYStyleVeggiePizza()
          elif type_ == "clam":
              pizza = NYStyleClamPizza()
          return pizza
  
  
  class ChicagotylePizzaStore(PizzaStore):
      
      def create_pizza(type_):
          pizza = None
          if type_ == "cheese":
              pizza = ChicagoStyleCheesePizza()
          elif type_ == "pepperoni":
              pizza = ChicagoStylePepperoniPizza()
          elif type_ == "veggie":
              pizza = ChicagoStyleVeggiePizza()
          elif type_ == "clam":
              pizza = ChicagoStyleClamPizza()
          return pizza
  ```
  
  - 이제 피자의 종류는 어떤 서브클래스를 선택했느냐에 따라 결정된다.
    - `PizzaStore.order_pizza()`메서드에서는 `Pizza` 객체를 가지고 피자를 준비하고, 굽고, 자르고, 포장하는 작업을 하지만, `Pizza`는 추상 클래스이므로 `PizzaStore.order_pizza()` 메서드는 실제로 어떤 `Pizza` 구상 클래스에서 작업이 처리되고 있는지 전혀 알 수 없다.
    - 즉, `PizzaStore`와 `Pizza`는 완전히 분리되어 있다.
    - `order_pizza()`에서 `create_pizza()`를 호출하면 `Pizza`의 서브클래스의 인스턴스가 생성된다.
    - 즉 `NYStylePizzaStore`에서 `order_pizza()`가 호출되면 `create_pizza()`메서드는 뉴욕 스타일 피자 인스턴스를 생성하고, `ChicagoStylePizzaStore`에서 `order_pizza()`가 호출되면 `create_pizza()`메서드는 시카고 스타일 피자 인스턴스르 생성한다.
    - 결국 서브 클래스에서 피자의 종류를 실시간으로 결정하는 것이 아니라, 어떤 서브클래스를 선택했느냐에 따라 피자의 종류가 결정되게 된다.
    - 결국 구상 클래스 인스턴스를 생성하는 일은 하나의 객체(simple factory)가 전부 처리하는 방식에서 일련의 서브 클래스가 처리하는 방식으로 바뀌었다.
    
  - Pizza class 만들기
    - 마지막으로 Pizza class와 그 서브 클래스를 만든다.
  
  ```python
  from abc import *
  
  
  class Pizza(metaclass=ABCMeta):
      def __init__(self):
          self.name = None
          self.dough = None
          self.sauce = None
          self.toppings = []
  
      def prepare(self):
          print("{} 피자 준비 중".format(self.name))
          print("도우를 돌리는 중")
          print("소스를 뿌리는 중")
          print("토핑을 올리는 중")
          for topping in self.toppings:
              print(topping)
  
      def bake(self):
          print("175도에서 25분 굽기")
  
      def cut(self):
          print("8등분으로 자르기")
  
      def box(self):
          print("상자에 피자 담기")
          
      def get_name(self, name):
          self.name = name
  
      def get_name(self):
          return self.name
  ```
  
  - Pizza의 구상 서브 클래스 만들기
  
  ```python
  class NYStyleCheesePizza(Pizza):
      def __init__(self):
          self.name = "뉴욕 스타일 소스와 치즈 피자"
          self.dough = "얇은 크러스트 도우"
          self.sauce = "마리나라 소스"
          self.toppings = ["잘게 썬 레지아노 치즈"]
      
      
  class ChicagoStyleCheesePizza(Pizza):
      def __init__(self):
          self.name = "시카고 스타일 딥 디쉬 치즈 피자"
          self.dough = "두꺼운 크러스트 도우"
          self.sauce = "플럼 토마토 소스"
          self.toppings = ["모짜렐라 치즈"]
      
      def cut(self):
          print("네모난 모양으로 자르기")
  ```



- Factory method 패턴
  
  - 지금까지 살펴본 패턴이 팩토리 메서드 패턴이다.
    - 모든 팩터리 패턴은 객체 생성을 캡슐화한다.
    - 팩토리 메서드 패턴은 서브클래스에서 어떤 클래스를 만들지를 결정함으로써 객체 생성을 캡슐화한다.
  
  - 정의
    - 객체를 생성할 때 필요한 인터페이스를 만들고, 어떤 클래스의 인스턴스를 만들지는 서브클래스에서 결정하는 패턴이다.
    - 더 정확히 말하면 서브 클래스에서 결정되는 것이 아니라, 사용하는 서브클래스에 따라 생산되는 객체 인스턴스가 결정된다.
  
  ![image-20230326135018688](design_pattern_part2.assets/image-20230326135018688.png)
  
  - Creator 추상 클래스
    - 객체를 만드는 메서드(위 UML에서는 `factory_method()`, 피자 예시에서는 `create_pizza()`), 즉 팩토리 매소드용 인터페이스를 제공한다.
    - 팩토리 메소드에 의해 생성된 구상 클래스의 인스턴스(예시의 경우 `ConcreteProduct`의 인스턴스, 피자 예시에서는 `NYStyleCheesePizza` 등)로 필요한 작업을 처리한다.
    - 그러나 실제 팩토리 메서드를 구현하고 구상 클래스의 인스턴스를 생성하는 일은 서브클래스에서만 할 수 있다.
  - 구상 생산자 클래스가 하나 뿐이라도 팩토리 메서드 패턴을 사용하는 것이 의미가 있는지?
    - `ConcreteCreator`가 하나 뿐이더라도 팩토리 메서드 패턴은 유용하다.
    - 다른 `ConcreteCreator`가 추가되거나 변경되더라도, `Creator` 클래스가 `ConcreteProduct`와 느슨하게 결합되어 있으므로 `Creator`는 건드릴 필요가 없다.
  - `Creator` 클래스의 `factory_method()`는 꼭 추상 메서드로 선언해야 하는지, 혹은 `Creator` 클래스는 꼭 추상 클래스여야 하는지?
    - 꼭 그럴 필요는 없다.
    - 몇몇 간단한 `ConcreteProduct` 생성을 위해 일반 메서드로 정의해서 `ConcreteCreator`를 설정하지 않았을 때 실행될 기본 팩토리 메서드로 사용해도 된다.
    - 즉, 위 예시에서는 `factory_method()`가 추상 메서드이므로 서브 클래스에서 반드시 구현을 해야 한다.
    - 반면에 일반 메서드로 구현하면, 서브 클래스에서 반드시 구현을 하지 않아도 되고, 구현하지 않았을 경우(오버라이딩 하지 않았을 경우) `Creator`에 정의된 `factory_method()`가 실행된다.
    - 즉, `Creator` 클래스에서 `factory_method()`를 추상 메서드로 선언하지 않으면, 이를 기본 팩토리 메서드로 사용할 수 있다.
  - Simple Factory와의 차이
    - 팩토리 메서드 패턴은 얼핏 보기에는 simple factory와 거의 유사해보인다.
    - 그러나 팩토리 메서드 패턴은 simple factory와는 달리 생성할 `ConcreteProduct`를 보다 유연하게 변경할 수 있다.



- 의존성 역전 원칙(Dependency Inversion Principle)

  - 객체 인스턴스를 직접 만들면 구상 클래스에 의존해야한다.
    - 예를 들어 아래와 같이 초기의 `PizzaStore`코드의 경우 Pizza 구상 클래스가 변경되면 `PizzaStore`까지도 변경되어야한다.
    - 따라서 `PizzaStore`는 피자 클래스(`CheesePizza`, `GreekPizza` 등)에 의존한다고 할 수 있다.

  ```python
  class PizzaStore:
      def order_pizza(self, type_):
          pizza = None
          if type_ == "cheese":
              pizza = CheesePizza()
          elif type_ == "greek":
              pizza = GreekPizza()
          elif type_ == "Pepperoni":
              pizza = PepperoniPizza()
  ```

  - 의존성 역전 원칙이란 "구상 클래스에 의존하지 않게 하고 추상화된 것에 의존하게 한다"는 원칙이다.
    - "구현보다는 인터페이스에 맞춰 프로그래밍한다"는 원칙과 유사하지만, 이 원칙이 추상화를 더욱 강조한다.
    - 고수준 구성 요소가 저수준 구성 요소에 의존하면 안 되며, 항상 추상화에 의존하게 만들어야 한다는 뜻이 담겨 있다.
    - 고수준 구성 요소란 다른 저수준 구성 요소에 의해 정의되는 행동들이 들어있는 구성 요소를 뜻한다.
    - 예를 들어 `PizzaStore`의 행동은 피자에 정의된 `bake()`, `cut()` 등을 사용하므로 `PizzaStore`는 고수준 구성 요소라고 할 수 있다.
  - 의존성 역전 원칙 적용하기
    - 위에서 살펴본 `PizzaStore`의 가장 큰 문제는 `PizzaStore`가 모든 종류의 피자에 의존한다는 점이다.
    - 이는 `order_pizza()` 메서드에서 구상 형식의 인스턴스를 직접 만들기 때문이다.
    - `Pizza`라는 추상 클래스를 만들긴 했지만, 구상 피자 객체를 생성하는 것은 아니기에, `Pizza`를 추상 클래스로 만들어 얻는 것이 별로 없다.
    - 따라서 `order_pizza()`에서 피자를 만드는 부분을 팩토리 메서드 패턴으로 뽑아내면, `PizzaStore` 추상 클래스는 오직 `Pizza`라는 추상 클래스에만 의존하게 된다(꼭 팩토리 메서드를 사용해야지 의존성을 역전시킬 수 있는 것은 아니다).
    - 이렇게 되면 고수준 구성 요소인 `PizzaStore`가 저수준 구성 요소인 구상 피자 클래스가 아닌 추상 클래스인 `Pizza`에 의존하게 된다.
  - 왜 "역전(inversion)"이라는 단어를 사용하는 것인가
    - 객체 지향 디자인을 할 때 일반적으로 생각하는 방법과는 반대로 뒤집어서 생각해야 하기에 역전이라는 단어를 사용한다.
    - 일반적으로 디자인할 때는 `PizzaStore → [CheesPizza, GreekPizza, PeperoniPizza]`와 같은 의존관계가 형성된다.
    - 반면에 의존성 역전 원칙을 적용한 뒤의 의존성은 다음과 같다.
    - `PizzaStore → Pizza ← [CheesPizza, GreekPizza, PeperoniPizza]`
    - 화살표의 방향도 바뀐 것을 확인할 수 있다.
  - 의존성 역전 원칙을 지키는 방법
    - 변수에 구상 클래스의 레퍼런스를 저장하지 말자.
    - 구상 클래스에서 유도된 클래스를 만들지 말자.
    - 베이스 클래스에 이미 구현되어 있는 메서드를 오버라이드하지 말자(베이스 클래스가 제대로 추상화되지 않는다. 베이스 클래스에서는 모든 서브클래스에서 공유할 수 있는 것만 정의해야 한다).
    - 이는 가이드라인일 뿐 모두 지켜서 개발하는 것은 사실상 불가능하므로, 지향점 정도로 생각하자.



- 지점에서 발생한 또 다른 문제

  - 이제 지점들이 본사가 정한 절차(굽고, 자르고, 포장하고 등)는 잘 따르는데, 피자에 들어가는 재료를 더 싼 재료로 바꾸는 일이 발생했다.
    - 따라서 재료도 본사에서 관리하려 하는데 문제는 각 스타일마다 들어가는 재료가 다르다는 것이다.
    - 예를 들어 뉴욕은 레지아노 치즈를, 시카고는 모짜렐라 치즈를 사용한다.
    - 즉 동일한 구성 요소(치즈, 야채, 소스)로 만들더라도 각 구성 요소별 세부 재료(레지아노 치즈, 모짜렐라 치즈, 양파, 마리나라 소스, 플럼토마토 소스)들이 다르다.
    - 따라서 이러한 재료군(family)을 관리할 방법이 필요하다.
  - 원재료 팩토리 만들기
    - 모든 원재료를 생산하는 팩토리 인터페이스를 정의한다.
    - 각 메서드는 재료 클래스를 반환한다.

  ```py
  from abc import *
  
  
  class PizzaIngredientFactory(metaclass=ABCMeta):
  	
      @abstractmethod
      def create_dough(self):
          pass
  	
      @abstractmethod
      def create_sauce(self):
          pass
  	
      @abstractmethod
      def create_cheese(self):
          pass
  	
      @abstractmethod
      def create_veggies(self):
          pass
  	
      @abstractmethod
      def create_pepperoni(self):
          pass
  ```
  
  - 뉴욕 원재료 팩토리 만들기
  
  ```python
  class NYPizzaIngredientFactory(PizzaIngredientFactory):
  
      def create_dough(self):
          return ThinCrustDough()
  
      def create_sauce(self):
          return MarinaraSauce()
  
      def create_cheese(self):
          return ReggianoChees()
  
      def create_veggies(self):
          return Veggies(veggies=[Garlic(), Onion(), Mushroom()])
  
      def create_pepperoni(self):
          return SlicedPepperoni()
  ```
  
  - Pizza 클래스 변경하기
    - Pizza 클래스가 원재료 팩토리에서 생산한 원재료만 사용하도록 코드를 변경한다.
    - `prepare()`를 추상 메서드로 변경한다.
  
  ```python
  from abc import *
  
  
  class Pizza(metaclass=ABCMeta):
      def __init__(self):
          self.name = None
          self.dough = None
          self.sauce = None
          self.veggies = []
          self.cheese = None
          self.pepperoni = None
          self.toppings = []
  
      # prepare를 추상 메서드로 변경한다.
      @abstractmethod
      def prepare(self):
          pass
  
      # ...
  ```
  
  - 더 이상 `Pizza`의 구상 클래스를 스타일 별로 만들 필요가 없다.
    - 기존에는 `Pizza`의 구상 클래스를 스타일별로 따로 만들었다(`NYCheesePizza`, `ChicagoCheesPiza` 등).
    - 이들은 다른 재료를 사용한다는 것만 빼면 다른 점이 없었다.
    - 따라서 더 이상 `Pizza`의 구상 클래스를 스타일 별로 생성하지 않고, 메뉴별로 생성한 뒤, 달라지는 부분은 원재료 팩터리에서 처리한다.
    - `Pizza`의 구상 클래스는 아래와 같이 원재료 팩토리를 사용하여 피자 재료를 만들며, 재료는 어떤 팩토리를 쓰느냐에 따라 달라지게 된다.
    - `Pizza`의 구상 클래스는 어떤 재료를 쓰는지 전혀 신경쓰지 않고, 피자를 만드는 방법만 알고 있으면 된다.
  
  ```python
  class CheesePizza(Pizza):
      def __init__(self, ingredient_factory: PizzaIngredientFactory):
          self.ingredient_factory = ingredient_factory
      
      def prepare(self):
          print("준비 중:" + name)
          dough = self.ingredient_factory.create_dough()
          sauce = self.ingredient_factory.create_sauce()
          cheese = self.ingredient_factory.create_cheese()
  ```
  
  - 지점 코드 변경하기
    - 피자 구상 클래스의 인스턴스를 생성할 때 지점별 원재료 팩토리 인스턴스를 인자로 넘긴다.
  
  ```python
  class NYStylePizzaStore(PizzaStore):
      def create_pizza(type_):
          pizza = None
          ingredient_factory = NYPizzaIngredientFactory()
          if type_ == "cheese":
              pizza = CheesePizza(ingredient_factory)
              pizza.set_name("NY style cheese pizza")
          elif type_ == "pepperoni":
              pizza = PepperoniPizza(ingredient_factory)
              pizza.set_name("NY style pepperoni pizza")
          elif type_ == "veggie":
              pizza = VeggiePizza(ingredient_factory)
              pizza.set_name("NY style veggie pizza")
          elif type_ == "clam":
              pizza = ClamPizza(ingredient_factory)
              pizza.set_name("NY style clam pizza")
          return pizza
  ```



- 추상 팩토리 패턴(Abstract Factory Pattern)

  - 위에서 발생한 문제를 해결한 방식을 추상 팩토리 패턴이라 부른다.
  - 정의
    - 구상 클래스에 의존하지 않고도 서로 연관되거나 의존적인 객체로 이루어진 제품군을 생산하는 인터페이스를 제공한다.
    - 구상 클래스는 서브 클래스에서 만든다.

  ![image-20230326155336911](design_pattern_part2.assets/image-20230326155336911.png)

  - 추상 팩토리 패턴을 사용하면 클라이언트에서 추상 인터페이스로 일련의 제품을 공급받을 수 있다.
    - 실제로 어떤 제품이 생산되는지는 전혀 알 필요가 없다.
    - 따라서 클라이언트와 팩토리에서 생산되는 제품을 분리할 수 있다.
  - 추상 팩토리에 들어 있는 각 메서드(`create_dough()`, `create_cheese()` 등)들은 팩토리 메서드 방식으로 구현될 수도 있다.

  - 팩토리 매서드 패턴과 추상 팩토리 패턴의 차이
    - 팩토리 메서드 패턴은 상속으로 객체를 만드는 반면, 추상 팩토리는 구성(composition)으로 객체를 만든다.
    - 또한 새로운 제품군이 추가될 경우 추상 팩토리는 인터페이스 변경이 필요하다는 단점이 있다. 예를 들어 `ProductC`를 추가해야한다면 `AbstractFactory` 인터페이스에 `create_productC` 코드를 추가해야한다.
    - 팩토리 메서드의 경우 단 하나의 Product만 생산할 수 밖에 없다는 단점이 있다.



- Python decorator를 사용하여 factory pattern 구현하기

  - 아래와 같이 file을 parsing하기 위한 세 개의 함수가 있다.
    - 이 때, file의 type에 따라 그에 맞는 parsing 함수를 호출하려 한다.

  ```python
  def parse_csv(file_path: str):
      print(f"parse {file_path} csv file")
  
  def parse_json(file_path: str):
      print(f"parse {file_path} json file")
  
  def parse_html(file_path: str):
      print(f"parse {file_path} html file")
  ```

  - 먼저 file type과 parsing 함수를 mapping할 dictionary와, mapping 함수를 decorator로 생성한다.

  ```python
  PARSERS = {}
  
  def register_parser(file_type: str):
      def decorator(func):
          PARSERS[file_type] = func
          return func
      return decorator
  ```

  - 위에서 생성한 mapping 함수를 사용하여 `PARSER`에 file type별 parsing함수를 등록한다.

  ```python
  @register_parser('csv')
  def csv_parser(file_path: str):
      return parse_csv(file_path)
  
  @register_parser('json')
  def json_parser(file_path: str):
      return parse_json(file_path)
  
  @register_parser('html')
  def xml_parser(file_path: str):
      return parse_html(file_path)
  ```

  - 아래와 같이 사용한다.

  ```python
  def get_parser(file_type: str):
      return PARSERS.get(file_type)
  
  data_csv = get_parser('csv')('data.csv')
  ```





# Singleton Pattern

- Instance를 단 하나만 생성하기 위한 패턴
  - Instance가 2개 이상일 때, 아래와 같은 문제가 발생할 수 있다.
    - 프로그램이 이상하게 돌아간다.
    - 자원을 불필요하게 잡아먹는다.
    - 결과에 일관성이 없어진다.
  - 따라서 단 하나의 instance만 생성하기 위한 pattern이 필요하다.
    - 굳이 싱글턴 패턴을 사용하지 않고 instance를 전역 변수로 선언한 뒤 사용하면 되지 않을까 생각할 수 있지만, 전역 변수를 사용하는 것과 차별점이 있다.
    - 단순히 전역 변수로 선언하면, 해당 인스턴스를 사용하지 않더라도 계속 메모리를 점유하고 있게 된다.
    - 반면에 싱글턴 패턴은 필요할 때만 인스턴스를 생성하여 메모리를 절약할 수 있게 된다.



- 고전적인 싱글턴 패턴 구현 방법

  - Java code는 아래와 같다.
    - `Singleton`도 일반적인 class이므로 다른 인스턴스 변수와 메서드들을 가질 수 있다.

  ```java
  public class Singleton {
      // Singleton class의 하나뿐인 인스턴스를 저장하기 위한 변수
      private static Singleton uniqueInstance;
      
      // 기타 인스턴스 변수
      
      // 생성자를 private으로 선언했으므로, Singleton에서만 class의 instance를 만들 수 있다.
      private Singleton(){}
      
      // class의 인스턴스를 만들어서 반환하는 정적 메서드이다.
      public static Singleton getInstance() {
          if (uniqueInstance == null) {
              uniqueInstance = new Singleton();
          }
          return uniqueInstance;
      }
      
      // 기타 메서드
  }
  ```

  - 방식
    - `Singleton`의 생성자 메서드를 private으로 선언해 class 외부에서 생성자에 접근할 수 없게 한다.
    - `getInstance()` 메서드를 정적 메서드로 선언하여 인스턴스를 생성하지 않고도 class만으로 호출할 수 있게한다.
    - 조건문을 통해 `uniqueInstance`가 null일 때만, 즉 한 번도 생성된 적 없을 때만 인스턴스를 생성하게 한다.



- 초콜릿 보일러 코드

  - 초콜릿 공장에서 초콜릿 끓이는 장치를 컴퓨터로 제어하는데, 이 장치를 초콜릿 보일러라 한다.
    - 초콜릿 보일러는 초콜릿과 우유를 받아서 끓이고 초코바를 만드는 단계로 넘겨준다.

  ```java
  public class ChocolateBoiler {
      private boolean empty;
      private boolean boiled;
      
      private ChocolateBoiler() {
          empty = true;
          boiled = true;
      }
      
      // 보일러가 비어 있을 때만 재료를 넣는다.
      public void fill() {
          if (isEmpty()) {
              empty = false;
              boiled = false;
          }
      }
      
      public void drain() {
          if (!isEmpty() && isBoiled()) {
              empty = true;
          }
      }
      
      public void boil() {
          if (!isEmpty() && !isBoiled()) {
              boiled = true;
          }
      }
      
      public boolean isEmpty() {
          return empty;
      }
      
      public boolean isBoiled() {
          return boiled;
      }
  }
  ```

  - 위 코드에는 싱글턴 패턴이 적용되지 않았다.
    - 따라서 둘 이상의 `ChocolateBoiler` 인스턴스가 생성되어 따로 작동할 경우 문제가 발생할 수 있다.



- 싱글턴 패턴(Singleton Pattern)

  - 정의
    - 클래스 인스턴스를 하나만 만들고, 그 인스턴스로의 전역 접근을 제공하는 패턴이다.
  - 클래스 인스턴스를 하나만 만든다.
    - 싱글턴 패턴을 실제로 적용할 때는 클래스에서 하나뿐인 인스턴스를 관리하도록 만들어야한다.
    - 어떤 클래스에서도 자신의 인스턴스를 추가로 만들지 못하게 해야한다.
  - 어디서든 인스턴스에 접근할 수 있도록 전역 접근 지점을 제공한다.
    - 언제든 이 인스턴스가 필요하면 클래스에 요청할 수 있게 만들어 놓고, 요청이 들어오면 그 하나뿐인 인스턴스를 건네주도록 만들어야 한다.
  - 즉, 단일 인스턴스를 저장할 변수와 단일 인스턴스를 생성 및 생성된 단일 인스턴스에 접근할 수 있게 해주는 메서드를 반드시 구현해야한다.
  - `ChocolateBoiler`에 고전적 싱글턴을 적용하기

  ```java
  public class ChocolateBoiler {
      private boolean empty;
      private boolean boiled;
      // 유일한 인스턴스를 담을 변수를 추가한다.
      private static ChocolateBoiler uniqueInstance;
  
      private ChocolateBoiler() {
          empty = true;
          boiled = true;
      }
  	
      // getInstanace 메서드를 추가한다.
      private static ChocolateBoiler getInstance() {
          if (uniqueInstance == null) {
              uniqueInstance = new ChocolateBoiler();
          }
          return uniqueInstance;
      }
      
      // 기타 메서드
  }
  ```



- 멀티스레딩 문제

  - 고전적 싱글턴 패턴을 적용했음에도, 멀티스레딩을 적용했을 때 문제가 발생했다.
    - 두 개의 스레드가 다른 보일러 객체를 사용하게 되어 이 같은 문제가 발생하게 됐다.
    - `fill()`메서드에서 아직 초콜릿이 끓고 있는데 새로운 재료를 넣어 우유와 초콜릿이 넘치고 말았다.
  - 원인
    - 두 개의 스레드가 거의 동시에 `getInstance()` 메서드를 실행한다.
    - `(uniqueInstance == null)` 를 체크 할 때 어떤 스레드도 아직 인스턴스를 생성하지 않았으므로, `(uniqueInstance == null)`의 값이 true가 되고, 두 스레드 모두 새로운 인스턴스를 생성한다.

  ```java
  private static ChocolateBoiler getInstance() {
      if (uniqueInstance == null) {
          uniqueInstance = new ChocolateBoiler();
      }
      return uniqueInstance;
  }
  ```

  - 해결
    - `synchronized` 키워드를 추가하여 한 스레드가 메서드 사용을 끝내기 전 까지 다른 스레드가 대기하도록 한다.

  ```java
  private static synchronized ChocolateBoiler getInstance() {
      if (uniqueInstance == null) {
          uniqueInstance = new ChocolateBoiler();
      }
      return uniqueInstance;
  }
  ```

  - 또 다른 문제
    - 한 스레드가 대기해야 하므로 속도가 문제가 될 수 있다.
    - 사실 위 메서드에서 동기화가 필요한 시점(즉, 한 스레드가 다른 스레드를 기다려야 하는 시점)은 `(uniqueInstance == null)`를 판단할 때 뿐이다.
    - 따라서 메서드 전체를 동기화시키는 것은 불필요한 오버헤드를 증가시킬 수 있다.



- 더 효율적인 해결 방법

  - 방법1. `getInstance()` 메서드의 속도가 그리 중요하지 않다면 그냥 둔다.
  - 방법2. 인스턴스가 필요할 때는 생성하지 말고 처음부터 만든다.

  ```java
  public class Singleton {
      private static Singleton uniqueInstance = new Singleton();
      
      private Singleton() {}
      
      public static Singleton getInstance() {
          return uniqueInstance;
      }
  }
  ```

  - 방법3. DCL을 써서 `getInstance()`에서 동기화되는 부분을 줄인다.
    - DCL(Double-Checked Locking)을 사용하면 인스턴스가 생성되어 있는지 확인한 다음 생성되어 있지 않았을 때만 동기화할 수 있다.
    - `volatile` 키워드를 사용하면 멀티 스레딩을 사용하더라도 `uniqueInstance` 변수가 `Singleton` 인스턴스로 초기화되는 과정이 올바르게 진행된다.

  ```java
  public class Singleton {
      private volatile static Singleton uniqueInstance;
      
      private Singleton() {}
      
      public static Singleton getInstance() {
          if (uniqueInstance == null) {
              synchronized (Singleton.class) {
                  if (uniqueInstance == null) {
                      uniqueInstance = new Singleton();
                  }
              }
          }
      }
  }
  ```



- 싱글턴 패턴의 문제점들

  - 느슨한 결합 원칙에 위배된다.
    - 싱글턴을 사용하다보면 느슨한 결합 원칙을 위배하기 쉽다.
    - 싱글턴을 바꾸면 연결된 모든 객체를 바꿔야할 가능성이 높아진다.

  - 한 클래스가 한 가지만 책임지기 원칙에 위배된다.
    - 싱글턴 클래스는 자신의 인스턴스를 관리하는 일 외에 그 인스턴스를 사용하고자 하는 목적에 부합하는 작업(위의 경우 초콜릿을 끓이는 것)을 책임져야한다.
    - 따라서 2가지를 책임지고 있다고 할 수 있다.
  - 리플렉션, 직렬화, 역직렬화가 문제가 될 수 있다.

  - 싱글턴의 서브 클래스 만들기가 까다롭다.
    - 생성자가 private으로 선언되어 있어 확장할 수 없기에 생성자를 public, protected로 선언해야 한다.
    - 그러나 이 경우 다른 클래스에서 인스턴스를 만들 수 있기에 싱글턴이라 할 수 없다.
    - 어찌 저찌 위 문제를 해결한다 하더라도, 싱글턴은 정적 변수를 바탕으로 구현한다는 문제가 있다.
    - 정적 변수를 바탕으로 구현하기에 모든 서브클래스가 같은 인스턴스 변수를 공유하게 된다.
  - 클래스 로더마다 서로 다른 네임스페이스를 정의하기에 클래스 로더가 2개 이상이라면 같은 클래스를 여러 번(각 클래스 로더마다 한 번씩)로딩할 수도 있다.
    - 싱글턴을 이런 식으로 로딩하면 인스턴스가 여러 개 만들어지는 문제가 발생할 수 있다.
    - 클래스 로더를 직접 지정하면 이 문제를 피할 수 있다.



- Enum을 활용한 보다 간편한 구현

  - Enum을 사용하면 위에서 언급한 문제들 중 동기화 문제, 클래스 로딩 문제, 리플렉션, 직렬화, 역직렬화 문제 등을 해결할 수 있다.

  - Enum으로 구현하기

  ```java
  public enum Singleton {
      UNIQUE_INSTANCE;
      // 기타 field 들
  }
  
  
  public class SingletonClient {
      public static void main(String[] args) {
          Singleton singleton = Singleton.UNIQUE_INSTANCE;
          // 여기서 싱글턴 사용
      }
  }
  ```

  - 실제로는 이 방식을 가장 많이 사용한다.
    - 사실 위에서 살펴본 고전적인 싱글턴 구현은 잘 사용하지 않는다. 
    - 그럼에도 살펴본 이유는 싱글턴의 작동 원리를 살펴보기 위해서다.







# Command Pattern

- 만능 리모컨 만들기

  - 여러 개의 가정용 기기를 제어할 수 있는 리모컨의 API를 제작해야한다.
    - 각 가정용 기기의 코드는 이미 고객사에서 완성시킨 상태이다.
    - 우리는 리모컨 API를 생성하여 고객사에서 완성시킨 가정용 기기의 코드를 호출하기만 하면 된다.
  - 리모컨은 아래와 같이 생겼다.
    - 7개의 슬롯 각각에 여러 기기들 중 하나를 등록해 놓고 ON, OFF 버튼만을 사용하여 해당 기기를 조작한다.
    - UNDO 버튼을 누르면 마지막으로 누른 버튼의 명령을 취소한다.

  ![image-20230409180628236](design_pattern_part2.assets/image-20230409180628236.png)

  - 문제
    - 다양한 종류의 가정용 기기들을 제어해야한다.
    - 단순히 on/off만 시키면 되는 것이 아니라 각 기기별로 추가적인 기능도 제어할 수 있어야 한다.
    - 제어해야하는 가정용 기기의 종류가 추후에 계속 추가 될 수도 있다.



- 커맨드 패턴에 따라 음식 주문하기

  - 음식 주문 과정
    - 종업원은 고객의 주문(`Order` class의 instance)을 받는다(`take_order()`).
    - 종업원은 주문 처리를 준비한다(`Order` 객체에 있는 `order_up()` 메서드를 호출한다).
    - `Order` 객체에는 음식을 준비할 때 필요한 모든 주문 사항이 들어있는데, `Order` 객체가 `make_burger()`, `make_shake()` 같은 메서드를 호출하여 주방장에게 행동을 지시한다.
    - 주방장은 `Order` 객체로부터 전달받은 지시사항에 따라 음식을 준비한다.
    
  - 주문서(`Order` 객체)의 역할
    - 주문서는 주문 내용을 캡슐화한다.
    - 주문서의 인터페이스에는 식사 준비에 필요한 행동을 캡슐화한 `order_up()` 메서드가 들어있다(이게 유일한 메서드이다).
    - 식사를 주문해야 하는 객체(주방장)의 레퍼런스도 들어있다.
    - 실제와 다른 점은 종업원이 고객이 무엇을 주문했는지, 누가 요리를 할 건지 등을 신경쓰지만, 여기서는 `Order` 객체가 그러한 역할을 한다는 점이다.
  - 종업원의 역할
    - 종업원은 `Order` 객체에서 `order_up()` 메서드를 호출하는 역할을 한다.
    - 실제 종업원과는 달리 주문서에 무슨 내용이 있는지, 누가 식사를 준비하는지 알 필요가 없다.
    - `take_order()` 메서드를 통해 `Order` 객체를 받아 `Order` 객체에서 `order_up()` 메서드를 호출하기만 하면 된다.
  - 주방장의 역할
    - 식사를 준비하는 데 필요한 정보를 가지고 잇다.
    - 종업원이 `Order` 객체에 있는 `order_up()` 메서드를 호출하면, 주방장이 음식을 만들 때 필요한 메서드를 전부 처리한다.
    - 주방장과 종업원은 완전히 분리되어 있으며 종업원은 각 `Order` 객체에 있는 메서드를 호출할 뿐이고, 주방장은 `Order`객체의 `order_up()` 메서드의 호출에 따라 움직일 뿐이다.



- 커맨드 패턴의 요소들

  - 음식 주문 예시와 대응하는 커맨드 패턴의 요소들을 다음과 같다.

  | 커맨드 패턴의 요소 | 음식 주문    |
  | ------------------ | ------------ |
  | Client             | 고객         |
  | Command            | Order        |
  | Invoker            | 종업원       |
  | Receiver           | 주방장       |
  | set_command()      | take_order() |
  | execute()          | order_up()   |

  - `Client` 
    - `Client`객체는 `Command` 객체를 생성한다.
    - `Command` 객체는 `Receiver` 객체에 전달할 일련의 행동으로 구성된다.
  - `Command` 
    - `Command`객체에는 행동과 `Receiver` 객체의 정보가 같이 들어있다.
    - `Command` 객체가 제공하는 메서드는 `execute()` 하나 뿐이며 이 메서드는 행동을 캡슐화하여 `Receiver` 객체에 있는 특정 행동(method)을 처리한다.
  - `Invoker`
    - `Client` 객체는 `Invoker` 객체의 `set_command()` 메서드를 호출하여 `Command` 객체를 넘겨준다.
    - `Command` 객체는 나중에 쓰이기 전까지 `Invoker` 객체에 보관된다.
    - `Client` 객체에서 요청이 오면 `Invoker` 객체는 전달 받은 `Command` 객체 내부의 `execute()` 메서드를 실행한다.
    - 이 때, `execute()` 메서드를 실행한 후 `Command` 객체를 `Invoker` 객체에서 지우도록 할 수도 있고, 지우지 않고 여러 번 실행시키도록 할 수도 있다.
  - `Receiver`
    - `Invoker` 객체가 `Command` 객체의 `execute()` 메서드를 실행하면, `Command` 객체는 생성시에 전달 받았던 `Receiver` 객체에 대한 정보를 토대로 `Receiver` 객체에 있는 행동들을 실행한다.



- 첫 번째 Command 객체 만들기

  - 가정용 기기를 제어하는 데 사용할 리모컨을 위한 커맨드 객체를 생성한다.
  - Command 객체는 모두 같은 인터페이스를 구현해야한다.
    - 이 인터페이스의 메서드는 `execute()`하나 뿐이다.

  ```python
  from abc import ABC
  
  
  class Command(ABC):
      def execute(self):
          pass
  ```

  - Receiver 클래스를 구현한다.
  
  ```python
  from abc import ABC, abstractmethod
  
  # Receiver 클래스
  class Light(ABC):
      @abstractmethod
      def on(self):
          ...
          
  class BathroomLight(Light):
      def on(self):
          print("turn on light of bathroom")
  ```
  
  - 조명을 켤 때 필요한 커맨드 클래스 구현
    - `Command` interface를 구현한 구상 클래스이다.
    - 생성자에 이 커맨드 객체로 제어할 특정 `Receiver`(거실 조명인지 차고 조명인지 욕실 조명인지 등)의 정보가 전달된다.
    - `execute()` 메서드가 호출되면 `Receiver`의 instance(`light`)에 있는 `on()` 메서드를 호출한다.

  ```python
  class LigthOnCommand(Command):
      # Command가 제어할 Receiver(Light)의 인스턴스를 전달 받는다.
      def __init__(self, light: Light):
          self.ligth = ligth
      
      def execute(self):
          # Receiver를 통해 행동을 처리한다.
          self.light.on()
  ```
  
  - 커맨드 객체 사용하기
    - 제어할 기기를 연결할 슬롯과 버튼이 각각 하나씩 밖에 없는 리모컨이 있다고 가정하고, 이 리모컨에서 커맨드 객체를 사용해본다.
    - 이 리모컨 객체가 Invoker 객체가 되는 것이다.
    - Invoker가 요청한 작업을 최종적으로 수행하는 Receiver 객체에 대한 아무런 정보도 가지고 있지 않다는 점에 주목해야 한다.
    - 이처럼 Command pattten은 작업을 요청하는 Invoker와 작업을 수행하는 Receiver를 완전히 분리하며, Command를 통해서만 소통이 이루어진다.
  
  ```python
  # Invoker 클래스
  class SimpleRemoteControl:
      def __init__(self):
          # Command 객체를 저장 할 하나의 slot
          self.slot = None
      
      # slot을 가지고 제어할 command를 설정하는 메서드
      def set_command(self, command):
          self.slot = command
      
      # 리모컨의 버튼을 눌렀을 때 호출되는 메서드
      def button_was_pressed(self):
          self.slot.execute()
  ```
  
  - Client 코드 작성하기
  
  ```python
  # Invoker 역할을 하는 SimpleRemoteControl의 instance 생성
  remote = SimpleRemoteControl()
  # Receiver 역할을 하는 BathroomLight의 instance 생성
  bathroom_light = BathroomLight()
  # Command 객체 생성, Receiver 객체를 전달하여 생성한다.
  light_on = LigthOnCommand(bathroom_light)
  
  # Invoker 객체에 Command 객체 저장
  remote.set_command(light_on)
  # Invoker에 저장된 command 객체에서 execute() 메서드 실행
  remote.button_was_pressed()
  ```



- 커맨드 패턴(Command Pattern)

  - 정의
    - 작업을 요청하는 쪽(`Invoker`)과 처리하는 쪽(`Receiver`)을 분리할 수 있게 해주는 패턴이다.
    - 요청 내역을 객체로 캡슐화해서 객체를 서로 다른 요청 내역에 따라 매개변수화 할 수 있다.
    - 이를 통해 요청을 큐에 저장하거나 로그로 기록하거나 작업 취소 기능을 사용할 수 있다.
  - `Command` 객체는 일련의 행동을 특정 `Receiver`와 연결함으로써 요청을 캡슐화한다.
    - 이를 위해 행동과 `Receiver`를 `Command`라는 한 객체에 넣고 `execute()`라는 메서드 하나만 외부에 공개하는 방법을 사용해야 한다.
    - `execute()` 메서드 호출에 따라 `Receiver`에서 일련의 작업을 처리한다.
    - 밖에서 볼 때는 어떤 객체가 `Receiver` 역할을 하는지, 그 `Receiver`가 어떤 행동을 하는지 알 수 없다.
    - 단순히 `execute()` 메서드를 호출하면 해당 요청이 처리된다는 사실만 알 수 있다.
  - `Command` 객체를 매개변수화 할 수도 있다.
    - `Invoker` 객체는 `Command` 객체가 특정 인터페이스(예시의 경우 `execute()` method)를 구현하기만 했다면, 해당 `Command`에서 실제로 어떤 일을 하는지 신경 쓸 필요가 없다.

  - 다이어그램
    - 클라이언트는 `Receiver`와 행동을 넣어 `ConcreteCommand`를 생성한다.
    - `Invoker`에는 command 객체가 들어있으며, `execute_command()` 메서드를 호출하여 `ConcreteCommand` 객체의 `execute()` 메서드를 수행한다.
    - `Command`는 모든 `ConcreteCommand` 객체가 구현해야하는 인터페이스로, `execute()` 메서드와 `undo()` 메서드를 포함하고 있다.
    - `execute()` 메서드는 `Receiver` 객체에 있는 메서드를 호출해서 요청된 작업을 수행한다.
    - `ConcreteCommand` 는 특정 행동과 Receiver를 연결해준다. `Invoker` 객체가 `execute()`를 실행시키면, `ConcreteCommand` 객체에서 `Receiver` 객체에 있는 메서드를 호출해서 그 작업을 처리한다.
    - `Receiver`는 요구 사항 수행을 위해 어떤 일을 해야하는지 알고 있는 객체이다. 

  ![image-20230409213916328](design_pattern_part2.assets/image-20230409213916328.png)



- 리모컨의 모든 슬롯에 기기 할당하기

  - 리모컨 코드 만들기
    - 총 7개의 슬롯이 있으므로 7개의 슬롯의 on/off 버튼에 할당할 command들을 저장할 `on_commands`와 `off_commands`를 선언한다.

  ```python
  class RemoteControl:
      def __init__(self):
          NUM_SLOT = 7
          self.on_commands = [NoCommand() for _ in range(NUM_SLOT)]
          self.off_commands = [NoCommand() for _ in range(NUM_SLOT)]
  
      def set_command(self, slot, on_command, off_command):
          self.on_commands[slot] = on_command
          self.off_commands[slot] = off_command
  
      def on_button_was_pushed(self, slot):
          self.on_commands[slot].execute()
  
      def off_button_was_pushed(self, slot):
          self.off_commands[slot].execute()
  ```

  - `NoCommand` 객체에 대해서
    - 위에서 `on_commands`와 `off_commands` 인스턴스 변수를 초기화 할 때 `NoCommand` 변수로 초기화했다.
    - 이는 아래 `on_button_was_pushed` 등에서 각 인스턴스 변수에 저장된 `Command` 객체에 인덱스로 접근하기에 `IndexError`가 발생하는 것을 방지하기 위함이다.
    - 이러한 객체를 널 객체라고도 하는데, 딱히 반환할 객체도 없고 클라이언트가 null을 처리하지 않게 하고 싶을 때 활용한다.
    - 구현은 아래와 같다.

  ```python
  class NoCommand(Command):
      def execute(self):
          pass
  ```

  - 조명을 끌 때 사용할 커맨드 클래스 만들기
    - 이번에는 조명을 끌 때 쓰는 `LightOffCommand` 클래스를 만든다.

  ```python
  class LigthOffCommand(Command):
      def __init__(self, light):
          self.light = light
      
      def execute(self):
          self.light.off()
  ```

  - 이번에는 조명 보다 조금 더 복잡한 오디오를 켜고 끌 때 사용할 커맨드 클래스를 만든다.
    - 오디오를 켤 때는 단순히 오디오를 켜기만 하는 것이 아니라 켜고 CD를 넣고, 볼륨을 기본값으로 설정한다.

  ```python
  class StrereoOnWithCDCommand(Command):
      def __init__(self, stereo):
          self.stereo = stereo
          
      def execute(self):
          self.stereo.on()
          self.stereo.set_cd()
          self.stereo.set_volume(10)
  
  class class StrereoOffCommand(Command):
      def __init__(self, stereo):
          self.stereo = stereo
          
      def execute(self):
          self.stereo.off()
  ```

  - 리모컨 테스트 해보기

  ```python
  # 각 기기를 생성한다.
  living_room_light = Light("Living Room")
  garage_light = Light("Garage")
  stereo = Stereo()
  
  # 각 기기별 Command 객체를 생성한다.
  living_room_light_on = LightOnCommand(living_room_light)
  living_room_light_off = LightOffCommand(living_room_light)
  garage_light_on = LightOnCommand(garage_light)
  garage_light_off = LightOffCommand(garage_light)
  stereo_on_with_cd = StrereoOnWithCDCommand(stereo)
  stereo_off = StrereoOffCommand(stereo)
  
  # Command 객체를 RemoteControl객체의 각 슬롯에 로드한다.
  remote_control = RemoteControl()
  remote_control.set_command(0, living_room_light_on, living_room_light_off)
  remote_control.set_command(1, garage_light_on, garage_light_off)
  remote_control.set_command(2, stereo_on_with_cd, stereo_off)
  
  # 실행한다.
  remote_control.on_button_was_pushed(0)
  remote_control.off_button_was_pushed(0)
  remote_control.on_button_was_pushed(1)
  remote_control.off_button_was_pushed(1)
  remote_control.on_button_was_pushed(2)
  remote_control.off_button_was_pushed(2)
  ```



- 작업 취소 기능 추가하기

  - 위에서 커맨드 디자인 패턴에 대해 "작업 취소 기능을 사용할 수 있다"고 했다.
    - 리모컨에 UNDO 버튼을 추가하면서 어떻게 작업 취소가 가능한지 살펴볼 것이다.
    - 예를들어 조명이 꺼진 상태에서 ON 버튼을 눌러 조명을 켠 후 UNDO 버튼을 눌러 조명이 다시 꺼지도록 구현할 것이다.
  - 커맨드에서 작업 취소 기능을 지원하려면 `execute()` 메서드와 비슷한 `undo()` 메서드가 있어야한다.
    - Command interface에 `undo()` 메서드를 추가한다.

  ```python
  from abc import ABC
  
  class Command(ABC):
      def execute(self):
          pass
      
      def undo(self):
          pass
  ```

  - ConcreteCommand class에 `undo()` 메서드를 추가한다.
    - 비교적 간단한 `LightOnCommand`, `LightOffCommand`에 추가해본다.

  ```python
  class LigthOnCommand(Command):
      def __init__(self, light):
          self.ligth = ligth
      
      def execute(self):
          self.light.on()
      
      def undo(self):
          self.ligth.off()
  
          
  class LigthOffCommand(Command):
      def __init__(self, light):
          self.ligth = ligth
      
      def execute(self):
          self.light.off()
      
      def undo(self):
          self.ligth.on()
  ```

  - 리모컨 class에 `undo_command`라는 인스턴스 변수와 `undo_button_was_pushed()` 메서드를 추가한다.
    - 또한 `on_button_was_pushed()`와 `off_button_was_pushed()` 메서드도 약간씩 수정한다.

  ```python
  class RemoteControl:
      def __init__(self):
          # ...
          self.undo_command = NoCommand()
  
      def set_command(self, slot, on_command, off_command):
          self.on_commands[slot] = on_command
          self.off_commands[slot] = off_command
  
      def on_button_was_pushed(self, slot):
          self.on_commands[slot].execute()
          self.undo_command = on_command[slot]
  
      def off_button_was_pushed(self, slot):
          self.off_commands[slot].execute()
          self.undo_command = off_command[slot]
          
      def undo_button_was_pushed(self):
          self.undo_command.undo()
  ```



- 작업 취소 기능을 구현할 때 상태를 사용하는 방법

  - 고객사에서 제공한 선풍기의 코드는 아래와 같다.
    - 선풍기의 속도와 방향을 instance 변수와 속도를 변경할 수 있는 메서드들, 그리고 현재 속도를 반환하는 메서드를 가지고 있다.
    - 선풍기에서 작업 취소 기능을 구현하기 위해서는 이전에 설정했던 선풍기 속도에 대한 정보가 필요하다.
    - 이전 속도를 저장해 뒀다가 `undo()` 메서드 호출시 이전 속도로 되돌아가도록 해야한다.

  ```python
  class CeilingFan:
      HIGH = 3
      MEDIUM = 2
      LOW = 1
      OFF = 0
  
      def __init__(self, location):
          self.location = location
          self.speed = self.OFF
  
      def high(self):
          self.speed = self.HIGH
  
      def medium(self):
          self.speed = self.MEDIUM
  
      def low(self):
          self.speed = self.LOW
  
      def off(self):
          self.speed = self.OFF
      
      def get_speed(self):
          return self.speed
  ```

  - 선풍기 속도를 high로 변경하는 Command 구현하기

  ```python
  class CeilingFanHighCommad(Command):
      def __init__(self, ceiling_fan):
          self.ceiling_fan = ceiling_fan
          self.prev_speed = None
  
      def execute(self):
          prev_speed = self.ceiling_fan.get_speed()
          self.ceiling_fan.high()
  
      def undo(self):
          if self.prev_speed == CeilingFan.HIGH:
              self.ceiling_fan.high()
          elif self.prev_speed == CeilingFan.MEDIUM:
              self.ceiling_fan.medium()
          elif self.prev_speed == CeilingFan.LOW:
              self.ceiling_fan.low()
          elif self.prev_speed == CeilingFan.OFF:
              self.ceiling_fan.off()



- 여러 동작을 한 번에 처리하기

  - 버튼 한 개만 누르면 조명이 어두워지면서 TV가 켜지고 DVD 모드로 변경되는 등의 동작이 한 번에 처리되게 하려고 한다.
  - 매크로 커맨드 구현하기

  ```python
  class MacroCommand(Command):
      def __init__(self, commands):
          self.commands = commands
      
      def execute(self):
          for command in self.commands:
              command.execute()
      
      def undo(self):
          for command in self.commands:
              command.undo()
  ```

  - 사용해보기

  ```python
  # Receiver들을 생성한다.
  light = Light("Living Room")
  stereo = Stereo()
  tv = TV()
  hottub = Hottub()
  
  # MacroCommand에 추가할 command들을 생성한다.
  party_on = [LightOnCommand(light), StereoOnCommand(stereo), TVOnCommand(tv), HottubOnCommand(hottub)]
  party_off = [LightOffCommand(light), StereoOffCommand(stereo), TVOffCommand(tv), HottubOffCommand(hottub)]
  
  # MacroCommand를 생성한다.
  party_on_macro = MacroCommand(party_on)
  party_off_macro = MacroCommand(party_off)
  
  # MacroCommand 객체를 버튼에 할당한다.
  remote_control.set_command(0, party_on_macro, party_off_macro)
  ```



- 요청을 큐에 저장하기
  - Command 객체를 큐에 넣는 방식으로 활용할 수 있다.
    - 이를 통해 클라이언트 애플리케이션에서 커맨드 객체를 생성한 뒤 오랜 시간이 지나도 Command 객체를 호출할 수 있게 된다.
    - 심지어 이를 다른 스레드에서 호출할 수도 있다.
    - 이점을 이용해 커맨드 패턴을 스케쥴러나 스레드 풀, 작업 큐와 같은 다양한 작업에 적용할 수 있다.
  - 작업 큐 예시
    - 큐에 Command 객체를 추가한다.
    - 큐에서 Command 객체를 하나씩 빼서 여러 개의 스레드로 분배한다.
    - 각 스레드는 받아 온 Command 객체에서 `execute()` 메서드를 실행한다.
    - 실행이 완료되면 작업 큐에서 새로운 Command 객체를 받아온다.



- 복구 시스템에 사용하기
  - Command 인터페이스에 `execute()` 메서드 뿐 아니라 `store()`, `load()` 메서드를 추가한다.
    - `store()` 메서드는 Command 객체를 저장하는 메서드이다.
    - `load()` 메서드는 Command 객체를 불러오는 메서드이다.
  - 복구 과정 예시
    - `InsertDataCommand`라는 command 객체가 있다.
    - 이 객체는 `execute()`가 실행될 때 임의의 저장소에 data를 1건씩 저장한다.
    - 그런데, 모종의 이유로 해당 저장소가 복구 할 수 없는 상태로 다운되었다.
    - 이 때, `InsertDataCommand`에 `store()`, `load()` 메서드가 있었다면 다음과 같이 처리할 수 있었을 것이다.
    - 먼저 `execute()` 메서드를 실행하여 저장소 A에 data를 저장한다.
    - 그 후 `store()` 메서드를 실행하여 저장소 B에 `InsertDataCommand` 객체를 저장한다.
    - 저장소 A가 다운 될 경우 저장소 B에 저장된 `InsertDataCommand` 객체들의 `load()` 메서드를 사용하여 하나씩 불러온다.
    - 불러온 `InsertDataCommand()` 객체들에서 `execute()` 메서드를 재실행한다. 







# 디자인 원칙 모아보기

- 구상 클래스에 의존하지 않게 하고 추상화된 것에 의존하게 한다.















