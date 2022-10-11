from tests.conftest import seeded_criteria

STRATEGIC_CASE_ID = "123"


def mock_get_round_full_data(*args, **kwargs):
    print("in mock_get_round")

    mock_round_data = {
        "assessment_criteria_weighting": [
            {
                "id": seeded_criteria[0].id,
                "name": seeded_criteria[0].criteria_name,
                "value": 0.8,
            },
            {
                "id": seeded_criteria[1].id,
                "name": seeded_criteria[1].criteria_name,
                "value": 0.1,
            },
            {
                "id": seeded_criteria[2].id,
                "name": seeded_criteria[2].criteria_name,
                "value": 0.1,
            },
        ],
        "assessment_deadline": "2023-03-30 12:00:00",
        "contact_details": {
            "email_address": "COF@levellingup.gov.uk",
            "phone": "",
            "text_phone": "",
        },
        "deadline": "2023-01-30 11:59:00",
        "fund_id": "fund_1",
        "id": "round_1",
        "opens": "2022-10-04 12:00:00",
        "short_name": "R2W2",
        "support_availability": {
            "closed": "Bank holidays",
            "days": "Monday to Friday",
            "time": "9am to 5pm",
        },
        "title": "Round 2 Window 2",
    }
    return mock_round_data


def mock_get_round_just_weightings(*args, **kwargs):
    return {
        "assessment_criteria_weighting": [
            {"id": STRATEGIC_CASE_ID, "name": "Strategic case", "value": 0.8},
        ]
    }
