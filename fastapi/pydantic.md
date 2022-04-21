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



- pydantic의 Dict type에 key, value 타입 지정하기

  - 리스트의 첫 번째 요소에 key의 type, 두 번째 요소에 value의 type을 입력한다.

   ```python
   from pydantic import BaseModel
   from typing import Dict
    
   class Foo(BaseModel):
       foo: Dict[str, int]
   ```

  - key 혹은 value의 값을 제한하기
      - Enum을 사용한다.
      - `Element`에 정의된 값만 받게 된다.

  ```python
  from pydantic import BaseModel
  from typing import Dict
  from enum import Enum
    
  class Element(Enum):
      RED="red"
      GREEN="green"
      YELLOW="yellow"
    
  class Foo(BaseModel):
      foo: Dict[str, Element]
  ```



- List  element들의 유효성 검증하기

  - 아래와 같이 배열에 일정한 값들이 담겨서 와야 할 때가 있다.

  ```json
  {
      "fruits":["apple", "orange", "banana"]
  }
  ```

  - 아래와 같이 model을 정의한다.
    - 정의한 배열에 있는 요소가 요청에서 빠져 있어도 유효한 것으로 판단한다.
    - 그러나 배열에 없는 요소가 요청으로 들어올 경우 유효하지 않은 것으로 판단한다.

  ```python
  from pydantic import BaseModel
  from typing import List, Optional, Literal
  
  
  class Fruit(BaseModel):
      fruits: Optional[List[Literal['apple', 'orange', 'banana']]]
  ```



- validation하기

  - pydantic에서 제공하는 `@validator` 데코레이터를 사용한다.
    - 첫 번째 인자로는 class 자체를 받는다.
    - 두 번째 인자는 검증 대상 필드를 받는다.
    - 세 번째 인자는 검증 대상 필드를 제외한 다른 필드들의 정보를 받는다.

  ```python
  from pydantic import BaseModel, ValidationError, validator
  
  
  class UserModel(BaseModel):
      name: str
      username: str
      password1: str
      password2: str
  
      @validator('name')
      def name_must_contain_space(cls, v):
          if ' ' not in v:
              raise ValueError('must contain a space')
          return v.title()
  
      @validator('username')
      def username_alphanumeric(cls, v):
          assert v.isalnum(), 'must be alphanumeric'
          return v
      
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



- pydantic validator 재사용하기

  - pydantic에서  한 class 내의 validation 함수 이름은 중복될 수 없다.
  - 두 개의 필드에 대해서 `change_to_str`라는 같은 이름의 validation 함수를 사용하면 error가 발생한다.

  ```python
  from datetime import date
    
    
  class MyRange(pyd.BaseModel):
      gte:date
      lte:date
  
      @pyd.validator('gte')
      def change_to_str(cls, v):
          return v.strftime('%Y-%m-%d')
  
      @pyd.validator('lte')
      def change_to_str(cls, v):
          return v.strftime("%Y-%m-%d")
  ```

  - 위와 같이 정확히 동일하게 동작하는 validate을 여러 필드에 해줘야 할 경우

  ```python
  from datetime import date, timedelta
  from pydantic import BaseModel, validator
  
  def change_to_str(date_param: date) -> str:
      return date_param.strftime("%Y-%m-%d")
  
  class MyRange(BaseModel):
      gte:date
      lte:date
  
      str_gte = validator('gte', allow_reuse=True)(change_to_str)
      str_lte = validator('lte', allow_reuse=True)(change_to_str)
  
  my_range = MyRange(gte=date.today()-timedelta(days=1), lte=date.today())
  print(my_range.gte)		# 2022-03-04
  print(my_range.lte)		# 2022-03-05
  ```

  - class 내의 모든 field에 하나의 validation 적용하기
    - class 내의 모든 field에 하나의 validation 적용하기

  ```python
  from datetime import date, timedelta
  from pydantic import BaseModel, root_validator
  
  
  class MyRange(BaseModel):
      gte:date
      lte:date
  
      @root_validator
      def change_to_str(cls, values):
          return {key:value.strftime("%Y-%m-%d") for key,value in values.items()}
  ```





- Enum class 사용하기

  - `use_enum_values`를 `True`로 주면, 자동으로 Enum 클래스의 value를 할당한다.

  ```python
  from enum import Enum
  from pydantic import BaseModel
  
  class Gender(str, Enum):
      MALE = "male"
      FEMALE = "female"
  
  class Student(BaseModel):
      name:str
      gender:Gender
  
      class Config:  
          use_enum_values = True
  
  student = Student(name="Kim", gender='male')
  print(student.dict())
  ```

  
