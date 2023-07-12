# flake8: noqa
from db.models.flags.enums import FlagType
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags.queries import find_qa_complete_flag
from db.queries.flags.queries import retrieve_all_flags_for_application
from db.queries.flags.queries import retrieve_flag
from db.queries.flags.queries import retrieve_flag_for_application
from db.queries.qa_complete.queries import create_qa_complete_record
from db.queries.qa_complete.queries import get_all_qa_complete_records
from flask import request


def post_qa_complete_for_application(
    application_id: str, user_id: str
) -> dict:
    created_qa_complete_record = create_qa_complete_record(
        application_id=application_id,
        user_id=user_id,
    )

    return created_qa_complete_record


def all_qa_complete_records() -> list:
    qa_complete_records = get_all_qa_complete_records()

    return qa_complete_records
