# argparse

- argparse
  - CLI로 Python에 옵션을 추가할 수 있게 해주는 library
  - Python 내장 library로 별도의 설치가 필요 없다.



- 실행해보기

  - argument 추가하기

  ```python
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", dest="api_port", action="store")
  parser.add_argument("-b", "--boolean", dest="boolean", action="store_true")
  args = parser.parse_args()
  
  print(args.api_port)
  print(args.boolean)
  ```

  - 실행하기

  ```bash
  $ python test.py -p 8000 -b
  ```



- 옵션
  - `dest` 옵션은 해당 argument를 어떤 이름으로 저장할 것인지를 선택한다.
    - 위 예시에서 `-p`로 받은 값을 `api_port`라는 이름으로 저장했다.
  - `action` 옵션은 argument에 어떤 action을 취할지를 지정한다.
    - `store`: argument 뒤에 반드시 값이 와야 한다.
    - `store_field`: argument 뒤에 값이 와선 안되며, argument의 유무만 판단한다.
    - 이 밖에도 [다양한 옵션](https://docs.python.org/ko/3/library/argparse.html#action)이 있다.
  - `type`
    - argument의 타입을 지정할 수 있다.
  - `required`
    - 필수 argument로 만들 수 있다.
  - `default`
    - argument가 입력되지 않았을 경우 기본 값을 지정할 수 있다.



- help

  - 기본적으로 `--help` 혹은 `-h` 옵션을 통해 arguments에 대한 정보를 볼 수 있다.
    - 이 경우 script는 실행하지 않고 arguments의 정보만 출력한다.

  ```bash
  $ python test.py -h
  ```

  - 각 argument에 대한 설명을 추가하는 것도 가능하다.
    - `add_argument` 메서드에 `help` 파라미터를 추가한다.

  ```python
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", dest="api_port", action="store", help="Port for API URI")
  
  args = parser.parse_args()
  ```





# click

> https://click.palletsprojects.com/en/8.0.x/

- Python CLI를 보다 쉽게 사용할 수 있게 해주는 library

  - Command Line Interface Creation Kit의 줄임말이다.
  - Python 내장 패키지인 argparse와 유사한 역할을 한다.
  - 설치

  ```bash
  $ pip install click
  ```



- 커맨드 생성하기

  - `@click.command` decorator를 함수에 추가하면 해당 함수는 command line tool이 된다.
    - `echo`는 `print` 함수 대신 사용하는 것으로, Python2와의 호환을 위해 만든 것이다.
    - `echo` 대신 `print`를 사용해도 된다.

  ```python
  import click
  
  
  @click.command()
  def hello():
      click.echo('Hello World!')
  
  if __name__ == '__main__':
      hello()
  ```

  - nested command 추가하기

  ```python
  import click
  
  
  @click.group()
  def cli():
      pass
  
  @click.command()
  def initdb():
      click.echo('Initialized the database')
  
  @click.command()
  def dropdb():
      click.echo('Dropped the database')
  
  cli.add_command(initdb)
  cli.add_command(dropdb)
  ```

  - 보다 간단하기 nested command 생성하기

  ```python
  # 혹은 아래와 같이 보다 간단하게 만들 수 있다.
  @click.group()
  def cli():
      pass
  
  # group decorator를 붙인 함수의 이름을 decorator로 쓴다.
  @cli.command()
  def initdb():
      click.echo('Initialized the database')
  
  @cli.command()
  def dropdb():
      click.echo('Dropped the database')
  ```

  - `--help` 명령어를 입력했을 때 나오는 값들도 자동으로 생성해준다.

  ```bash
  $ python test.py --help
  ```



- 파라미터 추가하기

  - `argument`와 `option`이 존재하는데 `option`이 더 많은 기능을 제공한다.

  ```python
  @click.command()
  @click.option('--count', default=1, help='number of greetings')
  @click.argument('name')
  def hello(count, name):
      for x in range(count):
          click.echo('Hello %s!' % name)
  ```

  - parameter의 type 설정하기

    > 지원하는 type 목록은 https://click.palletsprojects.com/en/7.x/options/#choice-opts에서 확인 가능하다.

    - 다음과 같이 type을 지정해준다.
    - 예시로 든 `click.Choice`은 list 안에 있는 값들 중 하나를 받는 것이며, `case_sensitive` 옵션은 대소문자 구분 여부를 결정하는 것이다.

  ```python
  @click.command()
  @click.option('--hash-type',
                type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
  def digest(hash_type):
      click.echo(hash_type)
  ```



- Option의 충돌

  - locust와 같이 자체적으로 cli을 사용하는 패키지와 함께 사용할 경우 충돌이 발생할 수 있다.
  - 이 경우 click으로 추가한 option들을 충돌이 발생한 패키지에도 추가해주거나, 충돌이 난 패키지에서 삭제해줘야 한다.
  - 삭제
    - `sys.argv`에는 option 값들이 List[str] 형태로 저장되어 있는데, 여기서 삭제해주면 된다.

  ```python
  import sys
  
  sys.argv.remove("<삭제할 옵션 이름>")
  ```

  - 추가
    - 충돌이 발생한 패키지에서 command line option을 추가하는 기능을 제공하면 click으로 받은 옵션 값들을 해당 패키지의 cli에도 추가해준다.



# Python gRPC

> 예시에서 사용한 source code는 https://github.com/grpc/grpc/tree/v1.46.3/examples/python/route_guide 에서 확인 가능하다.

- grpc 설치하기

  > Python 3.5 이상, pip 9.0.1 이상이 필요하다.

  - grpc 설치

  ```bash
  $ pip install grpcio
  ```

  - grpc tools 설치
    - `.proto`파일로부터 서버와 클라이언트 파일을 생성하는 plugin과 `protoc`가 포함되어 있다.

  ```bash
  $ pip install grpcio-tools
  ```



- `pb2_grpc` 파일과 `pb2` 파일 생성하기

  - 두 파일에는 아래와 같은 정보가 작성된다.
    - `message` 키워드로 정의된 데이터 타입의 class
    - `service` 키워드로 정의된 서비스의 class
    - `~Stub` class는 cleint가 RPC를 호출하는 데 사용된다.
    - `~Servicer` class는 서비스의 구현을 위한 인터페이스가 정의되어 있다.
    - `service` 키워드로 정의된 서비스의 함수.
  - `.proto` file 작성

  ```protobuf
  // route_guide.proto
  
  syntax = "proto3";
  
  service RouteGuide {
    rpc GetFeature(Point) returns (Feature) {}
  
    rpc ListFeatures(Rectangle) returns (stream Feature) {}
  
    rpc RecordRoute(stream Point) returns (RouteSummary) {}
  
    rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
  }
  
  message Point {
    int32 latitude = 1;
    int32 longitude = 2;
  }
  
  message Rectangle {
    Point lo = 1;
  
    Point hi = 2;
  }
  
  message Feature {
    string name = 1;
  
    Point location = 2;
  }
  
  message RouteNote {
    Point location = 1;
  
    string message = 2;
  }
  
  message RouteSummary {
    int32 point_count = 1;
  
    int32 feature_count = 2;
  
    int32 distance = 3;
  
    int32 elapsed_time = 4;
  }
  ```

  - `.proto` file으로 python code 생성하기
    - 아래 명령어의 결과로 `route_guide_pb2.py`,  `route_guide_pb2_grpc.py` 파일이 생성된다.

  ```bash
  $ python -m grpc_tools.protoc -I<proto file이 있는 폴더의 경로> --python_out=<pb2 파일을 생성할 경로> --grpc_python_out=<pb2_grpc 파일을 생성할 경로> <proto file의 경로>
  ```

  - `pb2`에서 2의 의미
    - Protocol Buffers Python API version 2에 따라 파일이 생성되었다는 의미이다.
    - Version 1은 더이상 사용되지 않는다.

  

- Server 생성하기

  - 서버를 생성하는 로직은 크게 두 부분으로 나뉜다.
    - servicer interface를 상속 받아 실제 service를 동작시키는 클래스와 함수의 구현.
    - client로부터 요청을 받을 gRPC서버를 실행시키기.
  - 예시
    - `route_guid_pb2_grpc.py`파일의 `RouteGuide` class에 정의된 모든 메서드를 구현한다.

  ```python
  from concurrent import futures
  import logging
  import math
  import time
  
  import grpc
  import route_guide_pb2
  import route_guide_pb2_grpc
  import route_guide_resources
  
  
  def get_feature(feature_db, point):
      """Returns Feature at given location or None."""
      for feature in feature_db:
          if feature.location == point:
              return feature
      return None
  
  
  def get_distance(start, end):
      """Distance between two points."""
      coord_factor = 10000000.0
      lat_1 = start.latitude / coord_factor
      lat_2 = end.latitude / coord_factor
      lon_1 = start.longitude / coord_factor
      lon_2 = end.longitude / coord_factor
      lat_rad_1 = math.radians(lat_1)
      lat_rad_2 = math.radians(lat_2)
      delta_lat_rad = math.radians(lat_2 - lat_1)
      delta_lon_rad = math.radians(lon_2 - lon_1)
  
      # Formula is based on http://mathforum.org/library/drmath/view/51879.html
      a = (pow(math.sin(delta_lat_rad / 2), 2) +
           (math.cos(lat_rad_1) * math.cos(lat_rad_2) *
            pow(math.sin(delta_lon_rad / 2), 2)))
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
      R = 6371000
      # metres
      return R * c
  
  
  class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
      """Provides methods that implement functionality of route guide server."""
  
      def __init__(self):
          self.db = route_guide_resources.read_route_guide_database()
  	
      #  client로부터 Point를 받아서 해당 Point와 일치하는 Feature를 DB에서 찾아서 반환한다.
      def GetFeature(self, request, context):
          feature = get_feature(self.db, request)
          if feature is None:
              return route_guide_pb2.Feature(name="", location=request)
          else:
              return feature
  	
      # response-streaming method
      def ListFeatures(self, request, context):
          left = min(request.lo.longitude, request.hi.longitude)
          right = max(request.lo.longitude, request.hi.longitude)
          top = max(request.lo.latitude, request.hi.latitude)
          bottom = min(request.lo.latitude, request.hi.latitude)
          for feature in self.db:
              if (feature.location.longitude >= left and
                      feature.location.longitude <= right and
                      feature.location.latitude >= bottom and
                      feature.location.latitude <= top):
                  yield feature
  	
      # request-streaming method
      def RecordRoute(self, request_iterator, context):
          point_count = 0
          feature_count = 0
          distance = 0.0
          prev_point = None
  
          start_time = time.time()
          for point in request_iterator:
              point_count += 1
              if get_feature(self.db, point):
                  feature_count += 1
              if prev_point:
                  distance += get_distance(prev_point, point)
              prev_point = point
  
          elapsed_time = time.time() - start_time
          return route_guide_pb2.RouteSummary(point_count=point_count,
                                              feature_count=feature_count,
                                              distance=int(distance),
                                              elapsed_time=int(elapsed_time))
  	
      # bidirectionally-streaming method
      def RouteChat(self, request_iterator, context):
          prev_notes = []
          for new_note in request_iterator:
              for prev_note in prev_notes:
                  if prev_note.location == new_note.location:
                      yield prev_note
              prev_notes.append(new_note)
  
  # gRPC서버 실행
  def serve():
      server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
      route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
          RouteGuideServicer(), server)
      server.add_insecure_port('[::]:50051')
      server.start()
      server.wait_for_termination()
  
  
  if __name__ == '__main__':
      logging.basicConfig()
      serve()
  ```



- client 생성하기

  - 구현

  ```python
  # Copyright 2015 gRPC authors.
  #
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """The Python implementation of the gRPC route guide client."""
  
  from __future__ import print_function
  
  import logging
  import random
  
  import grpc
  import route_guide_pb2
  import route_guide_pb2_grpc
  import route_guide_resources
  
  
  def make_route_note(message, latitude, longitude):
      return route_guide_pb2.RouteNote(
          message=message,
          location=route_guide_pb2.Point(latitude=latitude, longitude=longitude))
  
  
  def guide_get_one_feature(stub, point):
      # 동기적으로 실행하기
      feature = stub.GetFeature(point)
      # 비동기적으로 실행
      # feature_future = stub.GetFeature.future(point)
  	# feature = feature_future.result()
      if not feature.location:
          print("Server returned incomplete feature")
          return
  
      if feature.name:
          print("Feature called %s at %s" % (feature.name, feature.location))
      else:
          print("Found no feature at %s" % feature.location)
  
  
  def guide_get_feature(stub):
      guide_get_one_feature(
          stub, route_guide_pb2.Point(latitude=409146138, longitude=-746188906))
      guide_get_one_feature(stub, route_guide_pb2.Point(latitude=0, longitude=0))
  
  # response-streaming RPC
  def guide_list_features(stub):
      rectangle = route_guide_pb2.Rectangle(
          lo=route_guide_pb2.Point(latitude=400000000, longitude=-750000000),
          hi=route_guide_pb2.Point(latitude=420000000, longitude=-730000000))
      print("Looking for features between 40, -75 and 42, -73")
  
      features = stub.ListFeatures(rectangle)
  
      for feature in features:
          print("Feature called %s at %s" % (feature.name, feature.location))
  
  
  def generate_route(feature_list):
      for _ in range(0, 10):
          random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
          print("Visiting point %s" % random_feature.location)
          yield random_feature.location
  
  # request-streaming PRC
  def guide_record_route(stub):
      feature_list = route_guide_resources.read_route_guide_database()
  
      route_iterator = generate_route(feature_list)
      route_summary = stub.RecordRoute(route_iterator)
      print("Finished trip with %s points " % route_summary.point_count)
      print("Passed %s features " % route_summary.feature_count)
      print("Travelled %s meters " % route_summary.distance)
      print("It took %s seconds " % route_summary.elapsed_time)
  
  
  def generate_messages():
      messages = [
          make_route_note("First message", 0, 0),
          make_route_note("Second message", 0, 1),
          make_route_note("Third message", 1, 0),
          make_route_note("Fourth message", 0, 0),
          make_route_note("Fifth message", 1, 0),
      ]
      for msg in messages:
          print("Sending %s at %s" % (msg.message, msg.location))
          yield msg
  
  # bidirectionally-streaming
  def guide_route_chat(stub):
      responses = stub.RouteChat(generate_messages())
      for response in responses:
          print("Received message %s at %s" %
                (response.message, response.location))
  
  
  def run():
      with grpc.insecure_channel('localhost:50051') as channel:
          stub = route_guide_pb2_grpc.RouteGuideStub(channel)
          print("-------------- GetFeature --------------")
          guide_get_feature(stub)
          print("-------------- ListFeatures --------------")
          guide_list_features(stub)
          print("-------------- RecordRoute --------------")
          guide_record_route(stub)
          print("-------------- RouteChat --------------")
          guide_route_chat(stub)
  
  
  if __name__ == '__main__':
      logging.basicConfig()
      run()
  ```





# Pydantic

- 개요
  - 데이터 유효성 검사 및 python type annotation을 사용한 설정 관리를 제공한다.
  - 런타임에 type hint를 적용하고, 데이터가 유효하지 않을 때 사용자에게 에러를 제공한다.
  - 순수하고 표준적인 Python에서 data를 어떻게 다뤄야 하고, 잘 다루고 있는지 검증하고자 할 때 사용한다.



- 설치하기

  - Python 3.6 이상이 요구된다.
  - pip

  ```bash
  $ pip install pydantic
  ```

  - conda

  ```bash
  $ conda install pydantic -c conda-forge
  ```





## Basemodel

- 예시

  - `pydantic`에서 `BaseModel`을 import한다.
  - `BaseModel`을 상속받는 `User` 클래스를 작성한다. 
    - 클래스 내부에는 각 속성들의 type 혹은 기본값을 지정한다.
  - 기본값 없이 type만 지정
    - `id`는 기본값 없이 type만 지정해줬으므로 required 값이 된다.
    - String, floats이 들어오는 경우 int로 변환이 가능하다면 int로 변환된다.
    - 만일 int로 변환이 불가능하다면 exception이 발생한다.
  - type 없이 기본값만 지정
    - `name`은 type 없이 기본값만 지정해줬으므로 optional한 값이 된다.
    - 또한 기본값으로 지정해준 값이 문자열이므로 type은 string이 된다.
  - type과 기본값을 모두 지정
    - `signup_ts`, `friends`는 타입과 기본값을 모두 지정해주었으므로 optional한 값이 된다.
    - `signup_ts`의 경우 `typing.Optional`을 type으로 지정해줬는데, 아무 입력 값이 없을 경우 None을 받게 된다. 따라서, 뒤의 `=None`은 사실 불필요하지만, 입력이 없을 경우 `None`이 들어오게된다는 것을 명시적으로 표현하기 위해 추가해줬다.
    - `friends`의 경우 int가 들어있는 list이므로 만일 string이나 floats이 int로 변환 가능하다면 int로 변환되고, 불가능하다면 exception이 발생한다.
  
  ```python
  from datetime import datetime
  from typing import List, Optional
  from pydantic import BaseModel
  
  
  class User(BaseModel):
      id: int
      name = 'Theo'
      signup_ts: Optional[datetime] = None	# signup_ts: Optional[datetime]와 동일하다.
      friends: List[int] = []
  
  
  external_data = {
      'id': '123',
      'signup_ts': '2019-06-01 12:22',
      'friends': [1, 2, '3'],
  }
  user = User(**external_data)
  print(user.id)
  # 123
  print(repr(user.signup_ts))
  # datetime.datetime(2019, 6, 1, 12, 22)
  print(user.friends)	
  # [1, 2, 3]
  print(user.dict())	
  # {'id': 123, 'signup_ts': datetime.datetime(2019, 6, 1, 12, 22), 'friends': [1, 2, 3], 'name': 'John Doe'}
  ```
  
  - 주의 사항
  
    - field명 앞에 underscore를 붙이면 해당 field는 제외 대상 필드로 지정된다.
  
    > https://docs.pydantic.dev/1.10/usage/models/#automatically-excluded-attributes



- Pydantic의 dict type에 key, value 타입 지정하기

  - 리스트의 첫 번째 요소에 key의 type, 두 번째 요소에 value의 type을 입력한다.

   ```python
  from pydantic import BaseModel
  from typing import Dict
   
  class Foo(BaseModel):
      foo: Dict[str, int]
   ```

  - key 혹은 value의 값을 제한하기
    - Enum을 사용한다.
    - `Element`에 정의된 값만 받게 된다.

  ```python
  from pydantic import BaseModel
  from typing import Dict
  from enum import Enum
    
  class Element(Enum):
      RED="red"
      GREEN="green"
      YELLOW="yellow"
    
  class Foo(BaseModel):
      foo: Dict[str, Element]
  ```



- List  element들의 유효성 검증하기

  - 아래와 같이 배열에 일정한 값들이 담겨서 와야 할 때가 있다.

  ```json
  {
      "fruits":["apple", "orange", "banana"]
  }
  ```

  - 아래와 같이 model을 정의한다.
    - 정의한 배열에 있는 요소가 요청에서 빠져 있어도 유효한 것으로 판단한다.
    - 그러나 배열에 없는 요소가 요청으로 들어올 경우 유효하지 않은 것으로 판단한다.

  ```python
  from pydantic import BaseModel
  from typing import List, Optional, Literal
  
  
  class Fruit(BaseModel):
      fruits: Optional[List[Literal['apple', 'orange', 'banana']]]
  ```



- Enum class 사용하기

  - `use_enum_values`를 `True`로 주면, 자동으로 Enum 클래스의 value를 할당한다.

  ```python
  from enum import Enum
  from pydantic import BaseModel
  
  class Gender(str, Enum):
      MALE = "male"
      FEMALE = "female"
  
  class Student(BaseModel):
      name:str
      gender:Gender
  
      class Config:  
          use_enum_values = True
  
  student = Student(name="Kim", gender='male')
  print(student.dict())
  ```




- Pydantic model의 기본값

  - 만일 아래와 같이 다른 pydantic model을 field의 type으로 갖을 경우, 해당 field의 기본 값을 None으로 설정하면, 기존 field의 기본값은 무시된다.
    - 만일 기본값이 적용된다면 `foo=Foo(a=1, b='Hello')`가 출력되겠지만 기본값이 무시되므로 `foo=None`가 출력된다.

  ```python
  from pydantic import BaseModel
  
  # Bar model의 foo field의 기본값이 None이므로, Foo model의 기본값들은 무시된다.
  class Foo(BaseModel):
      a: int = 1
      b: str = "Hello"
  
  class Bar(BaseModel):
      foo: Foo = None
  
  bar = Bar()
  print(bar)	# foo=None
  ```

  - 따라서 기본값을 적용하고 싶다면 아래와 같이 Foo model의 인스턴스를 생성한 뒤 기본값으로 설정해준다.

  ```python
  from pydantic import BaseModel
  
  
  class Foo(BaseModel):
      a: int = 1
      b: str = "Hello"
  
  class Bar(BaseModel):
      foo: Foo = Foo()
  
  
  bar = Bar()
  print(bar)	# foo=Foo(a=1, b='Hello')
  ```




- Alias를 설정 가능하다.

  - 방법1. `Field`를 사용

  ```python
  from pydantic import Field, BaseModel
  
  
  class Person(BaseModel):
      name: str =  Field("John", alias="first_name")
  
  
  person = Person(**{"first_name":"Harry"})
  print(person)	# name='Harry'
  ```

  - 방법2. `Config.fields`를 사용

  ```python
  from pydantic import Field, BaseModel
  
  
  class Person(BaseModel):
      name: str = "John"
  
      class Config:
          fields = {"name":"first_name"}
  
  
  person = Person(**{"first_name":"Harry"})
  print(person)	# name='Harry'
  ```

  - 방법3. alias_generator를 사용
    - snake_case를 PascalCase로 바꿀 때 처럼 일괄적으로 바꿔야 할 때 유용하다.

  ```python
  from pydantic import Field, BaseModel
  
  
  class Person(BaseModel):
      first_name: str
      last_name: str
  
      class Config:
          @classmethod
          def alias_generator(cls, string: str) -> str:
              return ''.join(word.capitalize() for word in string.split('_'))
  
  
  person = Person(**{"FirstName":"Harry", "LastName":"Porter"})
  print(person)	# first_name='Harry' last_name='Porter'
  ```

  - alias를 적용한 대로 데이터를 보고 싶을 경우 아래와 같이 `by_alias=True`를 준다.

  ```python
  from pydantic import Field, BaseModel
  
  
  class Person(BaseModel):
      first_name: str
      last_name: str
  
      class Config:
          @classmethod
          def alias_generator(cls, string: str) -> str:
              return ''.join(word.capitalize() for word in string.split('_'))
  
  
  person = Person(**{"FirstName":"Harry", "LastName":"Porter"})
  print(person.dict(by_alias=True))	# {'FirstName': 'Harry', 'LastName': 'Porter'}
  ```

  - alias를 설정하면 기존 field 명은 사용할 수 없게 되는데 아래와 같이 설정하면 둘 다 사용 가능하다.

  ```python
  from pydantic import Field, BaseModel, ConfigDict
  
  
  class Person(BaseModel):
      name: str =  Field("John", alias="first_name")
  
      model_config = ConfigDict(
          populate_by_name=True
      )
  
  
  person = Person(**{"name":"Harry"})
  print(person)	# name='Harry'
  ```



- Basemodel로 선언한 field들의 기본값은 최초 1회만 초기화된다.

  - 이로 인해 예상치 못 한 결과가 나올 수 있다.
    - 아래 예시와 같이, 객체가 생성된 시간을 default 값으로 가져야 하는 class를 선언한 경우 예상치 못한 결과가 나올 수 있다.

  ```python
  import time
  from datetime import datetime
  
  from pydantic import BaseModel
  
  
  class Foo(BaseModel):
      my_time: datetime = datetime.now()
  
  
  
  foo1 = Foo()
  time.sleep(3)
  foo2 = Foo()
  print(foo1.my_time == foo2.my_time)		# True
  ```

  - `default_factory`를 사용하면 해결이 가능하다.
    - `Field` class의 `default_factory` argument에 객체를 생성하는 함수를 넘기면, pydantic 객체가 생성될 때 마다 default 값을 새로 생성한다.

  ```python
  import time
  from datetime import datetime
  
  from pydantic import BaseModel, Field
  
  
  class Foo(BaseModel):
      my_time: datetime = Field(default_factory=datetime.now)
  
  
  
  foo1 = Foo()
  time.sleep(3)
  foo2 = Foo()
  print(foo1.my_time == foo2.my_time)		# False
  ```



- 자기 자신을 참조하는 모델 정의하기

  - 개발을 하다보면 재귀적인 모델이 필요할 때가 있다.
    - 예를 들어 elasticsearch의 aggregaion은 하나의 aggregation 하위에 다른 aggregation이 올 수 있다.
    - 이를 모델로 정의하려면 재귀가 필요하다.
  - 모델명을 작은 따옴표로 감싸면 된다.

  ```python
  from pydantic import Basemodel
  from typing import Union
  
  
  class BucketAggregation(Basemodel):
      pass
  
  
  class MetricAggregation(Basemodel):
      pass
  
  
  class Aggregation(Basemodel):
      aggregation: Union[BucketAggregation, MetricAggregation]
      sub: 'Aggregation' = None
  ```



- Required, optional, nullable fields

  - Pydantic V2부터 `Optional` annotator를 사용했을 때의 로직이 변경되었다.
    - 이전까지는 `Optional`을 사용하면 해당 field는 문자 그대로 optional한 field가 되었다.
    - 그러나 V2부터는 `Optional`을 사용하더라도 required field가 된다.
    - V2 기준으로 optional한 값이 되게하려면 기본값을 줘야한다.
  - `Optional`의 의미
    - `Optional[T]`은 `Union[T, None]`과 동일하다.
    - 즉. `Optional[T]`는 해당 field가 T type이며, None이 될 수도 있다는 것을 의미한다.

  - `Optional`과 기본값에 따른 필드 정의는 아래와 같다.

  | State                                                       | Field Definition          |
  | ----------------------------------------------------------- | ------------------------- |
  | Required, cannot be `None`                                  | f1: str                   |
  | Not required, cannot be `None`, is "abc" by default         | f2: str = "abc"           |
  | Not required, can be `None`(implicit), is `None` by default | f3: str = None            |
  | Required, can be `None`                                     | f4: Optional[str]         |
  | Not required, can be `None`, is `None` by default           | f5: Optional[str] = None  |
  | Not required, can be `None`, is "abc" by default            | f6: Optional[str] = "abc" |
  | Required, can be any type (including `None`)                | f7: Any                   |
  | Not required, can be any type (including `None`)            | f8: Any = None            |

  - `str = None`과 `Optional[str] = None`의 차이
    - 둘 다 기능적으로는 동일하게 동작하지만, 아래와 같은 차이가 있다.
    - 엄밀히 말해서 `f1`의 경우 사실은 None이 될 수 없다.
    - 그러나 dynamic typing을 지원하는 Python의 특성상 None도 할당 가능한 것이다.

  ```python
  from pydantic import BaseModel
  from typing import Optional
  
  
  class Foo(BaseModel):
      f1: str = None
      f2: Optional[str] = None
  
  for field in Foo.model_fields.values():
      print(repr(field))
      
  """
  FieldInfo(annotation=str, required=False, default=None)
  FieldInfo(annotation=Union[str, NoneType], required=False, default=None)
  """
  ```

  - 그럼 `str = None`과 `Optional[str] = None` 중 어떤 방식을 사용해야 하는가?
    - Zen of Python에는 "암시적인 것 보다는 명시적인 것이 낫다(Explicit is better than implicit.)"는 항목이 있다.
    - 따라서 None이 될 수 있음을 보다 명시적으로 표현하는 `Optional[str] = None`를 사용하는 것이 더 나을 것 같다.





## Validator

- `Annotated`를 사용하여 validator를 설정할 수 있다.

  - 아래와 같이 설정한다.

  ```python
  from typing import Any, List, Annotated
  
  from pydantic import BaseModel, ValidationError
  from pydantic.functional_validators import AfterValidator
  
  # validation 함수1
  def check_squares(v: int) -> int:
      assert v**0.5 % 1 == 0, f'{v} is not a square number'
      return v
  
  # validation 함수2
  def double(v: Any) -> Any:
      return v * 2
  
  # validation 함수를 포함하여 type을 선언한다.
  MyNumber = Annotated[int, AfterValidator(double), AfterValidator(check_squares)]
  
  
  class DemoModel(BaseModel):
      number: List[MyNumber]
  
  
  print(DemoModel(number=[2, 8]))
  try:
      DemoModel(number=[2, 4])
  except ValidationError as e:
      print(e)
  ```

  - Validator function의 종류
    - `AfterValidator`: Pydantic의 내부 parsing이 완료된 후에 validator가 실행된다.
    - `BeforeValidator`: Pydantic의 내부 parsing이 실행되기 전에 validator가 실행된다.
    - `PlainValidator`: `mode='before'`와 같이 실행한 것과 유사하지만, Pydantic이 추가적인 내부 validation을 실행하지는 않는다.
    - `WrapValidator`: Pydantic이 내부 로직을 실행하기 전과 후에 모두 실행할 수 있는 validator이다.
    - 여러 개의 before, after, wrap validator를 사용할 수 있지만, `PlainValidator`는 오직 하나만 사용할 수 있다.
  - Validation 순서는 `Annotated`내에 작성한 순서에 따라 결정된다.
    - 먼저 before와 wrap validator가 뒤에서 앞으로 실행된다.
    - 그 후 after validator가 앞에서 뒤로 실행된다.

  ```python
  from typing import Any, Callable, List, cast, Annotated, Annotated
  
  from typing_extensions import TypedDict
  
  from pydantic import (
      AfterValidator,
      BaseModel,
      BeforeValidator,
      ValidationInfo
  )
  from pydantic.functional_validators import field_validator
  
  
  class Context(TypedDict):
      logs: List[str]
  
  
  def make_validator(label: str) -> Callable[[Any, ValidationInfo], Any]:
      def validator(v: Any, info: ValidationInfo) -> Any:
          context = cast(Context, info.context)
          context['logs'].append(label)
          return v
  
      return validator
  
  
  class A(BaseModel):
      x: Annotated[
          str,
          BeforeValidator(make_validator('before-1')),
          AfterValidator(make_validator('after-1')),
          BeforeValidator(make_validator('before-2')),
          AfterValidator(make_validator('after-2')),
          BeforeValidator(make_validator('before-3')),
          AfterValidator(make_validator('after-3')),
          BeforeValidator(make_validator('before-4')),
          AfterValidator(make_validator('after-4')),
      ]
  
      val_x_before = field_validator('x', mode='before')(
          make_validator('val_x before')
      )
      val_x_after = field_validator('x', mode='after')(
          make_validator('val_x after')
      )
  
  
  context = Context(logs=[])
  
  A.model_validate({'x': 'abc', 'y': 'def'}, context=context)
  for log in context['logs']:
      print(log)
   
  """
  val_x before
  before-4
  before-3
  before-2
  before-1
  after-1
  after-2
  after-3
  after-4
  val_x after
  """
  ```



- Model validator

  - `@model_validator`를 사용하면 전체 model을 validation 할 수 있다.
    - `@model_validator`를 추가한 method는 self instance를 반환해야한다(단, `mode`에 따라 달라질 수 있다).
    - 자식 class에서 부모 클래스의 `@model_validator` method를 사용할 수 있으며, 오버라이딩도 가능하다.
  - `mode`에 따라 달라지는 것들이 있다.
    - `mode='before'`일 경우 validator method는 class method여야 하며, 첫 번째 인자는 class 자체를 받는다.
    - `mode='after'`일 경우 validator method의 첫 번째 인자로 self를 받으며, 반드시 self를 반환해야한다.

  ```python
  from typing import Any
  
  from typing_extensions import Self
  
  from pydantic import BaseModel, ValidationError, model_validator
  
  
  class UserModel(BaseModel):
      username: str
      password1: str
      password2: str
  
      @model_validator(mode='before')
      @classmethod
      def check_card_number_omitted(cls, data: Any) -> Any:
          if isinstance(data, dict):
              assert (
                  'card_number' not in data
              ), 'card_number should not be included'
          return data
  
      @model_validator(mode='after')
      def check_passwords_match(self) -> Self:
          pw1 = self.password1
          pw2 = self.password2
          if pw1 is not None and pw2 is not None and pw1 != pw2:
              raise ValueError('passwords do not match')
          return self
  
  
  print(UserModel(username='scolvin', password1='zxcvbn', password2='zxcvbn'))
  
  try:
      UserModel(username='scolvin', password1='zxcvbn', password2='zxcvbn2')
  except ValidationError as e:
      print(e)
  try:
      UserModel(
          username='scolvin',
          password1='zxcvbn',
          password2='zxcvbn',
          card_number='1234',
      )
  except ValidationError as e:
      print(e)
  ```





### 특정 field를 validation하기(Pydantic 2.0 미만)

- 특정 field를 validation하기(Pydantic 2.0 이전)

  - Pydantic에서 제공하는 `@validator` 데코레이터를 사용한다.
    - 첫 번째 인자로는 class 자체를 받는다.
    - 두 번째 인자는 검증 대상 필드를 받는다.
    - 그 밖에 field 정보와 config 정보를 받는다.

  ```python
  from pydantic import BaseModel, ValidationError, validator
  
  
  class UserModel(BaseModel):
      name: str
      username: str
      password1: str
      password2: str
  
      @validator('name')
      def name_must_contain_space(cls, v):
          if ' ' not in v:
              raise ValueError('must contain a space')
          return v.title()
  
      @validator('username')
      def username_alphanumeric(cls, v):
          assert v.isalnum(), 'must be alphanumeric'
          return v
      
      @validator('password2')
      def passwords_match(cls, v, values, **kwargs):
          if 'password1' in values and v != values['password1']:
              raise ValueError('passwords do not match')
          return v
  
  
  try:
      UserModel(
          name='samuel',
          username='scolvin',
          password1='zxcvbn',
          password2='zxcvbn2',
      )
  except ValidationError as e:
      print(e)
  ```
  
  - 주의할 점은 값이 주어지지 않을 경우 해당 field는 validation을 하지 않는다는 점이다.
    - 이는 성능상의 이유 때문으로, 굳이 값이 주어지지 않은 field를 대상으로 validation을 할 필요가 없기 때문이다.
    - 값이 주어지지 않더라도 validation을 해야한다면 아래와 같이 `always`를 `True`로 주면 된다.
  
  ```python
  class DemoModel(BaseModel):
      ts: datetime = None
  
      @validator('ts', pre=True, always=True)
      def set_ts_now(cls, v):
          return v or datetime.now()
  ```



- Pydantic validator 재사용하기

  - pydantic에서  한 class 내의 validation 함수 이름은 중복될 수 없다.
  - 두 개의 필드에 대해서 `change_to_str`라는 같은 이름의 validation 함수를 사용하면 error가 발생한다.

  ```python
  from datetime import date
    
    
  class MyRange(pyd.BaseModel):
      gte:date
      lte:date
  
      @pyd.validator('gte')
      def change_to_str(cls, v):
          return v.strftime('%Y-%m-%d')
  
      @pyd.validator('lte')
      def change_to_str(cls, v):
          return v.strftime("%Y-%m-%d")
  ```

  - 아래와 같이 여러 field명을 넣으면 된다.

  ```python
  from datetime import date
    
    
  class MyRange(pyd.BaseModel):
      gte:date
      lte:date
  
      @pyd.validator('gte', 'lte')
      def change_to_str(cls, v):
          return v.strftime('%Y-%m-%d')
  ```
  
  - 위와 같이 정확히 동일하게 동작하는 validate을 여러 필드에 해줘야 할 경우
  
  ```python
  from datetime import date, timedelta
  from pydantic import BaseModel, validator
  
  def change_to_str(date_param: date) -> str:
      return date_param.strftime("%Y-%m-%d")
  
  class MyRange(BaseModel):
      gte:date
      lte:date
  
      str_gte = validator('gte', allow_reuse=True)(change_to_str)
      str_lte = validator('lte', allow_reuse=True)(change_to_str)
  
  my_range = MyRange(gte=date.today()-timedelta(days=1), lte=date.today())
  print(my_range.gte)		# 2022-03-04
  print(my_range.lte)		# 2022-03-05
  ```
  
  - class 내의 모든 field에 하나의 validation 적용하기
    - class 내의 모든 field에 하나의 validation 적용하기
  
  ```python
  from datetime import date, timedelta
  from pydantic import BaseModel, root_validator
  
  
  class MyRange(BaseModel):
      gte:date
      lte:date
  
      @root_validator
      def change_to_str(cls, values):
          return {key:value.strftime("%Y-%m-%d") for key,value in values.items()}
  ```



- `ValidationError`

  - 만일 class에서 설정해준 타입이 들어오지 않을 경우 pydantic 패키지에 포함된 `ValidationError`가 발생하게 된다.

  ```python
  from pydantic import ValidationError
  
  try:
      User(signup_ts='broken', friends=[1, 2, 'not number'])
  except ValidationError as e:
      print(e.json())
  ```

  - output
    - `ValidationError`에는 에러가 발생한 위치, message, type 등이 담겨 있다.
    - list의 경우 `loc` 에는 몇 번째 인덱스에서 문제가 생긴 것인지도 담겨 있다. 

  ```json
  [
    {
      "loc": [
        "id"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "signup_ts"
      ],
      "msg": "invalid datetime format",
      "type": "value_error.datetime"
    },
    {
      "loc": [
        "friends",
        2
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
  ```





### 특정 field를 validation하기(Pydantic 2.0 이상)

- `field_validator`를 사용한다.

  - Pydantic 2.0 version 이전에는 특정 field를 validation하는데 `validator`를 사용했다.
  - 그러나 Pydantic 2.0부터는 `validator` 대신 `field_valudator`를 사용한다.
    - 사용법은 `validator`와 유사하다.

  ```python
  from typing_extensions import Annotated
  
  from pydantic import BaseModel, Field, field_validator
  
  
  class Model(BaseModel):
      x: str = 'abc'
      y: str = 'def'
  
      @field_validator('x', 'y')
      @classmethod
      def double(cls, v: str) -> str:
          return v * 2
  ```

  - `field_validator` 사용시 주의할 사항
    - `@field_validator`는 class method이므로 첫 번째 argument로는 class의 instacne가 아니라 class 자체를 받는다.
    - 따라서 적절한 type checking을 위해 `@field_Validator` 아래에 `@classmethod` decorator를 두는 것이 권장된다.
    - 두 번째 argument는 validation할 field가 온다.
    - 세 번째 argument는 정의하지 않아도 되지만, 정의할 경우 `pydantic.ValidationInfo`의 instance가 온다.
    - Validator는 value를 반환하거나 `ValueError` 혹은 `AssertionError`를 raise해야한다.
    - 하나의 validator에 여러 field name을 전달하여 여러 field를 validation하는 데 사용할 수 있다.
    - Field를 지정할 때 `"*"`와 같이 입력하여 모든 field를 하나의 validator로 validation할 수 있다.

  - `validate_default` 
    - 기본적으로 `Annotated`를 사용한 validator나 `field_validator`를 사용한 validator 모두 기본값에 대해서는 validation을 하지 않는다.
    - 만약 기본값에 대해서도 validation을 하고자 한다면 반드시 `validate_default`값을 True로 설정해야한다.

  ```python
  from typing_extensions import Annotated
  
  from pydantic import BaseModel, Field, field_validator
  
  
  class Model(BaseModel):
      x: str = 'abc'
      y: Annotated[str, Field(validate_default=True)] = 'xyz'
  
      @field_validator('x', 'y')
      @classmethod
      def double(cls, v: str) -> str:
          return v * 2
  
  ```










# pyinstaller

> https://pyinstaller.org/en/stable/

- pyinstaller

  - Python script를 실행할 수 있는 파일로 변환해주는 패키지다.
  - 설치

  ```bash
  $ pip install pyinstaller
  ```



- 명령어

  ```bash
  $ pyinstaller [options] <변환할 Python script 경로>
  ```



- 옵션

  > https://pyinstaller.org/en/stable/usage.html#options 모든 옵션은 여기서 확인하면 된다.

  - `--dispath`
    - output을 생성할 경로를 지정한다.
    - 기본값은 `./dist`
  - `-F`, `--onefile`
    - 하나의 파일만 생성한다.
  - `-n`, `--name`
    - 실행 파일의 이름을 지정한다.
    - 기본 값은 script이름으로 설정된다.
  - `-w`, `--windowed`, `--noconsole`
    - console 창을 띄우지 않고 실행한다.





# 문장 분리

- kss(Korean Sentence Splitter, 한글 문장 분리기)

  - C++로 작성되어 Python과 C++에서 사용이 가능하다.
  - 설치

  ```bash
  $ pip install kss
  ```

  - 실행

  ```python
  import kss
  
  s = input()
  
  for sen in kss.split_sentences(s):
      print(sen)
  ```



- Kiwipiepy

  - 한국어 형태소 분석기인 Kiwi(Korean Intelligent Word Identifier)의 Python 모듈이다.
    - 문장 분리 기능뿐 아니라, 형태소 분석을 위한 다양한 기능을 제공한다.
  - C++로 작성되었으며, Python 3.6이상이 필요하다.
  - 설치

  ```bash
  $ pip install Kiwipiepy
  ```

  - 실행

  ```python
  from kiwipiepy import Kiwi
  
  s = input()
  kiwi = Kiwi()
  
  for sen in kiwi.split_into_sents(s):
      print(sen)
  ```

  - kss와 비교
    - kss에 비해 Kiwipiepy의 속도가 더 빠르다.
    - 심도 있는 테스트를 해 본 것은 아니지만, 몇 몇 문장을 테스트 해 본 결과 Kiwipiepy가 보다 문장을 잘 분리하는 것 처럼 보인다.

  ``` python
  from kiwipiepy import Kiwi
  import kss
  
  s = input()
  kiwi = Kiwi()
  print("-"*100)
  for sen in kiwi.split_into_sents(s):
      print(sen)
  
  for sen in kss.split_sentences(s):
      print(sen)
  
  # 테스트 문장
  """
  강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다. 회사 동료 분들과 다녀왔는데 분위기도 좋고 음식도 맛있었어요 다만, 강남 토끼정이 강남 쉑쉑버거 골목길로 쭉 올라가야 하는데 다들 쉑쉑버거의 유혹에 넘어갈 뻔 했답니다 강남역 맛집 토끼정의 외부 모습. 강남 토끼정은 4층 건물 독채로 이루어져 있습니다. 역시 토끼정 본 점 답죠?ㅎㅅㅎ 건물은 크지만 간판이 없기 때문에 지나칠 수 있으니 조심하세요 강남 토끼정의 내부 인테리어. 평일 저녁이었지만 강남역 맛집 답게 사람들이 많았어요. 전체적으로 편안하고 아늑한 공간으로 꾸며져 있었습니다ㅎㅎ 한 가지 아쉬웠던 건 조명이 너무 어두워 눈이 침침했던… 저희는 3층에 자리를 잡고 음식을 주문했습니다. 총 5명이서 먹고 싶은 음식 하나씩 골라 다양하게 주문했어요 첫 번째 준비된 메뉴는 토끼정 고로케와 깻잎 불고기 사라다를 듬뿍 올려 먹는 맛있는 밥입니다. 여러가지 메뉴를 한 번에 시키면 준비되는 메뉴부터 가져다 주더라구요. 토끼정 고로케 금방 튀겨져 나와 겉은 바삭하고 속은 촉촉해 맛있었어요! 깻잎 불고기 사라다는 불고기, 양배추, 버섯을 볶아 깻잎을 듬뿍 올리고 우엉 튀김을 곁들여 밥이랑 함께 먹는 메뉴입니다. 사실 전 고기를 안 먹어서 무슨 맛인지 모르겠지만.. 다들 엄청 잘 드셨습니다ㅋㅋ 이건 제가 시킨 촉촉한 고로케와 크림스튜우동. 강남 토끼정에서 먹은 음식 중에 이게 제일 맛있었어요!!! 크림소스를 원래 좋아하기도 하지만, 느끼하지 않게 부드럽고 달달한 스튜와 쫄깃한 우동면이 너무 잘 어울려 계속 손이 가더라구요. 사진을 보니 또 먹고 싶습니다 간사이 풍 연어 지라시입니다. 일본 간사이 지방에서 많이 먹는 떠먹는 초밥(지라시스시)이라고 하네요. 밑에 와사비 마요밥 위에 연어들이 담겨져 있어 코끝이 찡할 수 있다고 적혀 있는데, 난 와사비 맛 1도 모르겠던데…? 와사비를 안 좋아하는 저는 불행인지 다행인지 연어 지라시를 매우 맛있게 먹었습니다ㅋㅋㅋ 다음 메뉴는 달짝지근한 숯불 갈비 덮밥입니다! 간장 양념에 구운 숯불 갈비에 양파, 깻잎, 달걀 반숙을 터트려 비벼 먹으면 그 맛이 크.. (물론 전 안 먹었지만…다른 분들이 그렇다고 하더라구요ㅋㅋㅋㅋㅋㅋㅋ) 마지막 메인 메뉴 양송이 크림수프와 숯불떡갈비 밥입니다. 크림리조또를 베이스로 위에 그루통과 숯불로 구운 떡갈비가 올라가 있어요! 크림스튜 우동 만큼이나 대박 맛있습니다…ㅠㅠㅠㅠㅠㅠ (크림 소스면 다 좋아하는 거 절대 아닙니다ㅋㅋㅋㅋㅋㅋ) 강남 토끼정 요리는 다 맛있지만 크림소스 요리를 참 잘하는 거 같네요 요건 물만 마시기 아쉬워 시킨 뉴자몽과 밀키소다 딸기통통! 유자와 자몽의 맛을 함께 느낄 수 있는 뉴자몽은 상큼함 그 자체였어요. 하치만 저는 딸기통통 밀키소다가 더 맛있었습니다ㅎㅎ 밀키소다는 토끼정에서만 만나볼 수 있는 메뉴라고 하니 한 번 드셔보시길 추천할게요!! 강남 토끼정은 강남역 맛집답게 모든 음식들이 대체적으로 맛있었어요! 건물 위치도 강남 대로변에서 조금 떨어져 있어 내부 인테리어처럼 아늑한 느낌도 있었구요ㅎㅎ 기회가 되면 다들 꼭 들러보세요~ 🙂
  """
  ```




## tqdm

- tqdm

  - python 코드를 실행 했을 때 진행 상황을 볼 수 있는 모듈이다.
    - 실행에 오랜 시간이 걸리는 코드의 경우 중간에 print나 logging 모듈로 로그를 남기는 방식을 사용하기도 한다.
    - tqdm은 print나 logging 모듈 없이도 진행 상황을 확인하게 도와준다.




- 설치

  ```bash
  $ pip install tqdm
  ```




- 사용

  - iterable을 tqdm에 넘겨 사용한다.

  ```python
  import time
  from tqdm import tqdm
  
  
  def long_time_job():
      time.sleep(0.1)
  
  for i in tqdm(range(100)):
      long_time_job()
  ```

  - 결과

  ```bash
  $ python main.py 
  74%|████████████████████████████████████████████████████████████████████████████████████████████████▉              | 74/100 [00:07<00:02,  9.49it/s]
  ```



# Streamlit

> https://github.com/streamlit/streamlit

- Python을 활용하여 web UI를 생성하게 해주는 library, cloud service



- 설치 및 실행

  - Python 3.7 이상이 필요하다.
    - numpy, pandas 등도 함께 설치된다.

  ```bash
  $ pip install streamlit
  ```

  - 설치 확인

  ```bash
  $ streamlit hello
  ```

  - 실행
    - streamlit script를 실행시키려면 아래와 같이 입력하면 된다.

  ```bash
  $ streamlit run <script>
  
  # 혹은 아래와 같이 해도 된다.
  $ python -m streamlit run <script>
  ```



- Streamlit의 특징
  - Script의 수정사항을 app에 적용하려면, 전체 script를 재실행해야한다.
    - 자동으로 재실행 되도록 할 수도 있고, 사용자가 수동으로 재실행 할 수도 있다.
  - 자동으로 재실행 되도록 할 경우, 사용자가 script를 수정하고 저장하면, app이 자동으로 script 전체를 재실행하여 변경 사항을 app에 반영한다.
  - 만일 대량의 data를 받아와야 하는 등 리소스를 많이 필요로하는 logic이 있을 경우, 이는 문제가 될 수 있다.
    - script의 수정이 생길 때 마다 대량의 data를 다시 받아와야하기 때문이다.
    - Streamlit은 이를 위해 cache 기능을 제공한다.



- Streamlit cache의 동작 방식

  - `cache` annotation을 추가한 함수가 호출 될 때 아래 3가지를 체크하게 된다.
    - 함수의 bytecode(함수의 변경 여부 확인).
    - 함수가 의존하고 있는 code, 변수, 파일(함수가 의존하고 있는 것들의 변경 여부 확인).
    - 함수를 호출할 때 넘긴 parameter.
  - 함수를 호출할 경우
    - 만일 위 세 가지 중 하나로도 이전과 달라졌거나, 함수가 처음 호출되는 것이라면, 함수는 정의된 logic을 수행하고, data를 local cache에 저장한다.
    - 만일 함수가 처음 호출 된 것이 아니고, 위 세 가지가 이전과 정확히 동일하다면, 함수의 실행을 하지 않고, local cache에 저장된 data를 가져온다.
  - 한계
    - Streamlit은 오직 working directory의 변경 사항만을 파악한다. 따라서, 만일 working directory 외부의 변경 사항이 있다면, 이를 알아채지 못한다. 예를 들어 사용중인 library를 upgrade 했는데, 해당 library가 저장된 위치가 실행 중인 streamlit app의 working directory가 아니라면, 변경사항이 있음에도 cache가 그대로 적용된다.
    - 만일 cache annotation이 붙은 함수가 반환하는 값이 무선적인 값이거나, 외부에서 받아오는 값이 변경되어도, 위 세 가지가 변경되지 않았으므로, cache된 값을 그대로 반환한다.
    - cache된 함수가 반환한 값은 참조에 의해 저장되기 전 까지는 수정되선 안된다(성능상의 문제와 다른 library와의 호환성 문제로 막아뒀다).

  



- App 생성해보기

  - 필요한 package들을 import 해준다.

  ```python
  import streamlit as st
  import pandas as pd
  import numpy as np
  ```

  - app의 제목을 추가한다.
    	`st.title` method를 사용한다.

  ```python
  st.title("My first Streamlit app")
  ```

  - App에 띄워줄 data를 받아온다.
    - AWS S3에 저장되어 있는 Uber의 정보를 받아오는 code이다.
    - Data를 받아와서 pandas의 dataframe에 넣고, string type인 date column의 값을 datetime으로 변환한다.

  ```python
  DATE_COLUMN = 'date/time'
  DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
           'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
  
  def load_data(nrows):
      data = pd.read_csv(DATA_URL, nrows=nrows)
      lowercase = lambda x: str(x).lower()
      data.rename(lowercase, axis='columns', inplace=True)
      data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
      return data
  
  # data가 로딩 중이라는 text를 띄운다.
  data_load_state = st.text('Loading data...')
  # 10000 줄의 data를 받아온다.
  data = load_data(10000)
  # data를 받아오면, data 로딩이 끝났다는 것을 알려주는 text를 띄운다.
  data_load_state.text('Loading data...done!')
  ```

  - Cache 적용하기
    - Streamlit의 특성상, script에 수정사항이 있을 때 마다 전체 script를 재실행한다.
    - 따라서 위 script의 경우, 수정사항이 생길 때 마다 data를 계속 받아오게 된다.
    - 이를 막기 위해 cache를 추가해준다.

  ```python
  # cache decorator를 추가해주기만 하면 된다.
  @st.cache
  def load_data(nrows):
  ```

  - 받아온 data 확인하기
    - `subheader`를 통해 소제목을 설정하고 `text`를 통해 data를  rendering한다.
    - `write` 메서드는 data type에 가장 적합한 방식을 선택하여 data를 보여준다.

  ```python
  st.subheader('Raw data')
  st.write(data)
  ```

  - histogram 생성하기
    - `bar_chart` 메서드를 사용한다.

  ```python
  # 소제목을 추가하고
  st.subheader('Number of pickups by hour')
  
  # 시간별로 분류된 histogram을 생성한다.
  hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
  
  # histogram을 rendering한다.
  st.bar_chart(hist_values)
  ```

  - 지도에서 data 확인하기
    - `map` 메서드를 사용한다.

  ```python
  st.subheader('Map of all pickups')
  
  st.map(data)
  ```

  - filter 추가하기
    - filter를 추가하여 시간대 별로 filtering 된 결과를 보고 싶다면 아래와 같이 수정하면 된다.

  ```python
  hour_to_filter = st.slider('hour', 0, 23, 17)
  filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
  st.subheader('Map of all pickups at %s:00' % hour_to_filter)
  st.map(filtered_data)
  ```

  - checkbox 추가하기
    - 만일 checkbox에 따라 특정 내용이 보이게 하고 싶으면 아래와 같이 하면 된다.

  ```python
  if st.checkbox('Show raw data'):
      st.subheader('Raw data')
      st.write(data)
  ```



- 예시1. elasticsearch를 활용한 검색 demo page 만들기

  ```python
  import streamlit as st
  import pandas as pd
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("localhost:9200")
  
  def search(title):
      body = {
          "query":{
              "match_all":{}
          },
          "size":5
      }
      res = es_client.search(index="my_index", body=body)["hits"]["hits"]
      return [doc["_source"] for doc in res]
  
  
  st.title("Search Demo Page")
  
  title = st.text_input('검색어를 입력하세요.')
  
  if title:
      st.write(search(title))
  ```

  



