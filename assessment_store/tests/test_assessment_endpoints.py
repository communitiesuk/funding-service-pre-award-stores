"""
Test magic links functionality
"""
from tests.conftest import seeded_assessment_ids


class TestAssessmentEndpoints:

    EXISTING_APP_ID = "app_id_existing"

    def test_assessment_is_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments with and json payload
        which includes an application_id
        THEN an assessment record is created and returned
        :param client:
        """
        appId = "app_id_1"
        expected_link_attributes = {"applicationId": appId}
        payload = {"applicationId": appId}
        endpoint = "/assessments"
        response = client.post(endpoint, json=payload)
        assessment = response.get_json()

        assert response.status_code == 201
        assert assessment.get("applicationId") == expected_link_attributes.get(
            "applicationId"
        )

    def test_create_duplicate_application_assessment_fails(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments with and json payload
        which includes an application_id that already has an
        existing assessment
        THEN a 401 error message is returned
        :param client:
        """
        payload = {"applicationId": self.EXISTING_APP_ID}
        endpoint = "/assessments"
        response = client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 401
        assert (
            error_response.get("message")
            == "An assessment for this application already exists"
        )

    def test_get_assessment_by_id(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}
        THEN the appropriate assessment record is returned
        :param client:
        """
        expected_link_attributes = {"applicationId": self.EXISTING_APP_ID}
        assessment_id = seeded_assessment_ids[0]
        endpoint = f"/assessments/{assessment_id}"
        response = client.get(endpoint)
        assessment = response.get_json()

        assert response.status_code == 200
        assert assessment.get("applicationId") == expected_link_attributes.get(
            "applicationId"
        )

    def test_get_assessment_by_non_existent_id_fails(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/fake-id
        THEN a 404 error message is returned
        :param client:
        """
        assessment_id = "fake-id"
        endpoint = f"/assessments/{assessment_id}"
        response = client.get(endpoint)
        error_response = response.get_json()

        assert response.status_code == 404
        assert error_response.get("message") == "Assessment could not be found"

    def test_update_status(self, client):
        """
        GIVEN: our service runs on flask client and db.
        WHEN: we POST to /update-compliance with and json payload
            which includes an assessment_id  which already exists
            in db & new status to be updated.
        THEN: we check the response with new status.

        """
        assessment_id = seeded_assessment_ids[0]
        compliance_status = "COMPLIANT"
        payload = {"id": assessment_id, "compliance_status": compliance_status}
        endpoint = "/update-compliance"
        response = client.post(endpoint, json=payload)
        assert b"COMPLIANT" in response.data

    def test_update_status_by_incorrect_id_fails(self, client):
        """
        GIVEN: our service runs on flask client and db.
        WHEN: we POST to /update-compliance with and json payload
            which includes an incorrect assessment_id & new status
            to be updated.
        THEN: we check error 404 is returned.

        """
        assessment_id = "fake_id"
        compliance_status = "COMPLIANT"
        payload = {"id": assessment_id, "compliance_status": compliance_status}
        endpoint = "/update-compliance"
        response = client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 404
        assert error_response.get("message") == "Assessment could not be found"

    def testHealthcheckRoute(self, client):
        expected_result = {
            "checks": [{"check_flask_running": "OK"}, {"check_db": "OK"}]
        }

        result = client.get("/healthcheck")
        assert result.status_code == 200, "Unexpected status code"
        assert result.json == expected_result, "Unexpected json body"
