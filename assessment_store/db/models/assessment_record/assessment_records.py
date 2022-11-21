from db import db
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import UUID


class AssessmentRecord(db.Model):
    __tablename__ = "assessment_records"

    application_id = db.Column("application_id", UUID, primary_key=True)

    short_id = db.Column("short_id", db.String(255), nullable=False)

    type_of_application = db.Column(
        "type_of_application", db.String(255), index=True, nullable=False
    )

    project_name = db.Column(
        "project_name", db.String(255), index=True, nullable=False
    )

    funding_amount_requested = db.Column(
        "funding_amount_requested", db.Float(), index=True, nullable=False
    )

    round_id = db.Column("round_id", UUID, index=True, nullable=False)

    fund_id = db.Column("fund_id", UUID, index=True, nullable=False)

    language = db.Column("language", ENUM(Language), default="en")

    workflow_status = db.Column(
        "workflow_status", ENUM(Status), index=True, default="NOT_STARTED"
    )

    jsonb_blob = db.Column("jsonb_blob", JSONB, nullable=False)

    application_json_md5 = db.Column(
        "application_json_md5",
        TEXT,
        Computed(func.md5(cast(jsonb_blob, TEXT)), persisted=True),
    )


Index(
    "ix_application_jsonb",
    AssessmentRecord.jsonb_blob,
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

# This is very fast for "=" in WHERE clauses.
Index(
    "ix_application_id_hash",
    AssessmentRecord.application_id,
    postgresql_using="hash",
)

# Links the round_id and fund_id columns by an index.
Index(
    "ix_application_round_fund_id",
    AssessmentRecord.round_id,
    AssessmentRecord.fund_id,
)
