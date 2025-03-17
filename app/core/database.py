from contextlib import contextmanager
from typing import Generator, ContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings

engine = create_engine(
    settings.DB_URI,
    pool_size=20,
    pool_recycle=3600,
    max_overflow=0,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


@contextmanager
def session_scope() -> ContextManager[Session]:
    """Provide a transactional scope around a series of operations."""
    session = Session(autocommit=False, autoflush=False, bind=engine)
    try:
        yield session
        session.commit()
    except Exception as _:
        session.rollback()
        raise
    finally:
        session.close()
