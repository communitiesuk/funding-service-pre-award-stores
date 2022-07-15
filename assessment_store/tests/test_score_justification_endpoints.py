"""
Test magic links functionality
"""
import pytest
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.mark.usefixtures("flask_test_client")
class TestScoreJustificationEndpoints:

    assessment_id = str(SqliteTestDB.assessment_1.uuid)
    sub_criteria_id = str(SqliteTestDB.sub_criteria_1.uuid)
    endpoint = (
        f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/scores"
    )

    def test_get_scores_justifications_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
        THEN a list of scores and jsutifications is returned
        :param flask_test_client:
        """
        expected_scores_justifications = [
            {
                "scores_justifications_id": str(
                    SqliteTestDB.score_justification.uuid
                ),  # noqa
                "created_at": "2022-07-07T09:11:38.240578Z",
                "sub_criteria_id": str(SqliteTestDB.sub_criteria_1.uuid),
                "assessment_id": str(SqliteTestDB.assessment_1.uuid),
                "score": 5,
                "justification": "wow",
                "assessor_user_id": "person_1",
            }
        ]
        response = flask_test_client.get(self.endpoint)
        scores_justifications = response.get_json()

        assert response.status_code == 200
        assert (
            scores_justifications["scores_justifications"]
            == expected_scores_justifications
        )

    def test_score_justification_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
                with and json payload
        THEN an score and justification record is created and returned
        :param flask_test_client:
        """
        payload = {
            "justification": "bad",
            "assessor_user_id": "person_2",
            "score": 1,
        }
        response = flask_test_client.post(self.endpoint, json=payload)
        score_justification = response.get_json()

        assert response.status_code == 201
        assert score_justification.get("score") == 1

    def test_scores(self, flask_test_client):
        expected_response = [
            {
                "criteria_id": str(SqliteTestDB.crit_2_uuid),
                "criteria_name": "deliverability",
                "total_score": 7,
                "weight": 0.4,
                "weighted_score": 2.8000000000000003,
            },
            {
                "criteria_id": str(SqliteTestDB.crit_1_uuid),
                "criteria_name": "strategy",
                "total_score": 3,
                "weight": 0.3,
                "weighted_score": 0.8999999999999999,
            },
            {
                "criteria_id": str(SqliteTestDB.crit_3_uuid),
                "criteria_name": "value_for_money",
                "total_score": 5,
                "weight": 0.3,
                "weighted_score": 1.5,
            },
        ]
        assessment_id = str(SqliteTestDB.assessment_2_id)
        endpoint = f"/assessments/{assessment_id}/scores"
        response = flask_test_client.get(endpoint)
        assert response.json["scores"] == expected_response
