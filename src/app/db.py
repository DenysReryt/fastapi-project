from databases import Database
from sqlalchemy import create_engine, MetaData, Column, DateTime, Integer, String, Table
from config import POSTGRES_URL

# SQLAlchemy
engine = create_engine(POSTGRES_URL)
metadata = MetaData()

# конструктор запитів бази даних
database = Database(POSTGRES_URL)
