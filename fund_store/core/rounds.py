from connexion import NoContent
from core.data_operations import round_data

# from flask import request


def get_rounds_for_fund(fund_id: str):
    rounds = round_data.ROUNDS_DUMMY_DAO.get_all(fund_id)
    if len(rounds) > 0:
        return rounds
    else:
        return NoContent, 404


def get_round(fund_id: str, round_id: str):
    round = round_data.ROUNDS_DUMMY_DAO.get_one(fund_id, round_id)
    if round:
        return round
    else:
        return NoContent, 404
