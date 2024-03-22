from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from common.db import BaseModel


class PeriodicTask(BaseModel):
    """
    Database representation of a periodic celery task.

    If `SyncingScheduler` is used then beat will trigger tasks represented by this
    model.
    """

    __tablename__ = "periodic_task"
    __table_args__ = (UniqueConstraint("name", "arg", name="unique_name_arg"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    interval_seconds: Mapped[int] = mapped_column(nullable=False)
    arg: Mapped[str] = mapped_column(nullable=False)
