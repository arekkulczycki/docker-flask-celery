from typing import NamedTuple

from celery.canvas import Signature


class PeriodicTaskConfig(NamedTuple):
    """Template for a valid periodic tasks configuration."""

    name: str
    interval: float
