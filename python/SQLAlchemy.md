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





## Databasse Metadata

- Metadata

  - Database의 table과 column 등을 표현하는 Python object를 database metadata라고 부른다.

  - SQLAlchemy에서는 `MetaData`, `Table`, `Column`이라는 class를 통해 database medata를 다룰 수 있는 방법을 제공한다.
  - SQLAlchemy에서 table은 `Table`을 통해 직접 구성하거나, ORM Mapped class를 통해 간접적으로 구성할 수 있다.



- `Metadata`를 사용하여 table 생성하기

  - `MetaData` 생성하기
    - `MetaData`는 여러 개의 `Table` object들을 저장하고 있는 Python dictionary의 일종이며, table의 이름을 key로 가진다.
    - `MetaData`는 일반적으로 전체 application에 하나만 생성하고, 전역으로 사용한다.

  ```python
  from sqlalchemy import Metadata
  
  metadata = MetaData()
  ```

  - `MetaData` 객체를 통해 `Table` 객체 생성하기
    - `Table`을 통해 table 객체를 생성하며, table의 column은 `Column`을 통해 선언한다.	

  ```python
  from sqlalchemy import MetaData, Table, Column, Integer, String
  
  metadata = MetaData()
  user_table = Table(
      "user",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("name", String(30)),
      Column("fullname", String)
  )
  ```

  - `Column`의 제약 조건 설정하기
    - 위에서 살펴본 것 처럼 `primary_key`를 True로 줌으로써 primary key 제약 조건을 설정할 수 있다.
    - `ForeignKey`를 설정하여 foreign key 제약 조건을 설정할 수 있다.
    - 아래와 같이 `Column`을 선언하는 부분 내에서 `ForeignKey` object를 사용할 경우 type을 생략할 수 있으며, 생략할 경우 참조하는 column의 type으로 선언된다.
    - `nullable`을 False로 설정하여 NOT NULL 제약 조건을 설정할 수 있다.

  ```python
  from sqlalchemy import Table, Column, Integer, String, ForeignKey
  
  address_table = Table(
      "address",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("user_id", ForeignKey("user.id"), nullable=False),
      Column("email_address", String, nullable=False),
  )
  ```

  - `Table` 객체로 DB에 실제 table 생성하기
    - `MetaData.create_all()` method를 사용하여 DB에 table을 생성할 수 있다.
    - `Engine`의 instance를 인자로 넘긴다.
    - `MetaData.create_all()` method는 정확한 순서로 table들을 생성한다(위 예시에서는 address가 참조하는 user table이 먼저 생성되어야 하므로, `MetaData.create_all()` method는 user table을 먼저 생성하고 address table을 생성한다).

  ```python
  from sqlalchemy import create_engine
  
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  metadata.create_all(engine)
  ```



- ORM Declarative Form을 사용하여 table 생성하기

  - 앞에서는 `Table` class를 직접 사용하는 방식을 살펴봤다.
    - 이 방식이 내부적으로 SQLAlchemy가 DB table을 참조하는 방식이다.
    - 지금부터 살펴볼 방식은  SQLAlchemy ORM을 사용하는 declarative table이라는 방식이다.
    - Declarative table은 앞에서 살펴본 방식과 동일한 목표(`Table` 객체를 생성하고 이를 통해 DB에 table을 생성)를 ORM mapped class(혹은 mapped class)라 불리는 class를 통해 달성할 수 있다.
  - Declarative table을 사용할 때의 이점들
    - 보다 간결하고 Pythonic한 방식으로 column을 정의할 수 있다.
    - 선언한 mapped class는 SQL expression을 구성하는 데 사용할 수 있으며, 정적 분석 도구를 통해 유지 보수가 용이하다.
    - Table metadata 및 ORM mapped class 를 동시에 선언할 수 있다.
  - Declarative Base 선언하기
    - `DeclarativeBase`를 상속 받는 class를 선언하며, `DeclarativeBase`를 상속 받는 `Base` class가 Declarative Base가 된다.
    - Declarative Base는 자동으로 생성된 `MetaData`의 instance를 참조한다.
    - `Base`를 상속받는 class들은 DB의 특정 table을 참조하는 ORM mapped class가 된다.
    - 또한 Declarative Base는 `registry`를 참조하는데, `registry`에는mapper configuration에 관한 정보가 저장되어 있다. 

  ```python
  from sqlalchemy.orm import DeclarativeBase
  
  class Base(DeclarativeBase):
      pass
  
  print(Base.metadata)		# MetaData()
  print(Base.registry)		# <sqlalchemy.orm.decl_api.registry object at 0x...>
  ```

  - ORM Mapped Class 선언하기
    - PEP 484에 따라 type annotation을 적용하기 위해, `Mapped`라는 특수한 type을 사용하여 attribute가 특정 type과 mapping되었다는 것을 표현한다.
    - 각 class는 declarative mapping 과정에서 생성된 `Table` 객체를 참조하는데(`DeclarativeBase.__table__` attribtute를 통해 접근이 가능하다), `Table` 객체의 이름은 `__tablename__` attribute의 값으로 설정된다.
    - `Table` 객체를 직접 생성하고 `DeclarativeBase.__table__` attribute에 직접 할당하는 방식도 가능하며, 이 방식을 Declarative with Imperative Table이라 부른다.
    - `mapped_column`는 ORM mapped class가 참조하는 `Table` 객체에 `Column`을 생성한다.
    - `Optional`을 사용하여 nullable한 값이 되도록 할 수 있다(혹은 `<type> | None`, `Union[<type>, None]`과 같이도 할 수 있다).
    - `Mapped`를 사용하여 type을 명시하지 않고, `mapped_column`만을 사용해도 column 추가는 가능하다.
    - ORM mapped class는 `__init__()` method를 선언할 필요가 없으며, 기본값은 attribute들을 optional keyword arguments로 받는 것이다.
    - 아래 예시에서는 `__repr__()` method를 선언했지만, `__init__()` method와 마찬가지로 선언하지 않아도 자동으로 추가된다.

  ```python
  from sqlalchemy.orm import Mapped, mapped_column, relationship
  from typing import Optional
  from sqlalchemy import String
  
  
  class User(Base):
      __tablename__ = "user"
  
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str] = mapped_column(String(30))
      # 아래와 같이 선언할 수도 있고
      fullname: Mapped[Optional[str]]
      # 아래와 같이 type annotation을 사용하지 않을 수도 있다.
      # fullname = mapped_column(String(30), nullable=True)
  
      addresses: Mapped[list["Address"]] = relationship(back_populates="user")
  
      def __repr__(self) -> str:
          return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
      
  
  class Address(Base):
      __tablename__ = "address"
  
      id: Mapped[int] = mapped_column(primary_key=True)
      email_address: Mapped[str]
      user_id = mapped_column(ForeignKey("user.id"))
  
      user: Mapped[User] = relationship(back_populates="addresses")
  
      def __repr__(self) -> str:
          return f"Address(id={self.id!r}, email_address={self.email_address!r})"
  ```

  - ORM mapping을 사용하여 DB에 table 생성하기
    - `Base.metadata.create_all()` method를 사용하면 된다.
    - 상기했듯 Declarative Base는 자동으로 `MetaData`의 instance를 참조한다.
    - 따라서 `MetaData`의 instance에 접근하여 `create_all()` method를 실행할 수 있다.

  ```python
  Base.metadata.create_all(engine)
  ```



- Table Reflection

  - Table reflection은 현재 DB의 상태를 읽어 `Table` 혹은 `Table`과 관련된 object들을 생성하는 과정이다.
    - 앞에서 우리는 `Table` object를 생성하고, 이 object를 통해 DDL을 실행하여 DB에 table을 생성했다.
    - Table reflection은 이 과정을 반대로 실행하는 것이다.
    - 즉 이미 존재하는 DB를 읽어서 Python object를 생성한다.
  - 이미 존재하는 DB를 가지고 작업한다고 해서 반드시 table reflection을 사용해야 하는 것은 아니다.
    - 이미 존재하는 DB를 대상으로 작업한다고 하더라도 해당 DB에 있는 table과 동일한 object를 생성하여 작업하는 것이 일반적이다.
    - 또한 굳이 application에서 사용하지 않는 table들을 table reflection을 통해 가져오는 것은 비효율적이다.
  - Table reflection을 위해 새로운 table을 생성한다.

  ```python
  from sqlalchemy import create_engine
  from sqlalchemy import text
  
  
  # engine 생성
  engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
  
  # table 생성
  with engine.connect() as conn:
      conn.execute(text("CREATE TABLE some_table (x int, y int)"))
      conn.commit()
  ```

  - Table reflection을 실행한다.
    - Table reflection을 실행하는 다양한 방식이 있지만, 아래 예시에서는 `Table` class를 사용한다.
    - 첫 번째 인자로 table의 이름, 두 번째 인자로 metadata를 전달한다.
    - `autoload_with`는 `Engine`을 통해 `Column`과 `Constraint` 객체를 사용하지 않고 column과 제약조건을 읽어올 수 있게 해준다.

  ```python
  from sqlalchemy import Table, MetaData
  
  # metadata 생성
  metadata = MetaData()
  
  # table 생성
  some_table = Table("some_table", metadata, autoload_with=engine)
  ```





# CRUD 실행하기

## Insert

- Insert 실행하기

  - `insert()` method를 실행하여 새로운 data를 삽입하는 것이 가능하다.
    - `insert()` method는 `Insert`의 instance를 생성하며, `Insert`는 SQL의 INSERT문을 표현하는 class이다.

  ```python
  from sqlalchemy import String, insert, Table, Column, Integer, String, MetaData
  
  
  metadata = MetaData()
  
  user_table = Table(
      "user_account",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("name", String(30)),
      Column("fullname", String),
  )
  
  # insert()는 Insert class의 instance를 반환하며 Insert instance의 values() method를 사용해 값을 설정한다.
  stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
  print(stmt)		# INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
  ```

  - `compile()` method를 사용하여 문자열화 된 형식을 얻을 수 있다.

  ```python
  compiled = stmt.compile()
  print(compiled.params)		# {'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
  ```

  - SQL문 실행하기
    - INSERT문은 row를 반환하지 않지만, RETURNING 절을 지원하는 DB의 경우 값을 반환하기도 한다.

  ```python
  # table 생성
  user_table.metadata.create_all(engine)
  
  # SQL문 실행
  with engine.connect() as conn:
      result = conn.execute(stmt)
      conn.commit()
      print(result.inserted_primary_key)		# (1,)
  ```

  - INSERT는 보통 VALUES 절을 자동으로 생성한다.
    - 위 예시에서는 `Insert.values()`를 사용하여 값을 설정해줬다.
    - 값을 설정하지 않더라도 VALUES 절 자체는 추가가 된다.

  ```python
  # VALUES 절이 자동으로 추가된 것을 확인할 수 있다.
  print(insert(user_table))		# INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)
  ```

  - 이를 이용하여 아래와 같이 SQL문을 실행할 때 값을 설정하는 것이 가능하다.
    - 사실 이 방식이 보다 일반적인 방식이다.
    - `execute()`의 첫 번째 인자로 `Insert`의 instance를 넘기고, 두 번째 인자로 삽입할 값을 넘기면, SQLAlchemy가 이들을 조합하여 SQL문을 만든다.

  ```python
  with engine.connect() as conn:
      result = conn.execute(
          insert(user_table),
          [
              {"name": "sandy", "fullname": "Sandy Cheeks"},
              {"name": "patrick", "fullname": "Patrick Star"},
          ],
      )
      conn.commit()
  ```



- INSERT...RETURNING

  - RETURNING 절을 지원하는 DB를 대상으로 사용할 때는, RETUNING 절이 자동으로 포함된다.
    - RETURNING 절을 지원하는 DB들은 RETURNING 절에서 기본 값으로 반환하는 값(일반적으로 마지막으로 insert된 data의 primary key)을 가지고 있다.
    - SQLite는 RETURNING절을 지원하며, RETURNING 절이 있을 떄 기본 값으로 마지막으로 insert된 data의 primary key를 반환하도록 되어 있다.
    - SQLite를 사용한 위 예시에서 RETURNING절이 자동으로 포함되었고, RETURNING절이 반환하는 기본 값인 마지막으로 insert된 data의 primary key가 반환되었다.
  - 아래와 같이 명시적으로 지정하는 것도 가능하다.
    - `Insert.returning()` method를 사용하면 된다.	

  ```python
  insert_stmt = insert(user_table).returning(
      user_table.c.id, user_table.c.name
  )
  print(insert_stmt)		
  # INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname) RETURNING user_account.id, user_account.name
  ```

  - INSERT..FROM SELECT와 조합하는 것도 가능하다.

  ```python
  select_stmt = select(user_table.c.id, user_table.c.name)
  insert_stmt = insert(user_table).from_select(
      ["id", "name"], select_stmt
  )
  print(insert_stmt.returning(user_table.c.id, user_table.c.name))
  """
  INSERT INTO user_account (id, name) SELECT user_account.id, user_account.name 
  FROM user_account RETURNING user_account.id, user_account.name
  """ 
  ```




- INSERT...FROM SELECT

  - `Insert.from_select()` method를 사용하여 SELECT문으로 조회한 문서를 바로 삽입할 수 있다.

  ```python
  # SELECT문을 작성하고
  select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
  # SELECT문으로 조회한 row들을 삽입한다.
  insert_stmt = insert(address_table).from_select(
      ["user_id", "email_address"], select_stmt
  )
  print(insert_stmt)
  """
  INSERT INTO address (user_id, email_address)
  SELECT user_account.id, user_account.name || :name_1 AS anon_1
  FROM user_account
  """
  ```

  - 일반적으로 table을 copy할 때 사용한다.



## Select

- SELECT문 실행하기

  - `select()` 함수는 `Select`의 instance를 생성한다.
    - `Select` instance는 SELECT query를 실행하는 데 사용된다.
    - `Select`의 instance를 core의 `Connection.execute()`에 인자로 전달하거나 ORM의 `Session.execute()`의 인자로 전달하여 사용하며, 이 method들의 결과로 반환되는 `Result` instance를 통해 조회 결과를 확인할 수 있다.

  ```python
  from sqlalchemy import select
  
  
  metadata = MetaData()
  
  user_table = Table(
      "user_account",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("name", String(30)),
      Column("fullname", String),
  )
  
  user_table.metadata.create_all(engine)
  
  stmt = select(user_table)
  print(type(stmt))		# <class 'sqlalchemy.sql.selectable.Select'>
  print(stmt)
  
  """
  SELECT user_account.id, user_account.name, user_account.fullname 
  FROM user_account
  """
  ```

  - WHERE절과 함께 사용하기
    - `Select.where()`method를 사용하여 WHERE절을 구성할 수 있다.

  ```python
  from sqlalchemy import select
  stmt = select(user_table).where(user_table.c.name == "spongebob")
  print(stmt)
  
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  WHERE user_account.name = :name_1
  """
  ```

  - SELECT문을 실행한 결과로 `CursorResult`의 instance가 반환되며, `CursorResult`는 table의 row를 나타내는 `Row` 객체들을 가지고 있는 iterator이다.

  ```python
  with Session(engine) as session:
      session.execute(insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants"))
      result = session.execute(select(user_table).where(user_table.c.name == "spongebob"))
      print(type(result))		# <class 'sqlalchemy.engine.cursor.CursorResult'>
      for row in result:
          print(row)			# (1, 'spongebob', 'Spongebob Squarepants')
  ```

  - Label도 사용할 수 있다.

  ```python
  from sqlalchemy import func, cast
  stmt = select(
      ("Username: " + user_table.c.name).label("username"),
  ).order_by(user_table.c.name)
  with engine.connect() as conn:
      for row in conn.execute(stmt):
          print(f"{row.username}")
          
  """
  Username: patrick
  Username: sandy
  Username: spongebob
  """
  ```

  - Textual column expression을 사용하는 것도 가능하다.

  ```python
  from sqlalchemy import text
  stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
  with engine.connect() as conn:
      print(conn.execute(stmt).all())		
  
  # [('some phrase', 'patrick'), ('some phrase', 'sandy'), ('some phrase', 'spongebob')]
  ```



- COLUMNS와 FROM절 설정하기

  - `select()`에 table만 넣을 경우 해당 table의 모든 column을 조회한다.

  ```python
  print(select(user_table))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  """
  ```

  - 그러나 아래와 같이 조회할 column을 지정하는 것도 가능하다.
    - `Table.c`를 통해 접근할 수 있는 `Column` object를 인자로 넘기면 된다.
    - 혹은 `Table.c["column1", "column2"]`와 같이 접근하여 인자로 전달하면 된다.

  ```python
  print(select(user_table.c.name, user_table.c.fullname))
  """
  SELECT user_account.name, user_account.fullname
  FROM user_account
  """
  
  print(select(user_table.c["name", "fullname"]))
  """
  SELECT user_account.name, user_account.fullname
  FROM user_account
  """
  ```

  - ORM mapped class 사용하기
    - 위에서는` Table`의 instance를 인자로 넘겼지만, ORM mapped class 자체를 넘겨도 된다.

  ```python
  from typing import Optional
  
  from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
  from sqlalchemy import String, select
  
  
  class Base(DeclarativeBase):
      pass
  
  class User(Base):
      __tablename__ = "user_account"
  
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str] = mapped_column(String(30))
      fullname: Mapped[Optional[str]]
  
  
  print(select(User))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  """
  ```

  - ORM mapped class를 사용하여 조회하기
    - `Session.execute()`를 통해 실행할 수 있다.
    - 각 low의 단일 element를 가지는 tuple로 반환된다.

  ```python
  with Session(engine) as session:
      session.execute(insert(User).values(name="spongebob", fullname="Spongebob Squarepants"))
      session.commit()
      rows = session.execute(select(User))
      for row in rows:
          print(row[0])
  ```

  - `Session.scalars()`를 사용하면 보다 간편하게 조회가 가능하다.
    - 각 row가 tuple로 반환되지 않는다.

  ```python
  with Session(engine) as session:
      session.execute(insert(User).values(name="spongebob", fullname="Spongebob Squarepants"))
      session.commit()
      rows = session.scalars(select(User))
      for row in rows:
          print(row)
  ```

  - ORM mapped class도 마찬가지로 column을 지정해서 조회할 수 있다.
    - 이 때, `execute()`를 사용하여 조회할 경우 각 row는 ORM mapped class의 인스턴스가 아니라 각 column 값들의 tuple이 된다.

  ```python
  print(select(User.name, User.fullname))
  """
  SELECT user_account.name, user_account.fullname 
  FROM user_account
  """
  
  with Session(engine) as session:
      session.execute(insert(User).values(name="spongebob", fullname="Spongebob Squarepants"))
      session.commit()
      rows = session.execute(select(User.name, User.fullname))
      for row in rows:
          print(row)		# ('spongebob', 'Spongebob Squarepants')
  ```



- WHERE 절

  - SQLAlchemy는 Python operation을 SQL expression으로 변환해준다.

  ```python
  print(user_table.c.name == "squidward")	# user_account.name = :name_1
  print(address_table.c.user_id > 10)		# address.user_id > :user_id_1
  
  # 아래와 같이 where절을 생성할 때 사용 가능하다.
  print(select(user_table).where(user_table.c.name == "squidward"))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  WHERE user_account.name = :name_1
  """
  ```

  - AND를 통해 여러 조건을 설정하려면 `.where()` 메서드를 여러 번 사용하거나, 하나의 `.where()` 메서드 안에 여러 조건들을 넣으면 된다.

  ```python
  print(
      select(address_table.c.email_address)
      .where(user_table.c.name == "squidward")
      .where(address_table.c.user_id == user_table.c.id)
  )
  
  print(
      select(address_table.c.email_address).where(
          user_table.c.name == "squidward",
          address_table.c.user_id == user_table.c.id,
      )
  )
  
  # 결과는 같다.
  """
  SELECT address.email_address
  FROM address, user_account
  WHERE user_account.name = :name_1 AND address.user_id = user_account.id
  """
  ```

  - `and_()`와 `or_()` 메서드를 사용하여 AND와 OR를 표현할 수 있다.

  ```python
  from sqlalchemy import and_, or_
  print(
      select(Address.email_address).where(
          and_(
              or_(User.name == "squidward", User.name == "sandy"),
              Address.user_id == User.id,
          )
      )
  )
  
  """
  SELECT address.email_address
  FROM address, user_account
  WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
  AND address.user_id = user_account.id
  """
  ```

  - `Select.filter_by()`를 사용해도 AND를 표현할 수 있다.

  ```python
  print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))
  
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  WHERE user_account.name = :name_1 AND user_account.fullname = :fullname_1
  """
  ```



- 명시적인 FROM과 JOIN

  - FROM은 명시적으로 설정하지 않아도 자동으로 설정된다.

  ```py
  print(select(user_table.c.name))
  
  """
  SELECT user_account.name
  FROM user_account
  """
  ```

  - `Select.select_from()`을 사용하면 FROM을 명시적으로 설정하는 것이 가능하다.

  ```python
  from sqlalchemy import func
  print(select(func.count("*")).select_from(user_table))
  
  """
  SELECT count(:count_2) AS count_1
  FROM user_account
  """
  ```

  - `Select.join_from()` 메서드를 사용하여 join이 가능하다.
    - 좌측과 우측을 모두 parameter로 받는다.

  ```python
  print(
      select(user_table.c.name, address_table.c.email_address).join_from(
          user_table, address_table
      )
  )
  
  """
  SELECT user_account.name, address.email_address
  FROM user_account JOIN address ON user_account.id = address.user_id
  """
  ```

  - `Select.join()` 메서드를 사용하는 것도 가능하다.
    - 이 경우 우측만 받으며, 좌측은 자동으로 설정된다.

  ```python
  print(select(user_table.c.name, address_table.c.email_address).join(address_table))
  
  """
  SELECT user_account.name, address.email_address
  FROM user_account JOIN address ON user_account.id = address.user_id
  """
  ```

  - `Select.select_from()` 메서드와 함께 사용하려면 아래와 같이 하면 된다.

  ```python
  print(select(address_table.c.email_address).select_from(user_table).join(address_table))
  
  """
  SELECT address.email_address
  FROM user_account JOIN address ON user_account.id = address.user_id
  """
  ```

  - ON 절 설정하기
    - `Select.join()`와 `Select.join_from()` 메서드는 join 대상 table외에 추가적으로 ON 절에 사용할 표현식을 받는다.

  ```python
  print(
      select(address_table.c.email_address)
      .select_from(user_table)
      .join(address_table, user_table.c.id == address_table.c.user_id)
  )
  
  """
  SELECT address.email_address
  FROM user_account JOIN address ON user_account.id = address.user_id
  """
  ```

  - OUTER와 FULL join
    - `Select.join()`와 `Select.join_from()` 메서드는 `isouter`, `full`이라는 keyword argument를 받는다.
    - 각 값을 True로 주면 각각 OUTER join과 FULL join을 실행한다.

  ```python
  print(select(user_table).join(address_table, isouter=True))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account LEFT OUTER JOIN address ON user_account.id = address.user_id
  """
  
  print(select(user_table).join(address_table, full=True))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id
  """
  ```



- ORDER BY, GROUP BY, HAVING

  - ORDER BY
    - `Select.order_by()`를 통해 설정이 가능하다.
    - 오름차순, 내림차순 설정은 `ColumnElement`의 `.asc()`, `.desc()` 메서드를 사용하면 된다.

  ```python
  print(select(user_table).order_by(user_table.c.name))
  
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account ORDER BY user_account.name
  """
  
  print(select(User).order_by(User.fullname.desc()))
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account ORDER BY user_account.fullname DESC
  """
  ```

  - 집계 함수 사용하기
    - SQLAlchemy에서는 `func`을 통해 SQL의 집계 함수를 사용할 수 있다.
    - `func`은 새로운 `Function` 인스턴스를 생성하는 constructor 객체이다.

  ```python
  from sqlalchemy import func
  count_fn = func.count(user_table.c.id)
  print(count_fn)
  
  """
  count(user_account.id)
  """
  ```

  - GROUP BY와 HAVING 사용하기
    - 각각 `Select`의 `group_by()`, `having()` 메서드를 사용한다.

  ```python
  print(
  	select(User.name, func.count(Address.id).label("count"))
      .join(Address)
      .group_by(User.name)
      .having(func.count(Address.id) > 1)
  )
  
  """
  SELECT "user".name, count(address.id) AS count 
  FROM "user" JOIN address ON "user".id = address.user_id GROUP BY "user".name 
  HAVING count(address.id) > :count_
  """
  ```

  - Label 활용하기
    - Label을 사용하여 정렬과 grouping이 가능하다.

  ```python
  from sqlalchemy import func, desc
  stmt = (
      select(Address.user_id, func.count(Address.id).label("num_addresses"))
      .group_by("user_id")
      .order_by("user_id", desc("num_addresses"))
  )
  print(stmt)
  
  """
  SELECT address.user_id, count(address.id) AS num_addresses
  FROM address GROUP BY address.user_id ORDER BY address.user_id, num_addresses DESC
  """
  ```



- ALIAS 사용하기

  - 아래와 같이 alias를 설정할 수 있다.
    - `.alias()` 메서드는 `Alias` object를 생성하며, `Alias`는 `Table`과 마찬가지로 `Alias.c`를 통해 column들의 collection에 접근할 수 있다.

  ```python
  foo = user_table.alias()
  bar = user_table.alias()
  print(
      select(foo.c.name, bar.c.name).join_from(
          foo, bar, foo.c.id > bar.c.id
      )
  )
  
  """
  SELECT user_account_1.name, user_account_2.name AS name_1
  FROM user_account AS user_account_1
  JOIN user_account AS user_account_2 ON user_account_1.id > user_account_2.id
  """
  ```

  - ORM entitiy는 `aliased()`를 사용하여 alias를 설정할 수 있다.
    - `aliased()` 함수는 `Alias` object를 생성한다.

  ```python
  from sqlalchemy.orm import aliased
  foo = aliased(Address)
  bar = aliased(Address)
  print(
      select(User)
      .join_from(User, foo)
      .where(foo.email_address == "patrick@aol.com")
      .join_from(User, bar)
      .where(bar.email_address == "patrick@gmail.com")
  )
  """
  SELECT user_account.id, user_account.name, user_account.fullname
  FROM user_account
  JOIN address AS address_1 ON user_account.id = address_1.user_id
  JOIN address AS address_2 ON user_account.id = address_2.user_id
  WHERE address_1.email_address = :email_address_1
  AND address_2.email_address = :email_address_2
  """
  ```





## SQL function

- SQL function은 반환 타입이 있다.

  - 각 SQL function은 SQLAlchmey에 정의된 type들을 반환한다.

  ```python
  print(func.now().type)		# DateTime()
  ```

  - 내장 함수에는 이미 정의된 반환 타입이 있다.
    - `count`, `max`, `min` 같은 집계 함수는 적절한 반환 타입이 설정되어 있다.

  ```python
  m1 = func.max(Column("some_int", Integer))
  print(m1.type)		# Integer()
  
  m2 = func.max(Column("some_str", String))
  print(m2.type)		# String()
  ```



- 다양한 SQL function을 사용할 수 있다.

  - `.count()`

  ```python
  print(select(func.count()).select_from(user_table))
  
  """
  SELECT count(*) AS count_1
  FROM user_account
  """
  ```



