# import aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#
# from config import REDIS_URL
# from db import database

app = FastAPI()

origins = [
    "http://0.0.0.0:8080",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {'status': 'Working'}


# @app.on_event('startup')
# async def startup():
#     await database.connect()
#     app.state.redis = await aioredis.from_url(REDIS_URL)
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     await database.disconnect()
#     await app.state.redis.close()
