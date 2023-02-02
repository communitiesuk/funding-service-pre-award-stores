"""
Python functions to return responses of funds from our GET requests
"""
from core.data_operations import fund_data
from flask import request


def get_funds():
    """python function to return all funds
    :type search_items: List[str], optional
    :return: Tuple containing the list of funds and status code
    :rtype: Tuple
    """
    language = request.args.get("language")
    fund_data.FUNDS_DAO.load_data(fund_data.get_fund_data(language))
    list_of_funds = fund_data.FUNDS_DAO.get_all()
    if isinstance(list_of_funds, list):
        return list_of_funds, 200
    else:
        return {"code": 404, "message": "No funds exist."}, 404


def get_fund(fund_id: str):
    """python function to return a single specified fund from a fund_id

    :param fund_id: String value of the fund_id
    :type fund_id: str
    :return: Tuple of single fund filtered by the unique
                fund_id and response code
    :rtype: Tuple
    """
    language = request.args.get("language")
    fund_data.FUNDS_DAO.load_data(fund_data.get_fund_data(language))
    fund_search = fund_data.FUNDS_DAO.get_one(fund_id, language)
    if isinstance(fund_search, dict):
        return fund_search, 200
    else:
        return {
            "code": 404,
            "message": f"fund_id : {fund_id} cannot be found.",
        }, 404
