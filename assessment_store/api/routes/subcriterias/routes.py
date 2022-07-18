import json

from api.responses import error_response
from api.responses import sub_criteria_response
from db.models.sub_criteria import SubCriteriaError
from db.models.sub_criteria import SubCriteriaMethods
from flask import Response
from flask.views import MethodView
from sqlalchemy.exc import StatementError


class SubCriteriaView(SubCriteriaMethods, MethodView):
    def list(self, assessment_id: str = None):
        """
        GET /assessments/{assessment_id}/sub_criterias endpoint
        :return: Json Response
        """
        return Response(
            json.dumps(
                self.subcriterias_by_assessment_id(assessment_id, as_json=True)
            ),
            mimetype="application/json",
            status=200,
        )

    def get(self, assessment_id: str = None, sub_criteria_id: str = None):
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
        except SubCriteriaError as e:
            return error_response(404, e.message)
        except StatementError:
            return error_response(404, "Sub-Criteria could not be found")

        return sub_criteria_response(sub_criteria)
