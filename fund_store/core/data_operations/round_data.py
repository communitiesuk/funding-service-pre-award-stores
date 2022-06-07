"""Dummy data to use with testing
"""
from core.dummy_dao import RoundDAO


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

ROUNDS_DUMMY_DAO = RoundDAO()
ROUNDS_DUMMY_DAO.load_dummy(ROUND_DATA)
