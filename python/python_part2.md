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


  - `==`: 일치 할 경우 True, 불일치 할 경우 False
  - `!=`: 일치 할 경우 False, 불일치 할 경우 True

  ```python
  print("abc"=="abc")		# True
  print("abc"=="xyz")		# False
  print("abc"!="abc")		# False
  print("abc"!="xyz")		# True
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



