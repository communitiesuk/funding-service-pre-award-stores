import json
import uuid

from sqlalchemy import Index, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, BYTEA, ENUM
from db.models.enums.workflow_status import Status
from sqlalchemy_utils.types import UUIDType
from db import db
from copy import deepcopy

class AssessmentRecords(db.Model):

    id = db.Column(
		"id",
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

class AssessmentJsonBlobs(db.model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    assessment_record_id = db.Column(
		"id",
		ForeignKey(AssessmentRecords.id),
	)

    jsonb_blob = db.Column("jsonb_blob", JSONB)

class ApplicationIngestionRecords(db.model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    assessment_record_id = db.Column(
		"id",
		ForeignKey(AssessmentRecords.id),
	)

    application_json = db.Column("application_json", JSONB)

    application_json_sha256 = db.Column("application_json_sha256", BYTEA,
    default=func.sha256(application_json))

Index(
    "application_json_index",
    AssessmentRecords.application_json,
    postgresql_ops={
        "application_json": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

Index(
    "application_id_index",
    AssessmentRecords.application_id,
    postgresql_using="hash",
)

COF_json_mapper = {
    "id" : "$.id",
    "project_name" : "$.project_name",
    "short_id" : "$.reference",
    "fund_id" : "$.fund_id",
    "round_id" : "$.round_id",
    "application_json" : "$.forms",
    "funding_amount_requested" : "$.forms[*].questions[*].fields[?(@.key = 'JzWvhj')].answer",
    "DEFAULTS" : {
        "type_of_application" : "COF"
    }
}

def insert_application_record(json_string : str, json_row_mapper : dict):

    application_dict = json.loads(json_string)

    mapper = deepcopy(json_row_mapper)

    defaults = mapper.pop("DEFAULTS")

    jsonpath_matchers = []




def find_field_by_key(field_key: str, app_id : str):

    return (
        db.session.query(
                func.jsonb_path_query_first(
                AssessmentRecords.application_json,
                f"$[*].fields[*] ? (@.key == \"{field_key}\")",
            )
        )
        .filter(AssessmentRecords.application_id == app_id)
        .filter(
            AssessmentRecords.application_json.contains(
                [ { "fields": [ { "key" : field_key } ] } ]
            )
        )
        .one()
    )