import uuid
from distutils.util import strtobool

from flask import abort
from flask import current_app
from flask import jsonify
from flask import request
from fsd_utils.locale_selector.get_lang import get_lang

from db import db
from db.models import Round
from db.queries import get_all_funds
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import get_event as get_event_from_db
from db.queries import get_events_for_round as get_events_for_round_from_db
from db.queries import get_fund_by_id
from db.queries import get_fund_by_short_name
from db.queries import get_round_by_id
from db.queries import get_round_by_short_name
from db.queries import get_rounds_for_fund_by_id
from db.queries import get_rounds_for_fund_by_short_name
from db.queries import set_event_to_processed as set_event_to_processed_in_db
from db.schemas.event import EventSchema
from db.schemas.fund import FundSchema
from db.schemas.round import RoundSchema
from db.schemas.section import SECTION_SCHEMA_MAP


def is_valid_uuid(value):
    try:
        obj = uuid.UUID(value)
        return str(obj) == value.lower()
    except Exception:
        return False


def filter_fund_by_lang(fund_data, lang_key: str = "en"):
    def filter_fund(data):
        data["name"] = data["name_json"].get(lang_key) or data["name_json"]["en"]
        data["title"] = data["title_json"].get(lang_key) or data["title_json"]["en"]
        data["description"] = data["description_json"].get(lang_key) or data["description_json"]["en"]
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
        data["contact_us_banner"] = (
            data["contact_us_banner_json"].get(lang_key) or data["contact_us_banner_json"].get("en")
            if data["contact_us_banner_json"]
            else ""
        )
        data["instructions"] = (
            data["instructions_json"].get(lang_key) or data["instructions_json"].get("en")
            if data["instructions_json"]
            else ""
        )
        data["application_guidance"] = (
            data["application_guidance_json"].get(lang_key) or data["application_guidance_json"].get("en")
            if data["application_guidance_json"]
            else ""
        )
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
        return jsonify(filter_fund_by_lang(fund_data=serialiser.dump(funds, many=True), lang_key=language))
    current_app.logger.warning("No funds were found, please check this.")
    return jsonify(funds)


def get_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id) if fund_id else None
    else:
        fund = get_fund_by_id(fund_id) if is_valid_uuid(fund_id) else None

    if fund:
        serialiser = FundSchema()
        return jsonify(filter_fund_by_lang(fund_data=serialiser.dump(fund), lang_key=language))

    abort(404)


def get_round_from_db(fund_id, round_id) -> Round:
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        round = get_round_by_short_name(fund_id, round_id)
    else:
        round = get_round_by_id(fund_id, round_id) if is_valid_uuid(fund_id) and is_valid_uuid(round_id) else None
    return round


def get_round(fund_id, round_id):
    round = get_round_from_db(fund_id, round_id)
    language = request.args.get("language", "en").replace("?", "")
    if round:
        serialiser = RoundSchema()
        return filter_round_by_lang(round_data=serialiser.dump(round), lang_key=language)

    abort(404)


def get_eoi_deicision_schema_for_round(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "").lower()
    round = get_round_from_db(fund_id=fund_id, round_id=round_id)
    if not round:
        abort(404)

    if not round.eoi_decision_schema:
        return {}

    return round.eoi_decision_schema.get(language) or {}


def get_rounds_for_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        rounds = get_rounds_for_fund_by_short_name(fund_id)
    else:
        rounds = get_rounds_for_fund_by_id(fund_id) if is_valid_uuid(fund_id) else None

    if rounds:
        serialiser = RoundSchema()
        dumped = [serialiser.dump(r) for r in rounds]
        return filter_round_by_lang(round_data=dumped, lang_key=language)

    abort(404)


def get_sections_for_round_application(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        sections = get_application_sections_for_round(fund_id, round_id)
        if sections:
            section_schema = SECTION_SCHEMA_MAP.get(language)
            serialiser = section_schema()
            dumped = serialiser.dump(sections, many=True)
            return dumped
    abort(404)


def get_sections_for_round_assessment(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        sections = get_assessment_sections_for_round(fund_id, round_id, get_lang())
        if sections:
            section_schema = SECTION_SCHEMA_MAP.get(language)
            serialiser = section_schema()
            return serialiser.dump(sections, many=True)

    abort(404)


def get_events_for_round(fund_id, round_id):
    only_unprocessed = request.args.get("only_unprocessed", False, type=lambda x: x.lower() == "true")
    if is_valid_uuid(round_id):
        events = get_events_for_round_from_db(round_id=round_id, only_unprocessed=only_unprocessed)
        if events:
            serialiser = EventSchema()
            return serialiser.dump(events, many=True)
    abort(404)


def get_event(fund_id, round_id, event_id):
    if is_valid_uuid(event_id) and is_valid_uuid(round_id):
        event = get_event_from_db(round_id=round_id, event_id=event_id)
        if event:
            serialiser = EventSchema()
            return serialiser.dump(event)
    abort(404)


def set_event_to_processed(fund_id, round_id, event_id):
    processed = request.args.get("processed", type=lambda x: x.lower() == "true")
    if is_valid_uuid(event_id) and is_valid_uuid(round_id):
        event = set_event_to_processed_in_db(round_id=round_id, event_id=event_id, processed=processed)
        if event:
            serialiser = EventSchema()
            return jsonify(serialiser.dump(event))
    abort(404)


def get_available_flag_allocations(fund_id, round_id):
    # TODO: Currently teams are hardcoded, move it to database implementation
    from config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_2_ID
    from config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_3_ID
    from config.fund_loader_config.cof.cof_r3 import COF_FUND_ID
    from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_1_ID
    from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_2_ID
    from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_3_ID
    from config.fund_loader_config.cof.cof_r4 import COF_ROUND_4_WINDOW_1_ID
    from config.fund_loader_config.cyp.cyp_r1 import CYP_FUND_ID
    from config.fund_loader_config.cyp.cyp_r1 import CYP_ROUND_1_ID
    from config.fund_loader_config.digital_planning.dpi_r2 import DPI_FUND_ID
    from config.fund_loader_config.digital_planning.dpi_r2 import DPI_ROUND_2_ID
    from config.fund_loader_config.night_shelter.ns_r2 import NIGHT_SHELTER_FUND_ID
    from config.fund_loader_config.night_shelter.ns_r2 import NIGHT_SHELTER_ROUND_2_ID

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

    cyp_teams = [
        {"key": "COMMERCIAL_ASSESSOR", "value": "Commercial Assessor"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
    ]

    dpif_teams = [
        {"key": "ELIGIBILITY", "value": "Eligibility"},
        {"key": "MODERATION", "value": "Moderation"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
    ]
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        if fund_id == COF_FUND_ID and round_id in COF_ROUND_2_WINDOW_2_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_2_WINDOW_3_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_1_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_2_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_3_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_4_WINDOW_1_ID:
            return cof_teams
        elif fund_id == NIGHT_SHELTER_FUND_ID and round_id == NIGHT_SHELTER_ROUND_2_ID:
            return nstf_teams
        elif fund_id == CYP_FUND_ID and round_id == CYP_ROUND_1_ID:
            return cyp_teams
        elif fund_id == DPI_FUND_ID and round_id == DPI_ROUND_2_ID:
            return dpif_teams
    abort(404)


def update_application_reminder_sent_status(round_id):
    try:
        status = request.args.get("status")
        round_instance = Round.query.filter_by(id=round_id).first() if is_valid_uuid(round_id) else None

        if not round_instance:
            return jsonify({"message": "Round ID not found"}), 404
        reminder_status = round_instance.application_reminder_sent

        if status.lower() == "true" and reminder_status is False:
            round_instance.application_reminder_sent = True
            db.session.commit()
            current_app.logger.info(
                {f"application_reminder_sent status has been updated to True for round {round_id}"}
            ), 200
            return (
                jsonify({"message": f"application_reminder_sent status has been updated to True for round {round_id}"}),
                200,
            )
        else:
            return (
                jsonify({"message": "application_reminder_sent Status should be True"}),
                400,
            )

    except Exception as e:
        current_app.logger.error(f"The application_reminder_sent status could not be updated {e}"), 400
        return (
            jsonify({"message": f"The application_reminder_sent status could not be updated for round_id {round_id}"}),
            400,
        )
