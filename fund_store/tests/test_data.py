import sys

from slugify import slugify

TEST_FUND_DATA = [
    {
        "fund_name": "Harry's breakfast fund",
        "fund_description": (
            "A fund designed to supply Harry's endless supply of muesli."
        ),
    },
    {
        "fund_name": "Ram's Get Fit Feb fund",
        "fund_description": (
            "A fund designed to supply gym memberships to home workers during"
            " Feb."
        ),
    },
]


TEST_ROUND_DATA = [
    {
        "round_id": "brekky",
        "round_title": "Brekky",
        "fund_id": "harry-s-breakfast-fund",
        "eligibility_criteria": {"max_project_cost": 1},
        "assessment_criteria_weighting": {
            "strategy": 0.3,
            "deliverability": 0.4,
            "value_for_money": 0.3,
        },
        "opens": "2099-12-25 00:00:01",
        "deadline": "2099-12-26 00:00:00",
        "assessment_deadline": "2099-12-27 00:00:00",
        "application_url": (
            "https://funding-service-design-"
            "form-runner.london.cloudapps.digital/funding-application"
        ),
    }
]

# When processed by the api, a slugied fund-id is added to the fund
# dictionary. We simulate this step here
TEST_RESPONSE_FUND_DATA = [
    {"fund_id": slugify(i["fund_name"]), **i} for i in TEST_FUND_DATA
]
# setting parent path to get default fund data
sys.path.append("../core")
from core.data_operations.fund_data import (  # noqa
    FUND_DATA as DEFAULT_FUND_DATA,
)

DEFAULT_RESPONSE_FUND_DATA = [
    {"fund_id": slugify(i["fund_name"]), **i} for i in DEFAULT_FUND_DATA
]


HARRY_S_BREAKFAST_FUND = TEST_RESPONSE_FUND_DATA[0]


ROUNDS_IN_HARRY_S_BREAKFAST_FUND = [
    dict
    for dict in TEST_ROUND_DATA
    if dict["fund_id"] == "harry-s-breakfast-fund"
]


BREKKY_ROUND = [
    dict
    for dict in ROUNDS_IN_HARRY_S_BREAKFAST_FUND
    if dict["round_id"] == "brekky"
][0]
