import sys

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
        "title_translations": {
            "en": "English Round 1",
            "cy": "Welsh round 1"},
        "fund_id": "fb986cdc-8e02-477a-a7e0-41cf19dd7675",
        "assessment_criteria_weighting": [
            {
                "id": "e2fd30d2-9207-421c-b8b3-c961bcee138b",
                "name": "Strategic case",
                "value": 0.30,
            },
            {
                "id": "e557773a-74c9-43ee-a52c-88ccae279d08",
                "name": "Management case",
                "value": 0.30,
            },
            {
                "id": "9e282cdb-6c42-4430-9563-dc4995b59bdd",
                "name": "Potential to delivery community benefits",
                "value": 0.30,
            },
            {
                "id": "6020db6c-df67-4932-a2f3-2e9dd1934164",
                "name": "Added value to the community",
                "value": 0.10,
            },
        ],
        "opens": "2099-12-25 00:00:01",
        "deadline": "2099-12-26 00:00:00",
        "assessment_deadline": "2099-12-27 00:00:00",
        "title": "English Round 1"
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
