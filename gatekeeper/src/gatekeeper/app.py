from logging import getLogger, INFO

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from common.db import BaseModel
from routes import route_blueprint
from settings import settings, Settings


def create_app():
    app_ = Flask(__name__, instance_relative_config=True)
    app_.config.from_mapping(
        SECRET_KEY="654917cb6d1302e6013462fc81cf6db2db0689e66ebf8864cf737ed77341d56e",
        SQLALCHEMY_DATABASE_URI=settings.db_url,
    )
    Settings.db_session = SQLAlchemy(  # pyright: ignore
        app_,
        model_class=BaseModel,
        session_options={"expire_on_commit": False},
    ).session

    _redirect_logs_to_gunicorn()

    return app_


def _redirect_logs_to_gunicorn():
    logger = getLogger("app")
    gunicorn_logger = getLogger('gunicorn.error')
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)


app = create_app()
app.register_blueprint(route_blueprint)
