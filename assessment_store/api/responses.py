from db.models.assessment import Assessment
from flask import make_response


def error_response(code: int, message: str):
    return (
        make_response({"status": "error", "code": code, "message": message}),
        code,
    )


def assessment_201_response(assessment: Assessment):
    return (
        make_response(
            {
                "id": assessment.id,
                "applicationId": assessment.application_id,
            }
        ),
        201,
    )
