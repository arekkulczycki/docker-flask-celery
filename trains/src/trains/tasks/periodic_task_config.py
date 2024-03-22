from typing import NamedTuple


class PeriodicTaskConfig(NamedTuple):
    """Template for a valid periodic tasks configuration."""

    name: str
    interval: float
