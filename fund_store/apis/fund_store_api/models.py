"""Contains the models for the fund store API.
"""
from flask_restx import fields
from flask_restx import Namespace

api = Namespace("funds", description="Operations related to fund infomation")

eligibility_criteria_sub_model = api.model(
    "Eligibility",
    {
        "maximium_project_cost": fields.Integer(
            description="The maxmium amount a project can ask for"
        )
    },
)

full_fund_model = api.model(
    "Fund Full Data",
    {
        "fund_name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_id": fields.String(
            required=True, description="The unique id for the fund"
        ),
        "fund_description": fields.String(
            required=True, description="A description of the fund"
        ),
    },
)
