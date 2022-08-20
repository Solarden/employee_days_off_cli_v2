from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL


def get_engine():
    database_url: Optional[str] = DATABASE_URL
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment.")
    engine = create_engine(database_url)
    return engine


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session


session = get_session()
