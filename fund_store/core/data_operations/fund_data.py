"""
    Fund configuration
"""
from core.dummy_dao import FundDAO


FUND_DATA = [
    {
        "id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "name": "Community Ownership Fund",
        "contact_email": "COF@levellingup.gov.uk",
        "description": (
            "The Community Ownership Fund is a £150 million fund over 4 years to support community groups across "
            "England, Wales, Scotland and Northern Ireland to take ownership of assets which are at risk of being "
            "lost to the community."
        ),
    },
]

FUNDS_DUMMY_DAO = FundDAO()
FUNDS_DUMMY_DAO.load_dummy(FUND_DATA)
