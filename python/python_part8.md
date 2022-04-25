# Testing

## Test in Python

- Python에서 널리 사용되는 test 라이브러리에는 아래와 같은 것들이 있다.
  - pytest
  - unittiest



- pytest
  - Flask, Requests, pip에서 사용중이다.
  - 장점
    - unitest가 지원하지 않는 고급 기능을 많이 제공한다.
  - 단점
    - 일반적인 Python의 코드 흐름과 다른, pytest만의 독자적인 방식을 사용하기에 pylint 등의 코드 분석 툴이 에러로 감지할 수 있다.



- unittiest
  - Python 자체의 테스트 및 Django에서 사용중이다.
  - 장점
    - Python 기본 내장 라이브러리로 별도 설치가 필요 없다.
    - 다른 언어의 테스트 툴과 거의 사용법이 유사하다(Java의 JUnit이라는 테스트 프레임워크로부터 강한 영향을 받았다).
  - 단점
    - 테스트 코드를 작성하기 위해 반드시 클래스를 정의해야 하므로 코드가 장황해질 수 있다.
    - 보일러 플레이트 코드가 많아진다는 단점이 있다(매번 클래스를 생성하고, unitest를 상속 받아야 한다).
    - 테스트를 위한 메서드들이 모두 캐멀 케이스이다.



## 용어

- test double
  - 실제 객체를 대신해서 테스팅에서 사용하는 모든 방법의 총칭
  - 영화에서 위험한 장면을 대신 촬영하는 배우를 뜻하는 stunt double에서 유래되었다.
  - mock, fake, stub 등




- fixture
  - 테스트를 하는데 필요한 부분들을 미리 준비해 놓은 리소스 혹은 코드.
  - 예를 들어 어떤 테스트를 진행하는데 DB와 연결이 필요하다면 DB와 연결하는 코드가 fixture가 될 수 있다.



- Mock

  > [Mock Object란 무엇인가?](https://medium.com/@SlackBeck/mock-object%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-85159754b2ac) 참고

  - 테스트를 수행할 모듈이 의존하는 실제 외부의 서비스나 모듈을 사용하지 않고 실제 서비스 혹은 모듈을 흉내내는 가짜 모듈을 작성하여 테스트의 효용성을 높이는데 사용하는 객체이다.
  - 즉, 테스트의 의존성을 단절하기 위해 사용하는 객체이다.

  - 예를 들어 아래 코드는 휴대 전화 서비스 기능(의존성)을 제공 받아, 이를 사용한 휴대 전화 문자 발신기를 개발한 것이다.

  ```python
  class CellPhoneService:
      def send_mms(self, msg):
          """
          외부와 통신해야 하는 복잡한 로직
          """
  
  class CellPhoneMmsSender:
      cell_phone_service = None
  
      def __init__(self, cell_phone_service:CellPhoneService):
          CellPhoneMmsSender.cell_phone_service = cell_phone_service
      
      def send(self, msg):
          CellPhoneMmsSender.cell_phone_service.send_mms(msg)
  ```

  - 이 때 어떻게 하면 `send` 메서드를 테스트 할 수 있을까?
    - 가장 간단한 방법은 `send` 메서드의 반환 값을 체크하는 것이겠지만 `send` 메서드는 반환값이 존재하지 않는다.
    - `send` 메서드를 테스트할 때 중요한 점은 실제 메시지를 보내는 것은 `send` 메서드가 아닌 `send_mms` 메서드라는 것이다.
    - 따라서 `send` 메서드의 검증은 실제 메시지가 전송되었는지가 아니라 parameter로 받은 `msg`를 `send_mms`의 argument로 제대로 넘겨서 호출했는가를 확인하는 방식으로 수행되어야 한다.
    - 문제는 그 단순한 기능을 테스트하기 위해서 복잡한 `send_mms` 메서드가 실제로 실행되어야 한다는 점이다.
    - 이럴 때  mock object를 생성해서 테스트한다.
  - Mock Object 생성
    - `CellPhoneService`의 `send_mms`를 override하는 메서드를 생성한다.
    - 오버라이드한 메서드가 잘 실행됐는지 확인할 수 있는 메서드들과 변수들을 추가한다.

  ```python
  class CellPhoneService:
      def send_mms(self, msg):
  		"""
          외부와 통신하는 복잡한 로직
          """
          pass
  
  class CellPhoneMmsSenderMock(CellPhoneService):
      def __init__(self):
          self.is_send_mms_called = False
          self.sent_msg = ""
      
      def send_mms(self, msg):
          self.is_send_mms_called = True
          self.send_msg = msg
      
      def check_send_mms_called(self):
          return self.is_send_mms_called
      
      def get_sent_msg(self):
          return self.sent_msg
  ```

  - 테스트 코드 작성
    - 실제 의존하는 클래스가 아닌, mock object를 주입한다.

  ```python
  class CellPhoneService:
      def send_mms(self, msg):
          """
          외부와 통신하는 복잡한 로직
          """
          pass
  
  class CellPhoneMmsSender:
      cell_phone_service = None
  
      def __init__(self, cell_phone_service:CellPhoneService):
          CellPhoneMmsSender.cell_phone_service = cell_phone_service
      
      def send(self, msg):
          CellPhoneMmsSender.cell_phone_service.send_mms(msg)
  
  
  class CellPhoneMmsSenderMock(CellPhoneService):
      def __init__(self):
          self.is_send_mms_called = False
          self.sent_msg = ""
      
      def send_mms(self, msg):
          self.is_send_mms_called = True
          self.send_msg = msg
      
      def check_send_mms_called(self):
          return self.is_send_mms_called
      
      def get_sent_msg(self):
          return self.sent_msg
  
  
  def test_send():
      msg = "Hello World!"
      cell_phone_mms_sender_mock = CellPhoneMmsSenderMock()
      # 실제 의존하는 클래스가 아닌, mock object를 주입한다.
      cell_phone_mms_sender = CellPhoneMmsSender(cell_phone_mms_sender_mock)
      cell_phone_mms_sender.send(msg)
      assert cell_phone_mms_sender_mock.is_send_mms_called==True
      assert cell_phone_mms_sender_mock.send_msg=="Hello World!"
  ```

  




- 마저 작성
  - https://medium.com/@SlackBeck/mock-object%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-85159754b2ac
  - https://medium.com/@SlackBeck/%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%8A%A4%ED%85%81-test-stub-%EC%9D%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-ff9c8840c1b0#.68pavd8tg
  - https://eminentstar.github.io/2017/07/24/about-mock-test.html





## pytest

- 설치하기

  - 설치

  ```bash
  $ pip install pytest
  ```

  - 확인

  ```bash
  $ pytest --version
  ```



- 테스트 해보기

  - 테스트 코드 작성
    - 모듈 이름(테스트 파일 이름)은 반드시 `test_`를 prefix로 붙이거나 `_test`를 suffix로 붙인다.
    - 테스트 함수의 이름은 반드시 `test_`를 prefix로 붙여야 한다.

  ```python
  def func(x):
      return x + 1
  
  
  def test_answer():
      assert func(3) == 5
  ```

  - 테스트

  ```bash
  $ pytest
  ```

  - 결과

  ```bash
  ======================================= test session starts =======================================
  platform linux -- Python 3.8.0, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
  rootdir: /some/path
  plugins: anyio-3.4.0
  collected 1 item  # 하나의 테스트가 감지되었음을 의미한다.                                                                         
  
  sample_test.py F # sample_test.py의 테스트가 실패 했음을 의미한다(성공일 경우 .으로 표사).          [100%]
  
  ============================================ FAILURES =============================================
  ___________________________________________ test_answer ___________________________________________
  
      def test_answer():
  >       assert func(3) == 5
  E       assert 4 == 5
  E        +  where 4 = func(3)
  
  sample_test.py:6: AssertionError
  ===================================== short test summary info =====================================
  FAILED sample_test.py::test_answer - assert 4 == 5
  ======================================== 1 failed in 0.03s ========================================
  ```



- 특정 예외가 발생했는지 확인하기

  - 특정 예외가 발생했으면 pass, 아니면 fail이 된다.
  - 예시
    - `with`와 pytest의 `raises`를 활용한다.

  ```python
  import pytest
  
  
  def foo():
      raise ValueError
  
  
  def test_mytest():
      with pytest.raises(ValueError):
          foo()
  ```
  
  - 구체적인 예외 정보 확인하기
    - 아래 코드에서 `excinfo`는 `ExceptionInfo`의 인스턴스이다.
    - type, value, traceback 등의 정보를 확인 가능하다.
  
  ```python
  import pytest
  
  
  def my_func():
      raise ValueError("Exception 111 raised")
  
  def test_foo():
      with pytest.raises(ValueError) as excinfo:
          my_func()
      assert '111' in str(excinfo.value)
  ```
  
  - match parameter 사용하기
    - 정규표현식을 사용하여 발생한 예외의 메시지가 특정 형식과 일치하는지를 확인 가능하다.
  
  ```python
  import pytest
  
  
  def my_func():
      raise ValueError("Exception 111 raised")
  
  def test_foo():
      with pytest.raises(ValueError, match=r".* 111 .*"):
          my_func()
  ```
  
  - `xfail`을 사용하여 체크하는 것도 가능하다.
    - 코드 내에서 `raises`를 사용하는 방식은 특정 예외가 확실히 발생해야 하는 상황에서 정말 발생하는지 확인하는 용도이다.
    - `xfail`은 특정 예외가 발생할 수도 있는 상황에서 해당 예외가 발생해도 fail처리 하지 않겠다는 의미이다.
  
  ```python
  import pytest
  
  
  def my_func():
      raise ValueError("Exception 111 raised")
  
  @pytest.mark.xfail(raises=ValueError)
  def test_xfail():
      my_func()
  
  def test_raises():
      with pytest.raises(ValueError):
          my_func()
  ```
  
  - `xfail`을 사용할 경우 `raises`를 사용한 것과 표시도 다르게 해준다.
    - `xfail`은 `F`도 `.`도 아닌  `x`로, raises는 성공했으므로 `.`로 표기한다. 
  
  ```bash
  =========================================== test session starts ============================================
  platform linux -- Python 3.8.0, pytest-7.0.0, pluggy-1.0.0
  rootdir: /data/theo/workspace
  plugins: anyio-3.5.0, asyncio-0.18.0
  asyncio: mode=legacy
  collected 2 items                                                                                          
  
  test_qwe.py x.                                                                                       [100%]
  
  ======================================= 1 passed, 1 xfailed in 0.04s =======================================



- 마커 기반 테스트

  - 각 테스트별로 마커를 설정해줄 수 있다.
  - 테스트 함수에 `@pytest.mark.<marker명>`와 같이 데코레이터를 설정해준다.

  ```python
  import pytest
  
  
  @pytest.mark.foo
  def test_foo():
      pass
  ```

  - `-m` 옵션으로 특정 마커가 붙어있는 테스트 코드만 테스트 하는 것이 가능하다.

  ```bash
  $ pytest -m foo
  ```

  - built-in marker
    - pytest에 내장되어 있는 marker들이 있다.
    - 위에서 본 `xfail`도 내장 마커 중 하나이다.
    - 아래 명령어로 확인이 가능하다.

  ```bash
  $ pytest --markers
  ```



- Fail시에 설명 커스텀하기

  - `pytest_assertrepr_compare` hook을 사용하여 설명을 커스텀 할 수 있다.
  - 예시1

  ```python
  def test_compare():
      assert 1 == 2
  ```

  - conftest.py에 `pytest_assertrepr_compare` hook 작성

  ```python
  def pytest_assertrepr_compare(op, left, right):
      if op == "==":
          return [
              "Comparing Two Ingeger:",
              "   vals: {} != {}".format(left, right),
          ]
  ```

  - 결과1

  ```python
  ============================================== test session starts ===============================================
  platform linux -- Python 3.8.0, pytest-7.0.0, pluggy-1.0.0
  rootdir: /data/theo/workspace
  plugins: anyio-3.5.0, asyncio-0.18.0
  asyncio: mode=legacy
  collected 1 item                                                                                                 
  
  test_qwe.py F                                                                                              [100%]
  
  ==================================================== FAILURES ====================================================
  __________________________________________________ test_compare __________________________________________________
  
      def test_compare():
  >       assert 1 == 2
  E       assert Comparing Two Ingeger:
  E            vals: 1 != 2
  
  test_qwe.py:2: AssertionError
  
  ============================================ short test summary info =============================================
  FAILED test_qwe.py::test_compare - assert Comparing Two Ingeger:
  ========================================== 1 failed, 1 warning in 0.03s ==========================================
  ```

  - 예시2

  ```python
  # content of test_foocompare.py
  class Foo:
      def __init__(self, val):
          self.val = val
  
      def __eq__(self, other):
          return self.val == other.val
  
  
  def test_compare():
      f1 = Foo(1)
      f2 = Foo(2)
      assert f1 == f2
  ```

  - conftest.py에 `pytest_assertrepr_compare` hook 작성

  ```python
  # content of conftest.py
  from test_foo import Foo
  
  
  def pytest_assertrepr_compare(op, left, right):
      if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
          return [
              "Comparing Foo instances:",
              "   vals: {} != {}".format(left.val, right.val),
          ]
  ```

  - 결과2

  ```python
  ========================================== test session starts ===========================================
  platform linux -- Python 3.8.0, pytest-7.0.0, pluggy-1.0.0
  rootdir: /data/theo/workspace
  plugins: anyio-3.5.0, asyncio-0.18.0
  asyncio: mode=legacy
  collected 1 item                                                                                         
  
  test_qwe.py F                                                                                      [100%]
  
  ================================================ FAILURES ================================================
  ______________________________________________ test_compare ______________________________________________
  
      def test_compare():
          f1 = Foo(1)
          f2 = Foo(2)
  >       assert f1 == f2
  E       assert Comparing Foo instances:
  E            vals: 1 != 2
  
  test_qwe.py:13: AssertionError
          
  ======================================== short test summary info =========================================
  FAILED test_qwe.py::test_compare - assert Comparing Foo instances:
  ====================================== 1 failed, 1 warning in 0.03s ======================================
  ```



- class 단위로 테스트하기

  - class를 사용하면 일련의 test를 묶어서 테스트할 수 있다.
  - 코드

  ```python
  import pytest
  
  
  class TestClass:
      def test_one(self):
          x = "foo"
          assert "f" in x
      
      def test_two(self):
          x = "bar"
          assert "f" in x
  ```

  - 주의사항
    - 각각의 테스트는 각 테스트의 독립성을 위해서 고유한 클래스의 인스턴스를 지닌다.
    - 따라서 아래의 경우 `test_two`는 fail이 된다.

  ```python
  class TestClassDemoInstance:
      value = 0
  
      def test_one(self):
          self.value = 1
          assert self.value == 1
  
      def test_two(self):
          assert self.value == 1
  ```



- pytest 명령어

  - 아무 옵션도 주지 않을 경우
    - 현재 디렉터리와 하위 디렉터리의 모든 `test_*.py`, `*_test.py`파일을 테스트한다.
    - 해당 파일들에서 `test_` prefix가 붙은 모든 함수를 테스트한다.
    - `Test` prefix가 붙은 class 내부의 `test_` prefix가 붙은 메서드를 테스트한다(단, `__init__` 메서드가 없어야 한다.).
  - `-q`(`--quiet`)
    - pass, fail을 축약해서 보여준다.
    - fail이라 하더라도 왜 fail인지 이유는 보여준다.
  - `-s`
    - test code 내부의 print문을 터미널에 출력한다.
  
  - 모듈명 지정하기
    - 테스트할 파일을 입력하면 해당 모듈만 테스트한다.
    - `*`를 wildcard로 활용 가능하다.
  
  ```bash
  $ pytest [테스트_파일.py]
  ```

  - 테스트명 지정하기
    - `-k` 옵션으로 어떤 테스트를 실행할지 지정이 가능하다.
  
  ```bash
  $ pytest -k <지정할 테스트>
  
  # 예시: test.py 모듈에 있는 테스트들 중 테스트 이름에 elasticsearch가 포함된 것만 테스트한다.
  $ pytest -k elasticsearch test.py
  ```

  - `::`구분자 사용하기
    - `::` 구분자를 통해 특정 모듈의 특정 클래스의 특정 함수를 테스트 할수 있다.
  
  ```bash
  # test_foo.py 모듈의 FooClass 내부에 있는 test_foo 함수를 테스트한다.
  $ pytest test_foo.py:FooClass:test_foo
  ```
  
  - `--collect-only`를 사용하면 실제 테스트는 하지 않고 테스트 대상들만 보여준다.
    - 각 테스트의 ID 값도 알 수 있다.
    - 테스트 ID는 fixtrue가 있는 경우 `<Function 테스트함수명>`으로 생성된다.
  
  ```bash
  $ pytest --collect-only
  ```
  
  - warning 무시하기
    - 아래와 같이 두 가지 방식이 있다.
    - `--disable-warnings`는 상세한 warning을 출력을 안 할 뿐 summary로 몇 개의 warning이 있는지 보여주기는 한다.
    - 반면에 `-W ignore`는 워닝 자체를 보여주지 않는다.
  
  ```bash
  # --disable-warnings
  $ pytest --disable-warnings
  
  # -W ignore
  $ pytest -W ignore
  ```



- 명령어 실행시 새로운 옵션 추가하기

  - `conftest.py` 파일에 `pytest_addoption` 훅을 통해 새로운 옵션을 추가할 수 있다.

  ```python
  # conftest.py
  
  def pytest_addoption(parser):
      parser.addoption("--hello-world", action='store', default='False', choices=["True", "False"])
  ```

  - 테스트 코드 작성하기
    - `hello_world` fixture가 받은 request는 pytest의 built-in fixture이다.
    - `request`에는 config를 비롯한 각종 데이터가 들어 있다.
    - pytest의 Config 클래스의 `getoption` 메서드를 활용하여 옵션의 값을 가져올 수 있다(두 번째 인자로 해당 옵션이 없을 경우의 기본값을 받는다).

  ```python
  @pytest.fixture
  def hello_world(request):
      return request.config.getoption('--hello-world')
  
  def test_foo(hello_world):
      assert hello_world=="True"
  ```

  - 실행하기
    - 주의할 점은 여기서 넘어간 True는 bool 값이 아닌 string 값이라는 점이다.

  ```bash
  $ pytest --hello-world=True
  ```





### fixture


- fixture

  - 적용된 각 테스트 함수 직전에 실행되는 함수.
  - DB 연결 등의 외부 의존관계를 테스트 외부에서 설정하기 위해 사용한다.
    - 매 테스트마다 의존관계를 일일이 설정해줄 필요 없이 한 번 작성하면 여러 테스트에서 사용 가능하다.
  - 예시
    - fixture 이름을 테스트 함수의 인자에 넣어서 사용한다.

  ```python
  import pytest
  from elasticsearch import Elasticsearch
  
  
  @pytest.fixture
  def es_client():
      return Elasticsearch('127.0.0.1:9200')
  
  def test_ping(es_client):
      assert es_client.ping() == True
  ```

  - conftest
    - fixture 함수들을 `conftest.py` 파일에 작성하면 여러 테스트 파일들에서 접근가능하다.
    - 각 테스트는 테스트가 작성된 모듈 내에서 fixture를 먼저 찾고, 없을 경우 conftest.py에서 찾는다. 그래도 없을 경우 pytest가 제공하는 bulit-in fixture에서 찾는다.
    - `conftest.py`파일은 테스트 대상 모듈과 같은 디렉터리에 있거나 상위 디렉터리에 있으면 자동으로 감지된다.
    - `contest.py`의 위치를 찾을 때, pyest 명령을 실행하는 위치와는 관계가 없다. 오직 테스트 모듈의 위치를 기반으로 찾는다.
  - fixture 확인하기
    - 아래 명령어를 통해 확인 가능하다.

  ```bash
  $ pytest --fixtures
  ```

  - built-in fixture
    - pytest는 build-in fixture를 제공한다.
    - `--fixture` 옵션과 `-v` 옵션을 주면 built-in fixture를 확인 가능하다.

  ```bash
  # 아래 명령어를 통해 어떤 것들이 있는지 확인 가능하다
  $ pytest --fixtures -v
  ```



- fixture의 특징

  - fixture에서 다른 fixture를 호출할 수 있다.
    - 테스트 코드 뿐  아니라 fixture에서도 fixture를 호출할 수 있다.

  ```python
  import pytest
  
  
  @pytest.fixture
  def first_entry():
      return "a"
  
  
  @pytest.fixture
  def order(first_entry):		# fixture에서 다른 fixture를 호출
      return [first_entry]
  
  
  def test_string(order):
      # Act
      order.append("b")
  
      # Assert
      assert order == ["a", "b"]
  ```

  - fixture는 호출될 때마다 실행된다.
    - 따라서 여러 테스트에서 재사용이 가능하다.
    - 아래 예시에서 test_string 테스트에서 이미 order fixture를 호출했지만, test_int는 test_string이 호출하고 값을 추가한 fixture가 아닌, 새로운 fixture를 사용한다.

  ```python
  import pytest
  
  
  @pytest.fixture
  def first_entry():
      return "a"
  
  
  @pytest.fixture
  def order(first_entry):
      return [first_entry]
  
  
  def test_string(order):
      # Act
      order.append("b")
  
      # Assert
      assert order == ["a", "b"]
  
      
  def test_int(order):
      # Act
      order.append(2)
  
      # Assert
      assert order == ["a", 2]
  ```

  - 하나의 test 혹은 fixture에서 복수의 fixture를 사용하는 것이 가능하다.

  ```python
  import pytest
  
  
  @pytest.fixture
  def first_entry():
      return "a"
  
  
  @pytest.fixture
  def second_entry():
      return 2
  
  
  @pytest.fixture
  def order(first_entry, second_entry):
      return [first_entry, second_entry]
  
  
  @pytest.fixture
  def expected_list():
      return ["a", 2, 3.0]
  
  
  def test_string(order, expected_list):
      order.append(3.0)
  
      assert order == expected_list
  ```

  - 한 테스트에서 같은 fixture가 여러 번 호출될 경우 fixture를 caching한다.
    - 이 경우 매 번 fixture를 생성하지 않고, 생성된 fixture를 caching한다.
    - 만일 매 번 fixture를 생성한다면, 아래 예시는 fail 처리 될 것이지만, fixture를 caching하므로 pass된다.
    - 즉 `test_string_only`에서 `append_first` fixture를 호출하면서 `order` fixture에 `a`가 들어가게 되고, `test_string_only`가 두 번째 fixture로 `order`를 다시 받지만 이를 다시 생성하지 않고 이미 생성되어 cache된 order를 사용한다. 

  ```python
  import pytest
  
  
  @pytest.fixture
  def first_entry():
      return "a"
  
  
  @pytest.fixture
  def order():
      return []
  
  
  @pytest.fixture
  def append_first(order, first_entry):
      return order.append(first_entry)
  
  
  def test_string_only(append_first, order, first_entry):
      assert order == [first_entry]
  ```



- Autouse fixture

  - 특정 fixture를 모든 test에 사용해야 하는 경우 fixture 혹은 test에 fixture를 지정하지 않고도 자동으로 호출되도록 할 수 있다.
  - fixture decorator에 `autouse=True`를 추가하면 된다.
    - `append_first` fixture는 어디에서도 명시적으로 호출되지 않았지만 자동으로 호출 됐다.

  ```python
  import pytest
  
  
  @pytest.fixture
  def first_entry():
      return "a"
  
  
  @pytest.fixture
  def order(first_entry):
      return []
  
  
  @pytest.fixture(autouse=True)
  def append_first(order, first_entry):
      return order.append(first_entry)
  
  
  def test_string_only(order, first_entry):
      assert order == [first_entry]
  
  
  def test_string_and_int(order, first_entry):
      order.append(2)
      assert order == [first_entry, 2]
  ```

  - 아래와 같이 사용할 수는 없다.

  ```python
  import pytest
  
  
  @pytest.fixture(autouse=True)
  def my_list():
      return [1, 2, 3]
  
  def test_string_only():
      # my_list는 list가 아닌 function이다.
      assert my_list == [1, 2, 3]
  ```



- fixture의 scope 설정하기

  - fixture의 범위를 설정하여 동일한 fixture를 재호출 없이 사용할 수 있다.
  - `scope=<function, class, module, pacakge, session>`을 통해 설정이 가능하다.
    - 아래 예시에서 `test_foo`에서의 es_client의 id값과 `test_bar`에서의 es_client의 id 값은 같다.

  ```python
  from elasticsearch import Elasticsearch
  import pytest
  
  
  @pytest.fixture(scope="module")
  def es_client():
      return Elasticsearch('127.0.0.1:9200')
  
  def test_foo(es_client):
      assert id(es_client) == -1	# id 값 확인을 위해 일부러 fail이 뜨도록 한다.
  
  def test_bar(es_client):
      assert id(es_client) == -1
  ```

  - 아래와 같이 따로 scope를 설정해주지 않을 경우 기본 값은 function이며, 매 function마다 es_client가 재실행되어 두 테스트 함수에서의 es_client의 id 값이 달라지게 된다.

  ```python
  from elasticsearch import Elasticsearch
  import pytest
  
  
  @pytest.fixture
  def es_client():
      return Elasticsearch('192.168.0.242:9214')
  
  def test_foo(es_client):
      assert id(es_client) == -1	# id 값 확인을 위해 일부러 fail이 뜨도록 한다.
  
  def test_bar(es_client):
      assert id(es_client) == -1
  ```



- 동적 scope

  - 코드의 변경 없이 스코프를 변경하고 싶을 경우 scope를 반환하는 callable한 값을 입력하면 된다.
  - conftest.py에 옵션을 추가한다.

  ```python
  # 옵션에 추가해준다.
  import pytest
  
  
  def pytest_addoption(parser):
      parser.addoption("--my-scope", action='store', default='function', choices=['function', 'module'])
  ```

  - 테스트 코드 작성

  ```python
  from elasticsearch import Elasticsearch
  import pytest
  
  
  def determine(fixture_name, config):
      if config.getoption("--my-scope")=="module":
          return "module"
      return "function"
  
  
  @pytest.fixture(scope=determine)
  def es_client():
      return Elasticsearch('192.168.0.242:9200')
  
  
  def test_foo(es_client):
      assert id(es_client) == -1	# id 값 확인을 위해 일부러 fail이 뜨도록 한다.
  
  
  def test_bar(es_client):
      assert id(es_client) == -1
  ```

  - 테스트1

  ```bash
  $ pytest test_.py --my-scope=module
  
  # 두 테스트에 사용된 es_client의 id 값이 같은 것을 확인 가능하다.
  ============================================== short test summary info ==================================================
  FAILED test_.py::test_foo - AssertionError: assert 140035742347024 == -1
  FAILED test_.py::test_bar - AssertionError: assert 140035742347024 == -1
  ```

  - 테스트2

  ```bash
  # pytest test_.py --my-scope=function과 같다(default를 function으로 줬으므로)
  $ pytest test_.py
  # 두 테스트에 사용된 es_client의 id 값이 다른 것을 확인 가능하다.
  ============================================== short test summary info ==================================================
  FAILED test_.py::test_foo - AssertionError: assert 140163754811056 == -1
  FAILED test_.py::test_bar - AssertionError: assert 140163754908064 == -1
  ```



- params option을 통해 fixture를 parameter화 할 수 있다.

  - fixture 데코레이터에 params를 추가하고 그 값으로 리스트 형식의 데이터를 넘기면, 해당 리스트를 순회하면서 각 테스트가 실행된다.
  - 예시

  ```python
  from elasticsearch import Elasticsearch
  import pytest
  
  # params를 추가하고 값을 넘긴다.
  @pytest.fixture(params=['127.0.0.1:9200', '127.0.0.1:9201'])
  def es_client(request):
      return Elasticsearch(request.param)
  
  
  def test_foo(es_client):
      assert es_client.ping()==True
  ```

  - 결과
    - 테스트는 `test_foo` 뿐이지만 fixture에 params가 2개 선언되어 있으므로 2번 실행된다.
    - 첫 번째 실행과 두 번째 실행은 각기 다른 Elasticsearch에 연결된다.

  ```bash
  ========================================== test session starts ==========================================
  platform linux -- Python 3.8.0, pytest-7.0.0, pluggy-1.0.0
  rootdir: /data/theo/workspace
  plugins: anyio-3.5.0, asyncio-0.18.0
  asyncio: mode=legacy
  collected 2 items        # 2개의 테스트를 감지                                                                               
  
  test_.py ..                                                                                       [100%]
  
  =========================================== 2 passed in 0.24s ===========================================
  ```



- 각 테스트마다 id 값을 지정할 수 있다.

  - pytest의 모든 테스트는 각자의 id값을 가진다.
    - 아래 명령어를 통해 확인이 가능하다.

  ```bash
  $ pyteset --collect-only
  ```

  - 기본적으로 `<Function 테스트함수명[parameterized_fixture]>` 형태로 생성된다.

  ```python
  import pytest
  
  
  def idfn(fixture_value):
      if fixture_value == 'p':
          return "eggs"
      else:
          return None
  
  
  @pytest.fixture(params=['p', 'q'])
  def b(request):
      return request.param
  
  
  def test_b(b):
      pass
  
  # pytest --collect-only
  <Module test_.py>
    <Function test_b[p]>
    <Function test_b[q]>
  ```

  - fixture 데코레이터에 `ids`값을 주면 fixture 데코레이터의 params 순서대로 id가 생성된다.
    - None을 넘길 경우, ids를 설정하지 않았을 때와 마찬가지로 parameter 값으로 id를 생성한다.

  ```python
  import pytest
  
  @pytest.fixture(params=['p', 'q'], ids=[1, None])
  def b(request):
      return request.param
  
  
  def test_b(b):
      pass
  
  # pytest --collect-only
  <Module test_.py>
    <Function test_b[1]>
    <Function test_b[2]>
  ```

  - callable한 값을 넘길 수도 있다.

  ```python
  import pytest
  
  
  def idfn(fixture_value):
      if fixture_value == 'p':
          return "eggs"
      else:
          return None
  
  
  @pytest.fixture(params=['p', 'q'], ids=idfn)
  def b(request):
      return request.param
  
  
  def test_b(b):
      pass
  
  # pytest --collect-only
  <Module test_.py>
    <Function test_b[eggs]>
    <Function test_b[q]>
  ```



- 테스트가 끝난 후 fixture 정리하기

  > https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization 참고



- fixture 모듈화하기

  > https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization 참고



### parameterize

- test 함수에 인자 받기
  - pytest의 built-in marker인 `parametrize` 마커를 사용한다.
    - 인자로 넘긴 리스트의 길이만큼 테스트가 수행된다.
  
  ```python
  import pytest
  
  
  @pytest.mark.parametrize("test_input, expected", [('1+1', 2), ('3+3', 4)])
  def test_eval(test_input, expected):
      assert eval(test_input)==expected
  ```
  
  - 복수의  마커를 추가하는 것도 가능하다.
  
  ```python
  import pytest
  
  
  @pytest.mark.parametrize("x", [0, 1])
  @pytest.mark.parametrize("y", [2, 3])
  def test_foo(x, y):
      pass
  ```



- class에 추가하여  class 내부의 모든 테스트 함수에 적용되도록 할 수 있다.

  - 예시

  ```python
  import pytest
  
  
  @pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
  class TestClass:
      def test_simple_case(self, n, expected):
          assert n + 1 == expected
  
      def test_weird_simple_case(self, n, expected):
          assert (n * 1) + 1 == expected
  ```



- 전역으로 사용하기

  - `pytestmark`라는 이름으로 전역 변수를 선언하면 전역 parameter로 사용이 가능하다.
    - 다른 이름으로 선언하면 적용되지 않는다.

  ```python
  import pytest
  
  pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
  
  
  class TestClass:
      def test_simple_case(self, n, expected):
          assert n + 1 == expected
  
      def test_weird_simple_case(self, n, expected):
          assert (n * 1) + 1 == expected
  ```




## 참고

- [unittest vs pytest](https://www.bangseongbeom.com/unittest-vs-pytest.html#fn:python-internal-test)
- [Pytest](https://velog.io/@samnaka/Pytest)
- [pytest 공식 document](https://docs.pytest.org/en/7.0.x/contents.html)





# ETC

- Python에서 리눅스 명령어 실행하기

  - subprocess 모듈을 사용한다.
    - 실행하려는 명령이 시스템에 설치되어 있어야 한다.
    - 따라서 이식성이 떨어진다.
  - 예시
    - subprocess의 run 메서드를 호출하면 명령이 실행되고, 결과가 PIPE에 저장된다.
    - result.stdout은 str이 아니고 byte이기 때문에 unicode로 변환을 해줘야 한다.

  ```python
  import subprocess
  
  
  result = subprocess.run(['ls'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  
  result = subprocess.run(['wc', '-l', 'test.txt'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  ```

  

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

