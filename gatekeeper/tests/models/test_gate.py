# type: ignore
from datetime import datetime
from unittest.mock import patch, MagicMock

from pytest import fixture, mark, raises

from common.db import BaseModel
from common.station import Station
from models.gate import Gate

MA_RECENT_DATE: datetime = datetime(year=2022, month=2, day=3)
UBLIK_DATE: datetime = datetime(year=2022, month=2, day=1)


class TestGate:

    @staticmethod
    @fixture(scope="class")
    def sqlalchemy_declarative_base():
        return BaseModel

    @staticmethod
    @fixture(scope="class")
    def sqlalchemy_mock_config():
        return [
            (
                "gate",
                [
                    {"id": Station.MA.id, "closed": True, "open_permission": "ABCDEF"},
                    {
                        "id": Station.UBLIK.id,
                        "closed": False,
                        "open_permission": "DEFGHI",
                    },
                ],
            ),
            (
                "gate_switch",
                [
                    {
                        "id": 1,
                        "gate_id": Station.MA.id,
                        "value": True,
                        "created_at": MA_RECENT_DATE,
                    },
                    {
                        "id": 2,
                        "gate_id": Station.MA.id,
                        "value": False,
                        "created_at": datetime(year=2022, month=2, day=2),
                    },
                    {
                        "id": 3,
                        "gate_id": Station.MA.id,
                        "value": True,
                        "created_at": datetime(year=2022, month=2, day=1),
                    },
                    {
                        "id": 4,
                        "gate_id": Station.UBLIK.id,
                        "value": False,
                        "created_at": UBLIK_DATE,
                    },
                ],
            ),
        ]

    @staticmethod
    @mark.parametrize(
        "id_, expected_date",
        [[Station.MA.id, MA_RECENT_DATE], [Station.UBLIK.id, UBLIK_DATE]],
    )
    def test_get(mocked_session, id_, expected_date):
        mocked_settings = MagicMock(db_session=mocked_session)

        with patch("models.gate.settings", mocked_settings):
            gate = Gate.get(id_)

        assert gate.id == id_
        assert gate.switches[0].created_at == expected_date

    @staticmethod
    @mark.parametrize("closed", [True, False])
    def test_create(mocked_session, closed):
        id_ = Station.LAS.id
        mocked_settings = MagicMock(db_session=mocked_session)

        with patch("models.gate.settings", mocked_settings):
            Gate(id=id_, closed=closed, open_permission="ABCDEF").create()

        gate = mocked_session.query(Gate).filter_by(id=id_).first()

        assert gate.id == id_
        assert gate.closed == closed

    @staticmethod
    def test_create_inexistent(mocked_session):
        id_ = len(Station.__members__) + 1
        mocked_settings = MagicMock(db_session=mocked_session)

        with patch("models.gate.settings", mocked_settings), raises(ValueError):
            Gate(id=id_, closed=True, open_permission="ABCDEF").create()

    @staticmethod
    @mark.parametrize("closed", [True, False])
    def test_update(mocked_session, closed):
        id_ = Station.LAS.id
        mocked_settings = MagicMock(db_session=mocked_session)

        gate = Gate(id=id_, closed=not closed, open_permission="ABCDEF")
        mocked_session.add(gate)
        mocked_session.commit()

        with patch("models.gate.settings", mocked_settings):
            gate.update(closed, "ABCDEF")

        assert mocked_session.query(Gate).filter_by(id=id_).first().closed == closed
