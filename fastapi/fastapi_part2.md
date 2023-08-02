# Response model

- `response_model_exclude_unset`

  - `response_model_exclude_unset`를 True로 설정하면 데이터가 설정되지 않은 필드는 응답에서 제외시킨다.
    - 기본값이 있다고 하더라도, 기본값이 변경되지 않았다면 응답에서 제외된다.

  - 예시
  
  ```python
  from typing import List, Optional
  
  from fastapi import FastAPI
  from pydantic import BaseModel
  
  app = FastAPI()
  
  
  class Item(BaseModel):
      name: str
      description: Optional[str] = None
      price: float
      tax: float = 10.5
      tags: List[str] = []
  
  
  items = {
      "foo": {"name": "Foo", "price": 50.2},
      "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
      "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
  }
  
  
  @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
  async def read_item(item_id: str):
      return items[item_id]
  ```





## StreamingResponse

- 예외처리

  - StreamingResponse는 특성상 일단 응답을 보내기만 하면 error 발생 여부와 관계 없이 status code가 200 OK로 반환된다.
  - 아래 방법을 통해 error 발생시 status code를 변경해서 보낼 수 있다.
    - `middleware`에서 처리한다.

  ```python
  import time
  
  from fastapi import FastAPI
  from fastapi.responses import StreamingResponse, JSONResponse
  
  app = FastAPI()
  
  @app.middleware("http")
  async def test_middleware(request, call_next):
      res = await call_next(request)
      # /stream endpoint에만 적용한다.
      if request.url.path=="/stream":
          has_content = False
          try:
              # response에 enocde가 불가능한 error 객체가 넘어오면 아래 코드가 실행되지 않고 except문으로 넘어간다.
              async for _ in res.body_iterator:
                  has_content = True
                  break
          except:
              pass
          if not has_content:
              return JSONResponse(status_code=418)
      return res
  
  @app.get("/stream")
  async def stream():
      def iterfile():
          try:
              for _ in range(10):
                  raise
                  data = [str(i) for i in range(10)]
                  time.sleep(1)
                  yield from data
          except Exception as e:
              yield e
  
      return StreamingResponse(iterfile(), media_type="text")
  ```
  
  - `res.body_iterator`
    - `res.body_iterator`에 단순히 값이 없는 것(즉, 위 예시에서 `iterfile` 함수가 아무 것도 yield하지 않는 것)과 error가 발생한 것에는 차이가 있다.
    - `res.body_iterator`에 단순히 값이 없을 경우 `b''`라는 빈 bytes문자열이 1번 yield되어 for문이 실행은 된다.
    - 반면에 error가 발생한 경우 `res.body_iterator`은 아예 빈 값이 되어 for문이 아예 실행되지 않는다.
  - 한계
    - 실행 중간에 error가 난 경우에는 처리가 불가능하다.
    - 예를 들어 #1 부분에서 3번째 반복쯤에 raise를 설정했다면, 어쨌든 `res.body_iterator`안에는 1, 2번째 반복때 yield된 값은 들어있으므로 예외 처리가 불가능하다.



- fastapi redirect response

  - `status_code`를 따로 설정하지 않을 경우 `307 Temporary Redirect`를 반환한 후 바로 redirect url로 연결된다.
    - 따로 설정해주는 것도 가능한데, status_code에 따라서 redirection이 발생하지 않을 수 있다.

  - 방식1.

  ```python
  import uvicorn
  from fastapi import FastAPI
  from fastapi.responses import RedirectResponse
  
  app = FastAPI()
  
  
  @app.get("/hello-world")
  async def hello_world():
      return "Hello!"
  
  
  @app.get("/my-redirect")
  async def redirect_typer():
      return RedirectResponse("http://localhost:8002/hello-world")
  
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8002)
  ```

  - 방식2.

  ```python
  import uvicorn
  from fastapi import FastAPI
  from fastapi.responses import RedirectResponse
  
  app = FastAPI()
  
  
  @app.get("/hello-world")
  async def hello_world():
      return "Hello!"
  
  
  @app.get("/my-redirect", response_class=RedirectResponse)
  async def redirect_typer():
      return "http://localhost:8002/hello-world"
  
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8002)
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





# Dependencies

- Dependency injection
  - FastAPI에서의 dependency injection은 프로그래밍에서 일반적으로 사용되는 dependency injection의 의미와 동일하다.
    - FastAPI에서의 dependency란 path operation function이 필요로하는 것들이다.
    - Path operation function이란 endpoint로 요청이 들어왔을 때 실행되는 함수를 의미한다.
    - FastAPI라는 system은 path operation function이 필요로 하는 dependency들을 제공한다(의존성을 주입한다).
  - 목표
    - Logic을 공유하는 것.
    - Database connection을 공유하는 것.
    - 보안을 강화하고 인증과 인가 등을 처리하는 것.
    - 요약하자면 코드의 반복을 최소화하는 것이 목표이다.



- Dependency injection이 동작하는 방식

  - 예시 코드
    - 두 개의 path operation function이 완전히 동일한 parameter를 받을 경우 이를 의존성 주입을 통해 코드 중복을 최소화하는 코드이다.
    - `Depends` method는 parameter로 dependency를 받는데, 반드시 callable한 값을 입력해야한다.
    - Dependency의 type은 dependency의 반환 type(예시의 경우 dict)을 입력하면 된다.

  ```python
  from typing import Union
  # Depends를 import한다.
  from fastapi import Depends, FastAPI
  
  app = FastAPI()
  
  
  async def common_parameters(
      q: Union[str, None] = None, skip: int = 0, limit: int = 100
  ):
      return {"q": q, "skip": skip, "limit": limit}
  
  # path operation function의 parameter로 Depends를 사용하여 dependency를 선언한다.
  @app.get("/items/")
  async def read_items(commons: dict = Depends(common_parameters)):
      return commons
  
  
  @app.get("/users/")
  async def read_users(commons: dict = Depends(common_parameters)):
      return commons
  ```

  - 동작 방식
    - Request가 들어오면 우선 query parameter를 인자로 dependency를 호출한다.
    - Dependency로부터 반환값을 받고 그 값을 path operation function의 parameter로 넘긴다.



- Class를 주입하기

  - `Depends` method는 인자로 callable한 값을 받는다.
    - Python에서는 class도 callable한 값이므로 `Depends` method의 parameter가 될 수 있다.
  - 예시

  ```python
  from typing import Union
  
  from fastapi import Depends, FastAPI
  from typing_extensions import Annotated
  
  app = FastAPI()
  
  
  fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
  
  # class를 선언하고
  class CommonQueryParams:
      def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
          self.q = q
          self.skip = skip
          self.limit = limit
  
  # 의존성을 주입한다.
  @app.get("/items/")
  async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
      response = {}
      if commons.q:
          response.update({"q": commons.q})
      items = fake_items_db[commons.skip : commons.skip + commons.limit]
      response.update({"items": items})
      return response
  ```

  - 동작 방식
    - Request가 들어오면, dependency class의 `__init__` method가 호출되고, dependency class의 instance를 반환한다.
    - Dependency가 반환한 instance를 path operation function의 parameter로 넘긴다.
  - 위 예시를 보면 dependency를 선언하는 부분에 아래와 같이 `CommonQueryParams`가 중복되어 들어가는 것을 볼 수 있다.

  ```python
  async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
      pass
  ```

  - FastAPI는 아래와 같이 중복을 없앨 수 있는 shortcut을 제공한다.

  ```python
  from typing import Annotated
  
  
  async def read_items(commons: CommonQueryParams = Depends()):
      pass
  ```



- Sub dependency

  - Sub dependency를 설정할 수 있다.
    - Sub dependency의 깊이에는 제한이 없다.
  - 예시
    - `query_or_cookie_extractor` dependency는 `query_extractor`라는 또 다른 dependency를 가지고 있다.

  ```python
  from typing import Annotated
  
  from fastapi import Cookie, Depends, FastAPI
  
  app = FastAPI()
  
  
  def query_extractor(q: str | None = None):
      return q
  
  
  def query_or_cookie_extractor(
      q: Annotated[str, Depends(query_extractor)],
      last_query: Annotated[str | None, Cookie()] = None,
  ):
      if not q:
          return last_query
      return q
  
  
  @app.get("/items/")
  async def read_query(
      query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
  ):
      return {"q_or_cookie": query_or_default}
  ```



- Path operation decorator에 dependency 선언하기

  - Path operation decorator에도 dependency를 선언할 수 있다.
    - 때로는 dependency의 반환값을 사용할 필요는 없지만, dependency가 실행은 되어야 할 때가 있다.
    - 이런 경우에는 path operation function에 dependency를 parameter로 선언하는 것 보다 path operation decorator에 선언하는 것이 더 적절하다.
  - 예시
    - Path operation decorator에 작성된 dependency들의 반환 값은 사용되지 않는다.
    - 아래 예시에서 `verify_key` 함수는 반환값이 있긴 하지만 이 값은 사용되지 않는다.
    - 그럼에도 반환값을 지정한 이유는, 이 함수가 `read_item`의 dependency가 아닌 다른 곳에서 독립적으로 쓰일 때 반환값이 필요할 수 있기 때문이다.

  ```python
  from fastapi import Depends, FastAPI, Header, HTTPException
  from typing_extensions import Annotated
  
  app = FastAPI()
  
  
  async def verify_token(x_token: Annotated[str, Header()]):
      if x_token != "fake-super-secret-token":
          raise HTTPException(status_code=400, detail="X-Token header invalid")
  
  
  async def verify_key(x_key: Annotated[str, Header()]):
      if x_key != "fake-super-secret-key":
          raise HTTPException(status_code=400, detail="X-Key header invalid")
      return x_key
  
  
  @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
  async def read_items():
      return [{"item": "Foo"}, {"item": "Bar"}]
  ```

  



# Backround Tasks

- Response를 반환한 뒤 실행할 background task들을 설정하는 것이 가능하다.
  - Request가 들어올 때 실행되어야 하지만, 굳이 그 결과를 client에게 반환할 필요는 없을 때 유용하게 사용할 수 있다.
  - 예를 들어 request가 들어올 때 마다 mail을 전송하여 알림을 보내거나, 시간이 오래 걸리는 작업을 backround에서 처리해야하는 경우에 유용하다.
  - 만일 보다 많은 자원을 필요로 하는 task를 backround에서 실행해야 할 경우 Celery 등의 보다 큰 tool을 사용하는 것이 좋다.



- `BackgroundTasks`

  - `BackgroundTasks` 예시

  ```python
  import time
  # BackroundTasks를 import한다.
  from fastapi import BackgroundTasks, FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  # backround에서 실행할 function을 정의한다.
  def long_time_task(message: str):
      time.sleep(30)
      print(message)
  
  
  # BackroundTasks를 parameter로 받는다.
  @app.get("/")
  async def send_notification(background_tasks: BackgroundTasks):
      # BackroundTasks instance에 task를 추가한다.
      background_tasks.add_task(long_time_task, "Hello World!")
      return
  
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - `BackgroundTasks`는 `starlette.background`를 사용하여 구현하였다.
  - 동작 방식
    - `add_task`를 호출하면, 인자로 받은 function(task)를 `BackroundTasks` instance의 `tasks` attribute에 저장한다.
    - 실행시에는 `tasks`를 loop를 돌면서 `tasks`에 저장된 task들을 하나씩 실행한다.

  ```python
  class BackgroundTasks(BackgroundTask):
      def __init__(self, tasks: typing.Optional[typing.Sequence[BackgroundTask]] = None):
          self.tasks = list(tasks) if tasks else []
  
      def add_task(
          self, func: typing.Callable[P, typing.Any], *args: P.args, **kwargs: P.kwargs
      ) -> None:
          # Parameter로 받은 function과 argument들로 task를 생성한 후
          task = BackgroundTask(func, *args, **kwargs)
          # tasks에 넣고
          self.tasks.append(task)
  
      async def __call__(self) -> None:
          # tasks를 순회하면서
          for task in self.tasks:
              # 하나씩 실행시킨다.
              await task()
  ```



- 비동기 함수를 backround에서 실행시키기

  - 동기적으로 동작하는 함수를 실행시키는 것과 동일한 방식으로 `BackroundTasks`를 사용하여 비동기 함수를 backround에서 실행시킬 수 있다.
  - 예시

  ```python
  import asyncio
  
  from fastapi import BackgroundTasks, FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  async def long_time_task(message: str):
      asyncio.sleep(30)
      print(message)
  
  
  @app.get("/")
  async def send_notification(background_tasks: BackgroundTasks):
      background_tasks.add_task(long_time_task, "Hello World!")
      return
  
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  













