from logging import getLogger
from typing import List, cast

from celery.beat import Scheduler, ScheduleEntry

from common.models.periodic_task import PeriodicTask
from settings import settings

logger = getLogger("app")


class SyncingScheduler(Scheduler):
    """Periodically queries all current periodical tasks and updates beat schedule."""

    max_interval = settings.scheduler_interval_seconds
    sync_every = settings.scheduler_interval_seconds

    def sync(self):
        """Synchronize beat schedule with database."""

        logger.debug("syncing scheduler...")

        periodic_tasks: List[PeriodicTask] = cast(List[PeriodicTask], settings.db_session.query(PeriodicTask).all())

        for task in periodic_tasks:
            if task not in self.schedule:
                self._schedule_entry(task)

                logger.info(
                    f"scheduled new periodic task: {task.name} for {task.arg}"
                )

    def _schedule_entry(self, task: PeriodicTask) -> None:
        """Change database periodical task into a beat scheduler entry. Run the new entry immediately."""

        entry = ScheduleEntry(
            name=task.name, task=task.name, schedule=task.interval_seconds, args=(task.arg,),
        )
        self.schedule[task] = entry
        self.apply_entry(entry, producer=self.producer)
