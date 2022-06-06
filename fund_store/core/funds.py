from connexion import NoContent
from core.data_operations import fund_data


def get_funds():
    list_of_funds = fund_data.FUNDS_DUMMY_DAO.get_all()
    if type(list_of_funds) == list:
        return list_of_funds, 200
    else:
        return NoContent, 404


def get_fund(fund_id: str):
    fund_search = fund_data.FUNDS_DUMMY_DAO.get_one(fund_id)
    if type(fund_search) == dict:
        return fund_data.FUNDS_DUMMY_DAO.get_one(fund_id), 200
    else:
        return NoContent, 404
