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
