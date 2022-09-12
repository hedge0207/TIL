# SQL

- SQL(Structured Query Language)
  - RDBMS의 데이터를 관리하기 위해 설계된 특수 목적의 프로그래밍 언어이다.
  - 많은 수의 RDBMS에서 표준으로 채택하고 있다.



- 종류
  - DDL(Data Definition Language, 데이터 정의 언어)
    - 테이블과 인덱스 구조를 관리할 때 사용한다.
  - DML(Data Manipulation Language, 데이터 조작 언어)
    - 데이터베이스의 레코드를 조작하기 위해 사용한다.
  - DCL(Data Control Language, 데이터 통제 언어)
    - 데이터베이스와 관련된 권한을 통제하기 위해 사용한다.



## DDL

- DDL에는 아래와 같은 명령어들이 있다.

  | 명령어   | 설명                                     |
  | -------- | ---------------------------------------- |
  | CREATE   | 데이터베이스 오브젝트를 생성한다.        |
  | ALTER    | 데이터베이스 오브젝트를 변경한다.        |
  | DROP     | 데이터베이스 오브젝트를 삭제한다.        |
  | TRUNCATE | 데이터베이스 오브젝트의 내용을 삭제한다. |



- CREATE

  - 데이터베이스 생성

  ```sql
  CREATE DATABASE <db_name>;
  ```

  - 테이블 생성

  ```sql
  CREATE TABLE (
  	<컬럼명> <type> [제약조건],
  )
  ```

  - CREATE TABLE의 대표적인 제약조건
    - `PRIMARY KEY`: 테이블의 기본 키로 설정한다, 테이블의 각 행을 고유하게 식별할 수 있는 값이다.
    - `FOREIGN KEY`: 왜래 키를 정의한다.
    - `UNIQUE`: 해당 컬럼의 값은 테이블 내에서 고유해야한다.
    - `NOT NULL`: null 값이 들어가서는 안된다.
    - `CHECK`: True여야 하는 조건을 정의한다.
    - `DEFAULT`: 해당 컬럼의 값이 들어오지 않을 경우 기본 값으로 설정할 값을 지정한다.

  - 예시

  ```sql
  CREATE TABLE book
  (
  	book_id INT PRIMARY KEY, 
  	title VARCHAR(10) NOT NULL,
  	price INT DEFAULT 10000,
  	isbn VARCHAR(30) UNIQUE,
  	book_type VARCHAR(10) CHECK (book_type="E-book" OR book_type="Paper-book") 
  );
  ```



- ALTER

  - column 추가

  ```sql
  ALTER TABLE <table_name> ADD <col_name> <type> [제약조건];
  ```

  - column 삭제

  ```sql
  ALTER TABLE <table_name> DROP <col_name>
  ```

  - column 수정

  ```sql
  ALTER TABLE <table_name> MODIFY <col_name> <new_type> [new_제약조건];
  ```

  - column 이름 변경

  ```sql
  ALTER TABLE <table_name> CHANGE COLUMN <old_name> <new_name> <type> [제약조건];
  ```

  - talbe 이름 변경

  ```sql
  ALTER TABLE <old_name> RENAME <new_name>;
  ```



- DROP

  - database 삭제

  ```sql
  DROP DATABASE <DB_name>;
  ```

  - table 삭제
    - `CASCADE`와 `RESTRICT`는 테이블에 외래키가 포함되어 있을 때 고려해야 할 옵션이다.
    - `CASCADE`는 삭제 대상 테이블이 참조하고 있는 테이블까지 연쇄적으로 삭제한다.
    - `RESTIRCT`는 다른 테이블이 삭제 대상 테이블을 참조하고 있으면, 테이블을 삭제하지 못하게 막는다.

  ```sql
  DROP TABLE <table_name> [CASCADE | RESTRICT];
  ```



- TRUNCATE

  - 테이블 내의 모든 데이터 삭제

  ```sql
  TRUNCATE TABLE <table_name>;
  ```





## DML

- DML에는 아래와 같은 명령어들이 있다.

  | 명령어 | 설명                    |
  | ------ | ----------------------- |
  | SELECT | 테이블 내의 데이터 조회 |
  | INSERT | 테이블에 데이터 추가    |
  | UPDATE | 테이블의 데이터 수정    |
  | DELETE | 테이블의 데이터 삭제    |



- SELECT

  - 형식
    - `ALL` 과 `DISTINCT`: `ALL`은 모든 튜플을 검색할 때 사용하고(default), `DISTINCT`는  `SELECT` 뒤에 입력한 column의 값 중에서 중복; 된 값이 조회될 경우 중복 없이 검색한다.
    - `FROM`검색 대상이 될 테이블을 지정한다.
    - `WHERE`: 검색 조건을 기술한다.
    - `GROUP BY`: column의 값들을 그룹으로 묶어서 보기위해 사용한다.
    - `HAVING`: `GROUP BY`에 의해 그룹화 된 그룹들에 대한 조건을 지정한다.
    - `ORDER BY`: column의 값을 기준으로 정렬하기 위해 사용한다.

  ```sql
  SELECT [ALL | DISTINCT] <column1>, <column2>, ... FROM <table_name>
  [WHERE <조건식>] [GROUP BY <column1>, <column2>, ...] [HAVING <조건식>]
  [ORDER BY <column1>, <column2>, ... [ASC | DESC]]
  ```

  - 예시: Book table

  | title      | price | book_type  |
  | ---------- | ----- | ---------- |
  | Python     | 10000 | E-book     |
  | Java       | 12000 | E-book     |
  | Clean Code | 15000 | Paper-book |
  | RDBMS      | 10000 | Paper-book |
  | JavaScript | 10000 | Paper-book |

  - `DISTINCT`
    - 두 개 이상의 column을 설정한 경우 모든 값이 일치해야 중복으로 간주한다.

  ```sql
  SELECT DISTINCT book_type FROM book;
  
  /*
  book_type
  ----------
  E-Book
  Paper-book
  */
  
  # 두 개 이상의 column을 설정
  SELECT DISTINCT price, book_type FROM book;
  /*
  price | book_type 
  ______|__________
  10000 | E-book
  12000 | E-book
  15000 | Paper-book
  10000 | Paper-book
  */
  ```



- 조건식
  
  - 예시 데이터(fruit table)
  
  | id   | NAME        | PRICE |
  | ---- | ----------- | ----- |
  | 1    | apple       | 1000  |
  | 2    | apple mango | 3000  |
  | 3    | banana      | 3000  |
  | 4    | water melon | 18000 |
  | 5    | melon       | 20000 |
  
  - `=`: 값이 같은 경우 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE NAME="apple";
  
  # 1번 row가 조회된다.
  ```
  
  - `!=`, `<>`: 값이 다른 경우 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE NAME<>"apple";
  
  # 2,3,4,5 번 row가 조회된다.
  ```
  
  - `<`, `<=`, `>`, `>=`: 대소비교에 사용한다.
  
  ```sql
  SELECT * FROM fruit WHERE price>=18000;
  
  # 4,5번 row가 조회된다.
  ```
  
  - `BETWEEN`: gte, lte 값 사이의 값들을 구하기 위해 사용한다.
  
  ```sql
  SELECT * FROM fruit WHERE price BETWEEN 18000 AND 20000;
  
  # 4,5번 row가 조회된다.
  ```
  
  - `IN`: 컬럼이 `IN` 안에 포함된 경우의 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE name IN ('apple', 'melon');
  
  # 1,5번 row가 조회된다.
  ```
  
  - `NOT IN`: 컬럼이 `IN` 안에 포함되어 있지 않은 경우의 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE name NOT IN ('apple', 'melon');
  
  # 2,3,4번 row가 조회된다.
  ```
  
  - `LIKE`: 특정 패턴과 일치하는 데이터를 조회하기 위해 사용한다.
  
  ```sql
  SELECT * FROM fruit WHERE name LIKE '%melon'
  
  # 4,5번 row가 조회된다.
  ```
  
  - `IS NULL`: 컬럼이 NULL인 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE name IS NULL;
  
  # 아무 row도 조회되지 않는다.
  ```
  
  - `IS NOT NULL`: 컬럼이 NULL이 아닌 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE name IS not NULL;
  
  # 모든 row가 조회된다.
  ```
  
  - `AND`: 두 조건을 모두 만족하는 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE NAME='banana' AND price<=3000;
  
  # 3번 row만 조회된다.
  ```
  
  - `OR`: 두 조건 중 하나라도 만족하는 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE NAME='banana' OR price<=3000;
  
  # 1,2,3 번 row가 조회된다.
  ```
  
  - `NOT`(==`!`): 조건에 해당하지 않는 데이터를 조회한다.
  
  ```sql
  SELECT * FROM fruit WHERE not NAME='banana';
  
  # 1,2,4,5 번 row가 조회된다.





















# TO DO

- VIEW
- INDEX





