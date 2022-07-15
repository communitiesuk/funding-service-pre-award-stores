"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestScoreJustificationEndpoints:

    assessment_id = "123e4567-e89b-12d3-a456-426655440000"
    sub_criteria_id = "123e4567-e89b-12d3-a456-426655440001"
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
                "id": "123e4567-e89b-12d3-a456-426655440003",  # noqa
                "created_at": "2022-07-07T09:11:38.240578Z",
                "sub_criteria_id": "123e4567-e89b-12d3-a456-426655440001",
                "assessment_id": "123e4567-e89b-12d3-a456-426655440000",
                "score": 5,
                "justification": "wow",
                "assessor_user_id": "person_1",
            }
        ]
        response = flask_test_client.get(self.endpoint)
        scores_justifications = response.get_json()

        print(scores_justifications)

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
