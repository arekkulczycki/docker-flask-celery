from sqlalchemy import Column, Integer, String, UniqueConstraint

from common.db import BaseModel


class PeriodicTask(BaseModel):
    """
    Database representation of a periodic celery task.

    If `SyncingScheduler` is used then beat will trigger tasks represented by this model.
    """

    __tablename__ = "periodic_task"
    __table_args__ = (
        UniqueConstraint('name', 'arg', name='unique_name_arg'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    interval_seconds = Column(Integer, nullable=False)
    arg = Column(String, nullable=False)
