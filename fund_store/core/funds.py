from core.data_operations import fund_data
import warnings
from typing import List

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
    for fund_data in to_search:
        word_found = False
        for data_point in fund_data:
            for word in word_list:
                if word in fund_data[data_point]:
                    return_list.append(fund_data)
                    word_found = True
                    break
            if word_found:
                break

    return return_list

def get_funds(search_items = None):
    list_of_funds = fund_data.FUNDS_DUMMY_DAO.get_all()
    if search_items is None:
        if isinstance(list_of_funds, list):
            return list_of_funds, 200
        else:
            return {"code" : 404, "message" : "No funds exist."}, 404   
    else:
        return search(list_of_funds, search_items), 200

def get_fund(fund_id: str):
    fund_search = fund_data.FUNDS_DUMMY_DAO.get_one(fund_id)
    if isinstance(fund_search, dict):
        return fund_data.FUNDS_DUMMY_DAO.get_one(fund_id), 200
    else:
        return {"code" : 404, "message" : f"fund_id : {fund_id} cannot be found."}, 404
