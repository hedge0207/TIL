# MongoDB 소개

- MongoDB
  - 기존에는 MySQL, OracleDB, PostgreSQL 같은 RDBMS(관계형 데이터베이스)를 자주 사용했다.
    - 그런데 RDBMS에는 몇 가지 한계가 있다.
    - 데이터 스키마가 고정적이다. 따라서 새로 등록하는 형식이 기존에 있던 데이터들과 다르다면 기존 데이터를 모두 수정해야 한다.
    - 확장성이 낮다. RDBMS는 저장하고 처리해야 할 데이터 양이 늘어나면 여러 컴퓨터에 분산시키는 것이 아니라, 해당 데이터베이스 서버의 성능을 업그레이드 해주는 방식으로 확장해 주어야 했다.
  - MongoDB는 이런 한계를 극복한 문서 지향적 NoSQL 데이터베이스이다.
    - 유동적인 스키마를 지닌다.
    - 서버의 데이터양이 늘어나도 한 컴퓨터에서만 처리하는 것이 아니라 여러 컴퓨터로 분산하여 처리할 수 있도록 확장하기 쉽게 설계되어 있다.
  - 그렇다고 MongoDB가 무조건 기존의 RDBMS보다 좋다는 것은 아니다.
    - 상황별로 적합한 DB가 다를 수 있다.
    - 데이터의 구조가 자주 바뀐다면 MongoDB가 유리하다.
    - 까다로운 조건으로 data를 필터링하거나, ACID 특성을 지켜야 한다면 RDBMS가 더 유리할 수 있다.
    - ACID : 원자성(Atomicity), 일관성(Consistency), 고립성(Isolation), 지속성(Durability)의 앞 글자를 따서 만든 용어로, DB 트랜잭션이 안전하게 처리되는 것을 보장하기 위한 성질이다.



- 문서란

  - 문서 지향적이라는 말에서 문서란 RDBMS의 레코드와 개념이 비슷하다.
    - 문서의 데이터 구조는 한 개 이상의 키-값 쌍으로 되어 있다.
  - 문서는 **BSON(바이너리 형태의 JSON)** 형태로 저장된다.
    - 따라서 나중에 JSON 형태의 객체를 DB에 저장할 때, 큰 공수를 들이지 않고도 data를 DB에 등록할 수 있어 매우 편리하다.
    - 문서 하나에는 최대 16MB 만큼 데이터를 넣을 수 있다.
  - `_id`
    - 새로운 문서를 만들면 `_id`라는 고윳값을 자동으로 생성한다.
    - 이 값은 시간, 머신 아이디, 프로세스 아이디, 순차 번호로 되어 있어 값의 고유함을 보장한다.

  - 여러 문서가 들어 있는 곳을 **컬렉션**이라 한다.
    - 기존 RDBMS에서는 테이블 개념을 사용하므로 각 테이블마다 같은 스키마를 가지고 있어야 한다.
    - 새로 등록해야 할 데이터가 다른 스키마를 가지고 있다면, 기존 데이터들의 스키마도 모두 바꿔 줘야 한다.
    - 반면 MongoDB는 다른 스키마를 가지고 있는 문서들이 한 컬렉션에서 공존할 수 있다.



- MongoDB 구조와 스키마 디자인
  - MongoDB 구조
    - 서버 하나에 DB를 여러 개 가지고 있을 수 있다.
    - 각 DB에는 여러 개의 컬렉션이 있으며, 컬렉션 내부에는 문서들이 들어 있다.
  - 스키마 디자인
    - 기존 RDBMS에서 스키마를 디자인하는 방식과 완전히 다르다.
    - RDBMS에서 블로그용 DB를 설계한다면, 각 포스트, 댓글마다 테이블을 만들어 필요에 따라 JOIN해서 사용하는 것이 일반적이다.
    - 그러나 NoSQL에서는 그냥 모든 것을 문서 하나에 넣는다. 즉, 포스트 문서 내부에 댓글을 넣는다.
    - 포스트 문서 내부에 댓글 문서를 넣는 것 처럼 문서 내부에 또 다른 문서가 위치할 수 있는데 이를 **서브다큐먼트**라 한다.



- Cluster
  - MongoDB는 고가용성과 확장성을 위해 clustering을 지원한다.
  - Replica set
    - Data를 서로 공유하는 MongoDB node들을 의미한다.
    - 하나의 primary node와 0개 이상의 secondary node로 구성된다.
    - Primary node는 모든 쓰기 요청을 받는 역할을 하며, primary node의 모든 변경사항은 operaion log(oplog)라 불리는 collection에 기록된다.
    - Secondary node는 primary node의 operation log를 복제하여 primary node의 data와 동일한 data를 유지하는 역할을 한다.
    - Primary와 secondary node의 data 복제 작업은 비동기적으로 동작하기에 동일하지 않은 상태가 발생할 수도 있다.
    - 만약 primary node가 사용 불가능한 상태가 되면 secondary node들 중에서 새로운 primary node를 선출한다.
    - Arbiter node는 primary나 secondary node의 역할은 수행하지 않고 오직 선출에만 관여하는 node이다.
  - Replica set election이 발생하는 경우
    - Replica set이 시작 될 때.
    - Primary node가 사용 불가 상태일 때.
    - Replica set에 새로운 node가 합류할 때.
    - Secondary node가 primary node와 연결이 끊겼을 때.
  - Read preference
    - 기본적으로 모든 읽기 작업은 primary node로 전달되지만 어떤 node로 전달할지 선택할 수도 있는데, 이를 read preference라 한다.
    - primary, secondary, primary preferred, secondary preferred 등을 설정할 수 있다.
    - 그러나 primary와 secondary 사이의 데이터 복제는 비동기적으로 발생하기에 secondary에서 read할 경우 최신 data가 아닐 수 있다는 점은 주의해야한다.
  - Write concern
    - Data를 작성할 때, 작성한 data가 cluster에 제대로 전파되는를 확인하기 위해서 write concern 옵션을 줄 수 있다.
    - `w`에는 숫자를 설정하며, 이는 primary를 포함하여 몇 개의 node에서 쓰기 작업이 잘 되었는지 확인할지를 설정한다.
    - 만약 0일 경우 쓰기 작업이 잘 되었는지 확인하지 않겠다는 의미이고, 1이면 쓰기 작업이 잘 되었는지 primary node에서만 확인하겠다는 의미이다.
    - 만약 4라면 primary node + 3개의 secondary node에서 확인하겠다는 의미이다.
    - `j`에는 journal이라 불리는 disk 내의 특수 구역에 data를 저장할지를 설정하며, journal에 저장된 data는 MongoDB를 복구할 때 사용한다.
    - `wtimeout`은 응답이 올 때 까지 기다리는 시간을 설정한다.





# MongoDB 설치하기

> https://www.mongodb.com/compatibility/deploying-a-mongodb-cluster-with-docker

- Docker compose로 cluster 설치하기

  - MongoDB 공식 image를 pull 받는다.
  
  ```bash
  $ docker pull mongo[:version]
  ```
  
  - 아래와 같이 docker-compose.yml 파일을 작성한다.
  
  ```yaml
  version: '3.2'
  
  
  services:
    my-mongo1:
      image: mongo:latest
      container_name: my-mongo1
      command: mongod --replSet myReplicaSet --bind_ip localhost,my-mongo1
      ports: 
        - 27017:27017
      restart: always
      networks:
        - mongo-network
    
    my-mongo2:
      image: mongo:latest
      container_name: my-mongo2
      command: mongod --replSet myReplicaSet --bind_ip localhost,my-mongo2
      ports: 
        - 27018:27017
      restart: always
      networks:
        - mongo-network
    
    my-mongo3:
      image: mongo:latest
      container_name: my-mongo3
      command: mongod --replSet myReplicaSet --bind_ip localhost,my-mongo3
      ports: 
        - 27019:27017
      restart: always
      networks:
        - mongo-network
  
  networks:
    mongo-network:
      driver: bridge
  ```
  
  - 아래 명령어를 통해 container를 생성하고 실행한다.
  
  ```bash
  $ docker compose up
  ```
  
  - 아래 명령어를 실행하여 replica set을 initiate한다.
    - `_id`에는 위 docker compose file에서 command의 `--replSet`에 적어준 값(이 경우 myReplicaSet)을 적어준다.
    - `members.host`에는 각 MongoDB node의 container name을 적어준다.
    - 만일 client가 docker network를 사용하지 않을 경우 각 node의 `host:port`를 적어준다.
  
  ```bash
  $ docker exec -it mongo1 mongosh --eval "rs.initiate({
   _id: \"myReplicaSet\",
   members: [
     {_id: 0, host: \"my-mongo1\"},
     {_id: 1, host: \"my-mongo2\"},
     {_id: 2, host: \"my-mongo3\"}
   ]
  })"
  
  # 성공적으로 끝날 경우 { ok: 1 }가 출력된다.
  ```



- 새로운 replicaSet 추가하기

  - 아래와 같이 docker-compose file을 작성하여 MongoDB container를 생성한다.
    - 다른 서버에 해도 되고, 같은 서버에서 진행해도 된다.

  ```yaml
  version: '3.2'
  
  
  services:
    mongo4:
      image: mongo:7.0.0
      container_name: theo-mongo4
      command: mongod --replSet myReplicaSet --bind_ip localhost,mongo4
      ports: 
        - 27018:27017
      restart: always
  ```

  - 기존 primary node의 mongo shell에 접속해서 아래 명령어를 수행한다.

  ```bash
  > rs.add({host:"<새로 생성한 node의 host>:<port>"})
  ```

  - 잘 추가되었는지 확인한다.

  ```bash
  > rs.status()
  ```





## Replica Set에 새로운 member 추가 및 삭제

- Cluster 구성하기

  - 테스트를 위해 아래와 같이 docker-compose file을 작성한다.

  ```yaml
  version: '3.2'
  
  
  services:
  
    mongo1:
      image: mongo:latest
      container_name: mongo1
      command: mongod --replSet myReplicaSet --bind_ip localhost,mongo1
      ports: 
        - 27018:27017
      networks:
        - mongo-network
    
    mongo2:
      image: mongo:latest
      container_name: mongo2
      command: mongod --replSet myReplicaSet --bind_ip localhost,mongo2
      ports: 
        - 27019:27017
      networks:
        - mongo-network
    
    mongo3:
      image: mongo:latest
      container_name: mongo3
      command: mongod --replSet myReplicaSet --bind_ip localhost,mongo3
      ports: 
        - 27020:27017
      networks:
        - mongo-network
  
  networks:
    mongo-network:
      driver: bridge
  ```

  - 컨테이너들을 실행한다.

  ```bash
  $ docker compose up
  ```

  - 세 개의 노드 중 두 개 만으로 cluster를 구성한다.

  ```bash
  $ mongosh
  
  config = {
    _id: "myReplicaSet",
    protocolVersion: 1,
    members: [
      {_id:0, host: "mongo1:27017"},
      {_id:1, host: "mongo2:27017"}
    ]
  };
  
  rs.initiate(config);
  # 확인
  rs.status();
  ```



- 새로운 node 추가하기

  - 위에서 container를 실행은 했지만 replica set에 등록은 하지 않은 mongo3 node를 replica set에 추가할 것이다.

  - 확인해야 할 점

    - Replica set에 새로운 node를 추가할 때 주의할 점은 node는 반드시 하나의 replica set에만 속해야 한다는 것이다.
    - 즉, 이미 replica set에 속해 있는 node를 다른 replica set에 추가할 수 없다.

    - 또한 새로 추가되는 node의 data directory는 data가 포함되어서는 안 된다.
    - 만약 새로운 node가 recovering 상태라면, secondary 상태가 되어야 한다.

  - 만약 replica set에서 어떤 node가 primary인지 알 수 없을 경우, replica set에 속한 node 들 중 아무 곳에서나 아래 명령어를 입력하면, primary node 정보를 확인 가능하다.

  ```bash
  db.hello()
  ```

  - 기존 replica set에 새로운 node 추가하기

  ```bash
  rs.add({_id:2, host: "mongo3:27017"})
  ```

  - 정상적으로 추가 되었는지 확인한다.

  ```bash
  rs.status()
  ```



- Replica set에서 node 제거하기

  - Replica set의 primary node에서 아래 명령어를 실행한다.

  ```bash
  rs.remove("mongo3:27017")
  ```

  - 혹은 `rs.conf()`를 통해서도 가능하다.
    - 아래 예시에서는 `mongo2` node를 제거한다.

  ```bash
  # 현재 설정 복사
  config = rs.conf()
  
  # 현재 설정에서 멤버 제거
  config.members.splice(1,1)
  
  # 재설정
  rs.reconfig(cfg)
  ```






# Mongo Shell

- mongodb cli 실행

  - `mongosh` 명령어로 실행한다.
    - `mongo` 명령어로도 실행이 가능하지만 곧 사라질 예정이다.
  - 인증이 필요할 경우 아래 옵션을 준다.
    - `-u <사용자명> -p <비밀번호>`

  ```bash
  $ mongosh [옵션1] [옵션2] ...
  ```



- DB와 collection 확인

  - DB 목록 조회

  ```bash
  $ show dbs
  ```

  - DB 선택

  ```bash
  $ use <DB 명>
  ```

  - 현재 사용중인 DB 확인

  ```bash
  $ db
  ```

  - collection 목록 조회

  ```bash
  $ show collections
  ```




- 상태 확인

  - MongoDB status 조회

  ```bash
  $ rs.status()
  ```

  - Lock 확인

  ```bash
  $ db.adminCommand({lockInfo:1}).lockInfo
  ```

  - Collection 상태 확인

  ```bash
  $ db.<collection_name>.stats()
  ```



- 조회
  - `find`의 인자로 조건을 넣을 수 있다.
  - `.pretty()`는 결과를 json 형식에 맞게 출력한다.
  - 출력할 필드는 `{필드명: 0 or 1}` 형식으로 들어가며, 1일 경우에만 출력한다(아예 작성하지 않을 경우 모든 필드를 출력한다.).
  - `_id`의 경우 명시적으로 지정하지 않더라도 출력한다.

  ```bash
  $ db.<collection 명>.find([조건], [{출력할 필드들}])[.pretty()]
  
  # 예시1
  $ db.books.find({name:"hello"})
  
  # 예시2
  $ db.books.find({price:{$gt:5000, $lte:8000}}, {name, author, published_date})
  
  
  # 위 예시는 sql문으로 다음과 같다.
  select name, author. published_date from books where price > 5000 and price <=8000
  ```

  - 정렬하기
    - `sort`를 사용하여 정렬이 가능하다.
    - `{field:order}` 형식으로 설정하면 되며, `order`에 1을 줄 경우 오름차순으로, `-1`을 줄 경우 내림차순으로 정렬한다.

  ```bash
  $ db.<collection>.find().sort({<field>:<1 or -1>})
  
  # 예시
  $ db.books.find().sort({price:-1})
  ```

  - 출력 개수 제한하기

  ```bash
  $ db.<collection>.find().limit(<num>)
  ```



- 삽입

  - Database 생성
    - Mongo shell에는 create command가 따로 있지는 않고, 아래와 같이 `use`를 사용하여 context를 switching하면 된다.

  ```bash
  $ use <database_name>
  ```

  - 위 명령어만 입력했을 경우 `show dbs`를 통해 database들을 확인하더라도 아직 추가되지 않은 것을 볼 수 있다.
    - 이는 context만 변경된 것이기 때문이다.
    - Database의 실제 생성은 database에 첫 data가 저장될 때 이루어진다.
  - Document 삽입하기

  ```bash
  $ db.<collection_name>.insert(<json_data>)
  
  # db.book.insert({title:"foo", content:"bar"})
  ```

  - Collection 생성
    - Collection은 위와 같이 존재하지 않는 collection에 data를 삽입하면 자동으로 생성된다.
    - 만일 수동으로 생성하고자 한다면 아래와 같이 하면 된다.

  ```bash
  $ db.createCollection("<name>"[, options])
  
  # db.createCollection("book")
  ```



- 수정

  - `updateOne`
    - Filter에 matching되는 첫 번째 문서를 수정한다.

  ```sh
  $ db.<collection명>.updateOne(<조건>, {$set:<수정 내용>})
  
  # 예시
  $ db.books.updateOne({title:"foo"},
  {
    $set:{
      content:"Hello World",
      price: 100
    }
  })
  ```

  - `updateMany`
    - Filter에 matching되는 모든 문서를 수정한다.

  ```bash
  $ db.<collection명>.updateOne(<조건>, {$set:<수정 내용>})
  
  # 예시
  $ db.books.updateMany({title:"foo"},
  {
    $set:{
      content:"Hello World"
    }
  })
  ```

  - `replaceOne`
    - Document를 새로운 document로 대체한다.
    - 단, 이 때 `_id` field는 유지된다.
    - `_id` field도 새로운 문서에 포함시킬 수는 있으나, 이 경우 반드시 기존 문서의 `_id`값과 동일한 값을 넣어야 한다.
    - `update`와의 차이는 `update`는 일부 field의 값만을 변경하는 것이지만, `replaceOne`은 문서 전체를 입력된 문서로 교체한다는 것이다.

  ```bash
  $ db.<collection명>.updateOne(<조건>, <새로운 문서>)
  
  # 예시
  $ db.accounts.replaceOne(
    { account_id: 371138 },
    { account_id: 893421, limit: 5000, products: [ "Investment", "Brokerage" ] }
  )
  ```



- 삭제

  - `deleteOne`
    - 조건에 맞는 document 1개 삭제
    - 조건에 맞는 document가 없더라도 error가 발생하지는 않기에, 원하는 데이터가 정확히 삭제되었는지 확인해야 한다.
  
  ```bash
  $ db.<collection명>.deleteOne(<조건>)
  
  # 예시
  $ db.books.deleteOne({name:"foo"})
  
  # 결과
  # { acknowledged: true, deletedCount: 1 }
  ```
  
  - `deleteMany`
    - 조건에 맞는 document 모두 삭제
  
  ```bash
  $ db.<collection명>.deleteMany(<조건>)
  
  # 예시
  $ db.books.deleteMany({name:"foo"})
  ```
  





# Mongostat

- mongostat

  - 현재 실행중인 mongod 혹은 mongos의 상태를 보여주는 tool이다.
    - MongoDB 4.4부터 MongoDB와 독립적으로 versioning을 한다.
    - MongoDB Database Tools package의 일부로 별도의 설치 없이 사용할 수 있다.
  
  - 아래의 명령어로 실행시킨다.
  
  ```bash
  $ mongostat <options> <connection-string> <polling interval in seconds>
  
  # mongostat -u foo -p bar --authenticationDatabase=admin
  ```

  - Options
    - `-o`: 출력할 field들을 `field=출력할 field명` 형식으로 `,`로 구분하여 입력한다.
    - `-O`: 기본으로 출력되는 field들 외에 `serverStatus` [command](https://www.mongodb.com/docs/manual/reference/command/serverStatus/#serverstatus)에서 확인할 수 있는 field들을 추가하여 볼 수 있다.
  
  - Fields
    - `inserts`: 매 초마다 database에 insert되는 object의 개수.
    - `query`: 매 초마다 실행되는 query의 개수
    - `command`: 매 초마다 실행되는 command의 개수
    - `qrw`: `|`로 구분하여 왼쪽은 data를 읽기 위해 대기하는 queue의 길이, 오른쪽은 data를 쓰기 위해 대기하는 queue의 길이.
    - `arw`: `|`로 구분하여 왼쪽은 data를 읽기를 수행하고 있는 client의 수, 오른쪽은 data 쓰기를 수행하고 있는 client의 수.
    - `netIn`: MongoDB로 들어온 network traffic의 양(bytes)
    - `netOut`: MongoDB에서 나간 network traffic의 양(bytes)
    - `conn`: 열려 있는 connection의 개수





# MongoDB Connection Pool

- Connection Pool이란
  - 사용할 준비가 완료된 open 상태의 database connection들의 cache이며, driver에 의해 관리된다.
    - Driver란 application에서 database에 접근하기 위한 tool로 Python의 PyMongo나 Motor등이 이에 해당한다.
    - 즉, MongoDB instance와 application 사이의 connection들의 집합이다.
  - Application은 connection pool로부터 connection을 받아 DB에 접근하고, 작업이 완료된 후에는 connection을 pool에 반납한다.



- Connection Pool의 장점
  - Application의 지연 시간을 줄여주고, 새로운 connection이 생성되는 횟수를 줄여준다.
  - Application은 connection pool에 connection을 수동으로 반납할 필요 없으며, 자동으로 반납된다.
  - 만약 가용한 connection이 있을 때 application이 connection을 요청할 경우 새로운 connection을 생성하지 않고 connection pool에서 connection을 가져다 쓰면 된다.



- Connection Pool 사용하기
  - 대부분의 driver들은 `MongoClient`라는 object를 제공한다.
    - 하나의 application이 여러개의 MongoDB cluster에 연결되어있는 것이 아니라면, 하나의 application당 하나의 `MongoClient` instance를 사용한다.
    - 대부분의 driver에서 `MongoClient`는 thread-safe하다.
  - Connection Pool 관련 설정들
    - `maxPoolSize`: pool 내에 open될 connection들의 최대 개수를 설정하며, 만일 이 값 이상의 connection을 필요로 할 경우 `waitQueueTimeoutMS`에 설정한 시간만큼 대기한다.
    - `minPoolSize`: pool 내에 open 될 connection들의 최소 개수를 설정한다.
    - `connectionTimeoutMS`: Timeout을 설정한다.





# PyMongo

- pymongo

  > https://pymongo.readthedocs.io/en/stable/

  - mongodb 공식 라이브러리
  - Python에서 mongodb를 보다 쉽게 사용할 수 있게 해주는 라이브러리.
  - 설치

  ```bash
  $ pip install pymongo
  ```



- 사용해보기

  - mongodb에 연결하기 위한 클라이언트를 생성한다.

  ```python
  from pymongo import MongoClient
  
  # 방식1
  client = MongoClient('<mongodb host>', '<mongodb port>')
  
  # 방식2
  client = MongoClient('mongodb://<mongodb host>:<mongodb port>/')
  
  # 인증이 필요할 경우
  client = MongoClient("<mongodb host>:<mongodb port>",username="<username>",password="<password>",authSource="admin")
  ```









