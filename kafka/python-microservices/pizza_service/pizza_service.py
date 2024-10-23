import json
import time

from kafka import KafkaProducer, KafkaConsumer

from pizza import Pizza, PizzaOrder


PRODUCER_TOPIC = "pizza"
CONSUMER_TOPIC = "pizza-with-veggies"
BOOTSTRAP_SERVERS = ["localhost:9097"]

pizza_producer = KafkaProducer(acks=0, 
        compression_type="gzip", 
        bootstrap_servers=BOOTSTRAP_SERVERS,
        key_serializer=lambda x: json.dumps(x).encode("utf-8"),
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

pizza_warmer = {}

def order_pizzas(count):
    order = PizzaOrder(count)
    pizza_warmer[order.id] = order
    for _ in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.send(PRODUCER_TOPIC, key=order.id, value=new_pizza.__dict__)
    pizza_producer.flush()
    return order.id

def get_order(order_id):
    order = pizza_warmer[order_id]
    if order == None:
        return "Order not found, perhaps it's not ready yet."
    else:
        return order.__dict__

def load_orders():
    pizza_consumer = KafkaConsumer(
        CONSUMER_TOPIC,
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
        record = pizza_consumer.poll()
        if record:
            for messages in record.values():
                for message in messages:
                    pizza = message.value
                    add_pizza(pizza["order_id"], pizza)
            continue
        time.sleep(1)

def add_pizza(order_id, pizza):
    if order_id in pizza_warmer.keys():
        order = pizza_warmer[order_id]
        order.add_pizza(pizza)
