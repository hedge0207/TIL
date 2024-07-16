# 실행하기

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



- 특정 row가 이미 존재하면 update, 없으면 insert

  - `on conflict`의 대상이 되는 값은 반드시 pk값이어야한다.

  ```sql
  INSERT INTO test (application_id, name, age, ingested_date) VALUES('qqq', 'theo', 28, '2021-12-09') ON conflict (application_id, ingested_date) DO UPDATE SET application_id='qqq', NAME='theo', AGE='30';
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







# Replication

> [엑셈 기술 블로그](https://blog.ex-em.com/1781)의 PostgreSQL Replication 시리즈 참조

- Replication
  - Data의 저장 및 백업과 관련된 data를 호스트 컴퓨터에서 다른 컴퓨터로 복사하는 것을 말한다.
    - 이 때 원본과 목사본을 지칭하는 용어는 매우 다양한다.
    - 원본을 main, master, primary, publisher, active 등으로 지칭한다.
    - 복제본을 standby, slave, secondary, subscriber 등으로 표현한다.
  - Replication이 필요한 이유
    - 하나의 DB에서 DDL, DML 등의 여러 작업을 처리하면 DB에 부하가 발생할 수 있다.
    - 따라서 하나 이상의 읽기 전용 DB를 두어 SELECT query에 대한 분산 처리를 유도하면 DB를 보다 안정적으로 운영할 수 있게 된다.
    - 또한 여러 DB 중 한 대에 장애가 발생했을 때, replication DB를 사용하면 장애 상황에 대처가 가능하다.
  - Write-Ahead Log(WAL)
    - WAL이란 변경 내용을 기록한 log record를 저장소에 먼저 기록한 후 이후에 data 파일에 변경 내용을 적용하는 방식이다.
    - 즉 WAL이란 DB에 발생한 변경 내역을 기록한 일종의 명세서로, 이러한 특성을 이용해 main의 변경 내용을 standby에 replay 하는 용도로 사용한다.
  - WAL을 사용하는 이유
    - 트랜잭션 commit 마다 data page를 disk에 기록할 필요가 없다.
    - Data page에 적용되지 않은 변경 내용은 log record에서 취소가 가능하다.
    - Log 파일은 순차적으로 작성되며, log 파일 동기화 비용은 data page 쓰기 비용보다 훨씬 적다.
    - 소규모의 트랜잭션을 대량으로 처리하는 경우, log 파일의 fsync 하나로 여러 가지 트랜잭션을 commit 할 수 있다.
    - PITR(Point-In-Time Recovery)가 가능하다.
  - PostgreSQL의 replication
    - PostgreSQL은 크게 두 가지 종류의 replication 기능을 지원한다.
    - Physical Replication
    - Logical Replication



- Physical Replication

  - WAL 파일 자체를 전달하는 File-based Log Shipping 방식.
    - 완성된 WAL 파일을 standby로 전달하여 recovery 작업을 통해 replication하는 방식이다.
    - 즉 main에서 일정 크기(default는 16MB)의 WAL 파일이 채워지면 이 파일을 standby로 전달하여 복제하는 방식이다.
    - 따라서 WAL 파일이 일정 크기에 도달하기 전에는 main과 standby 사이에 동기화가 되지 않을 수 있으며, 장애 발생시 소실될 수 있다.

  - WAL 파일 저장 여부와 상관없이 WAL record를 전달하는 Streaming Replication 방식.
    - Main의 WAL 파일이 일정 크기에 도달할 때까지 기다리지 않고 WAL record를 실시간으로 streaming하는 방식이다.
    - WAL 파일 자체를 전달하는 것이 아니라 WAL record를 전달하는 방식으로 동작한다.
    - Main과 standby 사이의 동기화가 다른 방식에 비해 빨리 이루어지지만, main을 계속 streaming해야 하므로 main의 성능에 영향을 미칠 수 있다.
  - Physical replication의 한계
    - DB의 일부만 replication하는 것이 불가능하다(즉 특정 DB나 table에 대해서만 replication하는 것이 불가능하다).
    - Standby에서는 쓰기 작업이 불가능하다.
    - Main과 standby의 PostgreSQL major 버전이 다르면 replication이 불가능하다.
    - PostgreSQL이 설치된 platform이 다르면 replication이 불가능하다.



- Logical Replication

  - Physical replication의 한계를 극복하기 위해 등장한 방식이다.
    - PostgreSQL 10 버전부터 사용이 가능하다.
    - Replication identity(일반적으로 primary key)를 기반으로 data의 변경 사항을 복제하는 방법이다.
  - 동작 방식
    - 하나의 publisher와 하나 이상의 subscriber로 구성된다.
    - Subscriber는 자신이 구독 중인 게시자의 data를 가져와 이를 다시 게시하여 publisher가 될 수 있으며, 자신에 대한 subscriber도 만들 수 있따.
    - Publisher와 subscriber 사이의 replication은 복제 ID를 기반으로 수행되며, 복제 ID는 primary key 또는 unique key로 설정할 수 있다.
    - Primary key와 unique key가 둘 다 없을 경우 `REPLICA IDENTITIY FULL` 옵션으로 table 속성을 변경하여 사용할 수는 있지만, 이 방식은 table에 변경이 있을 때 마다 전체 table을 복제하므로 자원을 많이 소모할 수 있다.

  - Logical Replication의 장점
    - 특정 DB 또는 table만 replication이 가능하다.
    - Standby에서 DDL, DML 등의 쓰기 작업이 가능하다
    - 서로 다른 major version, platform 간의 replication이 가능하다.



- Logical replication 실행하기

  - Main에서 `postgresql.conf`를 아래와 같이 작성한다.

  ```toml
  listen_addresses = "*"		# default: localhost
  port = 5432					# default: 5432
  wal_level = logical			# default: replica
  ```

  - Main에서 `wal_level`을 확인한다.

  ```sql
  SHOW wal_level;
  ```

  - Main에서 replication 전용 DB user 생성
  
  ```sql
  CREATE role myuser REPLICATION LOGIN PASSWORD 'password';
  ```
  
  - Main에서 `pg_hba.conf`에 아래와 같이 추가한다.
    - `postgres` Docker image를 기준으로 `/var/lib/postgresql/data/pg_hba.conf`에 있다.
  
  ```toml
  # TYPE  DATABASE        USER            ADDRESS                 METHOD
  
  # ...
  host    all             myuser          <standby_host>/<subnet> trust
  ```
  
  - 여기까지 완료한 후 main PostgreSQL을 재실행한다.
  - Main에서 eplication 대상 table을 생성한다.
  
  ```sql
  CREATE TABLE product (
    id INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
  );
  ```

  - Main에서 publication을 생성한다.

  ```sql
  CREATE PUBLICATION my_publication FOR TABLE product;
  ```

  - Main에서 DB 사용자에게 `product` table에 대한 권한을 부여한다.

  ```sql
  GRANT SELECT ON TABLE product TO myuser;
  ```
  
  - Standby에서 replication 대상 table을 생성한다.
  
  ```sql
  CREATE TABLE product (
    id INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
  );
  ```
  
  - Standby에서 subscription을 생성한다.
    - 이 때 replication slot을 따로 생성하지 않은 경우 subscription이 생성되면서 main server에 subscription 이름으로 replication slot이 생성된다.

  ```sql
  CREATE SUBSCRIPTION my_subscription \
  CONNECTION 'dbname=postgres host=<main_host> port=<main_port> user=myuser password=password' \
  PUBLICATION my_publication;
  ```
  
  - 정상적으로 실행되었다면, process 조회시 `walsender`와 `logical replication launcher` 두 가지 process가 실행된다.
  
  ```bash
  $ ps -ef | grep postgres
  ```



- Replication slot
  - 안정적인 replication 유지를 위해서는 WAL 파일을 잘 관리해야 한다.
    - Standby의 연결이 끊어진 상태에서 main의 WAL파일이 덮어씌어진다면, replication을 유지할 수 없게 된다.
    - 따라서 error가 발생하더라도 WAL 파일을 잘 관리할 수 있도록 WAL 파일과 관련된 여러 설정을 조정해야 했다.
  - Replication slot은 main과 standby 사이의 연결이 끊어져도 WAL 파일이 main에 유지되도록 하는 기능을 말한다.
    - Replication slot을 통해 WAL파일(혹은 log record)가 standby로 전달되면 WAL 파일을 삭제 및 재사용한다.
  - Replication slot은 자동으로 삭제되지 않기 때문에 replication을 유지하지 않을 경우 수동으로 삭제해야한다.
  - Logical replication slot
    - Physical replication slot과는 달리 logical decoding이라는 방식을 통해 decoding된 message를 통해 복제를 수행한다.
    - `wal_level`의 설정값을 `logical`로 설정할 경우 logical replication slot을 사용한다.
  - Replication slot 생성하기
  
  ```sql
  SELECT pg_create_logical_replication_slot('<name>', '<plugin>');
  ```
  
  - Replication slot 삭제하기
  
  ```sql
  select pg_drop_replication_slot('<name>');
  ```



- Logical Replication 관련 catalog

  - `pg_stat_replication`
    - WAL sender process에 관한 정보를 확인할 수 있다.
    - WAL sender 하나 당 하나의 row가 된다.

  ```sql
  SELECT * FROM pg_stat_replication;
  ```

  - `pg_replication_slots`
    - Replication slot에 관한 정보를 확인할 수 있다.

  ```sql
  SELECT * FROM pg_replication_slots;
  ```

  - `pg_stat_replication_slots`
    - Logical replication slot 사용에 대한 집계 정보를 표시한다.
    - PostgreSQL 14부터 사용이 가능하다.

  ```sql
  SELECT * FROM pg_stat_replication_slots
  ```

  - `pg_publication`
    - Logical replication에서 사용하는 publisher에 대한 정보를 확인할 수 있다.

  ```sql
  SELECT * FROM pg_publication;
  ```

  - `pg_publication_rel`
    - DB와 publication 사이의 관계에 대한 정보를 확인할 수 있다.
    - oid를 표시하여 가독성은 떨어진다.

  ```sql
  SELECT * FROM pg_publication_rel;
  ```

  - `pg_publication_tables`
    - DB와 Publication 사이의 관계에 대한 정보를 확인할 수 있다.
    - Publication에 포함된 table의 정보를 조회할 수 있다.

  ```sql
  SELECT * FROM pg_publication_tables;
  ```

  - `pg_subscription`
    - Logical replication의 subcription에 대한 정보를 확인할 수 있다.

  ```sql
  SELECT * FROM pg_subscription;
  ```

  - `pg_subscription_rel`
    - Subscription과 publication 사이의 관계를 표현한다.

  ```sql
  SELECT * FROM pg_subscription_rel;
  ```

  - `pg_stat_subscription_stats`
    - Logical replication의 subscription error를 보여준다.
    - PostgreSQL 15부터 사용이 가능하다.

  ```sql
  SELECT * FROM pg_stat_subscription_stats;
  ```





# View

- Materialized View
  - 논리적인 table인 view와 달리 물리적으로 존재하는 table이다.
    - 자주 사용되는 view의 결과를 disk에 저장해서 query 속도를 향상시키는 방식이다.
  - PostgreSQL뿐 아니라 OracleDB 등에서도 지원한다(MySQL은 아직 지원하지 않는다).



- Materialized View 생성하기

  - `product` table 생성하기

  ```sql
  CREATE TABLE product (
    id INT NOT NULL,
    name VARCHAR(30) NOT NULL,
    updated_time TIMESTAMP NOT NULL default current_timestamp,
    PRIMARY KEY (id)
  );
  
  INSERT INTO product VALUES (0, 'iPad');
  
  INSERT INTO product VALUES (1, 'iPhone');
  
  INSERT INTO product VALUES (2, 'AirPods');
  ```

  - `description` table 생성하기

  ```sql
  CREATE TABLE "description" (
  	"id" INTEGER NOT NULL,
  	"description" TEXT NOT NULL,
  	PRIMARY KEY ("id")
  );
  
  INSERT INTO description VALUES (0, 'An iPad is a line of tablet computers designed, developed, and marketed by Apple Inc.');
  
  INSERT INTO description VALUES (1, 'An iPhone is a line of smartphones designed and marketed by Apple Inc.');
  
  INSERT INTO description VALUES (2, 'AirPods are a line of wireless earbuds designed and marketed by Apple Inc.');
  ```

  - Materialized view 생성

  ```sql
  CREATE MATERIALIZED VIEW product_with_description AS
  SELECT
      p.id,
      p.name,
      p.updated_time,
      d.description
  FROM
      product p
  LEFT JOIN
      description d
  ON p.id = d.id;
  ```

  - 조회하기

  ```sql
  SELECT * FROM product_with_description;
  ```



- Materialzied View 갱신하기

  - Materialized view는 자동으로 갱신되지 않는다.
    - 일반적인 view의 경우 매 번 결과를 조회하여 view를 생성하므로 항상 최신 데이터를 보여준다.
    - 그러나 materialized view는 갱신을 시켜줘야하며, 갱신하기 전에는 기반 table의 변경 사항(추가, 수정, 삭제)이 반영되지 않는다.
  - SQL로 갱신하기
    - SQL을 실행하여 수동으로 갱신시키는 방식이다.

  ```sql
  REFRESH MATERIALIZED VIEW <materialized_view_name>;
  ```

  - Trigger function에서는 DDL을 실행할 수 없어 trigger 함수를 등록하는 방식은 불가능한 것으로 보인다.
  - [pg_cron](https://github.com/citusdata/pg_cron)을 사용하여 주기적으로 갱신되도록 cron job을 설정할 수 있다.

