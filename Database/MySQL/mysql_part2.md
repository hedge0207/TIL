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





# Shorts

- UUID

  - UUID 생성
    - UUID1의 생성 방식에 따라 생성한다.

  ```sql
  SELECT UUID();
  ```

  - UUID를 binary 형태로 변환

  ```sql
  SELECT UUID_TO_BIN(UUID());
  ```

  - Binary UUID를 string UUID로 변환

  ```sql
  SELECT BIN_TO_UUID(<binary_uuid>);
  ```

  - 유효한 UUID인지 확인

  ```sql
  SELECT IS_UUID(<string_uuid>);
  ```

  - PK에 INT 대신 UUID를 사용할 때의 장점
    - UUID는 전역 고유성을 가지고 있어 table, DB, 혹은 다른 DB와 병합하는 데 사용할 수 있다.
    - 데이터에 대한 정보를 노출하지 않으므로 URL에서 사용하는 것이 더 안전하다.
    - 예를 들어 사용자 table의 PK값으로 AUTO_INCREMENT를 사용할 경우 URL 등에서 `/users/875` 등이 노출된다면, 전체 사용자 규모를 유추할 수 있게 된다.
  - PK에 INT 대신 UUID를 사용할 때의 단점
    - UUID(16바이트) 저장을 위한서는 INT(4바이트) 혹은 BIGINT(8바이트)보다 더 많은 저장 공간이 필요하다.
    - 사람이 읽기 힘든 값이므로 디버깅이 어려울 수 있다.
    - PK에 인덱스가 자동으로 설정되므로, UUID를 사용하면 인덱스 크기가 커지고, 이로 인해 테이블 크기와 조회 성능이 저하될 수 있다.
    - 순차 정렬이 불가능하므로 삽입시에 인덱스가 자주 재조정되고, 삽입 성능이 저하된다.
  - 권장 사항
    - 만약 많은 수의 데이터가 생성될 것이 예상되는 경우에는 table의 PK는 INT 타입의 sequential한 값으로 지정하고, UUID를 사용하는 column에 보조 index를 거는 방식으로 사용하는 것이 권장된다.
    - 그러나 많은 수의 데이터가 생성되지 않는다면 UUID 사용으로 인한 성능 저하가 크지 않을 것이므로 그냥 UUID를 PK 값으로 사용해도 무방하다.
    - MySQL에서는 기본적으로 UUID를 문자열(`VARCHAR(36)`)로 저장하지만, UUID는 원래 16바이트의 이진 데이터이므로, `BINARY(16)`으로 저장하면 공간을 절약하고 성능을 개선할 수 있다.
