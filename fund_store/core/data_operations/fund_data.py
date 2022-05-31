from core.dummy_dao import FundDAO

"""Dummy data to use with testing
"""
FUND_DATA = [
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

FUNDS_DUMMY_DAO = FundDAO()
FUNDS_DUMMY_DAO.load_dummy(FUND_DATA)
