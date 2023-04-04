"""Simple DAO class that works with static data defined in code.
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

    def load_data(self, fund_data):
        for fund in fund_data:
            self.create(fund)

    def search_by_short_name(self, short_name):
        return next(
            (
                fund
                for fund in self.get_all()
                if str.upper(fund["short_name"]) == str.upper(short_name)
            ),
            None,
        )


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

    def load_data(self, round_data):
        for round in round_data:
            self.create(round)

    def get_all(self):
        return list(self.rounds.values())

    def search_by_round_short_name(self, round_short_name, fund):

        fund_round_list = [
            round for round in self.get_all() if round["fund_id"] == fund.get("id")
        ]

        return next(
            (
                round
                for round in  fund_round_list
                if str.upper(round["short_name"]) == str.upper(round_short_name)
            ),
            None,
        )
