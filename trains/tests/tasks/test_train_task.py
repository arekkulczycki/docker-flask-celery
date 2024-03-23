# type: ignore
from unittest.mock import patch, MagicMock

from pytest import fixture

from common.db import BaseModel
from common.models.periodic_task import PeriodicTask
from tasks.train_task import TrainTask, ANNOUNCEMENT_TASK_CONFIGS


class TestTrainTask:

    @staticmethod
    @fixture(scope="class")
    def sqlalchemy_declarative_base():
        return BaseModel

    @staticmethod
    @fixture(scope="function")
    def celery_app():
        with patch("tasks.train_task.logger"):
            yield MagicMock()

    def test_add_train(self, mocked_session, celery_app):
        mocked_settings = MagicMock(db_session=mocked_session)

        with patch("tasks.train_task.settings", mocked_settings):
            TrainTask.add_train()

        assert mocked_session.query(PeriodicTask).count() == len(
            ANNOUNCEMENT_TASK_CONFIGS
        )
