# flake8: noqa
from db.models.flags.enums import FlagType
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags.queries import retrieve_flags_for_applications
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


def get_flags_for_application(application_id: str) -> list:
    flags = retrieve_flags_for_applications([application_id])
    return flags
