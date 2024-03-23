# type: ignore
from unittest.mock import patch, MagicMock

from pytest import fixture, mark

from clients.gatekeeper_client import GatekeeperClient


class TestGatekeeperClient:

    @staticmethod
    @fixture(scope="function")
    def client():
        with patch("clients.gatekeeper_client.logger") as mock_logger:
            client = GatekeeperClient()
            client.logger = mock_logger
            yield client

    @staticmethod
    @mark.parametrize(
        "put_status_code, logger_method_called", [[200, "info"], [400, "error"]]
    )
    def test_open_gate(
        client: GatekeeperClient, put_status_code: int, logger_method_called: str
    ):
        station_id = 123
        train_id = "ABC"
        expected_url = "http://gatekeeper:5000/gate/123/0"
        expected_put_body = {"train_id": train_id}

        mock_put = MagicMock(return_value=MagicMock(status_code=put_status_code))
        with patch("clients.gatekeeper_client.requests.put", mock_put):
            client.open_gate(station_id, train_id)

        mock_put.assert_called_once_with(expected_url, data=expected_put_body)
        assert getattr(client.logger, logger_method_called).called

    @staticmethod
    @mark.parametrize(
        "get_status_code, put_status_code, logger_calls",
        [
            [200, 200, {"info": 1}],
            [404, 200, {"warning": 1, "info": 1}],
            [404, 404, {"warning": 1, "error": 1}],
        ],
    )
    def test_close_gate(
        client: GatekeeperClient,
        get_status_code: int,
        put_status_code: int,
        logger_calls,
    ):
        station_id = 321
        train_id = "DEF"
        expected_url = "http://gatekeeper:5000/gate/321/1"
        expected_put_body = {"train_id": train_id}

        mock_get = MagicMock(return_value=MagicMock(status_code=get_status_code))
        mock_put = MagicMock(return_value=MagicMock(status_code=put_status_code))
        with patch("clients.gatekeeper_client.requests.get", mock_get), patch(
            "clients.gatekeeper_client.requests.put", mock_put
        ):
            client.close_gate(station_id, train_id)

        mock_put.assert_called_once_with(expected_url, data=expected_put_body)

        for method, times_called in logger_calls.items():
            assert getattr(client.logger, method).call_count == times_called
