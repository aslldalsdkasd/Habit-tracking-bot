import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    os.getenv('DATABASE_URL_CELERY'),
    pool_size=5,
    pool_timeout=30,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(bind=engine)
