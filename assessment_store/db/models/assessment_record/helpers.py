from db import db
from db.models.assessment_record.assessment_records import AssessmentRecords
from sqlalchemy import func


def find_answer_by_key_cof(field_key: str, app_id: str):

    return (
        db.session.query(
            func.jsonb_path_query_first(
                AssessmentRecords.jsonb_blob,
                "$.forms[*].questions[*].fields[*] ? (@.key =="
                f' "{field_key}")',
            )
        )
        .filter(AssessmentRecords.application_id == app_id)
        .one()
    )
