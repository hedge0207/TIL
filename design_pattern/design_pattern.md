# Design Pattern

> https://github.com/faif/python-patterns
>
> https://refactoring.guru/design-patterns



- Design pattern

  - 소프트웨어를 개발하면서 공통으로 발생하는 문제를 해결하기 위해 자주 사용되는 방법들을 정리한 패턴이다.

  - 생성, 구조, 행위 패턴이 있다.
    - 생성: 객체 인스턴스의 생성과 관련된 패턴
    - 구조: 더 큰 구조를 생성하기 위해 클래스나 객체의 조합을 다루는 패턴
    - 행위: 클래스나 객체들이 상호작용하는 방법과 역할 분담을 다루는 패턴



- concrete class
  - abstract class가 아닌 모든 class를 concrete class라 부른다.
  - 구상 클래스, 구현 클래스, 구체 클래스 등으로 번역한다.



## 생성

- Builder
  - 복잡한 인스턴스를 조립하여 만드는 구조
  - 객체를 생성하는 방법과 객체를 구현하는 과정을 분리하여 동일한 생성 절차에서 서로 다른 표현 결과를 만들 수 있는 패턴



- Prototype
  - 일반적인 원형을 만들고, 필요한 부분만 수정하여 사용하는 패턴
  - 기존 객체를 복제하여 새로운 객체 생성



- Factory Method
  - 상위 클래스에서 객체를 생성하는 인터페이스를 정의하고, 하위 클래스에서 인스턴스를 생성하도록 하는 패턴
  - 생성할 객체의 클래스를 국한하지 안고 객체를 생성



- Abstract Factory
  - 구체적인 클래스에 의존하지 않고 서로 연관되거나 의존적인 객체들의 조합을 만드는 인터페이스를 제공.
  - 동일한 주제의 다른 팩토리를 묶음



- Singleton
  - 객체를 하나만 생성하도록 하며 생성된 객체를 어디에서든지 참조할 수 있도록 하는 패턴
  - 한 클래스에 한 객체만 존재하도록 제한



## 구조

- Bridge
  - 기능의 클래스 계층과 구현의 클래스 계층을 연결
  - 구현뿐 아니라 추상화 된 부분까지 변경해야 하는 경우 사용



- Decorator
  - 구현되어 있는 클래스에 필요한 기능을 추가
  - 상속의 대안으로 사용



- Facade
  - 복잡한 시스템에 대하여 단순한 인터페이스를 제공하여 사용자와 시스템간 결합도를 낮춰 시스템 구조에 대한 파악일 쉽게 하는 패턴
  - 통합된 인터페이스 제공



- Flyweight
  - 다수의 객체를 생성할 경우 모두가 갖는 본질적인 요소를 클래스화하여 공유
  - 메모리 절약과 클래스 경량화 목적
  - 가상 인스턴스 제공



- Proxy
  - 미리 할당하지 않아도 상관 없는 것들을 실제 사용할 때 할당하게 하는 패턴
  - 정보 은닉의 역할도 수행한다.



- Composite
  - 객체들의 관계를 트리 구조로 구성하여 부분-전체 계층을 표현하는 패턴
  - 복합 객체와 단일 객체를 동일하게 취급



- Adapter
  - 기존에 생성된 클래스를 재사용할 수 있도록 중간에서 맞춰주는 역할을 하는 인터페이스를 만드는 패턴
  - 상속을 이용하는 클래스 패턴과 위임을 이용하는 인터페이스 패턴의 두 가지 형태로 사용된다.



## 행위

- Mediator
  - 서로 간 통신 시 중간에서 이를 통재하고 지시할 수 있는 역하를 하는 중재자를 두는 패턴.
  - 통신의 빈도수를 줄여준다.



- Interpreter
  - 여러 형태의 언어 구문을 해석할 수 있게 만드는 패턴



- Iterator
  - 컬렉션 구현 방법을 노출시키지 않으면서도 집합체 안에 들어있는 모든 항목에 접근할 방법을 제공하는 패턴



- Template Method
  - 상위 클래스에는 추상 메서드를 통해 기능의 골격을 정의, 하위 클래스에는 세부 처리를 구체화 하는 패턴



- Observer
  - 한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체들의 내용도 자동으로 갱신되는 패턴



- State
  - 객체의 상태에 따라 행위의 내용이 변경되는 패턴



- Visitor
  - 각 클래스 데이터 구조로부터 처리 기능을 분리하여 별도의 클래스를 생성하고, 해당 클래스의 메서드가 각 클래스를 돌아다니며 특정 작업을 수행



- Command
  - 실행될 기능을 캡슐화하여 주어진 여러 기능을 수행할 수 있는 재사용성이 높은 클래스를 설계하는 패턴
  - 각 명령이 들어오면 그에 맞는 서브 클래스가 선택되어 실행됨.



- Strategy
  - 알고리즘군을 정의하고 같은 알고리즘을 하나의 클래스로 캡슐화한 후 필요할 때 서로 교환해서 사용.
  - 행위를 클래스로 캡슐화해 동적으로 행위를 자유롭게 변환



- Memento
  - 객체의 정보를 저장할 필요가 있을 때 적용
  - Undo 기능을 개발할 때 사용



- Chain of Responsibility
  - 한 요청을 2 개 이상의 객체에서 처리



# Creational Patterns

## Builder

- 개요
  - 복합 객체의 생성과 표현을 분리한다.
  - 이를 통해 동일한 생성 절차로 다른 표현을 생성할 수 있다.
  - 객체의 spec을 실제 표현과 분리해야 할 때 유용하게 사용할 수 있다.



- 문제

  - 상황
    - House 클래스를 통해 인스턴스를 생성해야 한다고 가정해보자.
    - 간단한 객체를 생성하려 한다면 wall, door, window, roof, floor 등의 arguments만 받으면 될 것이다.
    - 그러나, House class를 통해 보다 다양한 유형의 인스턴스를 생성하고자 한다면, has_garden, has_heating_system, has_swimming_pool 등 보다 많은 arguments를 받아야 할 것이다.
  - 이를 House class에서 모두 관리를 하는 것은 비효율 적이다.
    - 예를 들어 굉장히 소수의 인스턴스만 has_swimming_pool의 값이 true로 들어올텐데, 이들을 생성시마다 넘겨주는 것은 비효율 적이다.
    - 또한 만약 요구사항 변경에 의해 새로운 arguments가 추가된다면, 예를 들어 has_garage argument가 추가된다면, 기존 House 인스턴스를 생성하는 모든 코드에 has_garage parameter를 추가해줘야 한다.
    - 또한 객체 생성 부분만 보고, 각 parameter가 무엇을 의미하는지 알기도 쉽지 않다.

  ```python
  class House:
  	def __init__(self, num_window, wall, roof, floor, 
  				has_garden, has_heating_system, has_swimming_pool):
  		pass
  
  simple_house = House(2, "stone", "wood", 1, False, False, False)
  fancy_house = House(8, "brick", "glass", 2, True, True, True)
  
  # 만일 새로운 argument가 추가된다면 simple_house, fancy_house의 생성 부분에 모두 parameter를 추가해야한다.
  # 또한 House(8, "brick", "glass", 2, True, True, True)만 보고는 어떤 집을 만드려는 것인지 파악이 쉽지 않다.
  ```



- 해결
  - 모든 Builder에 공통으로 들어가는 로직을 선언할 Builder interface를 생성한다(optional).
    - 이 interface를 Builder라 부르고, 이를 구체화 한 class를 Concrete Builder라 부르기도 한다.
  - Builder interface를 구체화 한 Concrete Builder class를 생성한다.
    - Builder interface를 생성하지 않았다면 그냥 Builder class를 생성한다.
  - Director를 생성하고, director에게 객체의 생성을 맡긴다(optional)
    - Director에는 builder 내에 정의되어 있는 객체 생성 메서드들을 어느 순서로 실행할지를 정의한다.
    - Director를 사용할 경우 client는 director를 통해서만 객체를 생성한다.
    - 따라서 객체의 생성을 client code로부터 완전히 감출 수 있다.



- 예시

  - 자동차를 생성하는 concrete builder class를 작성한다.
    - 자동차는 다양한 방식으로 생성된다.
    - 자동차를 생성하는 모든 방식을 망라하는 하나의 거대한 class를 만드는 대신 자동차를 조립하는 코드를 개별적인 builder로 분리해서 자동차를 생성한다.
  - 자동차의 메뉴얼을 생성하는 concrete builder class를 생성한다.
    - 자동차의 메뉴얼은 자동차의 종류에 따라 달라지며, 대부분 자동차의 부품에 대한 설명이다.
    - 따라서 자동차와 같은 builder interface를 구현하여 작성이 가능하다.

  ```python
  from abc import abstractmethod
  
  
  class Car:
  	def __init__(self):
  		self.num_seat = 0
  		self.engine = None
  		self.trip_computer = None
  		self.gps = None
  
  
  class Manual:
  	def __init__(self):
  		self.num_seat = ""
  		self.engine_name = ""
  		self.trip_computer_name = ""
  		self.gps_name = ""
  
  # builder (interface) 생성하기
  class Builder:
  
  	@abstractmethod
  	def reset(self):
  		pass
  
  	@abstractmethod
  	def set_seats(self):
  		pass
  
  	@abstractmethod
  	def set_engine(self):
  		pass
  
  	@abstractmethod
  	def set_trip_computer(self):
  		pass
  
  	@abstractmethod
  	def set_gps(self):
  		pass
  
  
  # Car 생성을 위한 (concrete) builder 생성하기
  class CarBuilder(Builder):
  
  	def __init__(self):
  		self.reset()
  	
  	def reset(self):
  		self._car = Car()
  
  	def set_seats(self, num_seat):
  		self._car.num_seat = num_seat
  
  	def set_engine(self, engine):
  		self._car.engine = engine
  
  	def set_trip_computer(self, trip_computer):
  		self._car.trip_computer = trip_computer
  
  	def set_gps(self, gps):
  		self._car.gps = gps
  	
  	@property
  	def car(self):
  		car = self._car
  		self.reset()
  		return car
  
  
  # Car Manual 생성을 위한 (concrete) builder 생성하기
  class ManualBuilder(Builder):
  
  	def __init__(self):
  		self.reset()
  	
  	def reset(self):
  		self._manual = Manual()
  
  	def set_seats(self, num_seat):
  		self._manual.num_seat = "number of seats : {}".format(num_seat)
  
  	def set_engine(self, engine):
  		self._manual.engine_name = "engine : {}".format(engine)
  
  	def set_trip_computer(self, trip_computer):
  		self._manual.trip_computer_name = "trip_computer : {}".format(trip_computer)
  
  	def set_gps(self, gps):
  		self._manual.gps_name = "gps : {}".format(gps)
  
  	@property
  	def manual(self):
  		manual = self._manual
  		self.reset()
  		return manual
  
  
  # Builder를 통한 객체 생성 순서를 정의하기 위한 Director 생성
  class Director:
  
  	def construct_sporst_car(self, builder):
  		builder.reset()
  		builder.set_seats(2)
  		builder.set_engine("sports_car_engine")
  		builder.set_trip_computer("sports_navi")
  		builder.set_gps("sports_gps")
  	
  	def construct_suv(self, builder):
  		builder.reset()
  		builder.set_seats(6)
  		builder.set_engine("suv_engine")
  		builder.set_trip_computer("suv_navi")
  		builder.set_gps("suv_gps")
  
  
  if __name__=="__main__":
  	# client code
  	# director를 사용했으므로, construct_sporst_car 메서드만 호출하면 되며,
  	# 내부적으로 sports car가 어떻게 생성되는지는 감출 수 있다.
  	direcotr = Director()
  	builder = CarBuilder()
  	direcotr.construct_sporst_car(builder)
  	car = builder.car
  
  	builder = ManualBuilder()
  	direcotr.construct_sporst_car(builder)
  	manual = builder.manual
  ```



- 한계
  - 결국 생성하려는 객체에 맞춰 builder를 계속 늘어나게 된다.
  - Python에서도 유용한 패턴인지 의문
    - Python의 경우 parameter에 기본값을 설정 가능하다.
    - Keyword argument를 통해 어떤 값을 넘기는지 명시적으로 표현이 가능하다.





## Factory

> https://bcp0109.tistory.com/366

- 객체의 생성을 다른 객체(factory)에게 위임하는 design pattern이다.



- 종류
  - Simple Factory
    - 디자인 패턴이라기보다 객체 지향에서 사용하는 하나의 개념에 가깝다.
  - Factory Method
  - Abstract Factory Method



- Simple Factory

  - 가장 기본적인 Factory로, 객체의 생성을 다른 객체에 위임하는 것이다.
    - 인터페이스나 상속 등의 개념을 사용하지 않는다.

  ```python
  class KoreanLocalizer:
  
      def __init__(self) -> None:
          self.translations = {"dog": "개", "cat": "고양이"}
  
      def localize(self, msg: str) -> str:
          """We'll punt if we don't have a translation"""
          return self.translations.get(msg, msg)
  
  
  class EnglishLocalizer:
      """Simply echoes the message"""
  
      def localize(self, msg: str) -> str:
          return msg
  
  
  def get_localizer(language: str = "English") -> object:
  
      """Factory"""
      localizers = {
          "English": EnglishLocalizer,
          "Korean": KoreanLocalizer,
      }
  
      return localizers[language]()
  ```

  - 한계
    - 확장에는 용이하지만 변경에 닫혀있어야 한다는 OCP 원칙에 위배된다.
    - 만약 위 예시에서 새로운 Localizer인 `JapaneseLocalizer`가 추가되었다면, `get_localizer` 메서드의 `localizers`에도 추가를 해줘야한다.
    - 확장을 할 때, 기존 코드를 수정해야 하므로, OCP 원칙에 위배된다.
    - Factory Method나 Abstract Factory Method의 경우 기존 코드를 변경하지 않고 확장이 가능하다.





### Factory Method

- 개요
  - 객체의 틀을 잡은인터페이스를 정의하고, 해당 인터페이스를 implement하는 Factory를 통해 객체를 생성한다.
    - 결국 다른 object를 생성하는 object이다.
  - 즉, 객체의 생성을 하위 클래스에 위임한다.



- 문제
  - 상황
    - truck으로 제품을 운송하는 업체를 관리하는 app을 만들었다고 가정해보자.
    - 사업이 성잠함에 따라, 육로가 아닌 해상으로 제품을 운송하는 방식에 대한 수요가 생겼다.
    - 기존에 작성된 대부분의 코드는 truck으로 운송하는 상황만을 생각하고 작성했기에, 모든 코드는 Truck class에 묶여있다.
    - 따라서 Ship class를 추가하려면, 전체 코드를 바꿔야하며, 항공 운송 등의 수요가 생기면 또 전체 코드를 수정해야 한다.
  - 위와 같은 상황이 거듭될수록 코드는 점점 복잡해지게 된다.



- 해결
  - 객체의 틀을 잡은 인터페이스를 정의한다.
  - 인터페이스에 따라 객체를 생성하기 위한 factory를 정의한다.

