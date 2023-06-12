import inspect

from invoke import task
from tasks.helper_tasks import _echo_input
from tasks.helper_tasks import _echo_print
from tasks.helper_tasks import _env_var

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
COF_ROUND_3_W1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"

NSTF_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NSTF_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"

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
            from uuid import uuid4
            from tests._helpers import seed_database_for_fund_round
            from config import Config

            config = {
                "COFR2W2": {
                    "fund_id": COF_FUND_ID,
                    "round_id": COF_ROUND_2_ID,
                    "type_of_application": "COF",
                },
                "COFR2W3": {
                    "fund_id": COF_FUND_ID,
                    "round_id": COF_ROUND_2_W3_ID,
                    "type_of_application": "COF",
                },
                "COFR3W1": {
                    "fund_id": COF_FUND_ID,
                    "round_id": COF_ROUND_3_W1_ID,
                    "type_of_application": "COF",
                },
                "NSTFR2": {
                    "fund_id": NSTF_FUND_ID,
                    "round_id": NSTF_ROUND_2_ID,
                    "type_of_application": "NSTF",
                },
                "RANDOM_FUND_ROUND": {
                    "fund_id": uuid4(),
                    "round_id": uuid4(),
                    "type_of_application": "RFR",
                },
            }

            choosing = not bool(fundround and appcount)
            if not choosing:
                fund_round = config[fundround]
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
                        f"{new_line} - {f' {new_line} - '.join(config.keys())}"
                        f"{new_line} > "
                    ),
                )
                fund_round = config[fundround]
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
