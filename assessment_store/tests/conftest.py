import pytest
from app import create_app
from config import Config
from db.models.assessment_record.record_inserter import (
    bulk_insert_application_record,
)
from flask_migrate import migrate, downgrade
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from tests.db_seed_data import create_rows
from tests.sql_infos import (
    no_gather_sql,
    attach_listeners,
    pytest_terminal_summary,  # noqa
)


def prep_db():
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """

    if not database_exists(Config.TEST_SQLALCHEMY_DATABASE_URI):
        create_database(Config.TEST_SQLALCHEMY_DATABASE_URI)

    upgrade()
    migrate()
    upgrade()


def row_data(rows_to_create):
    """row_data A fixture which provides the test row data."""

    row_data = list(create_rows(rows_to_create))

    return row_data


def seed_database(rows_to_create):

    test_input_data = row_data(rows_to_create)

    bulk_insert_application_record(test_input_data, "COF")


@pytest.fixture(scope="session")
def app():

    attach_listeners()

    app = create_app()

    yield app


@pytest.fixture(scope="session")
def _db(app, request):

    db = SQLAlchemy(app)

    rows_to_create = request.config.getoption("testrows")

    with no_gather_sql("--seeding-database"):
        with app.app_context():
            prep_db()
            seed_database(rows_to_create)

    def rollback():
        with no_gather_sql("--rollback-database"):
            with app.app_context():
                downgrade(revision="base")

    request.addfinalizer(rollback)

    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):

    pass


def pytest_addoption(parser):
    parser.addoption(
        "--testrows",
        action="store",
        default=20,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--statementdetails",
        action="store",
        default=False,
        help="The amount of rows to use when testing the db.",
        type=bool,
    )
