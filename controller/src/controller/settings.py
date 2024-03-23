from sys import modules

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the trains controller."""

    celery_broker_url: AnyUrl


settings = (
    Settings()  # pyright: ignore
    if "pytest" not in modules
    else Settings.model_construct()
)
