import aioredis
from src.app.config import REDIS_URL, DATABASE_URL

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware, db

from src.app.schema import User as SchemaUser
from src.app.model import User as ModelUser

# from src.app.custom_logging import logging_config


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

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


@app.post('/user/', response_model=SchemaUser)
async def user(user: SchemaUser):
    db_user = ModelUser(
        first_name=user.first_name,
        last_name=user.last_name,
        position=user.position,
        email=user.email)

    db.session.add(db_user)
    db.session.commit()

    return db_user


@app.get('/user/')
async def user():
    user = db.session.query(SchemaUser).all()
    return user


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     app.state.redis = await aioredis.from_url(REDIS_URL)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#     await app.state.redis.close()


# to run locally
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
