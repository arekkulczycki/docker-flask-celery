from logging import getLogger
from typing import Dict, ClassVar
from typing import List

from celery import Task
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from common.models.periodic_task import PeriodicTask
from settings import settings
from tasks.periodic_task_config import PeriodicTaskConfig
from tasks.train import Train

SPEED_ANNOUNCEMENT: str = "speed_announcement"
STATION_ARRIVAL_ANNOUNCEMENT: str = "station_arrival_announcement"

ANNOUNCEMENT_TASK_CONFIGS: List[PeriodicTaskConfig] = [
    PeriodicTaskConfig(
        SPEED_ANNOUNCEMENT,
        settings.speed_report_interval_seconds,
    ),
    PeriodicTaskConfig(
        STATION_ARRIVAL_ANNOUNCEMENT,
        settings.station_arrival_interval_seconds,
    ),
]
"""All available announcements a train produces."""

logger = getLogger("app")


class TrainTask(Task):
    """Celery task that holds references to all running trains."""

    trains: ClassVar[Dict[str, Train]] = {}

    @classmethod
    def get_train(cls, id_: str) -> Train:
        """Get train by its unique id or raise."""

        try:
            return cls.trains[id_]
        except KeyError:
            logger.error(f"train {id_} not found")
            raise

    @classmethod
    def add_train(cls) -> None:
        """Add a train to the system and register its announcements."""

        train = Train()
        cls.trains[train.id] = train

        try:
            cls._add_periodic_tasks(str(train.id))
        except IntegrityError as e:
            logger.error(f"integrity error adding task: {e}")
        except PendingRollbackError as e:
            logger.error(f"pending rollback error adding task: {e}")

        logger.debug(f"train {train.id} registered")

    @classmethod
    def _add_periodic_tasks(cls, arg: str) -> None:
        """Store new periodic tasks for the beat scheduler to act upon."""

        for name, interval in ANNOUNCEMENT_TASK_CONFIGS:
            settings.db_session.add(
                PeriodicTask(name=name, interval_seconds=interval, arg=arg)
            )
        settings.db_session.commit()
        settings.db_session.close()
