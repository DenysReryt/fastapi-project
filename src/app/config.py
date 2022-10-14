# Redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://")


# Postgres
POSTGRES_URL = os.getenv("DATABASE_URL", 'sqlite://')
