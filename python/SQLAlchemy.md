# 개요

- ORM(Object Relational Mapper)
  - Class 또는 object로 이루어진 코드와 SQL을 변환해주는 libarary를 ORM이라 부른다.
    - Object란 class와 그 instance로 이루어진 코드를 의미하며, OOP의 object와 동일한 개념이다.
    - Relational이란 SQL DB를 의미한다.
    - Mapper란 수학에서 어떤 것을 특정 집합으로부터 다른 집합으로 변환하는 것을 mapping function이라 부르는데, 이 개념을 가져온 것이다.
  - 다양한 ORM library가 있다.



- SQLAlchemy

  - SQL toolkit 겸 ORM이다.
    - Python에서 database를 다루기 위한 다양한 기능을 제공한다.
  - 크게 SQLAlchemy core와 SQLAlchemy ORM으로 구성된다.
    - Core는 DB toolkit으로써의 SQLAlchemy를 구성하는 부분으로 DB와의 연결을 관리하고 DB와 상호작용하는 것과 관련되어 있다.
    - ORM은 ORM으로써의 SQLAlchemy를 구성하는 부분으로 Python class를 DB table로 mapping하는 역할을 한다.
  - 설치
    - SQLAlchemy 2.0부터는 Python 3.7 이상을 요구한다.

  ```bash
  $ pip install SQLAlchemy
  ```



- DB와 연결하기

  - `Engine`을 사용하여 DB와 연결이 가능하다.
    - DB와의 connection을 생성하는 factory와 connection pool을 제공한다.
    - 일반적으로 특정 DB server에 대해 한 번만 생성하여 전역 객체로 사용한다.
  - `create_engine`을 사용하여 `Engine`을 생성할 수 있다.
    - `create_engine`은 DB의 종류(예시에서는 `sqlite`), 사용할 DBAPI(예시에서는 `pysqlite`), 그리고 DB의 접속 정보를 받는다.
    - `echo`는 SQL을 Python logger에 기록하도록 하는 옵션이다.

  ```python
  from sqlalchemy import create_engine
  
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  ```

  - Lazy connecting
    - `create_engine`을 통해 반환 된 `Engine`은 DB와 바로 연결하지는 않는다.
    - Lazy initialization pattern을 적용하여 처음으로 DB에 어떤 작업을 요청할 때 DB와 연결한다.



- DB와 연결하기

  - `Engine`의 주요 목적은 `Connection`이라 불리는 DB와의 연결을 제공하는 것이다.
  - `Connection`는 DB에 대한 open resource를 나타내기 때문에, `Connection` object가 사용되는 scope를 제한해야 한다.
    - 따라서 일반적으로 Python의 context manager와 함께 사용한다.
    - Python DBAPI의 기본 동작은 connection의 scope가 release되면 ROLLBACK이 일어나는 것이다.
    - 즉 transaction은 자동으로 commit되지 않는다.
    - commit을 원하면 명시적으로 commit을 실행해야 한다.

  ```python
  from sqlalchemy import create_engine, text
  
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  with engine.connect() as conn:
  	result = conn.execute(text("select 'hello world'"))
  	print(result.all())
      
  """
  2024-05-31 11:06:46,723 INFO sqlalchemy.engine.Engine BEGIN (implicit)
  2024-05-31 11:06:46,723 INFO sqlalchemy.engine.Engine select 'hello world'
  2024-05-31 11:06:46,723 INFO sqlalchemy.engine.Engine [generated in 0.00028s] ()
  [('hello world',)]
  2024-05-31 11:06:46,723 INFO sqlalchemy.engine.Engine ROLLBACK
  """
  ```

  - 변경 사항 commit하기
    - 앞서 살펴본 것 처럼 DBAPI는 자동으로 commit하지 않는다.
    - 따라서 commit을 위해서는 transaction을 commit하는 `commit()` 메서드를 호출해야 한다.
    - 이 방식을 commit as you go 방식이라 부른다.

  ```python
  from sqlalchemy import create_engine, text
  
  
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  with engine.connect() as conn:
      conn.execute(text("CREATE TABLE some_table (x int, y int)"))
      conn.execute(
          text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
          [{"x": 1, "y": 1}],
      )
      conn.commit()
  
  """
  2024-05-31 11:35:26,564 INFO sqlalchemy.engine.Engine BEGIN (implicit)
  2024-05-31 11:35:26,565 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
  2024-05-31 11:35:26,565 INFO sqlalchemy.engine.Engine [generated in 0.00032s] ()
  2024-05-31 11:35:26,565 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
  2024-05-31 11:35:26,565 INFO sqlalchemy.engine.Engine [generated in 0.00018s] (1, 1)
  2024-05-31 11:35:26,566 INFO sqlalchemy.engine.Engine COMMIT
  """
  ```

  - `begin()` method를 사용하면 `commit()` 메서드를 호출하지 않아도 context가 종료될 때 commit이 실행된다.
    - block 내의 내용이 성공적으로 수행됐다면 commit을 실행하고 exception이 발생했다면 rollback을 실행한다.
    - 이 방식을 begin once라 부른다.

  ```python
  from sqlalchemy import create_engine, text
  
  
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  with engine.begin() as conn:
      conn.execute(text("CREATE TABLE some_table (x int, y int)"))
      conn.execute(
          text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
          [{"x": 6, "y": 8}],
      )
      
  """
  2024-05-31 11:46:52,839 INFO sqlalchemy.engine.Engine BEGIN (implicit)
  2024-05-31 11:46:52,840 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
  2024-05-31 11:46:52,840 INFO sqlalchemy.engine.Engine [generated in 0.00020s] ()
  2024-05-31 11:46:52,841 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
  2024-05-31 11:46:52,841 INFO sqlalchemy.engine.Engine [generated in 0.00017s] [(6, 8), (9, 10)]
  2024-05-31 11:46:52,841 INFO sqlalchemy.engine.Engine COMMIT
  """
  ```



- 문(statement) 실행 기초

  - 데이터 조회하기
    - 데이터 조회의 결과로 `Result` 객체가 반환되며, 이 객체는 `Row`객체들을 담고 있다.

  ```python
  with engine.connect() as conn:
      result = conn.execute(text("SELECT x, y FROM some_table"))
      print(type(result))		# <class 'sqlalchemy.engine.cursor.CursorResult'>
      print(result)			# <sqlalchemy.engine.cursor.CursorResult object at 0x7fef70577ca0>
      for row in result:
          print(f"x: {row.x}  y: {row.y}")
  ```

  - `Row` 조회하기
    - `Row`는 아래와 같이 다양한 방법으로 조회가 가능하다.
    - `Row`는 Python의 named tuple과 유사하게 동작하도록 설계되어 있다.

  ```python
  with engine.connect() as conn:
      result = conn.execute(text("SELECT x, y FROM some_table"))
      for row in result:
          # tuple assignment
          x, y = row
          print(f"x: {x}  y: {y}")
          # index로 접근
          print(f"x: {row[0]}  y: {row[1]}")
          # attribute로 접근
          print(f"x: {row.x}  y: {row.y}")
      
      # mapping object로 접근
      for dict_row in result.mappings():
          print(dict_row)
  ```

  - Parameter 전송하기
    - SQL문은 함께 전달되어야 하는 data를 가지고 있는 경우가 있는데, SQLAlchemy는 이를 위한 기능을 제공한다.
    - Parameter의 이름 앞에 `:`을 붙이고, parameter는 dictionary 형태로 넘긴다.
    - Log로 남은 SQL output을 확인해 보면 parameter `:y`가 `?`로 표시된 것을 볼 수 있는데, 이는 SQLite가 qmark parameter style이라 불리는 format을 사용하기 때문이다.
    - DBAPI specification은 parameter에 대해서 총 6가지 format을 정의하고 있는데, qmark parameter style도 그 중 하나이다.
    - SQLAlchemy는 6가지 format을 추상화하여 `:`을 사용하는 하나의 format으로 사용할 수 있게 해준다.

  ```python
  with engine.connect() as conn:
      result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 8})
      for row in result:
          print(f"x: {row.x}  y: {row.y}")
          
          
  """
  2024-05-31 13:50:38,208 INFO sqlalchemy.engine.Engine BEGIN (implicit)
  2024-05-31 13:50:38,209 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
  2024-05-31 13:50:38,209 INFO sqlalchemy.engine.Engine [generated in 0.00019s] ()
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine [generated in 0.00019s] [(6, 8), (9, 10)]
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine COMMIT
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine BEGIN (implicit)
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ?
  2024-05-31 13:50:38,210 INFO sqlalchemy.engine.Engine [generated in 0.00018s] (8,)
  x: 9  y: 10
  2024-05-31 13:50:38,211 INFO sqlalchemy.engine.Engine ROLLBACK
  """
  ```

  - 여러 개의 parameter 전달하기
    - INSERT, UPDATE, DELETE 등의 DML은 여러 parameter를 전달해야 하는 경우가 있다.
    - 이 경우 `list[dict]` 형태로 전달하면 된다.

  ```python
  with engine.connect() as conn:
      conn.execute(
          text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
          [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
      )
      conn.commit()
  ```

  - ORM Session을 사용하여 문 실행하기
    - `Session`은 ORM을 사용할 때 기초가 되는 객체이다.
    - `Connection`과 매우 유사하며, `Session`은 내부적으로 `Connection`을 사용한다.
    - ORM 없이 `Session`을 사용할 경우 `Session`은 `Connection`을 사용하는 것과 큰 차이는 없다.
    - 아래 예시는 위에서 `Connection`을 사용했던 예시에서 `Connection`대신 `Session`을 사용하도록 바꾼것이다.

  ```python
  from sqlalchemy.orm import Session
  
  with Session(engine) as session:
      result = session.execute(text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y"), {"y": 8})
      for row in result:
          print(f"x: {row.x}  y: {row.y}")
  ```

  - `Session` 역시 `Connection`과 마찬가지로 "commit as you go" 방식을 사용한다.
    - 즉, 자동으로 commit하지 않는다.
    - 따라서 commit을 위해서는 수동으로 `Session.commit()`을 호출해야 한다.
    - `Session` 객체는 transaction이 종료된 후에는 더 이상 `Connection` 객체를 가지고 있지 않으며, 새로운 SQL을 실행해야 할 때 다시 `Engine`으로부터`Connection`을 받아온다.

  ```python
  with Session(engine) as session:
      result = session.execute(
          text("UPDATE some_table SET y=:y WHERE x=:x"),
          [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
      )
      session.commit()
  ```

