# 기초

### 1. 식별자와 예약어

 1)식별자:  변수, 함수, 모듈, 클래스 등을 식별하는데 사용되는 이름, 이름을 정의하여 필요할 때 사용하는 것.

   ex.  a = 3 에서 a가 식별자(이 경우 변수 이면서 식별자).

- 식별자의 규칙

  ①영문 알파벳, 밑줄(_), 숫자로 구성된다.

  ​    -띄어쓰기를 사용할 수 없기에 주로 스네이크 케이스와 캐멀 케이스라는 두 가지 방식을 사용한다.

  ​     ex. snake_case, CamelCase

  ②첫 글자로 숫자는 사용할 수 없다.

  ③길이에 제한이 없다.

  ④대소문자를 구분한다.

  ⑤예약어는 사용할 수 없다.

  ⑥내장함수나 모듈 등의 이름으로도 만들면 안된다.

     -함수에서 ()를 빼면 식별자다. 즉 함수의 이름은 식별자의 일종이다.

  ​    ex. print()라는 함수에서 print는 식별자다.

  ex. 내장함수로 식별자를 만드는 경우

  ```python
  str = 3										#내장함수인 str에 3을 넣을 경우 출력은 되지만
  print(str)
  
  out
  3
  ------------------------------------------
  
  a = str(5)
  print(a)
  
  out
  TypeError: 'str' object is not callable  	#더 이상 본래의 기능을 하지 못하게 된다.
  -------------------------------------------
  
  del str										#del을 통해 str에 부여된 값을 지우면 다시 원래												대로  사용할 수 있다.
  a = str(5)									
  print(a)
  
  out
  5
  ```

  

 2)예약어:  파이썬 내에서 특정 의미로 사용하는 이름, 파이썬이 이미 정의한 식별자.

 -False, None, True, and, as, assert, break, class, continue, def, del, elif, else, except, finally, for, from,  global, if, import, in, is, lambda, nonlocal, not, or, pass, raise, return, try, while, with, yield

```python
import keyword
print(keyword.kwlist)  #이 과정을 통해 예약어를 확인할 수 있다.


out
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
---------------------------------------------------------------------------------------
ex. 예약어를 식별자로 만드려고 할 경우
False = 3
print(False)

out
SyntaxError: can't assign to keyword       #할당할 수 없는 식별자라는 오류가 출력
```



### 2. 기초문법

인코딩은 선언하지 않더라도 `UTF-8`로 기본 설정이 되어있습니다. 만약, 인코딩을 설정하려면 코드 상단에 아래와 같이 선언합니다. 주석으로 보이지만, Python `parser`에 의해 읽혀집니다.

```python
# -*- coding: <encoding-name> -*- 
```

1)주석

   (1)주석은 #으로 표현한다.

```python
print("a")
# print("b")

out
a						#print("b")는 주석처리 되어 출력되지 않는다.
```



  (2)docstring은 """(큰 따옴표 3개)으로 표현한다.

- 이를 활용하여 여러 줄의 주석을 작성 할 수 있으며, 보통 함수/클래스 선언 다음에 해당하는 설명을 위해 활용.

- 파이썬 내에서도 함수의 상세설명을 누르면 표시되는 창은 docstring을 활용한 것이다.

  ```python
  def mysum(a, b):			#이 처럼 특정한 함수(이 경우엔 mysum)를 설명하기 위해 주로 사용
  """
  이 것은 덧셈 함수입니다.
  이 줄도 실행되지 않습니다.
  다만, docstring인 이유가 있습니다.
  """
  
  print(mysum.__doc__)		 #ㅏ정의한 함수.__doc__ㅓ을 통해 함수의 정의를 출력할 수 있다.
  
  out
      이 것은 덧셈 함수입니다.
      이 줄도 실행되지 않습니다.
  
      다만, docstring인 이유가 있습니다.
  ----------------------------------------
  
  
  print(sum.__doc__)					#사용자가 정의한 함수가 아닌 내장함수인 sum의                                                경우에도 마찬가지로 파이썬에서 정의한 sum의 정                                              의가 출력된다.
  out
  Return the sum of a 'start' value (default: 0) plus an iterable of numbers
  When the iterable is empty, return the start value.
  This function is intended specifically for use with numeric values and may
  reject non-numeric types.
  ```




  3)코드 라인

- 기본적으로 파이썬에서는 ;를 작성하지 않는다.

- 한 줄로 표기할 때는 ;를 작성하여 표기할 수 있다.

  ```python
  print('hello!')
  print('world')
  
  out
  hello!
  world
  -------------------------------
  
  print('hello!')print('world')
  
  out
  SyntaxError: invalid syntax
      
  
  print('hello!');print('world')		#이렇게 할 수는 있지만 가독성이 떨어져 권장하지는 않는다.
  
  out
  hello!
  world
  ```

  

- 여러줄 작성할 때는 역슬래시ㅏ\ㅓ를 사용하여 아래와 같이 할 수 있다.  

- [], {}, ()는 역슬레쉬 없이도 다능하다.

  ```python
  print('
   dd')
        
  out
  
  SyntaxError: EOL while scanning string literal
  #--------------------------------------------------
  print('\				#이처럼 \를 활용하면 여러줄로 작성할 수 있지만 역시 권장되지 않는다.
  dd')
        
  out
  
  dd
  #---------------------------------------------------
  lunch = [
      '자장면','탕수육',
      '군만두','물만두',
  ]                           #둘 모두 가능하지만 아래와 같이 쓰지는 않는다.
                              #또한 물만두 뒤의 ,는 나중에 수정을 편하게 하기 위해 붙이는 것으로  lunch = [ 				  	  스타일에 따라 안붙여도 된다.
      '자장면','탕수육',
      '군만두','물만두',
  (들여)]
  
   #pep8 가이드에 따르면 여러 줄의 생성자의 닫히는 괄호(소, 중, 대)는 마지막 줄의 공백이 아닌 첫번째 문자(요소) 위치에 오거나 마지막 줄에서 생성자가 시작되는 첫번째 열에 위치한다.
  ```

- 혹은 """를 활용하여 여러 줄로 작성하는 방법도 있다.

  ```python
  print("""
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  """)
  
  out						#결과는 이처럼 한 줄 띄어서 출력되고 마지막 줄 뒤에도 한 줄이 띄어진다.
  (한 줄 띄고)
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  (한 줄 띄고)
  
  # """\, \"""를 통해 이를 수정할 수 있다.
  print("""\
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세\
  """)
  
  out						#"""와 \를 함께 쓰면 첫 줄과 마지막 줄에 한 줄이 띄어지지 않는다.
  동해물과 백두산이
  마르고 닳도록
  하느님이 보우하사
  우리나라 만세
  ```

  

- 띄어쓰기는 문자열 내에서만 허용되며 콤마 없이 둘 이상의 자료형을 동시에 사용할 수 없다.

  ```python
  print("안녕 하세요")
  print(123 456)
  print("123 456")
  print("안녕"15)
  print("안녕",15)
  
  out
  안녕 하세요
  오류
  123 456
  오류
  안녕 15
  ```



### 3. 변수 및 자료형



- 변수란 값을 저장할 때 사용하는 식별자를 의미한다. 상자에 물건을 넣는 것으로 이해하면 쉽다.

  ex. pi = 3.14 라고 했을 때 pi는 변수(인 식별자)이고 3.14는 pi라는 상자에 들어간 물건이다.

   -변수의 주요 개념에는 선언, 할당, 참조가 있다.

   -변수의 선언이란 변수를 생성하는 것으로  파이썬에서는 변수 이름을 적기만 하면 된다.

    ex. pi

   -변수의 할당이란 변수에 값을 할당하는 것으로 "="기호를 사용한다. "="는 우변의 값을 좌변의 값에 넣겠다           는 의미이다.

​         ex. pi = 3.14

​         -변수의 참조란 변수에 할당된 닶을 꺼내는 것을 의미한다.

​         ex. 2pi == 6.28

- 복합 대입 연산자

  -변수를 활용하면 기존의 연산자와 조합해서 사용할 수 있는 연산자

  -숫자형은 아래 예시에 나와있는 것들을 사용할 수 있으며 문자열도 +=와 *=는 사용 가능하다.

  ```python
  num = 10			word = "안녕"
  num += 1			word += "하세요"
  print(num)			print(word)
  num -= 2			word *= 3
  print(num)			print(word)
  num *= 2
  print(num)
  num /= 3
  print(num)
  num %= 4
  print(num)
  num **= 2
  print(num)
  
  out
  11					안녕하세요
  9					안녕하세요안녕하세요안녕하세요
  18
  6.0
  2.0
  4.0
  ```

- 숫자는 정수형과 실수형이 있다. 정수(integer)형은 소수점이 없는 숫자를 의미하고 실수형(floating point, 부동소수점)은 소수점이 있는 숫자를 의미한다. 같은 수를 나타내고 있다고 하더라도 소수점이 있다면 실수형이다. 

​        ex. 7은 정수형이지만 7.00은 실수형이다.

- 실수형은 우리가 기존에 표현하던 방식대로 표현할 수도 있지만 e를 사용하여 "컴퓨터식 지수 표현 방식"으로 표현하기도 한다.

  ```python
  print(41.123*10**2)
  print(41.123e2)
  print(41.123E2)
  print(41.123*10**-2)
  print(41.123e-2)
  
  out
  4112.3
  4112.3
  4112.3
  0.41123
  0.41123
  ```

  





- input()함수는 사용자로부터 데이터를 입력 받는 함수이다. ()안에 들어가는 내용, 혹은 사용자가 입력하는 내용을 프롬프트 문자열이라고 하며 그 이름에 맞게 무엇을 입력해도 문자열 자료형이 된다.

  ```python
  print(type(input(5756)))
  print(type(input(Ture)))
  print(type(input("안녕하세요")))
  
  out
  <class 'str'>
  <class 'str'>
  <class 'str'>
  ```

  

- 자료형 변경

  -str(), int(), float()을 사용

  -int()의 경우 숫자가 아닌 것을 숫자로 변환할 수 없으며 소수점이 있는 숫자 형식의 문자열을 정수형으로 변환할 수 없다.

  -또한 변환 함수를 쓴다고 자료형이 영구히 바뀌는 것도 아니다.

  ```python
  a = "123"
  print(type(int(a)))
  print(type(float(a)))
  b = "안녕"
  print(type(int(b)))
  print(type(float(b)))
  c = "123.45"
  print(type(int(c)))
  
  out
  <class 'int'>
  <class 'float'>
  오류
  오류
  오류
  
  
  d = "789"
  int(d)				#변환 함수는 영구히 바뀌는 것은 아니다.
  print(type(d))
  d = int("789")
  print(type(d))		#계속 바꾸려면 변수에 새로운 값을 할당해야한다.
  
  out
  <class 'str'>
  <class 'int'>
  ```



1. 문자열 포맷팅

   1) ㅏ"{}".format()ㅓ함수를 사용할 수도 있다. 이는 중괄호 안에 소괄호에 들어간 숫자형 자료를 문자
      형으로 바꿔서 입력해주는 함수이다. 숫자형 외에 부동소수점형과 문자형도 가능하다.  또한 {}자체
      를 출력하고 싶으면 {{}}처럼 중괄호 안에 중괄호를 입력하면 된다.

```python
a = "{}".format(10)
b = "{}만 원".format(50)
c = "열심히 해서 성적이 {}% 올랐다.".format(40)
d = "내 키는 {}이다."format(162.4)
e = "나는 {}다.".format("남자")
print(a)
print(b)

out
10
50만 원
열심히 해서 성적이 40% 올랐다.
내 키는 162.4이다.
나는 남자다.
```

-format()함수의 기능

  ```python
#1. f와 d, 그리고 g
#중괄호 안에 :를 넣고 콜론 우측에 d를 넣으면 정수형이, f를 넣으면 부동소수점형이 입력되는데 이 때 d의 경우 소괄호에는 무조건 정수형이 와야 하지만 f의 경우 부동소수점뿐 아니라 정수형도 입력 가능하다. 또한 f의 경우 앞에 ㅏ.숫자ㅓ를 써주면 소수점이 그 숫자만큼만 출력된다.
#콜론 좌측에 g를 쓰면 의미없는 소수점인 0이 제거된 상태로 출력된다.
print("{:d}".format(555))
print("{:d}".format(555.22))
print("{:f}".format(555.22))
print("{:f}".format(555))
print("{:.1f}".format(555.222))
print("{}".format(77.0))
print("{:g}".format(77.0))

out
555
오류
555.22
555.000000
555.2
77.0
77

#2. 특정 칸에 출력하기
#콜론 우측에 숫자를 넣으면 그 숫자만큼 띄운 후 값이 출력된다.
#또한 <(좌),>(우),^(중앙)를 활용하여 정렬의 방향을 설정할 수 있다. 이렇게 기호를 사용하여 정렬한 경우 기호 앞에 채우고 싶은 문자를 입력할 수 있다.
print("{:5}".format(555))
print("{:10}".format(555))
print("{:<10}123".format("555"))
print("{:>10}123".format("555"))
print("{:^10}123".format("555"))
print("{:=^10}123".format("555")) #공백을 "="로 채우겠다.
print("{:a<10}123".format("555")) #공백을 "a"로 채우겠다.

out
  555
       555
555       123
       555123
   555    123
===555====123
555aaaaaaa123

#3. 빈칸을 0으로 채우기
#콜론 우측에 0을 입력하고 이어서 띄울 숫자를 입력하면 그 빈칸이 0으로 채워진다. 부동소수점도 같은 방법을 사용한다.
print("{:05}".format(555))
print("{:010}".format(555))

out
00555
0000000555

#4. 기호 붙여 출력하기
#양수와 음수를 함께 출력할 경우 양수는 보통 +를 붙이지 않으므로 둘의 위치가 않맞게 된다. 따라서 콜론 우측에 +를 쓰거나 한칸 띄움으로써 이를 맞춰줄 수 있다. 부동소수점도 같은 방법을 사용한다.
print("{:}".format(555))
print("{:}".format(-555))

out
555
-555            #맞지 않는다.
#+를 사용
print("{:+}".format(555))
print("{:+}".format(-555))

out
+555
-555

#띄어쓰기를 사용
print("{: }".format(555))
print("{: }".format(-555))
out
 555
-555

#5. 인덱싱
#여러개를 동시에 쓰고 싶은 경우 중괄호 안에 0부터 번호를 매기면 되며 번호를 매기지 않아도 순차적으로 소괄호 안의 값이 입력된다.
print("나는 {}와 {}와 {}를 가지고 싶다".format("사과","키위","포도"))
print("나는 {1}와 {2}와 {0}를 가지고 싶다".format("사과","키위","포도"))

out
나는 사과와 키위와 포도를 가지고 싶다
나는 키위와 포도와 사과를 가지고 싶다

#6. 일렬로 작성하지 않아도 된다.
print("{}{}{}{}".format(
    "a",
    "b",
    "c",
    "d"
    ))

out
abcd
  ```

 

 2)  포맷 코드를 활용한 방식

- "%x"%()가 기본 형식이다. x자리에 아래와 같은 문자를 입력하면 된다. %s의 경우 어떤 숫자를 입력하든 모두 문자열로 바뀌어서 입력된다.

| %s             | %c                  | %d                        | %f                       |
| -------------- | ------------------- | ------------------------- | ------------------------ |
| 문자열(String) | 문자 1개(character) | 정수(Integer)             | 부동소수(floating-point) |
| %o             | %x                  | %%                        |                          |
| 8진수          | 16진수              | Literal % (문자 `%` 자체) |                          |

```python
print("%s"%('나무'))
print("저건 %s다"%('나무'))
print("%d"%(58))
print("나는 %d키로다"%(58))
print("%f"%(58.123))
print("강수량이 %s%% 증가했다"%(5))   #% 자체를 출력하고자 하는 경우
print(type("%s"%(123)))
print(type("%s"%(123.456)))


out
나무
저건 나무다
58
나는 58키로다
58.123000
강수량이 5% 증가했다
<class 'str'>
<class 'str'>
```

- format()함수와 마찬가지로 정렬과 소수점 표현이 가능하다.

  -format()함수에서는 콜론 우측에 이를 넣었다면 포맷 코드를 사용할 경우 %와 문자 사이에 넣어주면 된다.

  ```python
  #1 정렬
  #우측 정렬은 양의 정수를, 좌측 정렬은 음의 정수를 넣으면 된다.
  print("저기에 %s가 있다."%('나무'))
  print("저기에 %10s가 있다."%('나무'))
  print("저기에 %-10s가 있다."%('나무'))
  
  out
  저기에 나무가 있다.
  저기에         나무가 있다.
  저기에 나무        가 있다.
  
  
  #소수점 표현
  #%와 문자 사이에ㅏ.정수ㅓ를 넣어 표현 할 수 있다. 
  print("%f"%(11.2222))
  print("%.1f"%(11.2222))
  print("%.2f"%(11.2222))
  
  out
  11.222200
  11.2
  11.22
  ```



3)f-string 포맷팅(3.6버전부터 지원)

- f"{}"를 사용하여 중괄호 안에 들어가는 값을 문자로 바꾸는 방법

  ```python
  a = 157
  b = 170
  print(f"나는 {a}cm이고 쟤는 {b}cm이다.")
  print(f"나는 {157}cm이고 쟤는 {170}cm이다.")
  
  out
  나는 157cm이고 쟤는 170cm이다.
  나는 157cm이고 쟤는 170cm이다.
  ```



- 정렬과 소수점 표현 방식, 공백 채우기 등은 format()함수와 동일하다.

  ```python
  a = "나무"
  b = 111.22222
  print(f"저건{a}이다")
  print(f"저건{a:10}이다")
  print(f"저건{a:>10}이다")
  print(f"저건{a:!^10}이다")
  print(f"소수점은 {b:.2f}이렇게 표현한다")
  
  out
  저건나무이다
  저건나무        이다
  저건        나무이다
  저건!!!!나무!!!!이다
  소수점은 111.22이렇게 표현한다
  ```

-split함수는 문자열을 리스트형으로 나눈다. 뒤에 오는 소괄호에 특정 값을 입력하면 그 값을 기준으로 나눠주고 입력하지 않으면 공백(탭, 스페이스, 엔터)을 기준으로 나눠준다. 또한 기준이 된 값은 리스트에 담기지 않는다.

```
a = "Life is too short"
print(a.split())

b = "Lifeaisatooashort"
print(b.split(a))

out
['Life', 'is', 'too', 'short']
['Life', 'is', 'too', 'short']
```

-upper와 lower는 각기 문자열 전체를 각기 대문자와 소문자로 바꿔준다.

```python
print("Hello Everyone".upper())
print("Hello Everyone".lower())

out
HELLO EVERYONE
hello everyone
```

-count는 문자의 개수를, len은 문자열의 길이를 알려준다.

```
a = "happy"
print(a.count("p"))
print(len(a))

out
2
5
```





4) 문자열과 관련된 연산자

- 기본적으로 문자 연결 연산자인 +와 문자 반복 연산자인 *가 있다.

  (1) 문자 선택 연산자(인덱싱): [], []안에 들어가는 숫자를 인덱스라고 부른다.

​       -문자열 내부의 문자 하나를 선택하는 연산자. []안에 들어가는 숫자에 따라 그에 맞는 문자열이  출력.

​       -0부터 시작하며, 뒤에서부터 출력하고자 한다면 -1부터 시작하는 음수를 넣으면 된다.	


  ```python
print("안녕하세요"[0])
print("안녕하세요"[1])
print("안녕하세요"[2])
print("안녕하세요"[-1])
print("안녕하세요"[-2])

out
안
녕
하
요
세
  ```



  (2)문자열 범위 선택 연산자(슬라이싱): [:]

​     -문자열의 특정 범위를 선택할 때 사용하는 연산자.

​     -대괄호 내의 클론을 기준으로 왼쪽은 범위의 시작, 오른쪽은 범위의 마지막-1을 의미한다.

​     -둘 중 하나를 생략한 채로 실행할 수 있으며, 왼쪽을 생략한 경우 첫 글자부터, 오른쪽을 생략한 경우 마지막 글            	  자 까지 범위에 포함된다.

```python
print("안녕하세요"[1:4])
print("안녕하세요"[:4])
print("안녕하세요"[1:])

out
녕하세
안녕하세
녕하세요
```





3. 조건문

- Boolean(bool)은 오직 True(참)와 False(거짓) 값만 가진다. 

- None, 숫자 0과 0.0, 빈 컨테이너(빈 문자열, 빈 바이트열, 빈 리스트, 빈 튜플, 빈 딕셔너리 등)은 False로 반환되며 이 외에는 모두 True로 반환된다.

- bool()함수는 괄호 안에 들어간 값의 참과 거짓을 구별해 준다.

  ```python
  print(bool(123))
  print(bool(None))
  
  out
  True
  False
  ```

  

​     1) 비교 연산자

​         -비교연산자의 결과로 bool형이 출력된다.

​         -한글도 비교가 가능하며 사전 순서에 따라 앞에 있는 단어가 뒤에 있는 단어 보다 큰 값을 지닌다.

| ==   | !=     | >    | >=          | <    | <=          |
| ---- | ------ | ---- | ----------- | ---- | ----------- |
| 같다 | 다르다 | 크다 | 크거나 같다 | 작다 | 작거나 같다 |

​     2) 논리 연산자

| not                      | and                                                          | or                                                           |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 아니다. 불을 반대로 전환 | 그리고. 피연산자가 모두 참일 때 True를 출력하고 그 외에는 모두 False를 출력 | 또는. 피연산자가 모두 거짓을 때만 False를 출력하고 하나라도 참이면 True를 출력 |

​     3) if 조건문

- 조건에 따라 코드를 실행하거나, 실행하지 않게 만들 때 사용하는 구문. 조건문이 True면 아래 명령문이 실행되며 False면 실행되지 않는다.

  ```python
  #if 조건식 : 
  #(들여쓰기)명령문     #일반적으로 띄어쓰기 4칸이나 tab을 활용한다.
  #(들여쓰기)명령문
  #( 들여쓰기 )명령문-이 경우 이 명령문은 수행X(∵들여쓰기가 위의 두개와 다르다)
  
  if True:
      print("참")
  if False:
      print("거짓")    
  out()
  참
    #False이기에 뒤에 "거짓"은 출력되지 않는다.
  ```

​    4)else와 elif구문

​		(1)else는 if 조건문 뒤에 사용되어, if조건문의 조건이 거짓일 때 사용된다.

```python
#f 조건식 : 
#(들여쓰기)명령문1-true일 때 실행할 명령문
#(들여쓰기)명령문2-true일 때 실행할 명령문
#else 키워드 :
#(들여쓰기)명령문3-false일 때 실행할 명령문
#(들여쓰기)명령문4-false일 때 실행할 명령문

if True:
    print("참")
else:
    print("거짓")    
out()
참
```

​        (2)elif는 세 개 이상의 조건을 연결해서 사용하는 조건문

```python
#if 조건식 : 
#(들여쓰기)명령문1
#(들여쓰기)명령문2
#elif 조건식2 :
#(들여쓰기)명령문3
#(들여쓰기)명령문4
#else :
#(들여쓰기)명령문5

score = 70						
if score >=90:
	grade = “A”	
elif 80<=score<90:	
	grade = “B”
elif 70<=score<80:
	garde = “C”	
elif 60<=score<70:
	grade = “D”	
else:
	grade = “F”
print(“%d 점은 %s 등급입니다.” %(score, grade))

out
70점은 C 등급입니다.
```

(3)pass

- 프로그래밍 전체의 골격을 잡아놓고, 내부에서 처리할 내용은 나중에 만들고자 할 때 pass를 입력해 둔다. 따라서 pass는 "아무것도 안함", ""곧 개발 할 것" 등의 의미를 지닌다.

  ```python
  num = 0
  if num == 0:
  else:
  
  out
  오류
  
  num = 0
  if num == 0:
      pass
  else:
      pass
  
  out
  #아무 값도 출력되지 않지만 오류가 발생하지도 않음
  ```


4)조건부 표현식: 조건문은 한 줄로 작성할 수도 있으며 조건부 표현식으로 더 축약할 수 있다.

```python
#조건부 표현식의 문법
#ㅏ조건문이 참인 경우 if 조건문 else 조건문이 거짓인 경우ㅓ

#원본
score = 88
if score >= 60:
    message = "success"
else:
    message = "failure"
print(message)

out
success

#한줄로 쓰기
score = 88
if score >= 60:message = "success"
else:message = "failure"
print(message)

out
success

#조건부 표현식
message = "success" if score>60 else "falure"
#message = "success" if score>60 else message = "falure"이렇게 적지 않는다.
#주의할 점은 else 뒤에는 다시 변수를 적지 않고 변수에 넣을 값만 적는다는 것이다.

out
success
```







1. 튜플, 리스트, 딕셔너리, 셋 형 자료형

1)리스트

- 자료를 모아놓은 자료형으로 리스트 내의 자료들을 요소라고 부른다.

- 리스트는 대괄호([])로 감싸고 각 요소는 쉼표로 구분한다.

- 리스트 안에는 어떠한 자료형이라도 포함시킬 수 있다. 리스트 안에 리스트도 포함 가능하다.

- 문자열처럼 인덱싱과 슬라이싱,  합(+)연산과 반복(*)연산, 그리고 len()함수 사용이 가능하다.

  ```python
  list_a = [1,2,3,4]
  list_b = [1,2,3,[5,6,7]]
  list_c = ["나무","자전거","물병"]
  
  #1. 인덱싱과 슬라이싱
  print(list_a[0])
  print(lsit_a[-1])
  print(list_a{1:3})      #슬라이싱
  print(list_c[2][1])		#리스트 내의 요소를 인덱싱
  print(list_b[-1][2])    #리스트 내의 리스트를 인덱싱하는 방법
  print(list_b[-1][1:3])  #리스트 내의 리스트를 슬라이싱
  
  out
  1
  4
  [2, 3]
  병
  7
  [6, 7]
  
  
  #2. 합연산, 반복연산, len
  print(list_a+list_b)	#리스트 합연산
  print(list_a*3)			#리스트 반복연산
  print(len(list_b))
  
  out
  [1, 2, 3, 4, 1, 2, 3, [5, 6, 7]]
  [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
  4
  ```

- 요소의 변경

  -리스트는 요소의 수정, 추가, 삭제 등 변경이 가능하다.

  ```python
  list_a = [1,2,3,4,5]
  #print()에 바로 쓰면 None이 출력된다.
  print(list_a.append(11))
  
  out
  None
  #이들은 원본(이 경우 list_a = [1,2,3,4,5])를 변경시키는 파괴적 함수이기 때문이다.
  
  #요소의 수정
  list_a[1] = 9
  print(list_a)
  
  out
  [1,9,3,4,5]
  
  
  #요소의 추가-.append()함수와 .insert(), extend()함수를 사용
  list_a.append(8)
  list_a.append(11)
  print(list_a)
  
  list_a.insert(0,8)
  list_a.insert(3,11)		#.insert(,)에서 ,뒤에는 추가할 요소가 오고 앞에는 해당 요 
  print(list_a)			 소가 위치할 자리를 입력한다.
  
  list_a.extend([6,7,8])  #여러개를 한번에 추가하고 싶을 때 사용
  print(list_a)
  
  out
  [1, 2, 3, 4, 5, 8, 11]	#list의 뒤에 순서대로 추가
  [8, 1, 2, 11, 3, 4, 5]  
  [1, 2, 3, 4, 5, 6, 7, 8]  
  
  
  #요소의 삭제-del, .remove(), .pop(), .clear()를 사용
  del list_a[0]
  print(list_a)
  list_a = [1,2,3,4,5]
  del list_a[0:2]
  print(list_a)
  
  list_b = [1,2,3,1,2,3]
  list_b.remove(3)   #리스트에 있는 요소 중 처음 나오는 요소를 삭제
  print(list_b)
  
  out
  [2,3,4,5]
  [3,4,5]
  [1,2,1,2,3]
  
  list_c = [1,2,3]
  list_c.pop(1)  			#아무것도 입력하지 않으면 -1을 입력한 것으로 간주한다.
  print(list_c.pop(1))    #입력한 인덱스에 해당하는 요소를 돌려주고 삭제한다.
  print(list_c) 
  
  list_c.clear()			#전부 삭제
  print(list_c) 
  
  out
  2
  [1,3]
  []
  ```

- 그 밖에 리스트와 관련된 함수들

  ```python
  #.sort(): 리스트를 순서대로 정렬
  list_a = [2,4,1,3]
  list_b = ["c","d","b","a"]
  list_a.sort()
  list_b.sort()
  print(list_a)
  print(list_b)
  
  out
  [1, 2, 3, 4]
  ['a', 'b', 'c', 'd']
  
  #.reverse(): 뒤집기
  list_c = [1,2,3,4]
  list_c.reverse()
  print(list_c)
  
  out
  [4, 3, 2, 1]
  
  #또는
  print(reversed(list_c))
  print(list(reversed(list_c)))
  
  out
  <list_reverseiterator object at 0x00000261BB73D2C8>
  #위와 같이 출력되는 것은 오류가 아닌 정상적으로 출력된 것이다.
  #ㅏlist_reverseiterator object at 주소ㅓ형태로 출력되며 list형이 아닌 위와 같이 주소를 알려주는 식으로 출력되는 이유는 기존의 리스트(이 경우 [1,2,3,4])를 활용하기 위해서다. 자료가 방대할 경우 기존의 리스트를 복제 한 뒤 뒤집어서 리턴하는 것 보다 기존의 리스트를 활용해서 작업하는 것이 더 효율적이기 때문이다. 따라서 리스트형으로 얻길 원한다면 list함수를 따로 입력해야 한다.
  [4, 3, 2, 1]
  
  #.count(): 개수 세기
  list_d = ["나무","나무","나무",2,2,3]
  print(list_d.count("나무"))
  
  out
  3
  
  
  #min(), max(), sum(): 각기 최솟값, 최댓값, 합을 구하는 함수
  a = [1,2,3,4,5]
  print(min(a)) #또는 min(1,2,3,4,5)
  print(max(a)) #또는 max(1,2,3,4,5)
  print(sum(a)) #sum은 위와 같이 할 수 없다.
  
  out
  1
  5
  15
  
  
  #enumerate()함수: index와 value를 튜플형으로 함께 출력해준다.
  a = ["a","b","c","d"]
  print(enumerate(a))
  print(list(enumerate(a)))
  #출력하고자 하는 값 뒤에 콤마를 붙이고 ㅏstart=ㅓ을 사용하여 첫 index 설정 가능
  print(list(enumerate(a,start=2)))
  
  
  out
  <enumerate object at 0x00000224BB33EA98>
  #위와 같이 출력되는 것은 오류가 아닌 정상적으로 출력된 것이다.
  #ㅏenumerate object at 주소ㅓ형태로 출력되며 reversed()와 마찬가지 이유로 위와 같이 주소를 출력한다. 리스트형으로 얻고자 하면 list()함수를 입력해야 한다.
  [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]
  [(2, 'a'), (3, 'b'), (4, 'c'), (5, 'd')] #idx가 2부터 시작
  ```

  

2)튜플

- 리스트와 거의 비슷하지만 다른 점으로는 튜플은 ()로 둘러싸며 리스트는 요소의 변경이 가능하지만 튜플은 불가능하다.

- 리스트와 마찬가지로 인덱싱, 슬라이싱, 합연산, 반복연산, len()함수의 사용이 가능하다.

- 리스트와 차이점으로 튜플은 괄호를 생략해도 무방하다.

  ```python
  tu_1 = 1, "나무", "자전거", "상자", 38, (1,2,3), [1,2,3]
  print(tu_1)
  
  out    	#괄호를 생략해도 튜플형으로 출력된다.
  (1, '나무', '자전거', '상자', 38, (1, 2, 3), [1, 2, 3])
  ```

  

3)딕셔너리

- Key와 Value를 중괄호({})로 감싸고 있는 형태로 리스트가 인덱스를 기반으로 값을 저장한다면 딕셔너리는 키를 기반으로 값을 저장하는 것이라고 볼 수 있다.  따라서 딕셔너리는 인덱싱이나 슬라이싱으로 요솟값을 얻을 수 없으며 오직 key를 통해서 value를 구할 수 있다.

  ```python
  list_a = ["야구","축구","농구","골프","당구"]
  dict_a = {"a":"야구","b":"축구","c":"농구","d":"골프","e":"당구"}
  #여기서 리스트의 경우 "골프"라는 값을 찾으려면 "야구"부터 시작해서 순차적으로 자료를 훓어야 하지만 딕셔너리의 경우 d라는 키값만 알면 바로 "골프"에 접근 할 수 있다. 
  print(dict_a["a"])
  
  out
  야구
  ```

- 딕셔너리 요소 변경하기

  ```python
  dict_1 = {"a":1}
  dict_1[b] = 2       #딕셔너리를 뜻하는 변수 뒤에[]를 넣고 그 안에 키가 될 값을 넣은 
  print(dict_1)		#후 =을 쓰고 그 뒤에 value가 될 값을 넣는다.
  
  out
  {"a":1, "b":2}
  
  #딕셔너리 요소 삭제하기
  dict_2 = {"a":1, "b":2, "c":3}
  del dict_2["b"]
  print(dict_2)
  
  out
  {"a":1, "c":3}
  ```

- 딕셔너리를 만들 때 주의사항

  -key는 고유한 값을 가지므로 중복되는 key를 설정하면 하나를 제외한 모든 key들은 무시된다.

  -key는 변하지 않는 값으로만 쓸 수 있기에 key에 리스트는 쓸 수 없지만 튜플은 쓸수 있다.

  -value에는 무엇이든 넣을 수 있다.

```python
dict_2 = {"a":1, "a":2, "a":3}
print(dict_2["a"])

out
3			#1과 2는 무시되고 3만 출력된다.
```

- 딕셔너리 관련 함수

  ```python
  # key리스트 만들기(.keys())
  dict_2 = {"a":1, "b":2, "c":3, "d": 4}
  print(dict_2.keys())
  print(list(dict_2.keys()))
  
  out
  dict_keys(['a', 'b', 'c', 'd'])
  ['a', 'b', 'c', 'd']
  
  #key값만 따로 출력하고 싶을 경우 for문을 사용
  for k in dict_2.keys():
      print(k)
  
  out
  a
  b
  c
  d
  
  # Value리스트 만들기(.values())
  print(dict_2.values())
  print(list(dict_2.values()))
  
  out
  dict_values([1, 2, 3, 4])
  [1, 2, 3, 4]
  #마찬가지로 value값만 따로 출력하고 싶을 경우 for문을 사용
  for v in dict_2.values():
      print(v)
  
  out
  1
  2
  3
  4
  
  
  #Key, Value 쌍 얻기(.items())
  print(dict_2.items())
  print(list(dict_2.items()))
  
  out
  dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
  [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
  
  
  #Key:Value쌍 모두 지우기(.clear())
  dict_2.clear()
  print(dict_2)
  
  out
  {}
  
  
  #Key로 Value얻기(.get())
  #.get(키,디폴트)은 입력한 키가 딕셔너리에 없을 경우 출력할 디폴트 값을 설정 가능하다.
  print(dict_2.get("a"))
  print(dict_2.get("z",123))
  print(dict_2.get("a",123))
  
  out
  1
  123		#찾으려는 키 "z"가 존재하지 않으므로 디폴트 값인 123을 출력
  1		#찾으려는 키 "a"가 존재하므로 디폴트 값이 아닌 Value를 출력
  #얼핏 보면 디폴트 값을 설정하는 것 외에는 그냥 dict_2["a"]와 차이가 없어 보이지만 그 차이는 존재하지 않는 key를 입력했을 때 알 수 있다.
  print(dict_2["z"])
  print(dict_2.get("z"))
  
  out
  KeyError: 'z'   #이처럼 dict_2["a"]는 오류를 출력하지만 print(dict_2.get("z"))
  None			#는 None을 출력한다.
  
  
  #해당 Key가 딕셔너리 안에 있는지 조사하기(in), True나 False를 출력
  print("a" in dict_c)
  
  out
  True
  ```



4)집합(set)자료형 

- 집합 자료형은 set() 함수를 활용하여 만들 수 있다. 

- 집합 자료형 안에는 문자열, 튜플, 리스트, 딕셔너리 등의 집합을 이루고 있는 것들이 들어간다.

- 출력은 중괄호로 표기된다.

- 순서가 없으며 중복을 허용하지 않는다는 특징을 지닌다.

- 순서가 없기에 리스트나 튜플처럼 인덱싱을 통해 값을 얻을 수 없다.

- 딕셔너리 역시 순서가 없이 키를 통해 구분하지만 출력은 입력한 순서대로 된다.  그러나 집합형은 무작위로 배치된 후 출력된다(단 집합형 내의 튜플은 순서가 변하지 않고 출력되는데 이는 튜플이 순서가 있는 자료형일 뿐 아니라 변형을 허용하지 않는 자료형이기 때문이다). 

  ```python
  set_t = set((1.25, 2.4848, 3.484))
  set_l = set(["사과", 1, (8,3,7)], "사과"])
  set_d = set({"a":1, "b":2, "c":3, "d": 4})
  print(set_t)
  print(set_l)
  print(set_d)
  
  out
  {1.25, 2.4848, 3.484}
  {1, (8, 3, 7), '사과'}	#중복된 "사과" 하나가 빠진 상태로 출력
  {'d', 'c', 'a', 'b'}
  ```



- 만일 set자료형에 저장된 값을 인덱싱으로 접근하려면 list나 tuple로 변환한 후 해야 한다.

  ```python
  set_l = set(["사과", 1, (8,3,7)], "사과"])
  list_s = list(set_l)
  print(list_s)
  print(list_s[2])
  
  out-1
  ['사과', (8, 3, 7), 1]	#단, 이 값의 순서가 계속 바뀌기에
  1						 #이 값의 순서도 계속 바뀐다.
  
  out-2
  [1, '사과', (8, 3, 7)]	#이처럼 다시 해보면 또 다른 값을 출력한다.
  (8, 3, 7)
  ```



- 합집합, 차집합, 교집합 구하기

  ```python
  s1 = set([1,2,3,4,5,6])
  s2 = set([4,5,6,7,8,9])
  #1. 합집합 구하기: |기호를 사용, .union()함수를 사용
  print(s1|s2)
  print(s1.union(s2))  #s1과 s2의 위치를 바꿔도 결과는 같다.
  
  out
  {1, 2, 3, 4, 5, 6, 7, 8, 9}
  {1, 2, 3, 4, 5, 6, 7, 8, 9}
  
  #2. 차집합 구하기: 빼기(-)사용, .difference()함수 사용
  print(s1-s2)
  print(s2-s1)
  print(s1.difference(s2))
  print(s2.difference(s1))
  
  out
  {1, 2, 3}
  {8, 9, 7}
  {1, 2, 3}
  {8, 9, 7}
  
  #3. 교집합 구하기: &기호 사용, .intersection(
  print(s1&s2)
  print(s1.intersection(s2))   #역시 s1과 s2의 위치를 바꿔도 값은 같다.
  
  out
  {4, 5, 6}
  {4, 5, 6}
  ```



- 집합 자료형 관련 함수들

  ```python
  #1. 값 1개 추가하기(.add())
  s_1 = set([1,2,3])
  s_2 = set([1,2,3])
  s_1.add(4)
  print(s_1)
  
  out
  {1, 2, 3, 4}
  
  #2. 값 여러 개 추가하기(.update())
  #이 때 추가하는 자료형은 꼭 기존의 자료형과 같을 필요는 없다.
  s_1.update([4,5,6])
  s_2.update("bike")
  print(s_1)
  print(s_2)
  
  out
  {1, 2, 3, 4, 5, 6}
  {1, 2, 3, 'e', 'i', 'b', 'k'}
  
  #3. 특정 값 제거하기(.remove())
  s_1.remove(2)
  print(s_1)
  
  out
  {1, 3}
  ```



1.while문

- bool 표현식이 참인동안 문장을 무한히 반복. 
- bool 표현식이 참인동안 문장을 무한히 반복하므로 종료조건을 설정해 주어야 하며 만일 종료조건을 설정하지 못했다면  `ctrl+c`를 누르면 강제종료 된다.

```python
#while의 기본 구조
While bool표현식:
(들여쓰기)명령문1
(들여쓰기)명령문2
...

i = 0
while i<10:
    print("{}번째 반복입니다.".format(i))
	i = i + 1 #혹은 i += 1        
out
0번째 반복입니다.
1번째 반복입니다.
2번째 반복입니다.
3번째 반복입니다.
4번째 반복입니다.
5번째 반복입니다.
6번째 반복입니다.
7번째 반복입니다.
8번째 반복입니다.
9번째 반복입니다.
```



- while과 관련된 함수

```python
#1.break: 특별한 조건식 없이 무한 반복을 벗어날 때 많이 사용
i = 0
while True:			#while에 종료 조건이 없이 True가 입력되어 무한반복
    print("{}번째 반복문입니다.".format(i))
    i += 1
    input_text = input("종료하시겠습니까?(y/n)")
    if input_text in ["y","Y"]:
        print("종료합니다")
        break		#break로 반복에서 벗어날 수 있다.
        
out
0번째 반복문입니다.
종료하시겠습니까?(y/n)n
1번째 반복문입니다.
종료하시겠습니까?(y/n)n
2번째 반복문입니다.
종료하시겠습니까?(y/n)n
3번째 반복문입니다.
종료하시겠습니까?(y/n)y
종료합니다


#2.continue: continue 이하는 실행하지 않고 다시 반복으로 돌아가게 할 때 사용
count = 0
while count<10:
    count +=1
    if count < 4:
        continue		#바로 위의 조건(<4)이 만족되었으므로 continue가 실행되어 밑의
    print("횟수:", count) #조건인 print는 실행되지 않고 다시 while문으로 돌아간다.
    
out
횟수: 4
횟수: 5
횟수: 6
횟수: 7
횟수: 8
횟수: 9
횟수: 10
```



2.for문

```python
#for문의 기본 구조
For 변수 in 순회할 객체:
(들여쓰기)명령문1
(들여쓰기)명령문2

#기본형
list_a = ["a", "b", "c"]
for i in list_a:
    print(i)
    
out
a
b
c


#반복하려는 자료가 문자열일 경우(문자열이 들어간 리스트형과는 다르다)
a = "어제,오늘,123"
b = ["안녕하세요", "반갑습니다", "12345"]  #문자열이 들어간 리스트형
for i in a:
    print(i)
for s in b:
    print(s)
    
out
어
제
,
오
늘
,
1
2
3
안녕하세요
반갑습니다
12345


#반복하는 자료가 튜플형일 경우
a = [(1,2),(3,4),(5,6),(7,8)]
for i in a:
    print(i)
    
out
(1,2)
(3,4)
(5,6)
(7,8)

#혹은 튜플형을 분리하고 싶으면
a = [(1,2),(3,4),(5,6),(7,8)]
for (first, second) in a:	#튜플 안에 들어있는 자료의 개수에 맞게 쓰면 된다.
    print(first,second)
    
out
1 2
3 4
5 6
7 8


#enumerate()함수 활용
a = ["A","B","AB","O"]

for h,t in enumerate(a):
    print(f'{h}번째 사람은 {t}형입니다.')
    
out
0번째 사람은 A형입니다.
1번째 사람은 B형입니다.
2번째 사람은 AB형입니다.
3번째 사람은 O형입니다.



#반복하려는 자료가 딕셔너리형일 경우
#변수(이 경우 i)에는 key가 들어가게 된다.
a = {"과일":"사과","운동":"야구","과자":"오예스","국가":"한국"}
for i in a:
    print(i)
    
out
과일
운동
과자
국가

#.items()함수 활용
a = {"과일":"사과","운동":"야구","과자":"오예스","국가":"한국"}
for k, v in a.items():
    print("가장 좋아하는 {}은(는) {}입니다.".format(k,v))

out
가장 좋아하는 과일은(는) 사과입니다.
가장 좋아하는 운동은(는) 야구입니다.
가장 좋아하는 과자은(는) 오예스입니다.
가장 좋아하는 국가은(는) 한국입니다.
    
```



- for문과 관련된 함수

```python
#1. continue: while문에서와 마찬가지로 continue문을 만나면 for문의 처음으로 돌아간다.
marks = [90, 25, 67, 45, 80, 60]


number = 0 
for mark in marks: 
    number = number +1 
    if mark < 60:
        print(f'{mark}점은 60점 미만입니다.')
    else:
        print(f'{mark}점은 60점 이상입니다.')
        
out
90점은 60점 이상입니다.
25점은 60점 미만입니다.
67점은 60점 이상입니다.
45점은 60점 미만입니다.
80점은 60점 이상입니다.
60점은 60점 이상입니다.


number = 0 
for mark in marks: 
    number = number +1 
    if mark < 60:
        continue
        print(f'{mark}점은 60점 미만입니다.')
    else:
        print(f'{mark}점은 60점 이상입니다.')
        
out		#conitnue 이하는 출력하지 않고 다시 반복으로 돌아가서 60점 이상인 경우만 출력
90점은 60점 이상입니다.
67점은 60점 이상입니다.
80점은 60점 이상입니다.
60점은 60점 이상입니다.


#2. range(): 
range(a,b,c)는 a부터 b-1까지 c만큼의 폭으로 범위를 생성한다.


print(range(5))
print(list(range(5)))

out
range(0,5)
[0,1,2,3,4]


#a,b,c에 수식을 넣는 것도 가능하다
print(list(range(11)))
print(list(range(1-1,12-1,1*1)))

out
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#역순으로 출력하는 것도 가능하다: range()함수의 매개변수를 사용하는 방법과 reversed()함
print(list(range(5,-1,-1)))  #수를 사용하는 방법
print(list(reversed(range(6))))
out
[5, 4, 3, 2, 1, 0]
[5, 4, 3, 2, 1, 0]
```



- 리스트 내포 사용하기

```python
#리스트 내포의 문법
리스트 이름 = 표현식 for 변수 in 순회할 객체
리스트 이름 = 표현식 for 변수 in 순회할 객체 if 조건문

#리스트 내포를 사용하지 않은 경우
a = [1,2,3,4,5,6]
result = []
for num in a:
    if num%2 == 0:
        result.append(num*3)
print(result)

out
[6, 12, 18]

#리스트 내포를 사용한 경우
a = [1,2,3,4,5,6]
result = [num*3 for num in a if num%2 == 0]
print(result)

out
[6, 12, 18]
```



1.함수

- 함수를 생성하는 것을 "함수를 선언한다"고 표현한다. 

- 함수를 사용하는 것을 "함수를 호출한다"고 표현한다.
- 함수를 선언할 때  괄호 내부에 여러 자료를 넣는데 , 이러한 자료를 매개변수(parameter)라고 부른다.
- 인자(인수,argument)는 함수를 호출할 때 입력하는 값이다.
- 함수를 호출해서 최종적으로 나오는 결과를 리턴값이라고 부른다.
- `def`를 통해 함수를 생성할 수 있다. 
- 함수를 return하면 return이하의 코드는 실행되지 않는다.

```python
#함수의 기본 구조
def 함수명(매개변수):
    수행할문장1
    수행할문장2
    ...

#예시
def n_times(value, n):    #value와 n이라는 매개변수를 입력
    for i in range(n):
        print(value)
n_times("안녕", 3)		#n_times()라는 함수를 호출, "안녕"과 3이라는 인자를 입력

out
안녕						#"안녕"이라는 리턴값
안녕
안녕
```



1)입력값과 결괏값의 유무에 따른 함수의 형태

```python
#1. 입력값의 있고 결괏값도 있는 함수(일반적인 경우)
#사용법: ㅏ결과값을 받을 변수 = 함수이름(입력인자1, 입력인자2, ...)ㅓ
#아래 예시의 경우 z = add(4,9)
def add(a,b):
    result = a+b	#이 함수는 2개의 입력값(a,b)를 받아서 서로 더한 결괏값(result)를
    return result	#돌려준다.
z = add(4,9)		
print(z)

out
13


#2. 입력값이 없는 함수
#사용법: ㅏ결과값을 받을 변수 = 함수이름()ㅓ
#아래의 경우 z = say()
def say():		#함수에 아무 값도 들어가지 않는다.
    return "Hi" #아무 값도 입력하지 않아도 "Hi"를 돌려준다.
z = say()
print(z)

out
Hi


#3. 결괏값이 없는 함수
#사용법: ㅏ함수이름(입력인자1, 입력인자2, ...ㅓ
#아래의 경우 z = abc(2,4) 
def abc(a,b):
    print(a,b)		
    a+b				#돌려주는 값이 없다.
z = abc(2,4)		#즉, 함수가 수행된 결괏값이 없기에 z에는 아무것도 담기지 않는다.
print(z)

out
2 4	  #2,4가 나온 것은 abc()함수 자체에 print(a+b)가 있기 때문, 2,4를 돌려준 것은 X
None  #담긴 것이 없으므로 None이 출력된다.

#print()함수를 없앤 경우
def abc(a,b):
    a+b
z = abc(2,4)

out
None

#결괏값이 있을 경우
def abc(a,b):
    print(a,b)	
    return a+b		#돌려주는 값이 있다.
z = abc(2,4)
print("구분선")
print(z)

out
2 4		#z = abc(2,4)가 "실행"된 결과로 출력
구분선
6		##z = abc(2,4)가 "실행"된 결과로 6이라는 값을 담게 된 z를 "print"한 결과 출력
#2 4는 abc()함수가 실행되면 print(a,b)가 되도록 설정된 것이므로 따로 print함수를 쓰지 않아도 실행버튼을 누르면 출력된다. 즉, 2 4는 z에 담기는 값이 아니라 함수로 인해 출력되는 값이다. z에 담기는 값은 abc()함수가 반환하는 값인 a+b뿐이다.


#4. 입력값도 없고 결괏값도 없는 함수
#아래의 경우 say() 
사용법: ㅏ함수이름()ㅓ
def say():		#입력값이 없고
    print("Hi")	#결과값도 없다.
say()			#say()라는 함수가 실행되면 함수에서 설정한 내용에 따라	

out
Hi				#단순히 Hi가 print된다.
```



2)매개변수와 인자

```python
#1. 위치인자: 함수는 기본적으로 인자를 위치로 판단한다.
def sub(a,b):
    return a-b
result_1 = sub(6,4)
result_2 = sub(4,6)
print(result_1)
print(result_2)

out
2
-2


#2.키워드 인자: 매개변수를 지정하여 호출하면 순서에 상관없이 사용할 수 있다.
#단, 키워드 인자를 활용한 이후에 위치 인자를 활용할 수는 없다.
def add(a,b):
    return a+b
result_1 = add(b=8, a=4)  #굳이 순서대로 넣지 않아도 된다.
result_2 = add(4, b=8)
result_3 = add(b=8, 4)
print(result_1)
print(result_2)
print(result_3)

out
12
12
오류		#키워드 인자 이후에 위치인자를 사용하여 오류가 발생


#3.기본 인자 값: 함수가 호출될 때, 인자를 지정하지 않아도 기본값이 입력된다.
#단, 기본 인자 이후에 기본값이 없는 인자를 사용할 수는 없다.
def add(a,b=4):
    return a+b
result_1 = add(4)
result_2 = add(4,8)
result_3 = add(,8)
print(result_1)
print(result_2)
print(result_3)

out
8		#인자를 입력하지 않으면 기본인자가 입력되고
12		#인자를 입력하면 기본인자가 아닌 직접 입력한 인자로 수행한다.
오류	  #기본인자 이후에 기본값이 없는 인자를 사용해 오류가 발생

#모든 매개변수가 기본 인자값을 지닐 경우
def add(a=2,b=4,c=6):
    return a+b+c
result_1 = add()
result_2 = add(b=8)
result_3 = add(b=5,a=7)  
print(result_1)
print(result_2)
print(result_3)

out			#순서와 무관하게 모두 정상적으로 출력이 가능하다.
12
16
18


#4. 가변 매개변수(가변 인자 리스트)
#원래 매개변수의 개수와 인자의 개수는 같아야 한다.
def add(a,b):
    return a+b
result_1 = add(4,7)
result_2 = add(4)
result_3 = add(4,7,8)

out
11
오류
오류

#그러나 여러 변수를 넣어야 할 때가 있는데 이 때 사용하는 것이 가변 매개변수다.
#ㅏ*매개변수ㅓ의 형태로 표현하며 자료형은 튜플형이다.
#관례상 인자(arguments)의 약자인 args를 많이 사용한다.
#몇 가지 규칙이 존재한다.
#①가변 매개변수 뒤에는 일반 매개변수가 올 수 없다.
#②가변 매개변수는 하나만 사용이 가능하다.

def add(*args):
    result = 0
    for i in args:
        result += i
    return result
asd1 = add(4,7)
asd2 = add(4)
asd3 = add(4,7,8)

out
11
4
19

#일반 매개변수를 함께 사용할 경우
def times(n,*values):
    result = 0
    for i in range(n):
        for value in values:
            result += value
    return result
a1 = times(1,1,2,3,4,5) 
a2 = times(2,1,2,3,4,5) 
a3 = times(3,1,2,3,4,5) 
print(a1, a2, a3)

out
15, 30, 45


#5. 키워드 파라미터(정의되지 않은 키워드 인자들 처리)
#ㅏkey=valueㅓ형태의 입력값을 모두 딕셔너리로 만들어서 출력한다.
#key에 해당하는 값에 숫자만 올 수는 없다.
#ㅏ**매개변수ㅓ형태로 표현한다. 
#관례상 키워드 인자(keyword arguments)의 약자인 kwargs를 주로 사용한다.
def dict_1(**kwargs):
    print(kwargs)
dict_1(a1="a",a2="b",a3="c",a4="d")

out
{'a1': 'a', 'a2': 'b', 'a3': 'c', 'a4': 'd'}
```



3)return

- 함수의 결괏값은 언제나 하나이다.
- return문을  만나는 순간의 값을 반환하며 return문 아래에 있는 코드는 실행되지 않고 함수를 호출한 곳으로 돌아간다.

```python
def add_mul(a,b):
    return a+b, a*b   #이 처럼 두 개의 결과값을 반환할 것 같은 코드도
s = add_mul(4,8)
print(s)

out
(12,32)				#튜플형이라는 하나의 결과값을 돌려준다.


def add_mul(a,b):
    return a+b
	return a*b
s = add_mul(4,8)
print(s)

out
12					#retrun을 만나는 순간 아래의 코드는 실행되지 않는다.
```









# python을 통한 운영체제 조작

- os를 import

  ```python
  import os
  ```

  

- 디렉토리 조회 및 이동

  - `.getcwd()`: 현재 디렉토리 조회
  - `.chdir()`: 디렉토리 이동
  - `.listdir()`: 입력한 경로의 파일과 폴더 목록을 리스트로 반환
  - `.path.exists()`: 특정 폴더의 유무를 boolean 값으로 반환

  ```python
  import os
  
  print("현재 디렉토리: ", os.getcwd())
  os.chdir("C:\\Users\Desktop\참고\TIL")
  print("변경 디렉토리: ", os.getcwd())
  print(os.listdir("C:\\Users\Desktop\참고\TIL"))
  print(os.path.exists("C:\\Users\Desktop\참고\TIL"))
  print(os.path.exists("C:\\Users\Desktop\참고\TILL"))
  
  #out
  현재 디렉토리:  C:\Users\Desktop\참고\TIL\etc
  변경 디렉토리:  C:\Users\Desktop\참고\TIL
  ['.git', '.idea', 'django', 'error.md', 'etc', 'Git.md', 'java', 'spring', '기타.md', '수학', '알고리즘', '웹']
  True
  False
  ```



- 디렉토리 생성, 삭제

  - `.mkdir()`: 경로의 제일 마지막에 적힌 하나의 폴더만 생성
  - `.mkdirs()`: 경로에 적힌 모든 폴더를 생성
  - 두 메소드 모두 생성하려는 폴더가 이미 있는 경우 에러 발생

  - `.rmdir()`: 경로의 제일 마지막에 적힌 하나의 폴더만 삭제
  - `.removedirs()`: 경로에 적힌 모든 폴더를 삭제
  - 두 메소드 모두 삭제하려는 폴더가 비어있지 않은 경우 에러 발생



- 텍스트 파일 읽고 쓰기

  - 파일을 생성하거나 조회할 때 모드를 지정할 수 있다.

  | 기호 | 모드         |
  | ---- | ------------ |
  | t    | 텍스트(기본) |
  | b    | 바이너리     |
  | r    | 읽기(기본)   |
  | w    | 쓰기         |
  | a    | 이어쓰기     |
  | +    | 읽기, 쓰기   |

  

  - 파일에 내용을 작성하는 순서는 `open`→`write`→`close` 순이다.

  ```python
  #열고, open 함수의 3번째 인자로 encoding 방식을 줄 수 있다.
  file = open("test.txt", "w")
  #쓰고
  file.write("내용내용")
  #닫고
  file.close()
  ```

  

  - 파일의 내용을 읽기

  ```python
  txt = open("c:\\tmep\test.txt")
  
  print(f.readlines())
  ```

  

- 엑셀, csv 파일 읽고 쓰기

  - txt 파일과 방식이 다르고 별도의 패키지 설치가 필요하다.

  - 추후 추가





# python의 모듈

- sys
  - 변수와 함수를 직접 제어할 수 있게 해주는 모듈이다.
  - 대화형 인터프리터(터미널)를 종료하는 것도 가능하다(`sys.exit()`).
  - `sys.stdin`은 대화형 인터프리터에 값을 입력받겠다는 것이다.