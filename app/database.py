from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_SCHEMA, DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.schema = DATABASE_SCHEMA


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
