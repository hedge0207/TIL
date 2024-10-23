import time
import json

from kafka import KafkaConsumer


BOOTSTRAP_SERVERS = ["localhost:9097"]
TOPIC = "pizza-with-meats"

meats = {}
def start_consumer():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        consumer_timeout_ms=10_000,
        enable_auto_commit=False,
        group_id="pizza_shop",
        max_poll_records=500,
        key_deserializer=lambda x: json.loads(x) if x else x,
        value_deserializer=lambda x: json.loads(x) if x else x
    )
    
    while True:
        record = consumer.poll()
        if record:
            for messages in record.values():
                for message in messages:
                    pizza = message.value
                    add_meat_count(pizza["meats"])
            continue
        time.sleep(1)
            
            
def add_meat_count(meat):
    if meat in meats:
        meats[meat] = meats[meat] + 1
    else:
        meats[meat] = 1

def generate_report():
    return meats   

