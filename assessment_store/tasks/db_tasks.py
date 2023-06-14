import inspect

from invoke import task
from tasks.helper_tasks import _echo_input
from tasks.helper_tasks import _echo_print
from tasks.helper_tasks import _env_var

# Needed for invoke to work on python3.11
# Remove once invoke has been updated.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


@task
def bootstrap_dev_db(c):
    """Create a clean database for development.

    Unit testing makes a seperate db.
    """

    from sqlalchemy_utils.functions import create_database
    from sqlalchemy_utils.functions import database_exists

    with _env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from config import Config

            if database_exists(Config.SQLALCHEMY_DATABASE_URI):

                _echo_print("Existing database found!\n")

            else:
                _echo_print(
                    f"{Config.SQLALCHEMY_DATABASE_URI} not found...",
                )
                create_database(Config.SQLALCHEMY_DATABASE_URI)
                _echo_print(
                    f"{Config.SQLALCHEMY_DATABASE_URI} db created...",
                )


@task
def generate_test_data(c):

    from tests._db_seed_data import get_dynamic_rows
    import json

    _echo_print("Generating data.")
    rows = [json.loads(row) for row in get_dynamic_rows(3, 3, 10)]

    _echo_print("Writing data to apps.json")
    with open("apps.json", "w") as f:
        json.dump(rows, f, indent=4)


@task(
    help={
        "fundround": "The round and fund to seed applications for assessment.",
        "appcount": "The amount of applications to seed.",
    }
)
def seed_dev_db(c, fundround=None, appcount=None):
    """Uses the `tests.conftest.seed_database` function to insert test data
    into your dev database."""
    from flask_migrate import upgrade

    with _env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():
            from tests._helpers import seed_database_for_fund_round
            from config import Config
            from config.mappings.assessment_mapping_fund_round import (
                fund_round_mapping_config,
            )

            choosing = not bool(fundround and appcount)
            if not choosing:
                fund_round = fund_round_mapping_config[fundround]
                apps = int(appcount)
                print(
                    f"Seeding {apps} applications for "
                    f"fund_round: '{fundround}'"
                )

            while choosing:

                new_line = "\n"
                fundround = str(
                    _echo_input(
                        "Please type the fund-round to seed:"
                        f"\nfund-rounds available to seed: "
                        f"{new_line} - {f' {new_line} - '.join(fund_round_mapping_config.keys())}"
                        f"{new_line} > "
                    ),
                )
                fund_round = fund_round_mapping_config[fundround]
                apps = int(
                    _echo_input("How many applications?" f"{new_line} > ")
                )
                choosing = (
                    not _echo_input(
                        f"Would you like to insert {apps} applications"
                        f" for {fundround}? y/n \n"
                    ).lower()
                    == "y"
                )

            _echo_print(
                f"Running migrations on db {Config.SQLALCHEMY_DATABASE_URI}.",
            )

            upgrade()

            _echo_print(
                f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with"
                f" {apps} test rows."
            )
            seed_database_for_fund_round(apps, {fundround: fund_round})

            _echo_print(
                f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} complete."
            )


@task
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    bootstrap_dev_db(c)
    seed_dev_db(c)
