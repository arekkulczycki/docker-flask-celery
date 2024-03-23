from __future__ import annotations

from random import choice, random, choices
from string import ascii_uppercase

from celery.canvas import Signature

from common.station import Station


class Train:
    """
    Simulator of a train.

    Announces its speed and arrival station, chosen at random.
    """

    ID_LENGTH: int = 10
    MAX_SPEED: float = 180.0

    def __init__(self) -> None:
        self.id: str = "".join(choices(ascii_uppercase, k=self.ID_LENGTH))

    def announce_speed(self, task_signature: Signature) -> None:
        """Produce announcement about trains speed."""

        task_signature.args = (self.id, self.speed)
        task_signature.apply_async()

    def announce_arrival(self, task_signature: Signature) -> None:
        """Produce announcement about trains arrival at a station."""

        task_signature.args = (self.id, self.next_station)
        task_signature.apply_async()

    @property
    def speed(self) -> float:
        """Randomly choose a speed between 0 and trains maximum speed."""

        return random() * self.MAX_SPEED

    @property
    def next_station(self) -> Station:
        """Randomly choose a member of `Station` enum class."""

        return choice(list(Station.__members__.items()))[1]
