"""
Test magic links functionality
"""
from operator import contains
from tests.conftest import seeded_assessment_ids
from tests.conftest import seeded_subcriteria

class TestCommentEndpoints:

    def test_comment_is_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/section/{section_id}/comments
                with a json payload
        THEN a comment is created for that sub_criterias section
         and the comment_id should be returned
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[2].id
        section_id = 2
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/"
            f"{sub_criteria_id}/section/{section_id}/comments"
        )
        payload = {
            "assessor_user_id": "person_3",
            "comment": "good job"
        }
        response = client.post(endpoint, json=payload)
        comment_response = response.get_json()

        assert response.status_code == 201
        assert comment_response.get("comment") == "good job"
        assert 'comment_id' in comment_response

    def test_get_comments_by_sub_criteria_section(self, client):
            """
            GIVEN a running Flask client and db
            WHEN we GET to /assessments/{assessment_id}/
                    sub_criterias/{sub_criteria_id}/section/{section_id}/comments
            THEN the comments for this section are returned as a list
            """
            assessment_id = seeded_assessment_ids[1]
            sub_criteria_id = seeded_subcriteria[2].id
            section_id = 2

            payloads = [{
                "assessor_user_id": "person_3",
                "comment": "Good evidence."
            },
            {
                "assessor_user_id": "person_1",
                "comment": "Great job."
            },
            {
                "assessor_user_id": "person_1",
                "comment": "I like this."
            }
            ]

            endpoint = (
                f"/assessments/{assessment_id}/sub_criterias/"
                f"{sub_criteria_id}/section/{section_id}/comments"
            )

            client.post(endpoint, json=payloads[0])
            client.post(endpoint, json=payloads[1])
            client.post(endpoint, json=payloads[2])
            response = client.get(endpoint)
            comment_list_response = response.get_json()

            assert response.status_code == 200
            assert len(comment_list_response["comments_list"]) == 3

    def test_comment_isnt_created_for_non_existent_sub_criteria(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/section/{section_id}/comments
                with a json payload but a non existent sub_criteria_id
        THEN we should be returned a 404
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = '8c3fd52e-abe3-46d2-932e-113292db1b2c'
        section_id = 2
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/"
            f"{sub_criteria_id}/section/{section_id}/comments"
        )
        payload = {
            "assessor_user_id": "person_3",
            "comment": "good job"
        }
        response = client.post(endpoint, json=payload)
        comment_response = response.get_json()

        assert comment_response["code"] == 404
        assert 'insert or update on table "comment" violates foreign key' in comment_response["message"] 