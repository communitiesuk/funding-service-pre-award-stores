import os
from contextlib import contextmanager
from colored import attr
from colored import fg
from colored import stylize
from flask_migrate import upgrade
from invoke import task
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database

ECHO_STYLE = fg("blue") + attr("bold")


@contextmanager
def env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


@task
def profile_pytest(c, testrows=100, resultsfile="profile.txt"):
    """Runs profiling during pytest to help find slow code."""
    if not resultsfile.endswith(".txt"):
        resultsfile = resultsfile.split(".")
        resultsfile = resultsfile[0] + ".txt"
    print(stylize("Profiling tests.", ECHO_STYLE))
    c.run(
        "python -m cProfile -s tottime -m pytest"
        f" > {resultsfile}"
    )
    print(stylize(f"Results saved in f{resultsfile}", ECHO_STYLE))


@task
def bootstrap_dev_db(c):
    """Create a clean database for development. Unit testing makes a seperate
    db."""

    with env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from config import Config

            if database_exists(Config.SQLALCHEMY_DATABASE_URI):

                drop = input(stylize("Existing database found! Would you like to drop it and recreate? y/n \n", ECHO_STYLE))

                if drop.lower() == "y":
                    drop_database(Config.SQLALCHEMY_DATABASE_URI)
                    print(
                        stylize(
                            f"{Config.SQLALCHEMY_DATABASE_URI} db dropped...",
                            ECHO_STYLE,
                        )
                    )

                    create_database(Config.SQLALCHEMY_DATABASE_URI)
                    print(
                        stylize(
                            f"{Config.SQLALCHEMY_DATABASE_URI} db created...",
                            ECHO_STYLE,
                        )
                    )
            else:
                print(
                        stylize(
                            f"{Config.SQLALCHEMY_DATABASE_URI} not found...",
                            ECHO_STYLE,
                        )
                    )
                create_database(Config.SQLALCHEMY_DATABASE_URI)
                print(
                    stylize(
                        f"{Config.SQLALCHEMY_DATABASE_URI} db created...",
                        ECHO_STYLE,
                    )
                )
            
            print(
                stylize(
                    "Running migrations on db"
                    f" {Config.SQLALCHEMY_DATABASE_URI}.",
                    ECHO_STYLE,
                )
            )
            upgrade()


@task
def seed_dev_db(c):

    with env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from tests.conftest import seed_database
            from config import Config

            choosing = True

            while choosing:

                apps = int(input(stylize("How many applications per round?", ECHO_STYLE)))
                rounds = int(input(stylize("How many rounds per fund?", ECHO_STYLE)))
                funds = int(input(stylize("How many funds?", ECHO_STYLE)))

                choosing = (not input(stylize(f"This will create {apps * rounds * funds} rows. Would you like to continue? y/n \n", ECHO_STYLE)).lower() == "y")

            print(
                stylize(
                    f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with"
                    f" {apps * rounds * funds} test rows.",
                    ECHO_STYLE,
                )
            )

            seed_database(apps, rounds, funds)

            print(
                stylize(
                    "Seeding db"
                    f" {Config.SQLALCHEMY_DATABASE_URI} complete.",
                    ECHO_STYLE,
                )
            )


@task(pre=[bootstrap_dev_db, seed_dev_db])
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    pass

@task()
def reqs_update(c):
    """Runs the pip-compile commands in the correct order."""

    c.run("pip-compile requirements.in")
    c.run("pip-compile requirements-dev.in")



