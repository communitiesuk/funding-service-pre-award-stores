import datetime
import uuid
from unittest.mock import MagicMock

import pytest
from api.routes.progress_routes import get_progress_for_applications
from db.models import Score
from db.queries.scores.queries import create_score_for_app_sub_crit
from db.queries.scores.queries import get_scores_for_app_sub_crit
from db.queries.scores.queries import get_sub_criteria_to_latest_score_map
from tests._helpers import get_assessment_record
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_scores_for_application_sub_crit(_db, seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    assert len(score_metadata) == 7
    assert score_metadata["date_created"]
    assert score_metadata["score"] == 3


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_latest_score_for_application_sub_crit(seed_application_records):
    """test_get_latest_score_for_application_sub_crit Tests we can add
    score records in the scores table and return the most recently created."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    score_metadata = get_scores_for_app_sub_crit(
        application_id, sub_criteria_id
    )
    latest_score_metadata = score_metadata[0]

    assert latest_score_metadata["date_created"] == create_score_metadata.get(
        "date_created"
    )
    assert latest_score_metadata["score"] == create_score_metadata.get("score")
    assert latest_score_metadata["justification"] == create_score_metadata.get(
        "justification"
    )


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_score_history(seed_application_records):
    """test_get_score_history Tests we can get all score
    records in the scores table"""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_metadata_1 = create_score_for_app_sub_crit(
        **assessment_payload_1
    )

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_metadata_2 = create_score_for_app_sub_crit(
        **assessment_payload_2
    )

    score_metadata = get_scores_for_app_sub_crit(
        application_id, sub_criteria_id, True
    )

    assert len(score_metadata) == 2
    assert score_metadata[0]["score"] == create_score_metadata_2["score"]
    assert (
        score_metadata[1]["justification"]
        == create_score_metadata_1["justification"]
    )


@pytest.mark.apps_to_insert(test_input_data)
def test_get_progress_for_applications(seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    application_id_1 = seed_application_records[0]["application_id"]
    application_id_2 = seed_application_records[1]["application_id"]
    sub_criteria_ids = ["benefits", "engagement"]

    score_payload_1 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[0],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_1)

    score_payload_2 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_2)

    score_payload_3 = {
        "application_id": application_id_2,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_3)

    request = MagicMock()
    request.get_json.return_value = {
        "application_ids": [
            application_id_1,
            application_id_2,
        ]
    }
    application_progress_list = get_progress_for_applications(
        [application_id_1, application_id_2]
    )

    assert len(application_progress_list) == 2
    for application in application_progress_list:
        if application["application_id"] == application_id_1:
            assert application["progress"] == 20
        if application["application_id"] == application_id_2:
            assert application["progress"] == 10


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_to_latest_score_map(_db, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(days=1)
    latest = now + datetime.timedelta(days=1)

    scores = [
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=5,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=1,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=3,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=5,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
    ]
    _db.session.add_all(scores)
    _db.session.commit()

    result = get_sub_criteria_to_latest_score_map(str(application_id))

    assert result[sub_criteria_1_id] == 2
    assert result[sub_criteria_2_id] == 5
