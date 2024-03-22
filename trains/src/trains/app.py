import sys

from celery import Celery
from kombu import Exchange, Queue
from sqlalchemy import text

from common.models.periodic_task import PeriodicTask
from settings import settings
from tasks.train_task import TrainTask


def create_celery_app() -> Celery:
    """Create and configure a celery application."""

    celery_app = Celery(
        "trains",
        broker=settings.celery_broker_url,
        task_cls=TrainTask,
        include=["tasks.tasks"],
    )

    celery_app.conf.task_queues = (
        Queue("trains", Exchange("trains", type="direct"), routing_key="trains"),
    )
    celery_app.conf.task_default_queue = "trains"

    return celery_app


def start_trains(celery_app: Celery) -> None:
    """Register a number of trains given in settings."""

    if not TrainTask.trains:
        clean_tasks()

        for _ in range(settings.number_of_trains):
            TrainTask.add_train(celery_app)


def clean_tasks() -> None:
    """Delete all periodic tasks that could be left in database before app started."""

    settings.db_session.execute(text(f"TRUNCATE TABLE {PeriodicTask.__tablename__}"))
    settings.db_session.commit()
    settings.db_session.close()


def is_worker() -> bool:
    """
    Check if the current process is a worker process, not the beat.
    """

    return "worker" in sys.argv


app = create_celery_app()

if is_worker():
    # FIXME: every periodic task is executed twice,
    #  once by parent and once by child celery process
    start_trains(app)
