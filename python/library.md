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



- 예시

  - `pydantic`에서 `BaseModel`을 import한다.
  - `BaseModel`을 상속받는 `User` 클래스를 작성한다. 
    - 클래스 내부에는 각 속성들의 type 혹은 기본값을 지정한다.
  - 기본값 없이 type만 지정
    - id는 기본값 없이 type만 지정해줬으므로 required 값이 된다.
    - String, floats이 들어오는 경우 int로 변환이 가능하다면 int로 변환된다.
    - 만일 int로 변환이 불가능하다면 exception이 발생한다.
  - type 없이 기본값만 지정
    - name은 type 없이 기본값만 지정해줬으므로 optional한 값이 된다.
    - 또한 기본값으로 지정해준 값이 문자열이므로 type은 string이 된다.
  - type과 기본값을 모두 지정
    - signup_ts, friends는 타입과 기본값을 모두 지정해주었으므로 optional한 값이 된다.
    - friends의 경우 int가 들어있는 list이므로 만일 string이나 floats이 int로 변환 가능하다면 변환되게 되고, 불가능하다면 exception이 발생한다.

  ```python
  from datetime import datetime
  from typing import List, Optional
  from pydantic import BaseModel
  
  
  class User(BaseModel):
      id: int
      name = 'Theo'
      signup_ts: Optional[datetime] = None
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



- pydantic의 Dict type에 key, value 타입 지정하기

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



- validation하기

  - pydantic에서 제공하는 `@validator` 데코레이터를 사용한다.
    - 첫 번째 인자로는 class 자체를 받는다.
    - 두 번째 인자는 검증 대상 필드를 받는다.
    - 세 번째 인자는 검증 대상 필드를 제외한 다른 필드들의 정보를 받는다.

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



- pydantic validator 재사용하기

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




- pydantic model의 기본값

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

  

  





