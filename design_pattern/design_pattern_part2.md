# 팩토리 패턴

- 최첨단 피자 코드 만들기

  - 피자 생성 코드
    - 여기서의 `Pizza`는 인터페이스가 아닌 구상 클래스이다.

  ```python
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
  def order_pizza(type_):
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
    - `GreekPizzar`를 제외하고 `VeggiePizza`와 `ClamPizza`가 추가되어야 한다.

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
    - 위 예시에서는 `order_pizza()`만 살펴봤지만, `show_ingredients()` 등 pizza 인스턴스가 필요한 수 많은 메서드가 있을 수 있다.
    - 만일 팩토리 한 곳에 위임해서 처리하지 않고, 모든 메서드에서 객체의 생성을 위와 같이 관리한다면, 수정사항이 있을 때 마다 모든 코드를 다 변경해줘야한다.
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
    - 새로운 피자의 추가, 삭제가 일어날 때에도 factory의 코드만 변경하면 된다.

  - Simple factory란 디자인 패턴이라기 보다는 프로그래밍에서 자주 쓰이는 관용구에 가깝다.
    - 워낙 자주 쓰이다 보니 simple factory를 factory pattern이라 부르는 사람들도 있다.
    - 그럼에도 simple factory는 정확히는 패턴은 아니다.
  - Static factory란
    - 정적 메서드를 사용하여 객체를 생성하는 factory를 의미한다.
    - Java에서 static 메서드는 해당 메서드가 포함된 클래스의 인스턴스를 생성하지 않아도 실행시킬 수 있는 메서드를 의미한다.
    - 정적 메서드를 사용하는 이유는 객체 생성을 위해 factory 클래스의 인스턴스를 만들지 않아도 돼서 보다 간편하게 객체를 생성할 수 있기 때문이다.
    - 다만, 서브클래스를 만들어 객체 생성 메서드의 행동을 변경할 수 없다는 단점이 있다.



- 다양한 팩토리 만들기

  - 피자 가게가 성장하면서 각 지역마다 지점을 내기로 했다.
    - 각 지역의 특성을 반영한 다양한 스타일의 피자를 출시하려 한다.
  - 각 피자 스타일별로 팩토리를 하나씩 생성하기로 한다.
    - 본사에서는 각 지역 스타일에 맞는 피자를 생성해주는 factory만 구현해준다.
    - 그리고 모든 지점에서 동일한 과정을 거쳐 피자를 만들게 하기 위해서 `PizzaStore`를 참고하여 각 지점마다 `PizzaStore` 클래스를 만들도록했다.  
    - 

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
  
  
  ny_store = PizzaStore(NYPizzaFactory())
  pizza = ny_store.order_pizza()
  
  chicago_store = PizzaStore(ChicagoPizzaFactory())
  pizza = chicago_store.order_pizza()
  ```

  - 위 방식의 문제
    - 각 지점마다 Pizza를 생성하는 팩토리를 제대로 쓰긴 하는데, 정작 그 factory가 생성하는 instance로 피자를 생성하는 로직이 담긴 `PizzaStore`를 지점마다 구현하다보니 지점 사이에 차이가 생기게 된다.
    - 즉 지점마다 다른 조리법, 다른 포장 상자 등을 사용하기 시작한다.
    - 이는 `PizzaStore`와 피자 제작 코드가 서로 분리되어 있기 때문에 발생한다.
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
    - 이제 `PizzaStore` 클래스의 `order_pizza()`메서드에서는 `Pizza` 객체를 가지고 피자를 준비하고, 굽고, 자르고, 포장하는 작업을 하지만, `Pizza`는 추상 클래스이므로 `order_pizza()` 메서드는 실제로 어떤 구상 클래스에서 작업이 처리되고 있는지 전혀 알 수 없다.
    - 즉, `PizzaStore`와 `Pizza`는 완전히 분리되어 있다.
    - `order_pizza()`에서 `create_pizza()`를 호출하면 `Pizza`의 서브클래스가 그 호출을 받아서 피자를 만들기에, `NYStylePizzaStore`에서 `order_pizza()`가 호출되면 뉴욕 스타일 피자가 만들어지고, `ChicagoStylePizzaStore`에서 `order_pizza()`가 호출되면 시카고 스타일 피자가 만들어진다.
    - 즉 서브 클래스에서 피자의 종류를 실시간으로 결정하는 것이 아니라, 어떤 서브클래스를 선택했느냐에 따라 피자의 종류가 결정되게 된다.

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



- 팩토리 메서드 패턴
  - 모든 팩터리 패턴은 객체 생성을 캡슐화한다.
  - 팩토리 메서드 패턴은 서브클래스에서 어떤 클래스를 만들지를 결정함으로써 객체 생성을 캡슐화한다.













