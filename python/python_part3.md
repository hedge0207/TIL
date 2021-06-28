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

  ```bash
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

  



# 함수

- 함수
  - 입력 값을 가지고 어떠한 작업을 수행한 후 그 작업의 결과물을 내놓는 것.
  - 프로그래밍을 하다 보면 같은 내용을 반복해서 작성해야 하는 경우가 있다. 함수를 사용하면 이러한 반복 작업을 할 필요가 없어지게 된다.
  - 함수를 생성하는 것을 "함수를 선언한다"고 표현한다. 
  - 함수를 사용하는 것을 "함수를 호출한다"고 표현한다.



- 함수의 구조

  - 입력값은 매개 변수(인자, parameter) 혹은 인수(arguments)라고 부른다.
    - 넘길 때는 인수(arguments), 받을 때는 매개 변수(인자,parameter )라고 부른다.
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
  def hello(name,age,city):
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
  lambda 매개변수1, 매개변수2,...:매개변수를 이용한 표현식
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

  - `print()`를 사용
    - 큰 따옴표로 둘러싸인 문자열은 + 연산과 동일하다.
    - 문자열  띄어 쓰기는 콤마로 한다.
    - 한 줄에 결과값 출력하고 싶다면 `end=''` 를 옵션으로 주면 된다. 따옴표 안에 출력 사이에 들어갈 문자를 입력한다.

  ```python
  print("안녕" "하세요")		# 안녕하세요
  print("안녕"+"하세요")		# 안녕하세요
  print("안녕","하세요")		# 안녕 하세요
  print("안녕"+" "+"하세요")	# 안녕 하세요
  
  for i in range(3):
      print(i,end=",")	# 0,1,2,
  ```

  



## 파일 읽고 쓰기

- `open(파일경로/파일명,모드)` 이라는 python 내장 함수를 사용한다.

  - 결과값으로 파일 객체를 돌려준다.
  - 일치하는 파일이 없을 경우 파일을 생성한다.

  ```python
  txt_file = open("pract.txt",'w')
  ```

  

- 모드는 다음과 같다.

  - `r` : 읽기모드, 파일을 읽기만 할 때 사용
  - `w` : 쓰기모드, 파일에 내용을 작성할 때 사용
  - `a` : 추가모드, 파일의 마지막에 새로운 내용을 추가 시킬 때 사용
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



- `os.path` 모듈

  - 파일, 디렉토리 경로와 관련된 함수를 제공한다.
  - `abspath(path)`
    - path의 절대경로를 반환한다.

  ```python
  import os
  
  print(os.path.abspath('test.txt')) # '/home/theo/data/test.txt
  ```

  - `basename(path)`
    - path의 상대경로를 반환한다.
    - 입력값으로 절대경로를 받는다.

  ```python
  import os
  
  print(os.path.basename('/home/theo/data/test.txt')) # test.txt 
  ```

  - `dirname(path)`
    - 입력 파일 혹은 디렉토리까지의 경로를 반환한다.

  ```python
  import os
  
  print(os.path.dirname('/home/theo/data/test.txt')) # /home/theo/data
  ```

  - `exists(path)`
    - 입력 받은 경로가 존재하는지 여부를 bool 값으로 반환한다.

  ```python
  import os
  
  print(os.path.exists('/home/theo/data/test.txt')) # True
  ```

  - `getmtime(path)`
    - 입력 받은 경로(폴더 혹은 파일)의 최근 변경시간을 반환한다.
    - `getmtime(path)` 으로 생성 시간을, `getatime(path)`으로 접근 시간을 구할 수 있다.

  ```python
  import os
  
  print(os.path.getmtime('/home/theo/data/test.txt')) # True
  ```

  - `getsize(path)`
    - 입력 받은 경로의 파일 크기를 반환한다.

  ```python
  import os
  
  print(os.path.getsize('/home/theo/data/test.txt')) # True
  ```

  - `isdir(path)`
    - 입력 받은 경로가 디렉토리인지 여부를 bool 값으로 반환한다.
    - `isfile(path)`로 파일이지 여부를, `isabs(path)`로 절대경로인지 여부를 확인 가능하다.

  ```python
  import os
  
  print(os.path.isdir('/home/theo/data/test.txt')) # False
  ```

  - `join(str1, str2, ...)`
    - 입력 받은 문자열을 경로 형태로 합쳐준다.

  ```python
  import os
  
  print(os.path.join('/home/theo',"data","test.txt")) # /home/theo/data/test.txt
  ```

  - `normpath(path)`
    - path에서 `.`, `..`와 같른 구분자를 제거해준다.

  ```python
  import os
  
  print(os.path.normpath('/home/theo/../data//test.txt')) # /home/theo/data/test.txt
  ```

  - `split(path)`
    - path에서 디렉토리와 파일을 구분하여 튜플로 반환한다.

  ```python
  import os
  
  print(os.path.split('/home/theo/data/test.txt')) # (''/home/theo/data', 'test.txt')
  ```

  























