# type: ignore
from datetime import datetime
from unittest.mock import patch

from pytest import fixture, mark

from app import create_app
from common.station import Station
from models.gate import Gate
from models.gate_switch import GateSwitch
from routes import route_blueprint


class TestRoutes:

    @staticmethod
    @fixture()
    def app():
        app_ = create_app()
        app_.config.update(
            {
                "TESTING": True,
            }
        )
        app_.register_blueprint(route_blueprint)

        return app_

    @staticmethod
    @fixture(scope="function")
    def client(app):
        return app.test_client()

    @staticmethod
    def test_get_gate_status(client):
        d = datetime(year=2022, month=2, day=2)
        gate = Gate(id=1, closed=True, open_permission="ABCDEF")
        gate.switches = [GateSwitch(gate=gate, value=True, created_at=d)]

        with patch("routes.Gate.get", return_value=gate):
            response = client.get(f"/gate/{Station.MA.id}")

        assert response.status_code == 200
        assert response.json["closed"] == gate.closed
        assert response.json["last_change"] == d.strftime(format="%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def test_get_gate_status_error(client):
        with patch("routes.Gate.get", return_value=None):
            response = client.get("/gate/123")

        assert response.status_code == 400

    @staticmethod
    @mark.parametrize("should_return_none", [True, False])
    def test_toggle_gate(client, should_return_none):
        gate = Gate(id=1, closed=False, open_permission="ABCDEF")
        get_return_value = None if should_return_none else gate

        with patch("routes.Gate.get_for_update", return_value=get_return_value), patch(
            "routes.Gate.create", return_value=gate
        ), patch("routes.Gate.update", return_value=gate):
            response = client.put(
                f"/gate/{Station.MA.id}/1", data={"train_id": "DEFGHI"}
            )

        assert response.status_code == 200
        assert response.json["closed"] == gate.closed

    @staticmethod
    def test_toggle_gate_error(client):
        with patch("routes.Gate.get_for_update", return_value=None), patch(
            "routes.Gate.create", side_effect=ValueError
        ):
            response = client.put(
                f"/gate/{Station.MA.id}/1", data={"train_id": "DEFGHI"}
            )

        assert response.status_code == 400
