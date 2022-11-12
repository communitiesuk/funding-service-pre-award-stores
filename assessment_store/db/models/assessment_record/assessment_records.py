from db import db
from db.models.enums.workflow_status import Status
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy import DDL, event


class AssessmentRecords(db.Model):
    __tablename__ = "assessment_records"

    application_id = db.Column(
        "application_id",
        db.Text(),
        primary_key=True,
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
        index=True,
        nullable=False
    )

    project_name = db.Column(
        "project_name",
        db.Text(),
        index=True,
        nullable=False
    )

    funding_amount_requested = db.Column(
        "funding_amount_requested",
        db.Float(),
        index=True,
        nullable=False
    )

    round_id = db.Column("round_id", db.Text(), index=True,
        nullable=False)

    fund_id = db.Column("fund_id", db.Text(), index=True,
        nullable=False)

    langauge = db.Column("langauge", db.Text(), default="en",
        nullable=False)

    workflow_status = db.Column(
        "workflow_status", ENUM(Status), index=True, default="NOT_STARTED"
    )

    jsonb_blob = db.Column("jsonb_blob", JSONB,
        nullable=False)

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

# A method of imposing a database level block to mutating application json.

func = DDL(
    """
CREATE FUNCTION block_blob_mutate()
RETURNS TRIGGER 
LANGUAGE PLPGSQL
AS
$$
BEGIN
	IF NEW.jsonb_blob <> OLD.jsonb_blob THEN
	RAISE EXCEPTION 'Cannot mutate application json.';
	END IF;
	RETURN NEW;
END;
$$"""
)

trigger = DDL(
    """CREATE TRIGGER block_updates_on_app_blob
BEFORE UPDATE
ON assessment_records
FOR EACH ROW
EXECUTE PROCEDURE block_blob_mutate();"""
)

event.listen(
    AssessmentRecords.__table__,
    "after_create",
    func.execute_if(dialect="postgresql"),
)

event.listen(
    AssessmentRecords.__table__,
    "after_create",
    trigger.execute_if(dialect="postgresql"),
)
