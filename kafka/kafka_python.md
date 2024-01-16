## Python에서 사용하기

- Python에서 Kafka에 접근할 수 있게 해주는 라이브러리에는 아래와 같은 것들이 있다.
  - confluent-kafka
    - 성능이 가장 좋다.
    - Kafka를 관리하고 있는 Confluent사에서 개발했다.
  - kafka-python
    - Pure python이기에 confluent-kafka-python에 비해 속도는 느리다.
    - 사용법이 직관적이고 간결하다.
  - aiokafka
    - Benchmark 상으로 성능이 가장 좋다.
    - kafka-python 기반으로 만들어졌다.



- 설치하기(kafka-python)

  ```bash
  $ pip install kafka-python
  ```



- Producer 구현

  ```python
  from kafka import KafkaProducer
  from json import dumps
  import time
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  
  data = {'Hello':'World!'}
  producer.send('test',value=data)
  producer.flush()
  ```

  - Producer 옵션

    > 상세는 https://kafka-python.readthedocs.io/en/1.1.0/apidoc/KafkaProducer.html#kafkaproducer 참고

    - `bootstrap_servers`: 브로커들을 리스트 형태로 입력한다.
    - `acks`: 메시지를 보낸 후 요청 완료 전 승인 수, 손실과 성능의 트레이드 오프로, 낮을수록 성능은 좋고 손실이 커진다.
    - `buffer_memory`: 카프카에 데이터를 보내기전 잠시 대기할 수 있는 메모리(byte)
    - `compression_type`: 데이터를 압축해서 보낼 수 있다(None, gzip, snappy, lz4 중 선택).
    - `retries`: 오류로 전송 실패한 데이터를 다시 보낼지 여부
    - `batch_size`: 여러 데이터를 배치로 보내는 것을 시도한다.
    - `linger_ms`: 배치 형태 작업을 위해 기다리는 시간 조정, 배치 사이즈에 도달하면 옵션과 관계 없이 전송, 배치 사이즈에 도달하지 않아도 제한 시간 도달 시 메시지 전송
    - `max_request_size`: 한 번에 보낼 수 있는 메시지 바이트 사이즈(기본 값은 1MB, 1048576 Bytes)

  - Partitioner

    - kafka-python과, kafka-python 기반의 aiokafka 패키지의 기본 partitioner는 round-robin, sticky partitioner가 아닌 random이다.
    - key가 있을 경우 kafka의 murmur2를 python으로 포팅하여 사용한다.

  ```python
  @classmethod
  def __call__(cls, key, all_partitions, available):
      """
      Get the partition corresponding to key
      :param key: partitioning key
      :param all_partitions: list of all partitions sorted by partition ID
      :param available: list of available partitions in no particular order
      :return: one of the values from all_partitions or available
      """
      if key is None:
          if available:
              return random.choice(available)
          return random.choice(all_partitions)
  
      idx = murmur2(key)
      idx &= 0x7fffffff
      idx %= len(all_partitions)
      return all_partitions[idx]
  ```



- Consumer 구현

  ```python
  from kafka import KafkaConsumer
  from json import loads
  
  
  consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', 
                          enable_auto_commit=True, group_id="my-group", value_deserializer=lambda x: loads(x.decode('utf-8')),
                          consumer_timeout_ms=1000)
  
  for message in consumer:
      print(message.topic)		# test
      print(message.partition)	# 0
      print(message.offset)		# 0
      print(message.key)			# None
      print(message.value)		# {'Hello': 'World!'}
  ```

  - Consumer 옵션
    - `bootstrap_servers`: 브로커들을 리스트 형태로 입력한다.
    - `auto_offset_reset`: earliest(가장 초기 오프셋값), latest(가장 마지막 오프셋값), none(이전 오프셋값을 찾지 못할 경우 에러) 중 하나를 입력한다.
    - `enable_auto_commit`: 주기적으로 offset을 auto commit
    - `group_id`: 컨슈머 그룹을 식별하기 위한 용도
    - `value_deserializer`: producer에서 value를 serializer를 한 경우 사용.
    - `consumer_timeout_ms`: 이 설정을 넣지 않으면 데이터가 없어도 오랜기간 connection한 상태가 된다. 데이터가 없을 때 빠르게 종료시키려면 timeout 설정을 넣는다.



- Kafka Consumer Multiprocessing

  - Broker에서 이벤트를 받아와서 각 프로세스들이 처리하게 하는 방법
    - `multiprocessing`의 `Process`와 `Queue`를 사용한다.

  - main.py
    - 이벤트를 처리하고자 하는 프로세스+1개의 프로세스를 생성한다.
    - 하나의 프로세스는 `Queue`에 지속적으로 이벤트를 추가한다.
    - 나머지 프로세스는 `Queue`를 공유하면서 이벤트를 받아와서 처리한다.

  ```python
  from multiprocessing import Process, Queue
  import consumer
  from kafka import KafkaConsumer
  import json
  
  
  def deserializer_value(value):
      try:
          return json.loads(value)
      except Exception as e:
          print(e)
  
  
  kconsumer = KafkaConsumer('test',
                          bootstrap_servers='127.0.0.1:9092',
                          group_id='test-group',
                          value_deserializer=deserializer_value,
                          auto_offset_reset='earliest',
                          max_poll_records=1,
                          max_poll_interval_ms=3600000,
                          enable_auto_commit=True)
  
  
  if __name__ == '__main__':
      queue = Queue()
      processes=[]
      def put_items(queue):
          # queue에 이벤트를 추가한다.
          for msg in kconsumer:
              queue.put(msg)
      
      for i in range(4):
          if i == 0:
              # Queue에 이벤트를 추가할 프로세스
              processes.append(Process(target=put_items, args=[queue]))	# queue를 인자로 넘긴다.
          else:
              # 실제 이벤트를 처리할 프로세스들
              processes.append(Process(target=consumer.consume_message, args=[queue]))  # queue를 인자로 넘긴다.
      
      for process in processes:
          process.start()
      for process in processes:
          process.join()
  ```

  - consumer.py

  ```python
  import os
  
  def consume_message(queue):
      while True:
          # 이벤트를 받아와서
          msg = queue.get()
         	# PID 확인
          print('PID:', os.getpid())
          # 필요한 처리를 수행한다.
          print(msg.value.get('message'))
          print("-"*50)
  ```

  - producer.py

  ```python
  import json
  from kafka import KafkaProducer
  
  
  producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                          max_block_ms=1000 * 60 * 10,
                          buffer_memory=104857600 * 2,
                          max_request_size=104857600)
  
  msg_list = ['Hello', 'World', 'Good', 'Morning']
  for msg in msg_list:
      value = {
          'message':msg
      }
      producer.send(topic='test', value=value)
      producer.flush()
  ```



- Kafka Consumer에 topic과 partition을 지정하는 방법

  - partition을 2개 이상 생성해줘야 한다.
    - 만일 docker-compose로 kafka를 띄운다면 `environment`의 `KAFKA_CREATE_TOPICS`에 `토픽명:partition 개수:replica 개수` 형태로 파티션 개수를 설정해준다.
    - 만일 kafka를 띄울 때 partition 생성을 하지 않았다면 아래와 같이 파티션을 생성해준다.

  ```python
  from kafka import KafkaAdminClient
  from kafka.admin import NewPartitions
  
  bootstrap_servers='127.0.0.1:9092'
  topic = 'test'
  
  # {topic명:NewPartition 인스턴스} 형태의 딕셔너리를 생셩한다.
  topic_partitions = {}
  topic_partitions[topic] = NewPartitions(total_count=3)
  
  admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
  # create_partitions 메서드에 위에서 생성한 딕셔너리를 인자로 넘겨 파티션을 생성한다.
  admin_client.create_partitions(topic_partitions)
  ```

  - producer
    - producer 쪽에서는 특별히 해줄 것이 없다.
    - 만일 특정 partition에 메시지를 보내고 싶다면 `send` 메서드에 `partition=파티션 번호` 인자를 추가해주면 된다.

  ```python
  import json
  from kafka import KafkaProducer
  
  
  producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                          value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                          max_block_ms=1000 * 60 * 10,
                          buffer_memory=104857600 * 2,
                          max_request_size=104857600)
  
  msg_list = ['Hello', 'World', 'Good']
  topic = 'test'
  for msg in msg_list:
      value = {
          'message':msg
      }
      producer.send(topic=topic, value=value)
      producer.flush()
  ```

  - consumer
    - `assign` 메서드를 통해 토픽과 파티션을 할당한다.

  ```python
  import json
  
  from kafka import KafkaAdminClient, KafkaConsumer
  from kafka.structs import TopicPartition
  from kafka.admin import NewPartitions
  
  
  
  def deserializer_value(value):
      try:
          return json.loads(value)
      except Exception as e:
          print(e)
  
  bootstrap_servers='127.0.0.1:9092',
  topic = 'test'
  
  # enable_auto_commit(default True) 값을 아래와 같이 False로 주면, 수동으로 커밋을 해줘야 한다.
  consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                          group_id='test-group', 
                          value_deserializer=deserializer_value, 
                          auto_offset_reset='earliest', 
                          enable_auto_commit=False)
  # topic과 partition을 할당
  consumer.assign([TopicPartition(topic, 1)])
  
  for msg in consumer:
      print(msg.value.get('message'))
      partitions = consumer.assignment()
      print(partitions)
      # enable_auto_commit을 False로 줬기에 아래와 같이 수동으로 commit을 해준다.
      consumer.commit()
  ```



- Kafka python topic 생성하기

  ```python
  from kafka import KafkaAdminClient
  from kafka.admin import NewTopic
  
  
  kafka_admin_client = KafkaAdminClient(bootstrap_servers="127.0.0.1:9092")
  topic = NewTopic("my-topic", 3, 1)
  kafka_admin_client.create_topics([topic])
  ```



- future

  - 모종의 이유로 producer에서 partition으로 message를 전송하지 못하더라도 error가 발생하지는 않는다.
    - message의 누락은 발생하는데, error는 발생하지 않으므로 누락이 생겨도 모를 수가 있다.
    - 따라서 누락이 생겼을 경우 이를 캐치해서 예외처리를 해 줄 필요가 있다.
  - Future는 `KafKaProducer.send` 메서드의 결과 반환되는 값으로 message의 적재가 성공했는지, 실패했는지 알 수 있다.
    - `Future.succeeded`, `Future.failed`를 통해 성공했는지 실패했는지를 알 수 있다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  
  time.sleep(0.1)
  print(future.succeeded())	# True
  print(future.failed())		# False
  
  producer.flush()
  ```

  - 주의할 점은 적재가 완료될 때까지는 성공/실패 여부를 알 수 없다.
    - 위 예시에서 `time.sleep`을 통해 잠시 멈춘 것은 적재가 완료되기를 기다리기 위해서다.
    - 아래는 `Future.succeeded`, `Future.failed` 메서드의 실제 코드로, `self.is_done`이 True여야, 즉 적재가 완료 되어야 True를 반환한다.

  ```python
  class Future(object):
      # (...)
      def succeeded(self):
          return self.is_done and not bool(self.exception)
  
      def failed(self):
          return self.is_done and bool(self.exception)
  ```

  - `FutureRecordMetadata.get` 메서드는 성공시 message의 상세 정보를 반환하다.
    - `FutureRecordMetadata.get` 메서드의 경우, `timeout`으로 설정한 시간 동안 적재가 완료될 때까지 기다리기 때문에,  `time.sleep`을 주지 않아도 된다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localgost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  try:
  	print(future.get(timeout=10))
  except Exception as e:
      print(e)
  print(future.succeeded())		# True
  print(future.failed())			# False
  
  producer.flush()
  ```

  - `FutureRecordMetadata.get`를 실행했을 때, 적재가 실패한 경우에는 exception을 raise한다.
    - `max_request_size`를 1로 줬으므로 적재에 실패하게 되고, exception을 raise한다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localgost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'), \
                          max_request_size=1)
  
  topic = "foo"
  
  future = producer.send(topic,value={"foo":"bar"})
  try:
  	print(future.get(timeout=10))
  except Exception as e:
      print(e)
  print(future.succeeded())		# False
  print(future.failed())			# True
  
  producer.flush()
  ```

  - 아래와 같이 callback 형식으로도 사용이 가능하다.

  ```python
  import time
  
  from kafka import KafkaProducer
  from json import dumps
  
  
  def on_send_success(record_metadata):
      print(record_metadata.topic)
      print(record_metadata.partition)
      print(record_metadata.offset)
  
  def on_send_error(excp):
      print(excp)
      # handle exception
  
  producer = KafkaProducer(acks=0, compression_type="gzip", bootstrap_servers=['localhost:9092'], \
                          value_serializer=lambda x: dumps(x).encode('utf-8'))
  
  topic = "foo"
  
  producer.send(topic,value={"foo":"bar"}).add_callback(on_send_success).add_errback(on_send_error)
  producer.flush()
  ```



