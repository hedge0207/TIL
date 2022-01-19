# Request Header

- Header parameter는 Query, Path 등과 같은 방식으로 정의할 수 있다.

  - `Header` class는 `Path`, `Query`, `Cookie` class와 동일하게 `Param` class 를 상속받는다.
  - 아래와 같이 정의한다.

  ```python
  from typing import Optional
  
  from fastapi import FastAPI, Header
  
  app = FastAPI()
  
  
  @app.get("/items/")
  async def read_items(user_agent: Optional[str] = Header(None)):
      return {"User-Agent": user_agent}
  ```



- 자동 변환

  - Header의 key에는 하이픈이 들어가는 경우가 많다.
    - `x-api-key`, `User-agent`
    - 그러나 위와 같은 값들은 Python에서 유효한 값이 아니기에 변환이 필요하다.
  - `Header` class는 하이픈을 언더스코어로 자동으로 변환한다.
    - 또한 직접 사용할 때도 마찬가지로 Python에서 사용하는 snake_case로 변경해서 사용하면 된다.
    - 예를 들어 `User-agent`는 `user_agent`로 사용한다.

  - 아래와 같이 `convert_underscores=False`를 줘서 비활성화 하는 것도 가능하다.

  ```python
  from typing import Optional
  
  from fastapi import FastAPI, Header
  
  app = FastAPI()
  
  
  @app.get("/items/")
  async def read_items(
  
      strange_header: Optional[str] = Header(None, convert_underscores=False)
  
  ):
      return {"strange_header": strange_header}
  
  ```

  

- 중복되는 header를 받는 것도 가능하다.

  - 아래와 같이 List형으로 선언하면 된다.

  ```python
  from typing import List, Optional
  
  from fastapi import FastAPI, Header
  
  app = FastAPI()
  
  
  @app.get("/items/")
  async def read_items(x_token: Optional[List[str]] = Header(None)):
      return {"X-Token values": x_token}
  ```



- Header의 유효성 검증하기

  - Header에 주로 인증 관련 정보들이 담겨 있으므로 그 정보의 유효성을 검증할 필요가 있다.
  - 아래와 같이 유효성을 검증할 함수를 생성한다.

  ```python
  from fastapi import Header, HTTPException
  
  def verify_token(authorization: str = Header(None)):
      if not authorization:
          raise HTTPException(status_code=401, detail="Token does not exist")
      if authorization != "something":
          raise HTTPException(status_code=403, detail="Token invalid")
  ```

  - api에 `dependencies`에 `Depends`를 활용하여 유효성 검증 함수를 추가한다.

  ```python
  from fastapi import FastAPI, Depends
  
  @app.get("/search", dependencies=[Depends(verify_token)])
  def get_items():
      pass
  ```



# Pydantic validator

- Pydantic에서 제공하는 `validator` 데코레이터를 통해 Request Model에 대한 validation이 가능하다.

  - model

  ```python
  from pydantic import BaseModel
  
  
  class UserModel(BaseModel):
      name: str
      username: str
      password1: str
      password2: str
  ```

  - `validator` 데코레이터 추가하기
    - `v`에는 validatiom 대상이 되는 값(예시의 경우 name)이 들어간다.
    - `values`에는 `v`보다 위에 선언 된 값 이 경우(name)이 들어간다.
    - `field`에는 검증 대상 값(`v`)에 대한 정보가 들어간다.
    - `**kwargs`:에는 추가적으로 제공된 값들이 들어가게 된다.

  ```python
  from pydantic import BaseModel, validator
  
  
  class UserModel(BaseModel):
      name: str
      username: str
      password1: str
      password2: str
  
      @validator('username')
      def username_must_contain_space(cls, v, values, field, **kwargs):
          if ' ' not in v:
              raise ValueError('must contain a space')
          return v.title()
  ```



- 예외처리하기

  - pydantic의 `ValidationError`를 활용한다.

  ```python
  from pydantic import BaseModel, validator
  
  
  class UserModel(BaseModel):
      name: str
      username: str
      password1: str
      password2: str
  
  
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



# Testing

- FastAPI는 Starlette의 TestClient를 사용한다.

  - Starlette은 requests를 사용하여 TestClient를 구현했다.
    - 테스트하려는 API에 request를 보내는 방식으로 테스트한다.
  - FastAPI에서 TestClient를 import해도 실제 import 되는 것은 Starlette의 TestClient이다.
    - `starlette.testclient`에서 import한 `TestClient`를 import하는 것이다.
    - 사용자의 편의를 위해서 아래와 같이 구현했다.

  ```python
  # 아래의 두 줄은 완전히 동일한 TestClient를 import한다.
  from fastapi.testclient import TestClient
  from starlette.testclient import TestClient
  
  
  # fastapi.testclient의 코드는 아래와 같다.
  from starlette.testclient import TestClient as TestClient  # noqa
  ```

  - pytest를 설치해야 한다.

  ```bash
  $ pip install pytest
  ```



- Test 코드 작성하기

  - fastapi에서는 일반적으로 아래의 규칙에 따라 테스트 코드를 작성한다.
    - 테스트 함수에 `async`를 붙이지 않으며, TestClient를 통해 테스트 할 때도 `await`을 붙이지 않는다.
    - 이는 pytest를 사용하여 직접 테스트 할 수 있도록 하기 위함이다.
    - 테스트 함수 이름은 `test_`를 prefix로 붙인다(pytest의 컨벤션이다).
  - 테스트 할 코드 작성

  ```python
  from fastapi import FastAPI
  
  app = FastAPI()
  
  
  @app.get("/")
  async def read_main():
      return {"msg": "Hello World"}
  ```

  - 테스트 코드 작성
    - TestClient는 인자로 app을 받는다.
    - Starlette은 내부적으로 requests 라이브러리를 사용하여 테스트한다.
    - 즉 아래 코드에서 `client.get`은 결국 `request.get`을 호출하는 것이다.

  ```python
  from fastapi.testclient import TestClient
  
  from main import app
  
  client = TestClient(app)
  
  
  def test_read_main():
      response = client.get("/")
      assert response.status_code == 200
      assert response.json() == {"msg": "Hello World"}
  ```

  - 테스트 실행
    - 실행하려는 폴더에서 아래 명령어를 입력한다.
    - 테스트 하려는 파일의 이름을 입력하지 않으면, 아래 명령을 실행한 디렉터레이서 `test`라는 이름이 포함 된 `.py` 파일을 모두 테스트 한다.

  ```bash
  $ pytest [파일 이름]
  ```



- 여러 개의 test case 작성하기

  - 테스트 할 코드

  ```python
  from typing import Optional
  
  from fastapi import FastAPI, Header, HTTPException
  from pydantic import BaseModel
  
  fake_secret_token = "coneofsilence"
  
  fake_db = {
      "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
      "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
  }
  
  app = FastAPI()
  
  
  class Item(BaseModel):
      id: str
      title: str
      description: Optional[str] = None
  
  
  @app.get("/items/{item_id}", response_model=Item)
  async def read_main(item_id: str, x_token: str = Header(...)):
      if x_token != fake_secret_token:
          raise HTTPException(status_code=400, detail="Invalid X-Token header")
      if item_id not in fake_db:
          raise HTTPException(status_code=404, detail="Item not found")
      return fake_db[item_id]
  
  
  @app.post("/items/", response_model=Item)
  async def create_item(item: Item, x_token: str = Header(...)):
      if x_token != fake_secret_token:
          raise HTTPException(status_code=400, detail="Invalid X-Token header")
      if item.id in fake_db:
          raise HTTPException(status_code=400, detail="Item already exists")
      fake_db[item.id] = item
      return item
  ```

  - 테스트 코드
    - 하나의 API에서 발생할 수 있는 경우의 수들을 고려해서 test case로 만든다.

  ```python
  from fastapi.testclient import TestClient
  
  from .main import app
  
  client = TestClient(app)
  
  
  def test_read_item():
      response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
      assert response.status_code == 200
      assert response.json() == {
          "id": "foo",
          "title": "Foo",
          "description": "There goes my hero",
      }
  
  
  def test_read_item_bad_token():
      response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
      assert response.status_code == 400
      assert response.json() == {"detail": "Invalid X-Token header"}
  
  
  def test_read_inexistent_item():
      response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
      assert response.status_code == 404
      assert response.json() == {"detail": "Item not found"}
  
  
  def test_create_item():
      response = client.post(
          "/items/",
          headers={"X-Token": "coneofsilence"},
          json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
      )
      assert response.status_code == 200
      assert response.json() == {
          "id": "foobar",
          "title": "Foo Bar",
          "description": "The Foo Barters",
      }
  
  
  def test_create_item_bad_token():
      response = client.post(
          "/items/",
          headers={"X-Token": "hailhydra"},
          json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
      )
      assert response.status_code == 400
      assert response.json() == {"detail": "Invalid X-Token header"}
  
  
  def test_create_existing_item():
      response = client.post(
          "/items/",
          headers={"X-Token": "coneofsilence"},
          json={
              "id": "foo",
              "title": "The Foo ID Stealers",
              "description": "There goes my stealer",
          },
      )
      assert response.status_code == 400
      assert response.json() == {"detail": "Item already exists"}
  ```

  

- 비동기 함수 테스트하기

  - Anyio
    - 테스트 함수 내부에서 비동기 함수를 호출해야 하는 경우, 테스트 함수도 비동기 함수여야 한다.
    - pytest의 Anyio를 통해 테스트 함수가 비동기적으로 호출되도록 할 수 있다.
  - HTTPX
    - 사실 API 함수에서 async를 사용하지 않아도, FastAPI 앱 자체는 비동기적으로 동작한다.
    - `TestClient`는 pytest를 활용하여, `async`를 붙이지 않은 test 함수에서 비동기적인 FastAPI 앱을 호출할 수 있게 한다.
    - 그러나 test 함수에 `async`를 사용하면 이 방식이 불가능해진다.
    - HTTPX는 Python3를 위한 HTTP 클라이언트이다.
    - HTTPX를 `TestClient` 대신 사용함으로써 비동기적인 test 함수를 구현할 수 있다.
  - 테스트 할 코드

  ```python
  from fastapi import FastAPI
  
  app = FastAPI()
  
  
  @app.get("/")
  async def root():
      return {"message": "Tomato"}
  ```

  - 테스트 코드
    - 위에서 말한 anyio와 httpx를 사용하여 구현한다.
    - `@pytest.mark.anyio` annotation은 pytest에게 이 테스트 함수는 비동기적으로 호출되어야 한다는 것을 알려준다.
    - 그 후 httpx의 `AsyncClient`에  app과 요청을 보낼 url을 넣는다.

  ```python
  import pytest
  from httpx import AsyncClient
  
  from main import app
  
  
  @pytest.mark.anyio
  async def test_root():
      async with AsyncClient(app=app, base_url="http://test") as ac:
          response = await ac.get("/")
      assert response.status_code == 200
      assert response.json() == {"message": "Tomato"}
  ```



- test 코드에서 이벤트 발생시키기

  - fastapi에는 앱이 시작될 때나 종료되는 등의 event가 발생할 때 특정 로직을 실행시킬 수 있다.
    - 그러나 테스트는 실제 앱을 실행하는 것은 아니므로 event가 발생하지는 않는데, test 코드에서 event를 발생시키는 방법이 있다.
  - 아래와 같이 `with`를 사용하면 앱이 실행된 것과 같은 효과가 있다.

  ```python
  from fastapi import FastAPI
  from fastapi.testclient import TestClient
  
  app = FastAPI()
  
  items = {}
  
  
  @app.on_event("startup")
  async def startup_event():
      items["foo"] = {"name": "Fighters"}
      items["bar"] = {"name": "Tenders"}
  
  
  @app.get("/items/{item_id}")
  async def read_items(item_id: str):
      return items[item_id]
  
  
  def test_read_items():
      with TestClient(app) as client:
          response = client.get("/items/foo")
          assert response.status_code == 200
          assert response.json() == {"name": "Fighters"}
  ```



- Dependency 테스트하기

  > https://fastapi.tiangolo.com/advanced/testing-dependencies/



















