import os

#Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://")

#Postgres
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db/user_db")
