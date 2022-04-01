# 클로저

- 변수의 사용 범위

  - 전역 변수
    - 함수를 포함하여 스크립트 전체에서 접근할 수 있는 변수
    - 전역 변수에 접근할 수 있는 범위를 전역 범위라 한다.

  ```python
  x = 10
  
  def foo():
      # 함수 안에서도 접근이 가능하고
      print(x)	# 10
     
  foo()
  # 밖에서도 당연히 접근이 가능하다.
  print(x)
  ```

  - 지역 변수
    - 특정 함수에서만 접근이 가능한 변수
    - 지역 변수에 접근할 수 있는 범위를 지역 범위라 한다.

  ```python
  def foo():
      x = 10
      print(x)	# 10
  
  # 지역 범위가 아닌 곳에서는 접근이 불가능하다.
  print(x)	# NameError: name 'x' is not defined
  ```

  - `global`
    - 함수 내에서는 전역 변수의 변경이 불가능하다.
    - `global` 키워드를 사용하면 함수 내에서 전역 변수에 접근뿐 아니라 변경도 가능해진다.
    - 전역 변수가 없는 상태에서 함수 내에 global을 통해 변수를 생성하면 해당 변수는 전역 변수가 된다.

  ```python
  x = 10
  y = 10
  def foo():
      global x
      x = 5
      y = 5
      print(x,y)	# 5 5
  
  foo()
  print(x,y)	# 5 10
  
  
  def bar():
      global z
      z = 10
      print(z)
  
  # bar 함수가 아직 실행되기 전이므로 z 변수는 생성되지 않은 상태이다.
  try:
  	print(z)
  except Exception as e:
      print(e)	# name 'z' is not defined
  bar()			# 10
  print(z)		# 10
  ```

  - 중첩 함수에서의 범위
    - 내부 함수에서는 외부 함수의 변수에 접근이 가능하다.
    - 내부 함수에서는 외부 함수의 변수의 변경은 불가능하다.
    - 외부 함수에서는 내부 함수의 변수에 접근이 불가능하다.

  ```python
  def outer():
      msg = "Hello!"
      my_num = 1
      def inner():
          # 내부 함수에서는 외부 함수의 변수에 접근이 가능하다.
          print(msg)	# Hello!
          my_num = 2
          inner_var = 0
      inner()
      # 내부 함수에서는 외부 함수의 변수의 변경은 불가능하다.
      print(my_num)	# 1
      # 외부 함수에서는 내부 함수의 변수에 접근이 불가능하다.
      print(inner_var)	# NameError: name 'inner_var' is not defined
  
  outer()	
  ```

  - `nonlocal`
    - 내부 함수에서 외부 함수에 선언된 변수의 값을 변경할 수 있게 해준다.
    - 현재 함수의 바깥 쪽에 있는 지역 변수 중 가장 가까운 함수부터 찾는다.

  ```python
  def outer():
      my_num = 1
      def inner():
          nonlocal my_num
          my_num = 2
  
      inner()
      print(my_num)	# 2
  
  
  outer()	
  
  
  # first의 지역변수인 num이 아닌 second의 지역변수인 num을 사용한다.
  def first():
      num = 1
      def second():
          num = 2
          def third():
              nonlocal num
              num+=1
              print(num)	# 3
          third()
      second()
  first()
  ```



- 클로저

  - 내부함수가 자신을 포함하고 있는 외부 함수보다 더 오래 유지되는 경우, 외부 함수 밖에서 내부 함수가 호출되더라도, 외부 함수의 변수(프리 변수)에 접근할 수 있는 함수.
    - 프리변수: 어떤 함수에서 사용은 되지만 그 함수 내부에서 선언되지 않은 함수

  - 다음의 조건을 만족하는 함수를 클로저라 부른다.
    - 어떤 함수의 내부 함수일 것
    - 그 내부 함수가 외부 함수의 변수를 참조할 것
    - 외부 함수가 내부 함수를 리턴할 것

  ```python
  def outer():
      msg = "World!"
      print("Execute?")
      # 내부 함수
      def inner():
          # 외부 함수의 변수를 참조
          print("Hello {}".format(msg))
  	
      # 외부 함수가 내부 함수를 return
      return inner
  
  my_func = outer()	# Execute?
  my_func()			# Hello World!
  ```

  - 설명
    - 위 예시에서 `outer` 함수는 `my_func = outer()` 부분에서 한 번만 실행된다. 
    - `my_func()`이 실행될 때도 `outer` 함수가 실행되었다면 `Execute?`가 한 번 더 출력되었겠지만 그렇지 않았다.
    - 그렇다면 `inner`는 `outer`가 실행되지 않았는데도 `outer`에 선언된 `msg`라는 변수를 참조했다는 말이 된다.
    - 이를 가능하게 한 것이 클로저이다.
    - 클로저는 함수를 둘러싼 환경을 계속 유지하다가, 함수가 호출되면 해당 환경에서 함수가 실행될 수 있도록 해준다.
    - 위 예시에서는 `my_func`에 저장된 함수가 클로저로, `outer`가 `inner`를 반환 할 때의 환경을 유지하고 있다가 클로저 함수(`my_func`에 할당된 함수)가 실행 될 때 해당 환경에서 함수를 실행시킨 것이다.

  - 확인
    - `dir` 함수로 클로저 함수를 분석해본다.
    - 클로저가 생성될 때 저장 된 `World`를 확인 가능하다.
    - 클로저가 아니더라도 `__closure__`라는 값을 가지고는 있으나, 클로저가 아닐 경우 None으로 고정되어 있다.

  ```python
  def outer():
      msg = "World!"
      print("Execute?")
      def inner():
          print("Hello {}".format(msg))
  	
      return inner
  
  my_func = outer()
  
  print(dir(my_func))					# [..., '__closure__', ...]
  # __closure__는 튜플 형태다.
  print(type(my_func.__closure__))	# <class 'tuple'>
  print(dir(my_func.__closure__[0]))	# [..., 'cell_contents', ...]
  print(my_func.__closure__[0].cell_contents)	# World!
  ```





# 데코레이터

- 일급 객체(First-class citizen)

  - 일급객체는 OOP에서 사용되는 주요 개념 중 하나로 아래의 조건을 만족하는 객체를 의미한다.
    - 변수 혹은 자료 구조 안에 담을 수 있어야 한다.
    - 매개 변수로 전달 할 수 있어야 한다.
    - 리턴값으로 사용될 수 있어야 한다.
  - 일급 함수
    - 일급 객체의 조건을 만족하면서 실행 중(run-time)에 함수를 생성할 수 있으면 일급 함수라 부른다.
    - 혹은 일급 객체가 함수일 경우 일급 함수라 부르기도 한다.
  - Python의 함수는 위의 모든 조건을 만족하므로 일급 객체라고 할 수 있다.
    - python의 함수는 def 안에서 def으로 함수를 만들거나, lambda를 활용하여 실행 중에 함수를 생성할 수 있으므로 일급 함수이기도 하다.

  ```python
  def print_message(message):
      print(message)
  
  # 변수에 할당할 수 있다.
  my_func = print_message
  my_func("Hello!")	# Hello!
  
  # 자료구조에 담을 수 있다.
  my_list = [print_message]
  my_list[0]("Hello!")	# Hello!
  
  # 매개변수로 전달이 가능하고 리턴값으로 사용될 수 있다.
  def return_func(func):
      return func
  
  my_func = return_func(print_message)
  my_func("Hello!")
  ```



- 데코레이터

  - 함수를 꾸며주는 함수이다.
    - 특정 함수가 실행되기 전, 혹은 실행된 후 부가적인 처리가 필요할 때 해당 처리를 해주는 함수이다.
    - 기존 함수의 수정 없이 데코레이터만 추가해주면 되므로 보다 간결한 코드를 작성할 수 있다.
    - 클로저를 활용하는데, 일반적인 클로저와의 차이는 인자로 함수를 넘긴다는 것이다.
  - Decorator 기본 형태
    - `deco_func`이라는 데코레이터 함수는 `say_name`라는 함수를 꾸며주는 역할을 한다.

  ```python
  def deco_func(orig_func):
      def wrapper_func():
          print("Hello!")
          orig_func()	# 2
          print("Bye!")
      return wrapper_func
  
  def say_name():	# 3
      print("Cha")
  
  
  my_var = deco_func(say_name)	# 함수를 인자로 넘긴다.
  my_var()	# 1
  ```
  
  - `@`와 데코레이터 함수명으로 보다 간결하게 사용하기
    - 꾸며주려는 함수 위에 `@<함수명>`을 입력하여 보다 간결하게 작성이 가능하다.
  
  ```python
  def deco_func(orig_func):
      def wrapper_func():
          print("Hello!")
          orig_func()
          print("Bye!")
      return wrapper_func
  
  @deco_func
  def say_name():
      print("Cha")
  
  say_name()
  '''
  Hello!
  Cha
  Bye!
  '''
  ```
  
  - 사용하는 이유1
    - 기존 함수의 변경 없이 기능 변경이 가능하다.
    - 위 예시에서 `say_name`이 실행되기 전에 `Hello`를 출력하고자 한다면 기존 함수인 `say_name`에 `print("Hello")`를 추가하는 것이 아니라 `wrapper_func`에 추가해주면 된다.
  
  ```python
  def deco_func(orig_func):
      def wrapper_func():
          print("Hello")
          orig_func()
      return wrapper_func
  
  @deco_func
  def say_name():
      print("Cha")
  
  say_name()	# Hello!
  ```
  
  - 사용하는 이유2
    - 많은 함수에 동일하게 들어가는 코드를 간편하게 변경할 수 있다.
  
  ```python
  # 데코레이터를 사용하지 않을 경우 두 함수에 공통으로 들어가는 print("Hello")를 변경하려면 두 함수를 모두 변경해야 한다.
  def func1():
      print("Hello")
      print("World")
   
  def func2():
      print("Hello")
      print("Everyone")
      
  
  # 데코레이터를 사용할 경우
  def deco(orig_func):
      def wrapper_func():
          # 공통으로 들어가는 부분을 여기에 추가해준다.
          print("Hello")
          orig_func()
      return wrapper_func
          
  @deco
  def func1():
      print("World")
  
  @deco
  def func2():
      print("Everyone")
  
  func1()
  func2()
  ```



- 꾸며줄 함수가 인자를 받아야 할 경우
  - 데코레이터를 공유하는 함수들끼리 인자의 개수와 종류가 다를 수 있으므로 `*`, `**`를 활용하여 `wrapper` 함수에서 인자를 받도록 한다.
  - 아래 예시에서 `print_start_message()`는 인자를 받지 않고, `say_hello`는 하나의 인자를 받는다. 따라서 데코레이터가 이들 둘을 동시에 꾸며주기 위해서 `*`, `**`를 활용하여 인자를 받는다.
  
  ```python
  def deco_func(orig_func):
      # 인자를 추가
      def wrapper_func(*args,**kargs):
          print("공통으로 실행할 로직")
          # 인자를 추가
          orig_func(*args,**kargs)
      return wrapper_func
    
  @deco_func
  def print_start_message():
      print("Start")
  
  @deco_func
  def say_hello(name):
      print("Hello {}!".format(name))
  
  print_start_message()
  say_hello("Cha")
  '''
  공통으로 실행할 로직
  Start
  공통으로 실행할 로직
  Hello Cha!
  '''
  ```
  



- 데코레이터 함수가 인자를 받아야 하는 경우

  - 이 경우 실제 데코레이터 역할을 하는 함수 상위에 파라미터를 받기 위한 함수를 선언해준다.

  ```python
  # 파라미터를 받기 위한 함수
  def is_bigger(num):
      # 실제 데코레이터 함수
      def real_decorator(orig_func):
          def wrapper_func(num1, num2):
              sum_num = orig_func(num1, num2)
              if sum_num > num:
                  print(f"my_sum 함수의 결과값은 {num}보다 큽니다.")
              else:
                  print(f"my_sum 함수의 결과값은 {num}보다 작습니다.")
              return sum_num
          return wrapper_func
      return real_decorator
  
  @is_bigger(5)
  def my_sum(num1, num2):
      return num1 + num2
  
  print(my_sum(7,8))
  '''
  my_sum 함수의 결과값은 5보다 큽니다.
  15
  '''
  print(my_sum(1,2))
  '''
  my_sum 함수의 결과값은 5보다 작습니다.
  3
  '''
  ```



- 클래스 형식으로 데코레이터 생성하기
  - 함수 형식이 아닌 클래스 형식으로도 데코레이터를 생성할 수 있다.
  - 그리 자주 쓰이지는 않는다.
  
  ```python
  class DecoClass:
      def __init__(self, orig_func):
          self.orig_func=orig_func
          
      def __call__(self, *args, **kargs):
          print("공통으로 처리할 로직")
          self.orig_func(*args, **kargs)
          
  @DecoClass
  def print_start_message():
      print("Start")
  
  @DecoClass
  def say_hello(name):
      print("Hello {}!".format(name))
  
  print_start_message()
  say_hello("Cha")
  '''
  공통으로 처리할 로직
  Start
  공통으로 처리할 로직
  Hello Cha!
  '''
  ```
  
  - 매개변수를 받는 클래스형 데코레이터 생성하기
    - `__init__`이 아닌 `__call__`에서 꾸며줄 함수를 받는다.
  
  ```python
  class DecoClass:
      def __init__(self, num):
          self.num=num
          
      def __call__(self, orig_func):
          def wrapper(num1, num2):
              result = orig_func(num1, num2)
              if result > self.num:
                  print(f"my_sum 함수의 결과값은 {self.num}보다 큽니다.")
              else:
                  print(f"my_sum 함수의 결과값은 {self.num}보다 작습니다.")
              return result
  
          return wrapper
          
  @DecoClass(8)
  def my_sum(num1, num2):
      return num1 + num2
  
  
  print(my_sum(3, 4))
  '''
  my_sum 함수의 결과값은 8보다 작습니다.
  7
  '''
  ```



- 복수의 데코레이터 설정하기
  - 복수개의 데코레이터를 설정하는 것도 가능하다.
  - 가장 아래에 있는 데코레이터부터 실행된다.
    - 데코레이터 함수 자체는 가장 아래 있는 데코레이터부터 실행되지만 wrapper 함수는 가장 위에 있는 데코레이터부터 실행된다.
  
  ```python
  def deco_func1(orig_func):
      def wrapper_func1(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func1
  
  def deco_func2(orig_func):
      def wrapper_func2(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func2
  
  
  @deco_func2
  @deco_func1
  def print_start_message():
      print("Start")		# Start
  
  print_start_message()
  '''
  wrapper_func1
  print_start_message
  Start
  '''
  ```
  
  - 중첩된 데코레이터가 실행되는 과정
    - `print_start_message` 함수가 실행된다.
    - `deco_func1` 함수에 `print_start_message` 함수가 인자로 전달되면서 실행된다.
    - `deco_func1` 함수가 `wrapper_func1` 함수를 리턴한다.
    - `deco_func2` 함수에 `deco_func1`의 리턴값인 `wrapper_func1`가 인자로 전달되면서 실행된다.
    - `deco_func2` 함수가 `wrapper_func2` 함수를 리턴한다.
    - `wrapper_func2` 함수가 실행되고 자신이 인자로 받은`orig_func`( `wrapper_func1` )을 실행
    - `wrapper_func1`가 실행되고 자신이 인자로 받은 `orig_func`( `print_start_message` )을 실행
    - `print_start_message`가 실행
  
  - `@`를 사용하지 않았을 경우 아래 코드와 같다.
  
  ```python
  def deco_func1(orig_func):
      def wrapper_func1(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func1
  
  def deco_func2(orig_func):
      def wrapper_func2(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func2
  
  
  def print_start_message():
      print("Start")		# Start
  
  decorated_func = deco_func2(deco_func1(print_start_message))
  decorated_func()
  '''
  wrapper_func1
  print_start_message
  Start
  '''
  ```



- `@wraps`
  
  - 위와 같이 중첩된 데코레이터에서 한 데코레이터의 내부 함수가 다른 데코레이터의 인자로 넘어가는 것을 막아주는 역할을 한다.
  - `functools` 모듈에 포함되어 있다.
  
  ```python
  from functools import wraps
  
  
  def deco_func1(orig_func):
      @wraps(orig_func)
      def wrapper_func1(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func1
  
  def deco_func2(orig_func):
      @wraps(orig_func)
      def wrapper_func2(*args,**kargs):
          print(orig_func.__name__)
          orig_func(*args,**kargs)
      return wrapper_func2
  
  @deco_func2
  @deco_func1
  def print_start_message():
      print("Start")
  
  print_start_message()
  '''
  print_start_message
  print_start_message
  Start
  '''
  ```



- 활용

  - 주로 로그 시스템을 만들 때 사용한다.

  ```python
  from functools import wraps
  import datetime
  import time
  
  
  def my_logger(orig_func):
      @wraps(orig_func)
      def wrapper(*args, **kwargs):
          timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
          print(
              '[{}] 실행결과 args:{}, kwargs:{}'.format(timestamp, args, kwargs))
          return orig_func(*args, **kwargs)
  
      return wrapper
  
  
  def my_timer(orig_func):
      @wraps(orig_func)
      def wrapper(*args, **kwargs):
          start = time.time()
          result = orig_func(*args, **kwargs)
          end = time.time() - start
          print('{} 함수가 실행된 총 시간: {} 초'.format(orig_func.__name__, end))
          return result
  
      return wrapper
  
  
  @my_timer
  @my_logger
  def display_info(name, age):
      time.sleep(1)
      print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))
  
  display_info('Jimmy', 30)
  ```





# 가상환경

- pyenv

  - python 버전 관리 툴이다.
  - 다양한 버전의 python으로 쉽게 전환할 수 있게 해준다.
  - windows에서는 사용이 불가능하다.
    - 사용 가능하게 만들어주는 패키지가 있지만 아직 불안정하다.
  - 설치하기

  ```bash
  $ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
  ```

  - pyenv 환경변수 설정

  ```bash
  $ vi ~/.bashrc
  
  # 맨 아래에 아래 내용 추가
  export PATH="~/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  ```

  - pyenv 필수 패키지 설치
    - 이 작업을 건너뛰고 그냥 사용할 경우 오류가 날 수 있다.

  ```bash
  $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev
  ```



- 가상환경 생성 방법1. venv 사용하기

  - 생성하기
    - 이 명령을 실행한 경로에 `가상환경 이름`에 해당하는 디렉터리가 생성된다.

  ```bash
  $ python -m venv <가상환경 이름>
  ```

  - 가상환경 활성화 하기

  ```bash
  # 윈도우
  $ source <가상환경 이름>/Scripts/activate
  
  # 리눅스, MacOS
  $ source <가상환경 이름>/bin/activate
  ```

  - 비활성화 하기

  ```bash
  $ deactivate
  ```



- 가상환경 생성 방법2. virtualenv 사용하기

  - virtualenv 모듈 설치

  ```bash
  $ pip install virtualenv
  ```

  - 가상환경 생성하기
    - 역시 명령어를 실행한 디렉토리에 `가상환경 이름`에 해당하는 디렉터리가 생성된다.

  ```bash
  $ virtualenv <가상환경 이름>
  ```

  - 활성화 하기

  ```bash
  # 윈도우
  $ source <가상환경 이름>/Scripts/activate
  
  # 리눅스, MacOS
  $ <가상환경 이름>/bin/activate
  ```

  - 비활성화 하기

  ```bash
  $ deactivate
  ```



- 가상환경 생성 방법3. conda 사용하기

  > 아래 사이트에 들어가서 설치 파일을 다운로드 한다.
  >
  > https://www.anaconda.com/products/individual

  - 리눅스에서 anaconda 설치파일 다운
    - 위 사이트로 들어가 리눅스 설치 경로를 복사해서 아래와 같이 입력

  ```bash
  $ wget <설치 파일 다운로드 경로>
  
  # wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
  ```

  - 설치
    - 설치 중에 몇 가지 선택지가 있는데 모두 yes한다.
    - 설치가 끝나면 터미널 창을 재부팅한다.

  ```bash
  $ bash [위에서 다운 받은 설치 파일 이름]
  ```

  - PATH 설정

  ```bash
  $ source ~/.bashrc
  ```

  - 만일 위 명령어를 입력했음에도 정상적으로 동작하지 않으면 아래와 같이 bashrc를 직접 수정한다.

  ```bash
  $ vi ~/.bashrc
  
  # 아래 내용을 추가해준다.
  # $ export PATH="/home/username/anaconda3/bin:$PATH"
  ```

  - windows의 경우
    - 위 사이트에서 설치 파일을 다운 받아서 설치 해준다.
    - anaconda prompt를 실행한다.
  - 버전 확인

  ```bash
  $ conda --version
  ```

  - 아나콘다 정보 확인

  ```bash
  $ conda info
  ```

  - 아나콘다를 최신 버전으로 업데이트

  ```bash
  $ conda update
  ```

  - 가상환경 생성하기

  ```bash
  $ conda create -n <가상 환경 이름> (python=python 버전)
  ```

  - 가상환경 목록 보기

  ```bash
  $ conda env list
  ```

  - 가상 환경 활성화

  ```bash
  $ conda activate <가상 환경 이름>
  ```

  - 비활성화

  ```bash
  $ conda deactivate
  ```

  - 가상 환경 삭제
    - `--all`: 모든 패키지를 삭제한다.
    - `-n`: 삭제할 가상 환경의 이름을 지정한다.
  
  
  ```bash
  $ conda remove -all -n <가상 환경 이름> 
  ```

  - 패키지 설치
    - `pip`로 설치할 때와  `conda`로 설치할 때의 차이는,  conda는 Python 패키지가 아니라도 설치가 가능하고, 의존성을 가진 패키지가 다 같이 설치되지만 `pip`는Python 패키지만 설치 가능하고, 지정한 패키지만 단독으로 설치된다.
  
  ```bash
  $ conda install <패키지명>(=버전) (패키지명2) (패키지명3)...
  ```
  
  - 특정 가상환경에 패키지 설치
  
  ```bash
  $ conda install -n <가상환경 이름> <패키지 이름>
  ```

  - 특정 패키지 업데이트
    - 패키지명 대신 `--all`을 주면 현재 가상환경에 설치된 모든 패키지가 업데이트 된다.
  
  ```bash
  $ conda update <패키지명>
  ```
  
  - 패키지 목록 보기
    - 패키지명을 옵션으로 주면 해당 패키지가 설치 되었는지를 확인 가능하다.
    - `-n 가상환경 이름`을 주면 해당 가상환경에 설치된 패키지 목록을 보여준다.
  
  ```bash
  $ conda list (패키지명) (-n 가상환경 이름)
  ```






## 심볼릭 링크

- Python은 버전 관리가 필수다.
  - 버전별로 패키지가 관리된다.
    - 따라서 한 버전의 Python으로 잘 동작하는 스크립트가 다른 버전에서는 패키지 문제로 동작하지 않을 수 있다.
    - 예를 들어 3.7 버전을 설치하여 numpy 패키지를 받아서 사용하다가 2.5 버전으로 Python 버전을 변경하면, 해당 버전에서는 numpy를 설치한 적이 없고, 설치한다 하더라도 numpy가 2.5 버전과 호환될지도 미지수이다.
  - 문제 상황 예시
    - 현재 리눅스 서버에서는 python 2.7.5 버전을 사용중인데 python 3.7.5 버전인 가상 환경에서 작업을 하는 중인 경우
    - python 3.7.5 버전을 사용할 것을 가정하고 python  스크립트를 작성했는데 리눅스 서버의 python 버전이 2.7.5라 실행이 되지 않는 경우
    - jupyter notebook에서는 3.7.5 버전을 사용중인데 python 버전이 2.7.5인 리눅스 터미널에서 jupyter notebook으로 작성한 파일을 실행하려 할 경우 
    - 위와 같은 경우에 각기 다른 버전이므로 설치 된 패키지도 다르고 호환도 문제가 될 수 있다.



- 다른 버전의 python 파일을 실행하는 방법.

  - 리눅스에서 python을 실행하는 명령어는 아래와 같다.

  ```bash
  $ python <python 파일명>
  ```

  - 이는 사실 심볼릭 링크가 잡혀 있는 python을 실행하는 명령어로, 다른 python을 실행하고 싶다면 아래와 같이 입력한다.

  ```bash
  $ <다른 python 경로> <python 파일명>
  
  # e.g.1 venv를 통해 생성한 python을 사용하고자 할 경우
  $ /venv/bin/python3 <python 파일명>
  
  # e.g.2 jupyter에서 사용 중인 python 파일을 사용하고자 할 경우
  $ /usr/local/bin/python3.7 <python 파일명>
  ```

  - 만일 실행 할 때마다 위와 같이 python 경로를 일일이 지정해주는 것이 불편하다면, 기본 python을 가리키는 심볼릭 링크를 변경해주면 된다.



- 심볼릭 링크 변경하기(사용하고자 하는 python 버전이 이미 설치되어 있다고 가정)

  - 현재 사용중인 파이썬 위치 확인

  ```bash
  $ which python
  ```

  - 심볼릭 링크가 가리키는 파일 확인

  ```bash
  $ ls -al <위에서 확인한 경로>
  ```

  - 데비안 계열 리눅스에서 심볼릭 링크 변경하기
    - `update-alternatives` 명령어를 지원한다.
    - 사용하고자 하는 python 경로를 추가하고, 이후에 어떤 경로의 python을 사용할지 선택한다.

  ```bash
  # python 경로 추가(복수의 python 경로를 추가 가능하다)
  $ update-alternatives --install <위에서 확인한 경로> python <사용하고자 하는 python 경로>
  # 사용할 python 선택(아래 명령어를 입력하면 선택 창이 뜨는데 원하는 번호를 입력하면 된다)
  $ update-alternatives --config python
  ```

  - 이외의 리눅스에서 심볼릭 링크 걸기
    - 안될 경우 `rm <위에서 확인한 경로>`로 기존 경로를 지워준다.

  ```bash
  $ ln -s <사용하고자 하는 python 경로> <위에서 확인한 경로>
  ```



## pip 없이 패키지 설치하기

- `.whl` 파일 다운 받기
  - pypi 사이트에서 원하는 패키지의 `whl` 파일을 다운 받는다.
    - `zip` 파일도 가능하다.
  - `Download files`에서 확인 가능하다.



- 설치하기

  - 아래 명령어로 설치한다.

  ```bash
  $ python -m pip install <whl(zip)파일 경로>
  ```





# 동시성, 병렬성 프로그래밍

- 동시성과 병렬성
  - 프로그램을 구현했는데 성능이 부족한 경우 고려해볼만 하다.
  - 동시성
    - 흔히 말하는 멀티 태스킹
    - A,B,C라는 태스크가 있을 때 이를 잘게 분할하여  A,B,C를 조금씩 번갈아가면서 처리하는 방식
    - 실제로는 A,B,C를 동시에 수행하는 것은 아니지만, 동시에 수행하는 것 처럼 보인다.
  - 병렬성
    - 동시성이 사실 한 순간에 하나의 일만 처리하는 것이라면, 병렬성은 실제로 한 순간에 여러 개의 일을 처리하는 것을 의미한다.
    - A,B,C라는 태스크가 있을 때 이를 모두 동시에 수행하는 것이다.
  - 어떤 것을 선택해야 하는가
    - 얼핏 병렬성을 사용하는 것이 더 좋아보이지만 항상 그런 것은 아니다.
    - 병렬성은 물리적인 코어의 개수에 제한이 있다.
    - 일반적인 컴퓨터에는 쿼드 코어(4개의 코어) CPU를 사용하므로 한 순간에 처리할 수 있는 일의 양이 제한적이다.
    - 만약 어떤 작업이 I/O 위주의 작업이라면 실제로 CPU가 처리해야 하는 시간은 상대적으로 적으며 대부분은 대기하는 데 소모한다.
    - 따라서 I/O 위주의 작업이 많다면 동시성이 더 유리할 수 있다.



- 프로세스와 스레드
  - 프로세스
    - 운영체제에서 어떤 프로그램이 실행될 때  CPU, memory와 같은 컴퓨터 자원을 사용한다.
    - 따라서 운영체제는 프로그램이 실행될 수 있는 전용 공간을 할당하는데, 이를 프로세스라 한다.
    - 즉, 프로그램이 메모리에 올라가서 실행 중인 것을 프로세스라 한다.
  - 스레드
    - 프로세스 내부에서 작업을 처리하는 주체를 스레드라 부른다.
    - 스레드는 프로세스 내부에 할당 된 자원을 공유한다.
    - 프로세스는 최소 하나 이상의 스레드를 갖으며 경우에 따라 여러 개의 스레드를 가질 수 있다.
    - 운영체제가 동시에 실행되는 여러 프로그램을 관리하는 작업을 스케줄링이라 하는데, 스케줄의 단위로 스레드를 사용한다.
  - 비유
    - 예를 들어 프로세스가 공장의 라인이라면, 스레드는 해당 라인에서 작업을 처리하는 직원이라고 할 수 있다.



- Python thread

  - Python에서 스레드를 다루는 다양한 방법이 있다.
    - 기본 모듈인 thread와 threading이 있는데 threading 모듈을 더 자주 사용한다.
    - 이 외에도 GUI 라이브러리인 PyQt의 QThread를 사용하기도 한다.
  - 예시
    - 메인 스레드가 5개의 서브 스레드를 생성하고  `start`메서드를 호출하여 `Worker` 클래스에 정의한 `run`메서드를 호출한다.
    - 메인 스레드와 5개의 서브 스레드는 운영체제의 스케줄러에 의해 스케줄링 되면서 실행된다.
    - 가장 먼저 메인 스레드가 끝나게 되고 서브 스레드들은 시작 순서와는 다르게 종료된다.
    - 기본적으로 메인 스레드에서 서브 스레드를 생성하면 메인 스레드는 자신의 작업을 모두 마쳤더라도 서브 스레드의 작업이 종료될 때 까지 기다렸다가 서브 스레드의 작업이 모두 완료되면 종료된다.

  ```python
  import threading
  import time
  
  
  class Worker(threading.Thread):
      def __init__(self, name):
          super().__init__()
          self.name = name
  
      def run(self):
          print("sub thread start", threading.currentThread().getName())
          time.sleep(3)
          print("sub thread end", threading.currentThread().getName())
  
  print("main thread start")
  for i in range(5):
      name = "thread {}".format(i)
      t = Worker(name)
      t.start()
  print("main thread end")
  
  '''
  main thread start
  sub thread start thread 0
  sub thread start thread 1
  sub thread start thread 2
  sub thread start thread 3
  sub thread start thread 4
  main thread end
  sub thread end thread 4
  sub thread end thread 1
  sub thread end thread 3
  sub thread end thread 2
  sub thread end thread 0
  '''
  ```

  - 데몬 스레드
    - 데몬 스레드는 메인 스레드가 종료될 때 함께 종료되는 서브 스레드를 의미한다.
    - 메인 스레드가 종료되면 서브 스레드도 종료되어야 하는 경우에 사용한다.
    - 아래 코드의 경우 메인 스레드가 종료되면 메인 스레드는 더 이상 서브 스레드의 종료를 기다리지 않고, 서브 스레드도 함께 종료된다.

  ```python
  import threading
  import time
  
  
  class Worker(threading.Thread):
      def __init__(self, name):
          super().__init__()
          self.name = name
  
      def run(self):
          print("sub thread start ", threading.currentThread().getName())
          time.sleep(3)
          print("sub thread end ", threading.currentThread().getName())
  
  
  print("main thread start")
  for i in range(5):
      name = "thread {}".format(i)
      t = Worker(name)
      t.daemon = True		# 이 부분을 추가해준다.
      t.start()
  
  print("main thread end")
  
  '''
  main thread start
  sub thread start  thread 0
  sub thread start  thread 1
  sub thread start  thread 2
  sub thread start  thread 3
  sub thread start  thread 4
  main thread end
  '''
  ```

  - Fork와 Join

    - 메인 스레드가 서브 스레드를 생성하는 것을 fork, 모든 스레드가 작업을 마칠 때 까지 기다리는 것을 join이라 한다.

    - join의 경우 보통 데이터를 여러 스레드를 통해서 병렬로 처리한 후 그 값들을 다시 모아서 순차적으로 처리해야 할 필요가 있을 때 사용한다.
    - 아래 실행 결과를 보면 t1, t2 스레드가 종료된 후 `main thread post job`이 출력된 것을 확인 가능하다.
    - 위 예제에서는 메인 스레드가 모든 실행을 완료한 후 서브 스레드가 종료될 때까지 기다렸지만 이 예제에서는 `join` 메서드가 호출되는 지점에서 기다린다는 차이가 있다.

  ````python
  import threading
  import time
  
  
  class Worker(threading.Thread):
      def __init__(self, name):
          super().__init__()
          self.name = name
  
      def run(self):
          print("sub thread start ", threading.currentThread().getName())
          time.sleep(5)
          print("sub thread end ", threading.currentThread().getName())
  
  
  print("main thread start")
  
  t1 = Worker("1")
  t1.start()
  
  t2 = Worker("2")
  t2.start()
  
  t1.join()
  t2.join()
  
  print("main thread post job")
  print("main thread end")
  '''
  main thread start
  sub thread start  1
  sub thread start  2
  sub thread end  2
  sub thread end  1
  main thread post job
  main thread end
  '''
  ````

  - 여러 서브 스레드를 생성해야하는 경우에는 생성된 스레드 객체를 list에 저장한 후 반복문을 이용해서 각 객체에서 `join()` 메서드를 호출할 수 있다.

  ```python
  import threading
  import time
  
  
  class Worker(threading.Thread):
      def __init__(self, name):
          super().__init__()
          self.name = name
  
      def run(self):
          print("sub thread start ", threading.currentThread().getName())
          time.sleep(5)
          print("sub thread end ", threading.currentThread().getName())
  
  
  print("main thread start")
  
  threads = []
  for i in range(3):
      thread = Worker(i)
      thread.start()
      threads.append(thread)
  
  
  for thread in threads:
      thread.join()	# join 메서드 호출
  
  print("main thread post job")
  print("main thread end")
  ```

