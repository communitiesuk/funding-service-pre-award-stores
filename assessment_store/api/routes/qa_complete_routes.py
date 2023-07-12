# flake8: noqa
<<<<<<< HEAD

from db.queries.qa_complete.queries import create_qa_complete_record
from db.queries.qa_complete.queries import get_qa_complete_record_for_application

=======
from db.models.flags.enums import FlagType
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags.queries import find_qa_complete_flag
from db.queries.flags.queries import retrieve_all_flags_for_application
from db.queries.flags.queries import retrieve_flag
from db.queries.flags.queries import retrieve_flag_for_application
from db.queries.qa_complete.queries import create_qa_complete_record
from db.queries.qa_complete.queries import get_all_qa_complete_records
from flask import request

>>>>>>> 030b00ca3c6e3d39c8cd6e2cddd396cbf2ffeca1

def post_qa_complete_for_application(
    application_id: str, user_id: str
) -> dict:
    created_qa_complete_record = create_qa_complete_record(
        application_id=application_id,
        user_id=user_id,
    )

    return created_qa_complete_record


<<<<<<< HEAD
def qa_complete_record_for_application(
        application_id: str
) -> dict:
    qa_complete_record = get_qa_complete_record_for_application(application_id)

    return qa_complete_record
=======
def all_qa_complete_records() -> list:
    qa_complete_records = get_all_qa_complete_records()

    return qa_complete_records
>>>>>>> 030b00ca3c6e3d39c8cd6e2cddd396cbf2ffeca1
