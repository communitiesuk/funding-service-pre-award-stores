from sqlalchemy import Index
from db import db
from db.models.assessment_record.enums import Status
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import UUID


class AssessmentRecords(db.Model):
    __tablename__ = "assessment_records"

    application_id = db.Column(
        "application_id", UUID(), primary_key=True
    )

    short_id = db.Column("short_id", db.Text(), nullable=False)

    type_of_application = db.Column(
        "type_of_application", db.Text(), index=True, nullable=False
    )

    project_name = db.Column(
        "project_name", db.Text(), index=True, nullable=False
    )

    funding_amount_requested = db.Column(
        "funding_amount_requested", db.Float(), index=True, nullable=False
    )

    round_id = db.Column("round_id", UUID(), index=True, nullable=False)

    fund_id = db.Column("fund_id", UUID(), index=True, nullable=False)

    langauge = db.Column("langauge", db.Text(), default="en", nullable=False)

    workflow_status = db.Column(
        "workflow_status", ENUM(Status), index=True, default="NOT_STARTED"
    )

    jsonb_blob = db.Column("jsonb_blob", JSONB, nullable=False)

    application_json_md5 = db.Column(
        "application_json_sha256",
        TEXT,
        Computed(func.md5(cast(jsonb_blob, TEXT)), persisted=True),
    )

Index(
    "application_jsonb_index",
    AssessmentRecords.jsonb_blob,
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

# This is very fast for "=" in WHERE clauses.
Index(
    "application_id_hash_index",
    AssessmentRecords.application_id,
    postgresql_using="hash",
)

# Links the round_id and fund_id columns by an index.
Index(
    "application_round_fund_id_index",
    AssessmentRecords.round_id,
    AssessmentRecords.fund_id,
)

Index(
    "application_jsonb_index",
    func.concat(AssessmentRecords.short_id, ' ', AssessmentRecords.project_name),
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)
