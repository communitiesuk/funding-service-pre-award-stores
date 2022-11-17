import json
import re
import uuid

from db import db
from db.models.assessment_record import AssessmentRecords
from db.schemas import AssessmentRecordMetadata
from db.queries.assessment_records.helpers import derive_values_from_json, get_mapper
from sqlalchemy import bindparam, insert, literal, literal_column, select
from sqlalchemy.orm import defer
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TEXT, JSONB, UUID
from sqlalchemy import cast, text
from sqlalchemy import Column
from sqlalchemy_utils import jsonb_sql
from sqlalchemy import column, String


def get_metadata_for_fund_round_id(fund_id, round_id):

    stmt = (
        select(AssessmentRecords)
        # Dont load json into memory
        .options(defer(AssessmentRecords.jsonb_blob)).where(
            AssessmentRecords.fund_id == fund_id,
            AssessmentRecords.round_id == round_id,
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

        row = {**derived_values, "jsonb_blob" : loaded_json, "type_of_application" : application_type}

        rows.append(row)

        del loaded_json

    db.session.bulk_insert_mappings(AssessmentRecords, rows)
    db.session.commit()

def find_answer_by_key_runner(field_key: str, app_id: str):

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

