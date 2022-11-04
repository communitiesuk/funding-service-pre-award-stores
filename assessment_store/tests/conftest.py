from collections import defaultdict
import traceback
from sqlalchemy.engine import Engine
import datetime
import pytest
from app import create_app
from db import db
from config import Config
from flask_migrate import upgrade
from db.models.assessment_records import AssessmentRecords
from tests.db_seed_data import create_rows
import inspect
from sqlalchemy import event

queries_types = defaultdict(int)

@event.listens_for(db.Session, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    
    if orm_execute_state.is_select:
        queries_types["selects"] =+ 1
    if orm_execute_state.is_insert:
        queries_types["inserts"] =+ 1

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(datetime.datetime.now())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = datetime.datetime.now() - conn.info["query_start_time"].pop(-1)
    if "SAVEPOINT" not in statement and 'pytest_pyfunc_call' in [frame.function for frame in inspect.stack()]:
        print(total.microseconds/1000, statement)

def pytest_addoption(parser):
    parser.addoption(
        "--testrows",
        action="store",
        default=20,
        help="The amount of rows to use when testing the db.",
        type=int,
    )

    parser.addoption(
        "--rowsperapp",
        action="store",
        default=10,
        help="The amount of rows to assign to each app use when testing the db.",
        type=int,
    )

def pytest_terminal_summary(terminalreporter):
    terminalreporter.section("Database test information")
    rows_to_create = terminalreporter.config.option.testrows
    database_url = Config.SQLALCHEMY_DATABASE_URI
    terminalreporter.write_line(f"Database URL: {database_url}")
    terminalreporter.write_line(f"Rows created: {rows_to_create} (Adjust with --testrows=INT)")
    terminalreporter.write_line(f"Selects made: {queries_types['selects']}")
    terminalreporter.write_line(f"Inserts made: {queries_types['inserts']}")
    terminalreporter.ensure_newline()


@pytest.fixture(autouse=True)
def row_data(request):

    rows_to_create = request.config.getoption("testrows")

    rows_per_app = request.config.getoption("rowsperapp")

    row_data = create_rows(rows_to_create, rows_per_app)

    yield row_data

@pytest.fixture(autouse=True)
def seed_data(db_session, row_data):

    for row in row_data:
        db.session.add(row)
    db.session.commit()
    

@pytest.fixture(scope="session")
def app():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    app = create_app()
    with app.app_context():
        upgrade()
    return app

@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """
    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):
    pass