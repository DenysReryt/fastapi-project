import uuid
from src.app.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func



class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default='False')
    verification_code = Column(String, nullable=True, unique=True)
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
