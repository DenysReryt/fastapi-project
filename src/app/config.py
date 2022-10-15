import os

#Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://")

#Postgres
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/postgres")
