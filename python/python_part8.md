# Testing

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



- 용어
  - fixture
    - 테스트를 하는데 필요한 부분들을 미리 준비해 놓은 리소스 혹은 코드.
    - 예를 들어 어떤 테스트를 진행하는데 DB와 연결이 필요하다면 DB와 연결하는 코드가 fixture가 될 수 있다.
  - Mock





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
  collected 1 item                                                                                  
  
  sample_test.py F                                                                            [100%]
  
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



- pytest 명령어

  - 아무 옵션도 주지 않을 경우
    - 현재 디렉터리와 하위 디렉터리의 모든 `test_*.py`, `*_test.py`파일을 테스트한다.
    - 해당 파일들에서 `test_` prefix가 붙은 모든 함수를 테스트한다.
    - `Test` prefix가 붙은 class 내부의 `test_` prefix가 붙은 메서드를 테스트한다(단, `__init__` 메서드가 없어야 한다.).
  - `-q`(`--quiet`)
    - pass, fail을 축약해서 보여준다.
    - fail이라 하더라도 왜 fail인지 이유는 보여준다.
  - 모듈명 지정하기
    - 테스트할 파일을 입력하면 해당 모듈만 테스트한다.

  ```bash
  $ pytest [테스트_파일.py]
  ```



- 특정 예외가 발생했는지 확인하기

  - 특정 예외가 발생했으면 pass, 아니면 fail이 된다.
  - 코드
    - `with`와 pytest의 `raises`를 활용한다.

  ```python
  import pytest
  
  
  def foo():
      raise ValueError
  
  
  def test_mytest():
      with pytest.raises(ValueError):
          foo()
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



- test 함수에 인자 받기
  - 



# 참고

- [unittest vs pytest](https://www.bangseongbeom.com/unittest-vs-pytest.html#fn:python-internal-test)