from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.sql import func
from src.app.db import Base, engine

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
