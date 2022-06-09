import json

from api.responses import assessment_201_response
from api.responses import error_response
from db.models.assessment import AssessmentError
from db.models.assessment import AssessmentMethods
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
        return assessment_201_response(assessment)

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
        return assessment_201_response(new_assessment)
