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
  
  ```python
  # Python
  name = "Cha"
  
  # name이라는 변수의 선언과 "Cha"라는 값의 할당이 동시에 이루어진다.
  ```
  
  - Python의 경우 선언과 할당이 동시에 이루어지지만 다른 언어의 경우 분리해서 할 수 있는 경우도 있다.
  
  ```javascript
  // JavaScript의 경우
  var name      //선언 하고
  name = "Cha"  //할당 한다.
  ```
  
  - Python은 값이 아닌 참조를 할당한다.
    - Python에는 다른 자료형들에 있는 원시 자료형이 존재하지 않는다.
    - 즉, 모든 것이 객체이므로, 변수에 값을 할당 할 때 값이 아닌 객체의 주소를 할당하게 된다.



- Python Multiple Assignment

  - 2개 이상의 값을 2개 이상의 변수에 동시에 할당하는 것이다.
    - Python만의 독특한 문법이다.
    - 다른 언어의 경우 두 변수에 할당된 값을 서로 교환하려면 변수 하나가 더 필요하지만, Python은 다중 할당을 사용하여 추가 변수 없이도 가능하다.

  ```python
  a, b = 1, 2
  print(a, b)		# 1 2
  a, b = b, a
  print(a, b)		# 2 1
  ```

  - 다중 할당의 경우 예상한 것과 값이 다르게 나올 수 있다.
    - 예를 들어 아래 두 예시는 같은 code 같아 보이지만 완전히 다른 결과를 가져온다.

  ```python
  # 예시1
  a = 1
  b = 2
  c = 3
  
  a, b, c = c, a, b
  print(a, b, c)		# 3 1 2
  
  # 예시2
  a = 1
  b = 2
  c = 3
  
  a = c
  b = a
  c = b
  print(a, b, c)		# 3 3 3
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
    - 한 문자 뿐 아니라 여러 개의 문자를 찾는 것도 가능하며 이 경우 첫 문자의 인덱스를 반환한다.
  
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

  - b-string 포맷팅
    - bytes를 의미하며 문자열을 바이트로 인코딩한다.
    - 얼핏 차이가 없어 보이지만 이는 사실 출력할 때 다시 문자열로 디코딩해서 보여주기 때문이다.

  ```python
  _bytes = b'Hello World'
  # 바이트라는 것을 표현하기 위해서 앞에 b가 붙어있다.
  print(_bytes)	# b'Hello World'
  ```

  - u-string 포맷팅
    - unicode를 의미하며 python2에서 사용되던 문법으로, 현재는 기본 인코딩이 unicode이므로 굳이 붙이지 않아도 된다.

  ```python
  # python2에서는 False, python3에서는 True가 나온다.
  print(u"Hello World" == "Hello World")
  ```

  - r-string 포맷팅
    - raw를 의미하며, 이스케이프 문자를 무시한다.

  ```python
  print("Hello\n World")
  print(r"Hello\n World")
  '''
  Hello
   World
  Hello\n World
  '''
  ```



- 문자열 슬라이싱
  - 내부적으로 매우 빠르게 동작하므로, 문자열 문제를 풀 때 문자열 슬라이싱으로 풀이가 가능하다면 문자열 슬라이싱을 적극 활용하는 것이 좋다.
  - 문자열을 list로 매핑하여 처리하는 것은 데이터 구조를 다루는 입장에서는 좋은 방법이지만, 별도 자료형으로 매핑하는 과정에서 상당한 연산 비용이 필요하므로 속도가 느려질 수 있다.
  - `[::-1]`을 사용하여 문자열을 뒤집는 것이 `reverse`로 list를 뒤집는 것 보다 5배 정도 빠르다.





- `__str__`, `__repr__`, `str()`

  - `str()`
    - 다른 타입의 값을 문자열로 변환할 때 사용하는 `str()`은 사실 내장 함수가 아니고 Python의 기본 내장 클래스이다.
    - 즉 `str(1)`은 내장 함수 `str`을 실행하는 것이 아니라, 내장 str 클래스의 생성자 메서드를 실행하고, 그 인자로 1을 넘겨주는 것이다.
  - `__str__`
    - Python은 내장 된 자료형들에 대한 연산을 정의하는 메서드들이 있는데, 해당 메서드들은 메서드 이름의 앞뒤에 `__`를 지니고 있다.
    - 예를 들어 `+` 연산을 사용하는 `3+5`와 같은 코드는 사실 내부적으로는 `int` 자료형에 내장되어 있는 `__add__` 메서드를 호출(`(3).__add__(5)`)하는 것이다. 
    - `str()`도 마찬가지로 어떤 객체에 `str()`을 실행하면 해당 객체 내부에 정의되어 있는 `__str__` 메서드가 실행된다.
    - 즉 `str()`은 그 자체로 문자열로 변환시켜주는 것이 아니라 사실은 `__str__` 메서드를 호출시켜주는 것이다.
    - `repr()`과 `__repr__`도 마찬가지다.
    - `print()`는 사실 인자로 받은 객체들에 내장된 `__str__` 메서드를 실행시켜 문자열화 한 뒤 출력하는 것이다.

  ```python
  # 예시
  a = 10
  b = [1,2,3]
  
  # a와 b에 내장되어 있는(int와 list에 내장되어 있는) __str__ 메서드를 호출하여 문자열로 변환한 뒤 출력한다.
  print(a, b)
  ```

  - `__repr__`
    - 어떤 객체의 출력될 수 있는 표현을 문자열의 형태로 반환한다.
    - `__str__`이 어떤 객체를 문자열로 변환하는 것에 방점이 찍혀 있다면 `__repr__`은 어떤 객체를 문자열로 표현하는 것에 방점이 찍혀 있다.
    - 즉 `__repr__`은 Python에서 해당 객체를 만들 수 있는 문자열을 출력한다(이를 공식적인 문자열이라 한다).

  ```python
  a = "Hello World!"
  
  # 아래의 출력 결과를 가지고는 바로 문자열 객체를 만들 수 없다.
  print(str(a))		# Hello World!
  try:
      # 따옴표가 없으므로 에러가 발생한다.
      b = Hello World!
  
  # 반면 아래의 출력 결과로는 바로 문자열 객체를 만들 수 있다.
  print(repr(a))		# 'Hello World!'
  try:
      b = 'Hello World!'
  ```





### Boolean

- True(참), False(거짓)의 두 가지 종류가 있다.
  - Python에서 Boolean은 내부적으로 0 과 1로 처리되는 정수형의 subclass이다.




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



- `all`, `any`

  - `all`
    - 인자로 받은 모든 요소가 True면 True를 반환하고, 하나라도 False면 False를 반환한다.
    - 인자로 iterable한 type을 받으며, 만일 비어 있을 경우 **True를 반환**한다.

  ```python
  print(all([1,1,1]))			# True
  print(all([0,1,1]))			# False
  print(all([[],[1,2,3]]))	# False
  print(all([]))				# True
  ```

  - `any`
    - 인자로 받은 요소 중 하나라도 True가 있으면 True를 반환하고, 모두 False면 False를 반환한다.
    - 인자로 iterable한 type을 받으며, 만일 비어 있을 경우 **False를 반환**한다.

  ```python
  print(any([0,0,1]))			# True
  print(any([0,0,0]))			# False
  print(any([]))				# False
  ```

  - 활용
    - 아래와 같이 활용이 가능하다.

  ```python
  num = 3
  lst = [4,5,6]
  print(all(num > i for i in lst))	# True
  print(all(num < i for i in lst))	# False
  ```





# Python의 동작 방식

> https://cjh5414.github.io/about-python-and-how-python-works/  참고

- Python에는 두 가지 의미가 있다.
  - 프로그래밍 언어로서의 Python 그 자체
  - Python 구현체(implementation)
    - 구현체란 Python이라는 언어를 이해하고 실행하는 기계를 말한다.
    - C로 Python을 구현한 CPython, Java로 구현한 Jython, Python으로 구현한 PyPy 등이 있다.
    - CPython이 Python 표준 구현체다.



- 어떤 언어를 인터프리터 언어 혹은 컴파일 언어로 구분할 수는 없다.
  - 이는 언어의 속성이 아니라 구현체의 디자인과 관련된 것이기 때문이다.
  - 예를 들어 Python(CPython)의 경우 아래 과정을 거쳐 실행된다.
    - Python 코드를 bytecode로 컴파일한다.
    - 컴파일된 파일을 인터프리터가 해석하고 실행한다.
  - 위 예에서 알 수 있듯이 컴파일과 인터프리터는 Python이라는 언어의 특성이 아니라 CPython이라는 구현체의 디자인일 뿐이다.



- Python은 어떻게 동작하는가

  > https://opensource.com/article/18/4/introduction-python-bytecode

  - Python code는 virtual machine을 위한 instruction들로 변환된다.
    - Python interpreter는 이 virtual machine의 구현이다.
    - 인터프리터 언어인 Python이 다른 인터프리터 언어와 다른 점은 bytecode로 컴파일 한다는 점이다.
    - `__pycache__` 폴더 내부의 `.pyc` 파일이 바로 컴파일된 바이트코드 파일이다.
    - 오직 Python 코드에 변경사항이 있을 경우에만 다시 컴파일한다.
    - 매번 인터프리터를 통해 한 라인씩 해석해서 실행해야 한다면 성능이 매우 떨어질 수 밖에 없어 택한 방식이다.
    - Python interpreter로 넘어가는 형식을 bytecode라 부른다.
    - 따라서 `.pyc` 파일에 있는 내용는 Python code의 더 빠르고 최적화된 버전이 아니며, Python의 virtual machine이 실행할 bytecode의 instruction들일 뿐이다.
    - 컴파일 된 파일을 인터프리터(virtual machine)가 기계어로 번역한 후 실행한다.
  - `dis`를 사용하면 bytecode로 변환된 내용을 사람이 읽기 쉬운 형식으로 출력해준다.
    - 아래 예시에서 `hello` 함수를 호출하는 코드를 추가하고, CPython interpreter를 사용하여 실행하면 아래 출력된 순서로 프로그램이 실행된다.

  ```python
  import dis
  
  
  def hello():
      print("Hello, World!")
  
  dis.dis(hello)
  """
    5           0 LOAD_GLOBAL              0 (print)
                2 LOAD_CONST               1 ('Hello, World!')
                4 CALL_FUNCTION            1
                6 POP_TOP
                8 LOAD_CONST               0 (None)
               10 RETURN_VALUE
  """
  ```

  - `__code__` attribute를 사용하는 방법
    - `__code__` attribute를 사용하여 여러 유용한 정보를 확인 할 수 있다(아래 예시 말고도 다양한 정보를 확인할 수 있다).
    - `co_consts`는 function body 내부에 등장한 모든 literal들을 tuple로 묶은 것이다.
    - `co_varnames`는 function body 내부에서 사용되는 지역 변수들의 이름을 tuple로 묶은 것이다.
    - `co_names`는 function body에서 참조되지만 지역 변수가 아닌 변수들의 이름을 tuple로 묶은 것이다.
    - `co_code`를 사용하면 bytecode 그대로를 보여준다.

  ```python
  print(hello.__code__)				# <code object hello at 0x7f6cb9e19660, file "test.py", line 1>
  print(hello.__code__.co_consts)		# (None, 'Hello, World!')
  print(hello.__code__.co_varnames)	# ()
  print(hello.__code__.co_names)		# ('print',)
  ```



- CPython은 stack 기반의 virtual machine을 사용하며, 아래와 같은 세 가지 종류의 stack이 있다.
  - Call stack
    - Python program이 실행되는 메인 구조이다.
    - 현재 활성화된 함수 호출 하나 당 frame이라 불리는 하나의 item을 가지고있다.
    - Stack의 bottom이 entry point가 된다.
    - 모든 함수 호출은 call stack에 새로운 frame을 push하며, 함수 호출이 끝날 때 마다 해당 frame이 pop 된다.
  - Evaluation stack(data stack)
    - 각 frame에는 evaluation stack을 가지고 있다.
    - Python의 함수 실행이 일어나는 곳이며, Python code를 실행한다는 것은 대부분의 경우에 evaluation stack에 data를 push하고, 조작하고, pop하는 것이다.
  - Block stack
    - 또 각 frame에는 block stack이 존재한다.
    - 이는 반복문, try/except block, with block 같은 특정 유형의 제어 구조를 추적하기 위해 사용한다.
    - 이들은 모두 block stack에 push되고, 해당 block을 빠져 나오면 pop된다.
    - 이들은 Python이 어떤 block이 특정 시점에 활성화 되어 있는지를 알 수 있게 해주어 `continue`, `break` 같은 동작이 가능하게 해준다.



- 대부분의 Python bytecode instruction은 현재 call-stack frame의 evaluation stack을 조작한다.
  - 예를 들어 `my_function(my_variable, 2)`와 같은 함수 호출이 있을 때, bytecode 상으로는 아래와 같은 과정을 거친다.
    - `LOAD_NAME` instruction은 `my_function`라는 함수 객체를 조회하고, 이를 evaluation stack의 top에 push한다.
    - 또 다른 `LOAD_NAME` instruction은 `my_variable`라는 변수를 조회하고, 이를 evaluation stack의 top에 push한다.
    - `LOAD_CONST` instruction은 literal integer 2를 evaluation stack의 top에 push한다.
    - `CALL_FUNCTION` instruction이 실행된다.
  - `CALL_FUNCTION` 
    - `CALL_FUNCTION` instruction은 2개의 argument를 가지고 있으며, 이는 Python이 두 개의 positional argument를 stack에서 pop해야 한다는 것을 의미하므로, 두 개의 값을 pop한다.
    - 그럼 top에는 호출 할 함수가 오게 되는데, 이 함수 역시 pop한다.
    - 그 후 Python 은 call stack에 새로운 frame을 할당하고, 함수 호출을 위한 local variable을 채운다.
    - 다음으로 frame 내부의 `my_function`의 bytecode를 실행한다.
    - 실행이 종료되면, frame은 call stack에서 pop되고, `my_function`의 반환 값이 original frame의 evaluation stack에 push된다.



- 위 정보를 기반으로 `dis`의 output을 해석하면 다음과 같다.

  ```python
  import dis
  
  
  def hello():
      print("Hello, World!")
  
  dis.dis(hello)
  """
    5           0 LOAD_GLOBAL              0 (print)
                2 LOAD_CONST               1 ('Hello, World!')
                4 CALL_FUNCTION            1
                6 POP_TOP
                8 LOAD_CONST               0 (None)
               10 RETURN_VALUE
  """
  ```

  - `LOAD_GLOBAL 0`
    - Python에게 `co_names`의 0번 인덱스에 있는 이름(예시의 경우 `print`)으로 참조된 전역 객체를 찾으라고 말해준다.
    - 그리고 이를 evaluation stack에 push한다.
  - `LOAD_CONST 1`
    - `co_consts`의 1번 인덱스에 있는 literal을 가져오고, 이를 evaluation stack에 push한다.
    - 0번 인덱스가 아니고 1번 인덱스에 있는 literal을 가져오는 이유는 0번 인덱스에 있는 값은 literal None이기 때문이다.
    - 이는 Python의 경우 함수에 return 값이 없으면 암시적으로 None을 반환하기 때문이다.

  - `CALL_FUNCTION 1`
    - Python에게 함수를 호출하라고 말해준다.
    - 이는 evaluation stack에서 하나의 positional argument를 pop해야하며, 이렇게 되면 evaluation stack의 top에는 호출해야 하는 함수가 오게 된다.



# EAFP와 LBYL

- EAFP와 LBYL

  > [PEP 463](https://peps.python.org/pep-0463/)

  - EAFP(Easier to Ask for Forgiveness than Permission)
    - 용서를 구하는 것이 허락을 구하는 것 보다 쉽다는 Python의 일반적인 코딩 스타일이다.
    - 유효한 key 혹은 attribute가 존재한다고 가정하고, 만일 가정이 틀렸을 경우(key 혹은 attribute가 존재하지 않을 경우) exception을 catch하는 방식으로 처리한다.
    - 예외를 방지하지 않고 예외 발생시킨 뒤 핸들링 하는 방식이다.
    - `try`, `catch`문을 사용한다.

  ```python
  try:
      return mapping[key]
  except:
      print("invalid key")
  ```

  - LBYL(Look Before You Leap)
    - 뛰기 전에 살펴보라는 코딩 스타일로, 누울 자리 보고 발 뻗으라는 속담과 유사한 뜻이다.
    - 예외 발생을 방지하는 방식이다.
    - `if`문을 사용한다.
    - 이 방식의 경우 multi-thread 혼경에서 문제가 발생할 수 있다.
    - 예를 들어 아래와 같은 code에서 한 thread가 `if key in mapping`를 수행하여 `mapping`에 `key`가 있다는 것을 확인하고 `mapping[key]`를 실행하기 직전에 다른 thread가 `mapping`에서 `key`를 삭제했다면 예외가 발생하게 된다.
    - 따라서 LBYL 방식을 사용할 경우 lock을 거는 등의 추가적인 처리가 필요하다.

  ```python
  if key in mapping:
      return mapping[key]
  ```

  - Guido van Rossum은 [이곳](https://mail.python.org/pipermail/python-dev/2014-March/133118.html)에서 아래와 같이 말했다.

    > Python에서 EAFP가 LBYL보다 낫다거나, 일반적으로 추천된다는 것에 동의하지 않는다.

    - EAFP와 LBYL 중 무엇이 더 Python 스러운 방식인지에 대한 의견은 아직도 분분한 상황으로 보인다.



- EAFP와 LBYL의 비교

  > https://realpython.com/python-lbyl-vs-eafp/#the-pythonic-way-to-go-lbyl-or-eafp

  - 아래와 같은 4가지 기준으로 비교가 가능하다.
    - Check 횟수
    - 가독성과 명확성
    - Race condition
    - 성능
  - 불필요한 check의 반복
    - 불필요한 check의 반복을 피하게 해준다는 면에서 EAFP가 LBYL보다 낫다.
    - 예를 들어 아래와 같이 양수를 string 형식으로 받아서 interger로 변환하여 반환하는 함수가 있다고 해보자.
    - 아래에서 LBYL 스타일을 적용한 함수는 `isdigit()` 메서드를 실행한 후 결과가 True면 value를 int로 변환하는데, 사실 이는 중복 check이다.
    - `int()`의 실행은 내부적으로 string을 integer로 변환하는데 필요한 모든 check를 수행한다. 즉, `isdigit()`이 반복 실행된다고 볼 수 있다.
    - 반면에 EAFP 스타일을 적용할 경우 이러한 중복 check를 피할 수 있다.

  ```python
  # LBYL
  def to_integer(value):
      if value.isdigit():
          return int(value)
      return None
  
  # EAFP
  def to_interger(value):
      try:
          return int(value)
      except ValueError:
          return None
  ```

  - 가독성과 명확성
    - 가독성과 명확성 측면에서도 EAFP가 낫다.
    - 예를 들어 아래와 같이 a, b를 인자로 받아 a를 b로 나눈 결과를 반환하는 함수가 있다고 하자.
    - 이 때, b 값으로 0이 들어오면 `ZeroDivisionError`가 발생할 것이다.
    - 각 스타일에서 이 error를 처리하는 방식에 차이가 있다.
    - LBYL의 경우 개발자로 하여금 주요 기능 보다 분기에 더 관심을 가지게 만든다.
    - 그러나, EAFP의 경우 주요 기능이 try 블록 안에 있으므로, try블록만 확인하면 주요 기능이 뭔지 쉽게 알 수 있다.

  ```python
  # LBYL
  def divide(a, b):
      if b==0:
          print("zero division detected")
      return a / b
  
  # EAFP
  def divide(a, b):
      try:
          return a / b
      except ZeroDivisionError:
          pass
  ```

  - Race condition
    - Race condition은 각기 다른 프로그램, 프로세스, 스레드 등이 동일한 자원에 동시에 접근할 때 발생하며, 꼭, multi-thread 환경이 아니더라도 다양한 상황에서 발생할 수 있다.
    - LBYL의 경우 race condition의 위험을 증가시킬 수 있다.
    - 아래 LBYL 코드에서 만약 `.is_active()`의 호출과 `.commit()`의 사이 시점에 db와 연결이 끊긴다면, error가 발생할 것이다.
    - 반면에 EAFP의 경우 db와 연결되었는지 확인하지 않고 바로 `.commit()`을 실행하여 race condition의 위험을 제거한다.

  ```python
  # LBYL
  connection = create_connection(db, host, user, password)
  
  if connection.is_active():
      connection.commit()
  else:
      # handle the connection error
      
  # EAFP
  connection = create_connection(db, host, user, password)
  
  try:
      connection.commit()
  except ConnectionError:
      # handle the connection error
  ```

  - 성능(EAFP가 성능상 우위를 보이는 경우)
    - 대부분의 Python 구현체(Cpython, PyPy 등)에서 예외 처리를 빠르게 할 수 있도록 구현하였다.
    - 그럼에도 많은 예외를 처리하는 것 보다는 많은 조건을 비교하는 것이 더 비용이 적게들기는 한다.
    - 반면에, 적은 수의 예외만을 처리하면 된다면 EAFP가 보다 효율적인 전략이 될 것이다.
    - 예를 들어, 아래 함수에서, except문은 counter에 char라는 key가 없을 때에만 실행된다.
    - 반면에, if문은 매 순회마다 반복적으로 실행된다.

  ```python
  # LBYL
  def char_frequency(text):
      counter = {}
      for char in text:
          if char in counter:
              counter[char] += 1
          else:
              counter[char] = 1
      return counter
  
  # EAFP
  def char_frequency(text):
      counter = {}
      for char in text:
          try:
              counter[char] += 1
          except KeyError:
              counter[char] = 1
      return counter
  ```

  - 성능(LBYL이 성능상 우위를 보이는 경우)
    - 위 예시에서는 character 단위로 끊었고, 영문만 들어온다 가정하면, execpt문은 최대 52번(알파벳 대소문자의 개수) 밖에 실행되지 않는다.
    - 그러나 만일 한글이거나, character 단위가 아닌 단어 단위로 끊는다면 except문의 실행 횟수나 조건문의 실행 회수에 차이가 없어지게 되고, 이 경우 조건문을 사용하는 것(LBYL을 사용하는 것)이 더 빠르다.

  ```python
  # LBYL
  def char_frequency(text):
      counter = {}
      for word in text.split():
          if word in counter:
              counter[word] += 1
          else:
              counter[word] = 1
      return counter
  
  # EAFP
  def char_frequency(text):
      counter = {}
      for word in text.split():
          try:
              counter[word] += 1
          except KeyError:
              counter[word] = 1
      return counter
  ```



- Duck typing과 EAFP

  - Type checking
    - Python에서 object의 type 혹은 attribute를 검사하는 것은 anti-pattern으로 여겨진다.
    - 이는 type checking이 Python의 핵심 원리들 중 두 가지를 침해하기 때문이다.
    - 이는 다형성과 duck typing으로, type을 check하는 것은 duck typing 스럽지 않기 때문이다.
  - Type checking의 문제점
    - 아래 예시는 `append`가 있다면 `list`로 보자는 duck typing의 원리를 따르는 코드가 아니라, list라면 append를 하는 코드이다.
    - 또 만일, list대신 deque를 사용하기로 했다고 하자, deque는 list와 마찬가지로 `append` 메서드를 지원하므로, EAFP 방식으로 구현했다면 코드를 수정하지 않아도 되지만 아래와 같이 type checking을 했다면 `isinstance`의 두 번째 인자를 list에서 deque로 변경해줘야한다.

  ```python
  def add_number(num, numbers):
      if isinstance(numbers, list):
          numbers.append(num)
  ```

  - EAFP 적용
    - 위 코드에 EAFP를 적용하면 아래와 같다.
    - 이는 duck typing도 침해하지 않으면서, list에서 deque으로 변경되더라도 함수를 변경하지 않아도 된다.

  ```python
  def add_number(num, numbers):
      try:
          numbers.append(num)
      except AttributeError:
          pass
  ```





# Easter Egg

- `import this`를 실행하면 The Zen of Python이라는 19가지 규칙이 나온다.

  ```
  The Zen of Python, by Tim Peters
  
  Beautiful is better than ugly.
  Explicit is better than implicit.
  Simple is better than complex.
  Complex is better than complicated.
  Flat is better than nested.
  Sparse is better than dense.
  Readability counts.
  Special cases aren't special enough to break the rules.
  Although practicality beats purity.
  Errors should never pass silently.
  Unless explicitly silenced.
  In the face of ambiguity, refuse the temptation to guess.
  There should be one-- and preferably only one --obvious way to do it.
  Although that way may not be obvious at first unless you're Dutch.
  Now is better than never.
  Although never is often better than *right* now.
  If the implementation is hard to explain, it's a bad idea.
  If the implementation is easy to explain, it may be a good idea.
  Namespaces are one honking great idea -- let's do more of those!
  ```

  

