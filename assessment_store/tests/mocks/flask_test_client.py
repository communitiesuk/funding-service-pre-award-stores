import pytest
from app import create_app
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.fixture(scope="class")
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    with create_app().app_context() as app_context:
        SqliteTestDB.create()
        with app_context.app.test_client() as test_client:
            yield test_client
        SqliteTestDB.remove()
