from sys import modules
from typing import ClassVar, Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy.orm import Session

from common.db import get_session


class Settings(BaseSettings):
    """Settings for the running trains and their announcement frequency."""

    _db_session: ClassVar[Optional[Session]] = None

    celery_broker_url: AnyUrl

    postgres_host: str = Field(default="postgres")
    postgres_user: str = Field(default="micro-train")
    postgres_password: str = Field(default="micro-train")
    postgres_db: str = Field(default="micro-train")

    number_of_trains: int = Field(default=1)
    speed_report_interval_seconds: float = Field(default=10)
    station_arrival_interval_seconds: float = Field(default=180)

    scheduler_interval_seconds: int = Field(default=15)

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


settings = (
    Settings()  # pyright: ignore
    if "pytest" not in modules
    else Settings.model_construct()
)
