import aioredis

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.models import engine, metadata, database
from app.config import REDIS_URL

metadata.create_all(engine)

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
def status():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await database.connect()
    app.state.redis = await aioredis.from_url(REDIS_URL)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await app.state.redis.close()


# to check local
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
