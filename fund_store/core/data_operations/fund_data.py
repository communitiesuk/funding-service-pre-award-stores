"""
    Fund configuration
"""
from core.fund_round_dao import FundDAO


def get_fund_data(language):
    return [
        {
            "id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
            "name": "Y Cronfa Perchnogaeth Gymunedol"
            if language == "cy"
            else "Community Ownership Fund",
            "title": "Gwneud cais am gyllid i achub ased yn eich cymuned" 
            if language =="cy"
            else "Apply for funding to save an asset in your community",
            "short_name": "COF",
            "description": (
                "The Community Ownership Fund is a £150 million fund over 4"
                " years to support community groups across England, Wales,"
                " Scotland and Northern Ireland to take ownership of assets"
                " which are at risk of being lost to the community."
            ),
        },
    ]


FUNDS_DAO = FundDAO()
