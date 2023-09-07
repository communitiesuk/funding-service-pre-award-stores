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
from db.schemas.section import SECTION_SCHEMA_MAP
from distutils.util import strtobool
from flask import abort
from flask import current_app
from flask import request
from fsd_utils.locale_selector.get_lang import get_lang


def filter_fund_by_lang(fund_data, lang_key: str = "en"):
    def filter_fund(data):
        data["name"] = data["name_json"].get(lang_key) or data["name_json"]["en"]
        data["title"] = data["title_json"].get(lang_key) or data["title_json"]["en"]
        data["description"] = (
            data["description_json"].get(lang_key) or data["description_json"]["en"]
        )
        return data

    if isinstance(fund_data, dict):
        fund = filter_fund(fund_data)
    elif isinstance(fund_data, list):
        fund = [filter_fund(item) for item in fund_data]
    else:
        fund = fund_data

    return fund


def filter_round_by_lang(round_data, lang_key: str = "en"):
    def filter_round(data):
        data["title"] = data["title_json"].get(lang_key) or data["title_json"]["en"]
        return data

    if isinstance(round_data, dict):
        round = filter_round(round_data)
    elif isinstance(round_data, list):
        round = [filter_round(item) for item in round_data]
    else:
        round = round_data

    return round


def get_funds():
    language = request.args.get("language", "en").replace("?", "")
    funds = get_all_funds()

    if funds:
        serialiser = FundSchema()
        return filter_fund_by_lang(
            fund_data=serialiser.dump(funds, many=True), lang_key=language
        )

    current_app.logger.warn("No funds were found, please check this.")
    return []


def get_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id)
    else:
        fund = get_fund_by_id(fund_id)

    if fund:
        serialiser = FundSchema()
        return filter_fund_by_lang(fund_data=serialiser.dump(fund), lang_key=language)

    abort(404)


def get_round(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        round = get_round_by_short_name(fund_id, round_id)
    else:
        round = get_round_by_id(fund_id, round_id)
    if round:
        serialiser = RoundSchema()
        return filter_round_by_lang(
            round_data=serialiser.dump(round), lang_key=language
        )

    abort(404)


def get_rounds_for_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        rounds = get_rounds_for_fund_by_short_name(fund_id)
    else:
        rounds = get_rounds_for_fund_by_id(fund_id)

    if rounds:
        serialiser = RoundSchema()
        dumped = [serialiser.dump(r) for r in rounds]
        return filter_round_by_lang(round_data=dumped, lang_key=language)

    abort(404)


def get_sections_for_round_application(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    sections = get_application_sections_for_round(fund_id, round_id)
    if sections:
        section_schema = SECTION_SCHEMA_MAP.get(language)
        serialiser = section_schema()
        dumped = serialiser.dump(sections, many=True)
        return dumped
    abort(404)


def get_sections_for_round_assessment(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    sections = get_assessment_sections_for_round(fund_id, round_id, get_lang())
    if sections:
        section_schema = SECTION_SCHEMA_MAP.get(language)
        serialiser = section_schema()
        return serialiser.dump(sections, many=True)

    abort(404)


def get_available_flag_allocations(fund_id, round_id):
    # TODO: Currently teams are hardcoded, move it to database implementation
    from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_1_ID
    from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_2_ID
    from config.fund_loader_config.cof.cof_r3 import COF_FUND_ID
    from config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_2_ID
    from config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_3_ID
    from config.fund_loader_config.night_shelter.ns_r2 import NIGHT_SHELTER_ROUND_2_ID
    from config.fund_loader_config.night_shelter.ns_r2 import NIGHT_SHELTER_FUND_ID

    cof_teams = [
        {"key": "ASSESSOR", "value": "Assessor"},
        {"key": "COMMERCIAL_ASSESSOR", "value": "Commercial Assessor"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
        {"key": "LEAD_COMMERCIAL_ASSESSOR", "value": "Lead Commercial Assessor"},
        {"key": "COF_POLICY", "value": "COF Policy"},
    ]

    nstf_teams = [
        {"key": "COMMERCIAL", "value": "Commercial"},
        {"key": "NSTF_TEAM", "value": "NSTF Team"},
        {"key": "HOUSING_JUSTICE", "value": "Housing Justice"},
        {"key": "HOMELESS_LINK", "value": "Homeless Link"},
        {"key": "RS_ADVISORS", "value": "RS Advisors"},
    ]

    if fund_id == COF_FUND_ID and round_id == COF_ROUND_2_WINDOW_2_ID:
        return cof_teams
    elif fund_id == COF_FUND_ID and round_id == COF_ROUND_2_WINDOW_3_ID:
        return cof_teams
    elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_1_ID:
        return cof_teams
    elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_2_ID:
        return cof_teams
    elif fund_id == NIGHT_SHELTER_FUND_ID and round_id == NIGHT_SHELTER_ROUND_2_ID:
        return nstf_teams
    else:
        abort(404)
