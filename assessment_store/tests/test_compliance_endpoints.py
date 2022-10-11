# flake8:noqa
"""
Test magic links functionality
"""
from tests.conftest import seeded_assessment_ids
from tests.conftest import seeded_compliance_records
from tests.conftest import seeded_subcriteria


class TestComplianceEndpoints:
    def test_get_compliance(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
        THEN a compliance status is returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[1].id

        endpoint = f"/assessments/{seeded_assessment_ids[1]}/sub_criterias/{sub_criteria_id}/compliance"
        response = client.get(endpoint)
        returned_compliance_record = response.get_json()

        assert response.status_code == 200
        assert (
            returned_compliance_record
            == seeded_compliance_records[0].as_json()
        )

    def test_get_non_exisiting_compliance(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                for assessment and subcriteria ids that do
                not exist
        THEN an error is returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[0].id
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        response = client.get(endpoint)
        error_response = response.get_json()
        assert response.status_code == 404
        assert (
            error_response.get("message")
            == "error - compliance record does not exist"
        )

    def test_compliance_is_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                with and json payload
        THEN a compliance record is created and returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[2].id
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        payload = {"is_compliant": False}
        response = client.post(endpoint, json=payload)
        compliance_record = response.get_json()

        assert response.status_code == 201
        assert compliance_record.get("is_compliant") == False  # noqa

    def test_duplicate_compliance_is_not_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                with and json payload
        THEN a compliance record is created and returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[1].id
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        payload = {"is_compliant": False}
        response = client.post(endpoint, json=payload)
        compliance_record = response.get_json()

        assert response.status_code == 201
        assert compliance_record.get("is_compliant") == False  # noqa

    def test_wrong_payload_compliance_is_not_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/compliance
                with a wrong json payload
        THEN a compliance record is not created and error returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[0].id
        endpoint = f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/compliance"
        payload = {"is_compliant": "something wrong here"}
        response = client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 400
        assert (
            error_response.get("detail")
            == "'something wrong here' is not of type 'boolean' - 'is_compliant'"
        )
