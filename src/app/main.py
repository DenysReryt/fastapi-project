import aioredis
from app.config import REDIS_URL, DATABASE_URL

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.schema import User as SchemaUser
from app.model import User as ModelUser

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

def make_logger(rotation_size, level):
    logger.remove()
    pid = os.getpid()
    dt = datetime.datetime.now()
    logger.add(
        f'data/logs/fastapi-{dt}-{pid}.log',
        rotation=rotation_size,
        enqueue=True,
        backtrace=True,
        level=level,
        format="{time} %s {level} {message}" % pid,
    )
    return logger.bind()

@app.get('/')
def status():
    return {"status": "Working"}

@app.post('/user/', response_model=SchemaUser)
async def user(user: SchemaUser):
    db_user = ModelUser(
        first_name = user.first_name,
        last_name = user.last_name,
        position = user.position,
        email = user.email)

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

