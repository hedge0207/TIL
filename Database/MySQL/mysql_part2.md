# DB 복사

- `mysqldump`를 사용하여 backup 파일을 생성할 수 있다.

  - `mysqldump`는 physical backup 방식이 아닌, logical backup 방식을 사용한다.
    - 즉 실제 data를 복제하는 것이 아니라, 복제 대상 데이터를 만들기 위한 SQL문을 생성한다.
    - Backup 파일(`.sql` 파일)을 load할 때는 backup 파일에 작성된 대로 SQL문을 실행시켜 table 생성, data 삽입등을 수행하는 방식으로 복사가 이루어진다. 

  - DB의 backup을 생성한다.
    - `-u` option 뒤에 user를 입력한다.
    - `-p`는 뒤에 password를 입력하는 방식으로 동작하지 않고, `-p`를 주면 명령어 실행시 후에 password를 입력받는 식으로 동작한다.

  ```bash
  $ mysqldump -u <user> -p <db_name> > <file_name>.sql
  ```

  - DB를 생성한다.

  ```sql
  CREATE DATABASE <DB_name>;
  ```

  - Dump file을 load한다.
    - Backup을 생성할 때와는 달리 `mysqldump`가 아닌 `mysql`을 사용한다.

  ```bash
  $ mysql -u <user> -p <db_name> < <file_name>.sql
  ```

