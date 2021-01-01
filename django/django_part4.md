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

  

- migrate하기

