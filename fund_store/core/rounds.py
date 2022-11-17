"""
Python functions to return responses of rounds from our GET requests
"""
from core.data_operations import round_data
from flask import request


def get_rounds_for_fund(fund_id: str):
    """python function to return all rounds in a given fund, by fund_id

    :param fund_id: fund_id to search rounds for given fund
    :type fund_id: str
    :return: Tuple containing the list of rounds for a given
                fund_id and response code
    :rtype: Tuple
    """
    rounds = round_data.ROUNDS_DUMMY_DAO.get_all_for_fund(fund_id)
    if len(rounds) > 0:
        return rounds, 200
    else:
        return {
            "code": 404,
            "message": f"Rounds for fund_id : {fund_id} cannot be found.",
        }, 404


def get_round(fund_id: str, round_id: str):
    """python function to return a single round given a fund_id and round_id

    :param fund_id: fund_id to search rounds for given fund
    :type fund_id: str
    :param round_id: round_id to search for specific round
    :type round_id: str
    :return: Tuple containgin the specific round given by the
                fund_id and round_id, and the response code
    :rtype: Tuple
    """
    language = request.args.get("language")
    round = round_data.ROUNDS_DUMMY_DAO.get_one(fund_id, round_id, language)
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
