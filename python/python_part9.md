

# GIL

- GIL(Global Interpreter Lock)

  > https://xo.dev/python-gil/
  >
  > https://dgkim5360.tistory.com/entry/understanding-the-global-interpreter-lock-of-cpython

  - CPython에서 여러 thread를 사용할 경우, 단 하나의 thread만이 Python object에 접근할 수 있도록 제한하는 mutex이다.
    - mutex: mutal exclusion(상호 배제)의 줄임말로, 공유 불가능한 자원의 동시 사용을 피하는 기법이다.
    - Python은 thread-safe하지 않기에 GIL이라는 mutex로 lock을 걸어놓은 것이다.
    - 즉, Python에서는 둘 이상의 thread가 동시에 실행될 수 없다.
    - 둘 이상의 thread가 동시에 실행되는 것 처럼 보인다면 각 thread가 빠른 속도로 번갈아가며 실행되고 있는 것이다.
  - Python은 thread-safe하지 않다.
    - thtead-safeness란 thread들이 race condition을 발생시키지 않으면서 각자의 일을 수행한다는 뜻이다.
    - race condition이란 하나의 값에 여러 스레드가 동시에 접근하여 값이 올바르지 않게 읽히거나 쓰이는 문제를 의미한다.
    - 예를 들어 아래 코드의 결과 x는 0이 될 것 같지만 그렇지 않다(0이 나올 수도 있지만, 여러 번 수행해보면 0이 아닌 값들도 나온다).
    - 이는 x라는 값에 2개의 스레스가 동시에 접근하여 race condition가 발생했기 때문이다.
    - GIL이 걸려 있어도 아래와 같이 race condition이 발생하게 된다.

  ```python
  import threading 
  
  x = 0
  
  def foo(): 
      global x 
      for i in range(100000): 
          x += 1
  
  def bar(): 
      global x 
      for i in range(100000): 
          x -= 1
  
  t1 = threading.Thread(target=foo) 
  t2 = threading.Thread(target=bar) 
  t1.start() 
  t2.start() 
  t1.join() 
  t2.join()
  
  print(x)
  ```

  - Python의 GC 방식
    - Python에서 모든 것은 객체다.
    - 모든 객체는 해당 객체를 가리키는 참조가 몇 개 존재하는지를 나타내는 참조 횟수(reference count) 필드를 지니고 있다.
    - 참조 될 때마다 1씩 증가하며, 0이 될 경우 GC에 의해 메모리에서 삭제된다.
    - `sys` 모듈의 `getrefcount` 메서드로 확인 가능하다.

  ```python
  import sys
  
  
  foo = []
  bar = foo
  print(sys.getrefcount(foo))		# 3(foo가 선언될 때 1번, bar에 할당될 때 1번, getrefcount 함수에 매개변수로 넘어가면서 1번)
  ```

  - 왜 Python은 thread-safe하지 않은가?
    - 참조 횟수를 기반으로 GC가 이루어지는 Python의 특성상 여러 스레드가 하나의 객체를 참조할 경우 참조 횟수가 제대로 count되지 않을 수 있다.
    - 따라서 삭제되어선 안 되는 객체가 삭제될 수도 있고, 삭제되어야 할 객체가 삭제되지 않을 수도 있다.
    - 만일 GC가 정상적으로 이루어지게 하려면 모든 개별 객체에 mutex가 필요하게 된다.
    - 그러나 모든 객체에 mutex를 사용할 경우 성능상의 손해뿐 아니라, deadlock이 발생할 수도 있다.
    - 따라서 CPython은 개별 객체를 보호하는 것이 아니라 Python interpreter 자체를 잠궈 오직 한 thread만이 Python code를 실행시킬 수 있게 했다.
  - 예시
    - 만약 화장실에 변기가 1칸 밖에 없다고 생각해보자.
    - 변기는 공유가 불가능한 자원으로, 여러 명이 동시에 사용할 수는 없다.
    - 따라서 사람들은 화장실에 들어가 화장실 문(mutex)를 닫고, 자기가 사용할 동안 다른 사람이 사용하지 못하도록 잠궈놓는다(lock).
    - 다른 사람들(theads)는 문이 잠겨 있는 동안은 화장실을 이용하지 못한다.
  - GIL이 영향을 미치는 범위
    - CPU bound는 GIL의 영향을 받고, I/O bound는 GIL의 영향을 받지 않는다는 설명들이 있는데 이는 잘못된 것이다.
    - GIL의 영향을 받는지 여부는 Python runtime과 상호작용을 하는가에 달려있다. 즉 python runtime과 상호작용을 하면 GIL의 영향을 받고, 반대일 경우 아니다.
    - CPU bound란 CPU 성능에 영향을 받는 작업으로, 일반적으로 연산을 수행하거나 image processing과 같이 수학적 계산을 많이 하는 작업들이 이에 속한다.
    - I/O bound란 대부분의 시간을 input/output을 기다리는데 사용하는 작업을 뜻하며, filesystem에 접근하거나 network 통신을 하는 작업들이 이에 속한다.
    - 보통 하나의 프로그램은 CPU bound와 I/O bound 작업들이 함께 섞여 있다.
    - 일반적으로 I/O bound의 작업들은 Python runtime과 상호작용을 하지 않으므로 GIL의 영향을 덜 받는다.
  - CPU bound 예시
    - multi thread를 사용했을 때 오히려 속도가 더 느려진다.
    - GIL로 인해 single thread로 동작할 뿐 아니라, lock을 걸고 해제하는 과정을 반복하면서 overhead가 발생하기 때문이다.
  
  ```python
  import time
  from threading import Thread
  
  
  N = 10000000
  
  def countdown(n):
      while n>0:
          n -= 1
  
  # single thread
  start = time.time()
  countdown(N)
  print(time.time()-start)	# 0.459784...
          
  
  # multi thread
  t1 = Thread(target=countdown, args=(N//2,))
  t2 = Thread(target=countdown, args=(N//2,))
  
  start = time.time()
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print(time.time()-start)	# 0.852366...
  ```
  
    - I/O bound 예시
      - multi thread가 single thread에 비해 훨씬 빠르다.
  
  ```python
  import time
  from threading import Thread
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("127.0.0.1:9200")
  
  N = 1000
  
  def send_reqeusts(n):
      for _ in range(n):
          es_client.cat.indices()
  
  # single thread
  start = time.time()
  send_reqeusts(N)
  print(time.time()-start)	# 10.40409...
         
  
  # multi thread
  t1 = Thread(target=send_reqeusts, args=(N//2,))
  t2 = Thread(target=send_reqeusts, args=(N//2,))
  
  start = time.time()
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print(time.time()-start)	# 5.85471...
  ```



  - Python에서 multi thread 자체가 불가능한 것은 아니다.
    - 여러 개의 thread를 실행시키는 것 자체는 가능하다.
    - 단지, 여러 개의 스레드가 병렬적으로 실행되는 것이 막혀있는 것이다.
    - 즉 동시성에는 열려있지만 병렬성에는 닫혀있다고 볼 수 있다.
    - 그러나 Python에서 multi thread는 성능상의 이점이 거의 존재하지 않기에(lock을 걸고(aquire) lock을 풀 때(release) overhead가 발생) multi process를 사용하거나 비동기 코드를 작성하는 것이 낫다.
    - 단, 위에서 봤듯 Python runtime과 상호작용하지 않는 작업들은 multi thread로 구현했을 때 성능상의 이득이 있을 수 있다.



- 의문들

    - 왜 다른 언어에는 GIL이 존재하지 않는가?
      - 다른 언어는 Python처럼 refcnt로 GC를 실행하지 않기 때문이다.

    - 왜 이렇게 설계 했으며, 왜 바꾸지 않는가?
      - Python이 공개됐던 1991년만 하더라도 하드웨어적인 한계로 인해 multi thread는 크게 고려할 사항이 아니었다.
      - 이전에 몇 번 GIL을 없애려는 시도가 있었으나 모두 실패로 돌아갔다.
      - 귀도 반 로섬은 GIL을 없앨 경우 기존에 개발된 라이브러리들과 제품들의 코드를 모두 수정해야 하므로 없애기 쉽지 않다고 밝혔고, 실제로 이전에 있었던 몇 번의 시도들도 위와 같은 이유 때문에 실패했다.
      - 그러나 없애고 싶지 않은 것은 아니며, 부작용을 최소화하면서 없앨 방법을 찾는 중이다.



  - race condition을 막는 방법

    - 방법1
      - 하나의 스레드가 작업을 종료하고 다른 스레드가 작업을 시작하도록 한다.

    ```python
    from threading import Thread
    
    x = 0
    N = 1000000
    mutex = Lock()
    
    def add():
    	global x
    	for i in range(N):
    		x += 1
    	
    def subtract():
    	global x
    	for i in range(N):
    		x -= 1
    	
    
    add_thread = Thread(target=add)
    subtract_thread = Thread(target=subtract)
    
    # 스레드가 시작하고
    add_thread.start()
    # 끝날때 까지 대기한다.
    add_thread.join()
    
    subtract_thread.start()
    subtract_thread.join()
    
    print(x)
    ```

      - 방법2. mutex를 설정한다.
        - 스레드에서 공유 객체에 접근하는 부분(임계영역)을 지정하고 lock을 설정한다.

    ```python
    from threading import Thread, Lock
    
    x = 0
    N = 1000000
    mutex = Lock()
    
    def add():
    	global x
        # lock을 걸고
    	mutex.acquire()
    	for i in range(N):
    		x += 1
        # 작업이 완료되면 lock을 푼다.
    	mutex.release()
    
    def subtract():
    	global x
    	mutex.acquire()
    	for i in range(N):
    		x -= 1
    	mutex.release()
    
    
    add_thread = Thread(target=add)
    subtract_thread = Thread(target=subtract)
    
    add_thread.start()
    subtract_thread.start()
    
    add_thread.join()
    subtract_thread.join()
    
    print(x)
    ```



