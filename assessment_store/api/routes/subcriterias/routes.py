import json

import sqlalchemy
from api.responses import error_response
from api.responses import sub_criteria_response
from db.models.sub_criteria import SubCriteria, SubCriteriaError
from db.models.sub_criteria import SubCriteriaMethods
from flask import Response
from flask.views import MethodView


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
            subcriteria = self.get_by_id(sub_criteria_id)
        except SubCriteriaError as e:
            return error_response(
                code=404,
                message=f"Subcriteria not found for assessment_id"
                "{assessment_id} and"
                f"sub_criteria_id {sub_criteria_id}",
            )
        except Exception as e:
            return error_response(code=500, message=e.__repr__)

        return sub_criteria_response(subcriteria)
