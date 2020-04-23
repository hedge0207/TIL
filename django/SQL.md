# 데이터 베이스

- 데이터 베이스: 여러 사람이 공유하여 사용할 목적으로 체계화해 통합, 관리하는 데이터의 집합
- DBMS: 데이터베이스(DataBase)를 관리(Manage)하는 시스템(System)

  - RDBMS: 관계형 모델을 기반으로 하는 데이터베이스 관리 시스템
    - Oracle, MySQL, SQLite 등이 있으나 수업에는 SQLite를 사용
- 관계형 데이터 베이스
  - 관계를 열과 행으로 이루어진 테이블 집합으로 구성(e.g.엑셀)
  - 각 열에 특정 종류의 데이터를 기록
  - 테이블의 행은 각 객체/엔터티와 관련된 값의 모음
- RDBMS와 NOSQL
  - RDBMS: RDBMS: 관계형 데이터 베이스, 데이터를 테이블 기반으로 처리한다. 스키마에 따라 데이터를 저장하여야 하기 때문에 명확한 데이터 구조를 보장하며 각 데이터에 맞게 테이블을 나누어 데이터 중복을 피해 데이터 공간을 절약 할 수 있다는 장점이 존재한다.
  - NOSQL: RDBMS와는 달리 데이터 간의 관계를 정의하지 않는다. 스키마가 존재하지 않는다. 따라서 자유롭게 데이터를 추가가 가능하다는 장점이 존재한다.



- 기본 용어

  - 스키마: 데이터 베이스에서 자료의 구조(e.g. datatype)와 제약조건(e.g.비워 둬도 되는지)에 관한 전반적 명세
  - 테이블: 열과 행의 모델을 사용해 조직된 데이터 요소들의 집합
    - column(열): 속성, 각 열에는 고유한 데이터 형식이 있다. 고유한 데이터 형식이 지정되는 열
    - row(행, 레코드): 단일 구조 데이터 항목을 가리키는 행, 데이터가 저장되는 곳 
    - PK: 각 행의 고유값으로, 저장된 레코드를 고유하게 식별할 수 있는 값



- 데이터베이스 장단점

  - 장점
    - 데이터 중복 최소화
    - 데이터 공유
    - 일관성, 무결성, 보안성
    - 데이터의 표준화 기능
    - 용이한 데이터 접근

  - 단점
    - 전문가 필요
    - 비용 부담
    - 백업과 복구가 어려웁
    - 시스템 복잡함
    - 과부하 발생



- 데이터 무결성: 데이터의 정확성과 일관성을 유지하는 것
  - 개체 무결성(Entitiy Integrity): 모든 테이블이  고유한 기본키(PK)를 가져야 하며, 빈 값은 허용되지 않음
  - 참조 무결성(Referntial Integrity): 모든 외래키 값은 참조 릴레이션의 기본키거나 NULL
  - 도메인 무결성(Domain Integrity): 정의된 도메인에서 모든 열(속성)이 선언되도록 규정







# SQL(Structured Query Language) 기본

- Query란 DB에 보내는 요청이라고 할 수 있다.
- 지금까지는 ORM을 통해서 DB에 접근했었다. 

  - 파이썬 클래스를 통해서 DB에 접근
  - 파이썬 코드를 SQL로 변경해서 실행하는 방식
  - ORM을 통해 SQL보다 편리하게 데이터베이스를 다룰 수 있었다.
  - 그럼에도 SQL을 배워야 하는 이유는 결국 ORM은 남이 짜놓은 코드이기에 한계가 있다.

- 데이터 베이스 관리를 위한 언어, RDBMS의 데이터를 관리하기 위해 사용하는 프로그래밍 언어

- 종류

  - DDL(데이터 정의 언어):데이터 정의(create,drop 등)
  - DML(데이터 조작 언어): 데이터 저장, 수정, 삭제(CRUD 관련)
  - DCL(데이터 제어 언어): 데이터베이스 사용자의 권한 등 제어

- SQL에서의 Datetype

  - INTEGER, TEXT, REAL(실수), NUMERIC(boolean), BLOB



- 테이블 생성, 삭제

  - 실행

  ```bash
  $ sqlite3 db.sqlite3
  
  #종료는 ctrl+d
  ```

    - sqlite에서만 사용 가능한 명령어

  ```sql
  --내가 생성한 table들 보기
  .tables
  --내가 생성한 테이블의 스키마 보기
  .schema 테이블명
  ```

  

    - 테이블 생성

  ```sql
  CREATE TABLE 테이블명 (
    컬럼명 datetype [constraints]
  )
  
  --이미 동일한 테이블이 있으면 생성하지 안음
  CREATE TABLE IF NOT EXISTS '테이블명' (
    컬럼명 datetype [constraints]
  )
  
  
  --예시
  sqlite>CREATE TABLE classmates(
      id는 숫자 타입이며, primary키 역할을 하고, 자동으로 1씩 증가한다.
      id INTEGER PPIMARY KEY AUTOINCREMENT, 
      name TEXT NOT NULL,  NOT NULL은 비워 둘 수 없다는 의미이다.
      age INTEGER,
      address TEXT
  )
  ```

    - 테이블 이름 변경

  ```sql
  ALTER TABLE 테이블명 RENAME TO 새 테이블명;
  ```

    - 테이블 삭제

  ```sql
  DROP TABLE table;
  ```



  - CRUD

    - 테이블에 데이터 추가(C)

    ```sql
    INSERT INTO 테이블명 (column) VALUES (value);
    ex. INSERT INTO 테이블명 (name,age) VALUES ('홍길동',23);
    
    --모든 column에 데이터를 넣을 때는 column을 입력할 필요가 없다. 순서대로 입력만 해주면 된다.
    ex. INSERT INTO 테이블명 VALUES ('홍길동',23, '대전');
    ```

      - 다른 곳에 작성한 sql파일을 불러와 추가하는 방법 
        - db파일과 동일한 위치에 csv파일을 만든다.
        - 터미널 창에 아래의 명령어 입력

    ```
    #date.csv
    
    #아이디는 이미 저장된 것과 겹치면 안된다.
    id,flight_num,departure,waypoint,arrival,price #헤더, 굳이 안 써도 된다.
    4,RT9122,Madrid,Beijing,Incheon,200   #공백을 넣으면 안된다. 공백을 넣으면 공백도 포함됨 
    5,XZ0352,LA,Moscow,Incheon,800 
    6,SQ0972,London,Beijing,Sydney,500
    ```

    ```sql
    sqlite> .mode csv
    sqlite> .headers on  --헤더가 있다는 것을 알려주고, 없으면 안 써도 된다.
    sqlite> .separator "," --""안에 csv파일 내의 자료들이 무엇으로 구분되어 있는지 적으면 된다.
    sqlite> .import data.csv flights
    ```

    

      - 테이블의 데이터 삭제(D)

    ```sql
    DELETE FROM 테이블명 WHERE 조건;
    ```

      - 수정(U)

    ```sql
    UPDATE 테이블명 SET column=value WHERE 조건;
    
    --여러 개를 수정하고자 하면 콤마로 구분하여 연속해서 입력
    UPDATE 테이블명 SET column1=value1, column2=value2 WHERE 조건;
    ```

      - 레코드 조회(R)

    ```sql
    --select문: 데이터를 읽어올 수 있으며 특정 테이블을 반환한다.
    SELECT column FROM 테이블명;   column칸에 *을 입력하면 모든 column을 조회
    
    --distinct: 중복 없이 가져오기
    SELECT DISTINCT column FROM 테이블명;
    ```




  - 표현식

    - count: 특정 테이블에 특정 레코드의 개수

    ```sql
    SELECT COUNT(column) FROM 테이블명;
    ```

    - avg: 특정 테이블에 특정 레코드의 평균

    ```sql
    SELECT AVG(column) FROM 테이블명;
    ```

    - sum: 특정 테이블에 특정 레코드의 합

    ```sql
    SELECT SUM(column) FROM 테이블명;
    ```

    - MIN: 특정 테이블에 특정 레코드의 최소값

    ```sql
    SELECT MIN(column) FROM 테이블명;
    ```

    - MAX: 특정 테이블에 특정 레코드의 최대값

    ```sql
    SELECT MAX(column) FROM 테이블명;
    ```

    

  - where: 조건문을 활용

    - 기본형

    ```sql
    SELECT column FROM 테이블명 WHERE 조건;
    
    --아래와 같이 and나 or을 사용할 수도 있다.
    SELECT column FROM 테이블명 WHERE 조건1 and/or 조건2;
    ```

    - like 활용: 특정 패턴을 보여준다.

    ```sql
    SELECT column FROM 테이블명 WHERE cloumn LIKE '패턴';
    
    --e.g.like 활용
    sqlited>SELECT * FROM classmates WHERE phone LIKE '010-%'
    ```

    - like에서 사용되는 키워드(와일드카드)

    | %:문자열이 있을 수도 있다.    | 2%      | %앞의 문자(이 경우 2)로 시작하는 값           |
    | ----------------------------- | ------- | --------------------------------------------- |
    |                               | %2      | %뒤의 문자로(이 경우2)로 끝나는 값            |
    |                               | %2%     | %사이의 문자(이 경우2)가 들어가는 값          |
    | _:반드시 한 개의 문자가 있다. | _2%     | 아무 값이나 들어가고 두번째가 2로 시작하는 값 |
    |                               | 1___    | 1로 시작하고 4자리인 값                       |
    |                               | 2\_%\_% | 2로 시작하고 적어도 3자리인 값                |




  - order_by: 특정 column을 기준으로 정렬

    ```sql
    SELECT column FROM 테이블명 ORDER BY column1 ASC/DESC column2 ASC/DESC;
    
    --column을 column1, column2 기준으로 오름/내림차순으로 정렬한다.
    --ASC: 오름차순(기본값)
    --DESC: 내림차순
    ```



- limit: 특정 테이블에서 원하는 개수만큼 가져오기

  ```sql
  SELECT column FROM 테이블명 LIMIT 숫자;
  ```



- offset: 특정 테이블에서 원하는 개수만큼 가져오기2

  ```sql
  --숫자2에서 1을 뺀 숫자에서부터(cf.인덱스) 숫자1만큼 가져온다.
  SELECT column FROM 테이블명 LIMIT 숫자1 offset 숫자2;
  ```



- gruop by: 특정 컬럼을 기준으로 그룹화

  ```sql
  SELECT column1 FROM 테이블명 GROUP BY column2;
  
  --column2를 기준으로 column1을 그룹화
  ```





# ORM

ref. migrate 할 경우 테이블명은 `앱이름_모델명(소문자)`으로 생성된다.

- orm과 sql
  - orm에서는 model을 정의하고 migrate를 해줘야 했다.
  - sql에서는 그 대신 테이블을 생성한다.
  - orm은 쿼리셋 형태로, sql은 테이블 형태로 데이터를 저장
    - 쿼리셋은 쿼리의 결과로 나오는 오브젝트이다.



- 쿼리의 메서드

  - 조회

    - get: 오직 하나의 쿼리 결과만을 반환, 하나가 아니면 모두 에러

      -ex. 특정 게시글로 연결해 줄 경우 하나의 게시글 번호를 요청한 것이 아니면 모두 에러를 띄운다.

    - filter: 쿼리셋(비어 있더라도)을 반환

      -ex.검색을 할 때에는 그에 해당하는 모든 게시글을 보여주고, 검색 결과가 없어도(비어도) 보여준다.

      - and: 메서드 체이닝, 인자로 넘겨주는 방식
      - or : Q로 묶어서 처리한다.
      - 대소관계
      - 패턴



- ORM 문법

  - 테이블 생성: sql의 테이블 생성에 대응하는 orm의 테이블 생성은 model을 정의하고 migrate하는 것

  - 모든 레코드 조회(R)

    > sql의 `select * from`

    ```shell
    모델명.objects.all()
    ```

    

  - 특정 레코드 조회(R)

    > sql의 `WHERE`

    ```shell
    User.objects.get(id=100)  #get은 오직 하나의 쿼리 결과만을 반환
    ```

    

  - 레코드 생성(C) - 기존의 C방식과 동일하게 하면 된다.

    > sql의 `INSERT INTO`

    ```shell
    #이 외의 2가지 방법을 사용해도 만들 수 있다(ref. CRUD 파트).
    모델명.objects.create(column=value)
    ```

    

  - 레코드 수정(U) 

    > sql의 `SET`

    ```python
    모델명오브젝트=.objects.get(조건)
    오브젝트.column = 수정할 내용
    오브젝트.save()
    
    #e.g.
    user = User.objects.get(id=100)
    user.last_name = '성'
    user.save()
    ```

    

  - 레코드 삭제(D)

    > sql의 `DELETE`

    ```
    모델명.objects.get(조건).delete()
    ```

    

  - 조건에 따른 쿼리문

    - 개수 세기

      >sql의 `COUNT`

    ```python
    모델명.objects.count()
    
    #e.g.
    User.objects.count()
    ```

    - 조건에 따른 값

      > sql의 `WHERE`

    ```python
    모델명.objects.filter(조건).values(가져올 값)
    
    #e.g.
    User.objects.filter(age=30).values('first_name')
    
    
    #조건이 2개 이상일 경우
    
    #조건이 AND일 경우
    #방법1
    모델명.objects.filter(조건1, 조건2).values(가져올 값)
    User.objects.filter(age=30, last_name='김').count()
    
    #방법2
    모델명.objects.filter(조건1).filter(조건2).values(가져올 값)
    User.objects.filter(age=30).filter(last_name='김').count()
    
    #방법2와 같이 filter에 다시 filter를 쓰는 것이 가능한 이유
    #filter의 결과도 queryset이기에 다시 filter 적용이 가능하다(기린의 번식의 결과 기린이 나오고 그 기린이 자라서 다시 번식이 가능한 것과 비슷하다).
    
    
    #조건이 OR일 경우
    from django.db.models import Q  #Q를 import해야 한다.
    #Q로 묶고 |로 구분한다.
    모델명.objects.filter(Q(조건1)|Q(조건2))
    
    #e.g.
    User.objects.filter(Q(balance__gte=2000)|Q(age__lte=40)).count()
    ```

  

  - lookup

    ```python
    모델명.objects.filter(column__lookup)
    ```

    - 대소관계

    ```python
    '''
    __gte:>=
    __gt:>
    __lte:<=
    __lt:<
    '''
    
    #e.g.
    User.objects.filter(age__gte=30)
    ```

    - 문자열 포함 관련

    ```python
    #i라는 prefix는 case-insensitive(대소문자 구분X)의 의미를 지닌다.
    """
    iexact: 정확하게 일치하는가
    contains, icontains: 특정 문자열을 포함하는가
    startswith, istartswith: 특정 문자열로 시작하는가
    endswith, iendswith: 특정 문자열로 끝나는가
    """
    
    #e.g.
    User.objects.filter(phone__startswith='02-') #02로 시작하는 데이터를 조회
    ```

    

  - 기타

    - 정렬

    ```python
    #내림차순
    모델명.objects.order_by('-column')
    
    #오름차순
    모델명.objects.order_by('column')
    
    #제한을 둘 경우(sql의 LIMIT)
    모델명.objects.order_by('column')[:숫자]
    
    #임의의 순서를 찾을 경우(sql의 OFFSET)
    모델명.objects.order_by('column')[숫자] #0부터 시작
    ```

    - 중복 없이 조회하고자 할 경우

    ```python
    #distinct()사용
    #e.g.
    #phone이 ‘011’로 시작하는 사람들의 나이를 중복 없이 조회
    User.objects.filter(phone__startswith='011').values('age').distinct()
    ```

    

  - 표현식

    - 표현식 사용을 위해서는 `aggregate`를 알아야 한다.

    ```python
    from django.db.models import Sum,Avg,Max,Min
    
    모델명.objects.aggregate(표현식)
    
    #e.g.
    User.objects.aggregate(Avg('age'))
    ```

    

  - group by

    - annotate는 개별 item에 추가 필드를 구성한다.

    ```python
    모델명.objects.values('column').annotate(표시할 내용)
    ```

    



# 1:N

- 관계형 데이터베이스에서는 데이터들 사이에 관계를 맺을 수 있는데, 하나의 데이터가 여러개의 데이터와 관계를 맺을 경우, 두 데이터의 관계를 1:N의 관계라고 한다.

  

- FK(Foreign Key, 외래키)

  - 데이터와 데이터의 관계에서 한 쪽의 PK값은 다른 데이터로 넘어가면 FK값이 된다.

  - 일반적으로 N의 위치에 있는 데이터가 FK값을 가진다.

  - 유저 정보를 관리하는 db테이블에 각 유저가 작성한 글을 저장하는 것 보다는 게시글 정보를 관리하는 db테이블에 유저 정보를 저장하는 것이 더 낫다.

  - 만일 유저 정보를 관리하는 db테이블에서 각 유저가 글을 작성할 때마다 그 글에 대한 정보를 db테이블에 장한다면 유저 정보를 관리하는 테이블은 무한히 늘어나야 할 것이다.
  
    | user |          |                 |                 |                 |      | article |          |
    | ---- | -------- | --------------- | --------------- | --------------- | ---- | ------- | -------- |
    | id   | nickname | create_article1 | create_article2 | create_article3 | ...  | title   | content  |
  | 1    | name1    | title1,content1 | article         | ...             |      | title1  | content1 |
    | 2    | name2    | title2,content2 | article1        | ...             |      | title2  | content2 |

  - 반면에 게시글 정보를 관리하는 db테이블에 유저 정보를 저장한다면 게시글 마다 유저 정보만 추가시켜주면 된다. 
  
    | user |          |      | article |          |             |
    | ---- | -------- | ---- | ------- | -------- | ----------- |
    | id   | nickname |      | title   | content  | user_id(FK) |
  | 1    | name1    |      | title1  | content1 | 1           |
    | 2    | name2    |      | title2  | content2 | 2           |

  - 유저의 PK값을 게시글 db에 저장한다. 그리고 원래 db가 아닌 다른 db에서 사용되는 pk값을 fk값이라고 부른다(유저db의 pk값을 게시글db에서 쓴다면 같은 값을 유저 db에서는 pk로, 게시글 db에서는 fk로 부른다).
  
  - 이 경우 한 명의 유저는 여러 개의 게시글을 작성할 수 있으므로 유저와 게시글 사이에 1:N의 관계가 성립한다고 볼 수 있다.



- django에서의 활용

  ```python
  # Creater 모델을 생성
  class Creater(models.Model):
      username = models.CharField(max_length=5)
  
  # POST 모델을 생성
  class Post(models.Model):
      title = models.CharField(max_length=10)
      content = models.TextField()
      creater = models.ForeignKey(Creater, on_delete=models.CASCADE)
      #ForeignKey는 첫 인자로 참고할 모델(Creater)을 넘긴다.
      #두 번째 인자로 on_delete를 넘긴다.
      #여기서 creater가 아닌 creater_id로 하는 것이 맞다고 생각할 수 있지만 필드가 ForeignKey 라면	   creater로 넘겨도 djnago에서 내부적인 처리를 통해 creater_id로 넘어가게 된다.
  ```

  - on_delete는 Django에서 모델을 구현할 때 데이터베이스 상에서 참조무결성을 유지하기 위해서 ForeignKeyField가 바라보는 값이 삭제될 때 해당 요소를 처리하는 방법을 지정하는 것이다.
    - CASCADE : ForeignKeyField를 포함하는 모델 인스턴스(row)도 같이 삭제한다.
    - PROTECT : 해당 요소가 같이 삭제되지 않도록 ProtectedError를 발생시킨다.    
    - SET_NULL : ForeignKeyField 값을 NULL로 바꾼다. null=True일 때만 사용할 수 있다.

    - SET_DEFAULT : ForeignKeyField 값을 default 값으로 변경. default 값이 있을 때만 사용 가능   
    - SET() : ForeignKeyField 값을 SET에 설정된 함수 등에 의해 설정한다.  
    - DO_NOTHING : 아무런 행동을 취하지 않는다. 참조 무결성을 해칠 위험이 있어, 잘 사용되지는 않는다.

  ```python
  #4개의 reporter를 생성
  Creater.objects.create(username='파이리')
  Creater.objects.create(username='꼬부기')
  Creater.objects.create(username='이상해씨')
  Creater.objects.create(username='피카츄')
  
  #creater1에 파이리(1)를 넣는다.
  creater1=Creater.objects.get(pk=1)
  
  
  #post(N)를 생성한다.
  post1 = Post()
  post1.title = '제목1'
  post1.content = '내용1'
  # creater는 creater 오브젝트를 저장
  post1.creater = r1
  # creater_id는 숫자(INTEGER)를 저장
  # a1.reporter_id = 1 
  post1.save()
  
  post2 = Post.objects.create(title='제목2', content='내용2', creater=creater1)
  
  
  #1(파이리):N(posts)관계 활용
  #`post` 의 경우 `creater`로 1에 해당하는 오브젝트를 가져올 수 있다.
  #`creater`의 경우 `post_set` 으로 N개(QuerySet)를 가져올 수 있다.
  
  #글의 작성자
  post1 = Post.objects.get(pk=2)
  post1.reporter
  
  # 2. 글의 작성자의 username
  post1.creater.username
  
  # 3. 글의 작성자의 id
  post2.creater.id
  post2.creater_id
  
  # 4. 작성자(1)의 글
  creater1 = Creater.objects.get(pk=1)
  creater1.post_set.all()  
  #전부 가져오는 것이 아닌 특정 조건을 충족하는 것들을 가져오고 싶다면
  creater1.post_set.filter()  
  ```

  

- 실제 장코 코드에서의 활용

  - 게시글(1)과 댓글(N)의 1:N의 관계

  ```python
  #models.py
  from django.db import models
  
  class POST(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  
  class Comment(models.Model):
      content=models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      post = models.ForeignKey(Article, on_delete=models.CASCADE)
      #위처럼 post_id가 아닌 post로 넘기면 post_id로 등록된다.
  ```

  ```python
  #forms.py
  from django import forms
  from .models import POST, Comment
  
  class PostForm(forms.ModelForm):
      class Meta:
          model = Article
          fields = '__all__'
  
  
  class CommentForm(forms.ModelForm):
      class Meta:
          model = Comment
          # fields = '__all__'을 하면 post_id도 넘어가게 되는데 그럼 댓글을 입력할 때 				post_id도 입력하게 된다. 따라서 post는 넘기지 않는다.
          fields = ['content']
          # updated_at,created_at은 자동으로 넘어간다.
  ```

  ```python
  #views.py
  from django.shortcuts import render, redirect, get_object_or_404
  from django.views.decorators.http import require_POST
  from django.contrib.auth.decorators import login_required
  from .forms import PostForm, CommentForm
  
  #유저 정보를 넘기지 않을 때의 구조(기존의 구조)
  @require_POST
  @login_required
  def comments_create(request,post_pk):
      form = CommentForm(request.POST)
      post=get_object_or_404(Post,pk=post_pk)
      if form.is_valid():
          comment=form.save()
      return redirect('posts:detail', post.pk)
  
  
  
  #유저 정보를 넘길 때의 구조
  #아래에는 comments_create를 예로 들었지만 실제로 유저 정보를 저장해야 하는 모든 것들(게시글 작성, 게시글 수정)에도 해줘야 한다. 단, 게시글 수정의 경우 작성자가 아닌 사람이 게시글을 수정하는 경우는 없을 것이므로 하지 않아도 큰 문제는 없지만 만에 하나 오류가 발생할 수 있으므로 해준다.
  @require_POST
  @login_required
  def comments_create(request,post_pk):
      form = CommentForm(request.POST)
      post=get_object_or_404(Post,pk=post_pk)
      if form.is_valid():
          comment=form.save(commit=False)
          """
          comment=form.save()를 하는 것이 아니라 comment=form.save(commit=False)를 하는 이유		 는 만일 바로 db에 반영(save)을 하면, 아직 post_id값은 넣어준 적이 없으므로 NULL값이다. 따		  라서 오류가 발생하게 된다. 그렇다고 save()안하고 comment=form를 할 수도 없다. form은 			save()를 하기 전까지는 반환받는 값이 없으므로, save()를 해줘야 비로소 다른 값에 할당할 수 		  있다. 따라서 post를 반환은 하되 데이터베이스에 반영은 하지 않는 처리를 해줘야 하는데 그 처리		 가 바로 .save(commit=False)이다.
          """
          comment.post=post  #post_id에 post.pk를 넘겨준다.
          #굳이 comment.post_id=post.pk라고 적지 않아도 알아서 id값이 넘어가게 된다.
          comment.save()
      return redirect('post:detail', post.pk)
  
  
  #댓글을 표시하는 detail페이지(게시글과 공유한다)-잘못된 방법
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comments = Comment.objects.all()
      #기존에 하던 것 처럼 위와 같이 넘기면 어떤 게시글을 보던지 같은 댓글이 보이게 된다. 따라서 각 게	 시글에 작성된 댓글만을 넘겨야 하는데 이 방법으로는 그렇게 할 수 없다.
      comment_form=CommentForm()
      context = {
          'post': post,
          'comment_form':comment_form,
          'comments':comments,
      }
      return render(request, 'post/detail.html', context)
  
  
  #댓글을 표시하는 detail페이지(게시글과 공유한다)-옳은 방법
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comments = post.comment_set.all()  #post에 작성된 comment를 모두 comments에 할당
      # 아래와 같이 쓰는 것과 같다.
      # comments=Comments.objects.filter(article_id=article.id)
      comment_form=CommentForm() #댓글 입력 창은 게시글 내에 있어야 하므로 입력from도 넘긴다.
      context = {
          'post': post,
          'comment_form':comment_form,
          'comments':comments,
      }
      return render(request, 'post/detail.html', context)
  
  #혹은 위와 같이 comments = post.comment_set.all()로 넘기는 것이 아니라 post만 넘기고 html에서 따로 처리를 해주는 방법도 있다.
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comment_form=CommentForm()
      context = {
          'post': post,
          'comment_form':comment_form,
      }
      return render(request, 'post/detail.html', context)
  #위와 같이 post를 넘긴 후
  ```
  
  ```html
  <!--아래와 같이 post.comment_set.all으로 처리하면 된다.-->
  {% load bootstrap4 %}
  <h3>댓글</h3>
      {% for comment in post.comment_set.all %}
          <li>{{ comment.user.username }} : {{ comment.content }}</li>
      {% endfor %}
      <hr>
      <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
          {% csrf_token %}
          {% bootstrap_form form %}
          <button class="btn btn-primary">작성</button>
      </form>
  
  <!--또는 detail함수에서 comments = post.comment_set까지만 넘겨받아 아래와 같이 쓸 수도 있다.-->
  
  {% load bootstrap4 %}
  <h3>댓글</h3>
      {% for comment in comments.all %}
          <li>{{ comment.user.username }} : {{ comment.content }}</li>
      {% endfor %}
      <hr>
      <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
          {% csrf_token %}
          {% bootstrap_form form %}
          <button class="btn btn-primary">작성</button>
      </form>
  ```
  
  ```html
  <!--로그인 한 사용자와 글 작성자가 같은 사용자일 경우에만 특정 내용을 띄우는 방법-->
  <!--아무나 게시글을 삭제하게 해선 안되므로 아래와 같이 게시글의 유저와 요청을 보낸 유저가 같을 때에만 게시글 삭제 창을 띄우게 할 수 있다.-->
  
  {% if article.user == request.user  %}
      <form action="{% url 'articles:delete' article.pk %}" method="POST">
          {% csrf_token %}
          <button class="btn btn-primary">삭제</button>
      </form>
  {% endif %}
  <!--==을 쓸 때는 반드시 좌우 한 칸씩을 띄워야 하며 띄우지 않을 경우 오류가 발생한다. 또한 == 대신 is를 사용 가능하다-->
  ```
  
  ```python
  #아래와 같이 함수 내에서 request.user, 즉 로그인한 유저의 정보를 사용하고자 한다면 @login_required를 붙여주는 것이 좋다. 로그인하지 않았을 경우 request.user에는 Anonymous 유저가 들어가게 되는데 자칫하면 에러가 발생할 수 있다. 
  
  @login_required
  def delete(request):
      request.user.delete()
      return redirect('articles:index')
  ```
  
  
  
- ERD: 데이터베이스 모델링에서 활용되는 다이어그램(추가 필요)
  - 카디널리티: 데이터 사이의 논리적 관계
    - 1:1 관계(직선)
    - 1:N 관계(까마귀 발이  있는 쪽이 N)
  - 데이터베이스 관계선택사항/옵셔널리티
    - 게시글 입장에서 댓글은 필수가 아니나, 댓글 입장에서는 게시글이 필수다.








