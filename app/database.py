from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import CreateSchema

from app.config import DATABASE_SCHEMA, DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
Base.metadata.schema = DATABASE_SCHEMA or None


def create_tables() -> None:
    """Create the database schema and all registered tables if they do not exist."""

    with engine.begin() as connection:
        if connection.dialect.name == "postgresql" and DATABASE_SCHEMA:
            connection.execute(
                CreateSchema(
                    DATABASE_SCHEMA,
                    if_not_exists=True,
                )
            )

        Base.metadata.create_all(bind=connection)


def get_db():
    """Provide a database session and close it after the request."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
