from src.app.database import metadata
from sqlalchemy import Integer, TIMESTAMP, Column, String, Boolean, text, DateTime, Table, ForeignKey, Float, ARRAY
from sqlalchemy.sql import func

users_of_company = Table(
    'users_of_company',
    metadata,
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('is_admin', Boolean, nullable=False, server_default='False')
)

invitations_from_company = Table(
    'invitations_from_company',
    metadata,
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('status', String, server_default='on review')
)

invitations_from_users = Table(
    'invitations_from_users',
    metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE')),
    Column('status', String, server_default='on review')
)

user_companies = Table(
    'user_companies',
    metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE')),
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
    Column('owner_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False, default=func.now()),
)

# Quizzes

quizzes = Table(
    'quizzes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE')),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('frequency', Integer, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True), nullable=False, default=func.now()),
)

questions = Table(
    'questions',
    metadata,
    Column('question_id', Integer, primary_key=True),
    Column('quiz_id', Integer, ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False),
    Column('question', String, nullable=False),
    Column('answers', ARRAY(String), nullable=False),
)

answers = Table(
    'answers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.question_id', ondelete='CASCADE'), nullable=False),
    Column('answer', String, nullable=False),
)

result_quiz = Table(
    'result_quiz',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('company', Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False),
    Column('quiz', Integer, ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False),
    Column('score', String, nullable=False),
    Column('result', Float, nullable=False),
    Column('time', DateTime, nullable=False)
)

rating = Table(
    'rating',
    metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('rating', Float, nullable=False)
)
