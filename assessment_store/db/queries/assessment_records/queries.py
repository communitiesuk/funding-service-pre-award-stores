"""Queries which are performed on the `assessment_records` table.

Joins allowed.
"""
import json
from typing import Dict
from typing import List

from db import db
from db.models.assessment_record import AssessmentRecord
from db.queries.assessment_records._helpers import derive_values_from_json
from db.schemas import AssessmentRecordMetadata
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.orm import defer


def get_metadata_for_fund_round_id(fund_id: str, round_id: str) -> List[Dict]:
    """get_metadata_for_fund_round_id Executes a query on assessment records
    which returns all rows matching the given fund_id and round_id. Excludes
    irrelevant columns such as `db.models.AssessmentRecord.jsonb_blob`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """

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


def bulk_insert_application_record(
    json_strings: List[str], application_type: str
) -> None:
    """bulk_insert_application_record Given a list of json strings (not
    `dict`s) and an `application_type` we extract key values from the json
    strings before inserting them with the remaining values into
    `db.models.AssessmentRecord`.

    :param json_strings: _description_
    :param application_type: _description_
    """

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

    stmt = postgres_insert(AssessmentRecord).values(rows)

    upsert_rows_stmt = stmt.on_conflict_do_nothing(index_elements=["assessment_records.applciation_id"])

    db.session.execute(upsert_rows_stmt)

    db.session.commit()


def find_answer_by_key_runner(field_key: str, app_id: str) -> List[tuple]:
    """find_answer_by_key_runner Given an application id `app_id` and a field
    to search for `app_id` we return the matching field object (A json with
    keys {key, answer, title, type}) within an SQLAlchemy result.

    :param field_key: The unique key of the field.
    :type field_key: str
    :param app_id: The application id of the queried row.
    :type app_id: str
    :return: The whole field object of the found field. Returned as a
    SQLAlchemy result.
    :rtype: List[tuple]
    """

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
