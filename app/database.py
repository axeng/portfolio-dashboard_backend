from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic.tools import lru_cache

from app import config


@lru_cache()
def get_postgres_settings():
    return config.Settings().postgres


SQLALCHEMY_DATABASE_URL = get_postgres_settings().get_postgres_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()