import random

import sqlalchemy

from db.models.assessment_record.assessment_records import AssessmentRecord
from db.queries.assessment_records import find_answer_by_key_runner
from db.queries.assessment_records.queries import find_assessor_task_list_state
from tests._helpers import get_random_row
import time
from db import db

from db.queries.scores.queries import create_score_for_app_sub_crit
from db.queries.scores.queries import get_scores_for_app_sub_crit


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


def test_create_scores_for_application_sub_crit():
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

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
    score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    assert len(score_metadata) == 7
    assert score_metadata["date_created"]
    assert score_metadata["score"] == 3


def test_get_latest_score_for_application_sub_crit():
    """test_get_latest_score_for_application_sub_crit Tests we can add
    score records in the scores table and return the most recently created."""

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
    create_score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    score_metadata = get_scores_for_app_sub_crit(application_id, sub_criteria_id)
    latest_score_metadata = score_metadata[0]

    assert latest_score_metadata["date_created"] == create_score_metadata.get("date_created")
    assert latest_score_metadata["score"] == create_score_metadata.get("score")
    assert latest_score_metadata["justification"] == create_score_metadata.get("justification")


def test_get_score_history():
    """test_get_score_history Tests we can get all score 
    records in the scores table """
    
    picked_row = get_random_row(AssessmentRecord)
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test"
    }
    create_score_metadata_1 = create_score_for_app_sub_crit(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test"
    }
    create_score_metadata_2 = create_score_for_app_sub_crit(**assessment_payload_2)
    
    score_metadata = get_scores_for_app_sub_crit(application_id, sub_criteria_id, True)

    assert len(score_metadata) == 2
    assert score_metadata[0]["score"] == create_score_metadata_1["score"]
    assert score_metadata[1]["justification"] == create_score_metadata_2["justification"]


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
