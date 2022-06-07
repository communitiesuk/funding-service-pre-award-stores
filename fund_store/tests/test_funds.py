"""
A file containing all tests related to the fund endpoint.
"""
from ast import literal_eval

import asserts
from flask import Flask
from flask import request
from tests.test_data import BREKKY_ROUND
from tests.test_data import FUND_DATA
from tests.test_data import HARRY_S_BREAKFAST_FUND
from tests.test_data import ROUNDS_IN_HARRY_S_BREAKFAST_FUND


def test_all_funds_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = FUND_DATA

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_all_rounds_in_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = ROUNDS_IN_HARRY_S_BREAKFAST_FUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )


def test_single_round_in_single_fund_endpoint(client: Flask):
    """
    GIVEN the flask test client running our api
    WHEN we execute a GET request on "/funds"
    THEN we expect a response containing our
    initial data.
    """
    host_url = request.host_url
    url = host_url + "funds/harry-s-breakfast-fund/rounds/brekky"
    api_response = client.get(url)

    raw_data = api_response.data
    response_data = literal_eval(raw_data.decode("utf-8"))

    expected_data = BREKKY_ROUND

    asserts.assert_equal(
        response_data,
        expected_data,
        msg_fmt="/funds didnt return the expected response, {msg}",
    )
