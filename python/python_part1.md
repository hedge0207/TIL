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

  - 공백
    - 들여쓰기는 공백 4칸을 권장
    - 한 줄은 최대 79자까지
    - 최상위 함수와 클래스 정의는 2줄씩 띄어 쓴다.
    - 클래스 내의 메소드 정의는 1줄씩 띄어 쓴다.
    - 변수 할당 앞 뒤에 스페이스를 하나만 사용한다.
  - 네이밍 규칙
    - 단일 글자 변수로 l(소문자 L), I(대문자 I), O(대문자 O)를 사용하지 않는다.
    - Producted 인스턴스 속성은 밑줄 하나로 시작한다.
    - Private 인스턴스 속성은 밑줄 두 개로 시작한다.
    - 모듈 수준의 상수는 모두 대문자로 구성한다.
    - 클래스 내 인스턴스 메서드에서 첫 번째 파라미터의 이름을 self로 지정한다.
    - 클래스 메서드의 첫 번째 파라미터의 이름은 cls로 지정한다.
  - 표현식과 문장
    - `if not A is B` 보다 `if A is not B`를 사용하는 것이 낫다.
    - 함수의 return 값이 없을 경우 `return None`을 확실하게 명시한다.
    - 항상 파일 맨 위에 import 문을 적는다.
    - import시에 한 모듈당 한 줄을 사용한다.
    - import 순서는 표준 라이브러리 모듈-서드파티 모듈-자신이 만든 모듈 순이다.
  - 스타일 가이드를 준수했는지 확인해주는 `pylint`라는 라이브러리가 있다. pycharm에는 내장되어 있다.





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



- 주석

  - 한 줄 주석은 `#`으로 표현한다.
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

  ```python
  print("hello! ");print("world!")
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



## 자료형

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

  

### Tuple

- 튜플 생성

  - 소괄호로 묶어서 생성할 수도 있고
  - 소괄호를 생략하고 콤마로만 구분해서 생성할 수도 있다.
  - 튜플의 원소가 하나일 경우, 반드시 마지막에 콤마를 찍어야 한다.
  - `tuple()` 생성자를 사용할 수도 있다.

  ```python
  tup1 = (1,2,3)
  tup2 = 1,2,3
  tup3_1 = 1
  tup3_2 = 1,
  tup4 = tuple("abcde")
  
  print(type(tup1))	# <class 'tuple'>
  print(type(tup2))	# <class 'tuple'>
  print(type(tup3_1))	# <class 'int'>
  print(type(tup3_2)) # <class 'tuple'>
  print(tup4)			# ('a', 'b', 'c', 'd', 'e')
  ```

  

- 튜플의 특징

  - 튜플을 포함한 모든 자료형이 튜플에 포함될 수 있다.
  - 순서가 있다.
  - 한 번 생성되면 값을 변경할 수 없다.
    - 그러나 + 연산, * 연산은 가능하다.
  - 튜플을 활용하면 여러 값을 한 번에 각기 다른 변수에 할당하는 것이 가능하다.
    - 상기했듯 굳이` ()`로 묶지 않아도 콤마로 구분만 되어 있으면 튜플이 생성된다.
  - 튜플의 해제 할당 기능을 사용하면 두 변수의 값을 바꾸는 것도 가능하다.

  ```python
  # 순서가 있으므로 인덱스를 통해 접근이 가능하다.
  tup = ('one','two', 'three')
  print(tup[0:2])    # ('one', 'two')
  
  # 값을 변경할 수 없다.
  tup[0] = 'zero'   # 'tuple' object does not support item assignment
  
  # +, * 연산은 가능하다.
  tup1 = (1,2,3)
  tup2 = (4,5,6)
  print(tup1+tup2)  # (1, 2, 3, 4, 5, 6)
  print(tup1*2)     # (1, 2, 3, 1, 2, 3)
  
  # 여러 값을 변수에 한 번에 할당하는 것이 가능하다.
  email,phone = "email@email.com", "010-1234-5678"
  print(email,phone)   # email@email.com 010-1234-5678
  
  # 두 변수의 값을 바꾸는 것도 가능하다.
  email, phone = phone, email
  print(email,phone)   # 010-1234-5678 email@email.com
  ```

  

### List

- 리스트 생성

  - `list()` 생성자를 사용하여 생성이 가능하다.
  - `[]` 로 생성이 가능하다.

  ```python
  lst1 = list()
  lst2 = []
  print(type(lst1))  # <class 'list'>
  print(type(lst2))  # <class 'list'>
  ```

  

- 리스트 특징

  - 리스트를 포함한 모든 자료형이 리스트에 포함될 수 있다.
  - 순서가 있다.
  - 한 번 생성된 값을 변경 가능하다.

  ```python
  # 순서가 있으므로 인덱스를 통해 접근이 가능하다.
  lst = ['one', 'two', 'three']
  print(lst[0:2])   # ['one', 'two']
  
  # 변경이 가능하다.
  lst[0] = 'zero'
  print(lst)        # ['zero', 'two', 'three']
  ```

  

- 리스트 관련 메서드

  > 아래 메서드들 중 일부는 튜플, 문자열 등에서도 사용 가능하다.

  - `len()`: 요소의 개수를 반환

  ```python
  lst = [1,2,3]
  print(len(lst))   # 3
  ```

  - `.append()`: 요소를 추가

  ```python
  lst = [1,2,3]
  lst.append(4)
  print(lst)   #[1, 2, 3, 4]
  ```

  - `.insert(인덱스, 추가할 값)`: 지정한 인덱스에 값을 삽입

  ```python
  lst = [1,2,3]
  lst.insert(1,4)
  print(lst)   # [1, 4, 2, 3]
  ```

  - `.remove()`: 요소를 삭제

  ```python
  lst = [1,2,3]
  lst.remove(1)
  print(lst)  # [2,3]
  ```

  - `del`: 요소를 삭제
    - `remove`와의 차이는 `remove`는 삭제할 값을 지정하지만 del은 삭제할 인덱스를 지정한다는 것이다.

  ```python
  lst = [1,2,3]
  del lst[1]
  print(lst)  # [1,3]
  ```

  - `.pop()`: 리스트의 마지막 요소를 삭제 후 반환

  ```python
  lst = [1,2,3]
  # 삭제 후 반환한다.
  print(lst.pop())  # 3
  print(lst)		  # [1,2]
  ```

  - `.clear()`: 모든 요소 삭제

  ```python
  lst = [1,2,3]
  lst.clear()
  print(lst)      # []
  ```

  - `.reverse()`: 순서를 뒤집는다.

  ```python
  lst = [1,2,3]
  lst.reverse()
  print(lst)    # [3, 2, 1]
  ```

  - `.sort()`: 정렬한다.

  ```python
  lst = [9,3,6]
  lst.sort()
  print(lst)    # [3,6,9]
  ```

  - `sorted()`: 정렬한다.
    - `.sort()`와의 차이는 원본 배열을 변경하지 않는다는 것이다.

  ```python
  lst = [9,3,6]
  print(sorted(lst))  # [3,6,9]
  print(lst)			# [9,3,6]
  ```

  - `.copy()`
    - 복사에는 얕은 복사와 깊은 복사가 있는데 `.copy()`를 사용하면 깊은 복사가 가능하다.
    - `[:]`를 활용해도 깊은 복사가 가능하다.

  ```python
  # 얕은 복사
  lst1 = [1,2,3]
  lst2 = lst1  
  lst2[0] = 9
  # 얕은 복사이기에 같은 객체를 가리키고 있어 하나를 변경하면 둘 다 변경된다.
  print(lst1,lst2)  # [9, 2, 3] [9, 2, 3]
  
  # 깊은 복사
  lst1 = [1,2,3]
  lst2 = lst1.copy()
  lst2[0] = 9
  # 깊은 복사이기에 서로 다른 객체를 가리키고 있어 하나를 변경해도 다른 하나는 변경되지 않는다.
  print(lst1,lst2)  # [1, 2, 3] [9, 2, 3]
  
  # [:]를 활용한 깊은 복사
  lst1 = [1,2,3]
  lst2 = lst1[:]
  lst2[0] = 9
  print(lst1,lst2)  # [1, 2, 3] [9, 2, 3]
  ```



### Dictionary

- 생성

  - `dict()`생성자를 사용해 생성 가능하다.
  - `{}`를 사용해 생성 가능하다.

  ```python
  dict1 = dict()
  dict2 = {}
  print(type(dict1))  # <class 'dict'>
  print(type(dict2))  # <class 'dict'>
  ```

  

- 딕셔너리의 특징

  - 키(key)-값(value) 쌍을 요소로 갖는 자료형이다.
  - 키는 중복이 불가능하다.
    - 키를 중복으로 사용할 경우 하나의 키를 제외한 모든 중복된 키는 무시된다.
  - 키는 변경 immutable 타입이어야 하며 값은 immutable과 mutable 모두 가능하다.
    - 변경 불가능한 문자열이나 튜플 등은 키가 될 수 있다.
    - 변경 가능한 리스트는 키가 될 수 없다.
    - 값에는 딕셔너리를 포함한 모든 자료형이 올 수 있다.
  - 순서가 없는 자료형으로 key를 통해 값에 접근해야 한다.
  - 이미 입력된 값의 변경이 가능하다.
  - 요소의 추가와 삭제가 가능하다.

  ```python
  # key에는 변경 불가능한 자료형이, 값에는 모든 자료형이 올 수 있다.
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28,"가족":{"엄마":"김엄마","아빠":"홍아빠"}}
  
  # key를 통해 값에 접근할 수 있다.
  print(my_dict['이름'])  	  # 홍길동
  
  # 변경이 가능하다.
  my_dict['나이']=14
  print(my_dict['나이']) 	  # 14 
  
  # 요소(키-값) 추가
  my_dict["email"] = "email@email.com"
  print(my_dict["email"])    # email@email.com
  
  
  # 요소(키-값) 삭제
  del my_dict['email']
  print(my_dict)  # {'취미': ['축구', '야구'], '이름': '홍길동', '나이': 14, '가족': {'엄마': '김엄마', '아빠': '홍아빠'}}
  ```



- 딕셔너리 관련 함수

  - `.keys()`: key를 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.keys())  # dict_keys(['취미', '이름', '나이'])
  ```

  - `.values()`: 값을 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.values())  # dict_values([['축구', '야구'], '홍길동', 28])
  ```

  - `.items()`: 키-값 쌍을 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.items()) # dict_items([('취미', ['축구', '야구']), ('이름', '홍길동'), ('나이', 28)])
  ```

  - `.clear()`: 모든 요소 삭제

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  my_dict.clear()
  print(my_dict)  # {}
  ```

  - `.get()`: 키로 값 얻기
    - 그냥 키로만 접근하는 것과의 차이는 존재하지 않는 키로 접근할 경우, 키로만 접근하면 error가 발생하지만,  `.get()`은 None을 반환한다는 것이다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict['email'])		 # KeyError: 'email'
  print(my_dict.get('email'))  # None
  ```

  

### Set

- 생성

  - 다른 자료형들과 달리 set은 `set()` 생성자로만 생성할 수 있다.
  - 반드시 문자열 또는 괄호로 묶어줘야 한다(괄호의 종류는 상관 없다).
  - 비어있는 자료형도 생성 가능하다.

  ```python
  my_set1 = set({1,2,3})
  my_set2 = set("Hello!")
  my_set3 = set()
  
  print(type(my_set1))  # <class 'set'>
  print(type(my_set2))  # <class 'set'>
  print(my_set1)		  # {1, 2, 3}
  print(my_set2)		  # {'l', '!', 'o', 'e', 'H'}
  print(my_set3)        # set()
  ```

  

- Set(집합) 자료형의 특징

  - 중복을 허용하지 않는다.
  - 순서가 없다.

  ```python
  my_set = set("Hello!")
  
  print(my_set2)		  # {'l', '!', 'o', 'e', 'H'}
  # 중복을 허용하지 않기에 두 번 들어간 l은 하나만 들어가게 된다.
  # 순서가 없기에 순서대로 들어가지 않는다.
  ```

  

- 교집합, 합집합, 차집합 구하기

  ```python
  my_set1 = set([1,2,3])
  my_set2 = set([3,4,5])
  
  # 교집합
  print(my_set1 & my_set2)				# {3}
  print(my_set1.intersection(my_set2))	# {3}
  
  # 합집합
  print(my_set1 | my_set2)				# {1, 2, 3, 4, 5}
  print(my_set1.union(my_set2))			# {1, 2, 3, 4, 5}
  
  # 차집합
  print(my_set1-my_set2)					# {1, 2}
  print(my_set1.difference(my_set2))		# {1, 2}
  print(my_set2-my_set1)					# {4, 5}
  print(my_set2.difference(my_set1))		# {4, 5}
  ```

  

- 집합 관련 함수들

  - `.add()`: 요소를 1개 추가한다.

  ```python
  my_set = set([1,2,3])
  my_set.add(4)
  print(my_set)   # {1, 2, 3, 4}
  ```

  - `.update()`: 요소 여러 개 추가하기

  ```python
  my_set = set([1,2,3])
  my_set.update([4,5,6])
  print(my_set)   # {1, 2, 3, 4, 5, 6}
  ```

  - `.remove()`: 특정 요소 제거하기

  ```python
  my_set = set([1,2,3])
  my_set.remove(2)
  print(my_set)   # {1, 3}
  ```

  

## 자료형의 변경

- `str()`, `int()`, `float()`, `bool()` 등의 함수를 사용해서 변경하면 된다.



- 주의점

  - `int()`의 경우 숫자가 아닌 것을 숫자로 변환할 수 없으며, 소수점이 있는 숫자 형식의 문자열을 정수형으로 변환할 수 없다.
  - 소수점이 없는 숫자 형식의 문자열은 정수형으로 변환이 가능하다.
  - 소수점이 있든 없든 숫자 형식이기만 하면 실수형으로 변환이 가능하다.
  - 변환 함수는 변환된 값을 반환할 뿐 실제로 자료형을 변경시키는 것은 아니다.

  ```python
  # 숫자 형식인 문자열의 정수와 실수 변환
  chr = "1"
  print(type(int(chr)))		# <class 'int'>
  print(type(float(chr)))		# <class 'float'>
  
  # 변환 함수는 변환된 값을 반환만 할 뿐이다.
  var = True
  print(type(str(var)))	# <class 'str'>
  print(type(var))		# <class 'bool'>
  
  # 아래와 같이 재할당 해주거나 다른 변수에 담아서 사용해야 한다.
  var = True
  var = str(var)
  print(type(var))		# <class 'str'>
  ```

  