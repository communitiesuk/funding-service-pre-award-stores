"""
    Round configuration
"""
from config import Config
from core.dummy_dao import RoundDAO

shared_cof_r2_data = {
    "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",

    "contact_details": {
        "phone": "",
        "email_address": "COF@levellingup.gov.uk",
        "text_phone": "",
    },
    "support_availability": {
        "time": "9am to 5pm",
        "days": "Monday to Friday",
        "closed": (
            "Easter Sunday, Christmas Day, Boxing Day and New"
            " Year’s Day"
        ),
    },

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
}

def get_round_data(language):

    return [
        {
            "id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
            "title": "Cylch 2 Window 2"
            if language == "cy"
            else "Round 2 Window 2",
            "short_name": "R2W2",
            "opens": "2022-10-04 12:00:00",
            "deadline": "2022-12-14 11:59:00"
            if not Config.FORCE_OPEN
            else "2024-12-31 11:59:00",
            "assessment_deadline": "2023-03-30 12:00:00",
            **shared_cof_r2_data
        },
        {
            "id": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
            "title": "Cylch 2 Window 3"
            if language == "cy"
            else "Round 2 Window 3",
            "short_name": "R2W3",
            "opens": "2023-02-08 12:00:00"
            if not Config.FORCE_OPEN
            else "2022-01-01 12:00:00",
            "deadline": "2023-04-05 11:59:00"
            if not Config.FORCE_OPEN
            else "2024-12-31 11:59:00",
            "assessment_deadline": "2023-05-05 12:00:00",
            **shared_cof_r2_data
        },
    ]


ROUNDS_DUMMY_DAO = RoundDAO()
