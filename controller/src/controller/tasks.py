from logging import getLogger

from app import app
from clients.gatekeeper_client import GatekeeperClient
from common.station import Station
from speed_logger import SpeedLogger

TIME_IN_STATION_VICINITY_SECONDS: int = 10

logger = getLogger("app")
gatekeeper_client = GatekeeperClient()


@app.task(name="speed_announced", exchange="trains")
def speed_announced(train_id: str, speed: float) -> None:
    """Handle trains speed announcement."""

    logger.info(f"train {train_id} announced speed {speed}")

    SpeedLogger.log_speed_to_file(train_id, speed)


@app.task(name="arrival_announced", exchange="trains")
def arrival_announced(train_id: str, station: str) -> None:
    """Handle trains arrival announcement."""

    logger.info(f"train {train_id} announced upcoming arrival at station {station}")

    try:
        gatekeeper_client.close_gate(Station(station).id, train_id)

        departure.s(train_id, station).apply_async(  # pyright: ignore
            countdown=TIME_IN_STATION_VICINITY_SECONDS
        )
    except Exception as e:
        logger.error(e)
        raise


@app.task(name="departure", exchange="trains")
def departure(train_id: str, station: str) -> None:
    """Handle trains departure from the station. Gate can be opened."""

    logger.info(f"train {train_id} exited the station {station}")

    gatekeeper_client.open_gate(Station(station).id, train_id)
