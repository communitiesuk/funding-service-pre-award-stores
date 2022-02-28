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

round_sub_model = api.model(
    "Fund Round",
    {
        "round_identifier": fields.Integer(
            required=True,
            description="An unique integer which identifies the round.",
        ),
        "opens": fields.DateTime(
            required=True, description="The round opening date"
        ),
        "deadline": fields.DateTime(description="The round closing date"),
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
            desciption="The eligiblity criteria of the fund",
        ),
        "rounds": fields.List(
            fields.Nested(round_sub_model),
            required=True,
            description=(
                "A list of the funding rounds, along with data regarding their"
                " opening and closing dates."
            ),
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
