from typing import List

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from db import db
from db.models.assessment_record.assessment_records import AssessmentRecords

# AssessmentJsonBlobs


def find_answer_by_key_cof(field_key: str, app_id: str):

    json_forms = db.Column("value", JSONB)

    return (
        db.session.query(
            func.jsonb_path_query_first(
                json_forms,
                f'$.questions[*].fields[*] ? (@.key == "{field_key}")',
            )
        )
        .select_from(
            AssessmentRecords,
            func.jsonb_array_elements(
                AssessmentRecords.jsonb_blob["forms"]
            ).alias("value"),
        )
        .filter(
            json_forms.contains(
                {"questions": [{"fields": [{"key": field_key}]}]}
            )
        )
        .filter(AssessmentRecords.application_id == app_id)
        .one()
    )


# def find_answer_by_key_cof(field_key: str, app_id : str):

#     return ( db.session.query(AssessmentJsonBlobs.jsonb_blob)
#     .filter(
#             AssessmentJsonBlobs.jsonb_blob.contains(
#                 { "questions" : [ {"fields": [ { "key" : field_key } ]} ] }
#             )
#         )
#     .filter(AssessmentRecords.application_id == app_id)
#     .one() )
