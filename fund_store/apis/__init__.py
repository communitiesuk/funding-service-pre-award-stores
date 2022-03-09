"""Contains the function which initialises the API with a cusdom DAO.

Returns:
    RestX API: A RestX Api ready to be attached to a flask app.
"""
from apis.fund_discovery_api.routes import api as discovery_api
from apis.fund_discovery_api.routes import init_discovery_routes
from apis.fund_store_api.routes import api as fund_api
from apis.fund_store_api.routes import init_store_routes
from flask_restx import Api


def load_dao(dao):

    api = Api(
        title="Fund Store API",
        version="0.2",
        description=(
            "An api for requesting infomation about funds from the fund store"
        ),
        # All API metadatas
    )

    init_discovery_routes(dao)

    init_store_routes(dao)

    api.add_namespace(fund_api, path="/funds")

    api.add_namespace(discovery_api, path="/funds/search")

    return api
