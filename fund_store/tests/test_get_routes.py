"""
Contains the tests regarding get requests to the Fund Store API
"""
import json


def expected_content_from_get(endpoint: str, expected_content, test_client):
    """Given a endpoint and expected contented we
    construct a test.

    Args:
        endpoint (str): The endpoint we wish to
        make a get request on.
        expected_content: The content we expect to find
        test_client (_type_): A flask test client with a get method.
    """

    response = test_client.get(endpoint, follow_redirects=True)
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
            "name": "Harry's breakfast fund",
            "fund_identifier": "harry-s-breakfast-fund",
        },
        {
            "name": "Ram's Get Fit Feb fund",
            "fund_identifier": "ram-s-get-fit-feb-fund",
        },
        {
            "name": "Funding service design",
            "fund_identifier": "funding-service-design",
        },
    ]

    expected_content_from_get("/funds", expected_content, flask_test_client)


def test_specific_fund_endpoint_get(flask_test_client):
    """
    GIVEN Our Api Fund Store
    WHEN a /funds/harry-s-breakfast-fund is requested using GET
    THEN check that the get response returns the expected data
    If this test succeedes then our apis is set up and returns
    detailed infomation about a single fund
    """
    expected_content = {
        "name": "Ram's Get Fit Feb fund",
        "fund_identifier": "ram-s-get-fit-feb-fund",
        "eligibility_criteria": {"maximium_project_cost": 100},
        "rounds": [
            {
                "round_identifier": 1,
                "opens": "2022-02-01T00:00:00",
                "deadline": "2022-07-23T00:00:00",
            },
            {
                "round_identifier": 2,
                "opens": "2022-02-01T00:00:00",
                "deadline": "2022-07-23T00:00:00",
            },
        ],
    }

    expected_content_from_get(
        "/funds/ram-s-get-fit-feb-fund", expected_content, flask_test_client
    )


def test_specific_round_endpoint_get(flask_test_client):
    """
    GIVEN Our Api Fund Store
    WHEN /funds/ram-s-get-fit-feb-fund/round/0 is requested using GET
    THEN check that the get response returns the expected data
    If this test succeedes then our apis is set up and returns
    detailed infomation about a single fund
    """
    expected_content = {
        "round_identifier": 1,
        "opens": "2022-02-01T00:00:00",
        "deadline": "2022-07-23T00:00:00",
    }
    expected_content_from_get(
        "/funds/ram-s-get-fit-feb-fund/round/1",
        expected_content,
        flask_test_client,
    )
