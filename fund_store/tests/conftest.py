import pytest
from apis.dummy_dao import FUNDS_DUMMY_DAO
from app import create_app


@pytest.fixture()
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    with create_app(FUNDS_DUMMY_DAO).test_client() as test_client:
        yield test_client
