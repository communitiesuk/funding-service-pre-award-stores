"""
    Round configuration
"""
from core.dummy_dao import RoundDAO


ROUND_DATA = [
    {
        "id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "title": "Round 2 Window 2",
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_criteria_weighting": {
            "strategy": 0.35,
            "deliverability": 0.35,
            "value_for_money": 0.3,
        },
        "opens": "2022-09-01 00:00:01",
        "deadline": "2023-01-30 00:00:01",
        "assessment_deadline": "2023-03-20 00:00:01",
    },
]

ROUNDS_DUMMY_DAO = RoundDAO()
ROUNDS_DUMMY_DAO.load_dummy(ROUND_DATA)
