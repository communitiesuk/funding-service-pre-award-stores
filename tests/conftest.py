"""
Contains test configuration.
"""

import pytest
from flask import Flask

from app import create_app  # noqa: E402

pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="session")
def app() -> Flask:
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client
