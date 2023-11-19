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



- INSERT

  - 데이터를 삽입하는 명령어

  - 형태

  ```sql
  # column을 지정하는 경우
  INSERT INTO <table_name>(column1, column2, ...) VALUES (value1, value2, ...)
  
  # column 지정 없이도 가능하다.
  INSERT INTO <table_name> VALUES (value1, value2, ...)
  ```



- UPDATE

  - 데이터를 변경하는 명령어
  - 형태

  ```sql
  UPDATE <table_name> SET <column> = <data> WHERE <조건>
  ```



- DELETE

  - 데이터를 제거하는 명령어

  - 형태

  ```sql
  DELETE FROM <table_name> WHERE <조건>
  ```





### SELECT

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
    - `%`: 0개 이상의 문자열과 일치
    - `[]`: 대괄호 내부의 1개의 문자와 일치
    - `[^]`: 대괄호 내부의 1개의 문자와 불일치
    - `_`: 특정 위치의 1개의 문자와 일치
  
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



- `GROUP BY`

  - 속성값을 그룹으로 분류할 때 사용한다.

  - 예시 데이터(employee table)

  | name | position | department | age  |
  | ---- | -------- | ---------- | ---- |
  | John | Backend  | ML         | 29   |
  | Choi | Backend  | DB         | 27   |
  | Mike | Frontend | ML         | 27   |
  | Jane | Frontend | ML         | 28   |

  - department별 age 합계

  ```sql
  SELECT department, SUM(age) FROM employee GROUP BY department;
  ```

  - position별 인원

  ```sql
  SELECT position, COUNT(*) FROM employee GROUP BY position;
  ```

  - position, department 별 나이 합계

  ```sql
  SELECT POSITION, department, sum(age) FROM employee GROUP BY POSITION, department;
  ```



- `HAVING`

  - `group by`로 그룹화 된 그룹에 대한 조건을 지정한다.
  - 예시
    - 구성원들의 연령 합계가 60 이상인 department 구하기

  ```sql
  SELECT department, sum(age) as total_age FROM employee GROUP BY department HAVING total_age >= 60;
  ```



- `ORDER BY`

  - 조회 결과를 정렬하기 위해 사용한다.

  - 형식
    - 기본값은 ASC(오름차순)이다.
    - 둘 이상의 정렬 기준을 설정할 경우 먼저 설정한 기준의 정렬 결과 중 같은 값이 있는 경우 다음 기준으로 정렬한다.

  ```sql
  order by <필드1> [ASC|DESC] [, <필드2> [ASC|DESC]]
  ```

  - 예시1
    - age가 큰 순으로 정렬된다.

  ```sql
  SELECT * FROM employee ORDER BY age DESC;
  ```

  - 예시2. 복수의 정렬 기준을 설정한 경우
    - 먼저 age를 기준으로 내림차순으로 정렬 후, 나이가 같을 경우, name을 기준으로 알파벳 순으로 정렬한다.

  ```sql
  SELECT * FROM employee ORDER BY age DESC, name;
  ```




- 서브 쿼리

  - SQL문 안에 포함된 또 다른 SQL문이다.

  - 서브 쿼리에서는 메인 쿼리의 컬럼 정보를 사용할 수 있으나, 메인 쿼리에서는 서브 쿼리의 컬럼 정보를 사용할 수 없다.

  - 서브 쿼리 유형

    - `FROM`  절 서브쿼리(인라인 뷰): 서브쿼리가 `FROM` 절 안에 들어있는 형태.
    - `WHERE` 절 서브쿼리(중첩 서브쿼리) 서브쿼리가 `WHERE` 절 안에 들어있는 형태.

  - 예시 데이터

    - employee, employee_salary 두 개의 table이다.


| employee_id | name |      | employee_id | salary |
| ----------- | ---- | ---- | ----------- | ------ |
| 1           | John |      | 1           | 400    |
| 2           | Jane |      | 2           | 300    |
| 5           | Tom  |      | 3           | 200    |
|             |      |      | 4           | 100    |

  - `FROM`절 서브쿼리 예시

  ```sql
select * from employee e, (select * from employee_salary) es where e.employee_id=es.employee_id;
  ```

  - 결과

| e.employee_id | e.name | es.employee_id | es.salary |
| ------------- | ------ | -------------- | --------- |
| 1             | John   | 1              | 400       |
| 2             | Jane   | 2              | 300       |

  - `WHERE`절 서브쿼리 예시

  ```sql
SELECT * FROM employee where employee_id in (select employee_id from employee_salary);
  ```

  - 결과

| employee_id | name |
| ----------- | ---- |
| 1           | John |
| 2           | Jane |



- `GROUP BY`

  - 속성값을 그룹으로 분류할 때 사용한다.

  - 예시 데이터(employee table)

  | name | position | department | age  |
  | ---- | -------- | ---------- | ---- |
  | John | Backend  | ML         | 29   |
  | Choi | Backend  | DB         | 27   |
  | Mike | Frontend | ML         | 27   |
  | Jane | Frontend | ML         | 28   |

  - department별 age 합계

  ```sql
  SELECT department, SUM(age) FROM employee GROUP BY department;
  ```

  - position별 인원

  ```sql
  SELECT position, COUNT(*) FROM employee GROUP BY position;
  ```

  - position, department 별 나이 합계

  ```sql
  SELECT POSITION, department, sum(age) FROM employee GROUP BY POSITION, department;
  ```



- `HAVING`

  - `group by`로 그룹화 된 그룹에 대한 조건을 지정한다.
  - 예시
    - 구성원들의 연령 합계가 60 이상인 department 구하기

  ```sql
  SELECT department, sum(age) as total_age FROM employee GROUP BY department HAVING total_age >= 60;
  ```



- `ORDER BY`

  - 조회 결과를 정렬하기 위해 사용한다.

  - 형식
    - 기본값은 ASC(오름차순)이다.
    - 둘 이상의 정렬 기준을 설정할 경우 먼저 설정한 기준의 정렬 결과 중 같은 값이 있는 경우 다음 기준으로 정렬한다.

  ```sql
  order by <필드1> [ASC|DESC] [, <필드2> [ASC|DESC]]
  ```

  - 예시1
    - age가 큰 순으로 정렬된다.

  ```sql
  SELECT * FROM employee ORDER BY age DESC;
  ```

  - 예시2. 복수의 정렬 기준을 설정한 경우
    - 먼저 age를 기준으로 내림차순으로 정렬 후, 나이가 같을 경우, name을 기준으로 알파벳 순으로 정렬한다.

  ```sql
  SELECT * FROM employee ORDER BY age DESC, name;
  ```




- 서브 쿼리

  - SQL문 안에 포함된 또 다른 SQL문이다.

  - 서브 쿼리에서는 메인 쿼리의 컬럼 정보를 사용할 수 있으나, 메인 쿼리에서는 서브 쿼리의 컬럼 정보를 사용할 수 없다.

  - 서브 쿼리 유형

    - `FROM`  절 서브쿼리(인라인 뷰): 서브쿼리가 `FROM` 절 안에 들어있는 형태.
    - `WHERE` 절 서브쿼리(중첩 서브쿼리) 서브쿼리가 `WHERE` 절 안에 들어있는 형태.

  - 예시 데이터

    - employee, employee_salary 두 개의 table이다.
  
  | employee_id | name |      | employee_id | salary |
  | ----------- | ---- | ---- | ----------- | ------ |
  | 1           | John |      | 1           | 400    |
  | 2           | Jane |      | 2           | 300    |
  | 5           | Tom  |      | 3           | 200    |
  |             |      |      | 4           | 100    |
  
    - `FROM`절 서브쿼리 예시
  
  ```sql
  select * from employee e, (select * from employee_salary) es where e.employee_id=es.employee_id;
  ```
  
    - 결과
  
  | e.employee_id | e.name | es.employee_id | es.salary |
  | ------------- | ------ | -------------- | --------- |
  | 1             | John   | 1              | 400       |
  | 2             | Jane   | 2              | 300       |
  
    - `WHERE`절 서브쿼리 예시
  
  ```sql
  SELECT * FROM employee where employee_id in (select employee_id from employee_salary);
  ```
  
    - 결과
  
  | employee_id | name |
  | ----------- | ---- |
  | 1           | John |
  | 2           | Jane |





#### JOIN

- `JOIN`

  - 둘 이상의 테이블을 연결하여 데이터를 검색하기 위해 사용한다.
  - 형식
    - 조인 조건에는 `ON`을 사용한다.
    - 같은 이름의 컬럼명이 여러 테이블에 있을 경우 구분을 위해 `별칭.컬럼명` 형태로 표현한다.

  ```sql
  select * from <table_1> [별칭] [join_type] JOIN <table_2> [별칭] [ON 조인조건];
  ```



- 예시 데이터

  - employee, employee_salary 두 개의 table이다.

  | employee_id | name |      | employee_id | salary |
  | ----------- | ---- | ---- | ----------- | ------ |
  | 1           | John |      | 1           | 400    |
  | 2           | Jane |      | 2           | 300    |
  | 5           | Tom  |      | 3           | 200    |
  |             |      |      | 4           | 100    |



- 내부 조인

  - 공통으로 존재하는 컬럼의 값이 같은 경우에만 추출
    - `INNER`는 생략 가능
  - 예시

  ```sql
  SELECT e.employee_id, e.name, es.salary FROM employee e INNTER JOIN employee_salary es ON e.employee_id=es.employee_id 
  ```

  - 결과

  | e.employee_id | e.name | es.salary |
  | ------------- | ------ | --------- |
  | 1             | John   | 400       |
  | 2             | Jane   | 300       |



- 왼쪽 외부 조인

  - 왼쪽 테이블의 모든 데이터와 오른쪽 테이블의 동일 데이터를 추출.
    - `LEFT`를 사용한다.
    - `OUTER`는 생략 가능하다.
  - 예시

  ```sql
  SELECT e.employee_id, e.name, es.employee_id, es.salary FROM employee e LEFT OUTER JOIN employee_salary es ON e.employee_id=es.employee_id
  ```

  - 결과

  | e.employee_id | e.name | es.employee_id | es.salary |
  | ------------- | ------ | -------------- | --------- |
  | 1             | John   | 1              | 400       |
  | 2             | Jane   | 2              | 300       |
  | 5             | Tom    | NULL           | NULL      |



- 오른쪽 외부 조인

  - 오른쪽 테이블의 모든 데이터와 왼쪽 테이블의 동일 데이터를 추출.
    - `RIGHT`를 사용한다.
    - `OUTER`는 생략 가능하다.
  - 예시

  ```sql
  SELECT e.employee_id, e.name, es.employee_id, es.salary FROM employee e RIGHT OUTER JOIN employee_salary es ON e.employee_id=es.employee_id 
  ```

  - 결과

  | e.employee_id | e.name | es.employee_id | es.salary |
  | ------------- | ------ | -------------- | --------- |
  | 1             | John   | 1              | 400       |
  | 2             | Jane   | 2              | 300       |
  | NULL          | NULL   | 3              | 200       |
  | NULL          | NULL   | 4              | 100       |



- 완전 외부 조인

  - 양쪽의 모든 데이터를 추출
    - `FULL`을 사용한다.
    - `OUTER`는 생략 가능하다.
    - MySQL 에서는 지원하지 않는다.
  - 예시

  ```sql
  SELECT e.employee_id, e.name, es.employee_id, es.salary FROM employee e FULL OUTER JOIN employee_salary es ON e.employee_id=es.employee_id 
  ```

  - 결과

  | e.employee_id | e.name | es.employee_id | es.salary |
  | ------------- | ------ | -------------- | --------- |
  | 1             | John   | 1              | 400       |
  | 2             | Jane   | 2              | 300       |
  | NULL          | NULL   | 3              | 200       |
  | NULL          | NULL   | 4              | 100       |
  | 5             | Tom    | NULL           | NULL      |



- 교차 조인

  - 조인 조건이 없는 모든 데이터 조합을 추출

  - 예시

  ```sql
  SELECT e.employee_id, e.name, es.employee_id, es.salary FROM employee e CROSS JOIN employee_salary es;
  ```

  - 결과

  | e.employee_id | e.name | es.employee_id | es.salary |
  | ------------- | ------ | -------------- | --------- |
  | 1             | John   | 1              | 400       |
  | 2             | Jane   | 1              | 400       |
  | 5             | Tom    | 1              | 400       |
  | 1             | John   | 2              | 300       |
  | 2             | Jane   | 2              | 300       |
  | 5             | Tom    | 2              | 300       |
  | 1             | John   | 3              | 200       |
  | 2             | Jane   | 3              | 200       |
  | 5             | Tom    | 3              | 200       |
  | 1             | John   | 4              | 100       |
  | 2             | Jane   | 4              | 100       |
  | 5             | Tom    | 4              | 100       |



- 셀프 조인

  - 자기 자신에게 별칭을 지정하고 다시 조인.
  - 예시 데이터

  | employee_id | name | nickname |
  | ----------- | ---- | -------- |
  | 1           | John | Tom      |
  | 2           | Jane | Book     |
  | 5           | Tom  | Air      |

  - 예시

  ```sql
  SELECT a.employee_id, a.name, b.employee_id, b.nickname FROM employee a JOIN employee b ON a.name=b.nickname
  ```

  - 결과

  | a.employee_id | a.name | b.employee_id | b.nickname |
  | ------------- | ------ | ------------- | ---------- |
  | 3             | Tom    | 1             | Tom        |








#### UNION

- UNION
  - 집합 연산자
  - 하나의 query의 결과를 하나의 집합으로 보고, 두 개의 query 결과를 하나로 결합하여 보여준다.
  - 집합 연산자 사용시 두 쿼리의 조회 대상 column이 같아야 한다.



- 예시 데이터

  | NAME   | PART     | AGE  |
  | ------ | -------- | ---- |
  | John   | Backend  | 22   |
  | Jane   | Frontend | 24   |
  | Albert | Devops   | 26   |
  | Sam    | UI/UX    | 28   |

  



- UNION

  - 중복 행된 행 중 하나만 남기고 나머지는 제거하여 보여준다.
    - 교집합을 제거하는 것은 아니다.
    - 교집합을 제거하는 것은 중복 행 자체를 보여주지 않는 것이지만 UNION은 중복 된 행 중 하나를 제거하여 보여주는 것이다.
  - 형태

  ```sql
  SELECT * FROM <table_name> [WHERE 조건] UNION SELECT * FROM <table_name> [WHERE 조건]
  ```

  - 예시

  ```sql
  SELECT NAME FROM emp WHERE age>22 UNION SELECT * FROM emp WHERE age>24
  ```

  - 결과
    - Albert와 Sam은 두 query에서 중복되기에 중복된 행 중 하나만 보여준다.

  | NAME   | PART     | AGE  |
  | ------ | -------- | ---- |
  | Jane   | Frontend | 24   |
  | Albert | Devops   | 26   |
  | Sam    | UI/UX    | 28   |



- UNION ALL

  - 중복된 행도 전부 보여준다.
  - 형태

  ```sql
  SELECT <columns> FROM <table_name> [options] UNION ALL SELECT <columns> FROM <table_name> [options]
  ```

  - 예시

  ```sql
  SELECT NAME FROM emp WHERE age>22 UNION ALL SELECT * FROM emp WHERE age>24
  ```

  - 결과

  | NAME   | PART     | AGE  |
  | ------ | -------- | ---- |
  | Jane   | Frontend | 24   |
  | Albert | Devops   | 26   |
  | Sam    | UI/UX    | 28   |
  | Albert | Devops   | 26   |
  | Sam    | UI/UX    | 28   |



- INTERSECT

  - 두 query에 공통적으로 포함되는 행만 보여준다.
    - 중복 행된 행 중 하나만 남기고 나머지는 제거하여 보여준다.
    - 교집합
  - 형태

  ```sql
  SELECT <columns> FROM <table_name> [options] INTERSECT SELECT <columns> FROM <table_name> [options]
  ```

  - 예시

  ```sql
  SELECT * FROM emp WHERE age > 22 INTERSECT SELECT * FROM emp WHERE age > 24;
  ```

  - 결과

  | NAME   | PART   | AGE  |
  | ------ | ------ | ---- |
  | Albert | Devops | 26   |
  | Sam    | UI/UX  | 28   |



- MINUS

  - 첫 query에는 있고, 두 번째 쿼리에는 없는 결과를 보여준다.
    - 차집합

  - 형태

  ```sql
  SELECT <columns> FROM <table_name> [options] MINUS SELECT <columns> FROM <table_name> [options]
  ```

  - 예시

  ```sql
  SELECT * FROM emp WHERE age > 22 MINUS SELECT * FROM emp WHERE age > 24;
  ```

  - 결과

  | NAME | PART     | AGE  |
  | ---- | -------- | ---- |
  | Jane | Frontend | 24   |





## DCL

- 데이터 제어어(Data Control Language)
  - 데이터 베이스에 대한 권한을 설정하는 명령어이다.



- GRANT

  - 권한 부여 명령어

  - 형태

  ```sql
  GRANT <권한> ON <table> TO <사용자>;
  ```



- REVOKE

  - 권한 회수 명령어
  - 형태

  ```sql
  REVOKE <권한> ON <table> FROM <사용자>
  ```

  









# Query

- 특정 컬럼의 값이 null이 아닌 테이블 찾기

  ```sql
  select * from some_table where some_column is not null
  ```




- 페이지네이션

  - limit과 offset의 순서가 바뀌면 안된다.
  - offset은 0부터 시작한다.

  ```sql
  select * from some_table limit [조회할 row 개수] offset [조회를 시작 할 row]
  ```

  - 예시

  ```sql
  # 1번째
  select * from test_table limit 10 offset 0
  
  # 2번째
  select * from test_table limit 10 offset 10
  ```




- 중복 데이터 제거

  - `distinct`를 사용한다.

  ```sql
  select distinct <column 명> from <테이블명>
  ```




- `%` 등의 특수문자를 문자 그대로 인식시키는 방법

  - 아래와 같은 테이블이 있다고 할 때, `theo%`를 찾는 방법

  | id   | name  |
  | ---- | ----- |
  | 1    | theo  |
  | 2    | theoo |
  | 3    | theo% |
  | 4    | theo\ |

  - 아래와 같은 쿼리를 입력하면 theoo와 theo%가 모두 나오게 된다.

  ```sql
  SELECT * FROM test WHERE NAME LIKE 'theo%'
  ```

  - `%`를 문자로 인식시키려면 `\`를 입력한다.

  ```sql
  SELECT * FROM test WHERE NAME LIKE 'theo\%'
  ```

  - `\`를 문자로 인식시키려면 앞에 하나를 더 붙여주면 된다.

  ```sql
  SELECT * FROM test WHERE NAME LIKE 'theo\\'
  ```




- Oracle 최장일치

  ```sql
  select min(t.<반환 받을 필드>) keep (DENSE_RANK first order by length(t.<검색 대상 필드>) desc)
  from <테이블명> t
  where <'찾을 문자열'> like t.keyword_cap || '%'
  ```




- partition

  - table 생성
    - table을 생성할 때 partition도 하나 이상 생성해줘야 한다.


  ```sql
CREATE TABLE `test` (
 `news_id` VARCHAR(30) NOT NULL,
 `published_at` DATETIME NOT NULL,
  PRIMARY KEY (`news_id`,`published_at`)  # partition의 기준이 되는 column은 반드시 PK여야 한다.
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=UTF8_BIN  
PARTITION BY RANGE (YEAR(published_at))
(PARTITION p1989 VALUES LESS THAN (1990) ENGINE = InnoDB)  # Partition 생성
  ```

  - 일까지 특정해서 생성하기

  ```sql
CREATE TABLE `kpf_test` (
	`id` VARCHAR(30) NOT NULL COLLATE 'utf8_bin',
	`title` TEXT NULL DEFAULT NULL COLLATE 'utf8_bin',
	`content` TEXT NULL DEFAULT NULL COLLATE 'utf8_bin',
	`created_at` DATETIME NOT NULL,
	PRIMARY KEY (`id`, `created_at`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=UTF8_BIN
PARTITION BY RANGE (to_days(created_at))
(PARTITION p2021_06 VALUES LESS THAN (TO_DAYS('2021-07-01')) ENGINE = InnoDB)
  ```



- Partition 추가

  ```sql
  alter table test add PARTITION
  (PARTITION p20210217 VALUES LESS THAN (2017) ENGINE = InnoDB,
   PARTITION p20210218 VALUES LESS THAN (2018) ENGINE = InnoDB, 
   PARTITION p20210219 VALUES LESS THAN (2019) ENGINE = InnoDB, 
   PARTITION p20210223 VALUES LESS THAN (2020) ENGINE = InnoDB)
  ```

  - 일까지 특정해서 생성하기

  ```sql
  alter table kpf_test add PARTITION (PARTITION p2021_06 VALUES LESS THAN (TO_DAYS('2021-07-01')) ENGINE = InnoDB)
  ```

  



- Partition 조회

  ```sql
  SELECT * FROM information_schema.partitions WHERE TABLE_NAME='<테이블명>'
  ```




- DB 복사

  - 테이블 구조만 복사

  ```sql
  CREATE TABLE <테이블 이름> AS SELECT * FROM <복사해올 테이블 이름> where <False 조건  e.g.1=2>
  ```

  - 테이블 구조와 데이터 복사

  ```sql
  CREATE TABLE <테이블 이름> AS SELECT * FROM <복사해올 테이블 이름>
  ```

  - 이미 생성된 테이블에 데이터만 복사(스키마 동일)

  ```sql
  INSERT INTO <복사해올 테이블 이름> SELECT * FROM <테이블 이름>
  ```

  

  















# TO DO

- VIEW
- INDEX





