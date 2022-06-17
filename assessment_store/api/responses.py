from db.models.assessment import Assessment
from flask import make_response


def error_response(code: int, message: str):
    return (
        make_response({"status": "error", "code": code, "message": message}),
        code,
    )


def assessment_response(assessment: Assessment, code: int = 200):
    return (
        make_response(
            {
                "id": assessment.id,
                "compliance_status": assessment.compliance_status,
                "applicationId": assessment.application_id,
            }
        ),
        code,
    )
