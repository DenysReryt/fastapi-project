# Postgres
import os

from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite://')

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# конструктор запитів бази даних
database = Database(DATABASE_URL)
