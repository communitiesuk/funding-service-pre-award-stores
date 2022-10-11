"""
Test magic links functionality
"""
import uuid

from tests.conftest import seeded_assessment_ids
from tests.conftest import seeded_subcriteria


class TestSubCriteriaEndpoints:
    def test_get_sub_criteria_list(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}/sub_criterias
        THEN a list of sub-criteria records are returned
        :param client:
        """

        endpoint = f"/assessments/{seeded_assessment_ids[1]}/sub_criterias"
        response = client.get(endpoint)
        sub_criterias = response.get_json()

        assert response.status_code == 200
        for i in range(4):
            assert (
                sub_criterias[i] == seeded_subcriteria[i].as_json()
            ), f"Sub criteria {i} does not match expected seeded data"

    def test_get_sub_criteria_by_id(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}
        THEN the appropriate sub_criteria record is returned
        :param client:
        """
        assessment_id = str(seeded_assessment_ids[1])
        sub_criteria_id = str(seeded_subcriteria[0].id)
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}"
        )
        response = client.get(endpoint)
        sub_criteria = response.get_json()

        assert response.status_code == 200
        assert sub_criteria.get("id") == sub_criteria_id

    def test_get_sub_criteria_by_non_existent_id_fails(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/fake-id
        THEN a 404 error message is returned
        :param client:
        """
        assessment_id = str(seeded_assessment_ids[1])
        sub_criteria_id = str(uuid.uuid4())
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}"
        )
        response = client.get(endpoint)

        assert response.status_code == 404
