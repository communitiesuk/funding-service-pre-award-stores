import random

import sqlalchemy
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.queries.assessment_records import find_answer_by_key_runner
from tests._helpers import get_random_row


def test_select_field_by_id():

    picked_row = get_random_row(AssessmentRecord)

    # We pick a random row to extract some data from.
    picked_app_id = picked_row.application_id

    picked_questions = random.choice(picked_row.jsonb_blob["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_runner(picked_key, picked_app_id)[0]

    assert field_found == picked_field


def test_jsonb_blob_immutable(db_session):

    picked_row = get_random_row(AssessmentRecord)
    picked_row.jsonb_blob = {"application": "deleted :( oops"}

    try:
        db_session.commit()
    except sqlalchemy.exc.InternalError as error:
        assert "Cannot mutate application json" in str(error)
    else:
        assert False


def test_non_blob_columns_mutable(db_session):

    try:
        picked_row = get_random_row(AssessmentRecord)
        picked_row.workflow_status = "IN_PROGRESS"
        db_session.commit()
    except sqlalchemy.exc.InternalError as error:
        raise AssertionError