"""
Imports the API and attaches routes to it.
"""
from apis.fund_store_api.models import api
from apis.fund_store_api.models import full_fund_model
from flask_restx import Resource


def init_store_routes(dao):
    """This functions allows for an
    arbituary DAO object to be used
    in the api. This allows for testing
    dummy data.

    Args:
        dummy_dao (_type_): A DAO object.

    Returns:
        _type_: None, but adds routes to the api.
    """

    @api.route("/")
    class FundList(Resource):
        @api.doc("list_funds")
        @api.marshal_list_with(full_fund_model)
        def get(self):
            """List all funds"""
            return dao.get_all()

    @api.route("/<fund_identifier>")
    @api.param("fund_identifier", "The id of the fund")
    @api.response(404, "Fund not found")
    class Fund(Resource):
        @api.doc("get_fund")
        @api.marshal_with(full_fund_model)
        def get(self, fund_identifier):
            """Fetch a fund given its name"""
            return dao.get(fund_identifier)
