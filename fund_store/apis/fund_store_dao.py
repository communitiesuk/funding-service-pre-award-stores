from apis.fund_api_models import api
from slugify import slugify


class FundDAO:
    """A dummy interface to use instead of a database ORM."""

    def __init__(self):
        self.funds = {}

    def get_all(self):
        return list(self.funds.values())

    def create(self, data):
        key = slugify(data["name"])
        data["fund_identifier"] = key
        self.funds[key] = data

    def load_dummy(self, fund_data):

        for fund in fund_data:

            self.create(fund)

    def get(self, identifier):
        if identifier in self.funds.keys():
            return self.funds[identifier]
        api.abort(404, f"Fund {identifier} doesn't exist")
