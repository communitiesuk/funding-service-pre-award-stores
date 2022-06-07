from core.data_operations import round_data


def get_rounds_for_fund(fund_id: str):
    rounds = round_data.ROUNDS_DUMMY_DAO.get_all(fund_id)
    if len(rounds) > 0:
        return rounds, 200
    else:
        return {
            "code": 404,
            "message": f"Rounds for fund_id : {fund_id} cannot be found.",
        }, 404


def get_round(fund_id: str, round_id: str):
    round = round_data.ROUNDS_DUMMY_DAO.get_one(fund_id, round_id)
    if round:
        return round, 200
    else:
        return {
            "code": 404,
            "message": (
                f"round_id : {round_id} in fund_id : {fund_id} cannot be"
                " found."
            ),
        }, 404
