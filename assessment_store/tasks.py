import os
from contextlib import contextmanager
from invoke import task
import invoke

@contextmanager
def env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val

def echo_print(to_print):

    from colored import attr
    from colored import fg
    from colored import stylize

    ECHO_STYLE = fg("blue") + attr("bold")

    print(stylize(to_print, ECHO_STYLE))

def error_print(to_print):

    from colored import attr
    from colored import fg
    from colored import stylize

    ECHO_STYLE = fg("red") + attr("bold")

    print(stylize(to_print, ECHO_STYLE))

def echo_input(to_print):

    from colored import attr
    from colored import fg
    from colored import stylize

    ECHO_STYLE = fg("blue") + attr("bold")

    return input(stylize(to_print, ECHO_STYLE))

@task
def profile_pytest(c, testrows=100, resultsfile="profile.txt"):
    """Runs profiling during pytest to help find slow code."""

    if not resultsfile.endswith(".txt"):
        resultsfile = resultsfile.split(".")
        resultsfile = resultsfile[0] + ".txt"
    echo_print("Profiling tests.")
    c.run(
        "python -m cProfile -s tottime -m pytest"
        f" > {resultsfile}"
    )
    echo_print(f"Results saved in f{resultsfile}")


@task
def bootstrap_dev_db(c):
    """Create a clean database for development. Unit testing makes a seperate
    db."""

    from sqlalchemy_utils.functions import create_database
    from sqlalchemy_utils.functions import database_exists
    from sqlalchemy_utils.functions import drop_database
    from flask_migrate import upgrade

    with env_var("FLASK_ENV", "development"):

        from app import app

        with app.app_context():

            from config import Config

            if database_exists(Config.SQLALCHEMY_DATABASE_URI):

                echo_print("Existing database found!\n")

            else:
                echo_print(
                            f"{Config.SQLALCHEMY_DATABASE_URI} not found...",
                    )
                create_database(Config.SQLALCHEMY_DATABASE_URI)
                echo_print(
                        f"{Config.SQLALCHEMY_DATABASE_URI} db created...",
                )
            
            echo_print(
                    "Running migrations on db"
                    f" {Config.SQLALCHEMY_DATABASE_URI}.",
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

                apps = int(echo_input("How many applications per round?"))
                rounds = int(echo_input("How many rounds per fund?"))
                funds = int(echo_input("How many funds?"))

                choosing = (not echo_input(f"This will create {apps * rounds * funds} rows. Would you like to continue? y/n \n").lower() == "y")

            echo_print(
                    f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with"
                    f" {apps * rounds * funds} test rows."
            )

            seed_database(apps, rounds, funds)

            echo_print(
                    "Seeding db"
                    f" {Config.SQLALCHEMY_DATABASE_URI} complete."
            )


@task()
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    bootstrap_dev_db(c)
    seed_dev_db(c)

@task()
def reqs(c):
    """Runs the pip-compile commands in the correct order."""

    c.run("pip-compile requirements.in")
    c.run("pip-compile requirements-dev.in")
