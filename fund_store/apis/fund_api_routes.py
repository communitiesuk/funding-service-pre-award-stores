"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_api_models import api
from apis.fund_api_models import full_fund_model
from apis.fund_api_models import identify_fund_view
from apis.fund_api_models import round_sub_model
from apis.fund_store_dao import FundDAO
from apis.fund_store_dummy_data import FUND_DATA
from flask_restx import Resource

FUNDS = FundDAO()
FUNDS.load_dummy(FUND_DATA)


@api.route("/")
class FundList(Resource):
    @api.doc("list_funds")
    @api.marshal_list_with(identify_fund_view)
    def get(self):
        """List all funds"""
        return FUNDS.get_all()


@api.route("/<fund_identifier>")
@api.param("fund_identifier", "The id of the fund")
@api.response(404, "Fund not found")
class Fund(Resource):
    @api.doc("get_fund")
    @api.marshal_with(full_fund_model)
    def get(self, fund_identifier):
        """Fetch a fund given its name"""
        return FUNDS.get(fund_identifier)


@api.route("/<fund_identifier>/round/<round_number>")
@api.param("fund_identifier", "The fund identifier of the fund")
@api.param("round_number", "The round identifier of the fund round")
@api.response(404, "Round not found")
class Round(Resource):
    @api.doc("get_round")
    @api.marshal_with(round_sub_model)
    def get(self, fund_identifier, round_number):
        """Fetch a fund given its name"""
        return FUNDS.get(fund_identifier)["rounds"][int(round_number) - 1]
