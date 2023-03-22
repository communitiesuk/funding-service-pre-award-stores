import random

import pytest
import sqlalchemy
from db.models import Comment
from db.models import Score
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.models.assessment_record.enums import Status
from db.models.comment.enums import CommentType
from db.queries import find_answer_by_key_runner
from db.queries.assessment_records.queries import (
    bulk_update_location_jsonb_blob,
)
from db.queries.assessment_records.queries import find_assessor_task_list_state
from db.queries.comments.queries import create_comment_for_application_sub_crit
from db.queries.comments.queries import get_comments_for_application_sub_crit
from tests._helpers import get_assessment_record
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_select_field_by_id(seed_application_records):
    """test_select_field_by_id Tests that the correct field is picked from the
    corresponding application."""
    picked_row = seed_application_records[0]

    # We pick a random row to extract some data from.
    picked_app_id = picked_row["application_id"]

    picked_questions = random.choice(picked_row["jsonb_blob"]["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_runner(picked_key, picked_app_id)[0]

    assert field_found == picked_field


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_jsonb_blob_immutable(_db, seed_application_records):
    """test_jsonb_blob_immutable Tests that attempting to update a json blob
    though the sqlalchemy interface raises an error.

    Error is defined in `db.models.assessment_record.db_triggers`.
    """

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    picked_row.jsonb_blob = {"application": "deleted :( oops"}

    try:
        with pytest.raises(sqlalchemy.exc.InternalError) as excinfo:

            _db.session.commit()
        assert "Cannot mutate application json" in str(excinfo.value)
    finally:
        _db.session.rollback()


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_non_blob_columns_mutable(_db, seed_application_records):
    """test_non_blob_columns_mutable Tests we haven't made the whole table
    immutable by accident when making the json blob immutable."""

    try:
        picked_row = get_assessment_record(
            seed_application_records[0]["application_id"]
        )
        picked_row.workflow_status = "IN_PROGRESS"
        _db.session.commit()
    except sqlalchemy.exc.InternalError:
        raise AssertionError
    finally:
        _db.session.rollback()


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_find_assessor_task_list_ui_metadata(seed_application_records):
    """test_find_assessor_task_list_ui_metadata Tests that the correct metadata
    is returned for the assessor task list UI."""

    metadata = find_assessor_task_list_state(
        seed_application_records[0]["application_id"]
    )
    assert metadata == {
        "fund_id": seed_application_records[0]["fund_id"],
        "project_name": "Mock that is used to test Assessors Task List",
        "short_id": "COF-R2W2-JWBTLN",
        "round_id": seed_application_records[0]["round_id"],
        "workflow_status": "NOT_STARTED",
        "date_submitted": "2022-10-27T08:32:13.383999",
        "funding_amount_requested": 4600.00,
    }


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_post_comment(seed_application_records):
    """test_post_comment tests we can create
    comment records in the comments table."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": "something",
    }
    comment_metadata = create_comment_for_application_sub_crit(
        **assessment_payload
    )

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == "test"
    assert comment_metadata["theme_id"] == "something"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_comments(seed_application_records):
    """test_get_comments tests we can get all comment
    records in the comments table filtered by application_id,
    subcriteria_id and theme_id"""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"
    theme_id = "theme"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": theme_id,
    }
    create_comment_for_application_sub_crit(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": theme_id,
    }
    create_comment_for_application_sub_crit(**assessment_payload_2)

    assessment_payload_3 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": "different theme",
    }
    create_comment_for_application_sub_crit(**assessment_payload_3)

    comment_metadata_for_theme = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id
    )
    assert len(comment_metadata_for_theme) == 2
    assert (
        comment_metadata_for_theme[0]["theme_id"]
        == comment_metadata_for_theme[1]["theme_id"]
    )

    comment_metadata_no_theme = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id=None
    )
    assert len(comment_metadata_no_theme) == 3

    # TODO: remove this once frontend is updated not to use 'theme_id=score'
    comment_metadata_score_theme_id = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id="score"
    )
    assert len(comment_metadata_score_theme_id) == 3


@pytest.mark.parametrize(
    "insertion_object",
    [
        Score(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            score=5,
            justification="great",
        ),
        Comment(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            comment="great",
            comment_type=CommentType.COMMENT,
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_update_workflow_status_on_insert(
    _db, insertion_object, seed_application_records
):
    application_id = seed_application_records[0]["application_id"]
    assessment_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .first()
    )

    assert assessment_record.workflow_status == Status.NOT_STARTED

    insertion_object.application_id = application_id
    _db.session.add(insertion_object)
    _db.session.commit()

    assert assessment_record.workflow_status == Status.IN_PROGRESS


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_bulk_update_location_data(_db, seed_application_records):
    application_id = seed_application_records[0]["application_id"]

    test_random_append = random.randint(999, 99999)

    location = {
        "error": False,
        "county": f"test_county_{test_random_append}",
        "country": f"test_country_{test_random_append}",
    }

    application_ids_to_location_data = [
        {"application_id": application_id, "location": location}
    ]

    bulk_update_location_jsonb_blob(application_ids_to_location_data)

    assessment_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .first()
    )
    assert location == assessment_record.location_json_blob
