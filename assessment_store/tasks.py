from colored import attr
from colored import fg
from colored import stylize
from invoke import task

ECHO_STYLE = fg("blue") + attr("bold")
DB_NAME = "fsd_assess_store_test"


@task
def bootstrap_test_db(c, database_host="localhost"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {DB_NAME}")
    print(stylize(f"{DB_NAME} db dropped...", ECHO_STYLE))
    c.run(f"createdb -h {database_host} {DB_NAME}")
    print(stylize(f"{DB_NAME} db created...", ECHO_STYLE))
