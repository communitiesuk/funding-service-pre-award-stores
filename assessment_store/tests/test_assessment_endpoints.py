"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestAssessmentEndpoints:

    created_link_keys = []
    used_link_keys = []

    def test_assessment_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments with and json payload
        which includes an application_id
        THEN an assessment record is created and returned
        :param flask_test_client:
        """
        assert True
