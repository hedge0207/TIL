# locust

- locust
  - performance testing tool
  - open source로 개발되었다.
  - 이름이 locust인 이유는 메뚜기 떼가 농장을 습격하듯 사용자들이 웹 사이트를 습격한다고 하여 붙인 이름이다.



- 특징
  - Python code로 test scenario 작성이 가능하다.
  - 많은 수의 유저가 동시에 사용하는 상황을 테스트 가능하다.
    - 이벤트 기반(gevnet 사용)으로 수천명의 동시 사용자를 테스트 가능하다.
  - Web 기반의 UI를 제공한다.
  - 어떤 시스템이든 테스트가 가능하다.
  - 가볍고 변경에 유연하다.



- 단점
  - 하드웨어 모니터링 기능이 없다.



- 설치

  - pip로 설치한다.

  ```bash
  $ pip install locust
  ```

  - 설치 확인

  ```bash
  $ locust -V
  ```



- locust 실행하기

  - fastapi로 아래와 같은 간단한 API를 만든다.

  ```python
  import uvicorn
  from fastapi import FastAPI
  
  app = FastAPI()
  
  
  @app.get("/hello")
  async def hello_world():
      return "Hello!"
  
  @app.get("/world")
  async def hello_world():
      return "World!"
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8000)
  ```

  - locust로 테스트 시나리오를 작성한다.
    - 테스트 시나리오의 파일 이름은 `locustfile.py`여야한다.
    - 아래 시나리오는 사용자가 `/hello`와 `/world`라는 api에 http requests를 반복적으로 보내는 시나리오이다.

  ```python
  from locust import HttpUser, task
  
  
  class HelloWorldUser(HttpUser):
      @task
      def hello_world(self):
          self.client.get("/hello")
          self.client.get("/world")
  ```

  - 실행하기

  ```bash
  $ locust
  ```

  - `http://localhost:8098`로 접속하면 아래와 같은 화면을 볼 수 있다.
    - Numver of users: 동시에 접속하는 최대 사용자 수를 설정한다.
    - Spwan rate: 시작할 때 몇 명의 사용자로 시작할지, 초당 몇 명씩 사용자를 늘릴지 설정한다.
    - Host: 테스트하려는 API의 주소를 입력한다.

  ![locust_main](locust.assets/locust_main.png)

  - Command line으로 바로 시작하기
    - Web UI는 부가적인 기능으로 꼭 사용해야하는 것은 아니다.
    - 아래와 같이 command line을 통해서도 실행이 가능하다.

  ```bash
  $ locust --headless --users <최대 사용자 수> --spawn-rate <초당 늘어날 사용자 수> -H <테스트하려는 API 주소>
  ```



- locust의 기본적인 동작 과정은 다음과 같다.	
  - 설정한 사용자 수 만큼 User class의 instance를 생성한다.
  - user instance는 각자의 green thread 안에서 동작을 시작한다.
  - 각 user instance는 task를 선택하고, task를 실행한다.
  - 그 후 설정된 시간 만큼 대기한다.
  - 대기 시간이 끝나면 다시 다음 task를 선택하고, 실행한다.





## locustfile 작성하기

### User class

- locustfile은 적어도 하나의 사용자 클래스가 있어야 한다.
  - 사용자 클래스인지는 `HttpUser` class를 상속 받은 클래스인가로 판단한다.



- 시뮬레이팅할 사용자 생성하기

  - class 형식으로 시뮬레이팅할 사용자를 생성한다.

  ```python
  from locust import HttpUser
  
  class QuickstartUser(HttpUser):
      pass
  ```

  - 테스트가 시작되면 locust는 사용자 클래스의 instance를 생성한다.



### HttpUser

- 사용자 클래스는 `HttpUser` class를 상속받는다.
  - 이를 통해 `HttpUser`의 attribute인 `client`에 접근할 수 있게 된다.
  - `client`는 `HttpSession`의 instance로, load test 대상 시스템에 HTTP 요청을 보내는 데 사용된다.
    - `HttpSession`은 `requests` 모듈의 `Session`를 상속받는다.



- validating response

  - 기본적으로 response code가 OK면 request가 성공한 것으로 간주한다.
  - 이를 custom할 수 있다.
    - `catch_response`를 True로 준다.

  ```python
  with self.client.get("/", catch_response=True) as response:
      if response.text != "Success":
          response.failure("Got wrong response")
      elif response.elapsed.total_seconds() > 0.5:
          response.failure("Request took too long")
  ```

  - 아래와 같이 400 이상의 status code가 반환되었을 때에도 성공으로 간주하게 할 수 있다.

  ```python
  with self.client.get("/does_not_exist/", catch_response=True) as response:
      if response.status_code == 404:
          response.success()
  ```



- JSON 형식으로 request보내고 응답 받아오기

  ```python
  from json import JSONDecodeError
  ...
  with self.client.post("/", json={"foo": 42, "bar": None}, catch_response=True) as response:
      try:
          if response.json()["greeting"] != "hello":
              response.failure("Did not get expected value in greeting")
      except JSONDecodeError:
          response.failure("Response could not be decoded as JSON")
      except KeyError:
          response.failure("Response did not contain expected key 'greeting'")
  ```



- Grouping requests

  - query parameter를 받는 경우 qeury parameter가 변경될 때마다 각기 다른 endpoint로 요청을 보내는 것으로 간주된다.
    - 즉 아래 예시와 같은 요청은 10개의 endpoint에 대한 요청을 1번씩 보내는 것으로 간주된다.
    - 이럴 경우 나중에 결과를 통계내기 어려워질 수 있으므로 그룹화 해야한다.

  ```python
  for i in range(10):
      self.client.get("/blog?id=%i" % i, name="/blog?id=[id]")
  ```

  - 그룹화하기

  ```python
  # /blog?id=[id] 라는 이름으로 그룹화된다.
  self.client.request_name="/blog?id=[id]"
  for i in range(10):
      self.client.get("/blog?id=%i" % i)
  self.client.request_name=None
  ```

  - boilerplate를 최소화하기 위해 아래와 같이 작성하는 것도 가능하다.

  ```python
  @task
  def multiple_groupings_example(self):
      # Statistics for these requests will be grouped under: /blog/?id=[id]
      with self.client.rename_request("/blog?id=[id]"):
          for i in range(10):
              self.client.get("/blog?id=%i" % i)
  
      # Statistics for these requests will be grouped under: /article/?id=[id]
      with self.client.rename_request("/article?id=[id]"):
          for i in range(10):
              self.client.get("/article?id=%i" % i)
  ```




### 옵션들

- `wait_time`

  - 각 task들의 실행 간격을 설정한다.

    - 주의할 점은 `wait_time`은 하나의 task가 끝나고 난 후부터 시간을 계산한다는 점이다.
    - task안에 몇 개의 request가 있든 하나의 task가 끝아야 시간을 계산하기 시작한다.
    - 따라서 RPS가 1인 상황을 테스트하려고 시간 간격을 1로 줬어도, task 안에 request가 3개라면, RPS는 3이 된다.

  - `constant(wait_time)`

    - 설정한 시간(초) 만큼의 간격을 두고 다음 task를 실행시킨다.

  - `between(min_wait, max_wait)`

    - 최솟값 이상, 최댓값 이하의 값들 중 랜덤한 시간(초)만큼의 간격을 두고 다음 task를 실행시킨다.

  - `constant_throughput(task_runs_per_second)`

    - 시간이 아닌 테스크가 초당 실행될 횟수를 받는다(reqeust per second가 아닌 task per second임에 주의).
    - 테스크가 초당 최대 설정한 값만큼 실행되는 것을 보장한다.

    - 예를 들어 초당 500번의 task를 실행시키고자 하고, 사용자 수가 5000명이라면, 인자로 0.1을 넘기면 된다.
    - 5000명이 초당 0.1번, 즉 10초에 1번씩 task를 실행하므로 초당 500번의 task가 실행된다.
    - 유념해야 할 점은 테스크의 실행 간격을 조정하여 RPS에 맞추는 것이지, 사용자의 수를 조정하는 것은 아니라는 점이다.
    - 따라서 위 예시에서 task의 실행 시간이 10초를 넘어간다면 RPS는 500보다 낮아지게 된다.

  ```python
  # 초당 500번의 task를 실행시키고자 하고 사용자 수가 5000이라고 가정할 때, task는 10초에 한 번씩 수행된다.
  # 그런데 아래 예시와 같이 task가 한 번 수행되는데 소요되는 시간이 10초를 넘어가면 RPS는 500보다 낮아지게 된다.
  class MyUser(User):
      wait_time = constant_throughput(0.1)
      
      @task
      def my_task(self):
          # 11초 동안 실행된다.
          time.sleep(11)
  ```

  - `constant_pacing(wait_time)`
    - 설정한 시간 동안 task가 최대 1번만 실행되는 것을 보장한다.
    - 아래 코드에서 task는 10초에 1번만 실행된다.
    - `constant_throughput`와 수학적으로 반대 개념이다.

  ```python
  class MyUser(User):
      wait_time = constant_pacing(10)
      @task
      def my_task(self):
          pass
  ```

  - custom
    - `wait_time`이라는 메서드를 생성하여 custom이 가능하다.

  ```python
  class MyUser(User):
      last_wait_time = 0
  
      def wait_time(self):
          self.last_wait_time += 1
          return self.last_wait_time
  ```



- 사용자 수 설정하기

  - User class가 둘 이상이라면, locust는 기본적으로 동일한 수의 사용자를 각 user class에서 생성한다.
  - `weight` 
    - 특정 유저가 더 많이 생성되도록 할 수 있다.
    - `WebUser`가 `MobileUser`에 비해 생성될 가능성이 3배 더 높다.

  ```python
  class WebUser(User):
      weight = 3
  
  class MobileUser(User):
      weight = 1
  ```

  - `fixed_count`
    - 각 user class별로 몇 명의 사용자를 생성할지 지정할 수 있다.
    - `weight`를 무시하고 무조건 설정된 수 만큼의 사용자를 먼저 생성한다.
    - 아래 예시에서 `AdminUser`의 instance는 전체 유저수와 무관하게 1명이 생성된다.

  ```python
  class AdminUser(User):
      wait_time = constant(600)
      fixed_count = 1
  
      @task
      def restart_app(self):
          pass
  
  class WebUser(User):
      pass
  ```



- etc

  - host를 미리 지정할 수 있다.

  ```python
  class QuickstartUser(HttpUser):
      host = "http://localhost:8002"
  ```

  - 사용자가 테스트를 시작할 때와 종료할 때 수행할 메서드를 설정 가능하다.
    - `on_start`, `on_stop` 메서드를 선언한다.
    - `on_start`는 사용자가 TaskSet을 실행하기 시작 했을 때, `on_stop`은  `interrupt()`가 호출되거나 해당 사용자가 kill 됐을 때 실행된다.

  ```python
  class QuickstartUser(HttpUser):
      def on_start(self):
          self.client.post("/login", json={"username":"foo", "password":"bar"})
      
      def on_stop(self):
          print("QuickstartUser stop test")
  ```





## Task

- task 생성하기

  - 사용자가 어떤 동작을 할 것인지를 정의한 시나리오이다.
  - User class의 method로 선언한다.
    - `@task` decorator를 붙여야한다.
    - 테스트가 시작되면 `QuickstartUser`의 instance들이 생성되고 각 instance들은 `foo`를 실행한다.

  ```python
  from locust import HttpUser, task
  
  
  class QuickstartUser(HttpUser):
      @task
      def foo(self):
          self.client.get("/foo")
  ```

  - 복수의 task를 설정하는 것도 가능하며, 각 task별로 가중치를 주는 것이 가능하다.
    - 복수의 task가 선언되었을 경우 task들 중 하나가 무선적으로 선택 되고 실행된다.
    - 가중치는 `@task` decorator 뒤에 `(number)` 형식으로 주면 된다.
    - 아래 예시의 경우 `bar` task가 `foo` task에 비해 선택(되어 실행)될 확률이 3배 높다.

  ```python
  class QuickstartUser(HttpUser):
      @task
      def foo(self):
          self.client.get("/foo")
      
      @task(3)
      def bar(self):
          self.client.get("/bar")
  ```




- Task를 user class의 method가 아닌 일반 함수로 선언하는 것도 가능하다.

  - 일반 함수로 선언 후 user class의 `tasks` attribute에 할당한다.
    - user를 인자로 받는다.
    - `tasks` attribute는 callable이나 TaskSet class를 list 형태, 혹은 dict 형태로 받는다.

  ```python
  from locust import User
  
  def my_task(user):
      pass
  
  class MyUser(User):
      tasks = [my_task]
  ```

  - 가중치 설정하기
    - dict 형태로 선언한다.
    - key에 task를, value에 가중치를 넣는다.

  ```python
  from locust import User
  
  def my_task(user):
      pass
  
  def another_task(user):
      pass
  
  class MyUser(User):
      # another_task에 비해 my_task가 3배 더 실행될 확률이 높다.
      tasks = {my_task:3, another_task:1}
  ```



- Tag 설정하기

  - `@tag` decorator를 통해 tag 설정이 가능하다.
    - 테스트 실행시에 `--tags` 혹은 `--exclude-tags` 옵션으로 어떤 tag가 붙어있는 task를 수행할지, 혹은 수행하지 않을지 지정 가능하다.
    - 예를 들어 `locust --tags tag1`은 task1과 task2만 실행한다.

  ```python
  from locust import User, constant, task, tag
  
  class MyUser(User):
      wait_time = constant(1)
  
      @tag('tag1')
      @task
      def task1(self):
          pass
  
      @tag('tag1', 'tag2')
      @task
      def task2(self):
          pass
  
      @tag('tag3')
      @task
      def task3(self):
          pass
  
      @task
      def task4(self):
          pass
  ```





## Event

- test시작, 종료시에 실행될 코드 작성하기

  - `@events.test_start.add_listener`, `@events.test_stop.add_listener` decorator를 사용한다.

  ```python
  from locust import events
  
  # test_start라는 event에 대한 listener를 추가한다.
  @events.test_start.add_listener
  def on_test_start(environment, **kwargs):
      print("A new test is starting")
  
  # test_stop이라는 event에 대한 listener를 추가한다. 
  @events.test_stop.add_listener
  def on_test_stop(environment, **kwargs):
      print("A new test is ending")
  ```



- `init` event

  - 각 locust process가 시작될 때 trigger 된다.
  - 분산 모드에서 각 locust process가 initialization이 필요할 때 유용하다.

  ```python
  from locust import events
  from locust.runners import MasterRunner
  
  @events.init.add_listener
  def on_locust_init(environment, **kwargs):
      if isinstance(environment.runner, MasterRunner):
          print("I'm on master node")
      else:
          print("I'm on a worker or standalone node")
  ```



- 더 상세한 event hook은 아래 링크 참고

  - https://docs.locust.io/en/stable/api.html#event-hooks

  - command line의 option을 custom하거나 각 request event마다 특정 동작을 수행하는 것이 가능하다.







## Library로 사용하기

- `locust` command 대신 python script로 test를 실행할 수 있다.

  - 코드
    - tag 등은 Environment를 통해 넣으면 된다.
  
  
  ```python
  import gevent
  from locust import HttpUser, task, between
  from locust.env import Environment
  from locust.stats import stats_printer, stats_history
  from locust.log import setup_logging
  
  setup_logging("INFO", None)
  
  
  class User(HttpUser):
      wait_time = between(1, 3)
      host = "https://docs.locust.io"
  
      @task
      def my_task(self):
          self.client.get("/")
  
      @task
      def task_404(self):
          self.client.get("/non-existing-path")
  
  
  # Environment의 instance 생성 후 runner 생성
  env = Environment(user_classes=[User])
  env.create_local_runner()
  
  # web ui 호스트와 포트 설정
  env.create_web_ui("127.0.0.1", 8089)
  
  # 테스트 상태가 print되도록 설정
  gevent.spawn(stats_printer(env.stats))
  
  # 과거 테스트 이력을 저장하도록 설정(chart 등에 사용)
  gevent.spawn(stats_history, env.runner)
  
  # 테스트 시작
  env.runner.start(1, spawn_rate=10)
  
  # 테스트 기간 설정
  gevent.spawn_later(60, lambda: env.runner.quit())
  
  # wait for the greenlets
  env.runner.greenlet.join()
  
  # stop the web server for good measures
  env.web_ui.stop()
  
  # aggs 결과 확인
  print(self.env.stats.total)
  
  # 각 task별 결과 확인
  for task, stats in self.env.stats.entries.items():
      print(task)
      print(stats)
  ```
  



## Locust Test Non Http service

- Locust를 사용하여 대부분의 시스템을 테스트할 수 있다.
  - Locust는 기본적으로 HTTP/HTTPS test만이 내장되어 있다.
  - 그러나 RPC를 사용하면 어떤 시스템이든 테스트가 가능하다.



- gRPC를 활용하여 테스트하기

  - `.proto` 파일 작성하기

  ```protobuf
  syntax = "proto3";
  
  package locust.hello;
  
  service HelloService {
    rpc SayHello (HelloRequest) returns (HelloResponse) {}
  }
  
  message HelloRequest {
    string name = 1;
  }
  
  message HelloResponse {
    string message = 1;
  }
  ```

  - `pb2`파일 생성하기

  ```bash
  $ python -m grpc_tools.protoc -I<proto file이 있는 폴더의 경로> --python_out=<pb2 파일을 생성할 경로> --grpc_python_out=<pb2_grpc 파일을 생성할 경로> <proto file의 경로>
  ```

  - gRPC 서버 작성하기

  ```python
  import hello_pb2_grpc
  import hello_pb2
  import grpc
  from concurrent import futures
  import logging
  import time
  
  logger = logging.getLogger(__name__)
  
  
  class HelloServiceServicer(hello_pb2_grpc.HelloServiceServicer):
      def SayHello(self, request, context):
          name = request.name
          time.sleep(1)
          return hello_pb2.HelloResponse(message=f"Hello from Locust, {name}!")
  
  
  def start_server(start_message):
      server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
      hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloServiceServicer(), server)
      server.add_insecure_port("localhost:50051")
      server.start()
      logger.info(start_message)
      server.wait_for_termination()
  ```

  - gRPC 클라이언트 겸 사용자를 생성하는 로직 추가.

  ```python
  import grpc
  import hello_pb2_grpc
  import hello_pb2
  from locust import events, User, task
  from locust.exception import LocustError
  from locust.user.task import LOCUST_STATE_STOPPING
  from hello_server import start_server
  import gevent
  import time
  
  # patch grpc so that it uses gevent instead of asyncio
  import grpc.experimental.gevent as grpc_gevent
  
  grpc_gevent.init_gevent()
  
  
  @events.init.add_listener
  def run_grpc_server(environment, **_kwargs):
      # gRPC 서버 시작하기
      # 첫 번째 인자로 spawn할 함수를 받고, 두 번째 인자로 해당 함수의 파라미터를 받는다.
      gevent.spawn(start_server, "gRPC server started")
  
  
  class GrpcClient:
      def __init__(self, environment, stub):
          self.env = environment
          self._stub_class = stub.__class__
          self._stub = stub
  
      def __getattr__(self, name):
          func = self._stub_class.__getattribute__(self._stub, name)
  
          def wrapper(*args, **kwargs):
              request_meta = {
                  "request_type": "grpc",
                  "name": name,
                  "start_time": time.time(),
                  "response_length": 0,
                  "exception": None,
                  "context": None,
                  "response": None,
              }
              start_perf_counter = time.perf_counter()
              try:
                  request_meta["response"] = func(*args, **kwargs)
                  request_meta["response_length"] = len(request_meta["response"].message)
              except grpc.RpcError as e:
                  request_meta["exception"] = e
              request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
              self.env.events.request.fire(**request_meta)
              return request_meta["response"]
  
          return wrapper
  
  
  class GrpcUser(User):
      abstract = True
  
      stub_class = None
  
      def __init__(self, environment):
          super().__init__(environment)
          for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
              if attr_value is None:
                  raise LocustError(f"You must specify the {attr_name}.")
          self._channel = grpc.insecure_channel(self.host)
          self._channel_closed = False
          stub = self.stub_class(self._channel)
          self.client = GrpcClient(environment, stub)
  
  
  class HelloGrpcUser(GrpcUser):
      # grpc 서버의 host를 설정한다.
      host = "localhost:50051"
      stub_class = hello_pb2_grpc.HelloServiceStub
  
      @task
      def sayHello(self):
          if not self._channel_closed:
              self.client.SayHello(hello_pb2.HelloRequest(name="Test"))
          time.sleep(1)
  ```



## Worker

- locust는 여러 개의 worker를 생성하여 테스트가 가능하다.

  - 간단한 테스트의 경우에는 하나의 프로세스로도 충분한 throughput을 발생시킬 수 있다. 그러나 복잡한 테스트를 진행하거나, 보다 많은 load를 실행하기 위해서는 여러 프로세스를 생성해야 한다.

  - master는 locust의 web interface를 실행하고, worker들에게 언제 User를 생성하는지나 멈추는 지를 알려주는 역할을 한다.
    - master는 직접 test를 실행하지는 않는다.
  - worker는 User를 생성하고, 테스트를 진행하며, 그 결과를 master에 전송한다.
  - Python은 GIL로 인해 프로세스 당 둘 이상의 코어를 완전히 활용할 수 없다.
    - 따라서 프로세서 코어 하나 당 worker 하나를 실행해야 한다.
    - 또한 하나의 프로세스에 worker와 master를 동시에 실행해선 안 된다.



- 실행하기

  - master 모드로 실행하기

  ```bash
  $ locust --master
  ```

  - worker 실행하기
    - 만일 master와 다른 machine에서 실행한다면 `--master-host` 옵션을 통해 master machine의 host를 입력해야 한다.

  ```bash
  $ locsut --worker
  ```

  - 옵션
    - `--master-bind-host`: master 노드가 bind할 network interface의 host를 입력한다.
    - `--master-bind-port`: master 노드의 port를 설정한다.
    - `--master-host`: worker를 master와 다른 machine에 생성한 경우에 master의 host를 입력한다.
    - `--master-port`: 만일 master의 port를 설정해준 경우에 woreker를 실행할 때 master의 port를 입력한다.
    - `--expect-workers`: master node를 `--headless` 옵션과 함께 실행할 때, master node는 설정값 만큼의 노드가 실행되기를 기다렸다가 테스트를 시작한다.



- 노드 사이의 통신

  ```python
  from locust import events
  from locust.runners import MasterRunner, WorkerRunner
  
  # Fired when the worker receives a message of type 'test_users'
  def setup_test_users(environment, msg, **kwargs):
      for user in msg.data:
          print(f"User {user['name']} received")
      environment.runner.send_message('acknowledge_users', f"Thanks for the {len(msg.data)} users!")
  
  # Fired when the master receives a message of type 'acknowledge_users'
  def on_acknowledge(msg, **kwargs):
      print(msg.data)
  
  @events.init.add_listener
  def on_locust_init(environment, **_kwargs):
      if not isinstance(environment.runner, MasterRunner):
          environment.runner.register_message('test_users', setup_test_users)
      if not isinstance(environment.runner, WorkerRunner):
          environment.runner.register_message('acknowledge_users', on_acknowledge)
  
  @events.test_start.add_listener
  def on_test_start(environment, **_kwargs):
      if not isinstance(environment.runner, MasterRunner):
          users = [
              {"name": "User1"},
              {"name": "User2"},
              {"name": "User3"},
          ]
          environment.runner.send_message('test_users', users)
  ```



## Pandas

- Pandas

  - 파이썬의 데이터 분석 라이브러리로 행과 열로 이루어진 데이터 객체를 만들어 다룰 수 있게 해줘 보다 안정적으로 대용량 데이터를 처리할 수 있게 도와준다.
- Anaconda에 기본적으로 제공되지만, 아나콘다를 사용하지 않을 경우에는 설치해야 한다.
  - import해서 사용해야 한다.
    - import 할 때 파일명을 import할 module 이름과 다르게 설정해야 한다.
- numpy





## Pandas의 자료 구조

- Series

  - 1차원 자료구조로 리스트와 같은 시퀀스 데이터를 받아들이는데, 별도의 인덱스 레이블을 지정하지 않으면 자동으로 0부터 시작되는 디폴트 정수 인덱스를 사용한다.
  - 파이썬의 리스트를 기초로 만든 자료형이다.
  - 생성

  ```python
  import pandas as pd
   
  # 방법1.
  data = [1, 3, 5, 7, 9]
  s = pd.Series(data)
  print(s)
  
  #out
  0  1
  1  3
  2  5
  3  7
  4  9
  dtype:int64
      
      
  #방법2. 인덱스를 직접 설정
  s2 = pd.Series([2,4,6,8],index=['a','b','c','d'])
  print(s2)
  
  #out
  a    2
  b    4
  c    6
  d    8
  dtype: int64
      
  
  #방법3. 딕셔너리를 사용
  obj = {'a':1,'b':2,'c':3,'d':4}
  s3 = pd.Series(obj)
  print(s3)
  
  #out
  a    1
  b    2
  c    3
  d    4
  dtype: int64
  ```

  - Series의 메소드

  ```python
  #Series의 값만 확인하기
  print(s.values)
  #Series의 인덱스만 확인
  print(s.index)
  #Series의 자료형 확인
  print(s.dtype)
  
  
  #out
  [1 3 5 7 9]
  RangeIndex(start=0, stop=5, step=1)
  int64
  ```

  - Series, index의 이름을 설정하는 것도 가능하다(value에 이름 넣는 것은 불가능).

  ```python
  s2.name='이름'
  s2.index.name="인"
  print(s2)
  
  #out
  인
  a    1
  b    2
  c    3
  Name: 이름, dtype: int64
  ```

  

- DataFrame

  - Series의 결합체

  ```python
  s1 = pd.core.series.Series([1,2,3])
  s2 = pd.core.series.Series(['a','b','c'])
  
  df=pd.DataFrame(data=dict(num=s1,word=s2))
  print(df)
  
  
  #out
     num word
  0    1    a
  1    2    b
  2    3    c
  ```

  - 생성

  ```python
  #기본적인 생성 방법
  변수명 = pd.DataFrame(data=데이터로 넣을 값, index=인덱스(행)로 넣을 값, columns=열로 넣을 값)
  
  #방법1-1. python의 dictionary를 사용
  data = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
   
  df = pd.DataFrame(data)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  
  #방법1-2. 인덱스와 컬럼을 함께 설정
  data = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
  df = pd.DataFrame(data,columns=['age','name'],index=['one','two','three'])
  print(df)
  
  #out
  #아래에서 확인 가능한 것 처럼 data의 순서와 DataFrame을 정의할 때의 columns의 순서가 달라도 key값을 알아서 찾아서 정의해준다. 단, data에 포함되어 있지 않았던 값(예시의 경우 weigth)은 NaN으로 나타나게 된다.
  #단, index의 경우 data의 개수와 맞지 않으면 에러가 발생하게 된다.
         age  name weight
  one     23   Kim    NaN
  two     25   Lee    NaN
  three   27  Park    NaN
  
  
  #방법2-1. python의 list를 사용
  data = [
      ['Kim',23],
      ['Lee',25],
      ['Park',27]
  ]
  col_name=['name','age']
  df=pd.DataFrame(data,columns=col_name)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  
  #방법2-2. 위 방법을 한 번에 하는 방법
  data = [
      ['name',['Kim','Lee','Park']],
      ['age',[23,25,27]]
  ]
  df = pd.DataFrame.from_items(data)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  ```

  

  - DataFrame의 메소드

  ```python
  #행의 인덱스
  print(df.index)
  #열의 인덱스
  print(df.columns)
  #값 얻기
  print(df.values)
  
  #out
  RangeIndex(start=0, stop=3, step=1)
  Index(['name', 'age'], dtype='object')
  [['Kim' 23]
   ['Lee' 25]
   ['Park' 27]]
  
  
  #연산 메소드
  
  #sum():합계
  print(df['height'].sum())
  #mean(): 평균
  print(df['height'].mean())
  #min(): 최소
  print(df['height'].min())
  #max(): 최대
  print(df['height'].max())
  #describe():기본적인 통계치 전부
  print(df.describe())
  #head(): 처음 5개의 행 표시, 괄호 안에 숫자를 넣을 경우 해당 숫자 만큼의 행 표시
  #tail(): 마지막 5개의 행 표시, 괄호 안에 숫자를 넣을 경우 해당 숫자 만큼의 열 표시
  
  #out
  75
  25.0
  23
  27
          age
  count   3.0
  mean   25.0
  std     2.0
  min    23.0
  25%    24.0
  50%    25.0
  75%    26.0
  max    27.0
  ```

  

  - 행, 열 인덱스의 이름 설정하기

  ```python
  print('before')
  print(df)
  df.index.name='index'
  df.columns.name='info'
  print()
  print('after')
  print(df)
  
  #out
  before
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  after
  info   name  age
  index
  0       Kim   23
  1       Lee   25
  2      Park   27
  ```

  

  - data에 접근

  ```python
  #행에 접근: 행 인덱싱을 통해 접근
  print(df[0:2]) #0번째 부터 2번째 앞까지 가져온다.
  
  
  #out
  info  name  age
  index
  0      Kim   23
  1      Lee   25
  
  
  
  # 열에 접근1. 인덱싱
  print(df['age'])   
  
  # 열에 접근2. 속성
  print(df.age)      
  
  # 열에 접근3-1.filter를 사용할 수도 있다. sql문과 동일하게 like, regex 등의 문법을 사용 가능하다.
  print(df.filter(items=['age']))
  
  
  #out
  index
  0    23
  1    25
  2    27
  Name: age, dtype: int64
          
  index
  0    23
  1    25
  2    27
  Name: age, dtype: int64
  
  #위 두 방식과 결과가 다르다.
  info   age
  index
  0       23
  1       25
  2       27
  
  #열에 접근 3-2. filter의 like,regex 활용
  #axis=1은 열을 필터링 하겠다는 뜻이다. 따라서 아래 코드는 열 중에서 m이 포함된 열을 찾는 것이다.
  print(df.filter(like='m',axis=1))
  #아래 코드는 열 중에서 e로 끝나는 열을 찾는 것이다.
  print(df.filter(regex='e$',axis=1))
  
  #out
  info   name
  index
  0       Kim
  1       Lee
  2      Park
  info   name  age
  index
  0       Kim   23
  1       Lee   25
  2      Park   27
  
  
  
  #boolean indexing과 함께 사용
  print(df.loc[df['gender']=='male',['year','height']])
  
  #out
           year  height
  two    2017.0    1.73
  three  2018.0    1.83
  ```

  

  - loc과 iloc의 차이
    - 공통점: 둘 다 첫 번째 인자로 행을, 두 번째 인자로 열을 받는다.
    - 차이점: loc은 label(index명, column 명)을 통해서 값을 찾지만 iloc은 interger position을 통해서 값을 찾는다.

  ```python
  #인덱스, 컬럼이 숫자일 경우
  data = [
      ['Kim',23,71,178],
      ['Lee',25,68,175],
      ['Park',27,48,165],
      ['Choi',22,57,168],
      ['Jeong',29,77,188],
  ]
  col_name=[1,2,3,4]
  df=pd.DataFrame(data,columns=col_name)
  # print('loc output')
  # print(df.loc['one':'three','age':'weight'])
  # print()
  # print('iloc output')
  # print(df.iloc[0:3,1:3])
  
  print('loc output')
  print(df.loc[0:3,1:3])  #인덱스의 이름이 0인 것부터 3인 것 까지, 컬럼의 이름이 1인것 부터 3인것 까지
  print()
  print('iloc output')
  print(df.iloc[0:3,1:3]) #0 번째 인덱스 부터 2번째 인덱스 까지, 1번째 컬럼부터 2번째 컬럼 까지, 
  
  #out
  loc output
        1   2   3
  0   Kim  23  71
  1   Lee  25  68
  2  Park  27  48
  3  Choi  22  57
  
  iloc output
      2   3
  0  23  71
  1  25  68
  2  27  48
  
  
  
  #인덱스, 컬럼이 숫자가 아닐 경우
  data = [
      ['Kim',23,71,178],
      ['Lee',25,68,175],
      ['Park',27,48,165],
      ['Choi',22,57,168],
      ['Jeong',29,77,188],
  ]
  col_name=['name','age','weight','height']
  df=pd.DataFrame(data,columns=col_name, index = ['one','two','three','four','five'])
  
  print('loc output')
  print(df.loc['one':'three','age':'weight'])
  print()
  print('iloc output')
  print(df.iloc[0:3,1:3])
  
  #out
  loc output
         age  weight
  one     23      71
  two     25      68
  three   27      48
  
  iloc output
         age  weight
  one     23      71
  two     25      68
  three   27      48
  ```

  

  

  - boolean indexing:  특정 조건의 데이터만 필터링
    - 어떤 방식으로 접근했는 가에 따라 결과 값이 다르다.

  ```python
  #인덱스로 접근
  print(df[df['age']>=25])
  print(df[df.age>=25])
  #속성으로 접근
  print(df.age>=25)
  #sql문 사용
  print(df.query('age>=25'))
  
  #out
  #일치하는 행만 반환
  info   name  age
  index
  1       Lee   25
  2      Park   27
  info   name  age
  index
  1       Lee   25
  2      Park   27
  
  #각 행별 조건에 부합하는지 여부를 boolean 값으로 반환
  index
  0    False
  1     True
  2     True
  Name: age, dtype: bool
          
  #일치하는 행만 반환
  info   name  age
  index
  1       Lee   25
  2      Park   27
  
  
  #새로운 값도 대입 가능, 새로운 값을 추가하는 것은 불가능
  df.loc[df['age']>25,'name']='Jeong'
  print(df)
  
  info    name  age
  index
  0        Kim   23
  1        Lee   25
  2      Jeong   27
  ```

  

  - 열 추가

  ```python
  df['gender']='male'
  print(df)
  
  df['gender']=['male','female','male']
  print(df)
  
  
  #out
  info   name  age gender
  index
  0       Kim   23   male
  1       Lee   25   male
  2      Park   27   male
  info   name  age  gender
  index
  0       Kim   23    male
  1       Lee   25  female
  2      Park   27    male
  
  
  #Series를 추가할 수도 있다.
  s = pd.Series([170,180],index=[0,2])
  df['some']=s
  print(df)
  
  
  #out
  #위에서 index를 지정한 0, 2번 행은 각기 some열에 값이 들어갔으나 지정해주지 않은 1번 행은 값이 들어가지 않았다. 
  info   name  age  gender   some
  index
  0       Kim   23    male  170.0
  1       Lee   25  female    NaN  
  2      Park   27    male  180.0
  
  
  #계산후 열 추가
  df['lifetime']=df['age']+70
  print(df)
  
  #out
  info   name  age  gender   some  lifetime
  index
  0       Kim   23    male  170.0        93
  1       Lee   25  female    NaN        95
  2      Park   27    male  180.0        97
  
  
  
  #함수를 사용하여 열 추가
  def A_or_B(gender):
      if gender=="male":
          return "A"
      else:
          return "B"
  df['some2']=df['gender'].apply(A_or_B)
  #df.some2=df['gender'].apply(A_or_B) -> 이 코드로는 수정은 돼도 추가는 안 된다.
  print(df)
  
  #out
     name  age  gender   some  lifetime some2
  0   Kim   23    male  170.0        93     A
  1   Lee   25  female    NaN        95     B
  2  Park   27    male  180.0        97     A
  ```

  - 열 수정

  ```python
  #열 전체 수정, 열 추가와 같다.
  df['some']=111
  print(df)
  
  #out
     name  age  gender  some  lifetime
  0   Kim   23    male   111        93
  1   Lee   25  female   111        95
  2  Park   27    male   111        97
  
  
  # 함수를 사용하여 열 수정, apply 사용, 열을 추가 할 때도 사용 가능.
  def A_or_B(age):
      print(age)
      if age>24:
          return "A"
      else:
          return "B"
  df.some=df.age.apply(A_or_B)
  #위 함수에서 바꿀 열의 값은 some이고 함수에 인자로 넘어가게 되는 값은 age이다.
  print(df)
  
  #out
  23
  25
  27
     name  age  gender some  lifetime
  0   Kim   23    male    B        93
  1   Lee   25  female    A        95
  2  Park   27    male    A        97
  ```

  

  - 열 삭제

  ```python
  #방법1. del을 사용
  del df['some']
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  
  
  #방법2-1. drop을 사용
  #drop은 기본적으로 행을 삭제할 때 사용하는 메소드이므로 열을 삭제하고자 한다면 axis=1을 입력하여 열을 삭제하려 한다는 것을 알려줘야 한다.
  df = df.drop('age',axis=1)
  print(df)
  
  #out
     name  gender  lifetime
  0   Kim    male        93
  1   Lee  female        95
  2  Park    male        97
  
  
  #방법2-2. 행 삭제와 마찬가지로 inplace 설정을 True로 하면 재할당 없이 바로 적용시킬 수 있다.
  df.drop('gender',axis=1, inplace=True)
  print(df)
  #out
     name  lifetime
  0   Kim        93
  1   Lee        95
  2  Park        97
  ```

  

  - 행 추가

  ```python
  #방법1. loc을 사용
  df.loc[3]=['Choi',21,'female',88]  #이 때 한 열의 값이라도 빠지면 에러가 발생
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  #방법2. append 를 사용
  df2 = pd.DataFrame([['Jeong',22,'male',89]],columns=['name','age','gender','lifetime'])
  
  #값이 실제로 바뀌진 않는다.
  print(df.append(df2))
  #ignore_index를 해주는 이유는 df2 역시 index가 0부터 시작될 것이므로 합치면 인덱스가 중복되게 되는데 ignore_index를 하면 합쳐지는 쪽의 인덱스가 합치는 쪽의 인덱스에 맞게 수정되어 들어가게 된다.
  print(df.append(df2,ignore_index=True))
  
  #out
  #인덱스 중복
      name  age  gender  lifetime
  0    Kim   23    male        93
  1    Lee   25  female        95
  2   Park   27    male        97
  3   Choi   21  female        88
  0  Jeong   22    male        89
  
  #gnore_index를 설정하여 인덱스가 중복이 일어나지 않았다.
      name  age  gender  lifetime
  0    Kim   23    male        93
  1    Lee   25  female        95
  2   Park   27    male        97
  3   Choi   21  female        88
  4  Jeong   22    male        89
  ```

  

  - 행 수정

  ```python
  # 행 추가와 마찬가지로 작성하면 되며 기존 행에 덮어씌워진다.
  print("before")
  print(df)
  print()
  
  df.loc[3]=['Cha',22,'male',60]
  print("after")
  print(df)
  
  
  #out
  before
     name  age  gender  lifetime
  0   Kim   23    male        93
  1   Lee   25  female        95
  2  Park   27    male        97
  3  Choi   21  female        88
  
  after
     name  age  gender  lifetime
  0   Kim   23    male        93
  1   Lee   25  female        95
  2  Park   27    male        97
  3   Cha   22    male        60
  ```

  

  

  - 행 삭제

  ```python
  #실제로 행이 삭제되지는 않는다.
  print(df.drop([2,3]))
  print()
  print(df)
  
  #out
  info  name  age  gender  lifetime
  index
  0      Kim   23    male        93
  1      Lee   25  female        95
  
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  # 삭제 1-1.drop한 DataFrame을 변수에 할당
  df = df.drop([1])
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  # 삭제 1-2.drop할 때 inplace 설정을 True로
  df.drop(0,inplace=True)
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  #삭제 2. boolean indexing을 활용하여 조건에 맞지 않는 값을 삭제
  df = df[df.age>=25]
  print(df)
  
  #out
  info   name  age
  index
  1       Lee   25
  2      Park   27
  ```

  

  - 데이터 프레임 정렬하기
    - `.sort_values()`: 특정 컬럼의 value를 기준으로 정렬
    - `.sort_index()`: index를 기준으로 정렬

  ```python
  name_age = pd.DataFrame({
    'name':['Kim','Lee','Park'],
    'age':[30,20,40]
  })
  print("정렬 안 한 상태")
  print(name_age)
  
  print("sort_values로 정렬하기")
  # .sort_values의 경우 column이 2개 이상일 때에는 by=''속성을 사용하여 어떤 컬럼을 기준으로 정렬할지 지정해 줘야 한다.
  print(name_age.sort_values(by="age"))
  print("내림 차순으로 정렬하기")
  # 내림 차순으로 정렬하려면 아래와 같이 ascending=boolean 속성을 사용한다.
  print(name_age.sort_values(by="age",ascending=False))
  
  print("sort_index로 정렬하기")
  print(name_age.sort_index())
  
  # 정렬해도 실제로 dataframe 자체가 변화하지는 않는데 실제로 변화시키기 위해서는 아래와 같이 implace=boolean 속성을 줘야 한다.
  name_age.sort_values(by='age',inplace=True)
  print("실제 변동된 값")
  print(name_age)
  
  #정렬시에 결측치를 처음과 끝 중 어디에 위치시킬지는 na_postion='first'/'last' 속성을 통해 결정 할 수 있다.
  
  #어떤 알고리즘으로 정렬할지는 kind='알고리즘명' 을 사용하여 설정 가능하다. quicksort 등 사용 가능 
  
  out
  정렬 안 한 상태
     name  age
  0   Kim   30
  1   Lee   20
  2  Park   40
  
  sort_values로 정렬하기
     name  age
  1   Lee   20
  0   Kim   30
  2  Park   40
  
  내림 차순으로 정렬하기
     name  age
  2  Park   40
  0   Kim   30
  1   Lee   20
  
  sort_index로 정렬하기
     name  age
  0   Kim   30
  1   Lee   20
  2  Park   40
  
  실제 변동된 값
     name  age
  1   Lee   20
  0   Kim   30
  2  Park   40
  ```

  

  

- Panel

  - 3차원 자료 구조로 Axis 0(items), Axis 1(major_axis), Axis 2(minor_axis) 등 3개의 축을 가지고 있는데 Axis 0은 그 한 요소가 DataFrame에 해당되며, Axis 1은 DataFrame의 행에 해당되고, Axis 2는 DataFrame의 열에 해당된다.



## 데이터 읽고 쓰기

- 외부 데이터 읽고 쓰기

  - pandas는 CSV, txt, Excel, SQL, HDF5 포맷 등 다양한 외부 리소스 데이터를 일고 쓸 수 있는 기능을 제공한다.

  - 엑셀 파일 저장을 위해선 `openpyxl`을 설치해야 한다.

    ```bash
    $ pip install openpyxl
    ```

  - 읽을 때는 `read_파일유형`, 쓸 때는 `to_파일유형`을 통해 가능하다.

    - excel의 경우 read_excel, to_excel로 사용하면 된다.
    - txt는 `read_csv`로 가져온다.

  - 각 열이 `,`로 구분되어 있으면 추가적인 코드 없이 `,`를 기준으로 분절되어 들어오지만 다른 것으로 구분되어 있을 경우 아래와 같이 `delimiter`라는 인자를 넘겨줘야 한다.

    ```python
    # 탭으로 구분된 경우
    df = pd.read_csv('data/list.txt',delimiter='\t')
    ```

  - 또한 읽어올 때 별도의 코드가 없으면 가장 첫 행이 열의 이름이 된다. 따라서 아래와 같이 `header=None`을 입력하면 열의 이름은 자동으로 0부터 시작하는 숫자가 들어가게 된다.

    ```python
    df=pd.read_csv('data/list.txt',header=None)
    
    #만일 header를 넣고 싶으면 아래와 같이 해주면 된다.
    df.columns = ['a','b','c']
    
    #두 과정을 동시에 하려면 아래와 같이 하면 된다.
    df=pd.read_csv('data/list.txt',header=None, names=['a','b','c'])
    ```

  - Dataframe을 파일로 저장

    ```python
    data = {
        'year': [2016, 2017, 2018],
        'name': ['김', '이', '박'],
        'height': ['1.637M', '1.73M', '1.83M']
    }
     
    df = pd.DataFrame(data)
    
    df.to_csv('파일명.csv')
    #엑셀 파일로 저장할경우
    #df.to_excel("test.xlsx")("파일명.xlsx")
    
    #코드를 작성한 파일이 있는 폴더에 파일명.csv 파일이 생성된다.
    
    #기본적으로 인덱스와 헤더가 함께 저장이 되는데 이를 막고 싶으면 아래와 같이 작성하면 된다.
    df.to_csv('파일명.csv',index=False,header=False)
    
    #또한 데이터가 비어있을 경우 기본적으로 빈칸이 되는데 이를 빈 칸이 아닌 다른 값으로 하고 싶다면 아래와 같이 하면된다.
    df.to_csv('파일명.csv',na_rap='대신할 값')
    ```

  

- sql 데이터를 읽어오는 방법

  > https://swalloow.github.io/db-to-dataframe/ 참고

  - sql 데이터를 읽고 쓰기 위해서는 `sqlalchemy`를 필수로 사용해야한다.

    ```bash
    $pip install sqlalchemy
    ```

  - 읽는 방법

    ```python
    import pandas as pd
    from sqlalchemy import create_engine
    
    engine = create_engine("mysql+pymysql://root:비밀번호@호스트:포트번호/db명", convert_unicode=True)
    conn = engine.connect()
    data = pd.read_sql_table('테이블명',conn)
    ```

    

  



## 데이터 처리

- 그룹화(`groupby`)

```python
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Lee',25,68,175,'female','psy'],
    ['Park',27,48,165,'female','phil'],
    ['Choi',22,57,168,'male','phil'],
    ['Jeong',29,77,188,'male','psy'],
    ['Han',34,47,158,'female','eco'],
    ['An',18,57,172,'male','phil'],
    ['Shin',37,71,178,'female','eco'],
    ['Song',29,48,168,'female','eco'],
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

groupby_major = df.groupby('major')
print(groupby_major)
print()
print(groupby_major.groups)

#out
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x00000297D560F780>

{'eco': Int64Index([5, 7, 8], dtype='int64'), 'phil': Int64Index([2, 3, 6], dtype='int64'), 'psy': Int64Index([0, 1, 4], dtype='int64')}


#활용
for n, g in groupby_major:
    print(n+":"+str(len(g))+'명')
    print(g)
    print()

#out
eco:3명
   name  age  weight  height  gender major
5   Han   34      47     158  female   eco
7  Shin   37      71     178  female   eco
8  Song   29      48     168  female   eco

phil:3명
   name  age  weight  height  gender major
2  Park   27      48     165  female  phil
3  Choi   22      57     168    male  phil
6    An   18      57     172    male  phil

psy:3명
    name  age  weight  height  gender major
0    Kim   23      71     178    male   psy
1    Lee   25      68     175  female   psy
4  Jeong   29      77     188    male   psy


#각 전공별 인원수를 DataFrame으로 만들기
dic = {
    'count':groupby_major.size()
    }
df_major_cnt = pd.DataFrame(dic)
print(df_major_cnt)

#out
       count
major
eco        3
phil       3
psy        3

# .reset_index()
#위에서 major가 각각의 행을 형성하고 있는데 이를 column으로 옮기려면 아래와 같이 reset_index()를 해주면 된다.
df_major_cnt = pd.DataFrame(dic).reset_index()
print(df_major_cnt)

#out
  major  count
0   eco      3
1  phil      3
2   psy      3
```





- 중복 데이터 삭제
  - `.duplicated()`: 중복 데이터가 있는지 확인
  - `.drop_duplicates()`

```python
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Lee',23,71,178,'male','psy'],  #하나만 다르다.
    ['Kim',23,71,178,'male','psy'],  #완전히 중복.
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

#중복 데이터가 있는지 확인
print(df.duplicated())

#out
0    False
1    False
2     True  #완전히 중복이어야 True를 반환
dtype: bool
    

#중복 데이터 삭제
print(df.drop_duplicates())  #실제로 삭제되지는 않는다. 실제로 삭제하려면 재할당 필요

#out
  name  age  weight  height gender major
0  Kim   23      71     178   male   psy
1  Kim   23      71     178   male   eco


#특정 열의 값이 중복되는 행을 확인
print(df.duplicated(['name']))

#out
0    False
1    False
2     True
dtype: bool
    
    
    
#특정 열의 값이 중복되는 행을 삭제
#첫 번째 인자로 중복을 확인해 삭제할 열을, 두 번째 인자로 중복된 행 중 어떤 행을 살릴 것인지를 keep을 통해 설정해준다. keep값을 주지 않을 경우  default는 first다.
print("keep='first'")
print(df.drop_duplicates(['name'],keep='first'))
print("keep='last'")
print(df.drop_duplicates(['name'],keep='last'))

#out
keep='first'
  name  age  weight  height gender major
0  Kim   23      71     178   male   psy
1  Lee   23      71     178   male   psy
keep='last'
  name  age  weight  height gender major
1  Lee   23      71     178   male   psy
2  Kim   23      71     178   male   psy
```





- NaN을 찾아서 원하는 값으로 변경하기

  - Pandas에서는 숫자가 올 열에 `None`을 넣으면 `NaN`이 들어가고 문자가 올 열에 넣으면 그대로 `None`이 들어간다.
  - `.shape`: DataFrame의 크기를 확인하는 메소드, `(행의 개수, 열의 개수)` 형태로 결과가 출력된다.
  - `.info()`: DataFrame의 정보를 확인하는 메소드
  - `.isna()`, `.isnull()`: `None` 값을 확인하는 메소드, 둘의 기능은 같다.
    - pandas의 소스 코드를 보면 `isnull=isna` 부분을 확인할 수 있다. 즉, `isnull`은 `isna`의 별칭이다.

  ```python
  data = [
      ['Kim',23,71,178,'male','psy'],
      ['Park',27,48,165,'female','phil'],
      ['Song',29,48,168,'female','eco'],
      ['Lee',23,71,None,'male',None],
      ['Lee',23,52,None,'female',None],
  ]
  col_name=['name','age','weight','height','gender','major']
  df=pd.DataFrame(data,columns=col_name)
  print(df)
  print()
  print(".shape")
  print(df.shape)
  print()
  print(".info()")
  print(df.info())
  print()
  print(".isna()")
  print(df.isna())
  print()
  print(".isnull()")
  print(df.isnull())
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     NaN    male  None
  4   Lee   23      52     NaN  female  None
  
  .shape
  (5, 6)
  
  .info()
  <class 'pandas.core.frame.DataFrame'>
  RangeIndex: 5 entries, 0 to 4
  Data columns (total 6 columns):
  name      5 non-null object
  age       5 non-null int64
  weight    5 non-null int64    #5개의 행 중 5개가 null 값이 아님
  height    3 non-null float64  #5개의 행 중 3개가 null 값이 아님
  gender    5 non-null object
  major     3 non-null object
  dtypes: float64(1), int64(2), object(3)
  memory usage: 368.0+ bytes
  None
  
  .isna()
      name    age  weight  height  gender  major
  0  False  False   False   False   False  False
  1  False  False   False   False   False  False
  2  False  False   False   False   False  False
  3  False  False   False    True   False   True
  4  False  False   False    True   False   True
  
  .isnull()
      name    age  weight  height  gender  major
  0  False  False   False   False   False  False
  1  False  False   False   False   False  False
  2  False  False   False   False   False  False
  3  False  False   False    True   False   True
  4  False  False   False    True   False   True
  ```

  

  - `.fillna()`: `Nan`을 괄호 안에 있는 값으로 변경

  ```python
  #방법1. 재할당
  df.height = df.height.fillna(0)
  df.major = df.major.fillna(0)   #다른 열에 들어 있는 자료형과 달라도 변경이 가능하다.
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     0.0    male     0
  4   Lee   23      52     0.0  female     0
  
  
  
  #방법2. inplace 사용으로 재할당 없이
  df['height'].fillna(0,inplace=True)
  df['major'].fillna(0,inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     0.0    male     0
  4   Lee   23      52     0.0  female     0
  
  
  
  #다른 열의 데이터에 따라 다른 값을 넣고자 할 때
  #null 값이 있어야 fillna를 쓸 수 있으므로 재선언 한 후
  #남자면 height를 남자의 평균으로, 여자면 height를 여자의 평균으로 넣으려 한다면
  # 아래 코드에서 df.groupby('gender')['height'].transform('median')까지가 넣을 값을 결정하는 코드다.
  df['height'].fillna(df.groupby('gender')['height'].transform('median'),inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71   178.0    male  None
  4   Lee   23      52   166.5  female  None
  
  
  
  #몸무게가 60 이상이면 경제학, 미만이면 심리학을 전공으로 넣으려 한다면
  def decide_major(weight):
      if weight>=60:
          return "eco"
      else:
          return "psy"
  df.major.fillna(df.weight.apply(decide_major),inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71   178.0    male   eco
  4   Lee   23      52   166.5  female   psy
  ```





- `apply` 심화

  ```python
  #추가 인자 전달(같은 방법으로 복수의 추가 인자를 넘기는 것이 가능)
  def get_birth(age,current_year):
      return current_year-age+1
  
  df['birth']=df['age'].apply(get_birth,current_year=2020)
  print(df)
  
  #out
     name  age  weight  height  gender major  birth
  0   Kim   23      71     178    male   psy   1998
  1  Park   27      48     165  female  phil   1994
  2  Song   29      48     168  female   eco   1992
  3   Lee   23      71     180    male   psy   1998
  4   Lee   23      52     170  female   eco   1998
  
  
  
  #복수의 열을 인자로 넘기는 방법
  def cal_bmi(row):
      return round(row.weight/(row.height**2)*10000,2)
  
  #df를 통째로 인자로 넘기는 코드로 axis=1을 줘서 행을 넘기는 것이다.
  df['BMI']=df.apply(cal_bmi,axis=1)
  print(df)
  
  #out
     name  age  weight  height  gender major  birth    BMI
  0   Kim   23      71     178    male   psy   1998  22.41
  1  Park   27      48     165  female  phil   1994  17.63
  2  Song   29      48     168  female   eco   1992  17.01
  3   Lee   23      71     180    male   psy   1998  21.91
  4   Lee   23      52     170  female   eco   1998  17.99
  
  
  
  #lambda 식을 사용하는 것도 가능하다.
  ```

  



- `map`, `applymap`

  - `.map()`: apply와 사용법이 동일하다. 다만 `map`은 `apply` 와 달리 함수를 사용하지 않고 dictionary로 직접 값을 변경 가능하다.

  ```python
  #apply와 동일한 사용법
  data = [
      ['1997-02-04'],
      ['1992-07-18'],
  ]
  col_name=['date']
  df=pd.DataFrame(data,columns=col_name)
  
  def year(date):
      return date.split('-')[0]
  
  df['year']=df['date'].map(year)
  print(df)
  
  #out
           date  year
  0  1997-02-04  1997
  1  1992-07-18  1992
  
  
  
  #apply와 다른 사용법
  df.year = df.year.map({'1997':197, '1992':192})
  print(df)
  
  #out
           date  year
  0  1997-02-04   197
  1  1992-07-18   192
  ```

  

  - `.applymap()`: DataFrame 내의 모든 값을 일괄적으로 변경시키기 위해 사용

  ```python
  def change_all(df):
      return 0
  
  df = df.applymap(change_all)
  print(df)
  
  #out
     date  year
  0     0     0
  1     0     0
  ```

  



- `unique`, `value_counts`

  - `.unique()`: 컬럼 내의 데이터를 중복되지 않게 뽑을 때 사용

  ```python
  data = [
      ['Kim',23,'male','psy'],
      ['Park',27,'female','phil'],
      ['Song',29,'female','eco'],
      ['Lee',23,'male','psy'],
      ['Lee',23,'female','eco'],
      ['Jeong',23,'female','geo'],
  ]
  col_name=['name','age','gender','major']
  df=pd.DataFrame(data,columns=col_name)
  
  print(df.major.unique())
  print(type(df.major.unique()))
  
  #out
  ['psy' 'phil' 'eco' 'geo']
  <class 'numpy.ndarray'>
  ```

  

  - `.value_counts()`: 각 데이터 별 개수 확인
    - `.value_counts` 처럼 `()`를 붙이지 않고 쓸 경우 완전히 다른 결과를 반환하므로 주의

  ```python
  print(df.major.value_counts())
  
  eco     2
  psy     2
  geo     1
  phil    1
  Name: major, dtype: int64
  ```

  



- 두 개의 DataFrame 합치기

  - `.concat()`: Pandas의 함수로 인자로 합칠 데이터 프레임 2개를 넘긴다.
  - `.append()`: DataFrame의 메소드로 합쳐질 데이터 프레임을 인자로 넘긴다.

  ```python
  # 행으로 합치기
  # 방법1. .concat()사용
  data1 = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
  df1 = pd.DataFrame(data1)
  
  data2 = {
      'name':['Choi','Jeong','An'],
      'age':[31,35,33],
  }
  df2 = pd.DataFrame(data2)
  
  result = pd.concat([df1,df2])
  print(result)
  
  #인덱스를 겹치지 않게 하려면 아래와 같이
  result = pd.concat([df1,df2],ignore_index=True)
  print(result)
  
  #out
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  0   Choi   31
  1  Jeong   35
  2     An   33
  
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  3   Choi   31
  4  Jeong   35
  5     An   33
  
  
  
  #방법2. .append()사용
  result = df1.append(df2, ignore_index=True)
  
  #out
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  3   Choi   31
  4  Jeong   35
  5     An   33
  
  
  
  
  #열로 합치기
  #열로 합칠 때 ingnore_index=True를 주면 열의 이름이 0부터 시작하는 숫자로 변하게 된다.
  data3 = {
      'major':['psy','eco','phil'],
      'gender':['male','male','female'],
  }
  df3 = pd.DataFrame(data3)
  
  #.concat()사용, .append()는 사용 불가
  result = pd.concat([df1,df3],axis=1)
  print(result)
  ```








# Matplotlib

- Matplotlib:  파이썬에서 데이타를 차트나 플롯(Plot)으로 그려주는 라이브러리 패키지로서 가장 많이 사용되는 데이타 시각화(Data Visualization) 패키지



- 기초

  - 그래프 선언과 출력

    - 그래프 선언 후 show()를 사용하여 그래프 출력

    ```python
    from matplotlib import pyplot as plt
     
    # 처음에 넣는 리스트가 x축이 되고, 두 번째로 넣는 리스트가 y축이 된다.
    plt.plot(["a","b","c"], [100,120,90])
    # show()를 사용하여 출력
    plt.show()
    
    plt.plot([1,2,3], ["A","B","C"])
    plt.show()
    ```

    

  - x,y축 레이블과 그래프의 제목 붙이기.

    ```python
    plt.plot(["a","b","c"], [48,67,58])
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.show()
    ```

    

  - 범례 추가

    ```python
    plt.plot(["a","b","c"], [48,67,58])
    plt.plot(["a","b","c"], [52,68,68])
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.legend(['Before', 'After'])
    plt.show()
    ```

    

  - DataFrame 사용

    - 아래와 같이 pandas의 dataframe 자료형을 사용하여 표현할 수 있다.

    ```python
    from matplotlib import pyplot as plt
    import pandas as pd
    
    df = pd.DataFrame({'Before': [48,67,58],'After': [52,67,68]},
                        index=["a","b","c"]
                        )
    plt.plot(df)
    plt.show()
    ```

    

  - 다른 형태의 그래프

    - 위에서 살펴본 직선 이외에도 아래와 같이 막대 그래프로 표현할 수 있다.

    ```python
    plt.bar(["a","b","c"], [48,67,58],width=0.5,color="blue")
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.show()
    
    #DataFrame 자료형을 통해 여러개의 막대를 표현할 수 있다.
    ```

    






# APScheduler

- Python에서 schedule 처리를 보다 간편하게 할 수 있게 해주는 package

  > [github](https://github.com/agronholm/apscheduler)

  - 관련 package로는 아래와 같은 것들이 있다.
    - Python의 내장 package인 `sched`
    - 분산 처리 큐 package인 `celery`
    - `sched`의 경우 지원하는 기능이 제한적이고, `celery`의 경우 package의 목적이 스케쥴링 보다는 분산 처리에 가깝다.
  - `APScheduler`를 사용하면 스케쥴링이 필요한 작업들을 동적으로 추가, 수정, 삭제할 수 있다.
  - 설치

  ```bash
  $ pip intall apscheduler
  ```

  - github에서 [다양한 예제 코드](https://github.com/agronholm/apscheduler/tree/3.x/examples/?at=master)를 볼 수 있다.



- 4개의 component로 구성된다.

  - Triggers
    - Scheduling과 관련된 logic이 포함되어 있다.
    - 모든 job은 job의 실행 시점을 결정하는 각각의 trigger를 가지고 있다.
  - Job stores
    - Job들을 저장하는 저장소이다.
    - 기본적으로 job들을 memory에 저장하지만, database 등의 저장소를 사용할 수도 있다.
  - Executors
    - Job의 실행을 통제하는 역할을 한다.
  - Scheduler
    - 여러 job들을 하나로 묶어서 관리하는 역할을 한다.
    - 일반적으로 하나의 application에 하나씩 존재한다.
    - 일반적으로 trigger, job store, executor를 직접 조작하진 않고, scheduler를 통해서 조작한다.
    - 다양한 종류의 Scheduler가 존재한다.
  - 구성 예시

  ```python
  from pytz import utc
  
  from apscheduler.schedulers.background import BackgroundScheduler
  from apscheduler.jobstores.mongodb import MongoDBJobStore
  from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
  from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
  
  # mongodb에 job들을 저장한다.
  jobstores = {
      'mongo': MongoDBJobStore(),
      'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
  }
  executors = {
      'default': ThreadPoolExecutor(20),
      'processpool': ProcessPoolExecutor(5)
  }
  job_defaults = {
      'coalesce': False,
      'max_instances': 3
  }
  scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
  ```



- 실행해보기

  - Job 추가 및 삭제
    - 예시에서는 `BackgroundScheduler`를 사용한다.
    - 삭제는 `add_job()`메서드가 반환한 job 객체의 id 속성을 사용하거나, job 객체 자체를 사용하여 삭제한다.
  
  
  ```python
  from datetime import datetime
  import time
  import os
  
  from apscheduler.schedulers.background import BackgroundScheduler
  
  
  def tick(foo):
      print(foo)
      print('Tick! The time is: %s' % datetime.now())
  
  
  if __name__ == '__main__':
      scheduler = BackgroundScheduler()
      # job을 등록하고
      job = scheduler.add_job(tick, 'interval', ["foo"], seconds=3)
      # scheduler를 실행시킨다.
      scheduler.start()
      print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  
      try:
          # BackgroundScheduler의 경우 이름처럼 background에서 실행되기 때문에 main process를 계속 실행중으로 유지해야한다.
          cnt = 0
          while True:
              cnt += 1
              if cnt == 5:
                  # job id를 통해 삭제한다.
                  scheduler.remove_job(job.id)
                  # 혹은 아래와 같이 job 객체 자체를 사용하여 삭제할 수도 있다.
                  # job.remove()
              time.sleep(2)
              
      except (KeyboardInterrupt, SystemExit):
          scheduler.shutdown()
  ```
  
  - 삭제를 더욱 편하게 하고자 한다면 아래와 같이 id를 지정해서 job을 생성할 수도 있다.
  
  ```python
  job = scheduler.add_job(my_func, 'interval', seconds=3, id="123")
  print(job.id)	# 123
  ```
  





# Linter & formmater

- Linter와 formmater의 차이
  - Linter
    - 소스 코드를 분석하여 bug가 발생할 수 있는 code를 찾아주는 기능을 하는 도구.
    - 잠재적 bug분석 뿐 아니라 bad practice도 표기해준다.
    - Python의 경우 Pylint, Flake8, Ruff 등이 있으며, Rust-Pyhon으로 개발된 Ruff가 매우 빠른 속도로 인기를 얻고 있다.
  - Formmater
    - 소스 코드가 일정한 스타일을 준수하여 작성되었는지르 검사해주는 도구.
    - Python으로 예시를 들면 PEP8을 준수하여 코드를 작성했는지를 검사해준다.
    - Python의 경우 CPython 개발자들이 개발한 Black 등이 있다.



- python poetry
  - 의존성 관리 툴
  - pip 대체제



- mypy
  - Python의 static type check 도구.



- Black

  > https://github.com/psf/black
  >
  > https://black.readthedocs.io/en/stable/

  - CPython을 개발한Python Software Foundation에서 개발한 code formmater이다.
    - Python community에서 가장 널리 쓰는 formmater 중 하나이다.
    - 사용자가 설정할 여지가 거의 없어 Black이 정한 규칙을 그대로 따라야한다.
    - 오히려 custom이 불가능하다는 점이 장점으로, 작업자들 사이에 코드 style을 정하는 것이 굉장히 힘들고 소모적인 논쟁을 불러올 수 있기 때문이다.
    - Black은 Python community의 다양한 의견을 수렴하고, 여러 프로젝트를 통해 실험하여 대부분의 프로젝트에 무난히 적용할 수 있는 style을 선택했다.
  - Black 설치하기

  ```bash
  $ pip install black
  ```

  - 사용해보기
    - 기존 file의 내용이 변경되므로 주의가 필요하다.

  ```bash
  $ black <source_file 또는 directory>
  
  # 또는
  $ python -m black source_file 또는 directory>
  ```

  - 아래와 같은 code가 있을 때

  ```python
  from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc
  x = {  'a':37,'b':42,
  
  'c':927}
  
  x = 123456789.123456789E123456789
  
  if very_long_variable_name is not None and \
   very_long_variable_name.field > 0 or \
   very_long_variable_name.is_debug:
   z = 'hello '+'world'
  else:
   world = 'world'
   a = 'hello {}'.format(world)
   f = rf'hello {world}'
  if (this
  and that): y = 'hello ''world'#FIXME: https://github.com/psf/black/issues/26
  class Foo  (     object  ):
    def f    (self   ):
      return       37*-2
    def g(self, x,y=42):
        return y
  def f  (   a: List[ int ]) :
    return      37-a[42-u :  y**3]
  def very_important_function(template: str,*variables,file: os.PathLike,debug:bool=False,):
      """Applies `variables` to the `template` and writes to `file`."""
      with open(file, "w") as f:
       ...
  # fmt: off
  custom_formatting = [
      0,  1,  2,
      3,  4,  5,
      6,  7,  8,
  ]
  # fmt: on
  regular_formatting = [
      0,  1,  2,
      3,  4,  5,
      6,  7,  8,
  ]
  ```

  - black을 적용하면, 아래와 같이 바뀐다.

  ```python
  from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc
  
  x = {"a": 37, "b": 42, "c": 927}
  
  x = 123456789.123456789e123456789
  
  if (
      very_long_variable_name is not None
      and very_long_variable_name.field > 0
      or very_long_variable_name.is_debug
  ):
      z = "hello " + "world"
  else:
      world = "world"
      a = "hello {}".format(world)
      f = rf"hello {world}"
  if this and that:
      y = "hello " "world"  # FIXME: https://github.com/psf/black/issues/26
  
  
  class Foo(object):
      def f(self):
          return 37 * -2
  
      def g(self, x, y=42):
          return y
  
  
  def f(a: List[int]):
      return 37 - a[42 - u : y**3]
  
  
  def very_important_function(
      template: str,
      *variables,
      file: os.PathLike,
      debug: bool = False,
  ):
      """Applies `variables` to the `template` and writes to `file`."""
      with open(file, "w") as f:
          ...
  
  
  # fmt: off
  custom_formatting = [
      0,  1,  2,
      3,  4,  5,
      6,  7,  8,
  ]
  # fmt: on
  regular_formatting = [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
  ]
  ```

  - [Black Playground](https://black.vercel.app/)에서 test해볼 수 있다.
  - Pycharm, Visual Studio Code, Vim 등의 editor에서 자동으로 실행되도록 설정이 가능하다.
    - 각 editor별 설정 방법은 [공식문서](https://black.readthedocs.io/en/stable/integrations/editors.html#)참고
