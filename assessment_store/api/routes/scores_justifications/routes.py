from api.responses import error_response
from api.responses import scores_justifications_response
from api.responses import scores_justifications_response_list
from db.models.scores_justifications import ScoresJustificationsError
from db.models.scores_justifications import ScoresJustificationsMethods
from flask import make_response
from flask.views import MethodView


class ScoresJustificationsView(ScoresJustificationsMethods, MethodView):
    def get(self, sub_criteria_id: str, assessment_id: str):
        """
        GET /assessments/{assessment_id}/sub_criterias/
                {sub_criteria_id}/scores_justifications endpoint
        return the scores page for the sub_criteria for the assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :return: 200 assessment JSON / 404 Error
        """
        try:
            scores_justifications_list = self.scores_justifications(
                sub_criteria_id, assessment_id
            )
        except ScoresJustificationsError as e:
            return error_response(404, e.message)

        return scores_justifications_response_list(scores_justifications_list)

    def calc_scores(self, assessment_id: str):

        try:
            scores_list = self.scores(assessment_id)
        except ScoresJustificationsError as e:
            return error_response(404, e.message)

        if len(scores_list) == 0:
            return error_response(
                404, f"No scores found for assessment {assessment_id}"
            )

        return make_response({"scores": scores_list}, 200)

    def post(self, sub_criteria_id: str, assessment_id: str, body: dict):
        """
        Registers a score and justification for assessment and subcriteria
        :param sub_criteria_id: ID of sub-criteria
        :param assessment_id: ID of assessment
        :param score: score given
        :param justification: justification given
        :param assessor_user_id: person's ID who provides the
                                    score and justification
        :return: a json of the score and justification
                created (or an error if failure)
        """
        score = body.get("score")
        justification = body.get("justification")
        assessor_user_id = body.get("assessor_user_id")

        try:
            new_score_and_justification = self.register_score_justification(
                sub_criteria_id,
                assessment_id,
                score,
                justification,
                assessor_user_id,
            )
        except ScoresJustificationsError as e:
            return error_response(401, e.message)

        return scores_justifications_response(new_score_and_justification, 201)
