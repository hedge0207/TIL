# 클래스

- 파이썬은 객체 지향 언어다.
  - 모든 것이 객체로 이루어져 있다.



- 클래스는 왜 필요한가

  - 함수로 더하기를 처리하여 그 결과값을 여러 변수에 저장하는 프로그램을 구현하는 상황을 가정해보자
  - 아래와 같이 변수의 수가 늘어날 수록 동일한 작업을 수행하는 함수의 수도 그에 맟줘 증가해야 한다.
  - 이는 굉장히 비효율적으로 객체를 사용하면 이러한 비효율을 해결 가능하다.

  ```python
  result1 = 0
  result2 = 0
  
  def plus1(a,b):
      global result1
      result1 = a+b
  
  def plus2(a,b):
      global result2
      result2 = a+b
  ```



- 클래스와 객체
  - 클래스: 데이터와 일정한 작업을 함께 묶어 놓은 것.
    - attribute와 method를 갖는 논리적인 단위.
    - method도 엄밀히 말하면 callable한 attribute이다.
  - 클래스와 객체는 과자틀과 과자틀에서 나온 과자의 관계와 같다.
    - 클래스가 과자틀이라면 객체는 그 과자틀로 만든 과자이다.
  - 객체와 인스턴스
    - 객체와 인스턴스는 동일한 말 처럼 보이지만 엄밀히 말하면 다르다.
    - 인스턴스란 특정 객체가 어떤 클래스의 객체인지를 관계 위주로 사용할 때 사용한다.
    - 즉, "a는 A 클래스의 인스턴스"라는 말이 "a는 A 클래스의 객체"라는 말보다 자연스럽고
    - "a는 객체"라는 말이 "a는 인스턴스"라는 말보다 자연스럽다.



- 클래스 사용하기

  - 클래스가 왜 필요한지 알아봤던 예시를 바탕으로 클래스를 사용하는 방법을 살펴본다.
  - 클래스와 인스턴스 생성

  ```python
  # 클래스 생성
  class Plus:
      pass
  
  # FourCal 클래스의 인스턴스 생성
  obj = Plus()
  print(type(obj))  # <class '__main__.Plus'>
  ```

  - 클래스에 작업(함수) 추가하기
    - 클래스 내부에 생성된 함수는 일반 함수와 구분하기 위해 메서드라고 부른다.
    - 일반 함수와 달리 메서드는 첫 번째 매개변수로 `self`를 받는다(`self`말고 다른 이름으로 해도 무관하지만 `self`로 하는 것이 관례다).
    - `self`에는 메서드를 호출한 인스턴스를 자동으로 받는다.
    - 메서드는 클래스가 아닌 인스턴스를 통해 호출한다.
  
  ```python
  # 메서드 생성
  class Plus:
      def set_data(self,first,second):  # 첫 번째 매개변수로 `self`를 받는다. 즉 아래 실행문은 다음과 같이 객체 변수를 변경한다.
          self.first = first			  # obj.first = first
          self.second = second		  # obj.second = second
          
  # 메서드 호출 방법 1.
  # 첫 번째 매개변수인 self에는 obj가 자동으로 넘어간다.
  obj = Plus()
  obj.set_data(2,3)
  print(obj.first)  # 2
  
  
  # 메서드 호출 방법 2.아래와 같이 클래스를 통해 메서드를 호출할 때는 첫 번째 인자로 인스턴스를 반드시 넘겨줘야 한다.
  obj = Plus()
  Plus.set_data(a,2,3)
  ```
  
  - 객체들 간의 변수 공유
    - 객체에 생성되는 객체만의 변수를 객체변수라 한다.
    - 같은 클래스로 생성했어도 서로 다른 객체들은 객체 변수를 공유하지 않는다.
  
  ```python
  # 메서드 생성
  class Plus:
      def set_data(self,first,second):
          self.first = first
          self.second = second
          
  
  obj1 = Plus()
  obj1.set_data(2,3)
  obj2 = Plus()
  obj2.set_data(4,5)
  
  # 둘의 id 값이 다른 것을 확인 가능하다.
  print(id(obj1.first))	# 1647180802384
  print(id(obj2.first))	# 1647180802448
  ```
  
  - 원하는 작업 추가하기
  
  ```python
  class Plus:
      def set_data(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  obj = Plus()
  obj.set_data(2,3)
  print(obj.add())  # 5
  ```



- 생성자

  - 위 예시에서는 `set_data`메서드를 활용하여 객체 변수를 설정하였다.
  - 객체에 초기값을 설정해야 할 필요가 있을 때는 메서드를 사용하는 방법 보다 `__init__` 메서드를 사용하는 것이 낫다.
    - `__init__` 메서드는 Python이 인스턴스를 생성할 때 내부적으로 사용하는 메서드이다.
    - 이 메서드를 오버라이딩해서 사용하는 것이다.

  ```python
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
  # 생성자는 first, second라는 두 개의 매개변수를 받으므로 생성할 때부터 인자를 넘겨줘야 한다.
  obj = Plus(2,3)
  print(obj.first, obj.second)	# 2 3
  ```



- 클래스 변수와 인스턴스 변수

  - 클래스 변수와 인스턴스 변수를 합쳐서 data member라 부른다.

  - 클래스 변수
    - 클래스 정의에서 메서드 밖에 존재하는 변수를 클래스 변수라 부른다.
    - 클래스로 만든 모든 인스턴스가 공유하는 변수이다.
    - `class명.클래스변수`의 형태로 클래스 내외부에서 접근이 가능하다.
    - `인스턴스명.클래스변수`의 형태로도 접근이 가능한데, 먼저 인스턴스 변수가 존재하는지 찾은 후 없으면 클래스 변수 중에 해당 변수가 있는지 확인한다.

  ```python
  class BlueClub:
      gender = "male"
  
  print(BlueClub.gender)	# male
  bc1 = BlueClub()
  bc2 = BlueClub()
  print(bc1.gender)	# male
  print(bc2.gender)	# male
  
  # 변경할 경우 모든 인스턴스의 클래스 변수도 함께 변경된다.
  BlueClub.gender = "female"
  print(bc1.gender)	# female
  print(bc2.gender)	# female
  ```

  - 인스턴스 변수
    - 각 인스턴스가 독립적으로 관리하는 변수이다.
    - 클래스 내부에서는 `self.변수명`, 외부에서는 `인스턴스명.변수명` 형태로 접근한다.
    - 단, 해당 변수가 생성된 적 있어야 한다(즉, 해당 인스턴스 변수를 선언하는 메서드가 호출된 적 있어야 한다).
    - 따라서 일반적으로 생성자 함수에 선언한다.
  
  ```python
  class MyClass:
      def my_method(self):
          self.foo = 'foo'
  
   
  my_instance = MyClass()
  print(my_instance.foo)		# AttributeError
  
  # 인스턴스 변수를 생성할 수 있도록 my_method 메서드를 실행.
  my_instance.my_method()
  print(my_instance.foo)		# foo
  ```
  
  - 클래스 변수 사용시 주의사항
    - 클래스 변수에 접근할 때는 특별히 이유가 없다면 `인스턴스.클래스변수` 나 `self.클래스변수`와 같이 접근하는 것은 피해야한다. 
    - python에는 인스턴스 변수를 인스턴스 객체로부터 생성하는 것이 가능하므로 의도치 않게 클래스 변수를 인스턴스 변수로 은폐해버리는 경우가 있다.
  - `self`를 통해 변수를 찾는 과정은 다음과 같다.
    - 인스턴스 변수를 먼저 찾는다.
    - 만일 인스턴스 변수가 존재하지 않는다면 클래스 변수를 찾는다.
    - 만일 클래스 변수가 존재하지 않는다면 부모 클래스에서 찾는다.



- private attribute 사용하기

  - Python에는 접근제어자가 존재하지 않는다.
    - 접근제어자: 외부에서 변수, 함수, 클래스 등에 어떤 방식으로 접근을 허용할지를 결정하는 역할을 한다.
    - Java와 같은 언어의 경우에는 public, private 등의 접근제어자가 존재한다.
    - Python에는 접근제어자가 존재하지 않으므로 기본적으로 모두 public 상태이다.
  - 그러나 naming을 통해 private으로 설정할 수 있다.
    - 이름 앞에 언더바 2개(`__`)를 붙이면 private이 되어 외부에서 접근이 불가능해진다.
    - 이름 앞에 언더바 1개(`_`)를 붙이는 것은 해당 변수 혹은 함수는 외부에서는 사용하지 않는다는 의미인데 문법적인 제약은 없다.
    - 아래 예시에는 나오지 않았지만 메서드 역시 마찬가지로 메서드명 앞에 언더바 2개를 붙이면 외부에서는 호출이 불가능하다.

  ```python
  class MyClass:
      def __init__(self):
          self.foo = "foo"
          self._bar = "bar"	# 내부에서만 사용하겠다는 의미이지만 문법적은 제약은 없다.
          self.__baz = "baz"
      
      def echo(self):
          print(self.foo)		# foo
          print(self._bar)	# bar
          print(self.__baz)	# baz
  
  my_instance = MyClass()
  my_instance.echo()			# 클래스 내부의 echo 메서드에서는 접근 가능
  
  # 외부에서는 접근 불가능
  print(my_instance.foo)		# foo
  print(my_instance._bar)		# bar
  print(my_instance.__baz)	# AttributeError
  ```



- 정적 매서드와 클래스 메서드

  - 정적 매서드와 클래스 메서드는 인스턴스를 통하지 않고 클래스에서 바로 호출이 가능하다.
  - 정적 메서드
    - class와 독립적이지만 로직상 클래스 내에 포함되는 메서드에 사용한다.
    - `self`를 인자로 받지 않는다.
    - `@staticmethod` 데코레이터를 통해 정적 메서드임을 표시한다.
    - 클래스 내부 뿐 아니라 외부에서도 호출이 가능하다.

  ```python
  class Email:
      def __init__(self):
          self.name = "theo"
          self.gender = "male"
          self.content = "I hope you ~"
      
      def read_email(self):
          # class를 통해 호출한다.
          salutation = Email.create_salutation(self.name, self.gender)
          print(salutation, self.content)
          
      
      # 인사말을 추가하는 것은 인스턴스에 의해 직접 호출되지 않으므로 class와 독립적이라고 볼 수 있지만 로직상 클래스 내에 포함된다.
      # decorator를 추가한다.
      @staticmethod
      def create_salutation(name, gender):	# self를 인자로 받지 않는다.
          if gender=="male":
              salutation = f"Dear Mr.{name} How are you?"
          else:
              salutation = f"Dear Ms.{name} How are you?"
  
          return salutation
  
  
  email = Email()
  email.read_email()
  ```

  - 클래스 메서드
    - 첫 번째 인자로 `cls`를 받는데, 이는 클래스를 의미한다(다른 이름으로 해도 되지만 관례상 cls로 작성한다).
    - `@classmethod` 데코레이터를 통해 클래스 메서드임을 표시한다.
    - 정적 메서드와 유사하지만 클래스 메서드는 클래스 변수에 접근이 가능하다는 점이 다르다.

  ```python
  class Email:
      end = "Yours Sincerely"
  
      def __init__(self):
          self.name = "theo"
          self.gender = "male"
          self.content = " I hope you ~ "
      
      def read_email(self):
          salutation = Email.create_salutation(self.name, self.gender)
          full_email = Email.add_end(salutation+self.content)
          print(full_email)
          
      
      @staticmethod
      def create_salutation(name, gender):
          if gender=="male":
              salutation = f"Dear Mr.{name} How are you?"
          else:
              salutation = f"Dear Ms.{name} How are you?"
  
          return salutation
      
      # 데코레이터를 통해 클래스 메서드라는 것을 표현한다.
      @classmethod
      def add_end(cls, content):	# 첫 번째 인자로 cls를 받는다.
          return content+cls.end	# 클래스 변수에 접근이 가능하다.
  
  
  
  email = Email()
  email.read_email()
  ```



- `__new__`, `__init__`, `__call__`
  - 인스턴스의 생성에 관여하는 스페셜 메서드들이다.
  - 아래 순서대로 실행이 이루어진다.
    - `__new__`: 클래스의 인스턴스가 생성될 때 해당 인스턴스를 위한 메모리를 할당한다.
    - `__init__`: 생성된 인스턴스를 초기화한다.
    - `__call__`: 생성된 인스턴스가 호출될 때 실행된다.



- 생성자(constructor)는 무엇인가?
  - 사람에따라 누군가는 `__new__`가 생성자라하고, 누군가는`__init__`이 생성자라 하는데 이런 의견차이가 생긴 원인은 바로 Python에 다른 언어(C 계열 언어 및 Java 등)에서의 생성자와 정확히 일치하는 역할을 하는 개념이 없기 때문이다.
    - 일반적인 의미(다른 언어에서 사용되는 의미)의 생성자는 **객체를 생성하고 초기화**하는 역할을 하는 것을 의미한다.
    - 그런데 Python의 경우 정확히 이런 역할을 하는 메서드가 존재하지 않는다.
  - `__new__` 는 생성된 인스턴스를 반환하기는 하지만 인스턴스를 위한 메모리를 할당하는 것이므로 생성이라 보기 어려우며 초기화 역할을 하지도 않는다.
  - `__init__`은 초기화 역할만을 담당한다.
  - 일반적으로 생성자의 두 가지 역할 중 객체의 초기화에 방점이 찍히게 되는데, 이런 관점에서 보면 `__init__`이 그나마 생성자에 가깝긴 하다.
    - Python 공식 문서에서도 `__init__`을 constructor라고 표현한다.



- object의 attribute 조작

  - 아래 4가지 함수를 통해 object의 attribute들을 조작 가능하다.
    - `getattr(object, attribute)`: `object`의 `atttirbute`를 반환한다(없을 경우 `AttributeError` 발생).
    - `hasattr(object, attribute)`: `object`에 해당 `attribute`가 있는지 여부를 bool 값으로 반환한다.
    - `setattr(object, attribute, value)`: `object`의 `attribute`를 `value`로 변경한다.
    - `delattr(object, attribute)`: `object`의 `attribute`를 삭제한다.
  - 예시

  ```python
  class MyClass:
      class_val = "Hello"
  
      def __init__(self, arg):
          self.instance_val = arg
      
      def foo(self):
          print(self.class_val, self.instance_val)
  
  my_instance = MyClass(1)
  
  # hasattr
  print(hasattr(my_instance, "class_val"))		# True
  print(hasattr(my_instance, "instance_val"))	# True
  print(hasattr(my_instance, "foo"))			# True
  print(hasattr(my_instance, "bar"))			# False
  
  # getattr
  print(getattr(my_instance, "class_val"))		# Hello
  print(getattr(my_instance, "ssalc_lav"))		# AttributeError
  
  # setattr
  setattr(my_instance, "class_val", "Bye")
  print(getattr(my_instance, "class_val"))		# Bye
  
  # delattr
  # delattr로 클래스 변수 및 메서드를 삭제하려면 class를 첫 번째 인자로 넣어야 한다.
  # class 자체도 하나의 object이므로 인자로 넘길 수 있다.
  delattr(first_instance, "instance_val")			
  print(hasattr(first_instance, "instance_val"))	# False
  delattr(MyClass, "foo")
  print(hasattr(first_instance, "foo"))			# False
  ```



- `__getattr__`, `__getattribute__`

  - `__getattr__`
    - 인스턴스에서 어떤 attribute를 호출할 때 해당 attribute가 없을 경우 호출된다.
    - 가장 후순위로 호출된다.
    - parameter로 해당 attribute를 받는다.

  - `__getattr__` 예시

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattr__(self, attr):
          print("__getattr__")
      
      def foo(self):
          print("FOO!")
  
  
  my_inst = MyClass('theo')
  my_inst.name
  my_inst.age		# 없을 때만 호출된다.
  ```

  - 없는 메서드를 호출할 경우
    - `bar()`는 없는 attribute(method)이므로 호출시에 `__getattr__`이 호출된다.
    - `__getattr__`은 아무 것도 return하지 않으므로 None을 return하게 되고, 결국 `bar()`는 `None()`이 되어 `TypeError`가 발생한다.

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattr__(self, attr):
          print("__getattr__")
          print(attr)
      
      def foo(self):
          print("FOO!")
  
  
  my_inst = MyClass('theo')
  my_inst.bar()	# TypeError: 'NoneType' object is not callable
  ```

  - 활용
    - attribute를 동적으로 생성하는데 활용이 가능하다.
    - 아래 `say_name`과 같이 원래 정의되지 않은 메서드를 동적으로 생성하는 것이 가능하다.

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattr__(self, attr):
          return lambda *args, **kwargs: print('name:', args[0], 'age:', kwargs['age'])
  
  my_inst = MyClass('theo')
  my_inst.say_name('theo', age=20)
  ```

  - `__getattribute__`
    - 인스턴스에서 어떤 attribute를 호출하든 먼저 호출된다.
    - 가장 선순위로 호출된다.
    - parameter로 해당 attribute를 받는다.
  - `__getattribute__` 예시

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattribute__(self, attr):
          print("__getattribute__")
      
      def foo(self):
          print("FOO!")
  
  
  my_inst = MyClass('theo')
  my_inst.name	# 있든 없든 호출된다.
  my_inst.age
  ```

  - 이미 존재하는 메서드를 호출할 경우
    - `__getattribute__`은 해당 attribute가 있던 없던 무조건 호출된다.
    - 따라서 `my_inst.name`가 호출될 때 `__getattribute__`가 호출되고, `__getattribute__`는 return값이 없으므로 None을 return한다.
    - 따라서 `my_inst.name`은 None이 된다.
    - `my_inst.foo()` 역시 마찬가지 이유로 `my_inst.None()`가 되어 `TypeError`가 발생한다.

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattribute__(self, attr):
          print("__getattribute__")
      
      def foo(self):
          print("FOO!")
  
  
  my_inst = MyClass('theo')
  print(my_inst.name)	# None
  my_inst.foo()	    # TypeError: 'NoneType' object is not callable
  ```

  - 해결법

  ```python
  class MyClass:
      def __init__(self, name):
          self.name = name
  
      def __getattribute__(self, attr):
          return super().__getattribute__(attr)
      
      def foo(self):
          print("FOO!")
  
  
  my_inst = MyClass('theo')
  print(my_inst.name)	# name
  my_inst.foo()	    # FOO!
  ```







##  상속

- 클래스의 상속

  - 어떤 클래스를 만들 때 다른 클래스의 기능을 물려 받는 것을 클래스의 상속이라 한다.
    - 기능을 물려주는 클래스를 기반 클래스(base class), 상속을 받아 새롭게 만드는 클래스를 파생 클래스(derived class)라 한다.
    - 보통 기반 클래스는 부모 클래스, 슈퍼 클래스라 부르고, 파생 클래스는 자식 클래스, 서브 클래스라고도 부른다.
  - 기존 클래스가 라이브러리 형태로 제공되거나 수정이 허용되지 않는 상황에서 상속은 유용하게 쓸 수 있다.
  - 위에서 만든 `Plus` 클래스를 상속한 후 뺄셈 기능을 추가하여 PlusMunis 클래스를 만들면 다음과 같이 만들 수 있다.

  ```python
  # 부모 클래스
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  # 아래와 같이 부모 클래스를 괄호 안에 넣으면 된다.
  class PlusMinus(Plus):
      def mul(self):
          return self.first-self.second
  
  # 부모 클래스의 생성자와
  pm = PlusMinus(5,4)
  # 메서드를 사용 가능하다.
  print(pm.add())		# 9
  print(pm.mul())		# 1
  ```

  - `issubclass` 함수를 통해 특정 클래스와 상속 관계에 있는 클래스인지 확인이 가능하다.
    - 첫 번째 인자로 자식 클래스, 두 번째 인자로 부모 클래스를 받는다.

  ```python
  class Person:
      pass
  
  
  class Programmer(Person):
      pass
  
  print(issubclass(Programmer, Person))	# True
  ```
  
  - 사실 Pyhon의 모든 클래스는 모든 클래스의 조상 클래스인 `object` 클래스를 상속받는다.
    - Python 3 이전 버전의 경우 모든 클래스를 정의할 때 `object`를 상속한다는 것을 명시적으로 표시해줘야 했다.
    - 그러나 Python 3 이후부터는 아무 것도 상속받지 않을 경우 자동으로 `object`를 상속 받도록 변경되었다.
  
  ```python
  # 아래 두 클래스는 완전히 동일하다.
  
  class Person:
      pass
  
  
  class Person(object):
  	pass




- 부모 클래스의 인스턴스 변수에 접근하기

  - 당연하게도 접근하려는 인스턴스 변수가 생성되어야 접근이 가능하다.
    - 아래 코드의 경우 Person의 `__init__` 메서드가 실행되지 않으므로 클래스 초기화가 발생하지 않아 `name`이라는 인스턴스 변수도 생성되지 않고, 따라서 접근이 불가능하다.

  ```python
  class Person:
      def __init__(self, name):
          print("Person __init__")
          self.name = name
          
          
  class Programer(Person):
      def __init__(self, part):
          print("Programmer __init__")
          self.part = part
  
  
  programmer = Programer('server')
  print(programmer.part)	# server
  print(programmer.name)	# AttributeError
  ```

  - `super()`를 통해 부모 클래스의 특정 메서드를 실행시킬 수 있다.

  ```python
  class Person:
      def __init__(self, name):
          print("Person __init__")
          self.name = name
          
          
  class Programer(Person):
      def __init__(self, name, part):
          print("Programmer __init__")
          super().__init__(name)		# super(Programer, self).__init__()와 동일한 코드
          self.part = part
  
  
  programmer = Programer('theo', 'server')
  print(programmer.part)		# server
  print(programmer.name)		# theo
  ```

  - 자식 클래스의 인스턴스가 인스턴스 변수를 찾는 과정
    - 자식 클래스에 해당 인스턴스 변수가 있으면, 해당 인스턴스 변수를 사용.
    - 자식 클래스에 해당 인스턴스 변수가 없으면, 부모 클래스의 인스턴스 변수를 탐색.
    - 부모 클래스에 해당 인스턴스 변수가 있으면, 해당 인스턴스 변수를 사용.
    - 부모 클래스에도 없을 경우 `AttributeError`
  - 자식 클래스에 `__init__` 메서드를 지정해주지 않을 경우, 자식 클래스가 생성될 때 부모 클래스의 `__init__`이 실행된다.
    - 따라서 부모 클래스의 인스턴스 변수에 바로 접근이 가능하다.

  ```python
  class Person:
      def __init__(self, name):
          print("Person __init__")
          self.name = name
          
          
  class Programer(Person):
      pass
  
  
  programmer = Programer('theo')
  print(programmer.name)
  ```

  - 단순히 부모 클래스의 `__init__`메서드의 호출 여부가 중요한 것이 아니다.
    - 아래와 같이 개별적으로 실행시킬 경우에도 부모 클래스의 인스턴스 변수에도 접근이 불가능하다.

  ```python
  class Person:
      def __init__(self, name):
          print("Person __init__")
          self.name = name
          
          
  class Programer(Person):
      def __init__(self, part):
          print("Programmer __init__")
          self.part = part
  
  
  Person('theo')
  programmer = Programer('server')
  print(programmer.name)	# AttributeError
  ```



- 메서드 오버라이딩

  - 부모 클래스의 메서드를 동일한 이름으로 다시 만드는 것을 메서드 오버라이딩이라 한다.
    - 부모 클래스의 메서드를 재정의해서 사용하는 것이다.
    - 코드의 가독성을 높이기 위해서 사용한다.
    - Java의 경우 메서드 이름, 매개변수, 반환값의 타입까지 동일해야 하지만 Python은 이름만 동일하면 된다.
  - 이렇게 하면 상속을 받은 클래스의 메서드가 실행된다.

  ```python
  class Person:
      def __init__(self, name):
          self.name = name
      
      def greeting(self):
          print("Hello My name is {}".format(self.name))
          
          
  class Programer(Person):
      def __init__(self, part):
          self.part = part
  
      def greeting(self):
          print("Hello I'm {} programmer".format(self.part))
  
  
  programmer = Programer('server')
  programmer.greeting()
  ```




- 메서드 오버로딩
  - Python은 자체적으로는 메서드 오버로딩을 지원하지는 않는다.
  - 관련 라이브러리를 사용하면 구현은 가능하다.



- 다중 상속

  - 둘 이상의 부모 클래스로부터 상속을 받을 수 있다.
    - 상속 받을 클래스들의 이름을 콤마로 구분해서 입력한다.

  ```python
  class Person:
      def greeting(self):
          print("Hello!")
          
  
  class Company:
      def work(self):
          print("work hard")
  
          
  class Programer(Person, Company):
      def coding(self):
          print('coding')
      
  
  
  programmer = Programer()
  programmer.greeting()
  programmer.work()
  programmer.coding()
  ```

  - 다이아몬드 상속
    - Husband와 Wife는 Person을 상속 받고, Child는 Husband와 Wife를 상속 받는다.
    - 이를 그림으로 표현하면 트럼프 카드의 다이아 모양이 되는데, 이런 상속 관계를 다이아몬드 상속이라 부른다.
    - 명확하지 않고 애매한 코드가 되므로 죽음의 다이아몬드라고도 불린다.
    - 예를 들어 아래 코드에서 `greeting` 메서드를 호출했을 때 어떤 `greeting` 메서드가 호출될지가 애매해진다.

  ```python
  class Person:
      def greeting(self):
          print("Hello!")
          
  
  class Husband(Person):
      def greeting(self):
          print("Huband")
  
          
  class Wife(Person):
      def greeting(self):
          print("Wife")
  
  class Child(Husband, Wife):
      pass
  
  
  child = Child()
  child.greeting()
  ```

  - 메서드 탐색 순서
    - 위 예시의 경우 `Husband` 클래스의 `greeting` 메서드가 호출되는데 이는 `Child`의 상속 관계를 정의할 때 `Husband`를 먼저 입력했기 때문이다.
    - `mro` 메서드를 통해 탐색 순서를 확인이 가능하다.

  ```python
  class Person:
      def greeting(self):
          print("Hello!")
          
  
  class Husband(Person):
      def greeting(self):
          print("Huband")
  
          
  class Wife(Person):
      def greeting(self):
          print("Wife")
  
  class Child(Husband, Wife):
      pass
  
  
  Child.mro()
  # [<class '__main__.Child'>, <class '__main__.Husband'>, <class '__main__.Wife'>, <class '__main__.Person'>, <class 'object'>]
  ```



- 추상 클래스

  - 미구현 추상 메서드의 목록만을 가진 클래스
    - 추상 클래스를 상속 받는 클래스에서 메서드 구현을 강제하기 위해 사용한다.
    - 추상 클래스를 상속 받은 자식 클래스에 추상 클래스에 정의된 추상 메서드가 정의되지 않았다면, 자식 클래스의 객체 생성시 에러가 발생한다. 
    - 추상 클래스는 인스턴스를 생성할 수 없다.
  - `abc` 모듈을 불러와서 사용해야 한다.
    - abstract base class의 약자이다.
  - 추상 클래스 생성하기

  ```python
  # abc 모듈을 불러온다.
  from abc import *
  
  
  # metaclass에 ABCMeta를 입력한다.
  class AbstractClass(metaclass=ABCMeta):
      # 데코레이터를 통해 추상 메서드를 생성한다.
      @abstractmethod
      def foo():
          pass
  ```

  - 자식 클래스에 추상 메서드를 구현하지 않을 경우
    - Hello!까지는 출력이 되지만 인스턴스를 생성할 때 에러가 발생한다.

  ```python
  from abc import *
  
  
  class AbstractClass(metaclass=ABCMeta):
      @abstractmethod
      def foo():
          pass
  
  
  class MyClass(AbstractClass):
      pass
  
  print("Hello!")		# Hello!
  my_inst = MyClass()	# TypeError
  ```



## 메타클래스

> https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python?rq=1

- Python의 class

  - 대부분의 언어에서 class는 어떻게 객체를 생성할지에 대해 정의하는 코드 조각일 뿐이다.
    - 물론 Python에서도 어떻게 객체를 생성할지 정의하는 역할을 한다.
  - 그러나 Python의 클래스는 객체이기도 하다.
    - `class` 키워드를 사용할 때 Python은 객체를 만들어낸다.
    - 즉 Python에서의 class는 객체를 생성하는 객체인 셈이다.
    - 아래 코드가 실행될 때 메모리에 `ObjectCreator`라는 이름의 객체를 생성한다.

  ```python
  class ObjectCreator:
      pass
  ```

  - 따라서 Python의 class는 아래와 같은 특징을 지닌다.
    - 변수에 할당이 가능하다.
    - 복사가 가능하다.
    - 새로운 속성을 추가할 수 있다.
    - 함수의 인자로 넘길 수 있다.



- `type` 함수로 class를 동적으로 생성하기

  - 정적인 class 생성
    - 일반적으로 class는 아래와 같이 정적으로 생성한다.

  ```python
  class MyClass:
      pass
  ```

  -  동적으로 생성하기
     - `type`  함수는 일반적으로 객체의 type을 알아내기 위해 사용한다.
     - `type` 함수는 class를 만들 때도 사용이 가능하다.

  ```python
  # 기본형
  # 모두 required이며, 상속 받을 클래스나 attributes가 없을 경우 각기 빈 튜플과 빈 딕셔너리를 넣어줘야 한다.
  type(<클래스명>, <상속 받을 클래스들(tuple)>, <attributes(dict)>)
  
  # 예시
  type('MyClass', (), {})
  ```



- Metaclass

  - class를 만드는 class라고 할 수 있다.
    - Python에서 class는 객체이므로 이 객체를 생성하는 class 역시 존재하는데, 이것이 바로 metaclass이다.
  - `type`
    - 위에서 `type` 함수를 활용하여 class를 생성했는데, 이것이 가능했던 이유는 `type`이 metaclass이기 때문이다.
    - 아래와 같이 모든 class의 class는 type이다.

  ```python
  class MyClass:
      pass
  
  # int class의 instance
  some_int = 1
  # str class의 instance
  some_str = 'hello'
  print(some_int.__class__.__class__)		# <class 'type'>
  print(type(type(some_int)))				# <class 'type'>
  print(some_str.__class__.__class__)		# <class 'type'>
  print(type(type(some_str)))				# <class 'type'>
  print(MyClass.__class__)				# <class 'type'>
  print(type(MyClass))					# <class 'type'>
  ```



- `type`이외의 metaclass를 직접 정의해 주는 것도 가능하다.

  - Python이 metaclass를 지정하는 방법
    - 생성하려는 클래스에 metaclass를 직접 지정해줬는지 확인한다.
    - 만일 metaclass를 지정해줬다면 해당 metaclass를 사용한다.
    - 지정해주지 않았다면 모듈 레벨에서 metaclass를 찾는다.
    - 그래도 찾을 수 없다면 가장 첫 번째 부모 클래스가 가진 metaclass를 사용한다.
  - Metaclass는 꼭 class일 필요는 없다.
    - callable하기만 하면 된다.
    - 그러나 일반적으로 class를 상용한다.
  - 간단한 예시
    - 기본 metaclass인 type을 상속 받아 생성한다.

  ```python
  class MyMetaClass(type):
      pass
  
  class MyClass(metaclasss=MyMetaClass):
      pass
  
  print(MyClass.__class__)	# <class '__main__.MyMetaClass'>
  ```

  - 함수 형태의 metaclass
    - `type`으로 생성한 class를 반환하는 함수를 metaclass로 사용한다.
    - class의 이름을 모두 대문자로 생성하는 metaclass

  ```python
  def upper_name(future_name, future_parents, future_attr):
      future_name = future_name.upper()
      return type(future_name, future_parents, future_attr)
  
  
  class MyClass(metaclass=upper_name):
      pass
  
  print(MyClass.__name__)		# MYCLASS
  ```

  - class 형태의 metaclass
    - `type`을 상속받는 클래스를 metaclass로 사용한다.
    - `__new__`는 항상 첫 번째 인자로 정의된 클래스를 받는다(일반적으로는 `cls`라는 이름을 사용한다).

  ```python
  class UpperNameMetaClass(type):
      def __new__(uppername_metaclass, future_name, future_parents, future_attr):
          future_name = future_name.upper()
  
          return type(future_name, future_parents, future_attr)
  
  
  class MyClass(metaclass=UpperNameMetaClass):
      pass
  
  print(MyClass.__name__)		# MYCLASS
  ```

  - OOP코드로 변경하기
    - 위 코드는 완전한 OOP 코드가 아니다.
    - type을 직접 호출했고, `__new__` 코드를 오버라이드하거나 호출하지 않았기 때문이다.

  ```python
  class UpperNameMetaClass(type):
      def __new__(uppername_metaclass, future_name, future_parents, future_attr):
          future_name = future_name.upper()
  
          return type.__new__(uppername_metaclass, future_name, future_parents, future_attr)
  
  
  class MyClass(metaclass=UpperNameMetaClass):
      pass
  
  print(MyClass.__name__)		# MYCLASS
  ```

  - super를 사용하여 더 깔끔하게 작성하기

  ```python
  class UpperNameMetaClass(type):
      def __new__(cls, future_name, future_parents, future_attr):
          future_name = future_name.upper()
  
          return super(UpperNameMetaClass, cls).__new__(cls, future_name, future_parents, future_attr)
  
  
  class MyClass(metaclass=UpperNameMetaClass):
      pass
  
  print(MyClass.__name__)		# MYCLASS
  ```



- 왜 사용해야 하는가?
  - class의 변형이 필요할 경우 사용한다.
    - 간단한 class의 변형이 필요하다고 해서 꼭 복잡하고 에러가 발생할 가능성이 큰 metaclass를 사용할 필요는 없다.
    - 복잡한 class의 변형이 필요할 경우 사용하는 것이 좋지만 클래스를 변형할 일이 많지는 않다.
  - Python 사용자의 99%는 metaclass를 사용할 필요가 없다.
    - metaclass를 진짜로 사용해야하는 사람들은 왜 필요한지에 대해 설명할 필요가 없는 사람들이다.



- metaclass로 singleton 구현하기

  - singleton은 클래스의 인스턴스를 하나만 생성하는 방식이다.
  - metaclass를 활용하면 간단하게 구현이 가능하다.

  ```python
  class Singleton(type):
      instances = {}
      def __call__(cls, *args, **kwargs):
          # 인스턴스가 생성된 적 없을 경우에만 새 인스턴스를 생성한다.
          if cls not in cls.instances:
              cls.instances[cls] = super().__call__(*args, **kwargs)
          
          return cls.instances[cls]
  
  
  class MyClass(metaclass=Singleton):
      pass
  
  
  first_inst = MyClass()
  second_inst = MyClass()
  print(first_inst is second_inst)
  ```



## Python property

> https://blog.naver.com/PostView.naver?blogId=codeitofficial&logNo=221701646124&parentCategoryNo=&categoryNo=7&viewDate=&isShowPopularPosts=false&from=postView

- getter와 setter

  - 객체의 필드에 직접 접근하는 대신 메서드를 통해 접근하는 방식이다.
  - 필드의 값을 가져오는 메서드를 getter, 필드에 값을 설정하는 메서드를 setter라 부른다.

  - 왜 사용해야 하는가?
    - Python은 type의 변환이 자유롭기 때문에 본래 의도한 값이 아닌 다른 값으로 수정해도 알 수 있는 방법이 없다.
    - 아래 예시에서 본래 `name` 필드에는 str이 오도록 설계됐지만, int type의 data가 와도 예외가 발생하지 않는다.
    - 따라서 getter와 setter를 사용하여 값에 대한 유효성을 검증하는데 사용한다.

  ```python
  class Employee:
      def __init__(self, name):
          self.name = name
      
  employee = Employee("Kim")
  employee.name=28
  ```

  - 유효성 검증

  ```python
  class Employee:
      def __init__(self, name):
          self._name = name
      
      def get_name(self):
          return self._name
  
      def set_name(self, name):
          if type(name) != str:
              raise ValueError("name must be str type")
          self._name = name
      
  employee = Employee("Kim")
  employee.set_name(28)
  ```



- Descriptor

  - Python에서 하나의 객체는 다른 객체를 속성으로 가질 수 있다.
  - 이 때 속성이 되는 객체의 값을 읽거나, 쓰거나, 삭제하려고 할 때 이루어질 동작이 미리 정의된 객체를 디스크립터라 한다.
    - `__get__`, `__set__`, `__delete__` 메서드를 사용하여 구현할 수 있다.
    - 셋 중 하나만 정의되어 있어도 디스크립터라 할 수 있다.
    - 각 메서드가 받는 파라미터들의 의미는  `obj`는 디스크립터를 속성으로 갖고 있는 인스턴스, `objtype`은 `obj`의 class, `val`는 새로 설정되는 인스턴스이다.

  ```py
  # desciptor
  class Company:
      def __init__(self, name, location):
          self.name = name
          self.location = location
      
      def __get__(self, obj, objtype):
          return "name: {}, location: {}".format(self.name, self.location)
      
      def __set__(self, obj, val):
          self.name = val.name
          self.location = val.location
  
      def __delete__(self, obj):
          self.name = ""
          self.location = ""
  
  # 다른 객체를 속성으로 가지는 객체
  class Person:
      company = Company("Kim", "CompanyCompany")
  
  property
  
  person = Person()
  person.company     # __get__ 실행
  changed_company = Company("Kim", "AnotherCompany")
  person.company = changed_company    # __set__ 실행
  del person.company    # __delelte__ 실행
  ```

  - Descriptor에는 2가지 종류가 있다.
    - Data descriptor: `__set__`, `__delete__` 중 하나라도 정의되어 있는  descriptor.
    - Non-data descriptor: `__get__`만 정의되어 있는 descriptor.



- Property

  - Descriptor를 보다 간결하게 생성하도록 도와주는 Python 객체이다.
    - 초기화시 getter, setter, deleter 메서드를 인자로 받는다.
    - `property`클래스의 인스턴스는 descriptor이다.

  ```python
  # property class의 코드
  class property:
      fget: Callable[[Any], Any] | None
      fset: Callable[[Any, Any], None] | None
      fdel: Callable[[Any], None] | None
      __isabstractmethod__: bool
      def __init__(
          self,
          fget: Callable[[Any], Any] | None = ...,
          fset: Callable[[Any, Any], None] | None = ...,
          fdel: Callable[[Any], None] | None = ...,
          doc: str | None = ...,
      ) -> None: ...
      def getter(self, __fget: Callable[[Any], Any]) -> property: ...
      def setter(self, __fset: Callable[[Any, Any], None]) -> property: ...
      def deleter(self, __fdel: Callable[[Any], None]) -> property: ...
      def __get__(self, __obj: Any, __type: type | None = ...) -> Any: ...
      def __set__(self, __obj: Any, __value: Any) -> None: ...
      def __delete__(self, __obj: Any) -> None: ...
  ```

  - 주로 decorator로 사용하지만 아래와 같이 사용하는 것도 가능하다.
    - 아래와 같이 사용하는 것이 property의 동작 원리를 이해하는데는 더 도움이 된다.
    - 실제 사용할 때는 decorator로 활용하는 것이 낫다.

  ```python
  class Company:
      def __init__(self, name):
          self._name = name
      
      def _get_name(self):
          return "name: {}".format(self._name)
      
      def _set_name(self, name):
          self._name = name
  
      def _delete_name(self):
          self._name = ""
      
      # property를 생성할 때 getter, setter, deleter 순으로 넘긴다.
      name = property(_get_name, _set_name, _delete_name)
  
  
  company = Company("Foo")
  company.name = "Bar"
  ```

  - decorator로 사용하기

  ```python
  class Company:
      def __init__(self, name):
          self._name = name
      
      @property
      def name(self):
          return "name: {}".format(self._name)
      
      @name.setter
      def name(self, name):
          self._name = name
  
      @name.deleter
      def name(self):
          self._name = ""
  
  
  company = Company("Foo")
  company.name = "Bar"
  ```











# 모듈

- 모듈
  - 함수나 변수 또는 클래스를 모아 놓은 파일
  - 다른 파이썬 프로그램에서 불러와 사용할 수 있게끔 만든 파이썬 파일이라고도 할 수 있다.



- 모듈 사용하기

  - 모듈 생성하기

  ```python
  # module1.py
  def hello():
      return "Hello!"
  
  def plus(a,b):
      return a+b
  ```

  - 모듈 불러오기
    - `import`를 통해 불러온 후 사용한다.
    - 특정한 함수, 클래스, 변수만 불러오고 싶으면 `from`을 사용한다.
    - 모든 것을 불러오고 싶다면 `from 모듈명 import *`와 같이 적으면 된다.
    - `as`를 사용하여 이름을 직접 정하는 것도 가능하다.

  ```python
  # pract.py
  import module1
  
  print(module1.hello())		# Hello!
  print(module1.plus(4,5))	# 9
  ```

  ```python
  from module1 import hello, plus
  # from module1 import * 와 위 문장은 같다.
  
  print(hello())	# Hello!
  ```



- `if__name__=="__main__"`

  - `module1.py`를 아래와 같이 수정하면

  ```python
  # module1.py
  def hello():
      return "Hello!"
  
  def plus(a,b):
      return a+b
  
  print(hello())
  print(plus(4,2))
  ```

  -  `import`할 때 print문이 실행되는 문제가 생긴다.

  ```python
  from module1 import hello
  
  # Hello!
  # 6
  ```

  - `if__name__=="__main__"`을 사용하면 위와 같은 문제를 해결할 수 있다.
    - 이제 `module1.py`를 직접 실행해야 `if__name__=="__main__"` 아래의 문장이 실행되고
    - import 만으로는 실행되지 않는다.

  ```python
  # module1.py
  def hello():
      return "Hello!"
  
  def plus(a,b):
      return a+b
  
  if __name__=="__main__":
      print(hello())
      print(plus(4,2))
  ```

  - `__name__`
    - 모듈의 이름이 저장되는 변수이다.
    - Python 내부적으로 사용하는 특별한 변수 이름이다.
    - 만일 직접 `module1.py` 파일을 실행할 경우, `module1.py`의 `__name__`에는 `__main__` 이라는 문자열이 저장된다.
    - 하지만 다른 파이썬 셸이나 다른 Python 모듈에서 `module1.py`을 `import` 할 때에는 `__name__` 변수에는 `module1.py`의 모듈 이름 값 `module1`가 저장된다.



- 모듈을 불러오는 또 다른 방법

  - 모듈이 있는 폴더로 실행 파일을 옮기지 않고 `sys`를 사용해 모듈을 불러올 수 있다.
  - `sys.path`는 python 라이브러리가 설치되어 있는 라이브러리를 보여 준다. 만약 파이썬 모듈이 위 디렉토리에 들어 있다면 모듈이 저장된 디럭토리로 이동할 필요 없이 바로 불러서 사용할 수 있다.

  ```python
  import sys
  
  print(sys.path)
  """
  ['', 'C:\\Windows\\SYSTEM32\\python37.zip', 'c:\\Python37\\DLLs', 
  'c:\\Python37\\lib', 'c:\\Python37', 'c:\\Python37\\lib\\site-packages', 
  'C:/doit/mymod']
  """
  ```

  - 모듈이 위치한 경로가 `D:\`일 경우
    - 명령 프롬프트에서는 `/`, `\` 둘 다 사용가능하다.
    - 소스코드에서는 반드시 `/` 또는 `\\`를 사용해야 한다.

  ```python
  import sys
  sys.path.append("D:/")
  
  import module1
  print(module1.hello())  # Hello!
  ```

  - 혹은 `	PYTHONPATH`환경 변수를 사용하는 방법도 있다.

  ```bash
  $ set PYTHON=D:/
  ```




- `-m` 옵션

  - `-m`
    - `python <실행시킬 python file>`은 스크립트를 실행시키는 명령어이다.
    - 여기에 `-m` 옵션을 추가하면 모듈을 sys.path에서 찾아서 실행시킨다.
  - 문제
    - 아래 예시에서 main.py를 실행하면 error가 발생하는데 그 이유는 다음과 같다.
    - import는 기본적으로 불러온 코드 전체를 실행한다.
    - 그런데 `script.py`에는 sys.argv로 인자를 받아오는 코드가 있는데, 인자를 넣어준 적이 없으니 error가 발생하는 것이다.

  ```python
  # script.py
  import sys
  
  def say_hello(name):
      print("Hello", name)
  
  say_hello(sys.argv[1])
  
  
  # main.py
  import say_hello
  
  say_hello('Theo')
  ```

  - 모듈화
    - 위와 같은 문제를 해결하기 위해 모듈화를 한다.
    - 이제 main.py를 실행시키든, script.py에 인자를 넘겨서 실행시키든 잘 동작한다.

  ```python
  # my_module.py
  def say_hello(name):
      print("Hello", name)
  
  
  # script.py
  import sys
  import my_module
  
  my_module.say_hello(sys.argv[1])
  
  
  # main.py
  import say_hello
  
  say_hello('Theo')
  ```

  - `__name__`의 활용
    - 위에서는 모듈과 해당 모듈을 사용하는 스크립트를 따로 작성했는데, `__name__`을 활용하면 이 코드를 합칠 수 있다.

  ```python
  # my_module.py
  import sys
  
  def say_hello(name):
      print("Hello", name)
  
  if __name__=="__main__":
      say_hello(sys.argv[1])
  ```

  - `-m` 옵션으로 실행
    - python 스크립트가 아닌 모듈을 실행하기에, 파일명이 아닌, 확장자를 떼고 입력한다.

  ```bash
  $ python -m my_module 'Theo'
  ```







# 패키지

- 패키지

  - python 모듈을 계층적(디렉토리 구조)으로 관리할 수 있게 해주는 것
  - 아래 구조에서 
    - person은 패키지 이름
    - person, family, school, company는 디렉터리 이름
    - 확장자가 .py 인 파일은 파이썬 모듈이다.

  ```python
  person/
  	__init__.py
      family/
      	__init__.py
          father.py
          husband.py
      school/
      	__init__.py
      	student.py
      company/
      	__init__.py
          employee.py
  ```



- 생성하기

  - 위 구조를 바탕으로 아래 파일들을 생성한다.

  ```python
  D:/test/person/__init__.py
  D:/test/person/company/__init__.py
  D:/test/person/company/employee.py
  D:/test/person/family/__init__.py
  D:/test/person/family/husband.py
  ```

  - employee.py 

  ```python
  def work():
      print("working")
  ```

  - husband.py

  ```python
  def clean():
      print("cleaning")
  ```

  - 환경 변수에 경로 추가하기

  ```bash
  set PYTHONPATH=D:/test
  ```

  

- 사용하기

  - 반드시 명령 프롬프트에서  파이썬 인터프리터를 실행하여 진행해야 한다. IDLE 셸이나 VSCode의 파이썬 셸에서는 에러가 발생한다.

  ```bash
  # 환경 변수를 추가 하고
  set PYTHONPATH=D:/test
  # python 인터프리터를 실행한다.
  python
  ```

  - 패키지 안의 함수 실행하기

  ```python
  # 첫 번째 방법
  >>> import person.company.employee
  >>> person.company.employee.work()
  working
  
  # 두 번째 방법
  >>> from person.company import employee
  >>> employee.work()
  working
  
  # 세 번째 방법
  >>> from person.company.employee import work
  >>> work()
  working
  
  # 아래 방법은 불가능하다.
  # 아래 방법은 game 디렉토리의 모듈 또는 game 디렉토리의 __init__.py에 정의한 것만 참조할 수 있다.
  >>> import person
  >>> person.company.employee.work()
  
  # 아래 방법도 불가능하다.
  # 도트 연산자(.)를 사용해서 import a.b.c처럼 import할 때 가장 마지막 항목인 c는 반드시 모듈 또는 패키지여야만 한다.
  >>> import person.company.employee.work  # import 자체가 안된다.
  ```

  

- `__init__.py`

  - 해당 디렉터리가 패키지의 일부임을 알려주는 역할.
  - 패키지에 포함된 디렉터리에 `__init__.py` 파일이 없다면 패키지로 인식되지 않는다.
    - python3.3 버전부터는 `__init__.py` 파일이 없어도 패키지로 인식한다.
  - 아래 예시에서 `*`를 사용하여 모든 것을 import했음에도 `work`가 정의되지 않았다는 에러가 뜬다.

  ```python
  >>> from person.company import *
  >>> employee.work()  # NameError: name 'employee' is not defined
  ```

  - 특정 디렉터리의 모듈을 `*`를 사용하여 import할 때에는 다음과 같이 해당 디렉터리의 `__init__.py` 파일에 `__all__` 변수를 설정하고 import할 수 있는 모듈을 정의해 주어야 한다.
    - `from person.company.employee import *`는 `__all__`과 상관 없이 모두 import 된다.
    - `from a.b.c import *`에서 c가 모듈인 경우에는 `__all__`과 무관하게 모두 import 된다.

  ```python
  # D:/test/person/company/__init__.py
  __all__ = ['employee']
  ```

  - 이제 다시 실행하면 이상 없이 실행되는 것을 확인할 수 있다.

  ```python
  >>> from person.company import *
  >>> employee.work()
  working
  ```



- relative 패키지

  - 만약 한 디렉토리의 모듈이 다른 디렉토리의 모듈을 사용하고 싶다면 다음과 같이 수정하면 된다.
  - `D:/test/person/company/employee.py` 모듈이 `D:/test/person/family/husband.py`의 모듈을 사용하고 싶다면

  ```python
  # employee.py
  from person.family.husband import clean
  
  def work():
      print("working")
      clean()
  ```

  - 이제 실행해보면 잘 실행되는 것을 확인 가능하다.

  ```python
  >>> from person.company.employee import work
  >>> work()
  working
  cleaning
  ```

  - 위 예시처럼 전체 경로를 사용하여 import 할 수도 있지만 다음과 같이 relative하게 import 하는 것도 가능하다.
    - relative 접근자는 모듈 안에서만 사용해야 한다. 인터프리터에서는 사용이 불가능하다.
    - `..`: 부모 디렉토리
    - `.`: 현재 디럭토리

  ```python
  from ..family.husband import clean
  
  def work():
      print("working")
      clean()
  ```




# import

- from과 import

  - from은 모듈을 불러올 경로를, import는 불러올 모듈 혹은 모듈 내의 불러올 것들(함수, class, 변수 등)를 지정한다.
  - 경로의 기준은 최초에 실행되는 파일이다.
    - 즉 아래와 같은 구조로 되어 있을 때 main.py를 실행한다고 하면 모든 경로는 main.py의 위치를 기준으로 설정해야 한다.
    - say_hello 함수를 직접 import하는 test.py 입장에서 보면 `from hello.hello import say_hello`와 같이 import 해야 하겠지만 모든 경로는 최초 실행 파일인 main.py를 기준으로 작성해야 한다.
    - 만일 test.py를 직접 실행한다면 `from hello.hello import say_hello`와 같이 import하는 것이 맞다.

  
  ```python
  '''
  module/
    - test.py
    - hello/
      - hello.py
  main.py
  '''
  
  # main.py
  from module.test import excute_say_hello
  
  
  excute_say_hello()
  
  
  # test.py
  from module.hello.hello import say_hello
  
  
  def excute_say_hello():
      say_hello()
      
      
  # hello.py
  def say_hello():
      print("Hello World!")
  ```



- import할 때 정확히 무슨 일이 일어나는가?
  - `import test`라는 명령어가 있을 때, python은 다음의 3가지 장소를 순서대로 돌아다니며 test를 찾는다.
    - 아래의 세 군데에서 모두 찾을 수 없으면 `ModuleNotFoundError`를 반환한다.
  - sys.modules
    - 이미 import 된 모듈과 패키지들이 딕셔너리 형태로 저장되어 있는 곳이다.
    - 이미 import 된 것들을 다시 찾을 필요가 없어지게 된다.
  - built-in modules
    - python이 제공하는 공식 라이브러리들이다.
  - sys.path
    - python 라이브러리들이 설치되어 있는 경로를 보여주며, string을 요소로 갖는 리스트로 이루어져 있다.
    - 실행시킨 Python 스크립트의 경로는 default로 sys.path에 포함되어 있다.
    - 따라서 절대경로는 현재 디렉토리부터 시작하게 된다.



- sys.path

  - 생성 과정
    - 최초 시행된 Python 스크립트의 디렉터리의 위치를 리스트에 추가한다.
    - 환경변수 중 `PYTHONPATH`의 값을 가져온다.
    - OS나 Python 배포판이 설정한 값들을 더한다.

  - `sys` module을 통해 list에 어떤 값들이 있는지 확인 가능하다.

  ```python
  import sys
  
  print(sys.path)
  ```



- 절대경로와 상대경로

  - 절대경로
    - import하는 파일이나 경로에 상관 없이 항상 동일한 경로를 작성한다.
    - 경로가 지나치게 길어질 수 있다는 문제가 존재한다.
  - 상대경로
    - import하는 위치를 기준으로 경로를 정의한다.
    - 상대 경로의 기준이 되는 현재 디렉터리는 `__name__`에 의해서 정해지게 된다.
    - 스크립트를 직접 실행시킨 경우 `__name__`에는 `__main__`이 저장되고, import한 경우 `__name__`에는 import 된 모듈의 경로가 저장된다.
    - 따라서 직접 실행시킬 파일에는 상대경로를 적용하면 안된다.
  - 상대경로 error 예시
    - 예를 들어 아래와 같이 test.py에서 import를 상대경로로 작성했을 시에, main.py를 실행하면 아무런 error도 발생하지 않는다.
    - main.py를 실행할 경우 test.py `__name__`에는 module.test가 들어가기 때문에 `module.test.py` 파일이 상대경로의 기준 경로가 된다.
    - 반면에, test.py를 실행할 경우 `__name__`에는 `__main__`이 들어가게 되고, python은 `__main__`이라는 경로를 찾을 수 없으므로 error를 반환한다.
  
  ```python
  '''
  module/
    - test.py
    - hello/
      - hello.py
  main.py
  '''
  
  # main.py
  from module.test import excute_say_hello
  
  
  excute_say_hello()
  
  
  # test.py
  from .hello.hello import say_hello
  
  
  def excute_say_hello():
      print(__name__)
      say_hello()
      
      
  # hello.py
  def say_hello():
      print("Hello World!")
  ```



- sys.path에 경로 추가하여 import하기

  - 다른 사람이 만든 패키지를 사용하거나, 직접 만든 패키지라도 경로를 일일이 지정해주기 힘들 경우 sys.path에 경로를 추가하여 사용하면 된다.
  - sys.path는 list형이므로 append를 통해, 문자열로 된 경로를 추가해주면 된다.

  ```python
  '''
  module/
    - test.py
  main.py
  '''
  
  # main.py
  import sys
  sys.path.append('D:/test/module')	# 추가해주고
  from my_module import say_hello		# 불러온다.
  
  
  say_hello()
  
  
  # test.py
  def say_hello():
      print(__name__)			# my_module
      print('Hello World!')
  ```

  - 절대경로로 import했을 때와의 차이점
    - 위와 디렉터리 구조는 동일하지만 아래와 같이 절대경로로 import하면 `__name__`이 달라지게 된다.

  ```python
  # main.py
  from module.my_module import say_hello	# 절대경로로 import
  
  say_hello()
  
  
  # test.py
  def say_hello():
      print(__name__)			# module.my_module
      print('Hello World!')
  ```

  - 주의점
    - 당연하게도 이미 존재하는 경로를 추가하거나, sys.modules, built-in modules에 존재하는 모듈 명을 추가할 경우, 문제가 생길 수 있다.
    - 또한 해당 파일의 sys.path에만 추가되는 것이지 해당 파일이 import하는 파일에는 추가되지 않는다.
    - 예를 들어 위에서 `main.py`파일 내의 sys.path에는 추가되었지만 `test.py` 파일 내의 sys.path에는 추가되어 있지 않다.
    - python 전역에 추가하는 방법도 있지만 권장되지는 않는다.





# 참고

https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/6581949#6581949
