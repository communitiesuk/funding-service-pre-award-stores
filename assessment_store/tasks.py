from contextlib import contextmanager
import os
from colored import attr
from colored import fg
from colored import stylize
from invoke import task, Call
from flask_migrate import migrate
from flask_migrate import upgrade
from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy_utils.functions import database_exists

ECHO_STYLE = fg("blue") + attr("bold")


@contextmanager
def env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


@task
def bootstrap_test_db(c, database_host="localhost"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {DB_NAME}")
    print(stylize(f"{DB_NAME} db dropped...", ECHO_STYLE))
    c.run(f"createdb -h {database_host} {DB_NAME}")
    print(stylize(f"{DB_NAME} db created...", ECHO_STYLE))


@task
def profile_pytest(c, testrows=100, resultsfile="profile.txt"):
    """Runs profiling during pytest to help find slow code."""
    if not resultsfile.endswith(".txt"):
        resultsfile = resultsfile.split(".")
        resultsfile = resultsfile[0] + ".txt"
    print(stylize("Profiling tests.", ECHO_STYLE))
    c.run(
        f"python -m cProfile -s tottime -m pytest --testrows={testrows} --statementdetails=True > {resultsfile}"
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

            if database_exists(Config.DEV_SQLALCHEMY_DATABASE_URI):
                print(
                    stylize(
                        f"{Config.DEV_SQLALCHEMY_DATABASE_URI} db dropped...",
                        ECHO_STYLE,
                    )
                )
                drop_database(Config.DEV_SQLALCHEMY_DATABASE_URI)

            create_database(Config.DEV_SQLALCHEMY_DATABASE_URI)
            print(
                stylize(
                    f"{Config.DEV_SQLALCHEMY_DATABASE_URI} db created...",
                    ECHO_STYLE,
                )
            )

            print(
                stylize(
                    f"Running migrations on db {Config.DEV_SQLALCHEMY_DATABASE_URI}.",
                    ECHO_STYLE,
                )
            )
            upgrade()


@task
def seed_dev_db(c, rows=1000):

    with env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from tests.conftest import seed_database
            from config import Config

            print(
                stylize(
                    f"Seeding db {Config.DEV_SQLALCHEMY_DATABASE_URI} with {rows} test rows.",
                    ECHO_STYLE,
                )
            )

            seed_database(rows)

            print(
                stylize(
                    f"Seeding db {Config.DEV_SQLALCHEMY_DATABASE_URI} complete.",
                    ECHO_STYLE,
                )
            )


@task(pre=[bootstrap_dev_db, seed_dev_db])
def gimme_db(c):
    """Creates and seeds a database for local development."""

    pass
