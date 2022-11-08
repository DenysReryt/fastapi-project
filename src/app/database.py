import databases
import aioredis
from starlette.requests import Request
from sqlalchemy import create_engine, MetaData

from src.app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

def get_redis(request: Request) -> aioredis.Redis:
    return request.app.state.redis
