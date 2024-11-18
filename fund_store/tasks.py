import os
from urllib.parse import urlparse

from colored import attr
from colored import fg
from colored import stylize
from invoke import task

ECHO_STYLE = fg("light_gray") + attr("bold")


@task
def recreate_local_db(c):
    """Create a clean database for testing"""

    # As we assume "db_name" is not yet created. First we need to connect to psql with an existing database
    # Replace database in database_url with "postgres" db
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise Exception("Please set the environmental variable 'DATABASE_URL'!")
    parsed_db_url = urlparse(database_url)
    database_host = parsed_db_url.hostname
    db_name = parsed_db_url.path.lstrip("/")
    parsed_db_url = parsed_db_url._replace(path="/postgres")
    database_url = parsed_db_url.geturl()

    c.run(f'psql {database_url} -c "DROP DATABASE IF EXISTS {db_name} WITH (FORCE);"')
    print(
        stylize(
            f"{db_name} db dropped from {database_host}...",
            ECHO_STYLE,
        )
    )
    c.run(f'psql {database_url} -c "CREATE DATABASE {db_name};"')
    c.run(f'psql {database_url} -c "create extension if not exists ltree;"')
    print(stylize(f"{db_name} db created on {database_host}...", ECHO_STYLE))


@task
def truncate_data(c):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise Exception("Please set the environmental variable 'DATABASE_URL'!")
    c.run(
        f'psql {database_url} -c "TRUNCATE TABLE section, round, fund,'
        " assessment_field, form_name, section_field CASCADE;ALTER SEQUENCE"
        ' section_id_seq RESTART WITH 1;";'
    )
