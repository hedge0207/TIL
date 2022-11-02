# Python은 왜 느린가?

> http://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/

- Python은 동적 타이핑 언어다.

  - 동일한 결과를 얻기 위해서 더 많은 과정을 거쳐야 하기에 Python은 느릴 수 밖에 없다.
  - C와 같은 정적 타이핑 언어는 변수를 선언할 때 변수의 type을 함께 정의해주기에, 해당 변수의 type을 바로 알 수 있다.

  ```c
  int a = 1;
  int b = 2;
  int c = a + b;
  
  /*
  int 타입인 1을 a에 할당한다.
  int 타입인 2를 b에 할당한다.
  + 연산자를 통해 그 둘을 더한다.
  더한 값을 c에 할당한다.
  */
  ```

  - 반면에 Python의 경우 Python 프로그램이 실행될 때, interpreter는 코드에 정의된 변수의 type을 모르는 상태다.
    - Interpreter가 아는 것은 각 변수가 모두 Python Object라는 것이다.

  ```python
  a = 1
  b = 2
  c = a + b
  
  """
  1. 1을 a에 할당
    - a 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  2. 2를 b에 할당
    - b 변수의 PyObject_HEAD의 typecode를 int로 설정
    - b에 int type인 2를 할당
  3. 더하기
    - a의 PyObject_HEAD의 typecode 찾기
    - a는 interger이며, a의 val은 1이라는 것을 인지
    - b의 PyObject_HEAD의 typecode 찾기
    - b는 interger이며, b의 val은 2라는 것을 인지
    - a와 b를 더한다.
  4. 결과 값을 c에 할당
    - c 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  """
  ```



- Python은 컴파일 언어 보다는 인터프리터 언어에 가깝다.
  - 좋은 컴파일러는 반복되거나 불필요한 연산을 미리 찾아내어 속도를 높일 수 있다.
  - 그러나 인터프리터 언어에 가까운 Python은 위 방식이 불가능하다.



- Python의 object model은 비효율적인 메모리 접근을 유발할 수 있다.

  - 많은 언어들은 원시 자료형을 지원한다.
    - 원시 자료형은 어떤 데이터의 참조를 담고 있는 자료형이 아닌 값 그 자체를 담을 수 있는 자료형이다.
    - 그러나 python에는 원시 자료형 자체가 존재하지 않는다.
  - Python의 모든 것은 객체이다.
    - Python의 모든 변수들은 data 자체를 저장하고 있는 것이 아니라 data를 가리키는 pointer를 저장하고 있다.

  - 예시

    - 다른 언어들에서 일반적으로 원시 자료형이라 불리는 integer 등도 하나의 객체이다.

    - C에서 `int a = 1`의 a는 숫자 1 자체를 저장하고 있지만, Python에서  `a = 1`의 a는 숫자 1을 가리키는 pointer를 저장하고 있는 것이다.





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





# Multi processing

- Python에서의 multi processing
  - Python은 GIL로 인해 thread 기반의 병렬 처리가 까다롭다.
  - 따라서 multi-thread 방식 보다는 multi-processing 방식으로 병렬 처리를 해야한다.
  - Python 내장 패키지 중 multiprocessing을 사용하면 간단하게 구현이 가능하다.



- Process 생성하기

  - Process를 생성하는 것을 spawning이라 한다.
  - `Process` class의 인스턴스를 생성하는 방식으로 process를 생성할 수 있다.
    - `Process`의 인스턴스를 생성할 때는 첫 번째 인자로 실행 시킬 함수를, 두 번째 인자로 해당 함수에 넘길 인자를 입력한다.
  - `start()`메서드를 사용하여 spawn된 process를 실행시킬 수 있다.

  ```python
  from multiprocessing import Process
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      p = Process(target=f, args=('bob',))
  ```



- multiprocessing은 platform(OS)에 따라 세 가지 다른 방식의 Process 실행 방식을 지원한다.

  - spawn
    - 자식 process는 부모 process로부터 `run()` 메서드를 실행시키는 데 필요한 자원만을 상속 받는다.
    - 불필요한 file descriptor와 handle은 상속받지 않는다.
    - fork나 forkserver에 비해 느리다.
    - Unix와 Windows에서 사용 가능하며, Windows와 macOS의 기본값이다.
  - fork
    - 부모 process는 `os.fork()`메서드를 사용하여 Python interpreter를 fork한다.
    - 자식 process는 부모 process로부터 모든 자원을 상속받는다.
    - 자식 process는 부모 process와 사실상 동일한 상태로 시작된다.
    - Unix에서만 사용 가능하며, Unix의 기본 값이다.
  - forkserver
    - 프로그램이 실행되고, forkserver start method를 선택하면, server process가 시작된다.
    - 이후 새로운 프로세스가 필요할 때마다 부모 프로세스는 server에 새로운 process를 fork하도록 요청한다.
    - 불필요한 자원은 상속되지 않는다.
    - Unix pipe를 통한 file descriptor를 지원하는 Unix에서만 사용 가능하다.
  - multiprocessing의 `set_start_method`를 통해 어떤 method로 실행시킬지 지정이 가능하다.

  ```python
  from multiprocessing import Process
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      multiprocessing.set_start_method('spawn')
      p = Process(target=f, args=('bob',))
  ```

  - 혹은 아래와 같이 `get_context()`메서드를 사용하는 방법도 있다.

  ```python
  from multiprocessing
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      ctx = multiprocessing.get_context('spawn')
      p = ctx.Process(target=f, args=('bob',))
  ```



- Process 사이의 communication channel 사용하기

  - `multiprocessing`은 두 가지 communication channel을 지원한다.
  - `Queue`
    - `queue.Queue`의 clone이다.
    - thread, process safe하다.

  ```python
  from multiprocessing import Process, Queue
  
  def f(q):
      q.put([42, None, 'hello'])
  
  if __name__ == '__main__':
      q = Queue()
      p = Process(target=f, args=(q,))
      p.start()
      print(q.get())    # prints "[42, None, 'hello']"
      p.join()
  ```

  - `Pipe`
    - `Pipe()` 함수는 `Pipe`로 연결된 한 쌍의 connection object를 반환한다.
    - 반환된 connection object들은 `send()`와 `recv()` 메서드를 가진다.

  ```python
  from multiprocessing import Process, Pipe
  
  def f(conn):
      conn.send([42, None, 'hello'])
      conn.close()
  
  if __name__ == '__main__':
      parent_conn, child_conn = Pipe()
      p = Process(target=f, args=(child_conn,))
      p.start()
      print(parent_conn.recv())   # prints "[42, None, 'hello']"
      p.join()
  ```



- Process 사이의 동기화

  - `multiprocessing`은 `threading`의 동기화 관련 요소들을 모두 포함하고 있다.
  - 예시
    - Lock을 사용하여 한 번에 하나의 proecess에서만 print를 출력하도록 하는 예시이다.

  ```python
  from multiprocessing import Process, Lock
  
  def f(l, i):
      l.acquire()
      try:
          print('hello world', i)
      finally:
          l.release()
  
  if __name__ == '__main__':
      lock = Lock()
  
      for num in range(10):
          Process(target=f, args=(lock, num)).start()
  ```



- Process간의 상태 공유

  - 동시성 프로그래밍을 할 때에는 왠만하면 상태의 공유를 피하는 것이 좋다.
    - 특히 multi process를 사용할 때는 더욱 그렇다.
  - 그럼에도 `multiprocessing`에서는 상태 공유를 위한 몇 가지 방법을 제공한다.
  - Shared memory
    - `Value`와 `Array`를 사용하여 data를 shared memory map에 저장할 수 있다.
    - `'d'`와 `'i'`는 typecode를 나타낸다. `d`는 double precision float type을 나타내고, `i`는 signed integer를 나타낸다. 

  ```python
  from multiprocessing import Process, Value, Array
  
  def f(n, a):
      n.value = 3.1415927
      for i in range(len(a)):
          a[i] = -a[i]
  
  if __name__ == '__main__':
      num = Value('d', 0.0)
      arr = Array('i', range(10))
  
      p = Process(target=f, args=(num, arr))
      p.start()
      p.join()
  
      print(num.value)
      print(arr[:])
  ```

  - Server process
    - `Manager()`가 반환한 manager 객체는 Python 객체를 가지고 있는 server process를 통제하고, 다른 process들이 proxy를 사용하여 이를 조정할 수 있도록 해주는 역할을 한다.
    - `Manager()`가 반환한 manager는 list, dict, Namespace, Lock, RLock, Semaphore, Boundedsemaphore, Condition, Event, Barrier, Queue, Value, Array type을 지원한다.

  ```python
  from multiprocessing import Process, Manager
  
  def f(d, l):
      d[1] = '1'
      d['2'] = 2
      d[0.25] = None
      l.reverse()
  
  if __name__ == '__main__':
      with Manager() as manager:
          d = manager.dict()
          l = manager.list(range(10))
  
          p = Process(target=f, args=(d, l))
          p.start()
          p.join()
  
          print(d)
          print(l)
  ```



- Pool 사용하기

  - `Pool` class는 worker process들의 pool을 생성한다.
  - `Pool` class는 task들을 process로 넘길 수 있는 몇 가지 method를 제공한다.
    - `apply()`: process에게 특정 작업을 실행시키고 해당 작업의 종료까지 기다린다.
    - `apply_async()`: process에게 특정 작업을 시키고 종료는 기다리지 않고 `AsyncResult`를 반환 받는다.  작업이 완료되었을 때 `AsyncResult`의  `get()` 메서드를 통해 작업의 반환값을 얻을 수 있다.
    - `map()`: process에게 iterable한 작업을 실행시킨다. 단, 사용하고자 하는 함수는 단일 인자를 받아야 한다. ` apply()`와 마찬가지로 작업의 종료까지 기다린다.
    - `async_map()`: process에게 iterable한 작업을 실행시킨다. 단, 사용하고자 하는 함수는 단일 인자를 받아야 한다. `apply_async()`와 마찬가지로 종료는 기다리지 않고 `AsyncResult`를 반환 받는다.
  - 예시

  ```python
  from multiprocessing import Pool, TimeoutError
  import time
  import os
  
  def f(x):
      return x*x
  
  if __name__ == '__main__':
      # 4개의 worker process를 시작한다.
      with Pool(processes=4) as pool:
  
          print(pool.map(f, range(10)))
  
          for i in pool.imap_unordered(f, range(10)):
              print(i)
  
          # evaluate "f(20)" asynchronously
          res = pool.apply_async(f, (20,))      # runs in *only* one process
          print(res.get(timeout=1))             # prints "400"
  
          # evaluate "os.getpid()" asynchronously
          res = pool.apply_async(os.getpid, ()) # runs in *only* one process
          print(res.get(timeout=1))             # prints the PID of that process
  
          # launching multiple evaluations asynchronously *may* use more processes
          multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
          print([res.get(timeout=1) for res in multiple_results])
  
          # make a single worker sleep for 10 secs
          res = pool.apply_async(time.sleep, (10,))
          try:
              print(res.get(timeout=1))
          except TimeoutError:
              print("We lacked patience and got a multiprocessing.TimeoutError")
  
          print("For the moment, the pool remains available for more work")
  
      # exiting the 'with'-block has stopped the pool
      print("Now the pool is closed and no longer available")
  ```

  - `Pool`과 `Process`의 차이
    - `Pool`은 처리할 일을 쌓아두고 process들이 알아서 분산 처리를 하게 만드는 방식이다.
    - `Process`는 각 process마다 할당량을 지정해주고 분산 처리를 하게 만드는 방식이다.



- Daemon process 생성하기

  - 특정 작업을 백그라운드에서 실행하기 위하여 daemon process를 실행할 수 있다.
    - `Process`의 인스턴스의 `daemon` 속성을 True로 주면 된다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo(num):
      time.sleep(10)
      print(os.getpid())
      print(num)
      print("-"*100)
  
  
  if __name__ == "__main__":
  
      p = Process(target=foo, args=[0])
      p.daemon = True
      p.start()
  ```

  - Daemon proecess는 main process가 종료되면 함께 종료된다.



- `join()` 메서드

  - `join()`메서드는 자식 process의 작업이 완료될 때 까지 부모 process가 기다리게 한다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      p.join()
      print("Parent process")
  ```

  - `join()`이 없을 경우

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      print("Parent process")
  ```

  - 자식 process는 join 없이 종료되고, 부모 process는 아직 실행중이라면 자식 process는 zombie process가 된다.
    - 아래 코드에서 자식 process가 join 없이 부모 프로세스보다 먼저 종료가 되는데, 이 상태에서 자식 프로세스의 pid로 process 상태를 확인해보면 `[python] <defunct>`와 같이 뜨게 된다.
    - 만일 부모 process가 종료되지 않고 계속 실행되는 코드였을 경우 자식 process는 zombie process인 상태로 계속 남아있게 되므로 반드시 join을 해줘야한다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      time.sleep(300)
      print("Parent process")
  ```

  - 명시적으로 `join()` 메서드를 호출하지 않아도, 부모 프로세스가 종료될 때가 되면 암묵적으로 `join()` 메서드가 호출된다.
    - 아래 코드를 보면 `join()`을 호출하지 않았음에도, 부모 process가 다 실행된 이후에도 종료되지 않고 자식 process의 실행이 완료되기를 기다린다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      time.sleep(20)
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.start()
      print("Parent process")
  ```

  - 단 `join()` 메서드의 암묵적인 호출은 non-daemonic process일 때 만이고 daemon process의 경우 부모 프로세스의 종료와 함께 종료된다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
      time.sleep(20)
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      print("Parent process")
  ```

  





