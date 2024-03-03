# 연산자

## 할당 연산자

- 할당 연산자

  - 우항에 있는 피연산자의 평가 결과를 좌항에 있는 변수에 할당

  ```python
  # =
  var = 8
  
  # +=
  var += 1 # 9
  
  # -=
  var -=1  # 7
  
  # *=
  var *= 2 # 16
  
  # /=
  var /= 2 # 4.0
  
  # /=
  var //=2 #4
  
  # %=
  var %= 3 # 2
  
  # **=
  var **= 2 #64
  ```



- Walrus operator(`:=`)

  > https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions

  - 표현식 내에서 변수에 값을 할당하게 해주는 연산자이다.
    - 가독성을 높이는데 목적이 있다.
    - PEP 572에서 assignment expression이라는 이름으로 제안되어 Python 3.8에 추가되었다.
    - `:=`의 형태가 바다코끼리의 눈과 엄니를 닮아 walrus operator라고도 불린다.
  - 기본 문법
    - 기본적인 syntax는 `NAME := expr`의 형태로, `expr`은 괄호 없는 튜플을 제외하고, 유효한 Python 표현식이라면 어떤 것이든 가능하다.
  
  ```python
  # 예를 들어, walrus operator를 사용하지 않은 코드는 아래와 같다.
  n = len(a)
  if n > 10:
      print("List is too long ({} elements, expected <= 10)".format{n})
      
  # 위 코드를 walrus operator를 사용하면 아래와 같이 변경 할 수 있다.
  if (n:=len(a) > 10):
      print("List is too long ({} elements, expected <= 10)".format{n})
      
  # List comprehension에서 아래와 같이 사용이 가능하다.
  [clean_name.title() for name in names 
   if (clean_name := normalize('NFC', name)) in allowed_names]
  ```
  
  - 예외 사항
    - Top level에서 괄호로 묶이지 않은 assignment expression은 유효한 문법이 아니다(assignment statement와 혼용을 피하기 위함).
    - Top level에서 괄호로 묶인 assignment expression은 유효한 문법이지만 추천되지 않는다.
    - 함수의 parameter에서 사용하거나, argument로 사용하는 것은 적절치 않다.
  
  
  ```python
  y := f(x)  # 유효하지 않음
  (y := f(x))  # 유효하지만 추천되지 않음
  
  # 부적절하다.
  foo(x=(p := 42)):
      pass
  
  # 부적절하다.
  ans = (y := foo(y))
  ```
  
  - 주의 사항
    - 괄호가 없는 tuple에서는 예상과 다르게 동작할 수 있다.
    - Python에서 괄호 없이 콤마로 구분된 값은 tuple이 되는데, assignment expression의 경우에는 이것이 적용되지 않는다.
  
  ```python
  assignment_statement = 1, 2
  # top level에서의 사용이므로 적절치는 않지만 예시를 위해 아래와 같이 사용
  (assignment_expression := 1, 2)
  
  print(assignment_statement)		# (1, 2)
  print(assignment_expression)	# 1
  ```







## 산술 연산자


- 단항 산술 연산자

  - `+`,`-`:양수, 음수 변경 및 표현, 단, "+"는 음수를 양수로 변경하지 않는다.



- 이항 산술 연산자

  - 덧셈 연산자
    - 리스트, 튜플, 문자열의 경우에도 덧셈이 가능하다.

  ```python
  print(1+2)  # 3
  print("str"+"ing")  # string
  print([1,2]+[3,4])  # [1,2,3,4]
  print((1,2)+(3,4))  # (1,2,3,4)
  ```

  - 뺄셈 연산자

  ```python
  print(2-1)  #1
  ```

  - 곱셈 연산자
    - 리스트, 튜플, 문자열의 경우에도 곱셈이 가능하다.
    - `*`: 일반적인 곱셈 연산자
    - `**`: 제곱 연산자.

  ```python
  print(1*2)      # 2
  print("a"*2)    # aa
  print([1,2]*2)  # [1, 2, 1, 2]
  print((1,2)*2)  # (1, 2, 1, 2)
  print(2**3)     # 8
  ```

  - 나눗셈 연산자
    - `/`: 일반적으로 사용하는 나눗셈
    - `//`: 몫만 계산
    - `%`: 나머지만 계산

  ```python
  print(8/3)	 # 2.6666666666666665
  print(8//3)	 # 2
  print(8%3)   # 2
  ```



## 비교 연산자

- 대소 관계 비교 연산자

  - `<`, `>` ,`<=` ,`>=`
  - 피연산자가 숫자일 경우 일반적인 상식대로 대소를 비교한다.
  - 피연산자가 문자일 경우 아스키 코드의 순서대로 크기를 비교한다.

  ```python
  print(3>=2)		# True
  print("a">"b")	# False
  print(ord("a"))	# 97
  print(ord("b")) # 98
  ```




- 일치 연산자


    - `==`: 값이 일치 할 경우 True, 불일치 할 경우 False


    - `!=`: 값이 일치 할 경우 False, 불일치 할 경우 True

  ```python
  print("abc"=="abc")		# True
  print("abc"=="xyz")		# False
  print("abc"!="abc")		# False
  print("abc"!="xyz")		# True
  ```

  - `is`: 같은 객체를 가리킬 경우 True, 다른 객체를 가리킬 경우 False

  ```python
  a = [1,2,3]
  b = [1,2,3]
  c = a
  
  # a와 b는 값은 같지만 다른 객체를 가리킨다.
  print(a is b)	# False
  print(a==b)		# True
  # a와 c는 같은 객체를 가리킨다.
  print(a is c)	# True
  ```





## 그 외 연산자

- `in`: 포함 여부를 boolean 값으로 반환한다.

  - 해당 객체가 포함되었는지 여부가 아닌 해당 값이 포함되었는지 여부를 평가한다.

  ```python
  # 값을 평가
  my_list = [1,2,3]
  print(1 in my_list)	 # True
  
  # 같은 객체인지 평가하지 않는다.
  my_list = [{1:'Hello'},{2:'World'}]
  my_dict = {1:'Hello'}
  print(my_dict in my_list)	# True
  ```



- 삼항 연산자: 조건에 따라 어떤 값을 할당할지 결정

  - `조건식이 참일 경우 반환 할 값 if 조건 else 조건식이 거짓일 경우 반환 할 값`

  ```python
  print("3은 4보다 작다." if 3<4 else "3은 4보다 크다.") # 3은 4보다 작다.
  
  # 아래와 같이 쓸 수도 있다.
  def f(gender):
      return 1 if gender=="male" else 2
  
  print(f("female"))  # 2
  ```



- 논리 연산자

  -  `and(&)`, `or(|)` , `not`
     -  좌항과 우항이 모두 boolean타입일 경우 `and` 대신 `&` , `or`, 대신 `|`를 사용 가능하다.
  -  우항과 좌항의 피연산자를 논리 연산한다.
  -  논리 부정(`not`) 연산자는 언제나 boolean 값을 반환한다.
  -  논리합(`and`) 연산자와 논리곱(`or`) 연산자는 일반적으로 boolean 값을 반환하지만 반드시 boolean 값을 반환해야 하는 것은 아니다(단축 평가).

  ```python
  print(not True)			# False
  print(not False)		# True
  print(True and True)	# True
  print(True and False)	# False
  print(True or False)	# True
  print(False or False)	# False
  ```

  - 단축 평가
    - 논리합 연산자와 논리곱 연산자에는 단축평가가 적용된다.
    - 단축평가: 논리 평가(true인가 false인가)를 결정한 피연산자의 평가 결과를 그대로 반영하는 것.

  ```python
  # 논리합 연산자는 두 피연산자 중 하나만 true라도 true를 반환한다.
  # 'apple'은 빈 문자열이 아니므로 true이다.
  # 'apple'이 true이므로 뒤의 피연산자가 true인지 false인지와 무관하게 연산의 결과는 true이다.
  # 따라서 뒤의 피연산자는 굳이 확인하지 않는다.
  # 결국 논리 평가를 결정한 피연산자는 'apple'이 된다.
  print("apple" or "banana")  # apple
  
  # 아래도 마찬가지 이유로 banana가 반환된다.
  print(0 or "banana")       # banana
  
  
  # 논리곱 연산자는 두 피연산자 모두 true여야 true를 반환한다.
  # 'apple'은 빈 문자열이 아니므로 true이다.
  # 그러나 두 피연산자 모두 true여야 true를 반환하므로 이것만으로는 true인지 false인지 구분할 수 없다.
  # 따라서 뒤의 피연산자 'banana'까지 확인을 한다.
  # 결국 논리 평가를 결정한 피연산자는 'banana'가 된다.
  print("apple" and "banana")  # banana
  
  # 아래도 마찬가지 이유로 0이 반환된다.
  print(0 and "banana")  # 0
  ```



- 그룹 연산자
  - `()` : 그룹 내(괄호 안)의 표현식을 최우선으로 평가한다.





# 제어문

## 조건문

- if문

  - 기본 구조
    - if문에 속하는 모든 문장은 들여쓰기를 해주어야 한다.
    - `pass`가 있을 경우 해당 조건이 참이라도 그냥 넘어가게 된다.

  ```python
  if 조건:
      조건이 참일 경우 수행할 문장
  elif 조건:
      조건이 참일 경우 수행할 문장
  else:
      if, elif의 조건이 모두 거짓을 경우 실행할 문장
  ```

  - 예시

  ```python
  if 3<4:
      print("3은 4보다 작다.")
  elif 3==4:
      print("3은 4와 같다.")
  else:
      print("3은 4보다 크다.")
  
  # 3은 4보다 작다.
  
  
  # pass 사용
  if 3<4:
      pass
  elif 3==4:
      print("3은 4와 같다.")
  else:
      print("3은 4보다 크다.")
  
  # 3<4가 참이지만 pass가 적혀 있으므로 아무 것도 실행되지 않는다.
  ```



- match문

  > 3.10 부터 사용이 가능하다.

  - 다른 언어들에 있는 switch case문과 유사하다.
    - 일반적으로 쓰이는 패턴 대조 외에도 다양한 용도로 활용이 가능하다.
  - 기본형
    - 맨 마지막 case에 있는 `_`는 다른 언어의 switch case문에서 default와 유사하다.
    - 또한, case문 내에 break가 없으면 아래 case들을 전부 수행하는 다른 언어와 달리 match case는 매칭된 case만 실행되고 종료된다.

  ```python
  match <subject>:
      case <pattern_1>:
          <action_1>
      case <pattern_1>:
          <action_1>
      case <pattern_1>:
          <action_1>
      case _:
          <action_wildcard>
  ```

  - 패턴 대조
    - 가장 일반적으로 쓰이는 용도이다.
    - `|`를 or 연산자로 사용이 가능하다.

  ```python
  status = 501
  
  match status:
      case 400:
          print("Bad request")
      case 404:
          print("Not found")
      case 418:
          print("I'm a teapot")
      case 500 | 501:
          print("Somthing wrong in sever") 
      case _:
          print("Something's wrong with the internet")
  ```

  - unpacking
    - 아래 코드가 실행되면, `case (x, y)`에 걸리게 되고, x와 y에는 각각 3, 4 가 할당되게 된다.

  ```python
  point = [3, 4]
  
  match point:
      case (0, 0):
          print("Origin")
      case (0, y):
          print(f"Y={y}")
      case (x, 0):
          print(f"X={x}")
      case (x, y):
          print(f"X={x}, Y={y}")
      case _:
          raise ValueError("Not a point")
  ```

  - class와 함께 사용

  ```python
  class Point:
      x: int
      y: int
  
  def location(point):
      match point:
          case Point(x=0, y=0):
              print("Origin is the point's location.")
          case Point(x=0, y=y):
              print(f"Y={y} and the point is on the y-axis.")
          case Point(x=x, y=0):
              print(f"X={x} and the point is on the x-axis.")
          case Point():
              print("The point is located somewhere else on the plane.")
          case _:
              print("Not a point")
  ```

  - if문과 함께 사용
    - case 뒤에 오는 if문을 guard라 부른다.
    - 만일 guard가 false면 다음에 매칭되는 case 블록을 실행한다.

  ```python
  status = 400
  
  match status:
      case 400 if False:
          print("Bad request")
      case 404:
          print("Not found")
      case 418:
          print("I'm a teapot")
      case _:
          print("Something's wrong with the internet")
  ```







## 반복문

- while 문

  - 기본 구조

  ```python
  while 조건문:
      조건문일 참일 동안 수행할 문장
  ```

  - 예시

  ```python
  cnt = 0
  
  while cnt<3:
      print(cnt)
      cnt+=1
      
  """
  0
  1
  2
  """
  
  # 아래 문장의 경우 조건이 계속 참이므로 무한 반복에 빠지게 된다.
  # 종료하려면 ctrl+c를 누르면 된다.
  while True:
      print("안녕하세요!")
  ```
  
  - 반복문과 관련된 키워드
    - `break`: 반복을 즉시 중지한다.
    - `continue`: 뒤는 실행하지 않고 다음 반복으로 넘어간다.

  ```python
  cnt = 0
  while cnt<4:
      cnt+=1
      if cnt==2:
          break    # cnt가 2이면 반복을 종료한다.
      print(cnt)
  """
  1
  """ 
  cnt = 0
  while cnt<4:
      cnt+=1
      if cnt==2:
          continue  # cnt가 2이면 continue를 만나 아래 문장은 실행하지 않고 다음 반복으로 넘어간다.
      print(cnt)
  """
  1
  3
  4
  """
  ```
  



- for문

  - 기본 구조
    - 리스트, 튜플, 딕셔너리, 문자열 등의 자료형을 보다 편리하게 순회할 수 있는 방법이다.
    - 일정 횟수를 반복하도록 할 수도 있다.

  ```python
  # 반복 가능한 자료형을 순회
  for 변수 in 반복 가능한 자료형:
      수행할 문장
      
  # 일정 횟수를 반복
  for 변수 in range(순회를 시작할 숫자, 종료할 숫자+1):
      수행할 내용
  ```

  - 예시

  ```python
  # 반복 가능한 자료형을 순회
  lst = ["one","two","three","four"]
  for i in lst:
      print(i)
  """
  one
  two
  three
  four
  """
  
  
  # 일정 횟수를 반복
  for i in range(0,3):
      print(i)
  """
  0
  1
  2
  """
  
  # 아래와 같은 방법도 가능하다. 
  lst = [[1,2],[3,4],[5,6]]
  
  for i,j in lst:
      print(i,j)
  """
  1 2
  3 4
  5 6
  """
  ```

  - `continue`, `break` 등의 키워드를 while문과 동일하게 사용 가능하다.

  - `range()`
    - 첫 번째 인자로 순회를 시작할 숫자
    - 두 번째 인자로 순회를 종료할 숫자+1
    - 세 번째 인자로 간격을 받는다.

  ```python
  print(list(range(0,7,2)))		# [0, 2, 4, 6]
  
  #역순으로 출력하는 것도 가능하다: range()함수의 매개변수를 사용하는 방법과 reversed()함수를 사용하는 방법
  print(list(range(5,-1,-1)))		# [5, 4, 3, 2, 1, 0]
  print(list(reversed(range(6))))	# [5, 4, 3, 2, 1, 0]
  ```

  - 리스트 내포
    - 리스트 안에 for문, if문을 포함하여 좀 더 편리하게 리스트를 생성할 수 있다.

  ```python
  # 반복문만 사용할 경우1
  result = [i for i in range(1,4)]
  print(result)  # [1, 2, 3]
  
  # 반복문만 사용할 경우2
  arr = [1,2,3,4]
  
  result = [num*3 for num in arr]
  print(result)    # [3, 6, 9, 12]
  
  # 조건문과 함께 사용할 경우
  result = [i for i in range(1,4) if i>=2]
  print(result)  # [2, 3]
  ```




- 반복문 + else문

  - Python은 C, Java와는 달리 반복문과 else문을 쓸 수 있다.
  - 형식
    - 반복문이 break로 중단되지 않고 반복이 끝나면 else문이 실행된다.
    - 만일 반복문이 중단될 경우 else문은 실행되지 않는다.

  ```python
  cnt = 0
  while cnt<3:
      cnt+=1
  else:
      print("else")
  
  for i in range(3):
      if i==2:
          break
  
  else:
      print("else")
  ```

  - 주로 flag 변수 대신 사용한다.

  ```python
  # 아래와 같이 flag 변수를 사용하는 코드를
  flag = False
  for i in range(3):
      if i==2:
          flag=True
          break
  if flag:
      print("hello world!")
      
  # 반복문+else로 아래와 같이 작성할 수 있다.
  for i in range(3):
      if i==2:
          break
  else:
      print("hello world!")
  ```





# 함수

- 함수
  - 입력 값을 가지고 어떠한 작업을 수행한 후 그 작업의 결과물을 내놓는 것.
  - 프로그래밍을 하다 보면 같은 내용을 반복해서 작성해야 하는 경우가 있다. 함수를 사용하면 이러한 반복 작업을 할 필요가 없어지게 된다.
  - 함수를 생성하는 것을 "함수를 선언한다"고 표현한다. 
  - 함수를 사용하는 것을 "함수를 호출한다"고 표현한다.



- 함수의 구조

  - 입력값은 매개 변수(인자, parameter) 혹은 인수(arguments)라고 부른다.
    - 넘길 때는 인수(arguments), 받을 때는 매개 변수(인자,parameter)라고 부른다.
  - 입력값은 있어도 되고 없어도 된다.
  - 결과값도 있어도 되고 없어도 된다.
  - 결과값을 return하면 return이하의 코드는 실행되지 않는다.

  ```python
  def 함수명(입력값):
      수행할 문장
      return 결과값
  ```



- 예시

  - 만일 a+b-c*d를 빈번히 계산 해야 하는 경우가 있다고 생각해보자
  - 함수를 사용하지 않으면 위 표현식을 계산 할 때마다 입력해야 한다.
  - 하지만 함수를 사용한다면, 표현식은 한 번만 입력하고 함수를 사용하여 훨씬 편리하게 계산이 가능하다.

  ```python
  # 함수를 사용하지 않을 경우
  num1 = 3+4-2*8
  num2 = 1+2-7*84
  num3 = 3+5-4*12
  
  # 함수를 사용할 경우
  def cal(a,b,c,d):    # a,b,c,d 를 파라미터로 받는다.
      return a+b-c*d   # 계산 결과를 반환한다.
  
  num1 = cal(3,4,2,8)  # 3,4,2,8을 인수로 넘긴다.
  num2 = cal(1,2,7,84)
  num3 = cal(3,5,4,12)
  ```

  - 입력값과 결과값의 유무

  ```python
  # 입력값과 결과값이 모두 있는 경우
  def say_hello(name):
      return "Hello! "+name
  
  print(say_hello("Cha"))  # Hello! Cha
  
  # 입력값은 없지만 결과값은 있는 경우
  def say_hi():
      return "Hi!"
  
  print(say_hi())  # Hi!
  
  # 입력값은 있지만 결과값은 없는 경우
  def say_hello(name):
      print("Hello! "+name)
  # 함수를 그냥 실행하면 함수 내부의 print문이 실행되어 Hello! Cha가 출력되지만
  say_hello("Cha")		   # Hello! Cha	
  # 함수를 출력해보면 함수가 실행되면서 Hello! Cha가 출력되지만 결과값은 없으므로 None이 출력된다.
  print(say_hello("Cha"))
  """
  Hello! Cha
  None
  """
  
  # 입력값과 결과값이 모두 없는 경우
  def say_hi():
      print("Hi!")
  say_hi()			# Hi!
  print(say_hi())
  """
  Hi!
  None
  """
  ```



- 매개 변수

  - 매개 변수를 위 처럼 순서대로 넘기지 않고 지정해서 넘기는 방법도 존재한다.

  ```python
  def hello(name, age, city):
      return "안녕하세요! "+name+"입니다. "+"저는 "+age+"살이고, "+city+"에 삽니다."
  
  # 매개 변수를 순서대로 넘길 경우
  print(hello("Cha", "28", "Daegu")) 					# 안녕하세요! Cha입니다. 저는 28살이고, Daegu에 삽니다.
  
  # 매개 변수를 지정해서 넘길 경우
  print(hello(city="Daegu", name="Cha", age="28"))	# 안녕하세요! Cha입니다. 저는 28살이고, Daegu에 삽니다.
  ```

  - 매개 변수가 몇 개일지 모를 경우
    - 매개 변수 앞에 `*`를 붙이면 복수의 매개 변수가 넘어온다는 것을 뜻한다.
    - 이 때 매개 변수 명은 아무거나 써도 되지만 관례상 arguments의 약자인 `args`를 사용한다.
    - 특정한 매개 변수와 몇 개인지 모를 매개 변수를 함께 넘겨야 할 경우에는 `*`가 붙은 매개 변수를 가장 마지막에 넘겨야 한다.
    - 키워드 파라미터는 매개변수 앞에 `**`를 붙이는 것인데 이는 받은 인자들을 딕셔너리로 만들어준다.

  ```python
  def add_many(*args):
      result = 0
      for i in args:
          result+=i
      return result
  
  print(add_many(1,2,3,4,5,6,7,8,9))  # 45
  
  
  # 특정한 매개 변수와 몇 개인지 모를 매개 변수를 함께 넘겨야 할 경우
  def say_words(a,b,*args):
      print(a)
      for i in args:
          print(i)
      print(b)
  
  say_words("알파벳 시작.", "알파벳 끝.", "a","b","c","...","x","y","z")
  """
  알파벳 시작.
  a
  b
  c
  ...
  x
  y
  z
  알파벳 끝.
  """
  
  def make_dict(**kargs):
      print(kargs)
  make_dict(name="Cha",gender="male") # {'name': 'Cha', 'gender': 'male'}
  
  
  # 둘을 함께 사용
  def foo(*args,**kargs):
      print(args)
      print(kargs)
  
  foo(1,2,3,4,5, name="Cha", gender="male")
  '''
  (1, 2, 3, 4, 5)
  {'name': 'Cha', 'gender': 'male'}
  '''
  ```

  - 매개 변수의 초기값 설정하기
    - 매개변수의 초기값을 설정하는 것이 가능하다.
    - 주의 할 점은, 초기값을 설정해 놓은 값은 항상 맨 마지막에 들어가야 한다는 점이다.

  ```python
  def user_info(name,age,gender="male",grade=1):
      return {"name":name, "age":age, "gender":gender, "grade":grade}
  
  # 인수를 넘기지 않으면 초기값이 매개변수로 들어가게 된다.
  print(user_info("Cha",27))  # {'name': 'Cha', 'age': 27, 'gender': 'male', 'grade': 1}
  
  # 인수를 넘기면 넘긴 인수가 우선적으로 매개변수로 들어가게 된다.
  print(user_info("Lee",27,"female",3)) # {'name': 'Lee', 'age': 27, 'gender': 'female', 'grade': 3}
  ```

  - 매개변수 unpacking
    - 인자 앞에 `*`를 붙이면 언팩이 가능하다.

  ```python
  def sum_four_nums(num1, num2, num3, num4):
      return num1+num2+num3+num4
      
  
  num_list = [1,2,3,4]
  # 이렇게 할 수도 있지만 코드가 길어진다.
  sum_four_nums(num_list[0], num_list[1], num_list[2], num_list[3])
  # 아래와 같이 하면 리스트 내부의 값들이 순서대로 인자로 들어가게 된다.
  sum_four_nums(*num_list)
  ```



- argument에 기본값을 설정하는 것이 가능하다.

  - argument 뒤에 `=`를 사용하여 기본값을 설정한다.

  ```python
  def plus(num1, num2=5):
      return num1+num2
  
  print(plus(1))	# 6
  ```

  - 기본값을 설정한 argument는, 기본값을 설정하지 않은 argument보다 뒤에 와야 한다.

  ```python
  def plus(num2=5, num1):		# SyntaxError
      return num1+num2
  
  print(plus(1))
  ```




- Python의 default parameter에 mutable object를 줄 경우 주의사항

  >  [Why are default values shared between objects?](https://docs.python.org/ko/3.7/faq/programming.html?highlight=default parameter#id14)

  - 아래와 같이 예상치 못 한 결과가 나올 수 있다.

  ```python
  def f(x,l=[]):
      for i in range(x):
          l.append(i)
      print(l) 
  
  f(2)			# [0, 1]
  f(3,[3,2,1])	# [3, 2, 1, 0, 1, 2]
  f(3)			# [0, 1, 0, 1, 2]
  ```

  - 이는 Python function의 default value는 함수가 정의될 때 딱 한 번만 평가되기 때문이다.
    - 따라서 공식 문서에서는 default value로 None을 주고, 함수 내에서 이를 체크해서 mutable 객체를 생성하는 것을 추천한다.

  - 왜 이렇게 설계했는가?
    - 얼핏 보면 버그 같지만, 사실은 의도된대로 동작하고 있는 것이다.
    - Python에서 모든 것은 객체이다.
    - 따라서 function또한 객체이며, function의 parameter는 function 객체의 attribute라고 볼 수 있다.
    - 만일 함수 호출이 발생할 때 마다 function 객체를 생성해야 한다면 메모리가 감당할 수 없을 정도로 커질 것이다.
    - 따라서 Python에서는 이러한 방식을 취했다.



- 함수가 keyword argument만 받도록 하는 방법

  - 가변인수 (일반적으로  `*args`) 뒤에는 keyword arguments만이 와야 한다는 점을 이용한다.
  - 가변인수 자체를 사용할 것은  아님므로 asterisk를 parameter로 선언한다.
    - asterisk 뒤에 선언된 모든 파라미터는 keyword arguments로 넘겨야 한다.

  ```python
  def foo(a, *qwe, b):
      print(a, b)
  
  
  foo(a=1, b=2)	# 1 2
  foo(1, b=2)		# 1 2
  foo(1, 2)		# TypeError: foo() takes 1 positional argument but 2 were given
  ```

  - `**kwargs`와 함께 사용하는 것도  가능하다.

  ```python
  def foo(*, a, b, **kwargs):
      print(a, b, kwargs)
  
  
  foo(a=1, b=2, c=3, d=4)		# 1 2 {'c': 3, 'd': 4}
  ```



- 함수의 결과값은 언제나 하나이다.

  - 복수의 결과값을 결과값으로 반환할 경우 튜플로 묶여서 반환된다.
  - 결국은 튜플 하나가 반환되는 셈이므로 결과값은 언제나 하나이다.

  ```python
  def cal(a,b):
      return a+b,a-b
  
  print(cal(4,2))  # (6, 2)
  
  plus,minus = cal(4,2)
  print(plus)		# 6
  print(minus)	# 2
  ```



- 함수 안에서 선언한 변수의 효력 범위

  - 함수 안에서 선언한 변수는 함수 안에서만 효력을 갖는다.
  - `global` 키워드를 사용하면 함수 밖의 변수를 함수 안에서 사용이 가능하다.

  ```python
  # 함수 안에서 선언한 변수를 함수 밖에서 사용하려고 하면 다음과 같이 에러가 발생한다.
  def test():
      a = 10
  
  print(a)	# NameError: name 'a' is not defined
  
  
  # 변수 이름이 같다고 해도 함수의 내부에 선언된 변수와 외부에 선언된 변수는 다른 값을 참조하고 있다.
  a = 1
  def vartest(a):
      a = a +1
      print("Inner Value id:",id(a))	# Inner Value id: 2521633024336
  
  vartest(a)
  print("Outer Value id:",id(a))		# Outer Value id: 2521633024304
  
  
  # global 키워드 사용
  a = 1
  def vartest():
      global a
      print("Inner Value id:",id(a))	# Inner Value id: 2778448685392
  
  vartest(a)
  print("Outer Value id:",id(a))		# Outer Value id: 2778448685392
  ```



- lambda

  - 보다 간편하게 함수를 사용할 수 있게 해준다.
  - 기본형

  ```python
  lambda [매개변수1, 매개변수2,...]:<매개변수를 이용한 표현식> [인자]
  ```

  - 예시

  ```python
  # 예시1
  cal = lambda a,b,c:a+b-c
  print(cal(3,2,4))	# 1
  
  # 예시2
  result = (lambda a,b:a+b)(1,2)
  print(result)	# 3
  ```



- `map()`

  - `map(함수,반복 가능한 자료형)`은 반복 가능한 자료형의 내부를 순회하면서 함수를 적용시키는 함수이다.
  - lambda를 사용하면 훨씬 간편하게 할 수 있다.

  ```python
  def plus(num):
      num+=1
      return num 
  
  result = list(map(plus,(1,2,3,4,5)))
  print(result)	# [2, 3, 4, 5, 6]
  
  result = list(map(lambda x:x+1,[1,2,3,4,5]))
  print(result)	# [2, 3, 4, 5, 6]
  ```



- `reduce()`

  - `reduce(함수, 반복 가능한 자료형)`은 반복 가능한 자료형 내부의 원소들을 누적하여 함수에 적용시킨다.
  - import 해서 사용해야 한다.
  - 첫 번째 연산에서는 첫 번째와 두 번째 원소가 인자로 들어가지만, 두 번째 연산 부터는 첫 번재 인자로는 첫 연산의 결과값이 들어가게 된다.

  ```python
  from functools import reduce
  
  print(reduce(lambda x,y:x+y,[1,2,3,4,5]))  # 15
  
  print(reduce(lambda x, y: y+x, 'abcde'))   # edcba
  """
  처음 a,b 가 x,y가 되고 y+x는 ba가 된다.
  이제 x에는 ba가, y에는 c가 들어가게 되어 y+x는 cba가 된다.
  위 과정을 반복하면 
  edcba가 된다.
  """
  ```



- `filter()`

  - `filter(함수, 반복 가능한 자료형)`은 반복 가능한 자료형 내부의 원소들을 필터링 하는 것이다.

  ```python
  # 홀수만 찾아서 리스트로 반환
  # 짝수일 경우 2로 나눴을 때 나머지가 0일 것이다.
  # 0은 False 값이므로 거짓으로 평가되어 필터링 되고 홀수만 넘어오게 된다.
  print(list(filter(lambda x:x%2,[1,2,3,4,5,6,7,8,9,10])))
  
  # [1, 3, 5, 7, 9]
  ```





# 입출력

## 사용자 입출력

- 사용자가 입력한 값을 변수에 대입하고 싶을 경우

  - `input()`을 사용하면 된다.

  ```python
  var = input()	# 안녕하세요! 를 입력할 경우	
  print(var)		# 안녕하세요!
  ```

  - 사용자가 어떤 값을 넣어야 하는지 알 수 있도록 다음과 같이 사용하는 것도 가능하다.

  ```python
  num = input("숫자를 입력하세요: ")
  ```

  - input으로 받은 자료의 경우 어떤 자료형을 입력으로 받든 모두 문자열로 취급한다.

  ```python
  num = input("숫자를 입력하세요: ")  # 3을 입력 할 경우
  print(type(num))	# <class 'str'>
  
  # 따라서 반드시 원하는 타입으로 형변환을 해줘야 한다.
  num = int(input("숫자를 입력하세요: "))
  print(type(num))	# <class 'int'>
  ```




- 출력

  > https://realpython.com/python-flush-print-output/ 참고
  
  - `print()`를 사용
    - 큰 따옴표로 둘러싸인 문자열은 + 연산과 동일하다.
    - 문자열  띄어 쓰기는 콤마로 한다.
    - 한 줄에 결과값 출력하고 싶다면 `end=''` 를 옵션으로 주면 된다. 따옴표 안에 출력 사이에 들어갈 문자를 입력한다.
    - `end`의 기본값은 개행문자이다.
  
  ```python
  print("안녕" "하세요")		# 안녕하세요
  print("안녕"+"하세요")		# 안녕하세요
  print("안녕","하세요")		# 안녕 하세요
  print("안녕"+" "+"하세요")	# 안녕 하세요
  
  for i in range(3):
      print(i,end=",")	# 0,1,2,
  ```
  
  - `print()`는 내부적으로 인자로 전달된 객체 내부의 `__str__()`메서드를 호출하여 문자열로 변환한 후 이를 출력한다.
  
  ```python
  class Foo:
      def __str__(self):
          return "hello"
  print(Foo())	# hello
  ```
  
  - `print()`는 인자로 넘겨진 값을 바로 출력하지 않고 buffer에 담아뒀다가 한 번에 출력한다.
    - `print()` 메서드의 `flush` 인자가 이를 조절하는 것으로, 만약 `flush`를 True로 주면 바로 출력된다.
    - 예를 들어, 아래 코드를 실행하면 0, 1, 2가 1초 간격으로 출력되지 않고 3초가 지난 후에 한 번에 출력된다.
    - Buffer를 사용하는 이유는 system call을 줄이기 위해서로, 출력이 발생할 때 마다 system call이 발생하기 때문이다.
  
  ```python
  import time
  
  for i in range(3):
      print(i, end=' ')
      time.sleep(1)
  
  for i in range(3):
      print(i, end=' ', flush=True)
      time.sleep(1)
  ```
  
  - Buffer에는 세 가지 종류가 있다.
    - Unbuffered: Buffer를 사용하지 않는 것으로, 모든 byte는 바로 출력된다.
    - Line-buffered: 개행문자(`\n`)를 만날 때 까지 buffer에 byte를 저장하다, 개행 문자를 만나면 방출한다.
    - Fully-buffered(Block-buffered): 특정 size에 도달하면 한 번에 방출한다.
  - Python의 경우 파일 출력에는 block buffering을 기본값으로 사용하고, interactive 환경에서는 line-buffer를 사용한다.
    - 위 예시에서 문자들이 한 번에 출력되는 이유는 `end`값을 기본값인 개행문자가 아닌 다른 문자로 줬기 때문이다.
    - Interactive 환경에서 기본값은 line-buffer이기에 개행문자를 만나지 않으면 출력을 하지 않는다.
  - Python script를 실행할 때, `-u` 옵션을 주면 모든 buffer를 사용하지 않고 바로 flush한다.
    - 혹은 `PYTHONUNBUFFERED` 환경변수를 비어있지 않은 string값으로 변경(기본값은 빈 스트링)해도 동일하게 동작한다.
    - 사실 `-u` 옵션 자체가 `PYTHONUNBUFFERED` 환경변수를 수정하는 옵션이다.
    - 단, 이는 stderr과 stdout 모두에서 buffer를 사용하지 않게 되므로, 만약 각기 다르게 지정(예를 들어 stdout에는 buffer를 사용하고, stderr에는 buffer를 사용하지 않는 식으로)해야한다면 이 방법은 사용할 수 없다.
  - Pycharm에서 사용할 경우
    - Pycharm의 경우 아래와 같은 script를 `Run '<module_name>'`을 통해 실행시키면 unbuffer 처럼 동작하는 것을 확인할 수 있다.
    - 아마 Pycharm은 `-u`를 기본적으로 추가해서 실행시키는 듯 하다.
  
  ```python
  import time
  
  for i in range(3):
      print(i, end = ' ')
      time.sleep(1)
  ```
  
  
  
  





## 파일 읽고 쓰기

- `open(파일경로/파일명,모드)` 이라는 python 내장 함수를 사용한다.

  - 결과값으로 파일 객체를 돌려준다.
  - 일치하는 파일이 없을 경우 파일을 생성한다.

  ```python
  txt_file = open("pract.txt",'w')
  ```

  - `open`의 첫 번째 인자인 읽을 파일의 경로는 실행 경로가 기준이 된다.




- 모드는 다음과 같다.

  - `r` : 읽기모드, 파일을 읽기만 할 때 사용
  - `w` : 쓰기모드, 파일에 내용을 작성할 때 사용
  - `a` : 추가모드, 파일의 마지막에 새로운 내용을 추가 시킬 때 사용
  - `x`: 생성모드, 파일을 생성하고, 쓰기 모드로 열며, 파일이 있을 경우 에러가 발생한다.
  - `r`, `a`, `w`뒤에 `+`를 붙이면 읽기와 쓰기를 동시에 할 수 있다.
    - `w+`, `r+` 사이에는 차이가 존재한다.
    - `w+`는 기존 파일의 내용을 전부 삭제하고 새로 쓴다.
    - `r+`는 기존 파일의 내용을 유지하고 이어쓴다.
  - `t`, `b`를 뒤에 붙일 수 있다.
    - `b` : 바이너리(이미지 파일 등)
    - `t` : 텍스트, 기본 
    - 즉 `r+t`는 기존 파일의 내용을 유지하면서 텍스트를 쓰고 읽기 위해 파일을 연다는 뜻이다.



- 닫기는 `close()` 함수를 사용한다.

  ```python
  txt_file = open("test.txt",'w')
  txt_file.close()
  ```




- 작성은 `write()`함수를 사용한다.

  ```python
  txt_file = open("test.txt",'w')
  txt_file.write("안녕하세요!")
  txt_file.close()
  
  # 해당 파일을 확인해보면 변경된 것을 확인 가능하다.
  ```



- `readline()`함수를 사용하면 파일을 한 줄씩 읽어 나간다.

  ```python
  # test.txt
  """
  안녕하세요!
  반갑습니다!
  저는 지금 행복합니다!
  """
  
  txt_file = open("test.txt",'r')
  
  for i in range(3):
      print(txt_file.readline())
      
  """
  안녕하세요!
  
  반갑습니다!
  
  저는 지금 행복합니다!
  """
  ```




- `readlines()` 함수는 파일의 모든 줄을 읽어서 한 줄을 하나의 요소로 갖는 리스트를 반환한다.

  ```python
  txt_file = open("test.txt",'r')
  
  print(txt_file.readlines())  # ['안녕하세요!\n', '반갑습니다!\n', '저는 지금 행복합니다!']
  ```




- `read()` 함수는 파일의 모든 내용을 문자열로 반환한다.

  - 인자로 정수를 넘길 수 있는데, 이 경우 해당 개수 만큼의 문자를읽어 온다.

  ```python
  txt_file = open("test.txt",'r')
  
  print(txt_file.read())
  """
  안녕하세요!
  반갑습니다!
  저는 지금 행복합니다!
  """
  ```




- with문은 블록을 벗어나는 순간 `close()`를 자동으로 수행해준다.

  ```python
  with open("test.txt","w") as txt_file:
      txt_file.write("안녕하세요!")
  ```




- PDF 파일 읽고 쓰기

  - 바이너리로 변환해야 한다.

  ```python
  # 바이너리로 읽고
  with open(file_path, 'rb') as file:
      file_contents = file.read()
  
  # 바이너리로 저장한다.
  with open(traslated_file_path, 'wb') as file:
      file.write(file_contents)
  ```




- `tell`과 `seek`

  - 워드나 메모장에 글을 입력할 때 깜빡 거리는 커서와 같이, 파일 오브젝트에도 커서가 존재한다.

  - seek
    - 커서의 위치를 이동한다.
    - 인자로 이동시킬 위치를 받는다.
  - tell
    - 커서의 현재 위치를 알려준다.







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
    - 따라서, 실제 해당 파일의 경로를 찾아서 실행할 필요 없이, 해당 모듈이 `sys.path`에 등록되어 있다면 `-m` 옵션으로 바로 실행할 수 있다.
  - `-m` 옵션으로 실행하면, 현재 디렉토리가 `sys.path`에 추가되어 별도의 추가 없이도 현재 디렉터리의 모듈들을 사용할 수 있다.
    - `-m` 옵션 없이 실행하면, 최초로 실행시킨 script가 위치한 directorty가 `sys.path`에 추가된다.

  ```bash
  # 만일 -m 없이 pip를 실행하려면 아래와 같이 pip의 실제 위치를 찾아서 실행시켜야 한다.
  $ python path/to/my/python/lib/site-packages/pip/__main__.py
  
  # 그러나 -m을 사용하면 sys.path에 등록된 pip 모듈을 바로 실행시킬 수 있다.
  $ python -m pip
  ```




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



## Namespace Package

- Python package의 종류

  - Python3.3부터는 directory에 `__init__.py` file이 없어도 package로 인식한다.
    - Python 3.3 전에는 특정 driectory가 package가 되기 위해서는 해당 driectory에 `__init__.py` file이 있어야했다.

  - Namespace package
    - `__init__.py` file 없이도 package로 인식된 package를 namespace package라 부른다.

  - Regular package
    - Python 3.3 전에 `__init__.py` file을 통해 package임을 표시한 package를 regular package라 부른다.
    - Regular package가 import되면 `__init__.py` file도 실행된다.
  - 두 package의 동작 방식은 차이가 나지 않는다.
    - 다만 일반적으로 namespace package가 regular package에 비해서 import 속도가 아주 약간 느리다.



- Namespace package

  - Namespace
    - Object group을 특정 이름으로 묶는 방식이다.
    - 값 들을 묶을 수도 있고, 함수들을 묶을 수도 있으며, object들을 묶을 수도 있다.
    - 여러 개의 package를 하나의 namespace로 묶는 것도 가능하다.
    - 예를 들어 `typing`을 import한다면 `typing`이라는 namespace에 대한 접근권을 얻는 것이며, `typing`내의 모든 객체를 사용할 수 있다.
  - Namespace package를 언제 사용하는가?
    - 공통된 namespace를 유지하고 싶지만, package 내의 모든 기능이 필요하지는 않을 때.
    - 서로 다르지만 관련된 package들이 있는 경우, 이들이 같은 namespace를 사용하도록 하고자 할 때.
  - 예를 들어 아래와 같은 구조를 가진 library가 있다.
    - foo와 bar라는 2개의 package를 가지고 있다.
    - foo와 bar는 parent/child라는 공통된 구조를 가지고 있다.

  ```
  /my-lib
  └── foo/
      └── common
          └── foo.py
          └── __init__.py
  
  /my-lib
  └── bar/
      └── common
          └── bar.py
          └── __init__.py
  ```

  - 이 때 위 두 개의 package를 `sys.path`에 추가하고 child를 import하면 아래와 같은 결과가 나온다.
    - 두 경로 모두 parent와 child를 공통으로 가지는 데 둘 중 하나만 나오게 된다.
    - 이렇게 나오는 이유는 import시에 sys.path를 순회하면서 `common`을 찾는데, `/my-lib/foo`가 먼저 추가되어 `/my-lib/foo`를 먼저 찾게 되고, 이후에 탐색을 중단하기 때문이다.

  ```python
  import sys
  
  sys.path.extend([
      "/my-lib/foo",
      "/my-lib/bar"
  ])
  
  import common
  
  print(common.__path__)		# ['/my-lib/foo/common']
  ```

  - 따라서 아래와 같이 `common`으로부터 `bar`를 import하려고 하면 error가 발생한다.

  ```python
  import sys
  
  sys.path.extend([
      "/my-lib/foo",
      "/my-lib/bar"
  ])
  
  from common import bar
  # ImportError: cannot import name 'bar' from 'common'
  ```

  - 반면에 아래와 같이 `__init__.py`를 없애고 namespace package로 전환하면

  ```
  /my-lib
  └── foo/
      └── common
          └── foo.py
              
  /my-lib
  └── bar/
      └── common
          └── bar.py
  ```

  - 두 개가 전부 나오는 것을 확인할 수 있다.

  ```python
  import sys
  
  sys.path.extend([
      "/my-lib/foo",
      "/my-lib/bar"
  ])
  
  import common
  
  print(common.__path__)	# _NamespacePath(['/my-lib/foo/common', '/my-lib/bar/common'])
  ```

  - 둘 다 import가 가능하다.
    - foo와 bar는 서로 다른 package에 있음에도 common이라는 같은 namespace로 import가 가능해진다.

  ```python
  from common import foo, bar
  ```



- 그럼 그냥 namespace package만 쓰면 되는 것인가?
  - Namespace package가 묵시적으로 생성된다고 해도(즉, `__init__.py` file이 없으면 자동으로 namespace package가 된다고 해도) 반드시 필요한 경우에만 사용해야한다.
  - 만약 namespace package가 필요한 경우가 아니라면 `__init__.py`를 붙여서 regular package를 사용해야한다.








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

