import logging
import time
import pytest
from app import create_app
from config import Config
from db.queries.assessment_records import (
    bulk_insert_application_record,
)
from flask_migrate import downgrade
from flask_migrate import migrate
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database
from tests.db_seed_data import create_rows
from tests.sql_infos import attach_listeners
from tests.sql_infos import pytest_terminal_summary  # noqa

def prep_db():
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """

    if database_exists(Config.SQLALCHEMY_DATABASE_URI):
        drop_database(Config.SQLALCHEMY_DATABASE_URI)

    create_database(Config.SQLALCHEMY_DATABASE_URI)

    upgrade()


def row_data(apps_per_round, rounds_per_fund, number_of_funds):
    """row_data A fixture which provides the test row data."""

    row_data = list(
        create_rows(apps_per_round, rounds_per_fund, number_of_funds)
    )

    return row_data


def seed_database(apps_per_round, rounds_per_fund, number_of_funds):

    start = time.time()

    test_input_data = row_data(
        apps_per_round, rounds_per_fund, number_of_funds
    )

    bulk_insert_application_record(test_input_data, "COF")

    end = time.time()

    print(
        'Creating test rows took:'
        f', time={end - start:.3f}'
    )


@pytest.fixture(scope="session")
def app():

    attach_listeners()

    app = create_app()

    yield app


@pytest.fixture(scope="session")
def _db(app, request):

    db = SQLAlchemy(app)

    apps_per_round = request.config.getoption("apps_per_round")
    rounds_per_fund = request.config.getoption("rounds_per_fund")
    number_of_funds = request.config.getoption("number_of_funds")

    with app.app_context():
        prep_db()
        seed_database(apps_per_round, rounds_per_fund, number_of_funds)

    def rollback():
        with app.app_context():
            downgrade(revision="base")

    request.addfinalizer(rollback)

    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):

    yield


def pytest_addoption(parser):
    parser.addoption(
        "--apps-per-round",
        action="store",
        default=100,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--rounds-per-fund",
        action="store",
        default=2,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--number-of-funds",
        action="store",
        default=5,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--statementdetails",
        action="store",
        default=True,
        help="The amount of rows to use when testing the db.",
        type=bool,
    )
