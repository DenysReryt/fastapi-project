import uuid
from src.app.database import metadata
from sqlalchemy import Integer, TIMESTAMP, Column, String, Boolean, text, DateTime, Table
from sqlalchemy.sql import func

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, unique=True, nullable=False),
    Column('password', String, nullable=False),
    Column('verified', Boolean, nullable=False, server_default='False'),
    Column('verification_code', String, nullable=True, unique=True),
    Column('role', String, server_default='user', nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
    Column('updated_at', DateTime(timezone=True), default=func.now(), nullable=False)
)
