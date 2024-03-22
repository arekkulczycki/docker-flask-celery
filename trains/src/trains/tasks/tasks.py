from logging import getLogger

from app import app
from tasks.train import Train
from tasks.train_task import (
    TrainTask,
    SPEED_ANNOUNCEMENT,
    STATION_ARRIVAL_ANNOUNCEMENT,
)

logger = getLogger("app")


@app.task(name=SPEED_ANNOUNCEMENT, exchange="trains", bind=True)
def speed_announcement(task: TrainTask, train_id: str) -> None:
    """Produce a random value."""

    train: Train = task.get_train(train_id)
    train.announce_speed()

    logger.info(f"train {train_id} announcing speed")


@app.task(name=STATION_ARRIVAL_ANNOUNCEMENT, exchange="trains", bind=True)
def station_arrival_announcement(task: TrainTask, train_id: str) -> None:
    """Produce a random value."""

    train: Train = task.get_train(train_id)
    train.announce_arrival()

    logger.info(f"train {train_id} announcing arrival")
