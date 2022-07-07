"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestSubCriteriaEndpoints:
    def test_get_sub_criteria_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}/sub_criterias
        THEN a list of sub-criteria records are returned
        :param flask_test_client:
        """
        expected_sub_criterias = [
            {
                "sub_criteria_id": "123e4567-e89b-12d3-a456-426655440001",
                "round_id": "hello",
                "criteria_id": "hi",
                "sub_criteria_title": "something",
            },
            {
                "sub_criteria_id": "123e4567-e89b-12d3-a456-426655440002",
                "round_id": "ciao",
                "criteria_id": "cya",
                "sub_criteria_title": "nothing",
            },
        ]
        endpoint = "/assessments/wow/sub_criterias"
        response = flask_test_client.get(endpoint)
        sub_criterias = response.get_json()

        assert response.status_code == 200
        assert sub_criterias == expected_sub_criterias

    def test_get_sub_criteria_by_id(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}
        THEN the appropriate sub_criteria record is returned
        :param flask_test_client:
        """
        assessment_id = "123e4567-e89b-12d3-a456-426655440000"
        sub_criteria_id = "123e4567-e89b-12d3-a456-426655440001"
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}"
        )
        response = flask_test_client.get(endpoint)
        sub_criteria = response.get_json()

        assert response.status_code == 200
        assert sub_criteria.get("round_id") == "hello"

    def test_get_sub_criteria_by_non_existent_id_fails(
        self, flask_test_client
    ):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/fake-id
        THEN a 404 error message is returned
        :param flask_test_client:
        """
        sub_criteria_id = "fake-id"
        endpoint = f"/assessments/wow/sub_criterias/{sub_criteria_id}"
        response = flask_test_client.get(endpoint)
        error_response = response.get_json()

        assert response.status_code == 404
        assert (
            error_response.get("message") == "Sub-Criteria could not be found"
        )
