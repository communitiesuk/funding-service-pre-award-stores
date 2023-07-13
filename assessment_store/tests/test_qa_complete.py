import pytest
from db.queries.qa_complete.queries import create_qa_complete_record
from tests._helpers import get_assessment_record
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_qa_complete_record_for_application(
    _db, seed_application_records
):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    user_id = "test_user"

    qa_complete_record_metadata = create_qa_complete_record(
        application_id, user_id
    )

    assert len(qa_complete_record_metadata) == 4
    assert qa_complete_record_metadata["date_created"]
    assert qa_complete_record_metadata["user_id"] == "test_user"


# @pytest.mark.apps_to_insert([test_input_data[0]])
# def test_get_latest_score_for_application_sub_crit(seed_application_records):
#     """test_get_latest_score_for_application_sub_crit Tests we can add
#     score records in the scores table and return the most recently created."""

#     picked_row = get_assessment_record(
#         seed_application_records[0]["application_id"]
#     )
#     application_id = picked_row.application_id
#     sub_criteria_id = "app-info"

#     assessment_payload = {
#         "application_id": application_id,
#         "sub_criteria_id": sub_criteria_id,
#         "score": 5,
#         "justification": "great",
#         "user_id": "test",
#     }
#     create_score_metadata = create_score_for_app_sub_crit(**assessment_payload)

#     score_metadata = get_scores_for_app_sub_crit(
#         application_id, sub_criteria_id
#     )
#     latest_score_metadata = score_metadata[0]

#     assert latest_score_metadata["date_created"] == create_score_metadata.get(
#         "date_created"
#     )
#     assert latest_score_metadata["score"] == create_score_metadata.get("score")
#     assert latest_score_metadata["justification"] == create_score_metadata.get(
#         "justification"
#     )
