# flake8:noqa
"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestComplianceEndpoints:
    def test_get_compliance(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
        THEN a compliance status is returned
        :param flask_test_client:
        """
        assessment_id = "123e4567-e89b-12d3-a456-426655440000"
        sub_criteria_id = "123e4567-e89b-12d3-a456-426655440001"
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        expected_compliance_record = {
            "id": "123e4567-e89b-12d3-a456-426655440004",
            "created_at": "2022-07-07T09:11:38.240578Z",
            "assessment_id": "123e4567-e89b-12d3-a456-426655440000",
            "sub_criteria_id": "123e4567-e89b-12d3-a456-426655440001",
            "is_compliant": True,
        }
        response = flask_test_client.get(endpoint)
        returned_compliance_record = response.get_json()
        assert response.status_code == 200
        assert returned_compliance_record == expected_compliance_record

    def test_get_non_exisiting_compliance(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                for assessment and subcriteria ids that do
                not exist
        THEN an error is returned
        :param flask_test_client:
        """
        assessment_id = "123e4567-e89b-12d3-a456-426655449999"
        sub_criteria_id = "123e4567-e89b-12d3-a456-426655449999"
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        response = flask_test_client.get(endpoint)
        error_response = response.get_json()
        assert response.status_code == 404
        assert (
            error_response.get("message")
            == "error - compliance record does not exist"
        )

    def test_compliance_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                with and json payload
        THEN a compliance record is created and returned
        :param flask_test_client:
        """
        assessment_id = "test"
        sub_criteria_id = "testing"
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        payload = {"is_compliant": False}
        response = flask_test_client.post(endpoint, json=payload)
        compliance_record = response.get_json()

        assert response.status_code == 201
        assert compliance_record.get("is_compliant") == False  # noqa

    def test_wrong_payload_compliance_is_not_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                with a wrong json payload
        THEN a compliance record is not created and error returned
        :param flask_test_client:
        """
        assessment_id = "123e4567-e89b-12d3-a456-426655449999"
        sub_criteria_id = "123e4567-e89b-12d3-a456-426655449999"
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        payload = {"is_compliant": "something wrong here"}
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 400
        assert (
            error_response.get("detail")
            == "'something wrong here' is not of type 'boolean' - 'is_compliant'"
        )