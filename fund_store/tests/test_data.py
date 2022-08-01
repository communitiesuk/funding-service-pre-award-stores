import sys

from slugify import slugify

TEST_FUND_DATA = [
    {
        "id": "fb986cdc-8e02-477a-a7e0-41cf19dd7675",
        "name": "Test fund 1",
        "description": "Test fund description 1",
    },
    {
        "id": "e356c266-68a8-4000-ad95-6e4d961f65b4",
        "name": "Test fund 2",
        "description": "Test fund description 2",
    },
]

TEST_ROUND_DATA = [
    {
        "id": "3b1ae9e8-eda4-4910-a5dd-fc144f9a8ba1",
        "title": "Test Round 1",
        "fund_id": "fb986cdc-8e02-477a-a7e0-41cf19dd7675",
        "assessment_criteria_weighting": {
            "strategy": 0.3,
            "deliverability": 0.4,
            "value_for_money": 0.3,
        },
        "opens": "2099-12-25 00:00:01",
        "deadline": "2099-12-26 00:00:00",
        "assessment_deadline": "2099-12-27 00:00:00",
    }
]

# When processed by the api, a slugied fund-id is added to the fund
# dictionary. We simulate this step here
TEST_RESPONSE_FUND_DATA = TEST_FUND_DATA

# setting parent path to get default fund data
sys.path.append("../core")
from core.data_operations.fund_data import (  # noqa
    FUND_DATA as DEFAULT_FUND_DATA,
)

DEFAULT_RESPONSE_FUND_DATA = DEFAULT_FUND_DATA


TEST_FUND_ONE = TEST_RESPONSE_FUND_DATA[0]


TEST_ROUNDS_IN_FUND_ONE = [
    dict
    for dict in TEST_ROUND_DATA
    if dict["fund_id"] == "fb986cdc-8e02-477a-a7e0-41cf19dd7675"
]


TEST_ROUND_ONE = [
    dict
    for dict in TEST_ROUNDS_IN_FUND_ONE
    if dict["id"] == "3b1ae9e8-eda4-4910-a5dd-fc144f9a8ba1"
][0]