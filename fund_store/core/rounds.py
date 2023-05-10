"""
Python functions to return responses of rounds from our GET requests
"""
from core.data_operations import fund_data
from core.data_operations import round_data
from core.funds import get_fund
from distutils.util import strtobool
from flask import request


def get_rounds_for_fund(fund_id: str):
    """python function to return all rounds in a given fund, by fund_id

    :param fund_id: fund_id to search rounds for given fund
    :type fund_id: str
    :return: Tuple containing the list of rounds for a given
                fund_id and response code
    :rtype: Tuple
    """
    language = request.args.get("language")
    round_data.ROUNDS_DAO.load_data(round_data.get_round_data(language))
    fund_data.FUNDS_DAO.load_data(fund_data.get_fund_data(language))
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)
    rounds = []
    if use_short_name:
        fund_search = fund_data.FUNDS_DAO.search_by_short_name(fund_id)
        if fund_search:
            rounds = round_data.ROUNDS_DAO.get_all_for_fund(fund_search["id"])
    else:
        rounds = round_data.ROUNDS_DAO.get_all_for_fund(fund_id)

    if len(rounds) > 0:
        return rounds, 200
    else:
        return {
            "code": 404,
            "message": f"fund_id : {fund_id} cannot be found"
            if not use_short_name
            else f"short_name {fund_id} cannot be found",
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
    round_data.ROUNDS_DAO.load_data(round_data.get_round_data(language))
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)
    if use_short_name:
        fund = get_fund(fund_id)[0]
        round_search = round_data.ROUNDS_DAO.search_by_round_short_name(round_id, fund)
    else:
        round_search = round_data.ROUNDS_DAO.get_one(fund_id, round_id, language)
    if isinstance(round_search, dict):
        return round_search, 200
    else:
        return {
            "code": 404,
            "message": f"round_id : {round_id} in fund_id : {fund_id} cannot be found.",
        }, 404
