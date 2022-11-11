import pytest
from app import create_app
from config import Config
from db import db
from db.models.assessment_record.record_inserter import (
    bulk_insert_application_record,
)
from flask_migrate import migrate
from flask_migrate import upgrade
from pytest import event
from sqlalchemy.engine import Engine
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database
from tests.db_seed_data import create_rows
from tests.sql_infos import *  # noqa


@pytest.fixture(scope="session")
def row_data(request):
    """row_data A fixture which provides the test row data. Uses caching to
    allow sharing data between test sessions.
    """

    rows_to_create = request.config.getoption("testrows")

    row_data = create_rows(rows_to_create)
    test_row_data = {
        "rows_to_create": rows_to_create,
        "test_rows": list(row_data),
    }

    return test_row_data


@pytest.fixture(autouse=True)
def seed_data(app, row_data):
    @event.listens_for(Engine, "before_cursor_execute", retval=True)
    def mark_seed_data_queries(
        conn, cursor, statement, parameters, context, executemany
    ):
        statement = statement + " --seeding-database"
        return statement, parameters

    with app.app_context():
        migrate()
        upgrade()

    bulk_insert_application_record(row_data["test_rows"], "COF")

    event.remove(Engine, "before_cursor_execute", mark_seed_data_queries)


@pytest.fixture(scope="session")
def app():
    """
    Creates a very minimal flask app just for testing db related functionality.
    """
    app = create_app()
    yield app


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """
    if not database_exists(Config.TEST_SQLALCHEMY_DATABASE_URI):
        create_database(Config.TEST_SQLALCHEMY_DATABASE_URI)
    yield db

    drop_database(Config.TEST_SQLALCHEMY_DATABASE_URI)


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):

    pass
