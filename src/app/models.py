from src.app.database import metadata
from sqlalchemy import Integer, TIMESTAMP, Column, String, Boolean, text, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

user_companies = Table(
    'user_companies',
    metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='cascade'), primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='cascade'), primary_key=True)
)

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


companies = Table(
    'companies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('visibility', Boolean, nullable=False, server_default='True'),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('owner_id', Integer, ForeignKey('users.id', ondelete='cascade'), nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False, default=func.now()),
)
