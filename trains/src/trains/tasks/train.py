from __future__ import annotations

from random import choice, random, choices
from string import ascii_uppercase

from celery import Celery

from common.models.periodic_task import PeriodicTask
from common.station import Station
from settings import settings


class Train:
    """
    Simulator of a train.

    Periodically announces its speed and arrival station, chosen at random.
    """

    ID_LENGTH: int = 10
    MAX_SPEED: float = 180.0

    def __init__(self, celery_app: Celery) -> None:
        self.id: str = "".join(choices(ascii_uppercase, k=self.ID_LENGTH))
        self.celery_app: Celery = celery_app

    def announce_speed(self) -> None:
        """Produce announcement about trains speed."""

        self.celery_app.send_task(
            "speed_announced",
            (
                self.id,
                self.speed,
            ),
            queue="controller",
        )

    def announce_arrival(self) -> None:
        """Produce announcement about trains arrival at a station."""

        self.celery_app.send_task(
            "arrival_announced",
            (
                self.id,
                self.next_station,
            ),
            queue="controller",
        )

    @property
    def speed(self) -> float:
        """Randomly choose a speed between 0 and trains maximum speed."""

        return random() * self.MAX_SPEED

    @property
    def next_station(self) -> Station:
        """Randomly choose a member of `Station` enum class."""

        return choice(list(Station.__members__.items()))[1]

    def __del__(self) -> None:
        """Clean periodic tasks related to this train."""

        settings.db_session.query(PeriodicTask).filter_by(arg=self.id).delete()
        settings.db_session.commit()
        settings.db_session.close()
