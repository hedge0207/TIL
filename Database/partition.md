# partition

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



- Partition 추가

  ```sql
  alter table test add PARTITION
  (PARTITION p20210217 VALUES LESS THAN (2017) ENGINE = InnoDB,
   PARTITION p20210218 VALUES LESS THAN (2018) ENGINE = InnoDB, 
   PARTITION p20210219 VALUES LESS THAN (2019) ENGINE = InnoDB, 
   PARTITION p20210223 VALUES LESS THAN (2020) ENGINE = InnoDB)
  ```



- Partition 조회

  ```sql
  SELECT * FROM information_schema.partitions WHERE TABLE_NAME='<테이블명>'
  ```

  




# ETC

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

  

  