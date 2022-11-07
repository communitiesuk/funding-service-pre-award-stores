import pytest
from app import create_app
from db import db
from flask_migrate import upgrade
from tests.db_seed_data import create_rows
from tests.sql_infos import *


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