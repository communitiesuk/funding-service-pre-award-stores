import json

from db import db
from db.models.assessment_record import AssessmentRecord
from db.queries.assessment_records.helpers import derive_values_from_json
from db.schemas import AssessmentRecordMetadata
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import defer


def get_metadata_for_fund_round_id(fund_id, round_id):

    stmt = (
        select(AssessmentRecord)
        # Dont load json into memory
        .options(defer(AssessmentRecord.jsonb_blob)).where(
            AssessmentRecord.fund_id == fund_id,
            AssessmentRecord.round_id == round_id,
        )
    )

    assessment_metadatas = db.session.scalars(stmt).all()

    metadata_serialiser = AssessmentRecordMetadata()

    assessment_metadatas = [
        metadata_serialiser.dump(app_metadata)
        for app_metadata in assessment_metadatas
    ]

    return assessment_metadatas


def bulk_insert_application_record(json_strings, application_type):

    rows = []

    for single_json_string in json_strings:

        loaded_json = json.loads(single_json_string)

        derived_values = derive_values_from_json(loaded_json, application_type)

        row = {
            **derived_values,
            "jsonb_blob": loaded_json,
            "type_of_application": application_type,
        }

        rows.append(row)

        del loaded_json

    db.session.bulk_insert_mappings(AssessmentRecord, rows)
    db.session.commit()


def find_answer_by_key_runner(field_key: str, app_id: str):

    return (
        db.session.query(
            func.jsonb_path_query_first(
                AssessmentRecord.jsonb_blob,
                "$.forms[*].questions[*].fields[*] ? (@.key =="
                f' "{field_key}")',
            )
        )
        .filter(AssessmentRecord.application_id == app_id)
        .one()
    )
