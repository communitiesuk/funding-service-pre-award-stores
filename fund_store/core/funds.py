"""
Python functions to return responses of funds from our GET requests
"""
import warnings
from typing import List
from typing import Tuple

from connexion import NoContent
from core.data_operations import fund_data


def search(to_search: dict, word_list: List[str]):
    """A dummy search function. Very inefficient,
    testing only please.
    Args:
        to_search (dict): A dictionary of funds.
        word_list (List[str]): A list of words to search for.
    Returns:
        _type_: A list of matching funds.
    """
    warnings.warn(
        "Search function used in the fund store shouldn't be used in"
        " production",
        DeprecationWarning,
    )
    return_list = []
    for fund_info in to_search:
        word_found = False
        for data_point in fund_info:
            for word in word_list:
                if word in fund_info[data_point]:
                    return_list.append(fund_info)
                    word_found = True
                    break
            if word_found:
                break

    return return_list


def get_funds(search_items=None) -> Tuple:
    """python function to return all funds or a filtered list
        of funds via search function

    :param search_items: List of strings to search for, defaults to None
    :type search_items: List[str], optional
    :return: Tuple containing the list of (filtered) funds and status code
    :rtype: Tuple
    """
    funds = fund_data.FUNDS_DUMMY_DAO.get_all()
    if search_items is None:
        if type(funds) == list:
            return funds, 200
        else:
            return NoContent, 404
    else:
        return search(funds, search_items), 200


def get_fund(fund_id: str) -> Tuple:
    """python function to return a single specified fund from a fund_id

    :param fund_id: String value of the fund_id
    :type fund_id: str
    :return: Tuple of single fund filtered by the unique
                fund_id and response code
    :rtype: Tuple
    """
    fund_search = fund_data.FUNDS_DUMMY_DAO.get_one(fund_id)
    if type(fund_search) == dict:
        return fund_data.FUNDS_DUMMY_DAO.get_one(fund_id), 200
    else:
        return NoContent, 404
