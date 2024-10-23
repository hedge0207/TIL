from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI
import uvicorn

import report_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    t = Thread(target=report_service.start_consumer)
    t.start()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/report')
def generate_report():
    return report_service.generate_report()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8089)