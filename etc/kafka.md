# Kafka란

- Kafka
  - 링크드인에서 스칼라로 개발한 메시지 프로젝트
  - Kafka라는 이름은 소설가 프란츠 카프카에서 따왔다.
  - Pub-Sub 모델의 메시지 큐
  - 분산 환경에 특화되어 있다는 특징을 가지고 있다.



- Pub/Sub 구조
  - 링크드인에서 기존에 사용하던 Point to Point 구조를 Pub/Sub 구조로 변경하였다.
    - A,B,C,D가 있다고 할 때 A가 누구에게 메시지를 보내야 할지 모르므로 A는 B,C,D와 모두 연결되어 있어야 하며, 이는 B, C, D도 마찬가지다.
    - Pub/Sub 구조는 A,B,C,D가 모두 연결되어 있는 것이 아니라 발신자, 수신자가 지정되어 있고 발신자는 카프카에만 요청을 보내고, 수신자는 카프카에게서만 메시지를 받는 구조이다(단방향 구조).
    - 따라서 발신자와 수신자 모두 Kafka와만 연결되어 있으면 된다.
  - Publish(Producer)
    - 발신을 하는 역할을 하는 사람은 카프카에게 전송만 하게 되고, 수신자가 누구인지 알 필요가 없다.
    - 따라서 특별히 수신자를 정해놓지 않고 서버에 전송하게 되는 심플한 구조를 갖게 된다.
    - 카프카는 내부에 발신자의 메시지를 토픽이라는 주소로 저장하게 된다.
  - Subscribe(Consumer)
    - 수신자는 카프카에 원하는 토픽을 구독한다.
    - 즉, 수신자 역시 발신자가 누구인지 관심은 없고 필요한 메시지만 구독을 하게 되는 것이다.



- 구성 요소
  - Event
    - Producer와 Consumer가 데이터를 주고 받는 단위
    - 메시지라고도 부른다.
  - Topic
    - 이벤트가 쓰이는 곳.
    - Producer는 Topic에 이벤트를 게시한다.
    - Consumer는 Topic으로부터 이벤트를 가져와서 처리한다.
    - Topic은 파일 시스템의 디렉터리와 유사하며, 이벤트는 디렉터리 안의 파일과 유사하다.
  - Broker
    - 카프카 서버
    - Producer에게 메시지를 받아서, Consumer에게 전달해주는 역할을 한다.
    - Topic이 저장되어 있는 곳이다.
    - Elasticsearch의 node와 유사하다.
  - Producer
    - Kafka 이벤트를 게시(post)하는 클라이언트 어플리케이션
  - Consumer
    - Topic을 구동하고 이로부터 얻어낸 이벤트를 처리하는 클라이언트 어플리케이션
  - Partition
    - Topic은 여러 Broker에 분산되어 저장되며 이렇게 분산된 Topic을 Partition이라고 한다.
    - 어떤 이벤트가 Partition에 저장될지는 이벤트의 key에 의해 정해지며, 같은 키를 가지는 이벤트는 항상 같은 Partition에 저장된다.
    - Topic의 Partition에 지정된 Consumer가 항상 정확히 동일한 순서로 Partition의 이벤트를 읽을 것을 보장한다.
  - Zookeeper
    - Broker에 분산 처리된 메시지 큐의 정보들을 관리한다.
    - Kafka는 Zookeeper 없이는 실행되지 않는다.



- 카프카를 비롯한 대부분의 분산 시스템의 장점
  - 높은 확장성
    - 카프카의 단일 브로커(노드)로는 처리가 힘들 경우 브로커를 늘리기만 하면 된다.
    - 또한 브로커를 추가하는 것이 매우 쉽다.
  - 안정성
    - 동일한 역할을 수행하는 브로커들 중 일부 브로커의 장애 발생시 나머지 브로커들이 장애 발생 노드 분까지 처리를 맡게 된다.
    - 이르 통해 안정적인 서비스 운영이 가능하다.



# 주요 개념

- Producer와 Consumer의 분리
  - Producer와 Consumer는 완전 별개로 동작한다.
    - Producer는  Broker의 Topic에 메시지를 게시하기만 하면 되며, Consumer는 Broker의 특정 Topic에서 메시지를 가져와서 처리만 하면 된다.
  - 이를 통해 Kafka는 높은 확장성을 지니게 된다.
    - 즉, Producer와 Consumer를 필요에 의해 스케일 인 아웃하기에 용이한 구조이다.
    - 만약 Producer와 Consumer가 별개로 동작하지 않는다면 확장 또는 축소시 이들을 모두 연결하거나 연결해제 해줘야 했을 것이다.



- Push 모델과  Pull 모델
  - Kafka의 Consumer는 Pull 모델을 기반으로 메시지 처리를 진행한다.
    - 즉, Broker가 Consumer에게 메시지를 전달하는 것이 아닌, Consumer가 필요할 때 Broker로 부터 메시지를 가져와 처리하는 형태이다.
  - 만일 Push 모델이라면(즉, Broker가 Consumer에게 메시지를 전달한다면) Consumer를 관리하기 어렵지만, Pull 모델은 Consumer가 처리 가능한 때에 메시지를 가져와 처리하기 때문에 Consumer를 관리하기 쉽다.
  - 또한 Push 모델일 경우에는, 여러 메시지를 한 번에 처리하도록 하기 위해 전송을 지연시킬 수 있다. 따라서, 메시지를 처리할 수 있는 Consumer가 있어도 메시지를 받을 때 까지 대기해야 한다.
  - 반면에 Pull 모델은 Consumer가 마지막으로 처리된 메시지 이후의 메시지를 처리 가능할 때 모두 가져오기 때문에 불필요한 지연이 발생하지 않는다.



- 소비된 메시지 축적(Commit과 Offset)

  - 메세지는 지정된 Topic에 전달된다.
    - Topic은 다시 여러 Partition으로 나뉠 수 있다.
    - 각 Partition에 저장된 메시지를 log라고 부른다.
    - 메시지는 partition에 순차적으로 추가되며, 이 메시지의 상대적인 위치를 offset이라 한다. 

  - Commit과 Offset

    - Consumer의 `poll()`은 이전에 commit한 offset이 존재하면, 해당 offset 이후의 메시지를 읽어온다.
    - 또 읽어온 뒤, 마지막 offset을 commit한다.
    - 이어서 `poll()`이 실행되면 방금전 commit한 offset 이후의 메시지를 읽어와 처리하게 된다.

  - 메시지 소비 중에는 다음과 같은 문제들이 발생할 수도 있다.

    - Broker가 메시지를 네트워크를 통해 Consumer에게 전달할 때 마다, 전달 즉시 메시지를 소비 된 메시지로 기록하면, Consumser가 메세지 처리를 실패할 경우 해당 메시지는 처리되지 못하고 소비 된 상태로 남게 된다.
    - 따라서, Broker는 메시지가 소비되었음을 기록하기 위해서, Consumer의 승인을 기다린다.
    - 그러나 이러한 방식은 다시 아래와 같은 문제를 발생시키게 된다.

    - Consumer가 메시지를 성공적으로 처리한 뒤 Broker에 승인을 보내기 전에 Broker가 실패하였다고 판단하고 다시 메시지를 보낼 경우, Consumer는 동일한 메시지를 두 번 처리하게 된다.
    - 따라서 Consumer는 멱등성을 고려해야 한다.
    - 즉 같은 메시지를 특수한 상황에 의해 여러 번 받아서 여러 번 처리하더라도, 한 번 처리한 것과 같은 결과를 가지도록 설계해야 한다. 

  - 메시지 전달 컨셉

    - At most once(최대 한 번): 메시지가 손실 될 수 있지만, 재전달은 하지 않는다.
    - At least once(최소 한 번): 메시지가 손실 되지 않지만, 재전달이 일어난다.
    - Exactly once(정확히 한 번): 메시지는 단 한 번만 전달 된다.



- Consumer Group

  - Consumer Group은 하나의 Topic을 구독하는 여러  Consumer들의 모음이다.
    - Topic을 구독하는 Consumer들을 Group화 하는 이유는, 가용성 때문이다.
    - 하나의 Topic을 처리하는 Consumer가 1개인 것 보다 여러개라면 당연히 가용성은 증가할 것이다.
    - Consumer Group의 각 Consumer들은 하나의 Topic의 각기 다른 Partition의 내용만을 처리할 수 있는데, 이를 통해 Kafka는 메시지 처리 순서를 보장한다.
    - 따라서 특정 Partition을 처리하던 Consumer가 처리 불가 상태가 된다면, 해당 Partition의 메시지를 처리할 수 없는 상태가 되어버린다.

  - Rebalance
    - 특정 Partition을 처리하던 Consumer가 처리 불가 상태가 될 경우, Partition과 Consumer를 재조정하여, 남은 Consumer Group 내의 Consumer들이 Partition을 적절하게 나누어 처리하게 된다.
    - 또한 Consumer Group 내에서 Consumer들 간에 Offset 정보를 공유하고 있기 때문에, 특정 Consumer가 처리불가 상태가 되었을 때, 해당 Consumer가 처리한 마지막 Offset 이후 부터 처리를 이어서 할 수 있다.
    - 이처럼 Partition을 나머지 Consumer들이 다시 나누어 처리하는 것을 Rebalance라고 한다.
  - Consumer Group과 Partition
    - 무조건 Consumer Group 내의 Consumer들은 모두 각기 다른 Partition에 연결되어야 한다.
    - 이를 통해 Consumer의 메시지 처리 순서를 보장하게 된다.
  - Consumer 확장
    - Consumer의 성능이 부족해, 이를  확장할 때, Consumer의 수가 Partition보다 많다면 Partition의 개수도 늘려줘야 한다.
    -  각 Consumer는 동일한 Partition을 처리할 수 없기 때문에 Consumer의 수가 Partition보다 많다면 Partitiom과 연결되지 않은 Consumer가 아무 처리도 하지 않는 상황이 발생할 수 있기 때문이다.



- Leader와 Follower
  - ES의 primary와 replica와 유사하다.
  - Topic을 복제해서 Follower에 저장한다.
  - 메시지를 생성하고 소비하는 작업은 모두 leader가 처리하고, follower들은 복제해서 가지고 있기만 한다.



# 사용하기

## Docker로 설치하기

- 이미지 받기

  - kafka 이미지 받기

  ```bash
  $ docker pull wurstmeister/kafka
  ```

  - zookeeper 이미지 받기

  ```bash
  $ docker pull zookeeper
  ```



- docker-compose.yml 작성

  ```yaml
  version: '3'
  
  services:
    zookeeper:
      container_name: zookeeper
      image: wurstmeister/zookeeper
      ports:
        - "2181:2181"
  
    kafka:
      image: wurstmeister/kafka
      ports:
        - "9092:9092"
      environment:
        KAFKA_ADVERTISED_HOST_NAME: localhost
        KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
  ```



- Topic 생성하기

  ```bash
  $ docker exec -t <컨테이너 명> kafka-topics.sh --bootstrap-server <host 명>:9092 --create --topic <토픽 이름>
  ```



## Python에서 사용하기

- Python에서 Kafka에 접근할 수 있게 해주는 라이브러리에는 아래와 같은 것들이 있다.
  - confluent-kafka-python
    - 성능이 가장 좋다.
    - C로 만든 라이브러리를 호출하여 사용하는 방식이므로 별도의 설치과정이 존재한다.
  - kafka-python
    - pure python이기에 confluent-kafka-python에 비해 속도는 느리다.
    - 사용법이 직관적이고 간결하다.



- 설치하기(kafka-python)

  ```bash
  $ pip install kafka-python
  ```



- Producer 구현

  ```python
  from kafka import KafkaProducer
  from json import dumps
  import time
  
  
  producer = KafkaProducer(acks=0,compression_type='gzip',bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  
  ```





# 참고

- https://galid1.tistory.com/793

- https://needjarvis.tistory.com/category/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B0%8F%20DB/%EC%B9%B4%ED%94%84%EC%B9%B4%28Kafka%29

