"""Contains the set up for our API and a basic DAO
for prototyping.
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
        "name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_identifier": fields.String(
            required=True, description="The unique id for this fund"
        ),
        "eligibility_criteria": fields.Nested(
            eligibility_criteria_sub_model,
            required=True,
            desciption="The eligiblity criteria of the fund",
        ),
        "opens": fields.DateTime(
            required=True, description="The fund opening date"
        ),
        "deadline": fields.DateTime(
            required=True, description="The fund closing date"
        ),
    },
)

identify_fund_view = api.model(
    "Fund Summary",
    {
        "name": fields.String(
            required=True, description="The name of the fund"
        ),
        "fund_identifier": fields.String(
            required=True, description="The unique id for this fund"
        ),
    },
)
