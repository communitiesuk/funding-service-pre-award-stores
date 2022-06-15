"""
A file containing all tests related to the fund endpoint.
"""
import asserts
from flask import Flask
from flask import request
from tests.test_data import BREKKY_ROUND
from tests.test_data import DEFAULT_RESPONSE_FUND_DATA
from tests.test_data import HARRY_S_BREAKFAST_FUND
from tests.test_data import ROUNDS_IN_HARRY_S_BREAKFAST_FUND
from tests.test_data import TEST_RESPONSE_FUND_DATA


def test_all_funds_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response length consistent
    with all inital data (including test data).
    """
    host_url = request.host_url
    url = host_url + "funds"
    api_response_json = client.get(url).json

    expected_data = DEFAULT_RESPONSE_FUND_DATA + TEST_RESPONSE_FUND_DATA

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund"
    api_response_json = client.get(url).json

    expected_data = HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_all_rounds_in_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds"
    api_response_json = client.get(url).json

    expected_data = ROUNDS_IN_HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_round_in_single_fund_endpoint(client: Flask, load_test_data):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds/brekky"
    api_response_json = client.get(url).json

    expected_data = BREKKY_ROUND

    asserts.assert_equal(
        api_response_json,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )
