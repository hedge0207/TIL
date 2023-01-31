

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

  

  
