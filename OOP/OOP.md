# 프로그래밍 패러다임

- 패러다임
  - 여기서 패러다임이란 프로그래밍 하는 방식을 의미한다.
  - 일반적으로 패러다임이란 무엇을 어떻게 해야 할지 보다 무엇을 해선 안되는지에 대해 이야기한다.



- 순차적 프로그래밍(Sequential Programming)
  - 순차적으로 실행되는 프로그래밍 방식
  - 코드가 위에서부터 아래로 실행되게 된다.
    - 따라서 자연스럽게 데이터의 처리도 위에서부터 아래로 흐르게 된다.
  - 현재까지도 모든 프로그래밍 언어는 위에서부터 아래로 실행되므로 패러다임이라고까지 할 순 없다.
  - GOTO문
    - GOTO는 위에서 아래로 흐르는 프로그램의 흐름을 제어하는 문이다.
    - 만일 아래에서 윗 부분의 코드를 다시 실행시키고자 할 경우 GOTO문을 통해 해당 코드로 이동시키게 된다. 
    - 프로그램의 규모가 커질수록 GOTO문도 많이 사용되었고 이는 프로그램의 복잡화를 불러왔다.



- 절차적 프로그래밍(Procedural Programming)
  - 프로시저(Procedure)를 활용하여 코드의 반복을 줄이는 프로그래밍 방식
    - 프로시저란 함수와 유사한 개념이다(요즘에는 함수와 구분하지 않고 사용한다).
    - 정확히는 함수에 속하는 개념이라 볼 수 있는데 반환값이 없고 실행이 주가 되는 함수를 의미한다.
  - 반복 될 가능성이 있는 코드(절차)를 재사용이 가능한 프로시저로 만든다.
    - 따라서 GOTO문을 사용하지 않아도 기존 코드의 재사용이 가능해졌다.
    - 하나의 큰 프로그램을 함수 단위로 쪼갠다고 하여 Top-Down 방식이라고도 한다.
  - 다익스트라가 최초로 고안했다.
    - 다익스트라 알고리즘을 고안한 사람이다.
    - [Go To Statement Considered Harmful] 라는 논문에서 GOTO문의 해로움을 주장하면서 프로시저 단위로 프로그래밍 할 것을 주장했다.
  - 구조적 프로그래밍(Structured Programming)
    - 절차적 프로그래밍이 보다 발전된 형태로, 유사한 프로시저들을 모아 모듈을 생성한다.
    - 모듈은 해석하기 나름이지만 일반적으로는 물리적인 소스코드 파일을 의미한다.
  - 한계
    - 프로시저는 추상적인 단위였고, 실제 물리적인 요소(변수나 상수 등)를 관리하는데는 그다지 관심이 없었다.
    - 즉, 데이터와 그 데이터를 처리하는 프로시저가 따로 존재하게 되고 이는 데이터와 데이터의 처리를 따로 관리해야한다는 문제를 야기했다.
    - 또한 데이터를 모두 전역으로 관리해야 했기에 전역 네임스페이스의 포화가 발생했다.



- 객체 지향 프로그래밍(Object-Oriented Programming)

  - 프로시저와 데이터가 따로 관리된다는 문제를 해결하기위해 그 둘을 한 곳에서 관리하기 위해 고안된 프로그래밍 패러다임
  - 프로시저와 데이터를 각기 메서드와 속성(attribute)라는 형태로 객체에 저장하고 객체 한 곳에서 관리한다.
  - 여러 개의 객체가 모여 하나의 프로그램을 형성하므로 Bottom-Up 방식이라고도 불린다.
  - 절차적 프로그래밍과의 차이
    - 예를들어 자판기에서 음료를 구입하는 과정을 절차 지향 프로그래밍으로 구현하면 다음과 같을 것이다.

  ```python
  # 절차 지향
  def insert_money():
      pass
  
  def check_money():
      pass
  
  def choice_beverage():
      pass
  
  def give_change_and_beverage():
      pass
  
  def take_change_and_beverage():
      pass
  
  menu = ['coke', 'splite', 'orange', ...]
  customer_money = input()
  beverage = input()
  
  insert_money()
  check_money()
  choice_beverage()
  give_change_and_beverage()
  take_change_and_beverage()
  
  
  # 객체 지향
  class VendingMachine:
      menu = ['coke', 'splite', 'orange', ...]
      
      def __init__(self, money):
          self.money = money
      
      def check_money():
          pass
      
      def give_change_and_beverage():
          pass
  
      
  class Customer:
      def __init__(self, money):
          self.money = money
          
      def insert_money():
          pass
      
      def choice_beverage():
          pass
      
      def take_change_and_beverage():
          pass
  ```






# Object Oriented Programming 개요

- OOP란
  - 프로그래밍 설계 패러다임 중 하나.
  - 정의
    - 컴퓨터 프로그래밍의 패러다임 중 하나이다. 객체 지향 프로그래밍은 컴퓨터 프로그램을 명령어의 목록으로 보는 시각에서 벗어나 여러 개의 독립된 단위, 즉 "객체"들의 모임으로 파악하고자 하는 것이다. 각각의 객체는 메시지를 주고받고, 데이터를 처리할 수 있다.  -_위키백과_
    - 즉 객체를 블럭으로 하여 프로그래밍을 블럭 조립하듯이 할 수 있게 된다.
  - 장점
    - 클래스의 상속 등을 통해 기존 코드의 재사용성이 높아진다.
    - 문제가 발생한 클래스 혹은 메서드만 수정해주면 되기 때문에 유지보수가 쉬워진다.
    - 클래스 단위로 모듈화 시켜서 개발할 수 있으므로 협업에 유리하다.
  - 단점
    - 설계시 많은 시간과 노력이 들어간다.



- 초기 OOP

  - 1967년 Alan Kay가 최초로 고안했다.
    - Alan Kay는 학부 때 생물학을 전공했다.
    - 세포들이 서로 상호작용 하는 방식을 소프트웨어 개발에도 적용할 수 있을 것이라 생각했다.
    - 세포들은 서로에게 message를 보내면서 상호작용하는데, 소프트웨어 개발에도 이를 적용하려 했다.
  - 초기 OOP의 핵심 개념은 data와 procedure라 불리는 data를 조작하는 로직을 하나로 묶어 객체를 만들고, 이 객체들은 서로 message를 통해 통신한다는 것이었다.
    - 상속, 다형성 등은 모두 나중에 등장한 개념이다.
    - Data와 procedure를 하나의 객체로 묶어 보다 편하게 관리할 수 있도록 하고, 객체 외부에서는 객체 내부의 data를 직접적으로 조작할 수 없게 하여 버그가 발생할 가능성을 낮추고, 객체 사이의 결합도를 낮추는 것이 최초의 목적이었다.
    - 객체와 객체 사이에는 message를 통해서만 통신을 함으로써 한 객체의 변경 사항이 다른 객체에는 영향을 미치지 않게 된다.

  - Alan Kay는 OOP에 대해 아래와 같이 말했다.

    > OOP to me means only **messaging**, **local retention and protection** and **hiding of state-process, and extreme late-binding** of all things.

    - Local retention and protection: data와 procedure를 하나의 객체로 묶어 외부에서 객체 내부의 data를 조작할 수 없게 한다.
    - Messaging: 만일 한 객체가 다른 객체의 data나 procedure가 필요하다면 오직 message를 보내서 요청해야하며, message를 받은 객체가 어떻게 처리할지는 message를 받은 객체에게 달려있다.
    - Hiding of state-process, and extreme late-binding: message를 보낸 객체는 message를 받은 객체가 어떻게 data를 처리하는지 알 필요가 없으며, message를 받는 객체는 달라질 수 있다.

  - Extream late-binding

    - Message를 보내는 객체와 받는 객체 사이의 binding을 의미한다.
    - Message를 보내는 객체는 compile time에 이미 결정되지만, 어떤 객체에 보낼지는 runtime에 동적으로 결정된다는 의미이다.
    - 이를 통해 보다 유연하게 코드를 작성할 수 있게 된다.

  - Alan Kay는 Dan Ingalls, Adele Goldberg 등과 함께 자신이 고안한 객체 지향의 개념을 담아 모든 것이 객체로 이루어진 Smalltalk이라는 언어를 만들었다.

  - Objec Oriented라는 용어에 대해

    - Alan Kay는 훗날 자신이 object라는 용어를 사용한 것을 후회한다는 말을 했다.
    - 자신이 고안한 개념에 object라는 개념을 붙임으로서 사람들이 사소한 개념들에 집중하게 만들었기 때문이다.
    - Alan Kay는 object oriented에서 정말로 집중해야 할 것은 객체 그 자체가 아니라 객체들이 상호작용하는 방식인 messaging이라고 말했다.





## OOP의 개념들

- 클래스, 객체 그리고 추상화(Abstraction)
  - **추상화**란 핵심적이고 특징적인 공통점들을 뽑아내는 과정을 말한다.
    - 프로그래밍에서의 추상화란 내가 개발하고자 하는 프로그램(핵심적)에서 공통적으로 필요한 것들을 뽑아내는 것이다.
  - 추상화를 통해 뽑아낸 핵심적인 공통점들을 속성(attribute)과 행위(method)로 묶은 것이 **클래스**이다.
  - 추상화된 클래스를 실체화한 것이 객체이다.
  - 예시
    - 노트북은 접을 수 있고 휴대가 가능하며 디스플레이, 키보드, 터치 패드가 존재한다고 추상화가 가능하다.
    - 노트북 클래스는 접히고, 휴대가 가능하다는 행위와 디스플레이, 키보드, 터치패드 등의 속성이 정의될 것이다.
    - 위와 같은 추상적인 개념을 바탕으로 맥북, 갤럭시북 등의 실체(객체)가 생성된다.



- 상속

  - 상위 클래스의 속성과 메서드를 하위 클래스에서 재정의 없이 물려 받아 사용하는 기법.
  - 코드의 재사용성을 높이고 유지 보수도 쉽게 해준다.
  - 예시
    - 어류라는 클래스를 상속 받는 광어, 우럭이라는 클래스가 있다고 가정.
    - 어류 클래스에 비늘, 아가미, 아가미 호흡 등이 정의되어 있다면 광어, 우럭에는 굳이 동일한 속성과 행동을 정의해줄 필요가 없다.
    - 또한 만일 어느날 모든 어류에게 비늘이 아닌 털이 나기 시작했다면 어류 클래스에서 비늘만 털로 변경해주면 된다.
  - 구체화(specialize)와 일반화(generalize)
    - 상속을 하고 상속을 받는 클래스 간에는 계층형 관계가 형성된다.
    - 아래 계층으로 내려갈수록 구체화되고, 위 계층으로 올라갈수록 일반화 된다.
    - 즉 아래 계층으로 내려갈 수록 각 클래스의 고유한 특징들이 강해지고, 일반화될 수록 더 많은 객체에게 영향을 주게 된다.

  - `is-a` 관계
    - 상속 관계가 성립되기 위해서는 부모 클래스와 자식 클래스 사이에 `is-a` 관계가 성립되어야 한다.
    - 즉 "자식 클래스는 부모 클래스이다."라는 명제가 참이어야 한다. 
  - `hsa-a` 관계
    - 상속에서 가장 흔히 하는 실수로 `has-a` 관계인 것을 상속하는 것이다.
    - `has-a`는 "부모 클래스는 자식 클래스를 가지고 있다"라는 관계를 상속시키는 것이다.
    - 예를 들어 어류 클래스를 상속 받아 아가미 클래스를 만드는 경우가 있을 수 있다.
    - 단순히 코드의 재사용만을 위해 이런 관계에 있는 두 클래스에 상속 관계를 형성하면 혼란이 발생할 수 있다.



- 다형성
  - 상황에 따라 다른 의미로 해석될 수 있는 특징을 말한다.
    - 즉 동일한 메서드나 속성이 상황에 따라 다르게 동작할 수 있는 특징이다.
  - 오버라이딩
    - Python을 비롯한 많은 언어에서 지원하는 오버라이딩은 다형성을 활용한 것이다.
    - 오버라이딩의 기본적인 개념은 자식 클래스에 부모 클래스에 정의된 메서드를 그대로 사용하지 않고 동일한 이름을 지닌 다른 역할을 하는 메서드를 정의하는 것이다.
    - 이렇게 하면 객체가 어떤 클래스에 의해 생성되었는지에 따라 동일한 이름을 가진 메서드라도 전혀 다르게 동작하게 된다.
  - 오버로딩
    - Java 등의 언어에서 지원하는 오버로딩도 다형성을 활용한 것이다(Python에서는 지원하지 않는다).
    - 오버라이딩이 메서드가 어떤 객체에 의해 호출되었는지에 따라 동작이 달라지는 것이라면, 오버로딩은 어떤 파라미터가 입력되었는지에 따라 동작이 달라지는 것이다.



- 캡슐화
  - 관련이 있는 속성과 메서드를 하나로 묶고 그것을 은닉하는 것을 의미한다.
    - 은닉이 필요한 이유는 내부적인 응집력은 높이고 외부와의 결합도는 낮추기 위해서이다.
    - 만일 객체 내부의 특정 변수를 객체 내부의 메서드가 아닌 다른 클래스로부터 생성된 객체의 메서드로 수정이 가능하다면 내부적인 응집력은 떨어지고 외부와의 결합도는 증가하게 된다.
    - 이럴 경우 유지보수가 힘들어진다.
  - 은닉을 위해 객체 지향 프로그래밍을 지원하는 언어들은 접근제한자라는 문법을 지원한다.
    - Python은 접근제한자 문법 자체를 제공하지는 않는다.



- 좋은 객체지향 설계의 5가지 원칙(SOLID)
  - SRP: 단일 책임 원칙(Single Responsibility Principle)
    - 하나의 클래스는 하나의 책임만 가져야 한다.
    - 하나의 책임이라는 것은 모호한 개념으로 클 수도, 작을 수도 있고, 문맥과 상황에 따라 다르다.
    - 중요한 기준은 변경이다. 변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 따른 것이다.
  - OCP: 개방-폐쇄 원칙(Open/Closed Principle)
    - 소프트웨어 요소는 확장에는 열려 있으나 변경에는 닫혀 있어야 한다. 
    - 즉, 아래에서 살펴볼 다형성을 잘 지키는 것이다.
    - 역할을 변경하지는 않되 다양한 구현을 만들어 확장하는 것이다.
    - 의존성 주입(DI)도 이 원칙을 유지하면서 변경을 하기 위해 사용하는 것이다.
  - LSP: 리스코프 치환 원칙(Liskov Substitution Principle)
    - 프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스를 바꿀 수 있어야 한다.
    - 다형성에서 하위 클래스(구현)은 인터페이스(역할) 규약을 다 지켜야 한다는 원칙이다.
    - 다형성을 지원하기 위한 원칙으로, 인터페이스를 믿고 사용하려면, 이 원칙이 필요하다.
    - 예를 들어 자동차라는 인터페이스에서 엑셀은 앞으로 가는 기능을 가지고 있다. 그러나 그 구현에서 엑셀에 뒤로 가게 구현한다면 이는 LSP 원칙을 위반한 것이다.
  - ISP: 인터페이스 분리 원칙(Interface Segregation Principle)
    - 특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다.
    - 예를 들어 자동차라는 범용 인터페이스에서 정비와 운전이라는 역할을 모두 수행하는 것 보다는 운전 인터페이스와 정비 인터페이스를 나누는 것이 더 낫다.
    - 이 원칙을 지키면 인터페이스가 명확해지고, 대체 가능성이 높아진다.
  - DIP: 의존관계 역전 원칙(Dependency Inversion Principle) 
    - 의존성 주입은 "프로그래머는 추상화에 의존해야지, 구체화에 의존하면 안된다." 는 원칙을 따르는 방법 중 하나다.
    - 즉 구현 클래스에 의존하지 말고, 인터페이스에 의존해야 한다는 뜻이다.



## 참조

- [[프로그래밍 패러다임\]순차적(비구조적),절차적(구조적),객체지향적 프로그래밍](https://kamang-it.tistory.com/entry/프로그래밍-패러다임순차적비구조적절차적구조적객체지향적-프로그래밍)

- https://gracefulprograming.tistory.com/130
- https://st-lab.tistory.com/151
- https://www.purl.org/stefan_ram/pub/doc_kay_oop_en
- https://medium.com/javascript-scene/the-forgotten-history-of-oop-88d71b9b2d9f
- https://velog.io/@eddy_song/alan-kay-OOP





# Dependency

- Dependency
  - Dependency의 사전적 정의는 아래와 같다.
    - 다른 것으로부터 영향을 받거나 결정되거나 종속되는 정도나 상태.
  - Dependency의 사전적 정의를 기반으로, software 개발에서 dependency는 아래와 같이 정의할 수 있다.
    - 두 component 사이의 dependency는 한 component의 변경이 다른 component에 영향을 줄 수 있는 가능성을 의미한다.
    - 즉 한 component가 다른 component를 강하게 의존한 다는 것은 한 component의 변경사항이 다른 component에도 강한 영향을 미칠 가능성이 높다는 것이다.
  - Coupling
    - Component들 간의 결합(coupling)은 의존성의 정도를 정확히 측정한다.
    - 강하게 결합된 component들은 높은 의존성을 가지고 있으며, 약하게 결합된 component들은 낮은 의존성을 가지고 있다.
    - Software 개발에서 절대적 진리로 여겨지는 개념 중하나는 component들을 약하게 결합해야한다는 것이다.
    - Component들이 강하게 결합될수록 한 component의 변경 사항이 다른 component에 영향을 미칠 가능성(의존성)이 높아지므로 개발 비용이 증가하게 된다.



- OOP와 dependency

  - OOP에서 위에서 말한 component라는 개념은 보통 type으로 정의된다.
    - 기본적으로 우리는 type들 사이의 의존성에 주의를 기울여야한다.
  - Class 사이의 관계(dependency)는 아래와 같은 방식으로 맺어지며, 아래로 갈수록 강하게 맺어진 관계이다.
    - Dependency
    - Association(Aggregation, Composition)
    - Inheritance
  - Dependency
    - 한 class의 object가 다른 class의 object와 짧은 시간 동안 함께 작업을 수행할 경우 dependency라 부른다.
    - 예를 들어 아래와 같은 경우가 dependency의 예시이다.
    - A의 object를 인자로 받아 해당 object를 사용하거나, A의 object를 반환하는 경우 등을 의미한다.
    - B는 A의 interface만 알면 되며, A의 interface(foo method)가 변경되지 않는 한, A가 변경되어도 B는 변경되지 않아도 된다.

  ```python
  class A:
      def foo(self):
          pass
      
  class B:
      def work_with_A(self, a: A):
          a.foo()
          
      def return_A(self) => A:
          return A()
  ```

  - Association(Aggregation과 Composition)
    - 한 class의 object가 다른 class의 object와 장기간 함께 작업을 수행할 경우 association이라 부른다.
    - 한 class가 다른 class의 object에 대한 reference를 attribute로 가지고 있으면 associtaion이라 볼 수 있다.
    - 예를 들어 아래와 같은 경우는 association이라 볼 수 있다.
    - 이전에는 오직 `work_with_A` method가 호출 될 때만 A와 관계를 유지했지만, 이제는 B의 object가 생성될 때부터 사라질 때 까지 관계를 유지하게 된다.
    - Aggregation은 association의 특수한 형태이며, composition은 aggregation의 특수한 형태이다.
    - UML diagram을 그려야 하는 것이 아니라면, 이들을 구분하기 보다는 한 객체가 다른 객체를 가지고 있다(A has B)는 개념으로 이해하면 된다.
    - Aggregation의 애매한 개념으로 인해 개발자들 사이에서도 association, aggregation, composition의 구분에 대한 갑론을박이 있었고, UML 2.0부터는 aggregation을 삭제했다.

  ```python
  class A:
      pass
  
  class B:
      def __init__(self, a:A):
          self.a = a
          
  class C:
      def __ini__(self):
          self.a = A()
  ```

  - Inheritance
    - 한 class가 다른 class를 상속하는 것을 inheritance라 부른다.

  ```python
  class A:
      pass
  
  class B(A):
      pass
  ```



- Dependency Injection

  - 객체의 외부에서 instance를 생성한 후 이를 객체에 전달해서 의존성을 해결하는 방법이다.
    - 이를 통해 결합도를 낮추고 응집도를 높일 수 있다.
  - 예를 들어 아래 코드를 보자
    - 아래에서 dependency에 해당하는 부분은 모두 주석으로 표기를 해놨다.

  ```python
  import os
  
  
  class ApiClient:
  
      def __init__(self) -> None:
          self.api_key = os.getenv("API_KEY")  # dependency
          self.timeout = int(os.getenv("TIMEOUT"))  # dependency
  
  
  class Service:
  
      def __init__(self) -> None:
          self.api_client = ApiClient()  # dependency
  
  
  def main() -> None:
      service = Service()  # dependency
      ...
  
  
  if __name__ == "__main__":
      main()
  ```

  - 아래는 의존성을 주입하도록 변경한 code이다.

  ```python
  import os
  
  
  class ApiClient:
  
      def __init__(self, api_key: str, timeout: int) -> None:
          self.api_key = api_key  # dependency is injected
          self.timeout = timeout  # dependency is injected
  
  
  class Service:
  
      def __init__(self, api_client: ApiClient) -> None:
          self.api_client = api_client  # dependency is injected
  
  
  def main(service: Service) -> None:  # dependency is injected
      ...
  
  
  if __name__ == "__main__":
      main(service=Service(
          api_client=ApiClient(
                  api_key=os.getenv("API_KEY"),
                  timeout=int(os.getenv("TIMEOUT"))
              )
          )
      )
  ```







## 참조

https://blog.rcard.in/programming/oop/software-engineering/2017/04/10/dependency-dot.html

https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html