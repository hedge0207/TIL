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





## Session

- Session
  - `Session`은 아래와 같은 역할을 한다.
    - Connection에 대한 transaction 확립.
    - 통신이 유지되는 동안 load했거나, load한 것과 관련된 모든 객체들의 holding zone.
    - ORM 매핑 개체를 반환하거나 수정하는 SELECT 및 기타 쿼리가 수행되는 인터페이스 제공.
  - `Session`은 대부분의 경우 stateless 상태로 생성된다.
    - `Session`은 필요할 때 마다 `Engine`에 connection을 요청하여 받아오고 해당 connection에 대한 transaction을 확립한다.
    - 그 후 DB로 부터 data를 load하여 data를 가지게 된다.
    - 이렇게 확립된 transaction은 transaction에 commit이나 rollback이 발생할 때 까지만 유지된다.
    - Transaction이 종료되면 connection은 release되어 connection pool로 돌아간다.
  - `Session`에 의해 관리되는 ORM 객체들은 `Session`에 의해 계측(instrumented)된다.
    - Instrumentation이란 특정 class의 method 및 attribute 집합을 확장하는 과정을 말한다.
    - 즉 Python program에서 attribute가 변화할 경우 `Session`은 이 변화를 기록한다.
    - Database에 query를 실행되려 하거나 transaction이 commit되려할 때, `Session`은 먼저 memory에 저장된 모든 변경사항들을 database로 flush한다.
    - 이를 unit of work pattern이라 한다.
  - Detached
    - Object가 `Session`안에서 가질 수 있는 상태 중 하나이다.
    - Detached object는 database identity(primary key)를 가지고는 있지만 어떤 session과도 관련이 없는 object를 의미한다.
    - `Session`에 속해 있던 object는 속해있던 `Session`이 close되거나 object가 말소되는 경우에 detached object가 된다.
    - 일반적으로 detach 상태는 session간에 object를 옮기기 위해 사용한다.
  - Transient object, Persistent object
    - Session에 의해 load된 object를 persistent object라 부른다.
    - Session에 의해 load되지 않은 object를 transient object라 부른다.



- Session 개요

  - `Session` 생성하기
    - `Session`은 자체적으로 생성하거나, `sessionmaker` class를 사용하여 생성할 수 있다.
    - 생성시에 `Engine`을 전달해줘야 한다.

  ```python
  from sqlalchemy import create_engine
  from sqlalchemy.orm import Session
  
  # engine 생성
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  
  # session 생성
  session = Session(engine)
  ```

  - Python의 context manager를 사용하면 `Session`이 자동으로 닫히도록 할 수 있다.
    - `Session.close()`를 호출하지 않아도, `with` block이 끝날 때 session도 함께 닫힌다.

  ```python
  with Session(engine) as session:
      ...
  ```

  - Commit
    - `Session`은 닫힐 때 변경사항을 자동으로 commit하지 않으므로, `Session.commit()` method를 통해 수동으로 commit을 실행해야한다.
    - 주의할 점은 `Session.commit()`이 호출된 후에는 `Session`과 관련되어 있단 모든 object들이 만료된다는 점이다.
    - 단, `Session.expire_on_commit` flag를 False로 설정하여 만료되지 않게 할 수 있다.

  ```python
  with Session(engine) as session:
      # ...
      session.commit()
  ```

  - Rollback
    - 현재 transaction을 roll back한다.

  ```python
  with Session(engine) as session:
      # ...
  	session.rollback()
  ```

  - begin, commit, rollback
    - 만약 모든 operation이 성공하면 commit을 수행하고, 하나라도 실패하면 rollback되기를 원한다면, 아래와 같이 작성하면 된다.

  ```python
  # 풀어서 작성하면 아래와 같다.
  with Session(engine) as session:
      session.begin()
      try:
          session.add(some_object)
          session.add(some_other_object)
      except:
          session.rollback()
          raise
      else:
          session.commit()
          
  # context manager를 중첩하여 작성하면, 보다 간결하게 작성이 가능하다.
  with Session(engine) as session:
      with session.begin():
          session.add(some_object)
          session.add(some_other_object)
          
  # 두 개의 context를 결합하면 보다 간결하게 작성이 가능하다.
  with Session(engine) as session, session.begin():
      session.add(some_object)
      session.add(some_other_object)
  ```

  - Auto Begin
    - `Session` 내에서 어떤 작업이 수행될 경우, `Session`은 transactional state로 자동으로 변환된다.
    - 즉 `Session.add()` 혹은 `Session.execute()` 등이 호출되거나 `Query`가 실행되거나 persistent object의 attribute가 수정되면 `Session`은 transactional state로 자동으로 변환된다.
    - `Session.in_transaction()` method를 통해 transactional state인지 확인이 가능하다.
    - `Session.begin()` 메서드를 호출하여 `Session`을 transactional state로 수동으로 전환시키는 것도 가능하다.

  ```python
  with Session(engine) as session:
      print(session.in_transaction())					# False
      session.execute(text("select 'hello world'"))
      print(session.in_transaction())					# True
  ```

  - 아래와 같이 Autobegin을 비활성화 하는 것도 가능하다.
    - `autobegin` parameter를 False로 넘긴다.
    - 이 경우 명시적으로 `Session.begin()` method를 호출해야한다.

  ```python
  with Session(engine, autobegin=False) as session:
      session.begin()
  ```

  - `sessionmaker` 생성하여 `Session` 객체 생성하기
    - `sessionmaker`는 `Session` object를 고정된 configuraion으로 생성하기 위한 factory를 제공한다.
    - 일반적으로 function level의 session/connection을 위한 module 단위의 factory로 사용한다.

  ```python
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker
  
  # engine 생성
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  
  # session 생성
  Session = sessionmaker(engine)
  ```

  - `sessionmaker`는 `Engine`과 마찬가지로 `begin()` method를 지원하며, `begin()` method는 `Session` object를 반환한다.
    - begin, commit, rollback을 명시하지 않아도 context manager block 내에서 자동으로 실행된다.

  ```python
  with Session.begin() as session:
      session.add(some_object)
      session.add(some_other_object)
  ```

  - Application을 작성할 때, `sessionmaker`는 `create_engine()` method에 의해 생성된 `Engine` object와 같은 scope를 가지는 것이 좋다.
    - 일반적으로 module 혹은 global scope를 가진다.
    - 두 객체 모두 factory이기 때문에, 여러 함수와 thread들에서 동시에 사용할 수 있다.
  - Close
    - `Session.close()` method는 `Session.expunge_all()` method를 호출하여 모든 ORM-mapped object를 session에서 삭제하고, `Engine`으로 부터 받아온 transaction/connection 관련된 자원들을 반환한다.
    - Connection이 connection pool로 반환될 경우, transactional state 역시 roll back된다.
    - 기본적으로, `Session`이 close되면 처음 생성됐던 것 같이 깨끗한 상태가 되는데, 이런 관점에서 `Session.reset()`은 `Session.close()`과 유사하다.
    - 이러한 close의 기본 동작 방식은 `Session.close_resets_only` parameter를 False로 줌으로써 변경이 가능하다.
    - `Session`을 context manager와 함께 사용할 경우 `Session.close()`를 명시적으로 호출하지 않아도 된다.

  ```python
  with Session(engine) as session:
      result = session.execute(select(User))
      
  # session이 자동으로 close된다.
  ```



- Session을 통해 DB의 data다루기

  - 조회하기
    - `select()` method를 사용하여 `Select` object를 생성하고, `Select` object를 사용하여 data를 조회한다.

  ```python
  from sqlalchemy import select
  from sqlalchemy.orm import Session
  
  with Session(engine) as session:
      # User object를 조회하기 위한 query
      statement = select(User).filter_by(name="ed")
  
      # User object들 조회하기
      user_obj = session.scalars(statement).all()
  
      # 개별 column들을 조회하기 위한 query
      statement = select(User.name, User.fullname)
  
      # Row object들 조회하기
      rows = session.execute(statement).all()
  ```

  - Primary key로 조회하기
    - `Session.get()` method를 사용하여 primary key로 조회가 가능하다.	

  ```python
  my_user = session.get(User, 5)
  ```

  - 삽입하기
    - `Session.add()` method는 session에 instance를 배치하기 위해 사용한다.
    - `Session.add()`를 통해 session에 배치된 instance는 다음 flush 때 INSERT 된다.
    - Persistent instance(session에 의해 이미 load된 instance)는 add할 필요가 없다.
    - Detached instance(session에서 제거된 instance)는 `Session.add()`를 통해 다시 `Session`에 배치되게 된다.
    - `Session.add_all()` method를 통해 여러 data를 추가하는 것도 가능하다.

  ```python
  user1 = User(name="foo")
  session.add(user1)
  
  user2 = User(name="bar")
  user3 = User(name="baz")
  session.add_all([user2, user3])
  session.commit()
  ```

  - 삭제하기
    - `Session.delete()` method를 통해 `Session`의 객체 목록에서 삭제되었다는 표시를 추가한다.
    - 삭제 표시가 있는 object들은 flush 이전까지는 `Session.deleted`에서 확인이 가능하다.
    - 실제로 삭제가 일어난 후에는 `Session`에서 말소된다.

  ```python
  # Session의 object 목록에서 obj1과 obj2가 삭제되었다는 표시를 한다.
  session.delete(obj1)
  session.delete(obj2)
  
  session.commit()
  ```

  - Flushing
    - Flush는 transaction을 DB로 전송하는 것을 의미하며, flush가 실행되도 commit이 되지 않았기 때문에 DB에 적용은 되지 않는다.
    - `Session`을 기본 설정으로 사용할 경우, flush는 항상 자동으로 실행된다.
    - `Session.flush()`를 사용하여 수동으로 실행하는 것도 가능하다.
    - `Session`을 생성할 때 flush의 자동 실행을 비활성화 하는 것도 가능하다.

  ```python
  session.flush()
  
  Session = sessionmaker(autoflush=False)
  ```



- Autoflush
  - 특정 method의 scope에서 자동으로 발생하는 flush를 의미한다.
    - 언제 자동으로 발생시킬지 설정이 가능하다.
  - 아래와 같은 동작들이 발생하기 전에 실행된다.
    - `Session.execute()` 혹은 SQL-executing method, `select()`와 같이 ORM entitiy 혹은 ORM-mapped attribute들을 참조하는 ORM-enabled SQL constructs가 실행되기 전.
    - Query가 호출되기 전.
    - DB에 조회하기 전에 `Session.merge()`가 실행되기 전.
    - Object들이 refresh되기 전.
    - Load되지 않은 object attribute들에 대해 ORM layz load가 발생하기 전.
  - 아래와 같은 동작들이 실행될 때는 무조건 실행된다.
    - `Session.commit()`이 실행될 때.
    - `Session.begin_nested()`가 호출될 때.
    - `Session.prepare()` 2PC method가 사용될 때. 



- `Session.delete()`와 관련된 몇 가지 중요한 행동들이 있다.
  - 삭제된 object와 `relationship()`을 통해 관계를 형성한 mapped object들은 기본적으로 삭제되지 않는다.
    - 만약 삭제된 object가 다른 object에서 foreign key로 사용되고 있었다면, foreign key의 값이 NULL로 변경된다.
    - 이 때, 만약 foreign key를 저장하던 column에 not null 제약조건이 있다면 제약조건을 위반하게 된다.
  - `relationship.secondary`를 통해 다대다 관계로 생성된 table의 row들은 참조하고 있는 object가 삭제될 경우 함께 삭제된다.
  - 만약 삭제된 object와 관계를 맺고 있는 object에 삭제된 object에 대한 외래 키 제약 조건이 포함되어 있고 해당 object가 속한 관련 컬렉션이 현재 memory에 load되지 않은 경우 unit of work는 기본 키 값을 사용하여 관련된 row들에 대해 UPDATE 또는 DELETE 문을 실행하기 위해 SELECT를 실행하여 관련된 모든 row들을 가져온다.
  - 삭제 표시된 object를 삭제할 경우, 해당 object는 collection들이나 해당 object를 참조하는 object reference에서 삭제되지는 않는다.
    - `Session`이 만료되면 collection들은 다시 load되어 삭제된 object가 더 이상 존재하지 않도록 한다.
    - 그러나 `Session.delete()`를 사용하는 것 보다 먼저 object를 collection에서 제거한 다음 delete-orphan을 사용하여 collection에서 제거된 보조 효과로 삭제되도록 하는 것이 권장된다.



- Expiring과 Refreshing

  - `Session`을 사용할 때 고려해야 할 중요한 사항 중 하나는 DB에서 load된 객체의 상태를 transaction에 있는 현재 객체의 상태와 동기화시키는 것이다.
    - SQLAlchemy ORM은 identity map의 개념을 기반으로 하므로, SQL query를 통해 object가 load될 때 특정 DB의 identity와 알치하는 unique한 Python object가 있어야 한다.
    - 이는 같은 row를 조회하는 두 번의 개별적인 query를 실행할 경우 두 query는 같은 Python object를 반환해야 한다는 의미이다.
    - 이에 따라 ORM은 query를 통해 row들을 가져올 때 이미 load된 객체에 대해서는 attribute를 채워넣지 않는다.
    - 이러한 설계는 완벽하게 격리된 transaction을 가정하고, 만약 transaction이 격리되지 않았다면, application이 DB transaction에서 object를 refesh할 수 있어야 한다고 가정한다.

  ```python
  u1 = session.scalars(select(User).where(User.id == 5)).one()
  u2 = session.scalars(select(User).where(User.id == 5)).one()
  print(u1 is u2)		# True
  ```

  - ORM mapped object가 memory에 load될 때, 해당 object를 내용을 현재 transaction의 내용으로 refresh 할 수 있는 세 가지 방법이 있다.

  - `Session.expire()`
    - 선택된 attribute 혹은 모든 attribute들을 삭제하여 다음에 접근할 때 DB에서 load되도록 한다.
    - Lazy loading pattern을 사용한다.

  ```python
  session.expire(u1)
  u1.some_attribute	# transaction으로부터 lazy load한다.
  ```

  - `session.refresh()`
    - `Session.expire()`가 수행하는 모든 작업을 수행하고, 여기에 더해서 object의 내용을 실제로 refresh하기 위해 하나 이상의 SQL query를 즉시 실행한다.

  ```python
  session.refresh(u1)		# SQL query를 실행한다.
  u1.some_attribute		# transaction으로부터 refresh 된다. 
  ```

  - `execution_options`와 `populate_existing`을 사용하는 방법
    - `populate_existing` option은 `Session` 내부에 load된 모든 instance들이 완전히 refresh 되도록 한다.
    - Object 내에 있는 모든 data들 지우고, load된 data로 다시 채워 넣는다.

  ```python
  u2 = session.scalars(
      select(User).where(User.id == 5).execution_options(populate_existing=True)
  ).one()
  ```



- Session 관리

  - Session의 lifecycle은 특정 data를 처리하는 function의 밖에서 관리해야 한다.
    - 이는 session의 lifecycle관리와 data와 관련된 operation이라는 두 개의 관심사를 분리하기 위함이다.

  ```python
  # 아래와 같이 session의 lifecycle을 data를 처리하는 function 내부에서 관리해선 안 된다.
  class ThingOne:
      def go(self):
          session = Session()
          try:
              session.execute(update(FooBar).values(x=5))
              session.commit()
          except:
              session.rollback()
              raise
  
  class ThingTwo:
      def go(self):
          session = Session()
          try:
              session.execute(update(Widget).values(q=18))
              session.commit()
          except:
              session.rollback()
              raise
  
  def run_my_program():
      ThingOne().go()
      ThingTwo().go()
      
      
      
  # 아래와 같이 외부에서 관리해야 한다.
  class ThingOne:
      def go(self, session):
          session.execute(update(FooBar).values(x=5))
  
  class ThingTwo:
      def go(self, session):
          session.execute(update(Widget).values(q=18))
  
  def run_my_program():
      with Session() as session:
          with session.begin():
              ThingOne().go(session)
              ThingTwo().go(session)
  ```

  - 하나의 session을 여러 thread에서 동시에 사용하거나 asyncio task에서 사용해선 안 된다.
    - Session은 단일 database transaction을 나타낸다.
    - 즉, session은 비동시적인 방식으로 사용되도록 고안되었다.
    - 따라서 여러 곳에서 동시에 사용해선 안 된다.

