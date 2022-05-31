from connexion import NoContent
from core.data_operations import fund_data

# from flask import request


def get_funds():
    return fund_data.FUNDS_DUMMY_DAO.get_all()


def get_fund(fund_id: str):
    fund_search = fund_data.FUNDS_DUMMY_DAO.get_one(fund_id)
    if type(fund_search) == dict:
        return fund_data.FUNDS_DUMMY_DAO.get_one(fund_id)
    else:
        return NoContent, 404
