from db import db
from db.models.assessment_record.enums import Status
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT


class AssessmentRecords(db.Model):
    __tablename__ = "assessment_records"

    application_id = db.Column(
        "application_id", db.Text(), primary_key=True, index=True
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

    round_id = db.Column("round_id", db.Text(), index=True, nullable=False)

    fund_id = db.Column("fund_id", db.Text(), index=True, nullable=False)

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
