from db import db
from db.models.enums.workflow_status import Status
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT


class AssessmentRecords(db.Model):
    __tablename__ = "assessment_records"

    application_id = db.Column(
        "application_id",
        db.Text(),
        primary_key=True,
    )

    short_id = db.Column(
        "short_id",
        db.Text(),
    )

    type_of_application = db.Column(
        "type_of_application",
        db.Text(),
    )

    project_name = db.Column(
        "project_name",
        db.Text(),
    )

    funding_amount_requested = db.Column(
        "funding_amount_requested",
        db.Float(),
    )

    round_id = db.Column("round_id", db.Text(), index=True)

    fund_id = db.Column("fund_id", db.Text(), index=True)

    langauge = db.Column("langauge", db.Text(), default="en")

    workflow_status = db.Column(
        "workflow_status", ENUM(Status), index=True, default="NOT_STARTED"
    )

    jsonb_blob = db.Column("jsonb_blob", JSONB)

    application_json_md5 = db.Column(
        "application_json_sha256",
        TEXT,
        Computed(func.md5(cast(jsonb_blob, TEXT)), persisted=True),
    )


# class AssessmentJsonBlobs(db.model):

#     application_id = db.Column(
# 		"application_id",
# 		db.ForeignKey(AssessmentRecords.application_id)
# 	)

#     jsonb_blob = jsonb_blob = db.Column("jsonb_blob", JSONB)

Index(
    "application_jsonb_index",
    AssessmentRecords.jsonb_blob,
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

# Index(
#     "application_jsonb_index",
#     AssessmentJsonBlobs.jsonb_blob,
#     postgresql_ops={
#         "jsonb_blob": "jsonb_path_ops",
#     },
#     postgresql_using="gin",
# )

# Index(
#     "assessment_records_id_index",
#     AssessmentJsonBlobs.application_id,
#     postgresql_using="hash",
# )

Index(
    "assessment_records_id_index",
    AssessmentRecords.application_id,
    postgresql_using="hash",
)
