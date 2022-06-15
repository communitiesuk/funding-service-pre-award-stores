"""
    Fund configuration
"""
from core.dummy_dao import FundDAO


FUND_DATA = [
    {
        "fund_name": "Funding service design",
        "fund_description": (
            "A fund designed to test the funding service design dev team."
        ),
    },
]

FUNDS_DUMMY_DAO = FundDAO()
FUNDS_DUMMY_DAO.load_dummy(FUND_DATA)
