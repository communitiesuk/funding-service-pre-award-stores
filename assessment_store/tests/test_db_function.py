import random

import sqlalchemy

from db.models.assessment_record.assessment_records import AssessmentRecord
from db.queries.assessment_records import find_answer_by_key_runner
from db.queries.assessment_records.queries import find_assessor_task_list_state
from tests._helpers import get_random_row


def test_select_field_by_id():
    """test_select_field_by_id Tests that the correct field is picked from the
    corresponding application."""
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
    """test_jsonb_blob_immutable Tests that attempting to update a json blob
    though the sqlalchemy interface raises an error.

    Error is defined in `db.models.assessment_record.db_triggers`.
    """

    picked_row = get_random_row(AssessmentRecord)
    picked_row.jsonb_blob = {"application": "deleted :( oops"}

    try:
        db_session.commit()
    except sqlalchemy.exc.InternalError as error:
        assert "Cannot mutate application json" in str(error)
    else:
        assert False


def test_non_blob_columns_mutable(db_session):
    """test_non_blob_columns_mutable Tests we haven't made the whole table
    immutable by accident when making the json blob immutable."""

    try:
        picked_row = get_random_row(AssessmentRecord)
        picked_row.workflow_status = "IN_PROGRESS"
        db_session.commit()
    except sqlalchemy.exc.InternalError:
        raise AssertionError


def test_find_assessor_task_list_ui_metadata():
    """test_find_assessor_task_list_ui_metadata Tests that the correct metadata
    is returned for the assessor task list UI."""

    metadata = find_assessor_task_list_state(
        "a3ec41db-3eac-4220-90db-c92dea049c00"
    )
    assert metadata == {
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "project_name": "Mock that is used to test Assessors Task List",
        "round_id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "workflow_status": "NOT_STARTED",
        "date_submitted": "2022-10-27T08:32:13.383999",
        "project_reference": "COF-R2W2-JWBTLN",
    }
