from slugify import slugify


RAW_FUND_DATA = [
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
    {
        "fund_name": "Funding service design",
        "fund_description": (
            "A fund designed to test the funding service design dev team."
        ),
    },
]


FUND_DATA = [{"fund_id": slugify(i["fund_name"]), **i} for i in RAW_FUND_DATA]


HARRY_S_BREAKFAST_FUND = FUND_DATA[0]


ROUND_DATA = [
    {
        "round_id": "spring",
        "round_title": "Spring",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 1200000},
        "opens": "2022-02-01 00:00:01",
        "deadline": "2022-06-01 00:00:00",
        "assessment_deadline": "2022-09-30 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/baseline-"
        + "application-questions",
    },
    {
        "round_id": "summer",
        "round_title": "Summer",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 1500000},
        "opens": "2022-06-01 00:00:01",
        "deadline": "2022-08-31 00:00:00",
        "assessment_deadline": "2023-03-30 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/baseline-"
        + "application-questions",
    },
    {
        "round_id": "autumn",
        "round_title": "Autumn",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 10400000},
        "opens": "2022-09-01 00:00:01",
        "deadline": "2022-11-30 00:00:00",
        "assessment_deadline": "2023-03-30 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/funding-application",
    },
    {
        "round_id": "brekky",
        "round_title": "Brekky",
        "fund_id": "harry-s-breakfast-fund",
        "eligibility_criteria": {"max_project_cost": 1},
        "opens": "2099-12-25 00:00:01",
        "deadline": "2099-12-26 00:00:00",
        "assessment_deadline": "2099-12-27 00:00:00",
        "application_url": (
            "https://funding-service-design-"
            "form-runner.london.cloudapps.digital/funding-application"
        ),
    },
]

ROUNDS_IN_HARRY_S_BREAKFAST_FUND = [
    dict for dict in ROUND_DATA if dict["fund_id"] == "harry-s-breakfast-fund"
]


BREKKY_ROUND = [
    dict
    for dict in ROUNDS_IN_HARRY_S_BREAKFAST_FUND
    if dict["round_id"] == "brekky"
][0]
