from db.queries import get_all_funds
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from db.queries import get_rounds_for_fund_by_id
from db.queries import get_rounds_for_fund_by_short_name
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
from db.schemas.section import SectionSchema
from distutils.util import strtobool
from flask import abort
from flask import request
from fsd_utils.locale_selector.get_lang import get_lang


def get_funds():
    # language = request.args.get("language")

    funds = get_all_funds()

    if funds:
        serialiser = FundSchema()
        return serialiser.dump(funds, many=True)

    abort(404)


def get_fund(fund_id):
    # language = request.args.get("language")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id)
    else:
        fund = get_fund_by_id(fund_id)

    if fund:
        serialiser = FundSchema()
        return serialiser.dump(fund)

    abort(404)


def get_round(fund_id, round_id):
    # language = request.args.get("language")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        round = get_round_by_short_name(fund_id, round_id)
    else:
        round = get_round_by_id(fund_id, round_id)
    if round:
        serialiser = RoundSchema()
        return serialiser.dump(round)

    abort(404)


def get_rounds_for_fund(fund_id):
    # language = request.args.get("language")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        rounds = get_rounds_for_fund_by_short_name(fund_id)
    else:
        rounds = get_rounds_for_fund_by_id(fund_id)

    if rounds:
        serialiser = RoundSchema()
        return serialiser.dump(rounds, many=True)

    abort(404)


def get_sections_for_round_application(fund_id, round_id):
    sections = get_application_sections_for_round(fund_id, round_id)
    if sections:
        serialiser = SectionSchema()
        return serialiser.dump(sections, many=True)

    abort(404)


def get_sections_for_round_assessment(fund_id, round_id):
    sections = get_assessment_sections_for_round(fund_id, round_id, get_lang())
    if sections:
        serialiser = SectionSchema()
        return serialiser.dump(sections, many=True)

    abort(404)
