# flake8: noqa

from db.queries.qa_complete.queries import create_qa_complete_record
from db.queries.qa_complete.queries import get_qa_complete_record_for_application


def post_qa_complete_for_application(
    application_id: str, user_id: str
) -> dict:
    created_qa_complete_record = create_qa_complete_record(
        application_id=application_id,
        user_id=user_id,
    )

    return created_qa_complete_record


def qa_complete_record_for_application(
        application_id: str
) -> dict:
    qa_complete_record = get_qa_complete_record_for_application(application_id)

    return qa_complete_record
