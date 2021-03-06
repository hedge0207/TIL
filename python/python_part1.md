# 기초

## 식별자와 스타일 가이드

- Python은 동적 타이핑 언어로 Java와 달리 변수를 선언할 때 타입을 지정해 주지 않아도 된다.



- 식별자
  - 정의: 변수, 함수, 모듈, 클래스 등을 식별하는데 사용되는 이름, 이름을 정의하여 필요할 때 사용하는 것.
  - 식별자는 이름만 보아도 뜻을 알 수 있도록 지정하는 것이 좋다.
  - 식별자의 규칙
    - 영문 알파벳, 밑줄(`_`), 숫자로 구성된다.
    - 첫 글자로 숫자는 사용할 수 없다.
    - 길이에 제한이 없다.
    - 대소문자를 구분한다.
    - 예약어(Keyword, Python 내에서 특정 의미로 사용하는 이름, 파이썬이 이미 정의한 식별자)는 사용할 수 없다.
    - 내장 함수나 모듈 등의 이름으로도 만들면 안된다(에러가 발생하지는 않지만 더 이상 내장 함수나 모듈을 사용할 수는 없다).



- Python에서 `_`(언더바)의 역할

  - 인터프리터에서의 마지막 값

  ```bash
  >>> 1
  1
  >>> _ + 1
  2
  ```

  - 무시하는 값
    - `*`를 활용하여 복수의 값을 무시할 수 있다.

  ```python
  lst = [1,2,3]
  a,_,c = lst
  print(a,c) # 1 3
  
  # 아래와 같이 반복문에도 사용이 가능하다.
  for _ in range(3):
      print("Hello World!")
  ```

  - 숫자의 자릿수를 구분하는 역할

  ```python
  a = 100000
  b = 100_000
  print(a==b)		# True
  ```

  - 네이밍
    - 언더바가 앞에 하나 붙은 경우에는 해당 식별자를 모듈 내에서만 사용하겠다는 의미이다. private이 없는 python의 특성상 private하게 활용하기 위해 사용한다. 다만, 외부 모듈에서 해당 모듈을 import할 때, 언더바가 하나 붙은 식별자는 import하지 않는다.
    - 뒤에 언더바가 하나 붙은 경우에는 Python 키워드와 식별자의 충돌을 피하기 위해 사용하는 것이다.
    - 앞에 언더바가 두 개 붙은 경우에는 네임 맹글링을 위해 사용한다. 이렇게 선언한 식별자는 일반적인 방법으로는 불러올 수 없다.
    - 앞 뒤로 언더바가 2개씩 붙은 경우에는 Python이 자체적으로 정의한 변수나 함수에 사용되며, 이 네이밍 룰이 적용된 함수를 매직 매서드 혹은 던더 메서드라 부른다(e.g. `__init__`).

  ```python
  # 네임 맹글링
  class Test():
      def __init__(self):
          self.__name = "Theo"
  
  test = Test()
  print(test.__name)  # error
  # 아래와 같이 접근해야 한다.
  print(test._Test__name) # theo
  ```



- 명명 스타일
  - 캐멀 표기법
    - 여러 단어를 연달아 사용할 때 각 단어의 첫 글자를 대문자로 적되, 맨 앞에 오는 글자는 소문자로 표기하는 방법.
    - `firstName`
  - 파스칼 표기법
    - 여러 단어를 연달아 사용할 때 각 단어의 첫 글자를 대문자로 적는 것
    - `FirstName`
  - 헝가리안 표기법
    - 접두어로 자료형을 붙이는 표기법.
    - `strFirstName`
  - 스네이크 표기법
    - 단어 사이에 언더바를 넣어서 표기하는 방법, 단 식별자의 첫 글자로는 사용하지 않는 것이 관례다.
    - `first_name`
  - Python의 경우
    - class Exception: 파스칼 표기법
    - 변수, 함수: 스네이크 표기법
    - 모듈: 무조건 소문자로만 적는다.



- 파이썬의 스타일 가이드

  > `PEP8` 참고
  >
  > 스타일 가이드를 준수했는지 확인해주는 `pylint`라는 라이브러리가 있다(pycharm에는 내장되어 있다).

  - 공백
    - 들여쓰기는 공백 4칸을 권장
    - 한 줄은 최대 79자까지(어쩔 수 없는 경우에도 99자를 넘기지 말아야 한다)이며, 넘어갈 경우 `\`로 줄바꿈을 한다.
    - 최상위 함수와 클래스 정의는 2줄씩 띄어 쓴다.
    - 클래스 내의 메소드 정의는 1줄씩 띄어 쓴다.
    - 변수 할당 앞 뒤에 스페이스를 하나만 사용한다.
  - 네이밍 규칙
    - 단일 글자 변수로 l(소문자 L), I(대문자 I), O(대문자 O)를 사용하지 않는다.
    - Producted 인스턴스 속성은 밑줄 하나로 시작한다.
    - Private 인스턴스 속성은 밑줄 두 개로 시작한다.
    - 모듈 수준의 상수는 모두 대문자로 구성한다(언더바로 구분한다).
    - 클래스 내 인스턴스 메서드에서 첫 번째 파라미터의 이름을 self로 지정한다.
    - 클래스 메서드의 첫 번째 파라미터의 이름은 cls로 지정한다.
  - 표현식과 문장
    - `if not A is B` 보다 `if A is not B`를 사용하는 것이 낫다.
    - 함수의 return 값이 없을 경우 `return None`을 확실하게 명시한다.
    - 항상 파일 맨 위에 import 문을 적는다.
    - import시에 한 모듈당 한 줄을 사용한다.
    - import 순서는 표준 라이브러리 모듈-서드파티 모듈-자신이 만든 모듈 순이다.
  - 연산자가 들어간 여러 줄의 계산식은 연산자를 제일 앞에 둬라

  ```python
  total_sum = (10
               +20
               +30
  ```

  - 여는 괄호의 뒤와 닫는 괄호의 앞에는 띄어쓰기 하지 않는다.
    - 괄호 내에서는 요소 단위로 띄어 쓰기를 사용한다.

  ```python
  # bad
  lst = [ 1,2,3 ]
  my_dict = { "a":1,"b":2,"c"3 }
  
  # good
  lst = [1, 2, 3]
  my_dict = {"a":1, "b":2, "c"3}
  ```

  - 할당 연산자 앞뒤로는 각각 한 개의 띄어쓰기를 사용한다.

  ```python
  # bad
  var=1
  
  # good
  var = 1
  ```

  - 할당 연산자 이외의 연산자 앞뒤도 각기 한 칸씩 띄운다.
    - 그러나 띄우지 않는 것이 더 가독성이 좋을 경우 띄우지 않는다.

  ```python
  # bad
  x = 2 + 3 * 1 + 2
  y = (3 + 4) * (6 + 5)
  
  # good
  x = 2 + 3*1 + 2
  y = (3+4) * (6+5)
  ```

  - 여러 줄을 작성해야 할 경우
    - 기본적인 원칙은 보기 좋은 코드를 작성하는 것이다.

  ```python
  # 첫 번째 줄에 인자가 없다면, 한 번 더 들여쓰기를 하여 다음 행과 구분이 되도록 한다.
  def very_long_function_name(
      	var_one,var_two,
      	var_three,var_four):
  	print(var_one)
   
  # 첫 번째 줄에 인자가 있다면 첫 번째 줄의 인자와 유사한 위치에 오도록 수직으로 정렬한다.
  def very_long_function_name(var_one,var_two,
      						var_three,var_four):
  	print(var_one)
  ```

  - 괄호는 마지막 줄에 맞추거나 첫 번째 줄에 맞춰서 닫는다.

  ``` python
  # 마지막 줄의 첫 번째 아이템에 맞춘다.
  my_lst = [
      1,2,3,
      4,5,6
  	]
  
  # 첫 번째 줄에 맞춘다.
  my_lst = [
      1,2,3,
      4,5,6
  ]
  ```

  - 객체의 타입을 비교할 때는 직접 비교하기보다 `isinstance()`를 활용하는 것이 좋다.

  ```python
  # bad
  a = 10
  if type(a)==type(1):
      pass
  
  # good
  a = 10
  if isinstance(a,int):
      pass
  ```
  
  - 예외처리를 할 때에는 `Exception`으로 퉁치지 말고 최대한 구체적으로 적어라
  
  ```python
  # bad
  try:
      print(var)
  except Exception as e:
      print(e)
  
  # good
  try:
      print(a)
  except NameError as e:
      print(e)
  ```





## 기초 문법

- 인코딩은 따로 선언하지 않아도 `UTF-8`로 설정 되어 있다.
  - 유니코드: 전 세계 모든 문자를 컴퓨터로 표현 할 수 있도록 만들어진 규약
    - 인코딩: 언어를 컴퓨터가 이해할 수 있는 언어로 변경하는 것
    - 컴퓨터에 문자를 저장할 때 영어권 국가만 생각해서 만들었기에 다른 나라들은 독자적인 방법을 고안해서 저장했다.
    - 때문에 언어가 다르면 제대로 표시되지 않는 현상이 발생
    - 이를 해결하기 위해 규약을 만들었다.
  - UTF-8: 유니코드 방식으로 가장 널리 쓰이는 방식
  - 만약 인코딩을 설정하려면 코드 상단에 아래와 같이 선언하면 된다.
    - 주석으로 보이지만 Python parser에 의해 읽힌다.
  
  ```python
  # -*- coding: <encoding-name> -*- 
  ```



- 출력하기

  - `print()`를 사용하여 출력한다.

  ```bash
  print("Hello World!")
  ```

  - 여러 값 사이에 문자 넣기

  ```python
  print("Hello", "World!", sep="//")	# Hello//World!
  ```

  - 줄 바꿔 출력하기
    - `\n`을 활용하여 출력한다.

  ```python
  print("a\nb\nc")
  '''
  a
  b
  c
  '''
  ```

  - 한 줄에 출력하기
    - `end` 옵션을 사용한다.

  ```python
  print("Hello!", end=", ")
  print("World")		# Hello!, World
  ```

  



- 주석

  - 한 줄 주석은 `#`으로 표현한다.
    - `#` 뒤에 한 칸의 공백을 두고 작성한다.
  - 여러 줄 주석은 `docstring`( `"""내용"""`)으로 표현한다.
    - docstring은 일반 주석과 달리 출력이 가능하다.
    - python의 내장 함수에 커서를 올리면 관련된 설명이 뜨는데 이는 모두 docstring으로 작성된 것이다.

  ```python
  def my_sum(a,b):
      """
      a+=2
      b+=2
      이 줄은 실행되지 않습니다.
      그러나 docstring이므로 출력은 가능합니다.
      """
      # 이 줄은 docstring이 아닙니다.
      return a+b
  
  print(my_sum(0,0))      //0
  print(my_sum.__doc__)
  """
  a+=2
  b+=2
  이 줄은 실행되지 않습니다.
  그러나 docstring이므로 출력은 가능합니다.
  """
  ```

  

- 코드 라인

  - 기본적으로 Python에서는 문장이 끝날 때 `;`를 붙이지 않는다.
    - 그러나 `;`는 문장이 끝났음을 의미한다.
    - `;` 앞에는 띄어쓰기를 하지 않고, 뒤에만 띄어쓰기를 한다(convention).
  
  ```python
  print("hello! "); print("world!")
  # hello!
  # world!
  
  # ; 없이 아래와 같이 작성하면 SyntaxError: invalid syntax 발생한다.
  print("hello! ")print("world!")
  ```
  
  - 여러 줄을 작성할 때는 역슬래시 `\`를 사용하여 아래와 같이 할 수 있다.
    - list, tuple, dictionary는 역슬래쉬 없이도 여러 줄을 작성 가능하다.
    - 그러나 권장되는 방식은 아니다.
  
  ```python
  print("
  Hello!")    # SyntaxError: EOL while scanning string literal
        
  print("\
  Hello!")    # Hello!
        
  lunch = [
      '자장면','짬뽕',
      '탕수육','냉면'
  ]
  print(lunch)  # ['자장면', '짬뽕', '탕수육', '냉면']
  ```
  
  - 혹은 `"""`를 활용하여 여러 줄로 작성하는 방법도 있다.
  
  ```python
  print("""
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  """)
  
  #결과는 이처럼 한 줄 띄어서 출력되고 마지막 줄 뒤에도 한 줄이 띄어진다.
  """					
  (한 줄 띄고)
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  (한 줄 띄고)
  """
  
  # """\, \"""를 통해 이를 수정할 수 있다.
  print("""\
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세\
  """)
  
  #"""와 \를 함께 쓰면 첫 줄과 마지막 줄에 한 줄이 띄어지지 않는다.
  """					
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  """
  ```
  
  





# 변수 및 자료형

## 변수

- 변수

  - 값을 저장할 때 사용하는 식별자를 의미한다.
  - 상자에 물건을 넣는 것으로 이해하면 쉽다.
  - 실제 값이 저장되어 있는 것은 아니고 값이 저장된 메모리의 주소를 가리키고 있는 것이다.
    - 메모리의 주소는 `id()`함수로 확인이 가능하다.

  ```python
  var = "Hello"
  print(id(var))  # 2107048935088
  ```

  



- 선언, 할당, 참조

  - 선언: 변수를 생성하는 것
  - 할당: 선언된 변수에 값을 할당하는 것으로 `=` 기호를 사용한다.
    - 우변에는 할당할 값을, 좌변에는 할당 받을 변수를 넣는다.
  - 참조: 변수에 할당 된 값을 꺼내는 것을 의미한다.
  - Python의 경우 선언과 할당이 동시에 이루어지지만 다른 언어의 경우 분리해서 할 수 있는 경우도 있다.

  ```python
  # Python
  name = "Cha"
  
  # name이라는 변수의 선언과 "Cha"라는 값의 할당이 동시에 이루어진다.
  ```

  ```javascript
  // JavaScript의 경우
  var name      //선언 하고
  name = "Cha"  //할당 한다.
  ```



## 자료형_part1

- Python의 자료형
  - Python의 모든 값에는 데이터 유형이 있다.
  - Python은 객체 지향 언어로 모든 것이 객체이기 때문에 실제 데이터 유형은 클래스이고 변수는 이러한 클래스의 인스턴스이다.



- 자료형의 확인

  - `type()` 함수를 사용한다.

  ```python
  print(type("Cha"))  # <class 'str'>
  ```





### 숫자

- 정수형(integer)
  - 양의 정수, 0, 음의 정수를 말한다.



- long
  - python 3 이전 버전까지 존재했다.
  - integer의 범위를 벗어나면 long integer 형으로 표시됐다.



- 실수형(부동소수점, floating point)
  - 소수점이 있는 숫자
  - 같은 수를 나타내고 있다고 하더라도 소수점이 있으면 실수형이다.
  - 컴퓨터 지수 표현 방식으로도 표현이 가능하다.



- 복소수형(complex)

  - `x+yj`처럼 복소수 형태로 쓴다.
  - 실수부와 허수부를 분리가 가능하다.
  - 복소수끼리의 연산도 지원한다.

  ```python
  # 정수형과 실수형
  num1 = 5
  num2 = 5.0
  
  print(type(num1))   # <class 'int'>
  print(type(num2))   # <class 'float'>
  
  
  # 컴퓨터 지수 표현 방식
  print(1.23*10**2)       #123.0
  print(1.23e2)			#123.0
  print(1.23E2)			#123.0
  print(100.23*10**-2)	#1.0023
  print(100.23e-2)		#1.0023
  print(100.23E-2)		#1.0023
  
  
  # 복소수형
  complex_num1 = 1.2+1.2j
  complex_num2 = 2.3+2.3j
  complex_num3 = complex_num1+complex_num2
  
  print(type(complex_num1))   # <class 'complex'>
  print(type(complex_num2))	# <class 'complex'>
  print(complex_num3)			# (3.5+3.5j)
  ```

  



### 문자열

- Python에는 문자 데이터 유형이 없다.
  - 다른 언어의 경우 문자와 문자열을 구분하는 경우가 있다.
  - 문자는 딱 한 자일 경우 문자형, 문자열은 2자 이상일 경우 문자열이다.



- 문자열을 만드는 방법

  - 문자열을 만들 때는 `''`, `""`, `""""""`을 사용한다.
  - 여러 줄 작성의 경우, 이전에 설명했던 `""""""`나 `\`를 사용하지만 권장하는 방식은 아니다.

  ```python
  name1 = "Cha"
  name2 = 'Kim'
  name3 = """Lee"""
  
  print(name1)   # Cha
  print(name2)   # Kim
  print(name3)   # Lee
  ```

  

- 문자열 관련 함수들

  - `len()`: 문자열의 길이를 구할 때 사용한다.

  ```python
  print(len("Kim"))  # 3
  ```

  - `.strip()`,`. lstrip()`, `.rstrip()`: 각각 앞뒤 공백, 앞의 공백, 뒤의 공백을 제거할 때 사용한다.

  ```python
  name = " Cha "
  # 좌우 공백을 제거
  print(name.strip(), "공백 확인")     # Cha 공백 확인 
  # 왼쪽 공백을 제거
  print(name.lstrip(), "공백 확인")    # Cha  공백 확인
  # 오른쪽 공백을 제거
  print(name.rstrip(), "공백 확인")    #  Cha 공백 확인
  ```

  - `.count()`: 문자열에서 지정 문자열의 개수를 세어준다.

  ```python
  print("Book".count("o"))  # 2
  ```

  - `.upper()`, `.lower()`: 각기 문자열을 대문자, 소문자로 바꿔준다.
    - `capitalize()`: 단어의 첫 글자만 대문자로 변환

  ```python
  book_name = "The Old Man and the Sea"
  print(book_name.upper())  # THE OLD MAN AND THE SEA
  print(book_name.lower())  # the old man and the sea
  ```

  - `.find()`, `.index()`: 찾으려는 문자열의 위치를 알려준다.

  ```python
  # 아래와 같이 여러 개가 포함되어 있어도 첫 번째 위치만 알려준다.
  print("book".find('o'))   # 1
  print("book".index('o'))  # 1
  
  # 둘의 차이는 찾으련는 문자열이 없을 때 드러난다.
  print("book".find('u'))     # -1
  print("book".index('u'))    # ValueError: substring not found
  ```

  - `.replace(원래 문자열,바꿀 문자열, 개수)`: 문자열 바꾸기
    - Python의 문자열은 불변 객체로 실제로 변경 되는 것이 아니라 새로운 객체를 만들어 리턴하는 것이다.
    - 왼쪽에서부터 개수를 세어 변환한다.
    - 개수를 입력하지 않을 경우 전부 변경된다.

  ```python
  name = "book"
  print(name.replace('o','u',1))   # buok
  print(name.replace('o','u',2))   # buuk
  print(name.replace('o','u'))     # buuk
  ```

  - `.split(구분의 기준이 되는 문자)`: 문자열을 나눈 결과를 리스트로 리턴한다.
    - 기준이 되는 문자를 입력하지 않으면 공백을 기준으로 나눈다.
    - 기준이 되는 문자를 `" "`직접 공백으로 지정해 줄 때와는 다른 결과가 나온다.

  ```python
  names = "Cha    Kim Park"
  print(names.split())  		# ['Cha', 'Kim', 'Park']
  print(names.split(" "))		# ['Cha', '', '', '', 'Kim', 'Park']
  ```

  - `중간에 넣을 문자.join()`: 문자열, 리스트, 튜플, 딕셔너리 등을 하나의 문자열로 합쳐준다.
    - 중간에 넣을 문자가 없을 경우 그냥 연달아 합쳐진다.

  ```python
  names = "Cha Kim Lee"
  names_list = ["Cha", "Kim", "Lee"]
  names_tuple = ("Cha", "Kim", "Lee")
  names_dict = {"one":"Cha", "two": "Kim", "three":"Lee"}
  
  print(",".join(names))			  # C,h,a, ,K,i,m, ,L,e,e
  print(",".join(names_list))		  # Cha,Kim,Lee
  print("".join(names_list))        # ChaKimLee
  print(",".join(names_tuple))      # Cha,Kim,Lee
  print(",".join(names_dict))       # one,two,three
  ```

  - `reversed()`
    - 문자열의 순서를 역전시킨다.
    - 문자열, 리스트 등의 순회 가능한 값을 받아서 reversed 객체를 반환한다.

  ```python
  a = "ABC"
  
  print(reversed(a))	# <reversed object at 0x000001DF70965220>
  print(''.join(reversed(a))) # CBA
  
  # 아래와 같이 하는 방법도 있다.
  print(a[::-1]) # CBA
  ```
  
  - 아스키 코드 값으로 변환
    - `ord()`: 문자의 아스키 코드 값을 리턴
    - `chr()`: 아스키 코드 값을 문자로 리턴
  
  ```python
  chr_a = "a"
  ord_a = ord("a")
  
  print(chr_a)   		# a
  print(ord_a)   		# 97
  print(chr(ord_a)) 	# a
  ```



- 문자열 포맷팅

  - `"{}".format()`
    - 중괄호 순서대로 소괄호 내의 값들이 들어가게 된다.
    - 중괄호 안에 `:` 를 넣고 콜론 우측에 d, f , g 중 무엇을 넣느냐에 따라 출력이 달라지게 된다.
    - 중괄호 안에 `:`를 넣고 콜론 우측에 <,>,^ 중 무엇을 넣느냐에 따라 출력 내용이 달라지게 된다. 이때 기호 앞에 문자를 넣으면 해당 문자로 공백이 채워지게 된다.
    - 중괄호 안에 `:`를 넣고 콜론 우측에 +를 넣으면 + 기호가 부호가 붙어서 출력된다.
    - 중괄호 내부에 0부터 시작하는 숫자를 입력하여 지정한 순서대로 출력되도록 할 수 있다.

  ```python
  last_name = "Cha"
  first_name = "JU"
  print("My last name is {} and first name is {}".format(last_name,first_name))
  # My last name is Cha and first name is JU
  
  # {:f}: 부동소수점
  print("{:f}".format(55))     # 55.000000
  print("{:f}".format(55.00))  # 55.000000
  
  # {:d}: 정수
  print("{:d}".format(55))     # 55
  print("{:d}".format(55.00))  # ValueError: Unknown format code 'd' for object of type 'float'
  
  # {:g}: 의미 없는 소수점 아래 수인 0이 제거
  print("{:g}".format(55))     # 55
  print("{:g}".format(55.00))  # 55
  print("{:g}".format(55.55))  # 55.55
  
  # {:숫자}: 좌측에 숫자 만큼 공백을 준다.
  print("{:5}".format(123))    		#   123
  
  # {:<숫자}: 우측에 숫자 만큼 공백을 준다.
  print("{:<10}222".format("111"))  	# 111       222
  
  # {:>숫자}: 좌측에 숫자 만큼 공백을 준다.
  print("{:>10}222".format("111"))    #        111222
  
  # {:^숫자}: 좌우로 숫자의 절반만큼 공백을 준다.
  print("{:^10}222".format("111"))    #    111    222
  
  # {:문자<>^숫자}: 공백을 문자로 채운다.
  print("{:#<10}222".format("111"))   # 111#######222
  print("{:#>10}222".format("111"))	# #######111222
  print("{:#^10}222".format("111"))   # ###111####222
  
  # -는 앞에 기호가 붙어서 출력되므로 줄이 맞지 않는 문제가 있다. 이를 해결하기 위해서 아래와 같은 방법을 사용한다.
  # +붙여서 출력하기, 띄어쓰기를 사용해도 같은 효과를 볼 수 있다.
  print("{:}".format(1))      // 1
  print("{:}".format(-1))     // -1
  print("{:+}".format(1))     // +1
  print("{:+}".format(-1))    // -1
  print("{: }".format(1))     //  1
  print("{: }".format(-1))    // -1
  
  # 원하는 순서대로 출력하기
  print("내 취미는 {1}이고, 내가 가장 좋아하는 음식은 {0}이다.".format("초밥","축구"))
  # 내 취미는 축구이고, 내가 가장 좋아하는 음식은 초밥이다.
  ```

  - 포맷 코드를 활용한 방식
    - `"%문자"%()`가 기본 형식이다. 문자 자리에 아래와 같은 문자를 입력하면 된다. %s의 경우 어떤 숫자를 입력하든 모두 문자열로 바뀌어서 입력된다.
    - format()함수와 마찬가지로 정렬과 소수점 표현이 가능하다.

  | %s             | %c                  | %d                        | %f                       |
  | -------------- | ------------------- | ------------------------- | ------------------------ |
  | 문자열(String) | 문자 1개(character) | 정수(Integer)             | 부동소수(floating-point) |
  | %o             | %x                  | %%                        |                          |
  | 8진수          | 16진수              | Literal % (문자 `%` 자체) |                          |

  ```python
  #기본형
  print("%s"%('나무'))               # 나무
  print("저건 %s다"%('나무'))		   # 저건 나무다
  print("%d"%(58))				  # 58
  print("나는 %d키로다"%(58))		   # 나는 58키로다
  print("%f"%(58.123))			  # 58.123000
  print("강수량이 %s%% 증가했다"%(5))  # 강수량이 5% 증가했다
  print(type("%s"%(123)))			  # <class 'str'>
  print(type("%s"%(123.456)))		  # <class 'str'>
  
  
  # 정렬
  print("저기에 %s가 있다."%('나무'))     # 저기에 나무가 있다.
  print("저기에 %10s가 있다."%('나무'))	# 저기에         나무가 있다.
  print("저기에 %-10s가 있다."%('나무'))	# 저기에 나무        가 있다.
  
  
  #소수점 표현
  print("%f"%(11.2222))    #11.222200
  print("%.1f"%(11.2222))  #11.2
  print("%.2f"%(11.2222))  #11.22
  ```

  - f-string 포맷팅(3.6 버전부터 지원)
    - `f"{}"`를 사용하여 중괄호 안에 들어가는 값을 문자로 바꾸는 방법
    - 정렬과 소수점 표현 방식, 공백 채우기 등은 format()함수와 동일하다.

  ```python
  a = 157
  b = 170
  print(f"나는 {a}cm이고 쟤는 {b}cm이다.")      # 나는 157cm이고 쟤는 170cm이다.
  print(f"나는 {157}cm이고 쟤는 {170}cm이다.")  # 나는 157cm이고 쟤는 170cm이다.
  
  a = "나무"
  b = 111.22222
  print(f"저건{a}이다")       			# 저건나무이다
  print(f"저건{a:10}이다")				# 저건나무        이다
  print(f"저건{a:>10}이다")				# 저건        나무이다
  print(f"저건{a:!^10}이다")				# 저건!!!!나무!!!!이다
  print(f"소수점은 {b:.2f}이렇게 표현한다")	# 소수점은 111.22이렇게 표현한다
  ```



### Boolean

- True(참), False(거짓)의 두 가지 종류가 있다.



- 빈 문자열, 숫자 0, 빈 리스트, 빈 튜플, 빈 오브젝트, None은 false로 취급된다.

  ```python
  print(bool(" "))    # True
  print(bool(""))		# False
  print(bool(None))	# False
  print(bool(0))		# False
  print(bool([]))		# False
  print(bool(()))		# False
  print(bool({}))		# False
  ```