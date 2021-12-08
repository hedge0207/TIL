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















