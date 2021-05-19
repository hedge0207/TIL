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
  - 클래스와 객체는 과자틀과 과자틀에서 나온 과자의 관계와 같다.
  - 클래스가 과자틀이라면 객체는 그 과자틀로 만든 과지이다.
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
  print(type(obj))  # <class '__main__.FourCal'>
  ```

  - 클래스에 작업(함수) 추가하기
    - 클래스 내부에 생성된 함수는 일반 함수와 구분하기 위해 메서드라고 부른다.
    - 일반 함수와 달리 메서드는 첫 번째 매개변수로 `self`를 받는다(`self`말고 다른 이름으로 해도 무관하지만 self로 하는 것이 관례다).
    - `self`에는 메서드를 호출한 객체를 자동으로 받는다.

  ```python
  # 메서드 생성
  class Plus:
      def set_data(self,first,second):  # 첫 번째 매개변수로 `self`를 받는다. 즉 아래 실행문은 다음과 같이 객체 변수를 변경한다.
          self.first = first			  # obj.first = first
          self.second = second		  # obj.second = second
          
  # 메서드 호출 방법 1.
  # 첫 번째 매개변수인 self에는 fc가 자동으로 넘어간다.
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
  - 객체에 초기값을 설정해야 할 필요가 있을 때는 메서드를 사용하는 방법 보다 생성자를 구현하는 것이 낫다.
  - **생성자(Constructor)**란 객체가 생성될 때 자동으로 호출되는 메서드를 말한다.

  ```python
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
  # 생성자는 first, second라는 두 개의 매개변수를 받으므로 생성할 때부터 인자를 넘겨줘야 한다.
  obj = Plus(2,3)
  print(obj.first, obj.second)	# 2 3
  ```

  

- 클래스의 상속

  - 어떤 클래스를 만들 때 다른 클래스의 기능을 물려 받는 것을 클래스의 상속이라 한다.
  - 위에서 만든 `Plus` 클래스를 상속한 후 뺄셈 기능을 추가하여 PlusMunis 클래스를 만들면 다음과 같이 만들 수 있다.
  - 기존 클래스가 라이브러리 형태로 제공되거나 수정이 허용되지 않는 상황에서 상속은 유용하게 쓸 수 있다.

  ```python
  # 피상속 클래스
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  # 아래와 같이 피상속 클래스를 괄호 안에 넣으면 된다.
  class PlusMinus(Plus):
      def mul(self):
          return self.first-self.second
  
  # 피상속 클래스의 생성자와
  pm = PlusMinus(5,4)
  # 메서드를 사용 가능하다.
  print(pm.add())		# 9
  print(pm.mul())		# 1
  ```

  

- 메서드 오버라이딩

  - 피상속 클래스의 메서드를 동일한 이름으로 다시 만드는 것을 메서드 오버라이딩이라 한다.
  - 이렇게 하면 상속을 받은 클래스의 메서드가 실행된다.

  ```python
  # 피상속 클래스
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  class PlusMinus(Plus):
      # 아래와 같이 피상속 클래스의 메서드와 동일한 이름으로 메서드를 생성하면 된다.
      def add(self):
          return self.first*self.second
      def mul(self):
          return self.first-self.second
  
  pm = PlusMinus(5,4)
  # 상속 받은 클래스의 메서드가 실행 된다.
  print(pm.add())		# 20
  print(pm.mul())		# 1
  ```

  

- 클래스 변수

  - 클래스로 만든 모든 인스턴스가 공유하는 변수이다.

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
    - 이제 `module1.py`에서 실행하면 `if__name__=="__main__"` 아래의 문장이 실행되고
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
    - Python 내부적으로 사용하는 특별한 변수 이름이다.
    - 만일 직접 `module1.py` 파일을 실행할 경우, `module1.py`의 `__name__`에는 `__main__` 값이 저장된다.
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

  

# 예외처리

- 예외처리
  - 프로그래밍을 하다 보면 수 없이 많은 오류와 마주하게 된다.
  - 오류가 발생하면 오류가 발생한 줄 아래로는 실행이 되지 않는데 때로는 오류가 발생하더라도 실행해야 할 때가 있다.
  - 그럴 때 사용하기 위한 것이 예외처리 기법이다.



- `try`, `except` 문

  - 기본 구조
    - try 블록 실행 중 오류가 발생하면 except 블록이 실행된다.
    - except문에 발생 오류를 적어놓으면 해당 오류가 발생했을 때에만 except 블록이 실행된다.

  ```python
  # 괄호 안의 내용은 모두 생략이 가능하다.
  try:
      실행할 문장
  except [발생 오류 as 오류 메세지 담을 변수]:
      실행할 문장
  ```

  - 예시

  ```python
  # arr을 설정해 준 적 없기에 아래 문장은 error을 발생시킨다.
  print(arr)
  print("에러가 발생했으므로 출력이 안됩니다.")
  """
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 6, in <module>
      print(arr)
  NameError: name 'arr' is not defined
  """
  
  # 아래와 같이 예외 처리가 가능하다.
  try:
      print(arr)
  except:
      print("에러 발생")
  print("에러가 발생했지만 실행이 됩니다.")
  """
  에러 발생
  에러가 발생했지만 실행이 됩니다.
  """
  
  # error를 특정하는 것도 가능하다.
  try:
      print(arr)
  except NameError as e:
      print("e에는 error message가 담겼습니다.")
      print(e)
  print("에러가 발생했지만 실행이 됩니다.")
  """
  e에는 error message가 담겼습니다.
  name 'arr' is not defined
  에러가 발생했지만 실행이 됩니다.
  """
  
  # error를 특정할 경우 특정하지 않은 에러가 발생하면 except로 빠지지 않는다.
  try:
      3//0
  except NameError as e:
      print("에러 종류가 다르므로 빠지지 않습니다.")
      print(e)
  """
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 2, in <module>
      3//0
  ZeroDivisionError: integer division or modulo by zero
  """
  ```

  

- `finally`

  - try문 수행 도중 예외 발생 여부와 무관하게 수행된다.
  - 보통 사용한 리소스를 close해야 할 때 사용한다.

  ```python
  try:
      3//0
  finally:
      print("ZeroDivisionError가 발생했지만 finally 블록은 실행됩니다.")
  """
  ZeroDivisionError가 발생했지만 finally 블록은 실행됩니다.
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 2, in <module>
      3//0
  ZeroDivisionError: integer division or modulo by zero
  """    
  ```

  

- 복수의 오류 처리하기

  - except를 여러 개 사용하면 된다.
  - 가장 먼저 빠진 except문만 실행 되고 다음 try 블록의 다음 줄은 실행 되지 않는다.

  ```python
  try:
      3//0
      print(arr)
  except ZeroDivisionError as e:
      print(e)
  except NameError as e:
      print(e)
  
  # integer division or modulo by zero 
  
  
  
  # 아래와 같이 하는 것도 가능하다.
  try:
      3//0
      print(arr)
  except (ZeroDivisionError,NameError) as e:
      print(e)
  
  # integer division or modulo by zero
  ```



- 오류 회피하기

  - except 블록에 pass를 쓰면 에러를 그냥 지나칠 수 있다.

  ```python
  try:
      3//0
      print(arr)
  except ZeroDivisionError as e:
      pass
  print("pass 됐습니다.")
  
  # pass 됐습니다.
  ```

  

- 오류 강제로 발생시키기

  - `raise`를 사용한다.
  - 프로그래밍을 하다 보면 예외를 강제로 발생시켜야 할 때가 있다.
  - Dog이라는 class를 생속 받는 자식 클래스는 반드시 bark라는 메서드를 구현하도록 하고 싶은 경우 아래와 같이 할 수 있다.
    - NotImplementedError는 python 내장 에러로 꼭 구현해야 할 부분이 구현되지 않았을 경우 발생한다.

  ```python
  class Dog:
      def bark(self):
          raise NotImplementedError
          
  class Bichon(Dog):
      pass
  
  bcn = Bichon()
  bcn.bark()			# NotImplementedError
  ```

  - 다음과 같이 bark 메서드를 오버라이딩하여 생성하면 에러가 발생하지 않는다.

  ```python
  class Dog:
      def bark(self):
          raise NotImplementedError
          
  class Bichon(Dog):
      def bark(self):
          print("멍멍")
  
  bcn = Bichon()
  bcn.bark()		# 멍멍
  ```

  

- 예외 만들기

  - Python 내장 클래스인 Exception 클래스를 상속하여 만들 수 있다.

  ```python
  class MyError(Exception):
      pass
  
  def is_num(a):
      if type(a)!=int:
          raise MyError
      print(a)
  
  is_num(1)		# 1
  is_num("1")		# __main__.MyError
  ```

  - 에러 메세지 만들기

  ```python
  class MyError(Exception):
      def __str__(self):
          return "입력하신 값은 숫자 타입이 아닙니다!"
  
  def is_num(a):
      if type(a)!=int:
          raise MyError
      print(a)
  
  is_num(1)		# 1
  is_num("1")		#__main__.MyError: 입력하신 값은 숫자 타입이 아닙니다!
  ```

  



# 이터레이터와 제너레이터

- yield

  - 제네레이터를 만들기 위한 Python keyword
  - 함수 안에서 yield를 사용하면 함수는 제너레이터가 되며, yield에는 값을 지정한다.

  ```python
  def number_generator():
      yield 0
      yield 1
      yield 2
   
  for i in number_generator():
      print(i)
  '''
  0
  1
  2
  '''
  ```

  















