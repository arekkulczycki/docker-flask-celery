from logging import getLogger
from typing import cast, Set

from celery.beat import Scheduler, ScheduleEntry

from common.models.periodic_task import PeriodicTask
from settings import settings

logger = getLogger("app")


class SyncingScheduler(Scheduler):
    """Periodically queries all current periodical tasks and updates beat schedule."""

    _active_task_ids: Set[int] = set()
    max_interval: int = settings.scheduler_interval_seconds
    sync_every: int = settings.scheduler_interval_seconds

    def sync(self):
        """Synchronize beat schedule with database."""

        logger.debug("syncing scheduler...")

        for task in settings.db_session.query(PeriodicTask).all():
            if task.id not in self._active_task_ids:
                self._schedule_entry(task)
                self._active_task_ids.add(task.id)

                logger.info(f"scheduled new periodic task: {task.name} for {task.arg}")

    def _schedule_entry(self, task: PeriodicTask) -> None:
        """
        Change database periodical task into a beat scheduler entry.

        Run the new entry immediately.
        """

        entry = ScheduleEntry(
            name=task.name,
            task=task.name,
            schedule=task.interval_seconds,
            args=(task.arg,),
        )
        cast(dict, self.schedule)[task] = entry
