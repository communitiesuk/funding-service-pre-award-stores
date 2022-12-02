import random

import sqlalchemy
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.queries.assessment_records import find_answer_by_key_runner
from tests._helpers import get_random_row
import time
from db import db

from db.queries.scores.queries import create_just_score_for_application_sub_crit
from db.queries.scores.queries import get_latest_just_score_for_application_sub_crit


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


def test_create_scores_for_application_su_crit():
    picked_row = get_random_row(AssessmentRecord)
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"
    
    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test"
    }
    score_metadata = create_just_score_for_application_sub_crit(**assessment_payload)

    assert len(score_metadata) == 7
    assert score_metadata.get("date_created")
    assert score_metadata.get("score") == 3


def test_scores_for_application_sub_crit():
    picked_row = get_random_row(AssessmentRecord)
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test"
    }
    score_metadata = create_just_score_for_application_sub_crit(**assessment_payload)

    latest_score_metadata = get_latest_just_score_for_application_sub_crit(application_id, sub_criteria_id)

    assert latest_score_metadata.get("date_created") == score_metadata.get("date_created")
    assert latest_score_metadata.get("score") == score_metadata.get("score")
    assert latest_score_metadata.get("justification") == score_metadata.get("justification")
