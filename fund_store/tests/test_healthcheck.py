"""
A file containing all tests related to the fund endpoint.
"""
from flask import Flask


def test_healthchecks_endpoint(client: Flask):
    response = client.get("/healthcheck")

    expected_dict = {
        "checks": [{"check_flask_running": "OK"}],
        "version": "123123"
    }

    assert 200 == response.status_code, "Unexpected status code"
    assert expected_dict == response.json, "Unexpected json body"
