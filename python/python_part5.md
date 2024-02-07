# Python 내장 함수

- `id(객체)`: 객체에 할당된 id를 반환한다.

  ```python
  my_list = []
  print(id(my_list))	# 객체 id가 출력된다.
  ```



- `dir(객체)`: 객체 정보를 반환한다.

  ```python
  my_list = []
  print(dir(my_list))
  '''
  ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
  '''
  ```



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

  

- `enumerate(순서가 있는 자료형)`: 순서가 있는 자료형을 입력 받아 인덱스 값을 포함하는 튜플을 반환한다.

  - 정확히는 iterator idx와 element의 쌍으로 된 iterator를 반환한다.
  
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

  - 혹은 특정 자료형의 형태를 띈 문자열을 형태에 맞는 자료형으로 변환한다.
  
  ```python
  print(eval('5+7'))				# 12
  print(eval('list((1,2,3,4))'))	# [1, 2, 3, 4]
  
  a = "{'a':'test','b':[1,2,3,4]}"
  print(type(a))			# <class 'str'>
  print(type(eval(a)))	# <class 'dict'>
  ```



- `exec()`: 실행 가능한 문자열을 입력으로 받아 실행한다.
  - `eval`과 달리 반환값이 없다.
  - 굉장히 위험한 기능으로 가급적 사용하지 않는 것이 좋다.
  
  ```python
  # 실행시킬 코드
  test_func = """
  def foo():
      return "bar"
  
  my_bar = foo()
  """
  
  a = {}
  # 코드 실행
  exec(test_func, a)
  print(a['my_bar'])	# bar
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



- `zip()`: 동일한 개수로 이루어진 반복 가능한 자료형을 tuple로 묶어 준다.

  ```python
  print(list(zip([1,2,3],[4,5,6],[7,8,9])))	# [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
  ```





# 패키지

- Python에서 리눅스 명령어 실행하기

  - subprocess 모듈을 사용한다.
    - 실행하려는 명령이 시스템에 설치되어 있어야 한다.
    - 따라서 이식성이 떨어진다.
  - 예시
    - subprocess의 run 메서드를 호출하면 명령이 실행되고, 결과가 PIPE에 저장된다.
    - result.stdout은 str이 아니고 byte이기 때문에 unicode로 변환을 해줘야 한다.

  ```python
  import subprocess
  
  
  result = subprocess.run(['ls'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  
  result = subprocess.run(['wc', '-l', 'test.txt'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  ```



- inspect

  - 내장 라이브러리로 별도의 설치가 필요 없다.
  - Python package 위치 확인하기
  
  ```python
  import inspect
  import requests
  
  print(inspect.getfile(requests))
  ```
  
  - 함수의 argument 확인하기
  
  ```python
  import inspect
  
  
  def foo(a, b):
      return
  
  print(inspect.signature(foo).parameters)
  ```



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

  - python 인터프리터의 위치

  ```python
  import sys
  
  print(sys.executable)
  ```
  
  - 객체의 사이즈 구하기
    - 단, 정확한 사이즈를 반환하지는 않는다.
    - Nested 형태의 객체일 경우 가장 외부에 있는 객체의 size만을 계산하고, 내부에 있는 객체를 전부 계산하지는 않는다.
  
  
  ```python
  import sys
  
  foo = []
  print(sys.getsizeof(foo))
  
  # my_array에는 빈 문자열, my_array2에는 abcde가 들어있음에도 같은 size를 반환한다.
  my_array = [1,2,3,""]
  my_array2 = [1,2,3,"abcde"]
  print(sys.getsizeof(my_array))		# 88
  print(sys.getsizeof(my_array2))		# 88
  ```
  
  - 참조된 횟수 구하기
    - 단, string, int와 같은 타입의 값은 CPython 내부에서 참조한 횟수도 포함되므로 직접 작성한 코드상에서 몇 번이나 참조되었는지 알 수는 없다.
    - 또한 백그라운드에서 실행 중인 프로그램에서 사용한 값들도 모두 count된다.
  
  ```python
  import sys
  
  foo = []
  print(sys.getrefcount(foo))	# 2 (foo를 선언하면서 1번, getrefcount 함수의 매개변수로 넘어가면서 1번)
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



## os

- 환경 변수나 디렉토리, 파일 등의 OS 자원을 제어할 수 있게 해주는 모듈이다.
  - 내 시스템의 환경 변수 값을 알고 싶을 때
    - 딕셔너리이기에 key로 접근 가능하다.
    - `get` 메서드를 사용해서 가져올 수 있다.
    - 혹은 `os.getenv()`도 사용할 수 있다.
    - 검색된 환경 변수가 없을 경우 기본 값을 지정할 수 있다.

  ```python
  import os
  
  print(os.environ)	# environ({.......})
  print(os.environ['PATH'])		# C:\Program Files\Git\.....
  print(os.environ.get('PATH'))	# C:\Program Files\Git\.....
  print(os.getenv('PATH'))		# C:\Program Files\Git\.....
  
  # 기본 값 지정하기
  # NAME이라는 환경변수가 지정되어 있지 않으면 THEO를 불러오겠다.
  print(os.environ.get('NAME', 'THEO'))	# THEO
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

  - 디렉토리 생성하기
    - `mkdir`: 깊이가 1인 폴더만 생성이 가능하다.
    - `makedirs`: 깊이가 2 이상인 폴더도 생성이 가능하다. `exist_ok`를 인자로 받으며, True로 설정하면 이미 해당 디렉토리가 존재하더라도 다시 생성하고 False일 경우 에러가 발생한다.

  ```python
  import os
  
  
  # 불가능(단, hello라는 폴더가 이미 존재하면 생성 가능)
  os.mkdir('./hello/world')
  # 가능
  os.makedirs('./hello/world')
  
  # 이미 ./hello폴더가 있을 경우
  # 정상 실행
  os.makedirs('./hello/world', exist_ok=True)
  # error
  os.makedirs('./hello/world', exist_ok=False)
  ```

  - 파일 삭제하기
    - `remove`를 사용한다.
    - 폴더를 삭제하려 할 경우 permissionerror가 발생한다.

  ```python
  import os
  
  
  os.remove('./tmp1/tmp2/tmp.txt')
  ```

  - 폴더 삭제하기
    - 폴더가 비어있지 않을 경우 에러가 발생한다.
    - shutil 모듈을 사용하면, 디렉터리가 비어있지 않아도 삭제가 가능하다.

  ```python
  import os
  import shutil
  
  
  os.rmdir('./qwe/asd')
  shutil.rmtree('./qwe')
  ```

  - 폴더 내부의 폴더 및 파일 목록 확인

  ```python
  import os
  
  
  print(os.listdir('./test'))
  ```

  - 파일명 혹은 폴더명 변경하기

  ```python
  import os
  
  
  os.rename('/old/file/or/folder/path', '/new/file/or/folder/path')
  ```

  - pid 얻기

  ```python
  import os
  
  print(os.getpid())
  ```

  - 부모 프로세스의 pid 얻기

  ```python
  import os
  
  print(os.getppid())
  ```



- os.path

  - 파일, 경로와 관련된 모듈
  - isdir: 경로가 디렉토리이면서 해당 디렉토리가 존재하면 True, 디렉토리가 아니거나 존재하지 않으면  False를 반환한다.
    - 일반적으로는 디렉터리인지 확인을 위해 사용하며, 존재 유무는 `exists`를 사용한다.
  
  ```python
  import os
  print(os.path.isdir('/User/Desktop'))	# True
  ```
  
  - abspath: 절대경로를 반환한다.
  
  ```python
  import os
  print(os.path.abspath('test')) # C:\Users\User\test\test
  ```
  
  - basename: 상대 경로를 반환한다.
  
  ```python
  import os
  print(os.path.basename('/Users/User/theo/test')) # test
  ```
  
  - getcwd: 실행 경로를 반환한다.
    - 실행 경로란 해당 python 파일을 실행시킨 경로를 의미한다.
    - 예를들어 python 파일은 `C:\Users\User\test\my_python.py`에 있고, 터미널은 `C:\Users\User\`에 있는 상태에서 `.\test\my_python.py` 명령어로 파일을 실행시키면, 이 파일을 실행시킨 경로인 `C:\Users\User\`가 반환된다.
  
  ```python
  import os
  print(os.getcwd())
  ```
  
  - exists: 해당 경로가 존재하면 True, 아니면 False를 반환한다.
  
  ```bash
  import os
  print(os.path.exists('/Users/User/theo/test'))	# True
  ```
  
  - join: 입력된 문자열들을 OS의 형식에 맞게 하나의 경로로 이어준다.
  
  ```python
  import os
  print(os.path.join("/Users/User/theo/test", "test.py")) # /Users/User/theo/test\test.py
  ```
  
  - split: 경로와 파일명을 분리하여 튜플로 반환한다.
  
  ```python
  import os
  print(os.path.splitext("/c/Users/User/test/test.py")) # ('/c/Users/User/test', 'test.py')
  ```
  
  - splitext: 파일명과 확장자를 분리하여 튜플로 반환한다.
  
  ```python
  import os
  print(os.path.splitext("/c/Users/User/test/test.py")) # ('/c/Users/42Maru/theo/test/test', '.py')
  ```
  
  - getsize: 파일 크기를 바이트 단위로 반환한다.
  
  ```python
  import os
  print(os.path.getsize('/Users/User/theo/test')) # 4096
  ```
  
  - getmtime: 최근 변경 시간을 반환한다.
  
  ```python
  import os
  print(os.path.getmtime('/Users/User/theo/test')) # 1623374338.4626312
  ```
  
  - `normpath(path)`
    - path에서 `.`, `..`와 같른 구분자를 제거해준다.
  
  ```python
  import os
  
  print(os.path.normpath('/home/theo/../data//test.txt')) # /home/theo/data/test.txt
  ```





## etc

- shutil

  - 디렉토리, 파일과 관련된 여러 기능을 제공해주는 패키지
  - 파일 복사
  
  ```python
  import shutil
  
  shutil.copy("test.txt", "test2.txt")	# test.txt 파일의 내용이 복사 된 text2.txt 파일이 생긴다.
  ```
  
  - 터미널 창의 size를 구하는 것도 가능하다.
  
  ```python
  import shutil
  
  print(shutil.get_terminal_size())	# os.terminal_size(columns=160, lines=24)
  ```
  
  



- glob

  - 디렉토리에 있는 파일들을 리스트로 만들어준다.
  - `*`, `?` 등의 메타 문자를 써서 원하는 파일만 읽는 것도 가능하다.

  ```python
  import glob
  
  print(glob.glob("D:/*"))	# ['D:/github','D:/PJT' 'D:/test', 'D:/메모.txt' ...]
  ```




- operator

  - `itemgetter()`
    - 피연산자에서 item을 꺼내는 콜러블 객체를 반환한다.
    - 이를 활용하면 이중 리스트에서 리스트 내부의 인자를 기준으로 정렬하는 것도 가능하다.

  ```python
  from operator import itemgetter
  
  
  a = [('1','2'),('8','1'),('2','7')]
  # 리스트 a의 2번째 인자를 꺼낸다.
  f = itemgetter(1)(a)
  print(f)		# ('8', '1')
  
  # 이중 리스트 내부의 2번째 인자로 정렬
  print(sorted(a, key=itemgetter(1)))	# [('8', '1'), ('1', '2'), ('2', '7')]
  ```




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



- trace 모듈을 사용하여 script 실행 추적하기

  - main option
    - `--trace`, `-t`
    - `--count`, `-c`
    - `--listfuncs`, `-l`
    - `--report`, `-r`
    - `--trackcalls`, `-T`

  - sub option
    - https://docs.python.org/ko/3/library/trace.html 참고

  ```bash
  $ python -m trace <main_option> [sub_option] <script_path>
  
  # 예시
  $ python -m trace --trace test.py
  ```



## time

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



- datetime

  - `time`과 마찬가지로 시간과 관련된 모듈
  - `datetime.now()`: 현재 날짜와 시간을 반환한다.
    - `datetime.datetime` 타입으로 반환한다.

  ```python
  import datetime
  
  
  print(datetime.datetime.now())			# 2021-10-19 14:20:46.924473
  print(type(datetime.datetime.now()))	# <class 'datetime.datetime'>
  ```

  - `strftime()`
    - `datetime.datetime`을 지정해준 형식에 맞는 문자열로 반환한다. 
    - 지원하는 형식은 `time.strftime()`와 같다.

  ```python
  import datetime
  
  
  now = datetime.datetime.now()
  print(now.strftime('%Y-%m-%d'))		# 2021-10-19
  ```

  - `date.now()`: 현재 날짜를 반환한다.

  ```python
  import datetime
  
  
  now = datetime.date.now()
  print(now)		# 2021-10-19
  ```

  - `timedelta()`: `datetime` 객체에 특정 시간을 더하거나 뺄 수 있게 해준다.
    - `days`(기본값), `seconds`, `microsecnds`, `milliseconds`, `minutes`, `hours`, `weeks`를 사용 가능하다.

  ```python
  import datetime
  
  
  today = datetime.date.today()
  print(today)						# 2021-10-19
  print(today-datetime.timedelta(1))	# 2021-10-18
  ```



- calendar
  - 파이썬에서 달력을 볼 수 있게 해준다.
  - `calendar.calendar(연도)`: 해당 연도 전체의 달력을 반환
  - `calendar.prmonth(연도, 월)`: 해당 연도, 해당 월의 달력을 반환
  - `calender.weekday(연도, 월, 일)`: 해당 날짜의 요일 정보를 숫자로 반환한다(0~6까지로 각기 월~일에 해당)
  - `calender.monthrange(연도, 월)`: 해당 월의 1일이 무슨 요일인지와 그 달이 며칠까지 있는지를 튜플 형태로 반환한다.



## argparse

- agrparse

  - 콘솔에서 Python 파일을 실행 시킬 때 인자를 넘겨주기 위한 패키지
    - Python 내장 패키지로 별도의 설치가 필요없다.

  - 기본형

  ```python
  import argparse
  
  # description 옵션을 통해 설명을 붙일 수 있다.
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("text")
  
  args = parser.parse_args()
  
  print(args.text)
  ```

  - `-h`로 위에서 정의한 인자를 확인 가능하다.

  ```bash
  $ python test.py -h
  ```

  - 실행

  ```bash
  $ python test.py Hello
  ```



- 이름 지정

  - `help` 옵션을 통해 인자에 대한 설명을 줄 수 있다.
  - 축약된 이름을 주는 것이 가능하다.
  - 단어를 구분할 때는 `-`와 `_`를 주는 것이 가능하다.
    - 그러나 `-`의 경우 python에서 지원하지 않으므로 `-`를 활용하여 이름을 지정해 줬어도 사용할 때는 `_`로 사용해야 한다.

  ```python
  parser.add_argument("--test-text","-tt",help="text to print")
  # 아래와 같이 _로 지정해줘야 한다.
  print(args.test_text)
  ```

  - dest
    - 저장 될 변수 명을 변경할 수 있다.

  ```python
  parser.add_argument("--test-text","-tt",help="text to print", dest="my_text")
  # 아래와 같이 _로 지정해줘야 한다.
  print(args.my_text)
  ```



- 자료형을 지정하기

  - 기본적으로 인자로 받은 모든 데이터를 문자열로 취급하기에, 문자열이 아닌 자료형으로 받고 싶다면 아래와 같이 타입을 지정해 줘야 한다.
  - FileType()함수로 파일에 접근하는 것도 가능하다.
  - list와 같은 타입은 사용이 불가능하다.

  ```python
  import argparse
  
  
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("test_int", type=int)
  
  args = parser.parse_args()
  
  print(5+args.test_int)
  ```

  - 실행

  ```bash
  $ python test.py 5
  ```
  
  - 자료형을 함수로 지정하는 것도 가능하다.
    - 인자로 넘긴 값은 자동으로 타입으로 지정해 준 함수의 인자로 넘어가게 된다.
  
  ```python
  import argparse
  
  
  def str_to_bool(args):
      args = args.lower()
      if args in ["1", "yes", "y"]:
          return True
      elif args in ["0", "no", "n"]:
          return False
  
  
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("--test-args", type=str_to_bool)
  
  args = parser.parse_args()
  
  print(args.test_args)
  ```
  
  - 실행
  
  ```bash
  $ python --test-args No
  ```



- positional/optional

  - 인자의 이름 앞에 `-`가 붙어 있으면 optional, 없으면 positional 인자가 된다.
  - positional 인자의 경우 필수로 넣어야 하며, optional 인자도 `required=True`를 옵션으로 주면 필수로 넣게 할 수 있지만, 권장되지 않는다.

  ```python
  import argparse
  
  
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("text")
  parser.add_argument("-op-int", type=int)
  parser.add_argument("-opr-int",required=True, type=int)
  
  args = parser.parse_args()
  
  print(args.text)
  print(5+args.op_int)
  print(5+args.opr_int)
  ```

  - 실행
    - positional 인자가 여러 개인 경우 반드시 순서를 지켜서 줘야 한다.
    - -op-int의 경우 주지 않아도 error가 발생하지 않지만 -opr-int는 주지 않으면 error가 발생한다.
    - optional 인자의 경우 `<args 명>=<args 값>`의 형태로 주거나 `<args 명> <args 값>` 형태로 주면 된다.

  ```bash
  $ python test.py hello -op-int=3 -opr-int 4
  ```



- default 값 지정

  - optional 인자의 경우 default 값을 지정하는 것이 가능하다.
  - `argparse.SUPPRESS`을 default 값으로 넣을 경우 None이 들어가는 것이 아니라 인자 자체가 생성되지 않는다.

  ```python
  import argparse
  
  
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("--text", default="Bye")
  parser.add_argument("--test", default=argparse.SUPPRESS)
  
  args = parser.parse_args()
  
  print(args.text)
  print(args.test)
  ```

  - 실행
    - 아래 명령어를 실행하면 `args.text`는 출력이 되지만, `args.test`에서 에러가 발생한다.

  ```bash
  $ python test.py
  ```



- action

  - `add_argument()`로 인자를 정의할 때 action을 지정할 수 있다.
  - `store`: 기본값, 인자로 받은 값을 해당 인자에 대입한다.

  ```python
  # 모두 아래 코드를 기반으로 한다.
  import argparse
  
  
  parser = argparse.ArgumentParser(description="Test parser")
  parser.add_argument("--my-args")
  
  
  args = parser.parse_args()
  
  print(args.my_args)
  ```

  - `store_const`:  미리 지정해준 `const`에 입력 받은 값이 대입된다.
    - 값 없이 인자만 넘겨주면, const에 지정 된 값이 대입되게 된다.
    - 인자와 값을 함께 넘겨줄 수는 없다.
    - 인자도 넘겨주지 않으면 None이 저장된다.

  ```bash
  # parser.add_argument("--my-args", action="store_const", const=0)
  $ python test.py --my-args
  ```

  - `store_true`, `store_false`: 값이 없는 인자를 받으면 각기 True, False를 저장한다.

  ```bash
  # parser.add_argument("--my-args", action="store_true")
  $ python test.py --my-args
  ```

  - `append`: 여러 개의 값을 저장하고자 할 때 사용한다.

  ```bash
  # parser.add_argument("--my-args", action="append")
  $ python test.py --my-args 1 --my-args 2
  ```

  - `append_const`: 사전에 지정한 const 값이 저장된다.

  ```bash
  # parser.add_argument("--my-args", action="append_const",const=3)
  $ python test.py --my-args --my-args
  ```

  - `count`: 인자를 적은 횟수만큼 값이 증가한다.



- 그 밖에 아래와 같은 옵션들을 줄 수 있다.
  - nargs: 인자로 여러 개의 값을 받을 수 있다.
  - choices: 값의 범위를 지정할 수 있다.
  - metavar: 도움말 메시지를 생성할 때 표시되는 이름을 변경할 수 있다.



## logging

- 추후 추가



## Json

- Json 라이브러리
  - Python 표준 라이브러리
  - 별도의 설치 없이 사용이 가능하다.
  - Python 오브젝트(딕셔너리, 리스트, 튜플 등)를 JSON 문자열로 변경(encodindg)이 가능하다.
    - 꼭 오브젝트가 아니더라도 변경은 된다.
  - JSON 문자열을 Python 오브젝트로 변경(decoding)이 가능하다.



- encoding

  - `dumps()` 메서드 사용
    - python object를 직렬화된 json 문자열로 변환

  ```python
  import json
  
  person = {
      "name": "John",
      "age": 26,
      "family": {
          "mother": "Aira", "father": "Stark"
      },
      "hobbies": ["watching movies", "building lego"]
  }
  
  json_string = json.dumps(person)
  print(json_string)
  # {"name": "John", "age": 26, "family": {"mother": "Aira", "father": "Stark"}, "hobbies": ["watching movies", "building lego"]}
  print(type(json_string))
  # <class 'str'>
  ```

  - `dump()`메서드 사용
    - python object를 파일로 변환
    - 따라서 저장할 파일명도 지정해줘야 한다.

  ```python
  import json
  
  person = {
      "name": "John",
      "age": 26,
      "family": {
          "mother": "Aira", "father": "Stark"
      },
      "hobbies": ["watching movies", "lego building"]
  }
  
  with open("person.json", "w") as f:
      json.dump(person, f)
  ```

  - `dump()`의 결과 파일

  ```json
  // person.json
  {"name": "John", "age": 26, "family": {"mother": "Aira", "father": "Stark"}, "hobbies": ["watching movies", "lego building"]}
  ```

  - 옵션
    - `indent`: json 형식에 indent를 적용한다. 문자열 혹은 이스케이프 시퀀스를 넣는 것이 가능하다.
    - `ensure_ascii`: ascii가 아닌 문자들은 모두 이스케이프 문자로 표현한다(기본값은 True).
    - 그 밖의 옵션은 https://docs.python.org/ko/3/library/json.html 참조

  ```python
  import json
  
  person = {
      "name": "John",
      "age": 26,
      "family": {
          "mother": "Aira", "father": "Stark"
      },
      "hobbies": ["watching movies", "lego building"],
      "Korean_name": "유동혁"
  }
  # indent와 ensure_ascii 옵션을 주지 않았을 경우
  with open("person.json", "w", encoding='utf-8') as f:
      print(json.dumps(person))
  '''
  들여쓰기도 되지 않고 한글의 경우 이스케이프 시퀀스로 변경되어 출력된다.
  {"name": "John", "age": 26, "family": {"mother": "Aira", "father": "Stark"}, "hobbies": ["watching movies", "lego building"], "Korean_name": "\uc720\ub3d9\ud601"}
  '''
  # indet를 줬을 경우
  	print(json.dumps(person,indent="\t"))
  '''
  {
          "name": "John",
          "age": 26,
          "family": {
                  "mother": "Aira",
                  "father": "Stark"
          },
          "hobbies": [
                  "watching movies",
                  "lego building"
          ],
          "Korean_name": "\uc720\ub3d9\ud601"
  }
  '''
  # ensure_ascii 옵션을 False로 줬을 경우
  	print(json.dumps(person, indent="\t", ensure_ascii=False))
  '''
  한글이 제대로 출력된다.
  {
          "name": "John",
          "age": 26,
          "family": {
                  "mother": "Aira",
                  "father": "Stark"
          },
          "hobbies": [
                  "watching movies",
                  "lego building"
          ],
          "Korean_name": "유동혁"
  }
  '''
  ```



- decoding

  - `loads()` 메서드 사용
    - Json 문자열을 파싱해서 python object로 변환
    - 문자열 내에 dictionary 형태로 작성할 때 key값은 반드시 `"`로 묶어야 한다.

  ```python
  import json
  
  # dictionary가 아닌 문자열이이다.
  # 아래와 같이 문자열 내부에 딕셔너리 형태로 작성할 때 key에 문자열이 오면 반드시 ""로 묶어야 한다.
  my_json_str = '{"name":"John","age":26,"hobbies":["watching movies", "lego building"], "family":{"mother":"Aira","father":"Stark"},"korean_name":"유동혁"}'
  
  print(json.loads(my_json_str))
  print(type(json.loads(my_json_str)))
  '''
  {'name': 'John', 'age': 26, 'hobbies': ['watching movies', 'lego building'], 'family': {'mother': 'Aira', 'father': 'Stark'}, 'korean_name': '유동혁'}
  <class 'dict'>
  '''
  ```

  - `load()`메서드 사용
    - json 파일을 읽어 파이썬 객체로 변환

  ```python
  import json
  
  
  with open("person.json", "r", encoding="utf-8") as f:
      print(json.load(f))
      # loads()를 사용할 경우, read()함수는 파일 객체를 읽어 문자열로 변환해준다.
      print(json.loads(f.read()))
  '''
  두 출력의 결과는 동일하다.
  둘을 위와 같이 동시에 쓸 경우 에러가 발생하는데 하나씩 주석처리 한 후 출력하면 정상적으로 출력된다.
  '''
  ```

  - 번외- 위 코드에서 에러가 발생하는 이유
    - `read()` 메서드는 파일 내용 전체를 반환한다.
    - 이미 한 번 전체를 반환했으므로 더 이상 반환할 값이 없어 연속 두 번 실행하면 아래와 같이 빈 문자열을 반환한다.
    - `json.load()` 메서드 내부에 `read()`를 실행시키는 로직이 있을 것이다(가정).
    - 따라서 두 번째 실행되는 `json.loads(f.read())`에서 `f.read()` 값은 빈 문자열이 되고 `loads()` 메서드의 인자로 빈 문자열이 넘어가게 되어 에러가 발생한다.

  ```python
  with open('person.json', "r", encoding="utf-8") as f:
      print(f.read())
      print("빈 문자열 반환")
      print(f.read())
      print("빈 문자열 반환")
  '''
  $ python test.py
  {
          "name": "John",
          "age": 26,
          "family": {
                  "mother": "Aira",
                  "father": "Stark"
          },
          "hobbies": [
                  "watching movies",
                  "lego building"
          ],
          "Korean_name": "유동혁"
  }
  빈 문자열 반환
  
  빈 문자열 반환
  '''
  ```




- csv를 json으로 변환하기

  - csv 파일

  | id   | nickname | age  | interest     |
  | ---- | -------- | ---- | ------------ |
  | 1    | John     | 22   | ["swimming"] |
  | 2    | Doe      | 23   | ["movie"]    |

  - 변환하기
    - `reader()` 메서드나 `Dictreader()`메서드를 사용한다.

  ```python
  import csv
  import json
  
  with open("User.csv", "r") as f:
      # reader() 메서드를 사용하여 csv 파일을 읽는다.
      csv_file = csv.reader(f)
      # 첫 줄은 컬럼 명으로 따로 저장한다.
      col_list = next(csv_file)
  	# {컬럼명:값} 쌍으로 딕셔너리를 만든다.
      for cols in csv_file:
          doc = {col_name: col for col_name, col in zip(col_list, cols)}
          # Json 형태로 변환한다.
          print(json.dumps(doc, ensure_ascii=False, indent="\t"))
  
  '''
  {
          "id": "1",
          "nickname": "John",
          "age": "22",
          "interest": "[\"swimming\"]"
  }
  {
          "id": "2",
          "nickname": "Doe",
          "age": "23",
          "interest": "[\"movie\"]"
  }
  '''
  
  # Dictreader 메서드의 경우 zip() 함수를 사용하지 않아도 된다.
  import csv
  import json
  
  with open("User.csv", "r") as user_csv:
      csv_file = csv.DictReader(user_csv, ['id', 'nickname', 'age', 'interest'])
      next(csv_file)
      for row in csv_file:
          print(json.dumps(row, ensure_ascii=False, indent="\t")) # 출력값은 위와 같다.
  ```

  - 변환 후 파일로 저장하기

  ```python
  import csv
  import json
  
  with open("User.csv", "r") as user_csv, open("User.json", "w") as user_json:
      # reader() 메서드를 사용하여 csv 파일을 읽는다.
      csv_file = csv.reader(user_csv)
      # 첫 줄은 컬럼 명으로 따로 저장한다.
      col_list = next(csv_file)
  	
      # 출력 결과를 깔끔하게 하기 위해 각 행을 리스트에 넣고 한 번에 json 파일로 변환한다.
      result = []
      for cols in csv_file:
          doc = {col_name: col for col_name, col in zip(col_list, cols)}
          result.append(doc)
      # 파일로 저장한다.
      json.dump(result, user_json, ensure_ascii=False, indent="\t")
  ```

  - 결과 파일

  ```json
  [
  	{
  		"id": "1",
  		"nickname": "John",
  		"age": "22",
  		"interest": "[\"swimming\"]"
  	},
  	{
  		"id": "2",
  		"nickname": "Doe",
  		"age": "23",
  		"interest": "[\"movie\"]"
  	}
  ]
  ```



## CSV

- csv 라이브러리
  - Python 표준 라이브러리
    - 별도의 설치 없이 사용이 가능하다.
  - CSV 파일을 읽고 쓸 수 있게 해준다.



- CSV 파일 쓰기

  - list를 CSV로 저장
    - `writer`를 사용한다.
    - `writerow`는 한 줄 쓰기, `writerows`는 여러 줄 쓰기

  ```python
  import csv
  
  
  fields = ['name','age','gender']
  people_list = [
      ['Theo', 28, 'male'],
      ['Cha',27,'female']
  ]
  
  with open('test.csv','w',newline='',encoding='utf-8') as f:
      writer = csv.writer(f)
      writer.writerow(fields)
      writer.writerows(people_list)
  ```
  
  - dict를 CSV로 저장
    - `DictWriter`를 사용한다.
    - `fieldnames` 파라미터에 필드 정보를 넘겨줘야 한다.
  
  ```python
  import csv
  
  
  fields = ['name','age','gender']
  people_dict = [
      {'name':'Theo','age':28,'gender':'male'},
      {'name':'Cha','age':27,'gender':'male'}
  ]
  
  with open('test.csv','w',newline='',encoding='utf-8') as f:
      writer = csv.DictWriter(f, fieldnames=fields)
      writer.writeheader()
      writer.writerows(people_dict)
  ```



- CSV 파일 읽기

  - `reader`로 읽기
    - 만일 최상위에 필드 정보가 있다면 아래 예시와 같이 `next`를 사용하면 된다.
    - 필드 정보와 필드 값을 함께 출력하려면 아래와 같이 `zip`을 활용하면 된다.

  ```python
  import csv
  
  
  with open('./test.csv', 'r', encoding='utf-8') as f:
      reader = csv.reader(f)
      col_list = next(reader)
      for row in reader:
          print(row)
          for col_name,column in zip(col_list,row):
              print(col_name,column)
  ```

  - `DictReader`로 읽기

  ```python
  import csv
  
  
  with open('./test.csv', 'r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      fields = reader.fieldnames
      for field in fields:
          print(field)
  
      for row in reader:
          print(row)
  ```




- 옵션들
  - `delimeter`
    - CSV 파일의 열을 무엇으로 구분할지 결정(기본 값은 콤마).
  - `qutechar`
    - 문자열이 무엇으로 묶여있는지 결정.
  - `quoting`
    - quotechar의 레벨을 결정한다
    - QUOTE_ALL, NONE, MINIMAL 중 선택.
  - 이 외에도 다양한 옵션이 존재한다.

  ```python
  import csv
  
  
  reader = csv.reader("test.csv", delimitr="|", quotechar='"', quoting=csv.QUOTE_ALL)
  ```



- CSV 파일과 xlsx 파일의 비교
  - 속도
    - 일반적으로 xlsx 파일에 비해 csv 파일이 쓰는 속도가 빠르다.
  - 크기
    - 일반적으로 xlsx 파일에 비해 csv 파일의 크기가 크다.
    - 이는 xlsx 파일은 데이터를 압축해서 저장하기 때문이다.
    - xlsx 파일은 반복되는 데이터가 있을 경우 해당 데이터의 참조를 생성하여 한 셀에만 실제 데이터를 저장하고, 중복 셀에는 해당 데이터의 참조를 저장하는 방식으로 압축한다.



- Python으로 csv를 생성하고 excel로 열 경우, 인코딩 문제로 한글이 깨지는 경우가 있다.

  - 반대의 경우도 마찬가지로 csv 파일을 python을 통해 읽을 경우 인코딩이 제대로 되지 않는 문제가 있다.
  - 이는 BOM(Byte Order Mask) 때문이다.
    - BOM은 Byte의 인코딩 방식을 표현한 기호 같은 것이다.
    - 파일의 가장 첫 부분에 들어가게 된다.
  - 만일 `open`을 통해 파일을 열 때 위와 같은 문제가 발생했다면 인코딩 방식을 `utf-8-sig`로 변경하면 된다.

  ```python
  with open('./test.csv', 'r', encoding="utf-8-sig") as f:
  	f.readlines()
  ```

  - 만일 StringIO등에 csv 데이터를 썼는데 위와 같은 에러가 났다면 BOM(아래의 경우 `u'ufeff'`)를 맨 앞에 추가해주면 된다.

  ```python
  import csv
  from io import StringIO
  
  data = [['안녕하세요', '반갑습니다'], ['안녕히가세요', '감사합니다']]
  
  output = StringIO()
  writer = csv.writer(output)
  writer.writerows()
  content=u'\ufeff'+output.getvalue()
  ```



# excel

- Python으로  excel을 다룰 수 있는 다양한 라이브러리가 존재한다.

  > http://www.python-excel.org/ 참고

  - 위 사이트에서 어떤 라이브러리들이 있는지 확인이 가능하다.
    - 위 목록에서 library를 선택할 때 중요한 기준 중 하나는  xlsx 파일을 지원하는지 여부이다.
      - xlsx는 Excel 2010부터 지원하기 시작한 파일로 기존에 사용하던 xls 파일은 행, 열 모두 최대 65,535까지밖에 지원하지 않는다.
      - 따라서 그 이상의 대용량 데이터를 처리할 경우 xlsx를 지원하는 라이브러리를 사용해야 한다.
    - 또한 excel파일을 다루는 속도도 중요한데 아래 표는 PyExcelerate 라이브러리에서 자체적으로 실시한 벤치마크 결과이다.
      - pyexcelerate - xlsxwriter - openpyxl 순으로 빠르다.

  | TEST_NAME                   | NUM_ROWS | NUM_COLS | TIME_IN_SECONDS |
  | --------------------------- | -------- | -------- | --------------- |
  | pyexcelerate value fastest  | 1000     | 100      | 0.47            |
  | pyexcelerate value faster   | 1000     | 100      | 0.51            |
  | pyexcelerate value fast     | 1000     | 100      | 1.53            |
  | xlsxwriter value            | 1000     | 100      | 0.84            |
  | openpyxl                    | 1000     | 100      | 2.74            |
  | pyexcelerate style cheating | 1000     | 100      | 1.23            |
  | pyexcelerate style fastest  | 1000     | 100      | 2.40            |
  | pyexcelerate style faster   | 1000     | 100      | 2.75            |
  | pyexcelerate style fast     | 1000     | 100      | 6.15            |
  | xlsxwriter style cheating   | 1000     | 100      | 1.21            |
  | xlsxwriter style            | 1000     | 100      | 4.85            |
  | openpyxl                    | 1000     | 100      | 6.32            |



- pyexcelerate
  - excel 파일을 읽는 것은 불가능하지만, excel을 다루는 라이브러리 중 쓰기 속도가 가장 빠르다.
  - 공식 문서가 따로 존재하지 않지만 github repository의 README에 예시가 존재한다.
  
  > https://github.com/kz26/PyExcelerate
  
  - 가끔 xlsx 파일이 깨지는 경우가 있다.



## Random

- 난수를 생성하는 모듈
  - Python에 기본적으로 내장되어 있으므로 별도의 설치 없이 사용이 가능하다.



- 메서드

  - `random()`
    - 0이상 1 미만의 숫자를 반환한다.

  ```python
  import random
  
  
  print(random.random())
  ```

  - `randrange()`
    - 첫 번째 인자 이상, 두 번째 인자 미만의 정수를 반환한다.
    - 첫 번째 인자만 줄 경우, 0 이상, 해당 인자 미만의 정수를 반환한다.

  ```python
  import random
  
  
  print(random.randrange(1,7))
  ```

  - `shuffle()`
    - 시퀀스를 뒤섞는다.

  ```python
  import random
  
  
  my_list = [1,2,3,4,5]
  random.shuffle(my_list)
  print(my_list)	# [2, 4, 1, 3, 5]
  ```

  - `choice()`
    - 시퀀스 타입을 인자로 받아 원소 하나를 반환한다.

  ```python
  import random
  
  
  my_list = [1,2,3,4,5]
  print(random.choice(my_list))
  ```

  - `sample()`
    - 지정한 개수 만큼의 무작위 원소를 반환한다.
    - 동일한 인덱스의 원소를 반환하지 않는다.
    - 동일한 값은 반환할 수 있다.

  ```python
  import random
  
  
  my_list = [1,2,3,4,5]
  print(random.sample(my_list, 2))
  ```



# Python type hint

- 타입 힌트
  - 타입 표시에 관한 표준 구문을 제공하고, 더 쉬운 정적 분석과 리팩토링 및 타입 정보를 추론하는 것에 대한 도움을 주기 위해 만들어졌다.
    - 정적 언어가 가지는 장점인 타입 시스템의 견고함을 동적 언어로써 조금이라도 따라잡을 수 있도록 도와준다.
  - 그렇다고 파이썬이 정적 타입을 지향하는 것은 아니다.
    - 타입 힌트는 말 그대로 힌트 기능일뿐으로, 정적 감사기와 IDE를 사용하며 코드의 질을 높이기 위해 사용 될 수 있으나 결코 런타임에 영향을 끼치지 않는다.
    - 예를 들어 정수형을 가질 변수에 문자열 타입을 힌트로 작성해 놓아도 파이썬은 에러를 발생시키지는 않는다.



- 타입 힌트를 표시하는 방법

  - 함수 선언부에서의 타입 힌트
    - 인수 뒤에 콜론을 붙여서 인수의 타입 힌트를 붙인다.
    - 괄호 뒤 콜론 전에 `->` 를 붙여 반환값에 대한 타입 힌트를 지정할 수 있다.

  ```python
  def f(name: str, age: int) -> str:
      ...
  ```

  - 변수의 타입은 함수 인수와 비슷한 형식으로 힌트를 붙일 수 있다.

  ``` python
  age: int = 28
  name: string = "Theo"
  # 새로 생성한 클래스 타입으로 선언
  test: Test = Test()
  ```

  - 클래스 멤버 변수

  ```python
  class Person:
      name: str
      age: int
      weight: float
      
      def __init__(self,name: str, age: int, weight: float):
          self.name = name
          self.age = age
          self.weight = weight
  ```



- 특별한 타입

  - Any
    - 말 그대로 모든 타입을 허용한다.

  ```python
  x: Any = 1
  y: Any = "Any"
  ```

  - NoReturn
    - 리턴값이 없을 경우 사용한다.
    - 예외를 발생시킬 때도 사용한다.

  ```python
  from typing import NoReturn
  
  def f() -> NoReturn:
      raise RuntimeError('Error')
  ```



- typing 모듈

  - 내장 타입을 이용해서 좀 더 복잡한 타입 어노테이션을 추가할 때 사용.

  ```python
  from typing import List, Set, Dict, Tuple
  
  num_lst: List[int] = [1,2,3]
  
  num_set: Set[int] = {4,5}
  
  coordinate: Dict[str, float] = {'x': 1.0, 'y': 0.9}
  
  theo: Tuple[int, str, List[float]] = (28, "Theo", [170, 62.4])
  ```

  - Union
    - 여러 개의 타입이 허용될 수 있는 상황에서 사용

  ```python
  from typing import Union
  
  
  def toString(num: Union[int, float]) -> str:
      return str(num)
  ```

  - Optional
    - None이 허용되는 함수의 매개 변수의 타입을 명시할 때 사용한다.
    - `Optional[type]`은 `Union[type, None]`의 shorthand다.
  
  ```python
  def repeat(name: str,message: Optional[str] = None) -> str:
      if message:
          return name+message
      else:
          return name
  ```
  
  - list, tuple 등의 자료형으로 type hint를 줄 경우 `typing.List`와 `list`의 차이
  
    >https://stackoverflow.com/questions/39458193/using-list-tuple-etc-from-typing-vs-directly-referring-type-as-list-tuple-etc
  
    - Python 3.8까지는 list, tuple 등의 내장 자료형이 generic type이 아니었기에 `baz`함수에서와 같이 내장 자료형으로 구체적인 type hint를 주는 것은 불가능했다.
    - 그러나 3.9부터는 내장 자료형으로도 `baz` 함수처럼 구체적인 type hint를 주는 것이 가능해졌다.
  
  ```python
  from typing import List
  
  
  def foo(lst: List[str]):
      pass
  
  # 3.8까지는 아래와 같이 type hint를 주는 것은 가능했지만
  def bar(lst: list):
      pass
  
  # 아래와 같이 주는 것은 불가능했다.
  def baz(lst: list[str]):
      pass
  ```
  



- `Annotated`

  > https://peps.python.org/pep-0593/
  >
  > https://docs.python.org/ko/3/library/typing.html

  - Type hint에 metadata를 추가하기 위해서 사용한다.
    - Python 3.9에서 `typing` moduke에 새롭게 추가된 class이다.
    - 이전까지는 `typing_extensions`에 있었다.
  - `T`라는 type에 `x`라는 meatadata를 추가하기 위해서 `Annotated[T, x]`와 같이 사용하면 된다.
    - 이렇게 추가된 metadata는 static analysis tool들과 runtime에 사용될 수 있다.
    - Runtime에 metadata는 `__metadata__` attribute에 저장된다.
  - Library나 tool이 `Annotated[T, x]`를 만났을 때, metadata에 대한 특별한 logic이 없다면, metadata를 무시하고, annotation을 T type으로 취급한다.

  ```python
  from typing import Annotated
  from dataclasses import dataclass
  
  
  @dataclass
  class ValueRange:
      lo: int
      hi: int
  
  MyType = Annotated[int, ValueRange(-10, 5), "foo"]
  print(MyType.__metadata__)							# (ValueRange(lo=-10, hi=5), 'foo')
  foo : MyType = ValueRange(-30, 10)
  print(foo)											# ValueRange(lo=-10, hi=5)
  ```
  
  - Type에 대한 metadata를 추가하기 위해 사용한다.
    - 특정 type에 대해 추가적인 설명이 필요할 경우 이를 metadata로 추가하기 위해 사용한다.
    - 당연하게도 강제성은 없다.
  
  ```python
  from typing import Annotated
  
  
  Name = Annotated[str, "fist lettser is Capital"]
  
  my_name: Name = "john"
  print(my_name)
  ```







# with

> https://velog.io/@zkffhtm6523/Python-With%EB%AC%B8-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0 참고

- 자원을 획득하고, 사용한 후 반납해야 하는 경우에 주로 사용한다.

  - 특히 파일 작업을 할 때 많이 사용한다.
  - 파일 작업을 할 때, `with`를 사용하지 않고 `open()` 내장함수를 사용할 경우에는 `close()`를 반드시 함께 사용해야 한다.
    - `close()`를 함께 사용하지 않을 경우 데이터가 소실될 수 있다.
    - 또한 `open()`과 `close()` 사이의 로직에서 에러가 발생할 경우 `close()`가 실행되지 않고 종료되기에, 에러가 발생해도 `close()`가 실행되도록 하기 위해서 일반적으로 `try`, `finally`를 함께 사용한다.

  ```python
  try:
      f = open("person.txt", "r")
      print(f.read())
  finally:
      f.close()
  ```

  - `with`를 사용하면 훨씬 간략하게 작성이 가능하다.
    - `with`는 호출 될 때 자원의`__enter__`메서드를 호출하고, 종료될 때 자원의 `__exit__` 메서드를 호출하게 되어 있다.
    - 파일 객체는 내부적으로 `__enter__` 메서드와 `__exit__` 메서드가 구현되어 있기에 `with`와 함께 사용하면 따로 `close()`를 사용하지 않아도 `with` 블록이 종료될 때 `close()`가 호출된다.

  ```python
  f = open("person.txt", "r")
  print(dir(f)) # 파일객체의 메서드 확인
  
  '''
  __init__과 __exit__구현되어 있다.
  ['_CHUNK_SIZE', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_finalizing', 'buffer', 'close', 'closed', 'detach', 'encoding', 'errors', 'fileno', 'flush', 'isatty', 'line_buffering', 'mode', 'name', 'newlines', 'read', 'readable', 'readline', 'readlines', 'reconfigure', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'write_through', 'writelines']
  '''
  ```



- 문법

  - 기본형

  ```python
  with 자원 [as 변수]:
      BLOCK
  ```

  - 예시
    - 아래 예시에서 `__enter__`와 `__exit__`은 호출하지 않았는데도 `with`가 사용될 때와, `with` 블록이 종료될 때 자동으로 호출된다.

  ```python
  class Hello:
  
      def __enter__(self):
          # 사용할 자원을 가져오거나 만든다
          print('Enter')
          return self  # 반환값이 있어야 VARIABLE를 블록내에서 사용할 수 있다
  
      def sayHello(self, name):
          # 자원을 사용한다. ex) 인사한다
          print('Hello ' + name)
  
      def __exit__(self, exc_type, exc_val, exc_tb):
          # 마지막 처리를 한다
          print('Exit')
  
  
  with Hello() as h:
      h.sayHello('Kim')
      h.sayHello('Park')	
  
  # Enter
  # Hello Kim
  # Hello Park
  # Exit
  ```

  - 파일 처리에 사용
    - 위에서 본 `open()`과 `close()`를 사용한 예시와 동일하게 동작하지만, 훨씬 간결하게 작성이 가능하다.

  ```python
  with open("person.txt", "r") as f:
      print(f.read())
  
  # name: Park
  # age: 26
  ```













