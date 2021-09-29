

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

  
