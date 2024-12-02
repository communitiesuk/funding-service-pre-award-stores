import inspect
import sys

sys.path.insert(1, ".")

from invoke import task  # noqa:E402

from app import app as connexionapp  # noqa:E402
from assessment_store.tasks.helper_tasks import (
    _echo_input,  # noqa:E402
    _echo_print,  # noqa:E402
    _env_var,  # noqa:E402
)

# Needed for invoke to work on python3.11
# Remove once invoke has been updated.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


@task
def bootstrap_dev_db(c):
    """Create a clean database for development.

    Unit testing makes a seperate db.

    """

    from sqlalchemy_utils.functions import create_database, database_exists

    with _env_var("FLASK_ENV", "development"):
        with connexionapp.app.app_context():
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
    import json

    from assessment_store.tests._db_seed_data import get_dynamic_rows

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
    """Uses the `tests.conftest.seed_database` function to insert test data into
    your dev database."""
    from flask_migrate import upgrade

    with _env_var("FLASK_ENV", "development"):
        with connexionapp.app.app_context():
            from assessment_store.config.mappings.assessment_mapping_fund_round import (
                fund_round_mapping_config,
            )
            from assessment_store.tests._helpers import seed_database_for_fund_round
            from config import Config

            choosing = not bool(fundround and appcount)
            if not choosing:
                fund_round = fund_round_mapping_config[fundround]
                apps = int(appcount)
                print(f"Seeding {apps} applications for fund_round: '{fundround}'")

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
                apps = int(_echo_input("How many applications?{new_line} > "))
                choosing = (
                    not _echo_input(f"Would you like to insert {apps} applications for {fundround}? y/n \n").lower()
                    == "y"
                )

            _echo_print(
                f"Running migrations on db {Config.SQLALCHEMY_DATABASE_URI}.",
            )

            upgrade()

            _echo_print(f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with {apps} test rows.")
            seed_database_for_fund_round(apps, {fundround: fund_round})

            _echo_print(f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} complete.")


@task
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    bootstrap_dev_db(c)
    seed_dev_db(c)


@task
def seed_local_assessment_store_db(c):
    with _env_var("FLASK_ENV", "development"):
        with connexionapp.app.app_context():
            import uuid

            from assessment_store.db.models.score import AssessmentRound, ScoringSystem
            from db import db
            from fund_store.db.models.round import Round

            # Insert scoring systems
            one_to_five_id = str(uuid.uuid4())  # Generate a UUID for OneToFive
            zero_to_three_id = str(uuid.uuid4())  # Generate a UUID for OneToThree

            scoring_system_data = [
                {
                    "id": one_to_five_id,
                    "scoring_system_name": "OneToFive",
                    "minimum_score": 1,
                    "maximum_score": 5,
                },
                {
                    "id": zero_to_three_id,
                    "scoring_system_name": "ZeroToThree",
                    "minimum_score": 0,
                    "maximum_score": 3,
                },
            ]

            one_to_five = (
                db.session.query(ScoringSystem).filter(ScoringSystem.scoring_system_name == "OneToFive").one_or_none()
            )
            zero_to_three = (
                db.session.query(ScoringSystem).filter(ScoringSystem.scoring_system_name == "ZeroToThree").one_or_none()
            )

            if one_to_five is None and zero_to_three is None:
                for dictionary in scoring_system_data:
                    db.session.add(ScoringSystem(**dictionary))
            else:
                one_to_five_id = one_to_five.id
                zero_to_three_id = zero_to_three.id

            round_ids = db.session.query(Round).with_entities(Round.id).all()

            for (id,) in round_ids:
                db.session.merge(AssessmentRound(round_id=id, scoring_system_id=one_to_five_id))

            _echo_print("Seeding DB with assessment_round data and scoring_system data")

            db.session.commit()
