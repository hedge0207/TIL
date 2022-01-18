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



















