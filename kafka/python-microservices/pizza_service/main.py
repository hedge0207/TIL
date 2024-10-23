from contextlib import asynccontextmanager
from threading import Thread
import json

from fastapi import FastAPI
import uvicorn

import pizza_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    t = Thread(target=pizza_service.load_orders)
    t.start()
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/order/{count}')
def order_pizzas(count):
    order_id = pizza_service.order_pizzas(int(count))
    return json.dumps({"order_id": order_id})


@app.get('/order/{order_id}')
def get_order(order_id):
    return pizza_service.get_order(order_id)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8094)