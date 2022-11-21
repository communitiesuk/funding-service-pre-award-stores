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
    """Create a clean database for development. Unit testing makes a seperate
    db."""

    from sqlalchemy_utils.functions import create_database
    from sqlalchemy_utils.functions import database_exists
    from flask_migrate import upgrade

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

            _echo_print(
                f"Running migrations on db {Config.SQLALCHEMY_DATABASE_URI}.",
            )
            upgrade()


@task
def seed_dev_db(c):

    with _env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from tests.conftest import seed_database
            from config import Config

            choosing = True

            while choosing:

                apps = int(_echo_input("How many applications per round?"))
                rounds = int(_echo_input("How many rounds per fund?"))
                funds = int(_echo_input("How many funds?"))

                choosing = (
                    not _echo_input(
                        f"This will create {apps * rounds * funds} rows. Would"
                        " you like to continue? y/n \n"
                    ).lower()
                    == "y"
                )

            _echo_print(
                f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with"
                f" {apps * rounds * funds} test rows."
            )

            seed_database(apps, rounds, funds)

            _echo_print(
                f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} complete."
            )


@task
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    bootstrap_dev_db(c)
    seed_dev_db(c)
