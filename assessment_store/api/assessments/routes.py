import json

from api.responses import assessment_response
from api.responses import error_response
from api.responses import scores_justifications_response
from api.responses import scores_justifications_response_list
from api.responses import sub_criteria_response
from db.models.assessment import AssessmentError
from db.models.assessment import AssessmentMethods
from db.models.scores_justifications import ScoresJustificationsError
from db.models.scores_justifications import ScoresJustificationsMethods
from db.models.sub_criteria import SubCriteriaMethods
from flask import request
from flask import Response
from flask.views import MethodView


class AssessmentsView(AssessmentMethods, MethodView):
    def search(self):
        """
        GET /assessments endpoint
        :return: Json Response
        """
        return Response(
            json.dumps(self.assessments(as_json=True)),
            mimetype="application/json",
        )

    def get(self, assessment_id: str):
        """
        GET /assessments/{assessment_id} endpoint
        If the assessment_id matches a valid assessment in the db
        return the assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :return: 200 assessment JSON / 404 Error
        """
        try:
            assessment = self.get_by_id(assessment_id)
        except AssessmentError as e:
            return error_response(404, e.message)

        return assessment_response(assessment)

    def register(self):
        """
        Registers an application for assessment and creates a new assessment
        :param applicationId: the application_id to register
        :return: a json of the assessment created (or an error of failure)
        """
        application_id = request.get_json().get("applicationId")
        if not application_id:
            return error_response(400, "Application ID is required")

        try:
            new_assessment = self.register_application(application_id)
        except AssessmentError as e:
            return error_response(401, e.message)

        return assessment_response(new_assessment, 201)

    def status(self):
        """Function receives a json payload containing assessment_id
        and compliance_status & calls the update_status func to
        search for an assessment_id & updates the status of
        that assessment_id in the database.

        Args: json data contains assessment_id & status

        Returns: Updated status with assessment_id & application_id

        """
        json = request.get_json()
        status = json.get("compliance_status")
        assessment_id = json.get("id")
        try:
            update_status = self.update_status(assessment_id, status)

        except AssessmentError as e:
            return error_response(404, e.message)
        return assessment_response(update_status)


class SubCriteriaView(SubCriteriaMethods, MethodView):
    def list(self):
        """
        GET /assessments/{assessment_id}/sub_criterias endpoint
        :return: Json Response
        """
        return Response(
            json.dumps(self.subcriterias(as_json=True)),
            mimetype="application/json",
        )

    def get(self, sub_criteria_id: str):
        """
        GET /assessments/{assessment_id}/sub_criterias/
                {sub_criteria_id} endpoint
        If the sub_criteria_id matches a valid sub_criteria in the db
        return the sub_criteria for the assessment
        If no matching valid link is found returns a 404 error message
        :param sub_criteria_id: id of the sub_criteria
        :return: 200 assessment JSON / 404 Error
        """
        try:
            sub_criteria = self.get_by_id(sub_criteria_id)
        except AssessmentError as e:
            return error_response(404, e.message)

        return sub_criteria_response(sub_criteria)


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

    def post(self, sub_criteria_id: str, assessment_id: str, body: dict):
        """
        Registers a score and justification for assessment and subcriteria
        :param sub_criteria_id: ID of sub-criteria
        :param assessment_id: ID of assessment
        :param score: score given
        :param justification: justification given
        :param person_id: person's ID who provides the score and justification
        :return: a json of the score and justification
                created (or an error if failure)
        """
        score = body.get("score")
        justification = body.get("justification")
        person_id = body.get("person_id")

        try:
            new_score_and_justification = self.register_score_justification(
                sub_criteria_id, assessment_id, score, justification, person_id
            )
        except ScoresJustificationsError as e:
            return error_response(401, e.message)

        return scores_justifications_response(new_score_and_justification, 201)
