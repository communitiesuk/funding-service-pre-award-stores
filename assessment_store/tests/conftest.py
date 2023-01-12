import pytest
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import (
    create_database,
    database_exists,
    drop_database,
)

from app import create_app
from config import Config
from db.queries import bulk_insert_application_record
from tests._db_seed_data import get_dynamic_rows, load_json_strings_from_file
from tests._sql_infos import pytest_terminal_summary  # noqa
from tests._sql_infos import attach_listeners


def prep_db(reuse_db=False):
    """Provide the transactional fixtures with access to the database via a
    Flask-SQLAlchemy database connection."""
    no_db = not database_exists(Config.SQLALCHEMY_DATABASE_URI)
    refresh_db = not reuse_db

    if no_db:

        create_database(Config.SQLALCHEMY_DATABASE_URI)

    elif refresh_db:

        drop_database(Config.SQLALCHEMY_DATABASE_URI)
        create_database(Config.SQLALCHEMY_DATABASE_URI)

    upgrade()


def row_data(apps_per_round, rounds_per_fund, number_of_funds):
    """row_data A fixture which provides the test row data."""

    row_data = list(
        get_dynamic_rows(apps_per_round, rounds_per_fund, number_of_funds)
    )

    return row_data


def seed_database_randomly(apps_per_round, rounds_per_fund, number_of_funds):
    test_input_data = row_data(
        apps_per_round, rounds_per_fund, number_of_funds
    )

    bulk_insert_application_record(test_input_data, "COF")


def seed_handcrafted_data():
    test_input_data = load_json_strings_from_file("hand-crafted-apps.json")

    bulk_insert_application_record(test_input_data, "COF")


def seed_database_deterministically():
    test_input_data = load_json_strings_from_file("apps.json")

    bulk_insert_application_record(test_input_data, "COF")


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
    current_run_is_random = request.config.getoption("randomdata")

    with app.app_context():

        # Did this and the last run use fixed test data?
        prev_run_deterministic = request.config.cache.get(
            "was_deterministic", False
        )
        current_run_deterministic = not current_run_is_random
        request.config.cache.set(
            "was_deterministic", current_run_deterministic
        )

        # Did this and the last run have the same db uri?
        prev_db_uri = request.config.cache.get("db_uri", False)
        current_db_uri = Config.SQLALCHEMY_DATABASE_URI
        request.config.cache.set("db_uri", current_db_uri)

        same_db_uri = prev_db_uri == current_db_uri
        both_determ = prev_run_deterministic and current_run_deterministic

        # If same data and uri then lets reuse the last test db..
        # NB: Pytest cleans up changes made during tests.
        reuse_db = same_db_uri and both_determ

        prep_db(reuse_db)
        if not reuse_db:
            if current_run_is_random:
                seed_database_randomly(
                    apps_per_round, rounds_per_fund, number_of_funds
                )
            else:
                seed_database_deterministically()

            # small number of records for testing
            seed_handcrafted_data()
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
    parser.addoption(
        "--randomdata",
        action="store",
        default=False,
        help="Decides if random data is used to seed the application rows..",
        type=bool,
    )
