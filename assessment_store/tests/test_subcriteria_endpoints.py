"""
Test magic links functionality
"""
import uuid

import pytest
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.mark.usefixtures("flask_test_client")
class TestSubCriteriaEndpoints:
    def test_get_sub_criteria_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/{assessment_id}/sub_criterias
        THEN a list of sub-criteria records are returned
        :param flask_test_client:
        """
        expected_sub_criterias = [SqliteTestDB.sub_criteria_1.as_json()]
        assessment_1_path = str(SqliteTestDB.assessment_1.uuid)
        endpoint = f"/assessments/{assessment_1_path}/sub_criterias"
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
        assessment_id = str(SqliteTestDB.assessment_1.uuid)
        sub_criteria_id = str(SqliteTestDB.sub_criteria_1.uuid)
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}"
        )
        response = flask_test_client.get(endpoint)
        sub_criteria = response.get_json()

        assert response.status_code == 200
        assert sub_criteria.get("sub_criteria_id") == sub_criteria_id

    def test_get_sub_criteria_by_non_existent_id_fails(
        self, flask_test_client
    ):
        """
        GIVEN a running Flask client and db
        WHEN we GET /assessments/fake-id
        THEN a 404 error message is returned
        :param flask_test_client:
        """
        assessment_id = str(uuid.uuid4())
        sub_criteria_id = str(uuid.uuid4())
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}"
        )
        response = flask_test_client.get(endpoint)

        assert response.status_code == 404
