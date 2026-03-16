from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base

from solution.secrets_accessor import BaseSecretsAccessor, get_secrets_accessor

secrets_accessor: BaseSecretsAccessor = get_secrets_accessor()


def _build_db_url() -> str:
    db_user = secrets_accessor.get_secret("DB_USER")
    db_pass = secrets_accessor.get_secret("DB_PASS")
    db_host = secrets_accessor.get_secret("DB_HOST")
    db_port = secrets_accessor.get_secret("DB_PORT")
    db_name = secrets_accessor.get_secret("DB_NAME")
    return f"mysql+aiomysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


SQLALCHEMY_DATABASE_URL = _build_db_url()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
