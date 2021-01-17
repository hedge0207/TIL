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