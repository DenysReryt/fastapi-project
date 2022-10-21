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

    REDIS_URL = os.getenv("REDIS_URL")

settings = Settings()
