#Redis
import os
REDIS_URL = os.getenv("REDIS_URL", "redis://")

# Postgres
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_PORT: int = os.getenv('DB_PORT')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_USER: str = os.getenv('DB_USER')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_HOSTNAME: str = os.getenv('DB_HOSTNAME')

    CLIENT_ORIGIN: str = 'http://localhost:3000'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='.env')
