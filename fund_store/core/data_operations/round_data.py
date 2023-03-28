"""
    Round configuration
"""
import os

from config import Config
from core.fund_round_dao import RoundDAO

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
            "Easter Sunday, Christmas Day, Boxing Day and New Year’s Day"
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


def override_fields_from_env(round_data: dict, overridable_fields: list):
    for field in overridable_fields:
        round_data[field] = os.getenv(
            f"force_{field}_{round_data['short_name']}", round_data[field]
        )
    return round_data


def get_round_data(language):

    overridable_fields = ["opens", "deadline", "assessment_deadline"]

    return [
        override_fields_from_env(
            {
                "id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
                "title": "Cylch 2 Cyfnod Cynnig 2"
                if language == "cy"
                else "Round 2 Window 2",
                "short_name": "R2W2",
                "opens": "2022-10-04 12:00:00"
                if not Config.FORCE_OPEN
                else "2022-01-01 12:00:00",
                "deadline": "2022-12-14 11:59:00"
                if not Config.FORCE_OPEN
                else "2024-12-31 11:59:00",
                "assessment_deadline": "2023-03-30 12:00:00",
                "instructions": "",
                "prospectus": "",
                **shared_cof_r2_data,
            },
            overridable_fields,
        ),
        override_fields_from_env(
            {
                "id": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
                "title": "Cylch 2 Cyfnod Cynnig 3"
                if language == "cy"
                else "Round 2 Window 3",
                "short_name": "R2W3",
                "opens": "2023-02-15 12:00:00"
                if not Config.FORCE_OPEN
                else "2022-01-01 12:00:00",
                "deadline": "2023-04-14 11:59:00"
                if not Config.FORCE_OPEN
                else "2024-12-31 11:59:00",
                "assessment_deadline": "2023-05-05 12:00:00",
                "instructions": (
                    "You must have received an invitation to apply. If we did not invite you, first"  # noqa
                    " <a href='https://www.gov.uk/government/publications/community-ownership-fund-prospectus'>"  # noqa
                    " express your interest in the fund</a>."  # noqa
                ),
                "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",  # noqa
                **shared_cof_r2_data,
            },
            overridable_fields,
        ),
    ]


ROUNDS_DAO = RoundDAO()
