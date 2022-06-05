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

  



