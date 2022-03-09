"""
Imports the API from fund_app.py and creates the routes
in it.
"""
from apis.fund_discovery_api.fund_discovery_search import search
from apis.fund_discovery_api.models import api
from apis.fund_discovery_api.models import full_search_result
from flask_restx import reqparse
from flask_restx import Resource


def init_discovery_routes(dao):
    """This functions allows for an
    arbituary DAO object to be used
    in the api. This allows for testing
    dummy data.

    Args:
        dummy_dao (_type_): A DAO object.

    Returns:
        _type_: None, but adds routes to the api.
    """
    search_parser = reqparse.RequestParser()
    search_parser.add_argument("search_items", action="split")

    @api.route("/")
    class FundSearch(Resource):
        @api.doc("search_funds")
        @api.marshal_list_with(full_search_result)
        @api.expect(search_parser, validate=True)
        def post(self):
            """List all funds"""
            args = search_parser.parse_args()
            return search(dao.get_all(), args["search_items"])
