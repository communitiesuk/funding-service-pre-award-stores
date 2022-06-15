"""
    Round configuration
"""
from core.dummy_dao import RoundDAO


ROUND_DATA = [
    {
        "round_id": "spring",
        "round_title": "Spring",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 1200000},
        "assessment_criteria_weighting": {
            "strategy": 0.35,
            "deliverability": 0.35,
            "value_for_money": 0.3,
        },
        "opens": "2025-12-28 00:00:01",
        "deadline": "2025-12-28 00:00:00",
        "assessment_deadline": "2026-1-28 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/baseline-"
        + "application-questions",
    },
    {
        "round_id": "summer",
        "round_title": "Summer",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 1500000},
        "assessment_criteria_weighting": {
            "strategy": 0.25,
            "deliverability": 0.45,
            "value_for_money": 0.3,
        },
        "opens": "2026-3-28 00:00:01",
        "deadline": "2026-4-28 00:00:00",
        "assessment_deadline": "2026-5-28 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/baseline-"
        + "application-questions",
    },
    {
        "round_id": "autumn",
        "round_title": "Autumn",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 10400000},
        "assessment_criteria_weighting": {
            "strategy": 0.2,
            "deliverability": 0.6,
            "value_for_money": 0.2,
        },
        "opens": "2026-6-28 00:00:01",
        "deadline": "2026-7-28 00:00:00",
        "assessment_deadline": "2026-8-28 00:00:00",
        "application_url": "https://funding-service-design-"
        + "form-runner.london.cloudapps.digital/funding-application",
    },
    {
        "round_id": "winter",
        "round_title": "Winter",
        "fund_id": "funding-service-design",
        "eligibility_criteria": {"max_project_cost": 10400000},
        "assessment_criteria_weighting": {
            "strategy": 0.3,
            "deliverability": 0.4,
            "value_for_money": 0.3,
        },
        "opens": "2026-9-28 00:00:01",
        "deadline": "2026-10-28 00:00:00",
        "assessment_deadline": "2026-11-28 00:00:00",
        "application_url": (
            "https://funding-service-design-"
            "form-runner.london.cloudapps.digital/funding-application"
        ),
    },
]

ROUNDS_DUMMY_DAO = RoundDAO()
ROUNDS_DUMMY_DAO.load_dummy(ROUND_DATA)
