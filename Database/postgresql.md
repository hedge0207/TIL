

- postgresql

  - postgresql 실행
    - `user명` 기본 값은 `postgres`

  ```bash
  $ psql -U <user명>
  ```

  - database list 보기

  ```bash
  $ \l
  ```

  - database 변경하기

  ```bash
  $ \connect <db명>
  ```

  - table list 보기

  ```bash
  $ \d
  ```

  - sql문을 실행할 때는 뒤에 `;`만 붙이면 된다.



- table이 존재하지 않을 경우에만 table 생성하기

  - postgresql 9.1 이상부터 지원

  ```sql
  CREATE TABLE IF NOT EXISTS public.<테이블명> (
  	id SERIAL NOT NULL,
  	name VARCHAR(50) NOT null,
  CONSTRAINT pk PRIMARY KEY (id)
  ) 
  ```



- shell script로 테이블 생성하기

  ```shell
  #!/bin/bash
  
  psql -U postgres -c "create database <DB명>"
  
  psql -U postgres -d search42 \
  -c "CREATE TABLE IF NOT EXISTS public.<table명> (
          id SERIAL NOT NULL,
          name VARCHAR(50) NOT null,
      CONSTRAINT qwe PRIMARY KEY (id)
      );
  ```