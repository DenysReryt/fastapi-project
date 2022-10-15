from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

from databases import Database

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()
user = Table(
    "User",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(50)),
    Column("password", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# конструктор запитів бази даних
database = Database(DATABASE_URL)
