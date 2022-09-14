"""
    Round configuration
"""
from core.dummy_dao import RoundDAO

ROUND_DATA = [
    {
        "id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "title": "Round 2 Window 2",
        "short_name": "R2W2",
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_criteria_weighting": [
            {
                "id": "e2fd30d2-9207-421c-b8b3-c961bcee138b",
                "name": "Strategic case",
                "value": 0.30
            },
            {
                "id": "e557773a-74c9-43ee-a52c-88ccae279d08",
                "name": "Management case",
                "value": 0.30
            },
            {
                "id": "9e282cdb-6c42-4430-9563-dc4995b59bdd",
                "name": "Potential to delivery community benefits",
                "value": 0.30
            },
            {
                "id": "6020db6c-df67-4932-a2f3-2e9dd1934164",
                "name": "Added value to the community",
                "value": 0.10
            }
        ],
        "opens": "2022-10-04 12:00:00",
        "deadline": "2023-01-30 11:59:00",
        "assessment_deadline": "2023-03-30 12:00:00",
        "contact_details": {
            "phone": "",
            "email_address": "COF@levellingup.gov.uk",
            "text_phone": ""
        },
        "support_availability": {
            "time": "9am to 5pm",
            "days": "Monday to Friday",
            "closed": "Easter Sunday, Christmas Day, Boxing Day and New Year’s Day"
        }
    },
]

ROUNDS_DUMMY_DAO = RoundDAO()
ROUNDS_DUMMY_DAO.load_dummy(ROUND_DATA)
