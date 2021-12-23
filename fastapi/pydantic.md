# 개요

- Pydantic
  - 데이터 유효성 검사 및 python type annotation을 사용한 설정 관리를 제공한다.
  - 런타임에 type hint를 적용하고, 데이터가 유효하지 않을 때 사용자에게 에러를 제공한다.
  - 순수하고 표준적인 Python에서 data를 어떻게 다뤄야 하고, 잘 다루고 있는지 검증하고자 할 때 사용한다.



- 설치하기

  - Python 3.6 이상이 요구된다.
  - pip

  ```bash
  $ pip install pydantic
  ```

  - conda

  ```bash
  $ conda install pydantic -c conda-forge
  ```



- 예시

  - `pydantic`에서 `BaseModel`을 import한다.
  - `BaseModel`을 상속받는 `User` 클래스를 작성한다. 
    - 클래스 내부에는 각 속성들의 type 혹은 기본값을 지정한다.
  - 기본값 없이 type만 지정
    - id는 기본값 없이 type만 지정해줬으므로 required 값이 된다.
    - String, floats이 들어오는 경우 int로 변환이 가능하다면 int로 변환된다.
    - 만일 int로 변환이 불가능하다면 exception이 발생한다.
  - type 없이 기본값만 지정
    - name은 type 없이 기본값만 지정해줬으므로 optional한 값이 된다.
    - 또한 기본값으로 지정해준 값이 문자열이므로 type은 string이 된다.
  - type과 기본값을 모두 지정
    - signup_ts, friends는 타입과 기본값을 모두 지정해주었으므로 optional한 값이 된다.
    - friends의 경우 int가 들어있는 list이므로 만일 string이나 floats이 int로 변환 가능하다면 변환되게 되고, 불가능하다면 exception이 발생한다.

  ```python
  from datetime import datetime
  from typing import List, Optional
  from pydantic import BaseModel
  
  
  class User(BaseModel):
      id: int
      name = 'Theo'
      signup_ts: Optional[datetime] = None
      friends: List[int] = []
  
  
  external_data = {
      'id': '123',
      'signup_ts': '2019-06-01 12:22',
      'friends': [1, 2, '3'],
  }
  user = User(**external_data)
  print(user.id)
  # 123
  print(repr(user.signup_ts))
  # datetime.datetime(2019, 6, 1, 12, 22)
  print(user.friends)	
  # [1, 2, 3]
  print(user.dict())	
  # {'id': 123, 'signup_ts': datetime.datetime(2019, 6, 1, 12, 22), 'friends': [1, 2, 3], 'name': 'John Doe'}
  ```



- `ValidationError`

  - 만일 class에서 설정해준 타입이 들어오지 않을 경우 pydantic 패키지에 포함된 `ValidationError`가 발생하게 된다.

  ```python
  from pydantic import ValidationError
  
  try:
      User(signup_ts='broken', friends=[1, 2, 'not number'])
  except ValidationError as e:
      print(e.json())
  ```

  - output
    - `ValidationError`에는 에러가 발생한 위치, message, type 등이 담겨 있다.
    - list의 경우 `loc` 에는 몇 번째 인덱스에서 문제가 생긴 것인지도 담겨 있다. 

  ```json
  [
    {
      "loc": [
        "id"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "signup_ts"
      ],
      "msg": "invalid datetime format",
      "type": "value_error.datetime"
    },
    {
      "loc": [
        "friends",
        2
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
  ```



- List  element들의 유효성 검증하기

  - 아래와 같이 배열에 일정한 값들이 담겨서 와야 할 때가 있다.

  ```json
  {
      "fruits":["apple", "orange", "banana"]
  }
  ```

  - 아래와 같이 model을 정의한다.
    - 정의한 배열에 있는 요소들이 요청으로 들어오지 않아도 유효한 것으로 판단한다.
    - 그러나 배열에 없는 요소가 요청으로 들어올 경우 유효하지 않은 것으로 판단한다.

  ```python
  from pydantic import BaseModel
  from typing import List, Optional, Literal
  
  
  class Fruit(BaseModel):
      fruits: Optional[List[Literal['apple', 'orange', 'banana']]]
  ```





