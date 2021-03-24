# FastAPI 튜토리얼

- 특징
  - 빠름:  Starlette과 Pydantic 덕분에 NodeJS 및 Go와 대등할 정도로 매우 높은 성능을 지녔다.
  - 빠른 코드 작성: 200~300%까지 개발 속도 증가
  - 적은 버그: 개발자에 의한 에러 40% 감소
  - 직관적: 훌륭한 편집기 지원, 모든 곳에서 자동완성, 적은 디버깅 시간.
  - 쉬움: 쉽게 사용하고 배우도록 설계.
  - 짧음: 코드 중복 최소화, 각 매개변수 선언의 여러 기능.



- 설치하기

  - Python 3.6 이상부터 사용 가능하다.
  - fastapi 설치

  ```bash
  $ pip install fastapi
  ```

  - uvicorn 설치

  ```bash
  $ pip install uvicorn[standard]
  ```



- 만들기

  - main.py 파일 생성

  ```python
  from typing import Optional
  from fastapi import FastAPI
  
  # application 생성
  app = FastAPI()
  
  @app.get("/")
  def read_root():
      return {"Hello":"World"}
  
  @app.get("/items/{item_id}")
  # int형 이어야 하는 경로 매개변수와 str형 이어야 하는 경로 매개변수 q를 받는다.
  def read_item(item_id: int, q: Optional[str]=None):
      return {"item_id": item_id, "q": q}
```
  
  - 서버 실행하기
    - 위 코드에서 `app = FastAPI()`로 생성된 app을 명령어로 넣는다.
  - `--reload`는 코드가 변경된 후 서버를 재시작하는 명령어이다.
  
  ```bash
  # uvicorn 파일명:FastAPI()로 생성한 객체 --reload
  
  $ uvicorn main:app --reload
```
  
- 요청 보내기
  
  ```json
  GET 127.0.0.1:8000/items/5?q=Theo
  
  {
      "item_id": 5,
      "q": "Theo"
  }
  ```



- API 문서
  - 대화형 API 문서
    -  주소 뒤에 `/docs`를 입력하면 대화형 API 문서로 접속이 가능하다.
  - 대안 API 문서
    - 주소 뒤에 `/redoc`을 입력하면 대화형 API 문서로 접속이 가능하다.
  - 코드가 변경되면 문서도 자동으로 업그레이드 된다.



- Request Body를 함께 보내기

  - `pydantic`을 활용한다.

  ```python
  from typing import Optional
  from fastapi import FastAPI
  from pydantic import BaseModel
  
  app = FastAPI()
  
  class Item(BaseModel):
      name: str
      price: float
      is_offer:Optional[bool] = None
  
  # (...중략...)
  
  
  @app.put("/itmes/{item_id}")
  def update_item(item_id: int, item: Item):
      return {"item_name":item.name, "item_id": item_id}
  ```






