# google 스타일 가이드 추가할것





# 소개

- PEP8
  - Python 스타일 가이드.
  - Python의 창시자인 귀도 반 로섬의 가이드와 다른 가이드를 종합하여 제작 됨.



- 융통성 있게 적용하는 것이 중요하다.
  - PEP8의 목적은 결국 코드의 가독성을 높이고 Python으로 작성된 코드들을 일관성있게 작성하기 위함이다.
  - 따라서 PEP8을 적용하는 것 보다 코드 내의 일관성과 가독성을 유지하는 것이 중요하다.
    - 예를 들어 기존 프로젝트에 PEP8과 배치되는 내용이 있을 경우 기존 프로젝트의 스타일과 다른 PEP8을 적용하는 것 보다 기존 프로젝트의 스타일을 유지하는 것이 가독성과 일관성을 높이는 데 도움이 된다면 당연히 기존 코드의 스타일을 유지해야 한다.



# 코드 레이아웃

- 들여쓰기

  - 4 space를 사용하여 들여쓰기를 한다.
    - Tab과 Space 중 Space가 더 선호된다.
    - Tap은 이미 Tap으로 만들어진 코드와의 일관성을 유지하기 위해서만 사용해야 한다.
    - 파이썬3에서는 Tap과 Space의 혼용을 금지하고 있다.
  - 여러 줄에 걸쳐 코드를 작성할 경우 들여쓰기를 활용하여 코드의 요소들을 수직으로 정렬해야한다.
    - 수직 정렬을 할 때에는 꼭 4 spaces 들여쓰기를 하지 않아도 된다.
    - 들여쓰기를 하되 꼭 4칸을 들여쓸 필요는 없고 수직 정렬에 필요한 만큼 들여쓰기 하면 된다.
  
  ```python
  #올바른 코드
  
  # arguments를 여러 줄에 걸쳐 작성해야 할 때, 첫 번째 줄에 arguments를 작성할 경우 다음 줄의 시작은 윗 줄에서 인자를 받는 부분과 맞춰준다.
  foo = long_function_name(var_one, var_two,
                           var_three, var_four)
  
  # arguments를 여러 줄에 걸쳐 적성해야 할 때, 첫 번째 줄에 arguments를 작성하지 않을 경우, 다음 줄의 arguments를 넘기는 부분은 들여쓰기를 하여 확실히 구분되게 해줘야 한다.
  foo = long_function_name(
      var_one, var_two,
      var_three, var_four)
  
  # 첫 번째 줄에 parameter를 받지 않을 경우, 다음 줄의 parameter를 받는 부분은 들여쓰기를 하여 함수의 선언부와 구분되도록 해야 한다.
  def long_function_name(
          var_one, var_two, var_three,
          var_four):
      print(var_one)
  
  
  
  
  # 잘못된 코드
  
  # 수직 정렬을 하지 않을 것이라면 첫 번째 줄에 arguments를 작성하지 않는다.
  foo = long_function_name(var_one, var_two,
      var_three, var_four)
  
  # 함수의 선언부와 구분될 수 있도록 parameter를 받는 부분에 추가적인 들여쓰기를 해준다.
  def long_function_name(
      var_one, var_two, var_three,
      var_four):
      print(var_one)
  ```
  
  - if 문이 줄을 넘어갈 정도로 긴 경우에 대한 명시적인 지침은 없지만, 아래와 같은 선택지가 존재한다.
    - 첫 줄의 `if (`가 총 4칸이므로 아랫줄에도 자연스럽게 4 space 들여쓰기가 된다.
    - 조건 부분과 실행문을 주석으로 구분해준다.
    - 추가적인 들여쓰기를 해준다.
  
  ```python
  # `if (`로 아랫 줄에 자연스럽게 4칸의 들여쓰기가 된다.
  # 단, 이 경우 조건 부분과 if 구문 내부의 실행문이 구분이 안된다는 문제가 있다.
  if (this_is_one_thing and
      that_is_another_thing):
      do_something()
  
  # 조건 부분과 실행문을 주석으로 구분
  if (this_is_one_thing and
      that_is_another_thing):
      # 두 조건이 모두 참이면 아래 함수를 실행
      do_something()
  
  #추가적인 들여쓰기를 해준다.
  if (this_is_one_thing
          and that_is_another_thing):
      do_something()
  ```
  
  - 여러 줄에 걸친 소/중/대괄호를 닫을 경우 다음의 방식이 모두 가능하다.
  
  ```python
  # 수직 정렬
  my_list = [
      1, 2, 3,
      4, 5, 6
  	]
  
  # 선언부에 맞추기
  result = some_function_that_takes_arguments(
      'a', 'b', 'c',
      'd', 'e', 'f',
  )
  ```



- 한 줄의 최대 길이
  - 모든 줄은 최대 79자로 제한한다.
    - 최대 100자까지는 팀 스타일에 따라 늘려도 좋다.
  - 주석이나 docstrings는 72자로 제한한다.
    - 팀 스타일과 무관하게 72자가 추천된다.
  - 여러 줄을 작성하는 가장 좋은 방법은 코드를 괄호로 묶는 것이다.
    - Python은 여는 괄호와 닫는 괄호 사이의 문장을 한 줄에 작성된 것으로 인식하기 때문이다.
  - 백 슬래시 역시 괄호 보다는 못하지만 여러 줄을 작성하는 적절한 방법일 수 있다.



- 줄바꿈 시 연산자의 위치

  - 연산자 뒤에서 줄바꿈을 하는 것은 가독성을 떨어뜨릴 수 있다.
    - 따라서 줄바꿈 후에 연산자를 표기한다.

  ```python
  # 잘못된 코드
  # 무엇과 무엇이 연산되는지 명확히 보이지 않고, 어떤 연산인지 한 눈에 들어오지 않는다.
  income = (gross_wages +
            taxable_interest +
            (dividends - qualified_dividends) -
            ira_deduction -
            student_loan_interest)
  
  # 올바른 코드
  income = (gross_wages
            + taxable_interest
            + (dividends - qualified_dividends)
            - ira_deduction
            - student_loan_interest)
  ```



- 빈 줄
  - 최상위 수준 함수와 클래스 정의는 두 줄을 띄워서 구분한다.
  - 클래스 안 메소드에 대한 정의는 한 줄을 띄워서 구분한다.
  - 관계된 함수의 모음을 구분하기 위해 추가적인 빈 줄을 활용 가능하다.
  - 논리적인 구분을 보여주기 위해 코드 내에서 빈줄을 사용할 수 있다.



- import

  - 한 줄에 하나의 패키지만 import한다.
  - 하나의 패키지에서 복수의 모듈을 import할 때는 한 줄에 작성한다.

  ```python
  # 올바른 코드
  import os
  import sys
  
  from subprocess import Popen, PIPE
  
  # 잘못된 코드
  import sys, os
  ```

  - import문의 위치는 아래와 같다.
    - 파일의 맨 위
    - 모듈 주석과 docstring 바로 아래
    - 모듈 전역 변수와 상수 위에
  - 다음과 같은 순서로 import한다.
    - 표준 라이브러리
    - 관련된 서브 파티 라이브러리
    - 로컬 라이브러리
  - 그 밖의 규칙
    - 각각의 import 그룹 사이에는 빈 줄을 넣어야 한다.
    - 절대 경로를 통해서 import하는 것이 권장된다.
    - 상대경로는 절대경로를 사용하는 것이 비합리적일 정도로 길어지는 경우에 사용한다.
    - 표준 라이브러리는 항상 절대 경로 import를 사용해야 한다.



# 공백

- 다음의 경우 공백을 피한다.

  - 모든 종류의 괄호의 안쪽
    - 괄호 내부의 요소 들을 구분할 때와, 콜론의 뒤를 제외하고는 공백을 사용하지 않는다.

  ```python
  # 올바른 코드
  spam(ham[1], {eggs: 2})
  
  # 잘못된 코드
  spam( ham[ 1 ], { eggs: 2 } )
  ```

  - 쉼 표와 그 뒤에 오는 닫는 괄호 사이

  ```python
  # 올바른 코드
  foo = (0,)
  
  # 잘못된 코드
  bar = (0, )
  ```

  - 쉼표, 세미콜론, 콜론의 바로 앞

  ```python
  # 올바른 코드
  if x == 4: print x, y; x, y = y, x
  
  # 잘못된 코드
  if x == 4 : print x , y ; x , y = y , x
  ```

  - 슬라이스에서 콜론 좌우의 공백은 주지 않는다.
    - 단, 콜론의 좌우에 다른 연산자가 있을 경우 반드시 공백을 줘야 한다.
    - 슬라이스의 매개변수를 생략하면, 공백도 생략해야 한다.

  ```python
  # 올바른 코드
  ham[1:9]
  ham[1:9:3]
  # 슬라이스의 매개변수를 생략하면, 공백도 생략해야 한다.
  ham[:9:3]
  ham[1::3]
  # 콜론의 좌우에 다른 연산자가 있을 경우 반드시 공백을 줘야 한다.
  ham[lower+offset : upper+offset]
  ham[lower + offset : upper + offset]
  ham[: upper_fn(x) : step_fn(x)]
  ham[:: step_fn(x)]
  
  # 잘못된 코드
  ham[lower + offset:upper + offset]
  ham[1: 9], ham[1 :9], ham[1:9 :3]
  ham[lower : : upper]
  ham[ : upper]
  ```

  - 함수 호출 시 인자 목록을 시작하는 여는 괄호의 바로 앞

  ```python
  # 올바른 코드
  spam(1)
  
  # 잘못된 코드
  spam (1)
  ```

  - 인덱싱 또는 슬라이싱을 시작하는 여는 괄호 바로 앞

  ```python
  # 올바른 코드
  dct['key'] = lst[index]
  
  # 잘못된 코드
  dct ['key'] = lst [index]
  ```

  - 정렬을 위해 두 개 이상의 공백을 사용하는 것

  ```python
  # 올바른 코드
  x = 1
  y = 2
  long_variable = 3
  
  # 잘못된 코드
  x             = 1
  y             = 2
  long_variable = 3
  ```

  - 키워드 arguments 또는 parmeter의 기본값을 나타낼 때 `=`의 좌우에는 공백을 주지 않는다.

  ```python
  # 올바른 코드
  def complex(real, imag=0):
      return magic(r=real, i=imag)
  
  # 잘못된 코드
  def complex(real, imag = 0):
      return magic(r = real, i = imag)
  ```



- 공백이 있어야 하는 경우

  - 슬라이스가 아닌 콜론의 뒤에는 공백이 있어야 한다.

  ```python
  # 올바른 코드
  my_dict = {"key": "value"}
  
  # 잘못된 코드
  my_dict = {"key":"value"}
  ```

  - 할당, 증강 할당, 비교, 논리 등의 연산자의 앞뒤에는 공백을 사용한다.
    - 단, 다른 연산자에 비해 우선순위를 갖는 연산자가 있다면 가장 낮은 우선순위를 갖는 연산자의 앞뒤에만 공백을 주는 것을 고려해볼만 하다.

  ```python
  # 올바른 코드
  i = i + 1
  submitted += 1
  x = x*2 - 1
  # 아래 연산에서 가장 낮은 우선순위를 갖는 +의 앞뒤에만 공백을 준다.
  hypot2 = x*x + y*y
  # 아래 연산에서 가장 낮은 우선순위를 갖는 *의 앞뒤에만 공백을 준다.
  c = (a+b) * (a-b)
  
  # 잘못된 코드
  i=i+1
  submitted +=1
  x = x * 2 - 1
  hypot2 = x * x + y * y
  c = (a + b) * (a - b)
  ```
  - 함수의 자료형을 명시할 때의 콜론의 뒤와 화살표 양측에는 항상 공백이 있어야 한다.

  ```python
  # 올바른 코드
  def munge(input: AnyStr):
      pass
  def munge() -> AnyStr:
      pass
  
  # 잘못된 코드
  def munge(input:AnyStr):
      pass
  def munge()->AnyStr:
      pass
  ```

  - 함수의 자료형을 명시했을 때, 기본값을 설정해준다면 `=`의 조우에 공백을 사용해야 한다.

  ```python
  # 올바른 코드
  def munge(sep: AnyStr = None):
      pass
  def munge(input: AnyStr, sep: AnyStr = None, limit=1000):
      pass
  
  # 잘못된 코드
  def munge(input: AnyStr=None):
      pass
  def munge(input: AnyStr, limit = 1000):
      pass
  ```



# 주석

- 일반 규칙
  - 코드와 모순되는 주석은 주석이 없는 것 보다 나쁘다.
  - 주석은 완전한 문장이어야한다.
    - 첫 번째 단어는 소문자로 시작하는 식별자가 아닌 경우 대문자로 입력해야 한다.
  - 마지막 문장을 제외하고 여러 문장으로 된 주석에서 문장 끝나는 부분 뒤에 2 spaces를 사용해야 한다.
  - 주석은 영어로 작성해야 한다.



- 블록 주석

  - 블록 주석의 각 행은 # 및 하나의 공백으로 시작한다.
  - 블록주석은 주석에 해당하는 코드와 동일한 수준으로 들여쓰기 해야한다.

  ```python
  for i in range(5):
      # If i is 3.
      if i==3:
          do_something()
  ```

  - 블록 주석 내부의 단락은 `#`하나로 공백 행을 주는 것으로 구분한다.

  ```python
  # Some comment
  #
  # Some comment
  ```



- 인라인 주석

  - 명령문과 같은 줄에 있는 주석을 말한다.
  - 명령문과 둘 이상의 공백으로 구분하여 작성한다.
  - 마찬가지로 `#` 기호와 공백 하나로 시작한다.

  - 꼭 필요한 경우를 제외하고 사용을 지양하는 것이 좋다.



- Docstrings

  - 공개된 모든 모듈, 함수, 클래스 및 메서드에 Docstring을 작성해야 한다.
    - 공개되지 않은 메서드에는 꼭 작성할 필요는 없다.
  - 한 줄일 경우
    - 여는 따옴표와 닫는 따옴표도 한 줄에 작성한다.
    - docstrings 윗 줄과 아랫줄에 공백을 넣지 않는다.
    - `Do this`, `Return that`과 같이 최대한 간결하게 작성하고, 상세한 설명은 지양한다.
    - 단순히 함수의 내용을 반복하는 서명과 같이 작성해서는 안된다.

  ```python
  # 올바른 코드
  def kos_root():
      """Return the pathname of the KOS root directory."""
      global _kos_root
      if _kos_root: 
          return _kos_root
  
  def function(a, b):
      """Do X and return a list."""
      my_list = [a, b]
      return my_list
      
  # 잘못된 코드
  # 단순히 함수의 내용을 반복하는 서명과 같이 작성해서는 안된다.
  def function(a, b):
      """function(a, b) -> list"""
      my_list = [a, b]
      return my_list
  ```

  - 여러 줄일 경우

    - 다양한 스타일이 존재한다.
    - Sphinx Style: Python documentation을 위한 스타일
    - Google Style: 함수에 대한 짤막한 설명, parmeter, return 값에 대한 설명을 작성.

    - 이 외에도 다양한 스타일이 존재한다.
    - 여는 따옴표는 첫 줄과 함께 작성해도 되고, 따로 작성해도 된다.

  ```python
  # Google Style의 예시
  def add_two_numbers(num1, num2):
      """Returns the sum of two numbers
      
      Args:
          num1 (int): First number to add
          num2 (int): Second number to add
      
      Returns:
          int: Sum of `num1` and `num2`
     """
  ```



# 명명 규칙

- 명명 스타일

  - Python에서는 기본적으로 다음과 같은 규칙을 사용한다.
    - class Exception: 파스칼 표기법
    - 변수, 함수: 스네이크 표기법
    - 모듈: 무조건 소문자로만 적는다.
  -  여러 표기법
  
  | 표기법                                                       | 명칭            | 예시                               |
  | ------------------------------------------------------------ | --------------- | ---------------------------------- |
  | 단일 소문자                                                  |                 | b                                  |
  | 단일 대문자                                                  |                 | B                                  |
  | 소문자                                                       |                 | foo                                |
  | 대문자                                                       |                 | FOO                                |
  | 소문자와 밑줄 결합                                           | 스네이크 표기법 | lower_case_with_undersocres        |
  | 대문자와 밑줄 결합                                           |                 | UPPER_CASE_WITH_UNDERSOCRES        |
  | 각 단어의 첫 글자를 대문자로 적되, 맨 앞에 오는 글자는 소문자로 표기 | 캐멀 표기법     | mixedCase                          |
  | 각 단어의 첫 글자를 대문자로 표기                            | 파스칼 표기법   | CapitalizedWord                    |
  | 접두어로 자료형을 표기                                       | 헝가리안 표기법 | strFirstName                       |
  | 소문자, 대문자, undersocore 조합                             |                 | Capitalized_Words_With_Underscores |
  



- Python keyword와 충돌을 피해야 할 때는 변수명 뒤에 `_`를 붙인다.

  - 예시
    - `from`은 python keyword이기에 사용이 불가능하다.
    - 따라서 뒤에 `_`를 붙여준다.

  ```python
  from_ = "2021-11-12"
  until = "2021-11-14"
  ```



# SQL Formatting

- pep8에서는 따로 SQL query에 대한 명명 규칙을 정해 놓지는 않았다.
  - 아래 내용은 SQL query를 Python 스럽게 작성하는 방법을 찾아본 것이다.
  - 아래에서 소개한 방법 말고도 더 나은 방법이 있을 수 있다.
  - 핵심은 보다 깔끔하고 눈에 잘 들어오는 sql 형식의 문자열을 만드는 것이다.



- 일반적으로 쿼리문 자체는 쌍따옴표(`"`)로 묶는 것이 권장된다.
  - 작은 따옴표(`'`)는 쿼리문 내에서 사용되기 때문이다.



- 소괄호를 사용하는 방법

  - 소괄호를 사용하여 긴 문자열을 보다 깔끔하게 만들 수 있다.

  ```python
  sql = (
      "select * "
      "from my_table "
      "where name = 'theo'"
  )
  
  print(sql)	
  # select * from my_table where name = 'theo'
  ```

  - 각 문장의 끝에 공백을 넣어줘야 한다는 단점이 있다.



- triple quotes을 사용하는 방법

  - 일반적으로는 docstring을 작성할 때 사용하지만 sql query를 작성할 때도 유용하다.

  ```python
  sql = """
  	select * 
  	from my_table
  	where name = 'theo'
  """
  print(sql)
  """
          select * 
          from my_table
          where name = 'theo'
  """
  ```

  - 위 처럼 공백과 줄 바꿈이 발생하지만 DB가 인식하는 데는 아무런 문제가 없다.



- SQL Paramstyle

  - sql문에 변수를 포함시키는 방식에는 아래와 같은 것들이 있다.

  | paramstyle | 설명                                           |
  | ---------- | ---------------------------------------------- |
  | qmark      | 물음표 활용(e.g. where name=?)                 |
  | numeric    | 숫자 활용(e.g. where name=:1)                  |
  | named      | 변수명 활용(e.g. where name = :name)           |
  | format     | ANSI C printf format 활용(e.g. where name=%s)  |
  | pyformat   | Python format 활용(e.g. where name = %(name)s) |

  - 각 DB library별로 권장하는 스타일이 다른데 이는 아래와 같이 확인 가능하다.
    - 대부분의 DB library가 `paramstyle`라는 변수에 자신들이 권장하는 스타일을 저장해놓았다.

  ```python
  pymysql.paramstyle
  'pyformat'
  
  MySQLdb.paramstyle
  'format'
  
  mysql.connector.paramstyle
  'pyformat'
  
  # Postgresql
  psycopg2.paramstyle
  'pyformat'
  
  # Oracle
  cx_Oracle.paramstyle
  'named'
  
  # Sqlite3
  sqlite3.paramstyle
  'qmark'
  ```

  - 각 library가 권장하는 방식을 사용하면 된다.



