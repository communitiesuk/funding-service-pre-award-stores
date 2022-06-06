"""
Contains test configuration.
"""
import pytest
from core.app import create_app
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    yield app
