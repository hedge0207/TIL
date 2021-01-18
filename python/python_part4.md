# Python 내장 함수

- `abs(숫자)`: 해당 숫자의 절댓값을 반환

  ```python
  print(abs(-3))  # 3
  ```



- `all(반복 가능한 자료형)`: 반복 가능한 자료형의 요소가 모두 참이면 True, 하나라도 거짓이면 False를 반환

  ```python
  arr1 = [1,2,3,4,5,6]
  arr2 = [0,1,2,3,4,5]  # 0이 있으므로 False를 반환
  arr3 = []			  # 빈 리스트의 경우 True를 반환
  
  print(all(arr1))	# True
  print(all(arr2))	# False
  print(all(arr3))	# True
  ```



- `any(반복 가능한 자료형)`: 반복 가능한 자료형의 요소 중 하나라도 참이면 True, 모두 거짓이면 False를 반환

  ```python
  arr1 = [0,'',False,[],None]
  arr2 = [0,'',False,[],1]	# 1이 있으므로 True
  arr3 = []					# 빈 리스트의 경우 False를 반환
  
  print(any(arr1))		# False
  print(any(arr2))		# True
  print(any(arr3))		# False
  ```



- `chr()`: 아스키 코드 값을 입력 받아 그 코드에 해당하는 문자를 반환하는 함수

  ```python
  print(chr(97))	# a
  ```



- `ord()`: 문자를 입력받아 아스키 코드 값을 반환하는 함수

  ```python
  print(ord(a))	# 97
  ```



- `dir()`: 객체가 가지고 있는 변수나 함수를 보여준다.

  ```python
  print(dir([]))
  """
  ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 
  'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
  """
  
  print(dir({'a':1}))
  """
  ['__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__ior__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__ror__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
  """
  ```



- `divmod(a,b)`: a를 b로 나눈 몫과 나머지를 튜플 형태로 반환한다.

  ```python
  print(divmod(8,3))	# (2, 2)
  ```

  

- `enumerate(순서가 있는 자료형)`: 순서가 있는 자료형을 입력 받아 인덱스 값을 포함하는 객체를 돌려준다.

  ```python
  for i,fruit in enumerate(["apple","banana","mango"]):
      print(i,fruit)
  """
  0 apple
  1 banana
  2 mango
  """
  ```



- `eval()`: 실행 가능한 문자열을 입력으로 받아 문자열을 실행한 결과값을 반환한다.

  ```python
  print(eval('5+7'))				# 12
  print(eval('list((1,2,3,4))'))	# [1, 2, 3, 4]
  ```



- `hex(정수)`: 정수를 16진수로 변환하여 반환한다.

  ```python
  print(hex(1))	# 0x1
  ```



- `oct()`: 정수를 8진수 문자열로 변경하여 반환한다.

  ```python
  print(oct(1))	# 0o1
  ```



- `isinstance(인스턴스, 클래스명)`: 인스턴스가 입력으로 받은 클래스의 인스턴스인지를 판단하여 boolean을 반환한다.

  ```python
  arr = list()
  print(isinstance(arr,list))		# True
  ```

  

- `max()`: 반복 가능한 자료형을 받아, 그 최댓값을 반환한다.

  ```python
  print(max([3,6,9])) 	# 9
  ```



- `min()`: 반복 가능한 자료형을 받아, 그 최솟값을 반환한다.

  ```python
  print(min([3,6,9]))		# 3
  ```

  

- `pow(a,b)`: a를 y제곱한 값을 돌려주는 함수

  ```python
  print(pow(3,4))		# 81
  ```

   

- `round(숫자, [반올림할 자리수])`:  숫자를 입력받아 반올림해 준다.

  ```python
  print(round(3.4))		# 3
  print(round(3.5))		# 4
  print(round(3.648,2)) 	# 소수점 2번째 자리까지 표시
  ```



- `sum()`: 입력 받은 리스트나 튜플의 모든 값을 합해준다.

  ```python
  print(sum([1,2,3,4,5]))  # 15
  ```



- `zip()`: 동일한 개수로 이루어진 반복 가능한 자료형을 묶어 준다.

  ```python
  print(list(zip([1,2,3],[4,5,6],[7,8,9])))	# [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
  ```

  



# 라이브러리

- sys

  - python 인터프리터가 제공하는 변수와 함수를 직접 제어할 수  있게 해주는 모듈이다.
  - 명령 행에서 인수 전달하기
    - 명령 프롬프트에서 받은 여러 개의 입력값을 처리하는 방법

  ```python
  import sys
  print(sys.argv)  # 입력 받은 갑들이 리스트 형태로 들어가게 되는데 첫 번째 요소는 파일명이, 두 번째 인자부터 입력받은 순서대로 들어가게 된다.
  ```

  ```bash
  $ python pract.py hi hello
  # ['pract.py', 'hi', 'hello']
  ```

  - 강제로 스크립트 종료하기
    - `ctrl+z`, `ctrl+d`를 눌러 대화형 인터프리터를 종료하는 것과 같은 기능을 한다.

  ```python
  import sys
  sys.exit()
  ```

  - 자신이 만든 모듈 불러와 사용하기
    - `sys.path`에는 파이썬 모듈들이 저장되어 있는 위치가 저장되어 있다.
    - 아래와 같이 모듈이 위차한 경로를 추가해 원하는 모듈을 사용 가능하다.

  ```python
  import sys
  sys.path.append("C:/test")
  ```

  

- pickle

  - 객체의 형태를 그대로 유지하면서 파일에 저장하고 불러올 수 있게 하는 모듈
  - 객체를 파일에 저장하기

  ```python
  import pickle
  
  txt_file = open('test.txt','wb')
  data = {1:'python',2:'java'}
  pickle.dump(data,txt_file)
  txt_file.close()
  ```

  - 파일에서 객체를 불러오기

  ```python
  import pickle
  
  txt_file = open('test.txt','rb')
  data = pickle.load(txt_file)
  print(data)		# {1: 'python', 2: 'java'}
  txt_file.close()
  ```



- os

  - 환경 변수나 디렉토리, 파일 등의 OS 자원을 제어할 수 있게 해주는 모듈이다.
  - 내 시스템의 환경 변수 값을 알고 싶을 때
    - 딕셔너리이기에 key로 접근 가능하다.

  ```python
  import os
  
  print(os.environ)	# environ({.......})
  print(os.environ['PATH'])	# C:\Program Files\Git\.....
  ```

  - 디렉토리 위치 변경하기

  ```python
  import os
  
  os.chdir("D:/")
  ```

  - 현재 디렉토리 위치 확인하기

  ```python
  import os
  
  print(os.getcwd())	# C:\Users\...
  ```

  - 시스템 명령어 호출하기

  ```python
  import os
  
  #아래와 같이 os.system("명령어")를 입력하면 된다.
  os.system("mkdir new_folder") # new_folder가 현재 디렉토리에 생성된다.
  ```

  

- shutil

  - 파일을 복사해주는 모듈

  ```python
  import shutil
  
  shutil.copy("test.txt", "test2.txt")	# test.txt 파일의 내용이 복사 된 text2.txt 파일이 생긴다.
  ```



- glob

  - 디렉토리에 있는 파일들을 리스트로 만들어준다.
  - `*`, `?` 등의 메타 문자를 써서 원하는 파일만 읽는 것도 가능하다.

  ```python
  import glob
  
  print(glob.glob("D:/*"))	# ['D:/github','D:/PJT' 'D:/test', 'D:/메모.txt' ...]
  ```

  

- time

  - 시간과 관련된 모듈
  - `time.time()`: UTC(Universal Time Coordinated 협정 세계 표준시)를 사용하여 현재 시간을 실수 형태로 돌려주는 함수이다. 1970년 1월 1일 0시 0분 0초를 기준으로 지난 시간을 초 단위로 돌려준다.
  - `time.localtime()`: `time.time()`이 반환한 실수 값을 연도, 월, 일, 시, 분, 초의 형태로 변환하는 함수이다.

  - `time.asctime()`: `time.localtime()`에 의해 반환된 튜플 형태의 값을 받아 날짜와 시간을 알아보기 쉬운 형태로 반환하는 함수이다.
  - `time.ctime`: `time.asctime(time.localtime(time.time()))`을 요약한 함수이다.

  ```python
  import time
  
  print(time.time())									# 1610977416.5125847
  print(time.localtime(time.time()))				
  # time.struct_time(tm_year=2021, tm_mon=1, tm_mday=18, tm_hour=22, tm_min=43, tm_sec=36, tm_wday=0, tm_yday=18, tm_isdst=0)
  print(time.asctime(time.localtime(time.time())))	# Mon Jan 18 22:43:36 2021
  print(time.ctime())									# Mon Jan 18 22:43:36 2021
  ```

  - `time.strftime()`: 시간에 관계된 것을 세밀하게 표현하는 여러 가지 포맷 코드를 제공
    - 아래 소개한 것 외에도 다양한 포맷 코드가 존재

  | 포맷 코드 | 설명                                  | 예시              |
  | --------- | ------------------------------------- | ----------------- |
  | %a        | 요일 줄임말                           | Mon               |
  | %A        | 요일                                  | Monday            |
  | %b        | 달 줄임말                             | Jan               |
  | %B        | 달                                    | January           |
  | %c        | 날짜와 시간 출력                      | 21/01/01 10:46:08 |
  | %d        | 날                                    | [01,01]           |
  | %H        | 현재 설정된 로케일에 기반한 날짜 출력 | 20/01/01          |
  | %X        | 현재 설정된 로케일에 기반한 시간 출력 | 15:11:17          |
  | %Z        | 시간대 출력                           | 대한민국 표준시   |

  - `time.sleep(초)`: 일정한 시간 간격을 두고 루프를 실행

  ```python
  import time
  
  for i in range(3):
      print(i)		#print가 1초 간격으로 이루어진다.
      time.sleep(1)
  ```

  

- calendar
  - 파이썬에서 달력을 볼 수 있게 해준다.
  - `calendar.calendar(연도)`: 해당 연도 전체의 달력을 반환
  - `calendar.prmonth(연도, 월)`: 해당 연도, 해당 월의 달력을 반환
  - `calender.weekday(연도, 월, 일)`: 해당 날짜의 요일 정보를 숫자로 반환한다(0~6까지로 각기 월~일에 해당)
  - `calender.monthrange(연도, 월)`: 해당 월의 1일이 무슨 요일인지와 그 달이 며칠까지 있는지를 튜플 형태로 반환한다.



- random

  - 난수를 발생시키는 모듈이다.
  - `random.random()`: 0~1사이의 실수 중에서 난수 값을 돌려준다.
  - `random.randomint(숫자1, 숫자2)`: 숫자1에서 숫자2 사이의 정수 중에서 난수 값을 반환한다.
  - `random.shuffle(순서가 있는 자료형)`: 반복 가능한 자료형의 순서를 변경시킨다.

  

  

- webbrowser
  - 기본 웹 브라우저를 자동으로 실행하는 모듈
  - `webbrower.open("주소")`: 주소에 해당하는 사이트를 기본 웹 브라우저로 접속
  - `webbrowser.open_new(주소)`: 주소에 해당하는 사이트를 기본 웹 브라우저로 새 창에서 열기



- threading

  - 스레드를 다루는 모듈

  ```python
  # 스레드를 사용하지 않을 경우
  import time
  
  def long_task():  # 한 번 실행에 3초의 시간이 걸리는 함수
      for i in range(3):
          time.sleep(1)  # 1초간 대기
          print("count:", i)
  
  print("Start")
  
  for i in range(3):  # long_task를 3회 수행한다.
      long_task()
  
  print("End")
  
  # 스레드를 사용하는 경우
  import time
  import threading
  
  def long_task():
      for i in range(3):
          time.sleep(1)
          print("count:", i)
  
  print("Start")
  
  threads = []
  for i in range(5):
      t = threading.Thread(target=long_task)  # 스레드를 생성
      threads.append(t)
  
  for t in threads:
      t.start()
  
  for t in threads:
      t.join()  # join으로 스레드가 종료될때까지 기다린다.
  
  print("End")
  ```

