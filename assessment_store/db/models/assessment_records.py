from functools import lru_cache
import json
from pprint import pprint
import uuid
import random
from sqlalchemy import Index, func, Computed
from sqlalchemy.dialects.postgresql import JSONB, BYTEA, ENUM, JSON
from db.models.enums.workflow_status import Status
from sqlalchemy_utils.types import UUIDType
from db import db
from copy import deepcopy
from jsonpath_ng.ext import parse

class AssessmentRecords(db.Model):

    id = db.Column(
		"assessment_id",
		db.Text(),
		primary_key=True,
        nullable=False,
        index=True
	)

    short_id = db.Column(
        "short_id",
        db.Text(),
        nullable=False
    )

    type_of_application = db.Column(
        "type_of_application",
        db.Text(),
        nullable=False
    )

    project_name = db.Column(
        "project_name",
        db.Text(),
        nullable=False
    )

    funding_amount_requested = db.Column(
        "funding_amount_requested",
        db.Float(),
        nullable=False
    )

    round_id = db.Column(
        "round_id",
        db.Text(),
        nullable=False,
        index=True
    )

    fund_id = db.Column(
        "fund_id",
        db.Text(),
        nullable=False,
        index=True
    )

    langauge = db.Column(
        "langauge",
        db.Text(),
        nullable=False,
        default="en"
    )

    workflow_status = db.Column(
        "workflow_status",
        ENUM(Status),
        nullable=False,
        index=True,
        default="NOT_STARTED"
    )


class AssessmentJsonBlobs(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    assessment_record_id = db.Column(
		db.ForeignKey(AssessmentRecords.id),
	)

    jsonb_blob = db.Column("jsonb_blob", JSONB)


class ApplicationIngestionRecords(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    assessment_record_id = db.Column(
		db.ForeignKey(AssessmentRecords.id),
	)

    application_json = db.Column("application_json", JSON)

    application_json_sha256 = db.Column("application_json_sha256", BYTEA,
    Computed(func.sha256(application_json), persisted=True))

Index(
    "application_jsonb_index",
    AssessmentJsonBlobs.jsonb_blob,
    postgresql_ops={
        "application_json": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

Index(
    "assessment_blob_id_index",
    AssessmentJsonBlobs.assessment_record_id,
    postgresql_using="hash",
)

Index(
    "assessment_records_id_index",
    AssessmentRecords.id,
    postgresql_using="hash",
)

COF_json_mapper = {
    "id" : "$.id",
    "project_name" : "$.project_name",
    "short_id" : "$.reference",
    "fund_id" : "$.fund_id",
    "round_id" : "$.round_id",
    "funding_amount_requested" : "$.forms[*].questions[*].fields[?(@.key = 'JzWvhj')].answer",
    "DEFAULTS" : {
        "type_of_application" : "COF"
    }
}

def get_mapper(json_type : str):

    match json_type:
        case "COF":
            return COF_json_mapper

@lru_cache
def jsonpath_extractors(json_type : str):

    json_mapper = get_mapper(json_type)

    jsonpath_matchers = {key : parse(jsonpath_str) for key,jsonpath_str in json_mapper.items() if key != "DEFAULTS"}

    return jsonpath_matchers

def extract_values(json_as_dict, json_type):

    json_mapper = get_mapper(json_type)

    parsed_json_paths = jsonpath_extractors(json_type)

    defaults = json_mapper["DEFAULTS"]

    found_values_from_json = {}

    for key,jsonpath_query in parsed_json_paths.items():

        found_values_from_json[key] = jsonpath_query.find(json_as_dict).pop().value

    return {**defaults, **found_values_from_json}


def cof_insert_application_record(json_string : str):

    loaded_json = json.loads(json_string)

    created_record_row = extract_values(loaded_json, json_type = "COF")

    created_ingestion_row = {"assessment_record_id" : created_record_row["id"], "application_json" : json_string}

    json_blob_rows = [{"assessment_record_id" : created_record_row["id"], "jsonb_blob" : form_jsonb} for form_jsonb in loaded_json["forms"]]

    assessment_record_row = AssessmentRecords(**created_record_row)
    json_ingrestion_row = ApplicationIngestionRecords(**created_ingestion_row)

    db.session.add(assessment_record_row)

    db.session.commit()

    db.session.add(json_ingrestion_row)

    db.session.commit()

    db.session.bulk_insert_mappings(AssessmentJsonBlobs, json_blob_rows)

    db.session.commit()


def find_field_by_key(field_key: str, app_id : str):

    return (
        db.session.query(
                func.jsonb_path_query_first(
                AssessmentJsonBlobs.jsonb_blob,
                f"$.questions[*].fields[*] ? (@.key == \"{field_key}\")",
            )
        )
        .filter(AssessmentJsonBlobs.assessment_record_id == app_id)
        .filter(
            AssessmentJsonBlobs.jsonb_blob.contains(
                { "questions" : [ {"fields": [ { "key" : field_key } ]} ] }
            )
        )
        .one()
    )