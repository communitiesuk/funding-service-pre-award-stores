from apis.fund_api_routes import api as fund_api
from flask_restx import Api

api = Api(
    title="Fund Store API",
    version="0.1",
    description=(
        "An api for requesting infomation about funds from the fund store"
    ),
    # All API metadatas
)

api.add_namespace(fund_api, path="/funds")
