"""A dummy DAO implementation. Acts as a template for our
future implementation.
"""


class FundDAO:
    """A dummy interface to use instead of a database ORM."""

    def __init__(self):
        self.funds = {}

    def get_one(self, fund_id, language):
        fund = self.funds.get(fund_id, language)
        return fund

    def get_all(self):
        return list(self.funds.values())

    def create(self, data):
        self.funds[data["id"]] = data

    def load_dummy(self, fund_data):
        for fund in fund_data:
            self.create(fund)


class RoundDAO:
    """A dummy interface to use instead of a database ORM."""

    def __init__(self):
        self.rounds = {}

    def get_one(self, fund_id, round_id, language):
        all_round_list = list(self.rounds.values())
        fund_round_list = [
            round for round in all_round_list if round["fund_id"] == fund_id
        ]
        the_round = next(
            (round for round in fund_round_list if round["id"] == round_id),
            None,
        )
        return the_round

    def get_all_for_fund(self, fund_id):
        all_round_list = list(self.rounds.values())
        fund_round_list = [
            round for round in all_round_list if round["fund_id"] == fund_id
        ]
        return fund_round_list

    def create(self, data):
        self.rounds[data["id"]] = data

    def load_dummy(self, round_data):
        for round in round_data:
            self.create(round)
