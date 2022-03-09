"""
Contains the tests regarding get requests to the Fund Store API
"""
import json


def expected_content_from_request(
    endpoint: str, expected_content, test_client, method="GET"
):
    """Given a endpoint and expected contented we
    construct a test.

    Args:
        endpoint (str): The endpoint we wish to
        make a get request on.
        expected_content: The content we expect to find
        test_client (_type_): A flask test client with a get method.
    """

    if method == "GET":
        response = test_client.get(endpoint, follow_redirects=True)
    if method == "POST":
        response = test_client.post(endpoint, follow_redirects=True)
    assert json.loads(response.data) == expected_content


def test_funds_endpoint_get(flask_test_client):
    """
    GIVEN Our Api Fund Store
    WHEN a /funds/ is requested using GET
    THEN check that the get response returns the expected data
    If this test succeedes then our apis is set up and returns
    a list of funds as expected.
    """
    expected_content = [
        {
            "fund_name": "Harry's breakfast fund",
            "fund_id": "harry-s-breakfast-fund",
            "fund_description": (
                "A fund designed to supply Harry's endless supply of muesli."
            ),
        },
        {
            "fund_name": "Ram's Get Fit Feb fund",
            "fund_id": "ram-s-get-fit-feb-fund",
            "fund_description": (
                "A fund designed to supply gym memberships to home workers"
                " during Feb."
            ),
        },
        {
            "fund_name": "Funding service design",
            "fund_id": "funding-service-design",
            "fund_description": (
                "A fund designed to test the funding service design dev team."
            ),
        },
    ]

    expected_content_from_request(
        "/funds", expected_content, flask_test_client
    )


def test_specific_fund_endpoint_get(flask_test_client):
    """
    GIVEN Our Api Fund Store
    WHEN a /funds/harry-s-breakfast-fund is requested using GET
    THEN check that the get response returns the expected data
    If this test succeedes then our apis is set up and returns
    detailed infomation about a single fund
    """
    expected_content = {
        "fund_name": "Ram's Get Fit Feb fund",
        "fund_id": "ram-s-get-fit-feb-fund",
        "fund_description": (
            "A fund designed to supply gym memberships to home workers during"
            " Feb."
        ),
    }

    expected_content_from_request(
        "/funds/ram-s-get-fit-feb-fund", expected_content, flask_test_client
    )


def test_search_endpoint_post(flask_test_client):
    """
    GIVEN Our Api Fund Store
    WHEN funds/search/?search_items=ram is requested using POST
    THEN check that the get response returns the expected data
    If this test succeedes then our seach api is set up and
    correctly searches.
    """
    expected_content = [
        {
            "fund_name": "Ram's Get Fit Feb fund",
            "fund_id": "ram-s-get-fit-feb-fund",
            "fund_description": (
                "A fund designed to supply gym memberships to home workers"
                " during Feb."
            ),
        }
    ]

    expected_content_from_request(
        "funds/search/?search_items=ram",
        expected_content,
        flask_test_client,
        method="POST",
    )
