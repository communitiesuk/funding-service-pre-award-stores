# flake8: noqa
from db.models.flags.enums import FlagType
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags.queries import find_qa_complete_flag
from db.queries.flags.queries import retrieve_flag_for_application
from flask import request


def post_flag_for_application() -> dict:
    args = request.get_json()
    created_flag = create_flag_for_application(
        justification=args["justification"],
        section_to_flag=args["section_to_flag"],
        application_id=args["application_id"],
        user_id=args["user_id"],
        flag_type=FlagType[args["flag_type"]],
    )

    return created_flag


def get_latest_flag_for_application(application_id: str) -> list:
    flag = retrieve_flag_for_application(application_id)
    is_qa_complete = find_qa_complete_flag(application_id)
    return flag | is_qa_complete if flag else {}
