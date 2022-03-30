from api.namespace.fund.routes import fund_ns
from api.namespace.search.routes import search_ns
from flask_restx import Api

api = Api(
    title="Funding Service Design Application Store API",
    version="0.1.0",
    description="A simple Funding Service Design Application Store API",
)

api.add_namespace(fund_ns)
api.add_namespace(search_ns)
