# FastAPI security

## 기본 개념

- Authentication & Authorization
  - 일반적으로 authentication은 인증, authorization은 인가라고 번역된다.
  - Authentication
    - 클라이언트에서 요청을 보낸 사용자를 검증하는 것.
    - 예를 들어 한국인이라는 증명으로 주민등록증을 제시하는 것은 authentication을 위한 과정이라 할 수 있다.
  - Authorization
    - 클라이언트에서 요청을 보낸 사용자가 해당 요청을 보낼 권한이 있는지 검증하는 것.
    - 예를 들어 담배를 구입하기 위해 주민등록증을 제시하는 것은 authorization을 위한 과정이라 할 수 있다.



- OAuth2
  - Authentication과 authorization을 처리하기 위한 여러 방식을 정의한 specification이다.
  - Third party를 사용한 authentication 방법도 포함된다.
    - Google로 로그인하기, Github으로 로그인하기 등



- OAuth1
  - OAuth2와 다른 specification이다.
    - OAuth2에 비해 훨씬 복잡하다.
    - 요즘에는 잘 사용하지 않는다.
  - 통신을 어떻게 암호화 할 것인지에 대한 specification이다.
    - OAuth2는 application이 HTTPS로 제공된다고 가정하므로, 통신을 암호화하는 것에 대해서는 다루지 않는다.



- OpenID Connect
  - OAuth2에 기반한 specfication이다.
    - OAuth2에서 상대적으로 모호한 것들을 구체화하여 확장한 것이다.
  - Google login 등에 사용된다.
    - Facebook login은 OpenID Connect를 지원하지 않는다.



- OpenID
  - OpenID Connect와는 다른 specification이다.
  - OpenID Connect와 같은 문제를 해결하기 위해 등장했다.
    - 그러나 OAuth2 기반은 아니다.
  - 요즘은 잘 사용되지 않는다.



- OpenAPI
  - API를 위한 specification이다.
    - FastAPI는 OpenAPI에 기반을 두고 있다.
  - security와 관련된 여러 scheme들을 정의해 놓았다.
    - `apiKey`
    - `http`
    - `oauth2`
    - `openIdConnect`





## OAuth2 기반 인증

- 기본 개념
  - 아래에서 설명하는 예시는 OAuth2 + password 기반 인증 + Bear token의 예시이다.
  - 꼭 위 셋을 함께 사용해야 하는 것은 아니며, 위 개념 들 중 대체 불가능한 것은 없다.
  - token은 특정 내용을 담고 있는 문자열로, 사용자를 검증하기 위해 사용한다.
  - Bearer는 토큰 기반 인증에 존재하는 여러 타입 중 하나로, OAuth2의 전문가 이거나, 다른 타입들위 무엇이 있으며, 해당 타입들이 어떤 상황에 어울리는지 정확히 모른다면, Bearer가 최고의 선택이다.



- Password를 사용할 때의 흐름
  - 클라이언트가 인증 관련 URL로 사용자명과 비밀번호가 담긴 인증 요청을 보낸다.
  - API는 사용자명과 비밀번호를 체크하고 token을 응답으로 보낸다.
  - 클라이언트는 해당 토큰을 어딘가에 임시로 저장한다.
  - 사용자가 인증이 필요한 작업을 하면 클라이언트는 `Authorizaion`이라는 header에 `Bearer + token`을 담아 API에 요청을 보낸다.



- 기본 예시

  - 아래 코드를 실행 후 `/docs`로 접속하면  `Authorize` 버튼이 활성화 된 것을 확인 가능하다.
    - 또한 각 endpoint의 우측 상단에도 자물쇠 모양이 생긴다.

  ```python
  from fastapi import Depends, FastAPI
  from fastapi.security import OAuth2PasswordBearer
  
  app = FastAPI()
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  
  @app.get("/items/")
  async def read_items(token: str = Depends(oauth2_scheme)):
      return {"token": token}
  ```

  - `OAuth2PasswordBearer`
    - OAuth2PasswordBearer의 인스턴스를 생성할 때, `tokenUrl`을 넘긴다.
    - 상대경로와 절대 경로 모두 사용 가능하다.
    - 클라이언트는 이 URL로 인증 요청을 보내야한다.
    - `tokenUrl`이 snake_case를 사용하지 않고, camelCase를 사용한 이유는 OpenAPI와 깉은 이름을 사용하기 위해서다.
  - `oauth2_scheme`
    - `OAuth2PasswordBearer`의 인스턴스로, callable한 값이다.
    - 따라서 `Depends`에 넘길 수 있다.
  - `Depends(oauth2_scheme)`
    - 이 종속성이 추가 된 endpoint들은 요청이 들어왔을 때, `Authentication` header에  `Bearer + token` 값이 있는지 확인한다.
    - 만일 `Authentication` header가 없거나 `Bearer + token` 값이 없을 경우 401 status error(UNAUTORIZED)를 반환한다.
    - 종속성을 추가함으로써 fastapi의 API 문서에 security scheme관련 OpenAPI schema가 추가된다.
  - `SecurityBase`
    - OpenAPI에 보안 관련 설정들이 추가되는 이유는 바로 해당 기능들이 `fastapi.security.base.SecurityBase`를 상속받기 때문이다.
    - `OAuth2PasswordBearer` 역시 `SecurityBase`를 상속받는다.



- 현재 사용자 가져오기

  - 사용자 모델 정의하기

  ```python
  from typing import Optional
  
  from pydantic import BaseModel
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  ```

  - 현재 사용자를 가져오는 dependency 정의하기
    - `get_current_user` dependency는 `oauth2_scheme`를 sub dependency로 갖는다.
    - `fake_decode_token`는 token을 받아서 `User`를 반환한다.
    - user가 없을 경우 반환하는 header(`headers={"WWW-Authenticate": "Bearer"}`) 역시 OAuth2 spec에 정의된 내용이다.
    - 모든 status code 401(UNAUTHORIZED)는 `"WWW-Authenticate` header를 반환하는 것으로 간주한다(따라서 아래 코드는 hearder를 넘기지 않아도 동작한다).
    - 아래 예시에서는 단지 spec에 따르기 위해 선언해주었다.

  ```python
  from fastapi import Depends
  
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  def fake_decode_token(token):
      return User(
          username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
      )
  
  async def get_current_user(token: str = Depends(oauth2_scheme)):
      user = fake_decode_token(token)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
      return user
  ```

  - 전체 코드
    - `read_users_me`에 `get_current_user`를 dependency로 추가한다.
    - 아래와 같이 의존성 주입을 통해 token의 활용 방식을 정의함으로써 보다 쉽게 token 사용이 가능해진다.

  ```python
  from typing import Optional
  
  from fastapi import Depends, FastAPI
  from fastapi.security import OAuth2PasswordBearer
  from pydantic import BaseModel
  
  app = FastAPI()
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  def fake_decode_token(token):
      return User(
          username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
      )
  
  
  user = fake_decode_token(token)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
      return user
  
  
  @app.get("/users/me")
  async def read_users_me(current_user: User = Depends(get_current_user)):
      return current_user
  ```



### OAuth2 + password + Bearer

- OAuth2 Specification

  - Password flow를 사용할 때 클라이언트는 반드시 `username`과 `password` field를 form data로 보내야 한다.
  - Field 명은 반드시 위와 일치해야 한다(`user-name`과 같이 보내선 안 된다).

  - `scope` 라는 field를 보낼 수 있다. 
    - White space로 구분 된 여러 개의 string이 값으로 오는데, 일반적으로 인가를 선언하기 위해 사용한다.
  - `grant_type`이라는 field도 보낼 수 있다.



- `username`과 `password` 받아오기

  - `OAuth2PasswordRequestForm`을 import한다.
  - `OAuth2PasswordBearer`에 인자로 넘긴 `tokenUrl`과 일치하는 endpoint를 생성한다.

  ```python
  from typing import Optional
  
  from fastapi import Depends, FastAPI, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
  from pydantic import BaseModel
  
  fake_users_db = {
      "johndoe": {
          "username": "johndoe",
          "full_name": "John Doe",
          "email": "johndoe@example.com",
          "hashed_password": "fakehashedsecret",
          "disabled": False,
      },
      "alice": {
          "username": "alice",
          "full_name": "Alice Wonderson",
          "email": "alice@example.com",
          "hashed_password": "fakehashedsecret2",
          "disabled": True,
      },
  }
  
  app = FastAPI()
  
  
  def fake_hash_password(password: str):
      return "fakehashed" + password
  
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  class UserInDB(User):
      hashed_password: str
  
  
  @app.post("/token")
  async def login(form_data: OAuth2PasswordRequestForm = Depends()):
      user_dict = fake_users_db.get(form_data.username)
      # 사용자가 DB에 없을 경우
      if not user_dict:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
      user = UserInDB(**user_dict)
      hashed_password = fake_hash_password(form_data.password)
      # 만일 요청으로 넘어온 password를 hashing한 값이 DB에 저장된 hashing된 password와 같지 않으면
      if not hashed_password == user.hashed_password:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
  
      return {"access_token": user.username, "token_type": "bearer"}
  ```



- `OAuth2PasswordRequestForm`
  - Form data를 선언하는 class dependency이다.
  - `username`, `password`, `scope`, `grant_type` 등이 담겨 있다.
  - 그 밖에도 `client_id`, `client_secret`등도 담겨 있다.
  - `OAuth2PasswordRequestForm`의 경우 `grant_type`은 강제하지 않는다.
    - 만일 `grant_type`을 강제하고자 한다면 `OAuth2PasswordRequestFormStrict`를 사용하면 된다.



- Password Hashing
  - 보안을 위해서 비밀번호를 절대로 그대로 저장해선 안되며, 반드시 hashing 과정을 거쳐 저장해야한다.
    - 만일 DB가 해킹되더라도 password가 hash로 저장되어 있다면, 해커는 원래 password를 알 수 없다.
    - 따라서 해당 시스템 뿐 아니라 사용자가 같은 password를 사용하는 다양한 시스템에 침투하는 것도 불가능해진다.
  - Hashing은 특정한 내용을 언뜻 보기에는 아무 뜻도 없어 보이는 연속된 bytes값으로 변경하는 것이다.
  - 정확히 같은 내용을 hashing하면 정확히 같은 bytes 값이 나와야한다.
    - 단 아래에서 사용할 bcrypt의 경우 salt 과정이 추가되어 항상 다른 값이 나온다.
  - 또한 hashing된 bytes값을 원래의 내용으로 전환도 불가능하다.



- Token 반환
  - `OAuth2PasswordBearer`의 파라미터로 넘긴 endpoint의 반환값은 json 형식이어야한다.
  - 또한 `access_token`과 `token_type`이라는 key를 가져야한다.



- Dependency 확장하기

  - 아래 코드는 오직 현재 active 상태(`disabled`가 True인 상태)인 user만 가져오는 dependency로 변경한 것이다.

  ```python
  from typing import Optional
  
  from fastapi import Depends, FastAPI, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
  from pydantic import BaseModel
  
  fake_users_db = {
      "johndoe": {
          "username": "johndoe",
          "full_name": "John Doe",
          "email": "johndoe@example.com",
          "hashed_password": "fakehashedsecret",
          "disabled": False,
      },
      "alice": {
          "username": "alice",
          "full_name": "Alice Wonderson",
          "email": "alice@example.com",
          "hashed_password": "fakehashedsecret2",
          "disabled": True,
      },
  }
  
  app = FastAPI()
  
  
  def fake_hash_password(password: str):
      return "fakehashed" + password
  
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  class UserInDB(User):
      hashed_password: str
  
  
  def get_user(db, username: str):
      if username in db:
          user_dict = db[username]
          return UserInDB(**user_dict)
  
  
  def fake_decode_token(token):
      # This doesn't provide any security at all
      # Check the next version
      user = get_user(fake_users_db, token)
      return user
  
  
  async def get_current_user(token: str = Depends(oauth2_scheme)):
      user = fake_decode_token(token)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
      return user
  
  
  async def get_current_active_user(current_user: User = Depends(get_current_user)):
      if current_user.disabled:
          raise HTTPException(status_code=400, detail="Inactive user")
      return current_user
  
  
  @app.post("/token")
  async def login(form_data: OAuth2PasswordRequestForm = Depends()):
      user_dict = fake_users_db.get(form_data.username)
      if not user_dict:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
      user = UserInDB(**user_dict)
      hashed_password = fake_hash_password(form_data.password)
      if not hashed_password == user.hashed_password:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
  
      return {"access_token": user.username, "token_type": "bearer"}
  
  
  @app.get("/users/me")
  async def read_users_me(current_user: User = Depends(get_current_active_user)):
      return current_user
  ```



### OAuth2 + password(hashing) + Bearer with JWT token

- 지금까지는 securiy의 기본적인 flow를 살펴봤다면 아래는 실제 application에 적용해도 될 수준의 예시이다.
  - Password를 hashing하여 저장한다.
  - JWT token을 사용한다.



- JWT(JSON We Tokens)

  > https://jwt.io/

  - JSON object를 공백 없는 문자열로 변경하기 위한 표준이다.
    - `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`와 같은 형태이다.
  - 암호화하지는 않기에 누구나 JWT token을 JSON object로 변환 가능하다.
  - 그러나 일종의 sign이 존재해서 JWT token이 정말 그것을 소유한 사람으로부터 온 것인지 검증이 가능하다.
    - 예를 들어 3일의 만료 기간을 가진 token을 생성했다고 가정했을때, 해당 토큰을 소유하기만 하면 다음 날에도 loggin 된 갓으로 인식된다.
    - 그러나 3일이 지난 후에는 토큰이 있다고 하더라도 이미 만료되었으므로, 다시 login해서 새로운 토큰을 발급받아야한다.
    - 또한 다른 사용자가 해당 토큰을 가지고 접근해도, 서명이 일치하지 않기에 불가능하다.



- 필요한 package 설치하기

  - `python-jose`
    - Python에서 JWT token을 다루는 package
    - `PyJWT`라는 package도 존재하지만, `python-jose`가 더 많은 기능을 담고 있다.

  ```bash
  $ pip install "python-jose[cryptography]"
  ```

  - `passlib`
    - hash를 보다 쉽게 다룰 수 있게 해주는 package
    - 다양한 hashing 알고리즘을 지원한다(`Bcrypt`가 가장 추천된다).

  ```bash
  $ pip install "passlib[bcrypt]"
  ```



- 비밀번호를 hashing하고 검증하기

  - PassLib의 context는 지금은 deprecate 된 이전 알고리즘에도 사용할 수 있다.
  - bcrypt는 같은 input이 들어와도 다른 output을  반환한다.
    - salt 과정이 추가되었기 때문이다.
    - 따라서 단순히 password를 hash된 password와 비교해서는 안되며, 별도의 방법으로 유요한 password인지 비교해야한다.
  
  ```python
  from typing import Optional
  
  # passlib context를 import한다.
  from passlib.context import CryptContext
  from pydantic import BaseModel
  
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  class UserInDB(User):
      hashed_password: str
  
  # password를 hashing하고 hashing된 값과 hash값을 비교
  def verify_password(plain_password, hashed_password):
      return pwd_context.verify(plain_password, hashed_password)
  
  # password를 hashing
  def get_password_hash(password):
      return pwd_context.hash(password)
  
  def get_user(db, username: str):
      if username in db:
          user_dict = db[username]
          return UserInDB(**user_dict)
  
  def authenticate_user(fake_db, username: str, password: str):
      user = get_user(fake_db, username)
      if not user:
          return False
      if not verify_password(password, user.hashed_password):
          return False
      return user
  ```



- JWT token 다루기

  - JWT token의 sign에 사용할 무선적인 secret key를 생성한다.

  ```sh
  $ openssl rand -hex 32
  # output
  09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
  ```

  - 코드

  ```python
  from datetime import datetime, timedelta
  from typing import Optional
  
  from jose import jwt
  from pydantic import BaseModel
  
  # 위에서 나온 값을 넣는다.
  SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  # JWT token의 sign을 위한 알고리즘을 입력한다.
  ALGORITHM = "HS256"
  # JWT token의 만료 기한을 설정한다.
  ACCESS_TOKEN_EXPIRE_MINUTES = 30
  
  # endpoint의 응답에 사용할 Pydantic Model을 정의한다.
  class Token(BaseModel):
      access_token: str
      token_type: str
  
  
  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
      to_encode = data.copy()
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  ```



- API에 적용

  - 전체 코드

  ```python
  from datetime import datetime, timedelta
  from typing import Optional
  
  from fastapi import Depends, FastAPI, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
  from jose import JWTError, jwt
  from passlib.context import CryptContext
  from pydantic import BaseModel
  
  
  SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30
  
  
  # password=1234
  fake_users_db = {
      "johndoe": {
          "username": "johndoe",
          "full_name": "John Doe",
          "email": "johndoe@example.com",
          "hashed_password": "$2b$12$jTjayMnq0quaGF7YGwiL2e/95vjr4li4LSNRFpd3Ou6QK/NVS4K2G",
          "disabled": False,
      }
  }
  
  
  class Token(BaseModel):
      access_token: str
      token_type: str
  
  
  class TokenData(BaseModel):
      username: Optional[str] = None
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  class UserInDB(User):
      hashed_password: str
  
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  app = FastAPI()
  
  
  def verify_password(plain_password, hashed_password):
      return pwd_context.verify(plain_password, hashed_password)
  
  
  def get_password_hash(password):
      return pwd_context.hash(password)
  
  
  def get_user(db, username: str):
      if username in db:
          user_dict = db[username]
          return UserInDB(**user_dict)
  
  
  def authenticate_user(fake_db, username: str, password: str):
      user = get_user(fake_db, username)
      if not user:
          return False
      if not verify_password(password, user.hashed_password):
          return False
      return user
  
  
  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
      to_encode = data.copy()
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  
  
  async def get_current_user(token: str = Depends(oauth2_scheme)):
      credentials_exception = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"},
      )
      try:
          # jwt token을 검증하고, json object로 변환한다.
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username: str = payload.get("sub")
          if username is None:
              raise credentials_exception
          token_data = TokenData(username=username)
      except JWTError:
          raise credentials_exception
      user = get_user(fake_users_db, username=token_data.username)
      if user is None:
          raise credentials_exception
      return user
  
  
  async def get_current_active_user(current_user: User = Depends(get_current_user)):
      if current_user.disabled:
          raise HTTPException(status_code=400, detail="Inactive user")
      return current_user
  
  
  @app.post("/token", response_model=Token)
  async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
      user = authenticate_user(fake_users_db, form_data.username, form_data.password)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect username or password",
              headers={"WWW-Authenticate": "Bearer"},
          )
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      # JWT access token을 생성하고 반환한다.
      access_token = create_access_token(
          data={"sub": user.username}, expires_delta=access_token_expires
      )
      return {"access_token": access_token, "token_type": "bearer"}
  
  
  @app.get("/users/me/", response_model=User)
  async def read_users_me(current_user: User = Depends(get_current_active_user)):
      return current_user
  
  
  @app.get("/users/me/items/")
  async def read_own_items(current_user: User = Depends(get_current_active_user)):
      return [{"item_id": "Foo", "owner": current_user.username}]
  ```

  - `sub`(subject)
    - JWT token의 정보가 담긴 부분을 payload라 부른다.
    - payload에 담긴 정보의 한 조각을 claim이라 부른다.
    - 위 예시에서 `get_current_user` 함수의 내부의 `payload.get("sub")`와 같이 JWT token의 json형에서 `sub`라는 claim으로 값을 가져오는 것을 확인 할 수 있다.
    - JWT token은 사용자 인증 외에 다양한 곳에서 사용될 수 있다.
    - 따라서 JWT token이 사용되는 다양한 곳에서 동일한 claim을 사용하면 충돌이 발생할 수 있다.
    - 이를 피하기 위해서 각각의 claim은 하나의 application 내에서 고유해야한다.

  ```json
  // payload 예시, name이라는 claim이 중복되었으므로 둘 중 하나를 변경해줘야한다.
  {
    "sub": "1234567890",
    "name": "John Doe",
    "name": "Jane Doe",
    "admin": true
  }
  ```



- 테스트 하기

  - Token 발급받기
    - 아래와 같이 form-data에 username과 password를 넣어서 보내야한다.

  ![get_token](fastapi_part3.assets/get_token.png)

  - 응답으로 온 token을 사용하여 요청 보내기
    - Authorization header에 아래와 같이 `Bearer + token` 형식으로 보낸다.

  ![use_token](fastapi_part3.assets/use_token.png)

  - `/users/me/` 경로로 요청을 보낸 경우
    -  `get_current_active_user` →  `get_current_active_user` → `oauth2_scheme` 순으로 실행된다.
    - `oauth2_scheme`가 실행되면 요청에 Authorization header가 있는지 확인하고, 그 값이 `Bearer + token` 형태인지 확인 후 token을 반환한다.



### Scope

> 대부분의 경우  scope의 사용은 과잉이다. 따라서 꼭 필요하지 않다면, 굳이 사용하지 않아도 된다.

- Scope
  - OAuth2에 정의 된 spec 중 하나이다.
    - 권한과 관련된 내용이 담겨 있다.
  - scope는 문자열로 구성된 목록으로, 스페이스로 구분된다.
    - 각각의 scope들은 어떤 포맷이든 가능하지만 스페이스는 사용할 수 없다.
    - `user:read`, `user:write` 등이 일반적인 형식이다.



- Scope 설정하기

  - 아래 예시에서는 입력 받은 모든 scope를 바로 넣어줬지만, 실제 application에서는 해당 입력받은 scope를 해당 user 가질 수 있는지 검증해야한다.
    - 즉 `login_for_access_token`에서 `data={"sub": user.username, "scopes": form_data.scopes}`와 같이 **바로 넣어선 안된다.**
  - `/tokem` endpoint가 사용하는 `OAuth2PasswordRequestForm`는 `scopes`라는 property를 포함하고 있다.
    - 값으로 str의 list를 받는다.
  - Endpoint에 scope 설정
    - endpoint에 scope를 설정하기 위해서는 `Security`를 import해야한다.
    - `Security`는 `Depends`처럼 dependency를 설정하기 위해 사용할 수 있으며, `scopes`라는 parameter(`List[str]`)를 받는다.
    - `Depends`와 마찬가지로 sub dependency를 가질 수 있다.
    - 사실 Security는 `Depends`의 subclass이다.
  - `SecurityScopes`는 `Request`와 유사하다.
    - `get_current_user`는 `SecurityScopes` 타입인 `security_scopes` 파라미터를 받는다.
    - `SecurityScopes`는 `scopes`라는 property를 갖는데(`List[str]`), 여기에는 해당 함수와, 해당 함수를 sub dependency로 사용하는 모든 dependency들의  scope가 담겨있다.
    - 즉, 요구되는 scope들의 목록이 담겨 있다.
    - 또한 `scope_str`이라는 attribute도 지니고 있는데, 여기에는 모든 scope들을 스페이스로 구분 된 하나의 문자열로 저장되어 있다.
  - Scope 검증 과정
    - 상기했듯 `SecurityScopes`의 `scopes` property에는 해당 함수와, 해당 함수를 sub dependency로 사용하는 모든 dependency들의 scope가 담겨있다.
    - 즉, 이 경우 `get_current_user`를 sub dependency로 사용하는 `get_current_active_user`와 `read_own_items`의 scope가 `scopes` property에 담기게 된다. 
    - 만일 `scopes` property에 있는 scope가  JWT token에 담긴 scope들의 목록에는 없다면, 해당 요청은 인가되지 않은 요청이라는 뜻이 된다.
  
  - 요청별로 요구되는 scope들
    - `read_own_items`: [`"items"`,`"me"`]
    - `read_users_me`: [`"me"`]
    - read_system_status: [ ]
  
  
  ```python
  import uvicorn
  from datetime import datetime, timedelta
  from typing import List, Optional
  
  from fastapi import Depends, FastAPI, HTTPException, Security, status
  # SecurityScopes를 import한다.
  from fastapi.security import (
      OAuth2PasswordBearer,
      OAuth2PasswordRequestForm,
      SecurityScopes,
  )
  from jose import JWTError, jwt
  from passlib.context import CryptContext
  from pydantic import BaseModel, ValidationError
  
  
  SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30
  
  
  fake_users_db = {
      # password = 1234
      "johndoe": {
          "username": "johndoe",
          "full_name": "John Doe",
          "email": "johndoe@example.com",
          "hashed_password": "$2b$12$jTjayMnq0quaGF7YGwiL2e/95vjr4li4LSNRFpd3Ou6QK/NVS4K2G",
          "disabled": False,
      },
      "alice": {
          "username": "alice",
          "full_name": "Alice Chains",
          "email": "alicechains@example.com",
          "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
          "disabled": True,
      },
  }
  
  
  class Token(BaseModel):
      access_token: str
      token_type: str
  
  # scopes를 추가한다.
  class TokenData(BaseModel):
      username: Optional[str] = None
      scopes: List[str] = []
  
  
  class User(BaseModel):
      username: str
      email: Optional[str] = None
      full_name: Optional[str] = None
      disabled: Optional[bool] = None
  
  
  class UserInDB(User):
      hashed_password: str
  
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  # scopes를 추가로 넘긴다.
  # key에 scope가 들어가고, value에 scope에 대한 설명이 들어가는 dict를 넘긴다.
  oauth2_scheme = OAuth2PasswordBearer(
      tokenUrl="token",
      scopes={"me": "Read information about the current user.", "items": "Read items."},
  )
  
  app = FastAPI()
  
  
  def verify_password(plain_password, hashed_password):
      return pwd_context.verify(plain_password, hashed_password)
  
  
  def get_password_hash(password):
      return pwd_context.hash(password)
  
  
  def get_user(db, username: str):
      if username in db:
          user_dict = db[username]
          return UserInDB(**user_dict)
  
  
  def authenticate_user(fake_db, username: str, password: str):
      user = get_user(fake_db, username)
      if not user:
          return False
      if not verify_password(password, user.hashed_password):
          return False
      return user
  
  
  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
      to_encode = data.copy()
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  
  
  # SecurityScopes의 instance를 추가로 받는다.
  async def get_current_user(
      security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
  ):
      # exception에 scope 관련 정보를 추가한다.
      if security_scopes.scopes:
          authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
      else:
          authenticate_value = f"Bearer"
      credentials_exception = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": authenticate_value},
      )
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username: str = payload.get("sub")
          # username이 들어 왔는지 검증
          if username is None:
              raise credentials_exception
          token_scopes = payload.get("scopes", [])
          # username과 scope의 type이 올바른지 검증
          token_data = TokenData(scopes=token_scopes, username=username)
      except (JWTError, ValidationError):
          raise credentials_exception
      user = get_user(fake_users_db, username=token_data.username)
      # user가 존재하는지 검증
      if user is None:
          raise credentials_exception
      for scope in security_scopes.scopes:
          # JWT token에 기록 된 scope들 중 하나라도 security_scopes에 존재하지 않으면 해당 요청은 인가되지 않은 요청이다.
          if scope not in token_data.scopes:
              raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Not enough permissions",
                  headers={"WWW-Authenticate": authenticate_value},
              )
      return user
  
  
  async def get_current_active_user(
      current_user: User = Security(get_current_user, scopes=["me"])
  ):
      if current_user.disabled:
          raise HTTPException(status_code=400, detail="Inactive user")
      return current_user
  
  
  @app.post("/token", response_model=Token)
  async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
      user = authenticate_user(fake_users_db, form_data.username, form_data.password)
      if not user:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(
          data={"sub": user.username, "scopes": form_data.scopes},
          expires_delta=access_token_expires,
      )
      return {"access_token": access_token, "token_type": "bearer"}
  
  
  @app.get("/users/me/", response_model=User)
  async def read_users_me(current_user: User = Depends(get_current_active_user)):
      return current_user
  
  # scope를 추가
  @app.get("/users/me/items/")
  async def read_own_items(
      current_user: User = Security(get_current_active_user, scopes=["items"])
  ):
      return [{"item_id": "Foo", "owner": current_user.username}]
  
  
  @app.get("/status/")
  async def read_system_status(current_user: User = Depends(get_current_user)):
      return {"status": "ok"}
  
  
  if __name__=="__main__":
      uvicorn.run("main:app", port=8080, reload=True)
  ```



- 테스트하기

  - 가장 많은 scope를 필요로 하는 `/users/me/items/` 기준
    - form-data에 scope라는 key로 scope들을 보낸다.

  ![image-20220329174610606](fastapi_part3.assets/image-20220329174610606.png)

  - 위에서 응답으로 받은 JWT token을 header에 담아 요청을 보낸다.

  ![image-20220329174647082](fastapi_part3.assets/image-20220329174647082.png)



- Third party를 통한 인증
  - `fastapi.security.oauth2`에 이와 관련된 기능이 포함되어 있다.





## HTTP Basic Auth

- OAuth2 기반 인증 보다 훨씬 간단하게 인증을 구현할 수 있다.
  - `Authorization` Header에 `Basic username:password` 형식의 값 base64로 인코딩한 값을 받아, 이를 통해 인증을 진행한다.
  - 만일 `Authorization` header가 없거나 값의 형식이 다를 경우 HTTP 401("Unauthorized") erorr를 반환한다.
  - 그 후 `WWW-Authenticate` header에 `Basic`라는 값과 realm(optional) parameter를 반환한다.
  - 이를 받은 브라우저는 username과 password 입력을 위한 창을 띄우게 된다.
  - 해당 창에 username과 password를 입력하면 인증이 진행된다.



- 예시

  - `HTTPBasic`, `HTTPBasicCredentials`를 사용한다.

  ```python
  from fastapi import Depends, FastAPI
  from fastapi.security import HTTPBasic, HTTPBasicCredentials
  
  app = FastAPI()
  # HTTPBasic의 인스턴스 생성
  security = HTTPBasic()
  
  
  # HTTPBasic의 인스턴스를 dependency로 넣어준다.
  # security는 HTTPBasicCredentials의 인스턴스를 반환한다.
  @app.get("/users/me")
  def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
      return {"username": credentials.username, "password": credentials.password}
  ```

  - `Authorization`  header를 넘기지 않을 경우
    - 아래와 같이 응답의 header에 `www-authentication`의 값으로 Basic을 반환한다.

  ![image-20220330180812647](fastapi_part3.assets/image-20220330180812647.png)

  - base64로 인코딩하기
    - `username:password` 형태의 문자열을 base64로 인코딩한다.
    - 암호화가 아닌 단순 인코딩만 하면 된다.

  ```python
  import base64
  
  value = "john:1234"
  bytes_value = value.encode()
  base64_value = base64.b64encode(bytes_value)
  print(base64_value)	# am9objoxMjM0
  ```

  - `Authorization`  header 넘기기
    - 위에서 encoding한 값을 `Basic 인코딩한 값` 형태로 넘긴다.

  ![image-20220330181238456](fastapi_part3.assets/image-20220330181238456.png)

  





# Nginx + FastAPI

- Uvicorn

  - 아래와 같이 web server로 nginx를 사용할 간단한 FastAPI app을 생성하고 uvicorn으로 실행한다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  app = FastAPI()
  
  
  @app.get("/foo")
  def foo():
      print("foo")
      return "foo"
  
  
  if __name__ == "__main__":
      uvicorn.run(app, host="123.456.7.890", port=8090)
  ```

  - `nginx.conf`의 `http` block에 아래와 같은 설정을 추가한다.
    - 아래에서 설정한 `proxy_pass` 외에도 다양한 설정이 있지만, 필수 설정은 `proxy_pass` 뿐이다.
  
  
  ```nginx
  # ...
  
  http {
      # ...
      server {
          listen 80;
          server_name 123.456.7.890;
  
          location / {
              proxy_pass http://123.456.7.890:8090;
          }
      }
  
      include /etc/nginx/conf.d/*.conf;
  }
  ```







# Uvicorn과 Gunicorn

- Uvicorn

  - Python을 위한 ASGI web server이다.
    - 현재까지는 HTTP/1.1과WebSocket을 지원한다.
  - 설치

  ```bash
  $ pip install uvicorn
  
  # 최소한의 dependency와 함께 설치
  $ pip install 'uvicorn[standard]'
  ```



- Uvicorn을 process manager와 함께 사용하기

  - Uvicorn을 process manager와 함께 사용하면 보다 탄력적으로 여러 process들을 관리할 수 있다.

    - Socket setup
    - 여러 sever process의 실행
    - Process들의 실행 여부 모니터링. 
    - Process 재실행을 위한 signal 청취
    - Process 종료
    - 실행 중인 process들의 개수 조절.

  - Built-in

    - Uvicorn에는 여러개의 worker process를 실행하기 위한 `--workers` option이 있다.

    - Gunicorn과 달리 uvicorn은 pre-fork하지 않고 [spawn](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)하는데, 이는 uvicorn의 multiprocess manager가 Windows에서도 동작할 수 있게 해준다.
    - Process manager는 process들의 상태를 모니터링하고, 예상치 못하게 종료된 process들을 restart하는 등의 역할을 수행한다.

  - Built-in 외에도 아래와 같은 것들을 사용할 수 있다.

    - Gunicorn
    - Supervisor
    - Circus



- Gunicorn으로 여러 개의 워커 실행하기

  - Fastapi는 내부적으로 uvicorn을 사용한다.
    - uvicorn은 ASGI 서버로 비동기적인 처리를 처리할 수 있다는 장점이 있다.
  - Gunicorn은 WSGI 서버이다.
    - WSGI 서버이기에 비동기 요청은 처리가 불가능하다.
    - gunicorn은 WSGI 서버이면서 process manager의 역할도 한다.
    - 즉 클라이언트로부터 들어온 요청을 여러 프로세스로 분배하는 역할을 한다.
  - uvicorn과 gunicorn을 함께 사용하면 비동기 처리와 multi processing이라는 각자의 이점을 모두 누릴 수 있다.
    - 상기했듯 gunicorn은 process manager의 역할도 한다.
    - 따라서 복수의 uvicorn worker process를  gunicorn에 등록하면, gunicorn에 요청이 들어올 때 마다 gunicorn이 각 uvicorn worker process에 전달하여 처리하게 할 수 있다.
    - uvicorn worker는 gunicorn으로 부터 받은 정보를 fastapi에서 사용할 수 있도록 ASGI 표준에 맞게 변환하고 처리한다.
    - uvicorn도 이를 염두에 두고 개발하여 `uvicorn.workers.UvicornWorker`에 gunicorn에 등록할 수 있는 UvicornWorker class를 작성해 놓았다.
  - 설치
    - uvicorn의 확장 패키지들도 함께 받는다(`uvicorn[standard]`)

  ```bash
  $ pip install uvicorn[standard] gunicorn 
  ```

  - 실행

  ```bash
  $ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
  ```

  - CPython이 아닌 PyPy로 실행하고자 한다면 아래와 같이 하면 된다.
    - `UvicornWorker`는 `uvloop`와 `httptools`를 사용한다.
    - 만약 PyPy로 실행하고자 한다면 pure-python implementation을 사용해야한다.
    - `UvicornWorker`대신 `UvicornH11Worker`를 사용하면 된다.

  ```bash
  $ gunicorn -w 4 --worker-class uvicorn.workers.UvicornH11Worker
  ```

  - 옵션

    - `main:app`: `main`은 실행하려는 python module 이름을 이고, `app`은 fastapi application의 이름이다.

    - `--workers`: 실행하려는 uvicorn worker의 개수를 적는다.
    - `--worker-class`: worker process로 사용하려는 worker class를 입력한다.
    - `--bind`: gunicorn이 요청을 받은 IP와 port를 입력한다.

  - uvicorn 역시 process manager로 사용하는 것이 가능하다.

    - 그러나 worker process들을 관리하는 능력이 아직까지는 gunicorn에 비해 제한적이므로 gunicorn을 process manager로 사용하는 것이 더 낫다.
    - 그러나 최근 버전에서는 uvicorn에도 여러 관리 기능이 추가되어, uvicorn만 사용해도 무방하다.

  ```bash
  $ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
  ```



- Gunicorn 설정
  - `worker_class`
    - 사용할 worker의 type을 설정한다.
    - `sync`, `eventlet`, `gevent`, `tornado`, `gthread` 중 하나의 값을 받는다.
    - 혹은 `gunicorn.workers.base.Worker`를 상속 받는 custom worker를 입력할 수도 있다.
    - `--worker-class`(`-k`)로 설정한다.
  - `workers`
    - Request를 처리하기 위한 worker의 개수를 설정한다(기본값은 1).
    - Gunicorn은 4-12개의 worker 만으로 초당 수백개에서 수천개의 요청을 처리할 수 있으므로, 지나치게 많은 수의 worker를 설정하는 것은 권장하지 않는다.
    - 일반적으로 `(2*<num_cores>) + 1`개가 [권장](https://docs.gunicorn.org/en/latest/design.html#how-many-workers)된다.
    - `--workers`(`-w`)로 설정한다.
  - `worker_connections`
    - Worker process 당 동시에 허용할 수 있는 connection의 개수를 설정한다.
    - 오직 worker type이 `gthread`, `eventlet`, `gevent`일 때만 유효하다.
    - `--worker-connections`로 설정한다.




- Gunicorn Logging

  - `--log-config` 옵션으로 logging을 위한 configuration 파일을 지정할 수 있다.
  - Python logging mudule과 동일한 형식으로 configuration 파일을 작성하면 된다.
    - `gunicorn.access` logger로 gunicron의 access log를 처리하고, `gunicorn.error` logger로 gunicorn의 error log를 처리한다.

  ```conf
  # logging.conf
  [loggers]
  keys=root,gunicorn.access
  
  [handlers]
  keys=consoleHandler
  
  [formatters]
  keys=simpleFormatter
  
  [logger_root]
  level=INFO
  handlers=consoleHandler
  
  [logger_gunicorn.access]
  level=INFO
  handlers=consoleHandler
  qualname=gunicorn.access
  
  [handler_consoleHandler]
  class=StreamHandler
  level=INFO
  formatter=simpleFormatter
  args=(sys.stdout,)
  
  [formatter_simpleFormatter]
  format=%(asctime)s - %(levelname)s - %(name)s - %(message)s
  ```

  - Fastapi app 생성

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  @app.get("/")
  def hello():
      return
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - Gunicorn으로 app 실행

  ```bash
  $ gunicorn main:app --bind 0.0.0.0:8080  --worker-class uvicorn.workers.UvicornWorker --log-config logging.conf
  ```

  - log 확인

  ```bash
  $ curl localhost:8080
  # 2023-06-21 10:26:44,125 - INFO - uvicorn.access - 127.0.0.1:12345 - "GET / HTTP/1.1" 200
  ```

  - 특정 endpoint로 들어오는 log 필터링하기
    - Endpoint를 특정할 수는 없으나 아래와 같이 Python logging 모듈의 filter기능을 사용하여 record 기반으로 필터링할 수 있다.
    - 아래와 같이 함수를 추가해줘도 되고, `logging.Filter`를 상속 받는 class를 지정해줘도 된다.
    - 단 class를 지정해줄 경우 반드시 `filter` 메서드를 가지고 있어야한다.
    - 주의할 점은 `gunicorn.access`가 아닌 `uvicorn.access`에 설정해줘야한다는 점이다.

  ```python
  from fastapi import FastAPI
  import logging
  import uvicorn
  
  
  class MyFilter(logging.Filter):
      def filter(self, record):
          return "GET / HTTP/1.1" not in record.getMessage()
  
  def filter(record):
      return "GET / HTTP/1.1" not in record.getMessage()
  
  # 함수를 사용할 경우
  logging.getLogger("uvicorn.access").addFilter(filter)
  # class를 사용할 경우
  logging.getLogger("uvicorn.access").addFilter(MyFilter())
  
  app = FastAPI()
  
  
  @app.get("/")
  def test():
      return
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```





