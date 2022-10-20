#Redis

import os
REDIS_URL = os.getenv("REDIS_URL", "redis://")

# Postgres
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_PORT: int = 5432
    DB_PASSWORD: str = 'password'
    DB_USER: str = 'postgres'
    DB_NAME: str = 'postgres'
    DB_HOST: str = 'db'
    DB_HOSTNAME: str = '127.0.0.1'

    CLIENT_ORIGIN: str = 'http://localhost:3000'

    class Config:
        env_file = './.env'


settings = Settings()


