from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()
