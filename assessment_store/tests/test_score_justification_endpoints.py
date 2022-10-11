"""
Test magic links functionality
"""
from unittest import mock

from tests.conftest import seeded_assessment_ids
from tests.conftest import seeded_criteria
from tests.conftest import seeded_scores_justifications
from tests.conftest import seeded_subcriteria
from tests.mocks.mock_round_store import mock_get_round_full_data


class TestScoreJustificationEndpoints:
    def test_get_scores_justifications_list(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
        THEN a list of scores and jsutifications is returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[2].id
        endpoint = (
            f"/assessments/{assessment_id}/"
            f"sub_criterias/{sub_criteria_id}/scores"
        )
        response = client.get(endpoint)
        scores_justifications = response.get_json()

        assert response.status_code == 200
        assert (
            scores_justifications["scores_justifications"][0]
            == seeded_scores_justifications[2].as_json()
        )

    def test_score_justification_is_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
                with and json payload
        THEN an score and justification record is created and returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[2].id
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/"
            f"{sub_criteria_id}/scores"
        )
        payload = {
            "justification": "bad",
            "assessor_user_id": "person_2",
            "score": 1,
        }
        response = client.post(endpoint, json=payload)
        score_justification = response.get_json()

        assert response.status_code == 201
        assert score_justification.get("score") == 1

    def test_scores(self, client):
        expected_response = [
            {
                "criteria_id": str(seeded_criteria[0].id),
                "criteria_name": seeded_criteria[0].criteria_name,
                "total_score": 0,
                "weight": 0.8,
                "weighted_score": 0,
            },
            {
                "criteria_id": str(seeded_criteria[1].id),
                "criteria_name": seeded_criteria[1].criteria_name,
                "total_score": 1,
                "weight": 0.1,
                "weighted_score": 0.1,
            },
            {
                "criteria_id": str(seeded_criteria[2].id),
                "criteria_name": seeded_criteria[2].criteria_name,
                "total_score": 4,
                "weight": 0.1,
                "weighted_score": 0.4,
            },
        ]
        assessment_id = str(seeded_assessment_ids[1])
        endpoint = f"/assessments/{assessment_id}/scores"
        with mock.patch(
            "api.routes.scores_justifications.utils.get_round_json",
            side_effect=mock_get_round_full_data,
        ):
            response = client.get(endpoint)
        assert response.json["scores"] == expected_response
