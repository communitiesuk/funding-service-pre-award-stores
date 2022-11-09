import random
import pytest
from app import create_app
from db import db
from flask_migrate import upgrade
from tests.db_seed_data import create_rows
from tests.sql_infos import *


@pytest.fixture
def row_data(request):

    test_row_data = request.config.cache.get("assessment_test_data", None)

    rows_to_create = request.config.getoption("testrows")
    rows_per_app = request.config.getoption("rowsperapp")

    if test_row_data is None or rows_per_app != test_row_data["rows_per_app"]:

        row_data = create_rows(rows_to_create, rows_per_app)
        test_row_data = {"rows_to_create" : rows_to_create,
        "rows_per_app" : rows_per_app, "test_rows" : row_data}

        request.config.cache.set("assessment_test_data", test_row_data)

    elif rows_to_create != test_row_data["rows_to_create"]:

        if rows_to_create > test_row_data["rows_to_create"]:

            rows_to_add = rows_to_create - test_row_data["rows_to_create"]
            row_data = create_rows(rows_to_add, rows_per_app)

            test_row_data["test_rows"] = test_row_data["test_rows"] + rows_to_add
            test_row_data["rows_to_create"] = rows_to_create

            request.config.cache.set("assessment_test_data", test_row_data)

        if rows_to_create < test_row_data["rows_to_create"]:

            row_data = random.sample(test_row_data["test_rows"], rows_to_create)
            test_row_data["test_rows"] = row_data
            
            test_row_data["rows_to_create"] = rows_to_create

            request.config.cache.set("assessment_test_data", test_row_data)

    return test_row_data

@pytest.fixture
def seed_data(db_session, row_data):

    for row in row_data["test_rows"]:
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
