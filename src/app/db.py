from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()
