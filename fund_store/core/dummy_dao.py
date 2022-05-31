"""A dummy DAO implementation. Acts as a template for our
future implementation.
"""
from slugify import slugify


class FundDAO:
    """A dummy interface to use instead of a database ORM."""

    def __init__(self):
        self.funds = {}

    def get_one(self, fund_id):
        return self.funds.get(fund_id)

    def get_all(self):
        return list(self.funds.values())

    def create(self, data):
        key = slugify(data["fund_name"])
        data["fund_id"] = key
        self.funds[key] = data

    def load_dummy(self, fund_data):
        for fund in fund_data:
            self.create(fund)
