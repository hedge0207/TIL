from abc import ABC, abstractmethod
import time
import json

from kafka import KafkaProducer, KafkaConsumer


class BaseService(ABC):
    _BOOTSTRAP_SERVERS = ["localhost:9097"]
    _topping_type = None

    def __init__(self, consumer_topic, producer_topic):
        self._producer_topic = producer_topic
        self._producer = KafkaProducer(acks=0, 
            compression_type="gzip", 
            bootstrap_servers=self._BOOTSTRAP_SERVERS,
            key_serializer=lambda x: json.dumps(x).encode("utf-8"),
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        self._consumer = KafkaConsumer(
            consumer_topic,
            bootstrap_servers=self._BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            consumer_timeout_ms=10_000,
            enable_auto_commit=False,
            group_id="meats",
            max_poll_records=500,
            key_deserializer=lambda x: json.loads(x) if x else x,
            value_deserializer=lambda x: json.loads(x) if x else x
        )
    
    def _add_topping(self, order_id, pizza):
        pizza[self._topping_type] = self._calc_topping()
        self._producer.send(self._producer_topic, key=order_id, value=pizza)
        self._producer.flush()
    
    @abstractmethod
    def _calc_topping(self):
        ...
    
    def start_service(self):
        while True:
            record = self._consumer.poll()
            if not record:
                continue

            for messages in record.values():
                for message in messages:
                    pizza = message.value
                    self._add_topping(message.key, pizza)

            time.sleep(1)
    
    
