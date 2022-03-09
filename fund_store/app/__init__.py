"""The entry point for app.py to start our app
"""
from apis import load_dao
from apis.dummy_dao import FUNDS_DUMMY_DAO
from flask import Flask


def create_app(dao) -> Flask:

    flask_app = Flask(__name__)

    api = load_dao(dao)

    api.init_app(flask_app)

    return flask_app


# When productionised we will pass a different DAO in here.
app = create_app(FUNDS_DUMMY_DAO)
