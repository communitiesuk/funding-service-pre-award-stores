from api.responses import error_response
from api.responses import comment_created, comments_response
from db.models.comments import CommentError
from db.models.comments import CommentMethods
from flask.views import MethodView


class CommentsView(CommentMethods, MethodView):
    def get(self, assessment_id: str, sub_criteria_id: str, section_id: int):
        """
        GET /comments endpoint
        return the comments for a sub_criteria of an assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :param section_id: id of the sub_criterias section
        :return: 200 assessment JSON / 404 Error
        """
        try:
            comments = self.get_section_comments(
                assessment_id, sub_criteria_id, section_id
            )
        except CommentError as e:
            return error_response(404, e.message)

        return comments_response(comments)

    def post(self, sub_criteria_id: str, assessment_id: str, section_id: int, body: dict):
        """
        POST /assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/section/{section_id}/comments endpoint
        returns the recorded comment_id
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :return: 201 assessment JSON / 404 Error
        """
        assessor_user_id = body.get("assessor_user_id")
        comment = body.get("comment")
        try:
            response = self.save_comment(
                assessment_id, sub_criteria_id, section_id, assessor_user_id, comment
            )
        except CommentError as e:
            return error_response(404, e.message)

        return comment_created(response)
        