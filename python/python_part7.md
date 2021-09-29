

# 이터레이터와 제너레이터

## 이터레이터

- 이터레이터
  - 값을 차례대로 꺼낼 수 있는 객체를 의미한다.
    - 반복자라고도 부른다.
  - `range`는 이터레이터를 생성하는 함수로, `range(10)`은 실제로 10개의 숫자를 생성하는 것이 아니라 이터레이터를 생성하는 것이다.
    - 이터레이터만 미리 생성하고 값이 필요한 시점이 되었을 때 값을 만든다.
    - 이처럼 데이터 생성을 뒤로 만드는 방식을 **지연평가**(lazy evaluation)라 한다.
  - 시퀀스 객체와의 차이
    - 시퀀스 객체는 기본적으로 반복 가능한 객체에 포함된다.
    - 둘의 차이는 시퀀스 객체는 이터러블한 객체 중에서도 순서가 보장되는 객체이다.
  - 이터레이터와 이터러블의 차이
    - 이터러블은 반복 가능한 객체를 의미하며 `__iter__` 메서드만 가지고 있으면 이터러블이다.
    - 이터레이터는 값을 차례대로 꺼낼 수 있는 객체를 의미하며 `__iter__`메서드와 `__next__`메서드를 가지고 있으면 이터레이터이다.
    - 즉 리스트, 튜플 등의 이터러블한 객체는 그 자체로 값을 차례로 꺼낼 수 있지 않다.
    - 값을 차례로 꺼내기 위해서는 `__iter__`메서드를 통해 이터레이터를 생성한 뒤 해당 이터레이터의 `__next__`메서드를 통해 값을 차례로 꺼내는 것이다.



- 이터레이터인지 확인하기

  - 객체에 `__iter__` 메서드가 있는지 확인하면 된다.

  ```python
  my_list = [1, 2, 3]
  print(dir(my_list))	# [..., '__iter__', ...]
  ```

  - `__iter__`를 호출하면 이터레이터가 나오게 된다.

  ```python
  my_list = [1, 2, 3]
  print(my_list.__iter__())	# <list_iterator object at 0x7fcd468eb580>
  ```

  - `__next__` 메서드를 화출하여 요소를 차례로 꺼낼 수 있다.
    - 더 이상 꺼낼 요소가 없다면 `StopIteration` 예외를 발생시킨다.

  ```python
  my_list = [1, 2, 3]
  my_iter = my_list.__iter__()
  print(my_iter.__next__())	# 1
  print(my_iter.__next__())	# 2
  print(my_iter.__next__())	# 3
  print(my_iter.__next__())	# StopIteration
  ```

  - for문의 동작 방식
    - `range(3)`는 이터레이터를 생성한다.
    - `range`에서 `__iter__`를 통해 이터레이터를 얻는다.
    - 반복할 때마다 이터레이터에서 `__next__`를 통해 반복을 수행한다.
    - 더 이상 꺼낼 것이 없으면  `StopIteration` 예외가 발생하고 반복이 종료된다.
    - `range`뿐 아니라 모든 이터레이터에 적용된다.
  - `__iter__`와 `__next__`를 가진 객체를 이터레이터 프로토콜을 지원한다고 말한다.



- 이터레이터 직접 구현하기

  - `__iter__`와 `__next__`메서드를 직접 구현하여 이터레이터를 만들 수 있다.

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
  - 이터레이터를 생성해주는 함수
    - 이터레이터는 클래스에 `__iter__`와 `__next__`  또는 `__getitem__` 메서드를 구현해야 하지만 제너레이터는 함수 안에서 `yield`라는 키워드만 사용하면 된다.
    - 즉, 이터레이터를 클래스로 작성하는 것 보다 훨씬 간단하게 작성이 가능하다.
    - 발생자라고도 부른다.
  - 즉, 제너레이터 객체는 이터레이터이다.



- yield

  - 제네레이터를 만들기 위한 Python keyword
    - yield는 ''양보하다''라는 뜻도 가지고 있는데, 함수 바깥으로 전달하면서 코드 실행을 함수 바깥에 양보한다는 의미에서 yield를 키워드로 지정한 것이다.
  - 함수 안에서 yield를 사용하면 함수는 제너레이터가 되며, yield에는 값을 지정한다.
    - `number_generator` 함수를 호출하면 제터레이터 객체가 반환된다.
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

  - yield와 return
    - yield도 제너레이터 함수 끝까지 도달하면 `StopIteration`가 발생한다.
    - return도 마찬가지로 중간에 return이 될 경우 `StopIteration`가 발생한다.

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



- `yield from`으로 여러 번 바깥으로 전달하기

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
    - `yield from`에는 반복 가능한 객체,, 이터레이터, 제네레이터를 지정한다.

  ```python
  def number_generator():
      x = [1, 2, 3]
      yield from x
  
  for i in number_generator():
      print(i)
  ```

  - `yield from`에 제네레이터 객체도 지정이 가능하다.

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
  - cooperative routine의 약어로 서로 협력하는 루틴이다.
    - 메인 루틴과 서브 루틴처럼 종속된 관계가 아니라 서로 대등한 관계이며 특정 시점에 상대의 코드를 실행한다.
    - 메인루틴-서브루틴과 마찬가지로 한 루틴이 실행되는 동안 다른 루틴은 대기상태에 있게 된다.
  - 함수의 코드를 실행하는 지점을 진입점(entry point)라 하는데 코루틴은 진입점이 여러 개인 함수이다.
    - 코루틴은 함수가 종료되지 않은 상태에서 메인 루틴의 코드를 실행한 뒤 다시 돌아와 코루틴의 코드를 실행한다.
    - 따라서 코루틴이 종료되지 않으므로 코루틴의 내용도 계속 유지된다.
  - 제너레이터의 특별한 형태이다.
    - 제너레이터는 yield로 값을 발생시키지만, 코루틴은 yield로 값을 받아올 수 있다.



- 코루틴에 값 보내기

  - 코루틴에 값을 보내면서 코드를 실행할 때는 `send` 메서드를 사용하고,  `send` 메서드가 보낸 값을 받아오기 위해 `(yield)` 형식으로 yield를 괄호로 묶어준 후 변수에 저장한다.

  ```python
  def my_coroutine():
      # 코루틴을 유지하기 위해 무한 루프를 사용한다.
      while 1:
          num = (yield)	# 코루틴 바깥에서 받은 값을 받아서 사용.
          print(num)
  
  co = my_coroutine()
  # 코루틴 내부의 yield까지 함수 실행(최초)
  next(co)
  
  co.send(1)	# 코루틴에 숫자 1 보내기
  co.send(2)	# 코루틴에 숫자 2 보내기
  co.send(3)	# 코루틴에 숫자 3 보내기
  ```

  - 실행 과정
    - 메인 루틴에서 코루틴을 생성하고 `next()`를 통해 코루틴을 실행한다.
    - while문이 실행되고 `yield` 키워드를 만나면서 메인루틴에 실행을 넘겨준다.
    - `send()`를 통해 코루틴에 값을 보내고, num이 print된후 다시 반복문을 돌아 yield키워드를 만나면서 메인루틴에 실행을 넘겨준다.



- 코루틴 바깥으로 값 내보내기

  - `(yield 변수)` 형식으로 yiled에 변수를 지정한 뒤 괄호로 묶어주면 값을 받아오면서 바깥으로 값을 전달한다.
    - `yield`로 바깥으로 전달한 값은 next 함수와 send 메서드의 반환값으로 나오게 된다. 

  ```python
  def sum_coroutine():
      total = 0
      while True:
          num = (yield total)    # 코루틴 바깥에서 값을 받아오면서 바깥으로 값을 전달
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
    - send를 통해 코루틴에 값을 보내고, `total += x`이 실행된 후 다시 반복문을 돌아 yield키워드를 만나면서 메인루틴에 실행을 넘겨주고 total을 반환한다.



- 코루틴을 종료하고 예외처리하기

  - `close` 메서드를 통해 코루틴을 종료할 수 있다.
    - Python 스크립트가 끝나도 코루틴이 자동으로 종료된다.

  ```python
  def number_coroutine():
      total = 0
      while True:
          num = (yield total)
          total += num
   
  co = number_coroutine()
  next(co)
   
  for i in range(5):
      print(co.send(i), end=" ")	# 0 1 3 6 10
   
  co.close()
  ```

  - `GeneratorExit` 예외처리하기
    - 코루틴 객체에서 close 메서드를 호출하면 코루틴이 종료될 때 `GeneratorExit ` 예외가 발생한다.

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
    - `throw` 메서드를 사용한다.

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



- 하위 코루틴의 반환값 가져오기

  - 주의
    - 실제로 아래와 같이 `yield from`을 사용할 일은 거의 없다.
    - Python 3.5 이상부터는 `async`를 대신 사용한다.
  - 코루틴에서는 `yield from`을 일반적인 제네레이터와는 다르게 사용한다.
    - 제네레이터에서 `yield from`을 사용하면 값을 바깥으로 여러 번 전달하는데 사용했다.
    - `yield from`에 코루틴을 지정하면 해당 코루틴에서 return으로 반환한 값을 가져온다.
    - `yield from`은 정확히는 `yield from` 뒤에 오는 루틴이 완전히 종료될 때 까지 실행을 양보하는 것이다.
  
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
          # 이제부터 send는 sum_coroutine이 아닌 accumulate로 가게 된다.
          # accumulate 내부의 yield가 반환하는 값 역시 sum_coroutine이 아닌 메인 루틴으로 가게 된다.
          total = yield from accumulate()    
          print(total)
   
  co = sum_coroutine()
  next(co)
   
  for i in range(1, 11):
      # 코루틴 accumulate에 숫자를 보내고, total을 받아온다.
      print(co.send(i), end=" ")	# 1 3 6 10 15 21 28 36 45 55
  
  # 코루틴 accumulate에 None을 보내서 합산을 끝낸다.
  co.send(None)	# 55
  ```



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

  



# async / await

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





- Python과 async
  - async
    - 비동기적으로 동작하는 함수를 만들 수 있게 해주는 Python keyword
    - Python 3.4에서 asyncio라는 비동기 처리를 위한 라이브러리가 표준 라이브러리로 채택되었다.
    - Python 3.5에서 async/await가 문법으로 채택되었다.
  - 코루틴과 async
    - async 키워드를 사용하여 비동기처리를 하는 함수를 코루틴이라 부른다.
    - Python에는 제네레이터 기반의 코루틴이 있으므로 async 기반의 코루틴과 구분하기 위해 async로 기반의 코루틴을 네이티브 코루틴이라 부른다.



- async 사용해보기

  - 아래와 같이 네이티브 코루틴을 비동기 함수가 아닌 곳에서 호출하면 Warning 메세지가 출력되고 실행도 되지 않는다.
    - 네이티브 코루틴이 실행되지 않는 것이지 error가 발생하진 않으므로 이후의 코드가 실행은 된다.

  ```python
  async def async_func():
      print("Hello")
  
  async_func()
  print("World!")
  '''
  test.py:4: RuntimeWarning: coroutine 'async_func' was never awaited
    async_func()
  RuntimeWarning: Enable tracemalloc to get the object allocation traceback
  World!
  '''
  ```

  - 따라서  asyncio 모듈을 사용해 실행해야 한다.
    - Python 3.7 이상에서는 `run` 메서드를 활용하여 훨씬 간편하게 호출이 가능하다.

  ```python
  import asyncio
  
  async def async_func():
      print("Hello")
  
  # 이벤트 루프를 가져온다.
  loop = asyncio.get_event_loop()
  # 비동기 함수가 종료할 때 까지 기다린다.
  loop.run_until_complete(async_func())
  # 이벤트 루프를 닫는다.
  loop.close()
  
  # Python 3.7+
  asyncio.run(async_func())
  print("World!")
  ```



- `await`

  - Python 3.5부터 사용 가능
    - 이전 버전에서는 `yield from`으로 대체한다.
  - async로 생성한 비동기 함수 내에서만 사용이 가능하다.
  - await가 붙은 부분은 동기적으로 처리된다.

  ```python
  import asyncio
   
  async def add(a, b):
      return a + b
   
  async def print_add(a, b):
      result = await add(a, b)
      print(result)	# 3
   
  asyncio.run(print_add(1, 2))
  ```



- 동기처리와 비동기처리 예시

  - 동기 처리

  ```python
  from os import stat_result
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
  
  async def count_number_sync(n):
      for i in range(1, n+1):
          print(i, '/', n)
          await asyncio.sleep(0.5)
  
  async def process_async():
      start = time.time()
      await asyncio.wait([
          count_number_sync(5),
          count_number_sync(5)
      ])
      print(time.time() - start)	# 2.5044925212860107
  
  asyncio.run(process_async())
  ```

  



