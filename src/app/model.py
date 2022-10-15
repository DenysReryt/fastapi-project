from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, create_engine)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    position = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    employee_id = Column(Integer, ForeignKey('employee.id'))

