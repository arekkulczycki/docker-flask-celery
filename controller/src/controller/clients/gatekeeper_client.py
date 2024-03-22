from logging import getLogger
from typing import Dict

import requests

logger = getLogger("app")


class GatekeeperClient:
    """
    Provider of the communication layer with `gatekeeper` and the gatekeeping logic.
    """

    GATEKEEPER_BASE_URL: str = "http://gatekeeper:5000/gate"
    CLOSE_GATE: str = "1"
    OPEN_GATE: str = "0"

    def open_gate(self, station_id: int, train_id: str) -> None:
        """
        Opens gate in a station on request.

        Gate should not be opened by one train when another arrives, therefore
        the last train to announce arrival has the permission to close.

        Moreover, concurrency should be taken care of, on db level,
        to avoid situation when open and close signals arrive at the same time
        and close is overwritten by open.
        """

        response = requests.put(
            self._get_url(str(station_id), self.OPEN_GATE),
            data={"train_id": train_id},
        )

        if response.status_code != 200:
            self._log_error(response.status_code, response.json(), "opening gate")
        else:
            logger.info("gate was successfully opened")

    def close_gate(self, station_id: int, train_id: str) -> None:
        self._check_if_closed_already(station_id)

        response = requests.put(
            self._get_url(str(station_id), self.CLOSE_GATE), data={"train_id": train_id}
        )

        if response.status_code != 200:
            self._log_error(response.status_code, response.json(), "closing gate")
        else:
            logger.info("gate was successfully closed")

    def _check_if_closed_already(self, station_id: int) -> None:
        """Produce a warning if the gate is unexpectedly closed."""

        response = requests.get(self._get_url(str(station_id)))
        response_json = response.json()
        if response.status_code != 200:
            logger.warning(f"gate not found for station {station_id}")

        elif response_json["closed"]:
            logger.warning(
                f"gate was already closed before train arrival, "
                f"closed by {response_json['train_id']}"
            )

    def _get_url(self, *args: str) -> str:
        return "/".join((self.GATEKEEPER_BASE_URL, *args))

    @staticmethod
    def _log_error(status_code: int, response_json: Dict, action: str) -> None:
        logger.error(
            f"gatekeeper responded with code {status_code} while {action}\n"
            f"error: {response_json['error']}"
        )
