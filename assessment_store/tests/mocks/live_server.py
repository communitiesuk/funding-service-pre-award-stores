import pytest
from app import create_app
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.fixture(scope="session")
def app():
    """
    Returns an instance of the Flask app as a fixture for testing,
    which is available for the testing session and accessed with the
    @pytest.mark.uses_fixture('live_server')
    :return: An instance of the Flask app.
    """

    with create_app(testing=True).app_context():
        SqliteTestDB.create()
        yield
        SqliteTestDB.remove()
