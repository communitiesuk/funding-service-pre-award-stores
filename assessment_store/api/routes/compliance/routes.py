from api.responses import compliance_response
from api.responses import error_response
from db.models.compliance import ComplianceError
from db.models.compliance import ComplianceMethods
from flask.views import MethodView
from sqlalchemy.exc import StatementError


class ComplianceView(ComplianceMethods, MethodView):
    def get(self, sub_criteria_id: str, assessment_id: str):
        """
        GET /assessments/{assessment_id}/sub_criterias/
                {sub_criteria_id}/compliance endpoint
        return the compliance page for the sub_criteria of the assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :return: 200 assessment JSON / 404 Error
        """
        try:
            compliance_record = self.get_compliance(
                sub_criteria_id, assessment_id
            )
        except ComplianceError as e:
            return error_response(404, "error - compliance record does not exist"
            )
        except IndexError:
            return error_response(
                404, "error - compliance record does not exist"
            )
        except StatementError:
            return error_response(404, 'please enter a uuid type')

        return compliance_response(compliance_record)


    def post(self, sub_criteria_id: str, assessment_id: str, body: dict):
        """
        Registers compliance status for an assessment and subcriteria
        :param sub_criteria_id: ID of sub-criteria
        :param assessment_id: ID of assessment
        :param is_compliant: bool value of complaince status
        :return: a json of the compliance record
                created (or an error if failure)
        """
        is_compliant = body.get("is_compliant")

        try:
            new_compliance = self.register_compliance(
                sub_criteria_id, assessment_id, is_compliant
            )
        except ComplianceError as e:
            return error_response(401, "error - could not create compliance record")
        except StatementError:
            return error_response(404, 'please enter a uuid type')

        return compliance_response(new_compliance, 201)
