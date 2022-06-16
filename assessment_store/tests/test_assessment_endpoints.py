"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestAssessmentEndpoints:

    assessment_ids = []

    def test_assessment_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments with and json payload
        which includes an application_id
        THEN an assessment record is created and returned
        :param flask_test_client:
        """
        expected_link_attributes = {"applicationId": "abc"}
        payload = {"applicationId": "abc"}
        endpoint = "/assessments"
        response = flask_test_client.post(endpoint, json=payload)
        assessment = response.get_json()
        self.assessment_ids.append(assessment.get("id"))

        assert response.status_code == 201
        assert assessment.get("applicationId") == expected_link_attributes.get(
            "applicationId"
        )

    def test_create_duplicate_application_assessment_fails(
        self, flask_test_client
    ):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments with and json payload
        which includes an application_id that already has an
        existing assessment
        THEN a 401 error message is returned
        :param flask_test_client:
        """
        payload = {"applicationId": "abc"}
        endpoint = "/assessments"
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 401
        assert (
            error_response.get("message")
            == "An assessment for this application already exists"
        )

    def test_get_assessments_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments
        THEN a list of assessment records is returned
        :param flask_test_client:
        """
        expected_assessments = [
            {
                "applicationId": "abc",
                "status": "UNASSESSED",
                "id": self.assessment_ids[0],
            }
        ]
        endpoint = "/assessments"
        response = flask_test_client.get(endpoint)
        assessments = response.get_json()

        assert response.status_code == 200
        assert assessments == expected_assessments

    def test_get_assessment_by_id(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}
        THEN the appropriate assessment record is returned
        :param flask_test_client:
        """
        expected_link_attributes = {"applicationId": "abc"}
        assessment_id = self.assessment_ids[0]
        endpoint = f"/assessments/{assessment_id}"
        response = flask_test_client.get(endpoint)
        assessment = response.get_json()

        assert response.status_code == 200
        assert assessment.get("applicationId") == expected_link_attributes.get(
            "applicationId"
        )

    def test_get_assessment_by_non_existent_id_fails(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/fake-id
        THEN a 404 error message is returned
        :param flask_test_client:
        """
        assessment_id = "fake-id"
        endpoint = f"/assessments/{assessment_id}"
        response = flask_test_client.get(endpoint)
        error_response = response.get_json()

        assert response.status_code == 404
        assert error_response.get("message") == "Assessment could not be found"

    def test_update_status(self, flask_test_client):
        """
        GIVEN: our service runs on flask client and db.
        WHEN: we POST to /update-compliance with and json payload
            which includes an assessment_id  which already exists
            in db & new status to be updated.
        THEN: we check the response with new status.

        """
        assessment_id = self.assessment_ids[0]
        compliance_status = "COMPLIANT"
        payload = {"id": assessment_id, "compliance_status": compliance_status}
        endpoint = "/update-compliance"
        response = flask_test_client.post(endpoint, json=payload)
        assert b"COMPLIANT" in response.data

    def test_update_status_by_incorrect_id_fails(self, flask_test_client):
        """
        GIVEN: our service runs on flask client and db.
        WHEN: we POST to /update-compliance with and json payload
            which includes an incorrect assessment_id & new status
            to be updated.
        THEN: we check error 401 is returned.

        """
        assessment_id = "fake_id"
        compliance_status = "COMPLIANT"
        payload = {"id": assessment_id, "compliance_status": compliance_status}
        endpoint = "/update-compliance"
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 404
        assert error_response.get("message") == "Assessment could not be found"
