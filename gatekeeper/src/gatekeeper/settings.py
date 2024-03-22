from typing import ClassVar, Optional

from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy.orm import Session

from common.db import get_session


class Settings(BaseSettings):
    """Settings for the trains controller."""

    _db_session: ClassVar[Optional[Session]] = None

    postgres_host: str = Field(default="postgres")
    postgres_user: str = Field(default="micro-train")
    postgres_password: str = Field(default="micro-train")
    postgres_db: str = Field(default="micro-train")

    @property
    def db_url(self) -> URL:
        return URL.create(
            "postgresql",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            database=self.postgres_db,
        )

    @property
    def db_session(self) -> Session:
        if Settings._db_session is None:
            Settings._db_session = get_session(self.db_url)

        return Settings._db_session

    @db_session.setter
    def db_session(self, session: Session) -> None:
        Settings._db_session = session


settings = Settings()  # pyright: ignore
