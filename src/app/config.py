# Postgres
import os
from pydantic import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('../..') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DB_PORT: int = os.getenv('DB_PORT')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_USER: str = os.getenv('DB_USER')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_HOSTNAME: str = os.getenv('DB_HOSTNAME')

    CLIENT_ORIGIN: str = os.getenv('CLIENT_ORIGIN')

    REDIS_URL: str = os.getenv("REDIS_URL")

    DOMAIN: str = os.getenv('DOMAIN')
    API_AUDIENCE: str = os.getenv("API_AUDIENCE")
    SECRET: str = os.getenv("SECRET")
    ALGORITHMS: str = os.getenv("ALGORITHMS")
    MY_ALGORITHMS: str = os.getenv("MY_ALGORITHMS")
    ISSUER: str = os.getenv("ISSUER")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    CONNECTION: str = os.getenv("CONNECTION")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

settings = Settings()
