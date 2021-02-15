# DB와 Django 연동하기

- Django는 기본적으로 sqlite3를 사용하는데 다른 DB와 연동해서 사용이 가능하다.
  - 아래 예시에서는 MariaDB를 사용할 것이다.





## DB 설치하기

- 사용하고자 하는 DB 설치(예시의 경우 MariaDB)

  > https://downloads.mariadb.org/mariadb/10.3.8/

  - 위 사이트에서 원하는 버전 선택 후 설치
  - 중간계 root 사용자의 비밀번호를 설정하고 기억해 둔다.



- 실행해보기
  - MySQL Client(시작 창에서 검색하면 나온다)를 실행하여 설치시 설정했던 root 비밀번호를 입력하면 MariaDB에 접속된다.





## DB 연동하기

- `mysqlclient` 설치하기

  ```bash
  $pip install mysqlclient
  ```



- settings.py 수정하기

  ```python
  # 기존 DATABASES는 아래와 같이 되어 있는데
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }
  }
  
  # 아래와 같이 수정한다.
  DATABASES = {
      'default': {
          'ENGINE':'django.db.backends.mysql',
          'NAME':'react',      # database명 입력
          'USER':'root',       # 사용자명 입력
          'PASSWORD':'1234',
          'HOST':'127.0.0.1',  # 사용하려는 host 입력
          'PORT':3306,         # 사용하려는 port 입력
      }
  }
  ```




- DB 설정은 비공개적이어야 하므로 이를 저장하기 위한 secrets.json 파일을 생성한다.

  - DB 설정 외에도 비공개적으로 관리할 데이터는 이곳에 저장한다.

  ```json
  {
      "DB_SETTINGS":{
          "default": {
              "ENGINE": "django.db.backends.mysql",
              "NAME": "inna",
              "USER": "root",
              "PASSWORD": "qwer",
              "HOST": "127.0.0.1",
              "PORT": 3306
          }
      }
  }
  ```

  - settings.py에 아래 코드를 추가

  ```python
  import os
  import json
  
  
  # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
  with open(os.path.join(BASE_DIR, 'secrets.json'), 'rb') as secret_file:
      secrets = json.load(secret_file)
  
  (...)
  
  DATABASES = secrets['DB_SETTINGS']
  ```

  - `.gitignore` 파일에 `/설정폴더/secrets.json` 추가



- migrate하기

