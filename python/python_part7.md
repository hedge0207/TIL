

# 이터레이터와 제너레이터

## 이터레이터

- 이터레이터
  - 값을 차례대로 꺼낼 수 있는 객체를 의미한다.
    - 반복자라고도 부른다.
    - 단순하게 말해서, `__iter__`, `__next__` 메서드를 지닌 객체를 말한다. 
  - `range`는 이터레이터를 생성하는 함수로, `range(10)`은 실제로 10개의 숫자를 생성하는 것이 아니라 이터레이터를 생성하는 것이다.
    - 이터레이터만 미리 생성하고 값이 필요한 시점이 되었을 때 값을 만든다.
    - 이처럼 데이터 생성을 뒤로 미루는 방식을 **지연평가**(lazy evaluation)라 한다.
  - 시퀀스 객체와의 차이
    - 시퀀스 객체는 기본적으로 반복 가능한 객체에 포함된다.
    - 단, 시퀀스 객체는 이터러블한 객체 중에서도 순서가 보장되는 객체만을 의미한다.
  - 이터레이터와 이터러블의 차이
    - 이터러블은 반복 가능한 객체를 의미하며 `__iter__` 메서드만 가지고 있으면 이터러블이다.
    - 이터레이터는 값을 차례대로 꺼낼 수 있는 객체를 의미하며 `__iter__`메서드와 `__next__`메서드를 가지고 있으면 이터레이터이다.
    - 즉 리스트, 튜플 등의 이터러블한 객체는 그 자체로 값을 차례로 꺼낼 수 있지 않다.
    - 값을 차례로 꺼내기 위해서는 `__iter__`메서드를 통해 이터레이터를 생성한 뒤 해당 이터레이터의 `__next__`메서드를 통해 값을 차례로 꺼내는 것이다.



- 이터레이터인지 확인하기

  - 먼저 객체에 `__iter__` 메서드가 있는지 확인한다.
    - `__iter__` 메서드는 이터레이터를 반환하는 메서드이다.
  
  
  ```python
  my_list = [1, 2, 3]
  print(dir(my_list))	# [..., '__iter__', ...]
  ```

  - `__iter__`를 호출하면 이터레이터가 반환된다.
  
  ```python
  my_list = [1, 2, 3]
  print(my_list.__iter__())	# <list_iterator object at 0x7fcd468eb580>
  ```
  
  - 다음으로 `__next__` 메서드가 있는지 확인한다. 
    - `__next__` 메서드는 호출할 때 마다 다음 값을 리턴하는 메서드이다.
    - 더 이상 꺼낼 요소가 없다면 `StopIteration` 예외를 발생시킨다.
  
  
  ```python
  my_list = [1, 2, 3]
  my_iter = my_list.__iter__()
  print(my_iter.__next__())	# 1
  print(my_iter.__next__())	# 2
  print(my_iter.__next__())	# 3
  print(my_iter.__next__())	# StopIteration
  ```
  
  - `range`의 동작 방식
    - `range(3)`는 이터레이터를 생성한다.
    - `range`에서 `__iter__`를 통해 이터레이터를 얻는다.
    - 반복할 때마다 이터레이터에서 `__next__`를 통해 반복을 수행한다.
    - 더 이상 꺼낼 것이 없으면  `StopIteration` 예외가 발생하고 반복이 종료된다.
    - `range`뿐 아니라 모든 이터레이터에 적용된다.
  - `__iter__`와 `__next__`를 가진 객체를 "이터레이터 프로토콜을 지원하는 객체"라고 말한다.



- 이터레이터 직접 구현하기

  - `__iter__`와 `__next__`메서드를 직접 구현하여 이터레이터를 만들 수 있다.
    - Python spec에 따르면 `__iter__`함수는 자기 자신(iterator)을 반환해야 한다.
  
  
  ```python
  class Iterator:
      def __init__(self, end):
          self.cur = 0
          self.end = end
         
      def __iter__(self):
          return self
      
      def __next__(self):
          if self.cur < self.end:
              num = self.cur
              self.cur += 1
              return num
          else:
              raise StopIteration	# 반복을 끝내기 위한 StopIteration
          
  class Iterable:
      # 인자로 반복을 끝낼 숫자를 받아 Iterator를 생성한다.
      def __init__(self, end):
          self.iter = Iterator(end)
  	
      # __init__에서 생성한 Iterator를 반환한다.
      def __iter__(self):
          return self.iter
  
  
  for i in Iterable(3):
      print(i)
  ```



- 이터레이터 언패킹

  - 이터레이터는 언패킹이 가능하다.

  ```python
  a, b, c = range(3)
  ```

  - 반환값을 _에 저장하는 경우
    - 반환값을 언더바에 저장하는 경우는 특정 반환값을 사용하지 않겠다는 관례적 표현이다.

  ```python
  # range의 반환값을 받기는 하지만 사용은 하지 않는다.
  for _ in range(3):
      print("Hello World!")
  ```



- 인덱스로 접근할 수 있는 이터레이터 만들기

  - 인덱스를 통한 접근은  `__getitem__`메서드를 통해 이루어진다.
    - 즉 `my_list[1]`은 사실 `my_list.__getitem__(1)`을 호출하는 것이다.

  ```python
  my_list = [1, 2, 3]
  print(my_list.__getitem__(2))	# 3
  ```

  - 이터레이터 생성
    - `__getitem__`만 구현해도 이터레이터가 되며, `__iter__`, `__next__`는 생략해도 된다.

  ```python
  class MyIter:
      def __init__(self, end):
          self.end = end
         
      def __getitem__(self, index):
          if index < self.end:
              return index
          else:
              raise IndexError
  
              
  for i in MyIter(3):
      print(i)
  ```



- `iter`, `next` 함수 사용하기

  - `iter`는 객체의 `__iter__` 메서드를 호출하고, `next`는 객체의 `__next__`메서드를 호출해준다.

  ```python
  my_iter = iter(range(3))
  print(next(my_iter))	# 1
  print(next(my_iter))	# 2
  print(next(my_iter))	# 3
  print(next(my_iter))	# StopIteration
  ```

  - iter는 반복을 끝낼 값을 지정하면 해당 값이 나올 때 반복을 종료한다.
    - 이 경우 반복 가능한 객체 대신 호출 가능한 객체를 넣어준다.
    - 반복을 끝낼 값을  sentinel이라 부른다.
    - iter 함수를 활용하면  조건문으로 매번 해당 숫자인지 검사하지 않아도 되므로 코드가 좀 더 간결해진다.

  ```python
  # iter(호출 가능한 객체, 반복을 끝낼 값)
  my_iter = iter(lambda : random.randint(0, 5), 2)
  # 2가 나올때까지 계속 반복한다.
  for i in my_iter:
      print(i)
  ```

  - `next`
    - 기본값을 지정할 수 있다.
    - 기본값을 지정하면 반복이 종료돼도 `StopIteration`이 발생하지 않고 기본값을 출력한다.

  ```python
  my_iter = iter(range(3))
  print(next(my_iter, 10))	# 1
  print(next(my_iter, 10))	# 2
  print(next(my_iter, 10))	# 3
  print(next(my_iter, 10))	# 10
  ```





## 제너레이터

- 제너레이터
  - 이터레이터를 생성해주는 함수이다.
    - 즉, 제너레이터 객체는 이터레이터이다.
    - 발생자라고도 부른다.
  - 이터레이터는 훌륭한 기능이지만, 작성해야 하는 코드가 많아진다는 단점이 있다.
    - 이터레이터는 클래스에 `__iter__`와 `__next__`  또는 `__getitem__` 메서드를 구현해야 하지만 제너레이터는 함수 안에서 `yield`라는 키워드만 사용하면 된다.
    - 이터레이터를 클래스로 작성하는 것 보다 훨씬 간단하게 작성이 가능하다.



- `yield`

  - 제네레이터를 만들기 위한 Python keyword
    - yield는 ''양보하다''라는 뜻도 가지고 있는데, 함수 바깥으로 전달하면서 코드 실행을 함수 바깥에 양보한다는 의미에서 `yield`를 키워드로 지정한 것이다.
  - 함수 안에서 yield를 사용하면 함수는 제너레이터가 되며, yield에는 값을 지정한다.
    - `number_generator` 함수를 호출하면 **제터레이터 객체가 반환**된다(함수가 실행되는 것이 아니다).
    - 제네레이터는 `__next__` 메서드가 호출될 때마다 yield 까지 코드를 실행하며, yield에서 값을 발생시킨다.
    - yield가 값을 발생시킨 후에는 다음 `__next__` 메서드가 실행되기 전까지 함수 바깥으로 코드 실행을 양보한다.

  ```python
  def number_generator():
      print("Hello!")
      yield 0
      print("Good")
      yield 1
      print("Morning!")
      yield 2
   
  for i in number_generator():
      print(i)
  '''
  Hello!
  0
  Good
  1
  Morning!
  2
  '''
  ```

  - 제너레이터 객체가 이터레이터인지 확인하기
    - `__iter__`, `__next__` 메서드가 있는지 확인한다.

  ```python
  def number_generator():
      yield 0
      yield 1
      yield 2
  
  print(dir(number_generator()))
  # [..., '__iter__', ..., '__next__', ...]
  ```

  - `yield`와 `return`
    - `yield`도 `next` 함수와 마찬가지로 제너레이터 함수 끝까지 도달하면 `StopIteration` exception이 발생한다.
    - `return`도 마찬가지로 중간에 return이 될 경우 `StopIteration` exception이 발생한다.

  ```python
  def number_generator():
      yield 0
      yield 1
  
  
  ng = number_generator()
  print(next(ng))		# 0
  print(next(ng))		# 1
  print(next(ng))		# StopIteration
  
  
  def number_generator():
      yield 0
      return
  
  
  ng = number_generator()
  print(next(ng))		# 0
  print(next(ng))		# StopIteration
  ```



- 제너레이터 만들기

  - `range()`와 유사하게 동작하는 제터레이터 만들기

  ```python
  def numger_generator(end):
      n = 0
      while n < end:
          yield n
          n += 1
  
  for i in number_generator(3):
      print(i)
  ```

  - yield에서 함수 호출하기

  ```python
  def cap_generator(animals):
      for animal in animals:
          yield animal.upper()
          
          
  animals = ['dog', 'cat', 'tiger', 'lion']
  for i in cap_generator(animals):
      print(i, end=" ")	# DOG CAT TIGER LION
  ```

  - 표현식으로도 생성이 가능하다.

  ```python
  print((i for i in range(10)))
  # <generator object <genexpr> at 0x7fb97a4ea900>



- `yield from`

  - `yield from`은 다른 반복 가능한 객체에 실행을 위임하기 위해 사용한다.
    - `yield from`에는 반복 가능한 객체를 지정한다.
    - 바깥쪽 호출자와 가장 안쪽에 있는 하위 제너레이터 사이에 양방향 채널을 열어주는 역할을 한다.
  - `yield from` 관련 용어
    - 대표 제너레이터(delegating generator): `yield from <반복형>`을 담고 있는 제너레이터 함수, 즉 다른 제너레이터를 호출하는 제너레이터.
    - 하위 제너레이터(subgenerator): `yield from` 표현식 중 <반복형> 가져오는 제너레이터.
    - 호출자(caller): 대표 제너레이터를 호출하는 코드.
  - `yield from`의 동작 원리
    - `yield from`은 뒤에 오는 반복자의 `iter` 메서드를 호출한다.
    - 하위 제너레이터가 실행되는 동안 대표 제너레이터는 중단된다.
    - 호출자는 하위 제너레이터에 데이터를 직접 전송하고, 하위 제너레이터는 다시 데이터를 생성해서 호출자에 전달한다.
    - 하위 제너레이터가 실행을 완료하고 인터프리터가 반환된 값을 첨부한 StopIteraion을 발생시키면 대표 제너레이터가 실행을 재개한다.
    - 따라서 반드시 하위 제너레이터에 종료 조건이 있어야한다.
  
  - `yield from`을 사용하지 않고 여러 번 바깥으로 전달하기
    - 기존에는 아래와 같이 반복문을 사용하여 전달했다.
  
  
  ```python
  def number_generator():
      x = [1, 2, 3]
      for i in x:
          yield i
   
  for i in number_generator():
      print(i)
  ```
  
  - `yield from`을 사용하면 반복문을 사용하지 않고 여러 번 바깥으로 전달할 수 있다.
    - 반복이 종료될 때 까지 `yield from x`가 계속 실행된다.
    - 즉, `yield from`에 지정한 반복 가능한 객체가 종료될 때 까지 해당 객체에 실행을 양보한다.
  
  ```python
  def number_generator():
      x = [1, 2, 3]
      yield from x
      print("Hello!")
  
  for i in number_generator():
      print(i)
  '''    
  1
  2
  3
  Hello!
  '''
  ```
  
  - `yield from` 뒤에 제네레이터 객체도 지정이 가능하다.
  
  ```python
  def number_generator(end):
      n = 0
      
      while n < end:
          yield n
          n += 1
   
  def three_generator():
      # 제네레이터인 number_generator를 지정
      yield from number_generator(3)
   
  for i in three_generator():
      print(i)
  ```
  
  - `yield from`의 pseudo code(단순화 한 버전)
    - PEP 380에서 제안된 `yield from`이 사용된 대표 제너레이터의 내부 sudo code를 더 단순화 시킨 것이다.
    - 실제로는 호출자가 호출하는 `throw()`와 `close()`를 처리해서 하위 제너레이터에 전달해야 하므로 실제 논리는 더 복잡하다.
  
  ```python
  """
  RESULT = yield from EXPR
  위와 같은 yield from 구문은 아래 과정을 거치게 된다.
  """
  
  
  # 하위 제너레이터를 가져온다.
  _i = iter(EXPR)
  try:
      _y = next(_i)	# 하위 제너레이터를 기동시킨다.
  except StropIteration as _e:
      _r = _e.value	# StopIteration이 발생하면 예외 객체에서 value 속성을 꺼내 _r에 할당한다.
  else:
      # 이 루프가 실행되는 동안 외부적으로 대표 제너레이터의 실행은 중단된다.
      while 1:
          _s = yield _y	# 하위 제너레이터에서 생성한 값을 그대로 생성하고, 호출자가 보낼 _s를 기다린다.
          try:
              _y = _i.send(_s)	# 호출자가 보낸 _s를 하위 제너레이터에 전달하고, 하위 제네레이터의 실행이 재개된다.
          # 하위 제너레이터가 StopIteraion 예외를 발생시키면, 예외 객체 안의 value 속성을 가져와 _r에 할당한다.
          # 그 후 루프를 빠져나오고 대표 제너레이터의 실행을 재개한다.
          except StopIteration as _e:	
              _r = e.value
              break
  # _r이 전체 yield from의 표현식 값이 되어 RESULT에 저장된다.
  RESULT = _r
  ```
  
  - `yield from`의 pseudo code 전체
    - 전체 코드에서 yield는 단 한 번밖에 사용되지 않는다.
  
  ```python
  EXPR = "QWE"
  
  _i = iter(EXPR)
  try:
      _y = next(_i)
  except StopIteration as _e:
      _r = _e.value
  else:
      while 1:
          try:
              _s = yield _y
          # 대표 제너레이터와 하위 제너레이터의 종료를 처리한다.
          except GeneratorExit as _e:
              try:
                  _m = _i.close
              # 모든 반복형이 하위 제너레이터가 될 수 있으므로, 하위 제너레이터에 close()메서드가 없을 수 있다.
              except AttributeError:
                  pass
              else:
                  _m()
              raise _e
          # 호출자가 throw로 던진 예외를 처리한다.
          except BaseException as _e:
              _x = sys.exc_info()
              try:
                  _m = _i.throw
              # 하위 제너레이터에 throw() 메서드가 구현되어있지 않을 경우
              # 대표 제너레이터레서 예외가 발생한다.
              except AttributeError:
                  raise _e
              else:
                  # 하위 제너레이터가 throw 메서드를 가진 경우, 호출자로부터 받은 예외를 이용해서 호출한다.
                  # 하위 제너레이터는 예외를 처리하거나(이 경우 루프는 계속 실행된다).
                  try:
                      _y = _m(*_x)
                  # StopIteration 예외를 발생시키거나
                  # 여기서 처리할 수 없는 예외를 발생시킬 수도 있다(이 예외는 대표 제너레이터로 전파된다)
                  except StopIteration as _e:
                      _r = _e.value
                      break
          # yield문에서 예외가 발생하지 않은 경우
          else:
              try:
                  # 마지막으로 호출자로부터 받은 값이 None이면 next 호출
                  if _s is None:
                      _y = next(_i)
                  # 아니면 send를 호출한다.
                  else:
                      _y = _i.send(_s)
              except StopIteration as _e:
                  _r = _e.value
                  break
  RESULT = _r
  ```







# 코루틴

- 메인루틴과 서브루틴

  - 아래 예시에서 직접 실행한 `say`가 메인 루틴, 메인 루틴 내부에서 실행된 `excuse`가 서브 루틴이다.
    - 꼭 함수 사이에만 성립하는 것은 아니다.
  - 메인 루틴이 먼저 실행되고 서브루틴이 실행되는데 서브루틴이 실행되는 동안 메인루틴은 서브루틴이 종료될 때까지 대기하다가, 서브루틴이 종료되면 다시 실행된다.
  - 서브루틴은 메인 루틴에 종속된 관계다.
    - 서브 루틴이 끝나면 서브 루틴의 내용은 모두 사라진다.

  ```python
  def excuse():
      print("Excuse me")
  
  def say(msg):
      excuse()
      print(msg)
      
  say("May I help you?")
  ```



- 코루틴
  - Cooperative routine의 약어로 서로 협력하는 루틴이다.
    - 메인 루틴과 서브 루틴처럼 종속된 관계가 아니라 서로 대등한 관계이며 특정 시점에 상대의 코드를 실행한다.
    - 메인루틴-서브루틴과 마찬가지로 한 루틴이 실행되는 동안 다른 루틴은 대기상태에 있게 된다.
  
  - 함수의 코드를 실행하는 지점을 진입점(entry point)라 하는데 코루틴은 진입점이 여러 개인 함수이다.
    - 코루틴은 함수가 종료되지 않은 상태에서 메인 루틴의 코드를 실행한 뒤 다시 돌아와 코루틴의 코드를 실행한다.
    - 따라서 코루틴이 종료되지 않으므로 코루틴의 내용도 계속 유지된다.
  
  - 제너레이터의 특별한 형태이다.
    - 제너레이터는 yield로 값을 발생시키지만, 코루틴은 `send()`로 값을 받아올 수 있다.
    - 코루틴을 명확히 정의하기는 쉽지 않지만 일반적으로 "`send`를 호출하거나 `yield from`을 이용해서 데이터를 보내는 클라이언트에 의해 실행되는 제너레이터"로 정의한다.
    
  - 코루틴은 네 가지 상태를 가진다.
  
    > inspect.getgeneratorstate 함수로 확인 가능하다.
  
    - GEN_CREATED: 실행을 위해 대기하고 있는 상태
    - GEN_RUNNING: 현재 인터프리터가 실행하고 있는 상태(이 상태는 다중 스레드에서만 볼 수 있다)
    - GEN_SUSPENDED: 현재 yield 문에서 대기하고 있는 상태
    - GEN_CLOSED: 실행이 완료된 상태



- 코루틴에 값 보내기

  - 코루틴에 값을 보낼때는 `send` 메서드를 사용한다.
    - `yield`와 그 뒤의 값에 괄호를 씌울 경우 연산 우선순위를 조정 가능하다(예를 들어 `yield x + y`와 `(yield x) + y`는 다르다).
  
  
  ```python
  def my_coroutine():
      # 코루틴을 유지하기 위해 무한 루프를 사용한다.
      while 1:
          num = yield	# 코루틴 바깥에서 받은 값을 받아서 사용.
          print(num)
  
  # 코루틴 생성
  co = my_coroutine()
  # 코루틴 내부의 yield까지 함수 실행(최초)
  next(co)
  
  co.send(1)	# 코루틴에 숫자 1 보내기
  co.send(2)	# 코루틴에 숫자 2 보내기
  co.send(3)	# 코루틴에 숫자 3 보내기
  ```
  
  - 실행 과정
    - 메인 루틴에서 코루틴을 생성하고 `next()`를 통해 코루틴을 실행한다.
    - `while`문이 실행되고 `yield` 키워드를 만나면서 메인루틴에 실행을 넘겨준다.
    - `send()`를 통해 코루틴에 값을 보내고, num이 출력된후 다시 반복문을 돌아 `yield` 키워드를 만나면서 메인루틴에 실행을 넘겨준다.



- 기동(primming)

  - 코루틴은 기동(primming) 과정이 필요하다. 
    - 즉, 코루틴 객체를 생성하고 난 후, `next`를 통해 코루틴이 호출자로부터 값을 받을 수 있도록 처음 나오는 `yield`문까지 실행을 진행하는 과정이 필요하다.
    - 만일 기동 과정 없이 `send`를 호출하면 error가 발생하는데, 이는 data를 받아올 `yield`문이 아직 실행되지도 않았기 때문이다.
  - Decorator를 통해서 코루틴 생성 시에 자동으로 기동이 되게 할 수 있다.
    - 단, 모든 코루틴이 이러한 방식으로 기동되는 것 만은 아니라는 것을 염두에 두어야 한다.
    - 예를 들어 `yield from`은 뒤에 오는 코루틴이 기동된 적 없다고 가정하고 자동으로 기동을 시킨다(따라서 아래와 같이 decorator를 사용하면 2번 기동된다).
  
  
  ```python
  def coroutine(func):
      def wrapper(*args, **kwargs):
          gen = func(*args, **kwargs)
          next(gen)
          return gen
      return wrapper
  
  @coroutine
  def test_coro():
      cnt = -10
      while cnt<0:
          x = yield cnt
          cnt+=1
          print(x)
  
  coro = test_coro()
  for i in range(0,10):
      print(coro.send(i))
  ```



- 코루틴 바깥으로 값 내보내기

  - `yield 변수` 형식으로 yield에 변수를 지정하면 값을 받아오면서 바깥으로 값을 전달한다.
    - `yield`로 바깥으로 전달한 값은 next 함수와 send 메서드의 반환값으로 나오게 된다. 

  ```python
  def sum_coroutine():
      total = 0
      while True:
          num = yield total    # 코루틴 바깥에서 값을 받아오면서 바깥으로 값을 전달
          total += num
   
  co = sum_coroutine()
  print(next(co))      # 0
   
  print(co.send(1))    # 1
  print(co.send(2))    # 3
  print(co.send(3))    # 6
  ```

  - 실행 과정
    - 메인 루틴에서 코루틴을 생성하고 `next()` 를 통해 코루틴을 실행한다.
    - 실행되면서 yield를 만나게 되고 total을 반환한다.
    - send를 통해 코루틴에 값을 보내고, `total += num`이 실행된 후 다시 반복문을 돌아 `yield`키워드를 만나면서 메인루틴에 실행을 넘겨주고 total을 반환한다.



- 코루틴을 종료하고 예외처리하기

  - 코루틴의 종료
    - 코루틴은 아래의 두 가지 경우에 종료된다.
    - `close()` 메서드를 호출하는 경우
    - 해당 객체에 대한 참조가 모두 사라져 GC 되는 경우
  
  - `close()` 메서드를 통해 코루틴을 종료할 수 있다.
    - Python 스크립트가 끝나도 코루틴이 자동으로 종료된다.
  
  ```python
  def number_coroutine():
      total = 0
      while True:
          num = yield total
          total += num
   
  co = number_coroutine()
  next(co)
   
  for i in range(5):
      print(co.send(i), end=" ")	# 0 1 3 6 10
   
  co.close()
  ```
  
  - `GeneratorExit` 예외처리하기
    - 코루틴 객체의 `close()` 메서드를 호출하면 코루틴이 종료될 때 `GeneratorExit ` 예외가 발생한다.
  
  ```python
  def number_coroutine():
      total = 0
      try:
          while True:
              num = (yield total)
              total += num
      except GeneratorExit:
          print("코루틴 종료")
   
  co = number_coroutine()
  next(co)
   
  for i in range(5):
      print(co.send(i), end=" ")
   
  co.close()
  ```
  
  - 코루틴 안에서 예외 발생시키기
    - 코루틴 안에서 예외를 발생시켜 코루틴 종료하기
    - `throw()` 메서드를 사용한다.
  
  ```python
  def sum_coroutine():
      total = 0
      try:
          while True:
              x = (yield)
              total += x
      except RuntimeError as e:
          print(e)
          yield total    # 종료시 코루틴 바깥으로 값 전달
   
  co = sum_coroutine()
  next(co)
   
  for i in range(5):
      co.send(i)
   
  print(co.throw(RuntimeError, '코루틴 종료'))
  ```



- 코루틴의 반환값 가져오기

  - Python 3.3부터 코루틴이 값을 반환하는 기능이 추가되었다.
  - 코루틴이 종료되면 `StopIteration` 예외가 발생한다.
    - `return` 문이 반환하는 값은 `StopIteration` 예외의 속성이 담겨 호출자에게 전달된다.

  ```python
  from itertools import count
  
  
  def averager():
      total = 0.0
      cnt = 0
      average = None
      while 1:
          term = yield
          if term is None:
              break
          total += term
          cnt += 1
          average = total / cnt
      return average
  
  coro = averager()
  next(coro)
  for i in range(1,4):
      coro.send(i)
  # yield from은 아래 로직을 자동으로 처리해준다.
  try:
  	coro.send(None)
  except StopIteration as e:
      # StopIteration 예외의 value에 코루틴의 반환값이 담기게 된다.
      print(e.value)
  ```



- `yield from`을 사용하여 코루틴의 반환값 가져오기

  - 주의
    - 실제로 아래와 같이 `yield from`을 사용할 일은 거의 없다.
    - Python 3.5 이상부터는 `async`를 대신 사용한다.
  - `yield from` 이 실행되는 동안에는 대표 코루틴의 동작이 멈추게 된다.
  - `yield from` 내부에는 StopIteration 예외가 발생했을 때 해당 예외 객체에서 `value`를 추출하는 작업이 짜여져 있다.
    - 즉 `accumulate`이 `return total`을 만나는 순간 StopIteration가 발생하고 그 객체에 반환값을 넣는다.
    - `yield from`은 반환된 StopIteration 객체에서 value를 추출한다.
  
  
  ```python
  # 합계를 계산할 코루틴
  def accumulate():
      total = 0
      while True:
          x = (yield total)         # 코루틴 바깥에서 값을 받아옴
          if x is None:       	  # 받아온 값이 None이면 total을 반환
              return total
          total += x
  
  # 합계를 출력할 코루틴
  def sum_coroutine():
      while True:
          # accumulate에 실행을 양보하고 accumulate이 실행이 종료되는 시점에 반환값을 받아온다.
          total = yield from accumulate()    
          print(total)
   
  co = sum_coroutine()
  next(co)
  
  for i in range(1, 11):
      # 코루틴 accumulate에 숫자를 보내고, total을 받아온다.
      print(co.send(i), end=" ")	# 1 3 6 10 15 21 28 36 45 55
  
  # 코루틴 accumulate에 None을 보내서 합산을 끝낸다.
  print("\n")
  co.send(None)	# 55
  ```
  
  - 실행 순서
  
    > https://pythontutor.com/live.html#mode=edit 참고
  
    - 메인 루틴에서 `sum_coroutine` 코루틴을 생성하고 `next()` 를 통해 코루틴을 실행한다.
    - `total = yield from accumulate()`가 실행되면서 `accumulate` 코루틴이 생성되고 실행된다.
    - `accumulate` 코루틴에서 `x = (yield total) `가 실행되면서 다시 `sum_coroutine`로 실행이 돌아오고 `total = yield from accumulate()`의 실행이 완료되면서 메인 루틴으로 돌아온다.
    - 메인 루틴의 for문으로 진입하고  `print(co.send(i), end=" ")`가 실행되면서 다시 `sum_coroutine` 코루틴으로 실행이 넘어간다.
    - `sum_coroutine`은 `total = yield from accumulate()`부터 실행을 다시 시작하고, 동시에 `accumulate`로 실행을 넘긴다.
    - `accumulate`는 `x = (yield total)`부터 실행을 다시 시작하고 `x`가 None이 아니므로 `total`에 `x`를 더하고 다음 반복으로 넘어간다.
    - 다음 반복에서 `x = (yield total)`를 실행하면서 실행을 다시 `sum_coroutine`의 `total = yield from accumulate()`에 넘긴다.
    - `sum_coroutine`은 `total = yield from accumulate()`의 실행이 완료되면서 다시 메인루틴에 실행을 넘기고 `accumulate`->`sum_coroutine`을 거쳐 받아온 `total`을 출력하고 다음 반복으로 넘어간다.
    - 이 과정을 10번 반복한다.
    - 메인 루틴의 for문이 종료되고 `co.send(None)`가 실행되면서 루틴은 다시 `sum_coroutine`->`accumulate` 순서로 넘어가게 되고  `x`가 None이므로 `return total`이 실행된다.
    - `accumulate`루틴이 완전히 종료되었으므로 루틴이 `sum_coroutine`로 넘어오게 되고 `print("Hello!")`가 출력되면서 다음 반복으로 넘어간다.
    - 다음 `total = yield from accumulate()`이 실행되면서 `accumulate` 코루틴이 다시 생성된다.
  
  - 주의
    - 위 예시 코드에서 `sum_coroutine` 코루틴 내부의 while문은 실제로는 2 번밖에 실행되지 않는다.
    - `accumulate` 코루틴의 실행이 종료되기 전(return을 만나던가 스크립트가 끝나기 전)까지는 `total = yield from accumulate()`가 계속 실행되고 있으며 지속적으로 `accumulate` 코루틴에 실행을 넘겨주기만 한다.
    - 그러다 x 값으로 None이 넘어오고, `accumulate` 코루틴의 실행이 종료되고 나서야 비로소 첫 반복이 종료되는 것이다.



- `StopIteration` 예외 발생시키기

  - 코루틴도 제네레이터이므로 return을 사용하면 `StopIteration`이 발생한다.
    - 따라서 코루틴에서 `return 값`은 `raise StopIteration(값)`과 동일하게 사용할 수 있다(Python 3.6 이하에서만 해당).
    - Python 3.7부터는 제네레이터 안에서 raise로 `StopIteration`를 발생시키면  RuntimeError로 바뀌므로 이 방법은 사용할 수 없다.

  - return 대신 사용하기(Python 3.6 이하)
    - 위 코드와 동일하게 동작한다.

  ```python
  # 합계를 계산할 코루틴
  def accumulate():
      total = 0
      while True:
          x = (yield total)
          if x is None:
              raise StopIteration(total)
          total += x
  
  # 합계를 출력할 코루틴
  def sum_coroutine():
      while True:
          total = yield from accumulate()    
          print(total)
   
  co = sum_coroutine()
  next(co)
   
  for i in range(1, 11):
      print(co.send(i), end=" ")
  
  co.send(None)	# 55
  ```



- 코루틴 사용 예시

  > https://github.com/fluentpython/example-code/blob/master/16-coroutine/taxi_sim.py

  - 코루틴이 반복적으로 핵심 루프에 제어권을 넘겨 주어 핵심 루프가 다른 코루틴을 활성화하고 실행할 수 있게 해줌으로써 작업을 동시에 실행한다.
  
  ```python
  import random
  import collections
  import queue
  import argparse
  
  
  DEFAULT_NUMBER_OF_TAXIS = 3
  DEFAULT_END_TIME = 180
  SEARCH_DURATION = 5
  TRIP_DURATION = 20
  DEPARTURE_INTERAVAL = 5
  
  
  # time은 event가 발생했을 때의 시간을 의미하고, proc은 taxi process instance의 번호를 의미하며, action은 활동 내용을 의미한다.
  Event = collections.namedtuple('Event','time proc action')
  
  # 각 텍시마다 한 번씩 호출되어 택시의 행동을 나타내는 제너레이터 객체를 생성한다.
  def taxi_process(ident, trips, start_time=0):
      '''
      :param ident: taxi number
      :param trips: the number of trips before the taxi goes home
      :param start_time: Time to leave the garage
      :return: 
      '''
      # 각 상태 변화마다 이벤트를 발생키는 시뮬레이터에 양보한다.
      time = yield Event(start_time, ident,'leave garage')
      for _ in range(trips):
          time = yield Event(time, ident,'pick up passenger')
          time = yield Event(time, ident,'drop off passenger')
      yield Event(time, ident,'going home')
      # 코루틴이 끝 까지 실행되면 제너레이터 객체가 StopIteration 예외를 발생시킨다.
  
  
  def compute_duration(previous_action):
      # 지수분포를 이용하여 행동 기간을 계산한다.
      if previous_action in ['leave garage','drop off passenger']:
          # 손님 없이 배회하는 상태가 된다.
          interval = SEARCH_DURATION
      elif previous_action =='pick up passenger':
          # 손님을 태우고 운행하는 상태가 된다.
          interval = TRIP_DURATION
      elif previous_action =='going home':
          interval = 1
      else:
          raise ValueError('Unkonw previous_action: %s'% previous_action)
      return int(random.expovariate(1/interval)) + 1
  
  
  # Start simulation
  class Simulator:
  
      def __init__(self, procs_map):
          # 이벤트를 시간 순으로 정렬해서 보관 할 변수
          self.events = queue.PriorityQueue()
          # taxis 딕셔너리의 사본, 시뮬레이션이 실행되면 집으로 돌아가는 택시들이 self.procs에서는 제거되지만,
          # 클라이언트가 전달한 객체를 변경하면 안되기 때문에 사본을 사용한다.
          self.procs = dict(procs_map)
  
      def run(self, end_time):
          '''
          Schedule and display events until the end of the time
          :param end_time: only one parameter needs to be specified for the end time
          :return:
          '''
          # 각 taxi의 첫 번째 event를 events에 추가한다.
          for _, proc in sorted(self.procs.items()):
              # 코루틴을 기동한다.
              first_event = next(proc)
              # 기동시에 생성된 이벤트(leave garage)를 우선순위큐에 추가한다.
              self.events.put(first_event)
  
          sim_time = 0
          # 시뮬레이션 핵심 루프
          while sim_time < end_time:
              if self.events.empty():
                  print('*** end of event ***')
                  break
              # 우선순위 큐에서 time 값이 가장 작은 이벤트를 가져와서 current_event에 저장한다.
              current_event = self.events.get()
              sim_time, proc_id, previous_action = current_event
              print('taxi:', proc_id, proc_id * ' ', current_event)
              # 활성화된 택시에 대한 코루틴을 가져온다.
              active_proc = self.procs[proc_id]
              next_time = sim_time + compute_duration(previous_action)
              try:
                  # 택시 코루틴에 시각을 전송한다.
                  # 코루틴은 다음 이벤트를 반환하거나 StopIteration 예외를 발생시킨다.
                  next_event = active_proc.send(next_time)
              except StopIteration:
                  # StopIteration 예외가 발생하면, self.procs 딕셔너리에서 해당 코루틴을 제거한다.
                  del self.procs[proc_id]
              else:
                  # 예외가 발생하지 않으면 다음 이벤트를 우선순위 큐에 넣는다.
                  self.events.put(next_event)
          else:
              msg ='*** end of simulation time: {} event pendding ***'
              print(msg.format(self.events.qsize()))
  
  
  def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
           seed=None):
      # 난수 생성을 초기화, 프로세스 생성, 시뮬레이션 실행
      if seed is not None:
          random.seed(seed) # 다시 생성할 수 있는 결과를 가져온다.
      
      # 제너레이터를 value로 갖는 dict
      taxis = {i: taxi_process(i, (i + 1) * 2, i*DEPARTURE_INTERAVAL)
               for i in range(num_taxis)}
      sim = Simulator(taxis)
      sim.run(end_time)
  
  
  if __name__ =='__main__':
      parser = argparse.ArgumentParser(description='Taxi fleet simulator.')
      parser.add_argument('-e','--end-time', type=int,
                          default=DEFAULT_END_TIME,
                          help='simulation end time; default=%s'% DEFAULT_END_TIME)
      parser.add_argument('-t','--taxis', type=int,
                          default=DEFAULT_NUMBER_OF_TAXIS,
                          help='number of taxis running; default = %s'% DEFAULT_NUMBER_OF_TAXIS)
      parser.add_argument('-s','--seed', type=int, default=None,
                          help='random generator seed (for testing)')
  
      args = parser.parse_args()
      main(args.end_time, args.taxis, args.seed)




- Generator based coroutine
  - 위와 같이 generator를 통해 만든 coroutine을 generator base coroutine이라 부른다.
  - `async`, `await`가 공식 문법으로 채택된 python 3.7 부터는 굳이 사용하지 않는 방식이다.
  - Python 3.10에서 삭제되었다.



# async / await

> https://it-eldorado.tistory.com/159

- 비동기처리

  - 동기 처리와 비동기 처리

    - 동기 처리는 task를 순차적으로 처리하는 것을 의미한다.
    - 하나의 task를 완료 해야 다음 task로 넘어간다.
    - 비동기 처리는 task를 동시에 처리하는 것을 의미한다.
    - 하나의 task가 진행되는 와중에도 다른 task가 생기면 해당 task를 함께 처리한다.

  - 멀티 스레드와 비동기 처리

    - 멀티 스레드는 실제로 둘 이상의 스레드를 생성하여 task를 처리하는 것이다.
    - 예컨데 전화 받기와 메일 쓰기를 해야 한다면 사람을 한 명 더 불러서 한 명은 전화를 받고, 한 명은 메일을 쓰는 것이다.

    - 비동기처리는 단일 스레드가 여러 개의 task를 처리하는 것이다.
    - 예컨데 위와 동일한 상황에서 한 사람이 전화를 받으면서 메일을 작성하는 것이라고 할 수 있다.

  - 왜 비동기 처리를 해야 하는가

    - 전통적으로 동시 프로그래밍은 멀티 스레드를 활용하여 이루어졌다.
    - 그러나 thread safe한 프로그램을 작성하는 것은 쉬운 일이 아니며, 하드웨어의 사양에 따라 성능 차이가 심하게 날 수 있다.
    - 이러한 이유로 최근에는 하나의 스레드로 동시 처리가 가능한 비동기 처리가 주목받고 있다.
    - 더구나 Python은 GIL로 인해 multi thread의 효용이 떨어지므로 더구나 비동기 처리가 중요하다.



- Python과 async
  - `async`
    - 비동기적으로 동작하는 함수를 만들 수 있게 해주는 Python keyword.
    - 코루틴(제너레이터)를 보다 쉽게 작성할 수 있도록 해주는 일종의 문법적 설탕이다.
    - Python 3.4에서 asyncio라는 비동기 처리를 위한 라이브러리가 표준 라이브러리로 채택되었다.
    - Python 3.5에서 async/await가 문법으로 채택되었다.
  - 코루틴과 async
    - `async` 키워드를 사용하여 비동기처리를 하는 함수를 코루틴이라 부른다.
    - Python에는 제네레이터 기반의 코루틴이 있으므로 async 기반의 코루틴과 구분하기 위해 async 기반의 코루틴을 네이티브 코루틴이라 부른다.



- `async`

  - `async` keyword를 붙여서 선언한 함수를 코루틴 함수라고 한다.
    - `async`를 붙여서 선언한 함수는 호출시에 실행되지 않고, 코루틴 객체를 반환한다.
    - 아래 함수는 corotine 객체를 반환 받고, `await`로 실행시키지 않았으므로 warning이 발생하지만, 코루틴 함수의 반환 type이 `coroutine`이라는 것은 확인할 수 있다.
  
  ```python
  import asyncio
  
  
  async def async_func():
      return "Hello World!"
  
  
  if __name__ == "__main__":
      coro = async_func()
      print(type(coro))	# <class 'coroutine'>
  ```

  - 코루틴 객체를 실행하려면 Eventloop에 코루틴 객체를 등록하고, Eventloop가 해당 객체를 실행할 수 있도록 Eventloop에 제어권을 넘겨줘야한다.
    - Python 3.7 이상에서는 `run` 메서드를 활용하여 훨씬 간편하게 호출이 가능하다.
    - 이벤트 루프(런 루프)는 무한 루프를 돌며 매 iteration마다 등록된 event들을 하나씩 실행시키는 로직을 의미한다.
    - 스레드당 실행 중인 Eventloop는 하나뿐이어야한다.
  
  ```python
  import asyncio
  
  async def async_func():
      print("Hello")
  
      
  # Python 3.7 전까지는 아래와 같이 실행해야 했다.
  # 이벤트 루프를 가져온다.
  loop = asyncio.get_event_loop()
  # 코루틴 객체가 실행이 완료될 때 까지 기다린다.
  loop.run_until_complete(async_func())
  # 이벤트 루프를 닫는다.
  loop.close()
  
  # Python 3.7 이후
  asyncio.run(async_func())
  print("World!")
  ```



- `await`

  - `yield from`을 보다 쉽게 작성해 줄 수 있도록 하는 문법적 설탕이다.
    - Python 3.5부터 사용 가능하다.
    - 이전 버전에서는 `yield from` 뒤에 generator를 두는 방식으로 사용했다면, `await` 키워드는 뒤에 코루틴 객체(뿐 아니라 `__await__` 메서드가 구현된 awaitable한 객체)를 두는 방식으로 사용한다.
  - `async`로 생성한 코루틴 함수 내에서만 사용이 가능하다.
  
  ```python
  import asyncio
   
  async def add(a, b):
      return a + b
   
  async def print_add(a, b):
      result = await add(a, b)
      print(result)	# 3
   
  asyncio.run(print_add(1, 2))
  ```
  
  - `await`는 두 가지 동작을 한다.
    - `await` 뒤에 있는 awaitable 객체를 Eventloop에 등록한다.
    - 제어권을 Eventloop에게 넘기고, 등록한 awaitable 객체의 실행이 종료되면 제어권을 받아온다. 



- 동기처리와 비동기처리 예시

  - 동기 처리

  ```python
  import time
  
  def count_number_sync(n):
      for i in range(1, n+1):
          print(i, '/', n)
          time.sleep(0.5)
  
  start = time.time()
  count_number_sync(5)
  count_number_sync(5)
  print('time:', time.time()-start)	# time: 5.006292104721069
  ```
  
  - 비동기처리
  
  ```python
  import time
  import asyncio
  
  async def count_number_async(n):
      for i in range(1, n+1):
          print(i, '/', n)
          await asyncio.sleep(0.5)
  
  async def process_async():
      start = time.time()
      await asyncio.wait([
          asyncio.create_task(count_number_async(5)),
          asyncio.create_task(count_number_async(5))
      ])
      print(time.time() - start)	# 2.5044925212860107
  
  asyncio.run(process_async())
  ```



- `Future`

  > https://tech.buzzvil.com/blog/asyncio-no-2-future/
  >
  > https://docs.python.org/3.10/library/asyncio-future.html#asyncio.Future

  - `asyncio.Future`

    - 어떤 작업의 실행 상태 및 결과를 저장하는 class.
    - 실행 상태는 `PENDING`, `CANCELLED`, `FINISHED` 중 한 가지 값을 가진다.
    - 아직은 완료되지 않았지만, 언제가 완료될 작업의 결과를 저장하는 데 사용한다.
    - 단순히 어떠한 실행 상태 및 결과를 저장할 뿐, 작업의 실행을 개시하는 역할은 수행하지 않는다.
    - 일반적으로 application level의 code에서 `Future`의 인스턴스를 생성할 일은 없다.

  - Futrue는 Python에 국한된 개념이 아니라 비동기 프로그래밍에서 널리 사용되는 개념이다.

    - 주로 비동기 연산의 결과를 저장하는 객체이다.
    - 비동기 함수의 경우 호출하는 곳에서 반환 값을 바로 받아볼 수 없다.
    - 따라서 일단은 Future 객체를 반환하고, 비동기 함수의 호출이 완료되면 반환했던 Future 객체에 결과를 저장하는 방식으로 사용된다.

  - `asyncio.Future`의 특징 및 기능

    - Awaitable이므로 `await` keyword를 사용할 수 있다.
    - `done()`으로 연산이 끝났는지 확인할 수 있다.
    - `set_result()`로 연산의 결과를 지정할 수 있다.
    - `cancel()`로 연산을 취소할 수 있다.
    - `add_done_callback()`으로 call back 함수를 등록할 수 있다.

  - `asyncio.Future`를 사용하여 유사 Semaphore 구현
  - `asyncio.Future`를 사용하면 busy wating 방식을 사용하지 않고도 polling이 가능한 Semaphore를 구현할 수 있다.
    
  - `asyncio.Future` 객체 생성시에 `asyncio.Future()`와 같이 객체를 직접 생성하는 방식보다, 아래의 `loop.create_future()`와 같이 생성하는 것이 권장된다.
  
  ```python
  from datetime import datetime
  from collections import deque
  import asyncio
  
  
  class FutureSemaphore:
      def __init__(self, initial_value: int = 1) -> None:
          self._value = initial_value
          self._waiters = deque()
  
      async def acquire(self) -> None:
          if self._value <= 0:
              loop = asyncio.get_running_loop()
              # Future 객체를 생성한다.
              future = loop.create_future()
              self._waiters.append(future)
              # release가 호출 되어 future가 끝날 때 까지 대기한다.
              await future
  
          self._value -= 1
  
      def release(self) -> None:
          self._value += 1
          if len(self._waiters) > 0:
              fut = self._waiters.popleft()
              # future에 값을 추가하고 Future를 끝낸다.
              fut.set_result(None)
  
  async def run_job(semaphore, job_id):
      await semaphore.acquire()
      print(f'{datetime.now()} - start job {job_id}')
      await asyncio.sleep(1)
      print(f'{datetime.now()} - job {job_id} finished')
      semaphore.release()
  
  
  async def main() -> None:
      semaphore = FutureSemaphore()
      await asyncio.gather(
        run_job(semaphore, 1),
        run_job(semaphore, 2),
        run_job(semaphore, 3),
        run_job(semaphore, 4),
        run_job(semaphore, 5),
      )
      
  if __name__ == "__main__":
      asyncio.run(main())
  ```



- Task
  - `asyncio.Task`

    - `coroutine` 객체를 감싸고 있는 wrapper class이다.
    - `asyncio.Future` class를 상속 받는다.
    - `asyncio.Future`와 마찬가지로 어떠한 작업의 실행 상태 및 결과를 저장하지만, `Task` class는 작업의 실행을 개시하는 역할도 수행한다.
    - `Task` 객체는 생성시에 코루틴 객체를 받아 `_coro`라는 attiribute로 저장한다.
    - Eventloop 내에서 적절한 때가 왔을 때 coroutine이 실행될 수 있도록 일정을 조율한다.
  - `Task` 객체의 동작 방식

    - `Task`객체는 생성되는 즉시 현재 스레드에 설정되어 있는 Eventloop에게 자신의 `__step()` 메서드를 호출해줄 것을 예약한다.
    - `__step()` 메서드는 `Task` 객체에 저장된 코루틴 객체를 사용하여 해당 코루틴을 실행시키는 메서드이다.
    - Eventloop는 적절한 때가 되면  `__step()` 메서드를 호출하고, 코루틴이 실행된다.

    - 코루틴이 실행되다가 `await` keyword를 만나게 되면 또 다른 코루틴을 실행시키게 되고, 그 코루틴 안에서 또 다른 코루틴을 실행시키면서 코루틴 체인이 형성될 수 있다.

    - 코루틴이 실행되다가 I/O 관련 코루틴을 만나게 되면, 자신의 실행을 중단하고 이후의 실행을 예약한 뒤 Eventloop에 제어권을 넘긴다.
    - 제어권을 넘겨 받은 Eventloop는 예약된 코루틴 중 우선 순위가 높은 것을 선택하여 이를 실행시킨다.
    - 이전에 실행이 중단되었던 코루틴이 다시 실행할 수 있는 상태가 되면, 다시 실행된다.
    - `Task` 객체가 처음 실행한 코루틴의 실행이 완료되면, 코루틴 객체로부터 반환 값을 받아 자기 자신의 결과 값을 업데이트한다.



- Eventloop의 동작 과정

  - Python 3.7 전까지는 아래와 같이 코루틴을 실행했다.
    - 3.7 이후부터는 `asyncio.run()`만으로 간단하게 실행할 수 있지만, 아래 코드가 동작 과정을 더 잘 보여주므로, 아래 코드를 가지고 설명한다.

  ```python
  import asyncio
  
  loop = asyncio.get_event_loop()
  loop.run_until_complete(first_coroutine())
  loop.close()
  ```
  
  - `get_event_loop()`
    - 현재 스레드에 설정된 Eventloop를 반환하는 함수로, 만약 설정된 Eventloop가 없다면, 새로 생성하여 이 스레드에 설정한 뒤 반환한다.
  - `run_until_complete(coroutine)`
    - 앞에서 반환 받은 Eventloop를 실행시키는 메서드이다.
    - 인자로 넘어오는 코루틴 객체를 이용하여 `Task`의 instance를 생성하고, 그 과정에서 해당 `Task ` 객체가 나타내는 task의 실행이 Eventloop에 의해 즉시 예약된다(정확히는 `Task` 객체의 `__step()` 메서드를 callback 함수로 넘긴다).
    - 적절한 때가 오면 Eventloop는 해당 `Task` 객체의 `__step()` 메서드를 호출한다. 
    - `__step()`메서드는 `Task` 객체의 `_coro` attribute에 저장된 `coroutine` 객체의 `send()` 메서드를 호출하여 코루틴을 실행한다.
    - 코루틴이 실행되면서 `await` keyword를 마주칠 때 마다 연쇄적으로 코루틴을 호출하며 코루틴 체인을 형성하게 된다.
    - 코루틴 실행 중에 Sleep 혹은 I/O 관련 코루틴을 `await`하는 코드를 만나게 되는데, 이러한 종류의 코루틴들은 `Future` 객체를 `await`하도록 구현되어 있다.
    - 이 `Future` 객체는 코루틴 체인을 따라 `yield`되면서  `Task` 객체의 `__step()` 메소드에 까지 전달되게 되고, 전달된 `Future`객체는 `Task`객체의 `__fut_waiter` attribute에 저장된다.
    - 만약 sleep과 관련된 코루틴일 경우 `Future`객체를 생성한뒤 Eventloop에게 Eventloop 자체의 타이머를 이용하여 지정된 sleep 시간 이후에 해당 `Future` 객체의 결과 값을 업데이트하도록 요청한고, 해당 `Future` 객체를 await한는데, 이는 마찬가지로 코루틴 체인을 따라 `Task` 객체의 `__step()`메서드까지 전달된다.
    - 그 후 `Future` 객체의 `add_done_callback()` 메서드를 호출하는데, 이 메서드는 해당 `Future` 객체가 완료됐을 때, Eventloop에 callback 함수의 실행을 예약하도록 해준다.
    - `add_done_callback()` 메서드가 호출된다고 Eventloop에 즉시 callback 함수의 호출이 예약되는 것이 아니라, `Future` 객체가 완료됐을 때, Eventloop에 callback 함수의 호출을 예약하는 것으로, 예약의 예약이라고 볼 수 있다.
    - 이 때 등록하는 callback 함수는 `Future` 객체 자신의 `__step()` 메서드이다.
    - 여기까지 마치고 나면 `Task` 객체는 자신의 실행을 중단하고 제어를 Eventloop에게 넘긴다.
    - 제어권을 받은 Eventloop는 실행이 예약된 task들 중(callback 함수들 중) 우선 순위가 높은 것을 선택하여 실행한다.
    -  더 이상 실행이 예약된 task가 없어지면, Eventloop는 Future 객체의 결과 값을 업데이트하고, 이로 인해 `add_done_callback()` 메서드를 통해 예약해 둔대로 Eventloop에 callback 함수(`__step()`)의 실행이 예약되게 된다.
    - `__step()` 메서드를 통해 task가 다시 실행되면, Future 객체와의 바인딩을 해제하고, `send()` 메서드를 호출하여 해당 코루틴의 실행을 재개하게 되고, 다시 코루틴 체인을 따라 올라가 다시 실행이 재개된다.
    - 결국 task가 실행한 최초의 코루틴이 `return`에 도달하는 순간이 오게 되고, 해당 `Task` 객체의 `__step()` 메서드에서 `StopIteration` 예외가 발생하게 된다.
    - `Task` 객체는 해당 예외 객체의 `value` attribute 값으로 자신의 결과 값을 업데이트 하고, 자신의 실행을 종료한다.
  - `loop.close()`
    - Eventloop를 닫는 메서드이다.
    - Eventloop에 남아 있는 모든 데이터들을 제거한다.



- `asyncio.create_task()`

  - 코루틴을 실행시키는 방법은 대표적으로 세 가지가 있다.
    - `await` keyword 사용
    - `asyncio.run()`
    - `asyncio.create_task()`
    - 이 중 `await` keyword는 코루틴 내에서만 사용 할 수 있다는 제약이 있으므로 `asyncio.run()`과 `asyncio.create_task()`만이 코루틴 체인을 실행시킬 수 있는 entrypoint이다.
  - `asyncio.run()`은 하나의 task만 실행할 수 있다.
    - 코루틴 체인에서 추가적인 task를 생성하여 실행하지 않는다면, `asyncio.run()`으로 실행시킨 task가 종료되면, Eventloop는 실행시킬 다른 task가 없는 상태가 된다.
    - 즉,  task를 하나밖에 실행시킬 수 밖에 없는 `asycio.run()`의 특성상, 동시적인 실행이라고 볼 수 없다.
  - 여러 task의 동시적인 실행을 위해서는 `asyncio.create_task()` 메서드를 사용해야한다.
    - `create_task()` 메서드는 `coroutine` 객체를 인자로 받아 이를 이용하여 `Task` 객체를 생성하고 반한환다.
    - 이 때 해당 task의 실행이 Eventloop에 예약된다.




- `asyncio.gather()`

  - `Future` 객체(`Task` 객체 포함)들이 완료 상태가 될 때까지 기다리는 함수이다.
    - 인자로 여러 개의 awaitable 객체를 받을 수 있으며, `coroutine` 객체를 받을 경우 자동으로 `Task` 객체로 warpping도 시켜준다.
    - 인자로 받은 모든 awaitable 객체들이 완료되면 그것들의 결과 값들을 list 형태로 반환한다.

  - 예시

  ```python
  import asyncio
  import time
  
  
  async def foo(sec):
      await asyncio.sleep(sec)
      return sec
  
  async def main():
      task1 = asyncio.create_task(foo(1))							# 2
      task2 = asyncio.create_task(foo(2))
      tasks_results = await asyncio.gather(task1, task2)			# 3
      return tasks_results
  
  
  if __name__ == "__main__":
      st = time.time()
      result = asyncio.run(main())								# 1
      print('result : {}'.format(result))
      print('total time : {0:.2f} sec'.format(time.time() - st))
  ```

  - 위 코드의 실행 과정은 아래와 같다.
    - 1번에 의해 Task 0가 생성되고, 실행이 Eventloop에 예약된다.
    - Eventloop에 기존에 예약되어 있던 task가 없으므로, 새로 예약된 task가 바로 실행되어 `main()` 코루틴이 실행된다.
    - 2번에 의해서 Task1과 Task2가 생성되고, 실행이 Eventloop에 예약된다.
    - 3번에서 `asyncio.gather()` 메서드가 실행되면서 Task0가 Task 1이 완료될 때까지 제어권을 Eventloop에게 넘기고 대기한다.
    - Eventloop가 Task1을 실행한다.
    - Task1은 `foo()` 코루틴을 실행하고, `foo()` 코루틴 내에서 다시 `asyncio.sleep()` 코루틴이 실행된다.
    - `asyncio.sleep()` 코루틴은 Future 1 객체를 만들고, 1초 뒤에 Future 1객체의 결과 값이 갱신되도록 Eventloop에 예약을 건 뒤 Future 1객체를 await한다.
    - Task1은 Future 1객체가 완료 상태가 될 때까지 대기하고 Eventloop에게 제어권을 넘긴다.
    - Eventloop는 Task 2를 실행한다.
    - Task1과 동일한 과정을 거쳐 Future 2 객체를 만들고, 2초 뒤에 Future 2 객체의 결과값이 갱신되도록 Eventloop에 예약을 건 뒤 Futrue 2 객체를 await한다.
    - Task2는 Future 2객체가 완료 상태가 될 때까지 대기하고 Eventloop에게 제어권을 넘긴다.
    - Eventloop는 제어권을 받았으나 실행할 task가 없으므로 대기한다.
    - Future 1 객체가 값의 갱신을 예약한지 1초가 지나면 Future 1객체의 결과값을 갱신하고, Task 1의 실행이 다시 예약된다.
    - Eventloop가 Task1 을 다시 실행한다.
    - `asyncio.sleep()` 코루틴으로 돌아가 실행을 재개한다.
    - `asyncio.sleep()` 코루틴이 반환되고 `foo()`도 1을 반환하면서 종료된다.
    - Task1 객체의 결과 값이 1로 설정되면서 Task 1의 실행이 완료된다.
    - Task 1 객체가 완료 될 때까지 기다리던 Task 0의 실행이 예약된다.
    - Eventloop가 Task 0을 실행한다.
    - `asyncio.gather()`로 돌아가 실행이 중단되었던 부분부터 실행이 재개된다.
    - `asyncio.gather()` 코루틴은 Task 1 객체의 결과 값을 저장하고, Task2 객체를 await한다.
    - Task 0는 Task 2객체가 완료 상태가 될 때까지 기다리고, Eventloop에게 제어권을 넘긴다.
    - Eventloop는 실행할 task가 없으므로 대기한다.
    - Future 2 객체가 값의 갱신을 예약한지 2초가 지나면 Future 2객체의 결과값을 갱신하고, Task 2의 실행이 다시 예약된다.
    - Eventloop가 Task2를 다시 실행하고, 이후 과정은 Task1과 같다.
    - Task 2 객체가 완료 상태가 될 때 까지 기다리던 Task0의 실행이 다시 예약된다.
    - Eventloop가 Task0을 실행한다.
    - `asyncio.gather()`로 돌아가 실행이 중단되었던 부분부터 실행이 재개된다.
    - `asyncio.gather()` 코루틴은 Task1의 결과값과 Task2의 결과값을 반환한다.
    - `main()` 코루틴도 결과값을 반환한다.
    - Task 0 객체의 결과값이 [1,2]로 설정되면서 Task 0의 실행이 완료된다.








# 예외처리

- 예외처리
  - 프로그래밍을 하다 보면 수 없이 많은 오류와 마주하게 된다.
  - 오류가 발생하면 오류가 발생한 줄 아래로는 실행이 되지 않는데 때로는 오류가 발생하더라도 실행해야 할 때가 있다.
  - 그럴 때 사용하기 위한 것이 예외처리 기법이다.



- `try`, `except` 문

  - 기본 구조
    - try 블록 실행 중 오류가 발생하면 except 블록이 실행된다.
    - except문에 발생 오류를 적어놓으면 해당 오류가 발생했을 때에만 except 블록이 실행된다.

  ```python
  # 괄호 안의 내용은 모두 생략이 가능하다.
  try:
      실행할 문장
  except [발생 오류 as 오류 메세지 담을 변수]:
      실행할 문장
  ```

  - 예시

  ```python
  # arr을 설정해 준 적 없기에 아래 문장은 error을 발생시킨다.
  print(arr)
  print("에러가 발생했으므로 출력이 안됩니다.")
  """
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 6, in <module>
      print(arr)
  NameError: name 'arr' is not defined
  """
  
  # 아래와 같이 예외 처리가 가능하다.
  try:
      print(arr)
  except:
      print("에러 발생")
  print("에러가 발생했지만 실행이 됩니다.")
  """
  에러 발생
  에러가 발생했지만 실행이 됩니다.
  """
  
  # error를 특정하는 것도 가능하다.
  try:
      print(arr)
  except NameError as e:
      print("e에는 error message가 담겼습니다.")
      print(e)
  print("에러가 발생했지만 실행이 됩니다.")
  """
  e에는 error message가 담겼습니다.
  name 'arr' is not defined
  에러가 발생했지만 실행이 됩니다.
  """
  
  # error를 특정할 경우 특정하지 않은 에러가 발생하면 except로 빠지지 않는다.
  try:
      3//0
  except NameError as e:
      print("에러 종류가 다르므로 빠지지 않습니다.")
      print(e)
  """
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 2, in <module>
      3//0
  ZeroDivisionError: integer division or modulo by zero
  """
  ```

  

- `finally`

  - try문 수행 도중 예외 발생 여부와 무관하게 수행된다.
  - 보통 사용한 리소스를 close해야 할 때 사용한다.

  ```python
  try:
      3//0
  finally:
      print("ZeroDivisionError가 발생했지만 finally 블록은 실행됩니다.")
  """
  ZeroDivisionError가 발생했지만 finally 블록은 실행됩니다.
  Traceback (most recent call last):
    File "c:\Users\pract.py", line 2, in <module>
      3//0
  ZeroDivisionError: integer division or modulo by zero
  """    
  ```




- 복수의 오류 처리하기

  - except를 여러 개 사용하면 된다.
  - 가장 먼저 진입한 except문만 실행 되고 다음 try 블록의 다음 줄은 실행 되지 않는다.

  ```python
  try:
      3//0
      print(arr)
  except ZeroDivisionError as e:
      print(e)	# integer division or modulo by zero 
  except NameError as e:
      print(e)
  
  
  
  # 아래와 같이 하는 것도 가능하다.
  try:
      3//0
      print(arr)
  except (ZeroDivisionError,NameError) as e:
      print(e)	# integer division or modulo by zero
  ```



- 오류 회피하기

  - except 블록에 pass를 쓰면 에러를 그냥 지나칠 수 있다.

  ```python
  try:
      3//0
      print(arr)
  except ZeroDivisionError as e:
      pass
  print("pass 됐습니다.")
  
  # pass 됐습니다.
  ```




- 오류 강제로 발생시키기

  - `raise`를 사용한다.
  - 프로그래밍을 하다 보면 예외를 강제로 발생시켜야 할 때가 있다.
  - Dog이라는 class를 생속 받는 자식 클래스는 반드시 bark라는 메서드를 구현하도록 하고 싶은 경우 아래와 같이 할 수 있다.
    - NotImplementedError는 python 내장 에러로 꼭 구현해야 할 부분이 구현되지 않았을 경우 발생한다.

  ```python
  class Dog:
      def bark(self):
          raise NotImplementedError
          
  class Bichon(Dog):
      pass
  
  bcn = Bichon()
  bcn.bark()			# NotImplementedError
  ```

  - 다음과 같이 bark 메서드를 오버라이딩하여 생성하면 에러가 발생하지 않는다.

  ```python
  class Dog:
      def bark(self):
          raise NotImplementedError
          
  class Bichon(Dog):
      def bark(self):
          print("멍멍")
  
  bcn = Bichon()
  bcn.bark()		# 멍멍
  ```




- 예외 만들기

  - Exception을 상속받는 class 생성

  ```python
  class CustomException(Exception):
      def __init__(self):
          super().__init__('CustomException occur!')
  ```

  - 예외 발생시키기

  ```python
  from custom_exception import CustomException
  
  
  msg = "Bye"
  
  try:
      if msg=="Bye":
          raise CustomException
  except Exception as e:
      print("Exception:",e)	# Exception: CustomException occur!
  ```

  - 혹은 상속만 받고 예외를 발생시킬 때 메시지를 넣어줄 수도 있다.

  ```python
  class CustomException(Exception):
      pass
  ```

  - 예외 발생시키기

  ```python
  from custom_exception import CustomException
  
  
  msg = "Bye"
  
  try:
      if msg=="Bye":
          raise CustomException("CustomException occur!")
  except Exception as e:
      print("Exception:",e)	# Exception: CustomException occur!
  ```

  - class를 아래와 같이 작성하여 추가적인 인자를 받을 수도 있다.
    - `__str__`이 반환하는 내용이 출력되게 된다.

  ```python
  class CustomException(Exception):
      def __init__(self, code, name):
          self.code  = code
          self.name  = name
      
      def __str__(self):
          return f'{self.code}, {self.name} error occur!'
  ```

  - 예외 발생시키기
    - 또한 args를 통해 직접 작성한 예외 클래스의 인자들을 확인 가능하다.

  ```python
  from custom_exception import CustomException
  
  
  msg = "Bye"
  
  try:
      if msg=="Bye":
          raise CustomException(1, "some exception")
  except Exception as e:
      print("Exception:",e)	# Exception: 1, some exception error occur!
      print(e.args)			# (1, 'some exception')
  ```



- traceback

  - Exception을 출력하는 것으로는 traceback까지는 확인이 불가능한데, traceback 모듈을 사용하면 traceback도 확인이 가능하다.
  - `format_exc()`
    - traceback을 문자열로 변환

  ```python
  import traceback
  
  try:
      1//0
  except Exception as e:
      print(e)	# integer division or modulo by zero
      print(traceback.format_exc())
  """
  Traceback (most recent call last):
    File "test.py", line 4, in <module>
      1//0
  ZeroDivisionError: integer division or modulo by zero
  """
  ```

  - `extract_tb()`와 `sys.exc_info()`를 활용하면 최초에 Exception이 발생한 파일을 추적 가능하다.

  ```python
  # error를 발생시킬 파일
  # error_occur.py
  def print_hello():
      print(msg)
  
  
  # error가 발생한 파일을 추적하는 코드
  # test.py
  import os
  import sys
  import traceback
  
  from test2 import print_hello
  
  
  try:
      print_hello()
  except Exception as e:
      error_file_path = traceback.extract_tb(sys.exc_info()[-1])[-1].filename
      print(error_file_path)
  ```



- error가 발생한 모듈 이름을 얻는 방법

  - `traceback` 모듈의 `extract_tb()` 메서드를 사용한다.
  - my_module.py

  ```python
  def foo():
      print(1//0)
  ```

  - test.py

  ```python
  import sys
  import os
  import traceback
  
  import my_module
  
  
  try:
      module.foo()
  except Exception as e:
      print(traceback.extract_tb(sys.exc_info()[-1])[-1].filename)
  ```



- try, execpt, else

  - else는 except 절이 실행되지 않았을 경우 실행되는 절이다.

  ```python
  try:
      print("hello world")
  except:
      print("error!")
  else:
      print("no error!")	# 실행된다.
  
      
  try:
      1//0
  except:
      print("error!")
  else:	
      print("no error!")	# 실행되지 않는다.
  ```



- Python의 모든 Exception class는 `BaseException` class를 상속받은 것이다.

  - pydoc을 통해 확인이 가능하다.

  ```bash
  $ pydoc builtins
  ```

  - `BaseException` class는 `__new__`메서드(`__init__` 메서드가 아니다)의 인자로 `args`를 받는다.
    - 따라서 `BaseException`을 상속 받은 하위 class에서 `__init__` 메서드를 실행하더라도 `args`는 여전히 존재하게 된다.
    - CPython의 `BaseException` code의 일부를 Python code로 변환하면 아래와 같다.

  ```python
  class BaseException(Exception):
      def __new__(cls, *args):
          # self = self.에 object를 생성하여 할당하는 code
          self.args = args
          return self
  ```

  - `args`가 **유일하게** 사용되는 곳은 `__str__` 메서드로, `args`를 string으로 변환하여 반환하는 역할을 한다.
    - CPython의 `BaseException`내부의 `__str__` 메서드를 python code로 변환하면 아래와 같다.

  ```python
  def __str__(self):
      if len(self.args) == 0:
          return ""
      if len(self.args) == 1:
          return str(self.args[0])
      return str(self.args)
  ```

  - 확인해보기

  ```python
  try:
      raise Exception
  except Exception as e:
      print(e)	#
  try:
      raise Exception("hello")
  except Exception as e:
      print(e)	# "hello"
  try:
      raise Exception("hello", "world", 42)
  except Exception as e:
      print(e)	# ('hello', 'world', 42)
  ```



- 새로운 Exception 만들기

  - Exception을 만들어야하는 이유
    - 개발을 하다보면 Python에서 제공하는 built in exception로 처리할 수 없는 예외들이 존재한다.
    - 따라서 개발자가 이러한 예외들을 직접 만들어서 처리해줘야한다.
  - 항상 `Exception` class를 상속받아야 한다.
    - `Exception` class는 `BaseException` class를 상속 받는 class이다.

  ```python
  class MyException(Exception):
      pass
  ```

  - 반드시 어떤 예외가 발생한 것인지 정확히 할 수 있도록 정확한 메시지를 남겨야한다.

  ```python
  class MyException(Exception):
      def __init__(self, msg):
          super(MyException, self).__init__(msg)
  ```

  - 굳이 부모 class의  `__init__` 메서드를 실행해야 하는 이유는?
    - 사실 위와 같이 직접 작성한 Exception class가 인자를 하나만 받을 때는 굳이 부모 class의 `__init__` 메서드를 실행시키지 않아도 된다.
    - 부모 class의 `__init__`메서드가 실행되며, msg가 넘어가기 때문이다.
    - 그러나 아래와 같이 default msg를 설정해줘야 하거나 인자를 둘 이상 받을 때는 반드시 `__init__` 메서드를 실행해야한다.

  ```python
  # default msg를 설정하고자 하는 경우
  class MyException(Exception):
      def __init__(self, msg=None):
          if msg is None:
              msg = "Default detail message"
          super(MyException, self).__init__(msg)
          
  # 인자를 둘 이상 받아야 하는 경우
  class MyException(Exception):
      def __init__(self, foo, msg=None):
          print(foo)
          if msg is None:
              msg = "Default detail message"
          super(MyException, self).__init__(msg)
  
  # 만일 인자를 둘 이상 받을 때, 부모 class의 __init__메서드를 실행시키지 않으면, 모든 인자가 부모 class의 args인자로 넘어가게 된다.
  # 아래 예시에서 실제 exception 메시지로 사용하려 한 것은 world인데, world뿐 아니라 hello까지 부모 class의 __init__ 메서드의 args로 넘어가게 된다.
  class MyException(Exception):
      def __init__(self, foo, msg=None):
          pass
  
  try:
      raise MyException("hello", "world")
  except MyException as e:
      print(e)	# ('hello', 'world')
  ```

  - 인자로 받은 값을 활용하기
    - 인자로 받은 값을 활용하여 보다 구체적인 예외 처리가 가능하다.

  ```python
  class MyException(Exception):
      def __init__(self, msg, foo):
          self.msg = msg
          self.foo = foo
          super(MyException, self).__init__(msg)
    
  try:
  
      raise MyException("Exception!!", False)
  except Exception as e:
      if e.foo:
          do_something()
  ```

