from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


def get_session(db_url: URL) -> Session:
    engine = create_engine(db_url)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseModel.metadata.create_all(engine)

    return session_factory()
