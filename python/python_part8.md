# Testing

## 테스트시 주의 사항

> https://jojoldu.tistory.com/614

- 테스트 코드에서 내부 구현 검증은 피해라

  - 테스트 코드는 내부 구현이 아닌 최종 결과를 검증해야한다.
    - 내부 구현을 검증하는 테스트들은 구현을 조금만 변경해도 테스트가 깨질 가능성이 높다.
  - 예를 들어 아래와 같은 코드가 있다고 하자.
    - `OrderAmountSum`의 주요 기능은 `get_sum_amount`이고, `add_plus_amount`, `add_minus_amont`는 부차적인 기능이다.
    - 테스트를 할 때 흔히 하는 실수 중 하나가 부차적인 기능들까지 테스트하는 것이다.

  ```python
  class OrderAmountSum:
      def __init__(self, amounts):
          self.plus_sum = 0
          self.minus_sum = 0
          self.add_minus_amont(amounts)
          self.add_minus_amont(amounts)
  
      def get_sum_amount(self):
          return self.plus_sum + self.minus_sum
      
      def add_plus_amount(self, amounts):
          self.plus_sum = sum([num for num in amounts if num > 0])
      
      def add_minus_amont(self, amounts):
          self.minus_sum = sum([num for num in amounts if num < 0])
  
  # 테스트 코드
  def test_order_amount_sum():
      oas = OrderAmountSum([1,2,3,-1,-1,-1])
      # 부차적인 기능 테스트
      assert oas.plus_sum == 6
      # 부차적인 기능 테스트
      assert oas.minus_sum == -3
      assert oas.get_sum_amount() == 3
  ```

  - 만일 테스트 하려는 코드가 아래와 같이 바뀌었다고 생각해보자.
    - 이제 기존에 작성했던 테스트는 `get_sum_amount`를 제외하고눈 전부 깨지게 된다.

  ```python
  class OrderAmountSum:
      def __init__(self, amounts):
          self.amounts = amounts
  
      def get_sum_amount(self):
          return sum(self.amounts)
  ```

  - 따라서 부가적인 기능을 전부 테스트하기보다는 비즈니스 기능 단위의 검증만 테스트코드로 작성하는 것이 낫다.
    - 이것에 구현에 독립적인 테스트를 작성하는 최선의 방법이다.



## 용어

> https://martinfowler.com/bliki/TestDouble.html
>
> https://martinfowler.com/articles/mocksArentStubs.html
>
> https://blog.pragmatists.com/test-doubles-fakes-mocks-and-stubs-1a7491dfa3da
>
> http://xunitpatterns.com/Test%20Double%20Patterns.html



- SUT(System Under test)
  - 테스트하고자하는 대상이 되는 unit을 의미한다.
  - 테스트 코드가 아닌, 테스트 코드를 통해 테스트하고자 하는 unit을 의미한다.
  -  OUT(Object-Under-Test)라고도 불린다.



- 협력객체
  - 테스트하고자하는 대상이 되는 unit은 아니지만, 테스트에 사용되는 객체.
  - SUT이 의존성을 가진 객체라고 볼 수 있다.
  - DOC(Depended-On Conponent)라고도 부른다.



- 상태 기반 테스트와 행위 기반 테스트
  - 상태 기반 테스트(statebased test)
    - 상태 검증(state verification)이라고도 부른다.
    - 메서드가 실행된 후 SUT과 협력객체의 상태를 살펴봄으로써 실행된 메서드가 올바르게 동작했는지를 판단한다.
  - 행위 기반 테스트(behavior based test)
    - 행위 검증(behavior verification)이라고도 부른다.
    - SUT이 협력객체의 메서드를 올바르게 호출했는지를 판단한다.



- test double
  - 실제 객체를 대신해서 테스팅에서 사용하는 모든 방법의 총칭
  - 영화에서 위험한 장면을 대신 촬영하는 배우를 뜻하는 stunt double에서 유래되었다.
  - mock, fake, stub 등
    - 이들의 구분은 모호하다.
    - 따라서 정확히 이들의 차이가 무엇인지 보다는 테스트에 어떻게 이들의 특성을 활용할 것인지를 고민해야 한다.



- Fake

  - 실제로 동작하는 구현을 가지고는 있지만, 실제 프로덕션에는 적합하지 않은 객체이다.
    - 일반적으로 단순화된 동작을 제공한다.
    - 인메모리 데이터 베이스가 좋은 예이다.
  - 예를 들어 게시글을 작성하는 코드의 테스트 코드를 작성해야 한다고 가정해보자.
    - 게시글 작성을 위해서 사용자는 반드시 토큰을 함께 보내야 한다.
    - 그런데 아직 사용자 관련 기능이 구현되지 않아 DB에서 사용자 정보를 가져올 수 없는 상황이다.
    - 이 때  DB와 통신하는 가짜 객체(Fake)를 만들어 실제 DB와 통신하는 것 처럼 동작하게 할 수 있다.

  ```python
  class PostRepository:
      def create_post(self, token, post_id, content):
          pass
      
      def get_post(self, post_id):
          pass
  
  class FackAccountRepository:
      def __init__(self):
          # 인 메모리 데이터베이스 역할
          self.accounts = {}
      
      def hash_password(self):
          pass
      
      def get_token(self, user_name, password):
          pass
      
      def sign_in(self, user_name, password):
          self.accounts[user_name] = self.hash_password(password)
      
      def login(self, user_name, password):
          hased_password = self.accounts.get(user_name)
          if hased_password == self.hash_password(password):
              return self.get_token(user_name)
  
  def test_create_post():
      encoded_pwd = "e1geg544g8sd4gege"
      fake_repo = FackAccountRepository()
      fake_repo.sign_in("John", "1234")
      token = fake_repo.login("John", "1234")
      post_repo = PostRepository()
      post_repo.create_post(token,"1", "some_content")
      post = post_repo.get_posts("1")
      assert post.id == "1"
      assert post.content == "some_content"
  ```

  - 주의 사항
    - Fake 오브젝트는 다른 오브젝트를 대체하는 간소화된 오브젝트라고는 해도, 경우에 따라서는 상당한 코드를 작성해야 할 수도 있다.
    - Fake 오브젝트가 정상적으로 동작한다는 것을 보장해야하기에 Fake 오브젝트를 테스트하는 테스트 코드를 작성해야 할 수도 있다.



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
    - 실제 의존하는 클래스(`CellPhoneService`)가 아닌, mock object를 주입한다.
    - 얼핏 보면 상태 기반 테스트처럼 보이지만 `is_send_mms_called`, `send_msg`라는 상태를 체크하는 것이 아니라 해당 상태를 통해 행위를 체크하는 것이다.

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

  -  Mock Object 사용시 주의 사항
    - Mock Object를 만들기 전에 정말 필요한 것인지 생각해본다.
    - Mock Object를 사용한 테스트가 통과했다는 사실이 실제 객체가 들어왔을 때에도 잘 동작한다는 것을 보장하지는 않는다.



- Stub

  - 테스트 중인 유닛의 요청에 따라 canned answer를 제공하는 객체.
    - canned answer란 정해진 질문에 대해 사전에 준비한 답을 의미한다.
    - 미리 정의된 data를 가지고 있다가 테스트 대상 유닛으로부터 요청이 오면 해당 데이터를 반환한다.
  - 아래와 같은 경우에 주로 사용한다.
    - 구현이 되지 않은 함수나 라이브러리에서 제공하는 함수를 사용할 때.
    - 함수가 반환하는 값을 임의로 생성하고 싶을 때(주로 특이한 예외 상황을 테스트하고자 할 때).
    - 의존성을 가지는 유닛의 응답을 모사하여 독립적으로 테스트를 수행하고자 할 때.
  - 예시
    - 만약 영어를 일본어로 번역하고 일본어를 다시 한국어로 번역하는 서비스를 개발한다고 가정해보자.
    - 일본어를 한국어로 번역하는 기능은 직접 개발하고, 영어를 일본어로 번역하는 기능은 비용이 발생하는 외부 API를 사용한다면, 테스트 할 때마다 비용이 발생하므로 사용이 부담스럽다.
    - 따라서 외부 API가 반환한 영어를 일본어로 번역한 결과물을 stub으로 생성하고 테스트 할 때는 외부 API에 요청을 보내는 대신 stub에서 데이터를 받아오는 식으로 구현이 가능하다.
  
  ```python
  def english_to_japanese_stub():
      return {"original":"Hello", "translated":"こんにちは"}
  
  def japanese_to_korean():
      """
      일본어를 한국어로 번역한 후 번역된 한국어를 반환
      """
  
  def test_foo():
      japanese = english_to_japanese_stub()
      result = japanese_to_korean(japanese)
      assert result == "안녕하세요"
  ```
  
  - 주의사항
    - 정해진 질문에 대한 정해진 답변(canned answer)만 반환하므로 다양한 경우에 대한 테스트가 어려울 수 있다.
  
  - Mock과 stub의 차이
    - Mock은 행위 검증에 사용한다.
    - Mock을 제외한 다른 test double들은 상태 검증에 사용한다.




- fixture
  - 테스트를 하는데 필요한 부분들을 미리 준비해 놓은 리소스 혹은 코드.
  - 예를 들어 어떤 테스트를 진행하는데 DB와 연결이 필요하다면 DB와 연결하는 코드가 fixture가 될 수 있다.



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



### pytest

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



#### fixture


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
      return Elasticsearch('localhost:9214')
  
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
      return Elasticsearch('localhost:9200')
  
  
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



- 테스트 전후에 특정 코드 실행하기

  - `yield`를 활용하여 테스트를 실행하기 전과 후에 특정 코드를 실행시킬 수 있다.

  ```python
  import pytest
  
  
  @pytest.fixture
  def run_before_and_after_tests(tmpdir):
      # test 전에 실행할 코드를 작성한다.
  
      yield # test가 실행된다.
  
      # test가 끝난 후에 실행할 코드를 작성한다.
  ```

  - 예시
    - 만일 Elasticsearch test를 위해서 미리 data를 bulk하고, 테스트 종료 후 index를 삭제해야 하다면 아래와 같이 하면 된다.
  
  ```python
  @pytest.fixture
  def bulk_data():
      bulk_data()
      yield
      delete_test_index()
  ```



- fixture 모듈화하기

  > https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization 참고



#### parameterize

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

