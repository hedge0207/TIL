# Locust

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

  ![locust_main](packages_part4.assets/locust_main.png)

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





# Shorts

- faker

  - 언어를 한국어로 설정하고 `catch_phrase()`를 사용하면 무작위로 생성된 짧은 문자열을 얻을 수 있다.

  ```python
  from faker import Faker
  
  fake = Faker("ko-KR")
  print(fake.catch_phrase())
  ```



- Python StateMachine

  - Python을 사용하여 직관적으로 finite state machine(FSM)을 구현할 수 있게 해주는 package

  - 설치

  ```bash
  $ pip install python-statemachine
  ```

  - 실행해보기
    - state와 event를 구현한다.
    - `send()` method에 event로 선언한 변수명을 string 형태로 넣으면 transition이 발생한다.
    - `before_<evnet>` method를 통해 transition이 발생하기 전에 실행할 action을 설정 가능하다.
    - `on_enter_<state>`, `on_exit_<state>` method를 통해 state로 transition될 때, state에서 다른 state로 transition 될 때 실행할 action을 설정 할 수 있다.

  ```python
  from statemachine import StateMachine, State
  
  
  class TrafficLightMachine(StateMachine):
      # state를 정의한다.
      green = State(initial=True)
      yellow = State()
      red = State()
  
      # event를 정의한다.
      cycle = (
          green.to(yellow)
          | yellow.to(red)
          | red.to(green)
      )
      
      def before_cycle(self, event: str, source: State, target: State, message: str = ""):
          message = ". " + message if message else ""
          return f"Running {event} from {source.id} to {target.id}{message}"
      
      def on_enter_red(self):
          print("Don't move.")
      
      def on_exit_red(self):
          print("Go ahead!")
  
  state_machine = TrafficLightMachine()
  print(state_machine.current_state)		# State('Green', id='green', value='green', initial=True, final=False)
  print(state_machine.send("cycle"))		# Running cycle from green to yellow
  print(state_machine.current_state)		# State('Yellow', id='yellow', value='yellow', initial=False, final=False)
  print(state_machine.send("cycle"))		# Don't move.
  										# Running cycle from yellow to red
  print(state_machine.current_state)		# State('Red', id='red', value='red', initial=False, final=False)
  										# Go ahead!
  print(state_machine.send("cycle"))		# Running cycle from red to green
  ```



- Provider override

  - 한 provider를 다른 provider로 override할 수 있다.
    - Test시에 유용하게 사용할 수 있는데, 실제 API client를 개발용 stub으로 변경하는 등과 같이 사용할 수 있기 때문이다.
  - Override를 위해서는 `Provider.override()` method를 호출해야한다.
    - 이 method는 overriding이라 불리는 하나의 argument를 받는다.
    - 만약 overriding에 provider를 넘길 경우 provider 호출 시 원래 provider 대신 이 provider가 호출된다.
    - 만약 overriding에 provider가 아닌 값을 넘길 경우 원래 provider 호출 시 원래 provider가 호출되는 대신 이 value가 반환된다.

  - 예시

  ```python
  import dataclasses
  import unittest.mock
  
  from dependency_injector import containers, providers
  
  
  class ApiClient:
      ...
  
  
  class ApiClientStub(ApiClient):
      ...
  
  
  @dataclasses.dataclass
  class Service:
      api_client: ApiClient
  
  
  class Container(containers.DeclarativeContainer):
  
      api_client_factory = providers.Factory(ApiClient)
  
      service_factory = providers.Factory(
          Service,
          api_client=api_client_factory,
      )
  
  
  if __name__ == "__main__":
      container = Container()
  
      # 운영 환경에서 사용할 ApiClient 대신 ApiClientStub을 생성하도록 override한다.
      container.api_client_factory.override(providers.Factory(ApiClientStub))
      service1 = container.service_factory()
      assert isinstance(service1.api_client, ApiClientStub)
  
      # 2. override를 context manager로 사용하여 APIClient의 mock object를 override한다.
      with container.api_client_factory.override(unittest.mock.Mock(ApiClient)):
          service2 = container.service_factory()
          assert isinstance(service2.api_client, unittest.mock.Mock)
  
      # 3. .reset_override()룰 사용하여 override를 해제한다.
      container.api_client_factory.reset_override()
      service3 = container.service_factory()
      assert isinstance(service3.api_client, ApiClient)
  ```

  

