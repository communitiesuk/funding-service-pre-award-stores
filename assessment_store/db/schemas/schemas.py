from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from marshmallow import post_dump
from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    workflow_status = Enum(Status)
    language = Enum(Language)


ASSESSOR_TASK_LIST_METADATA_FIELDS = (
    "short_id",
    "project_name",
    "workflow_status",
    "jsonb_blob",
    "fund_id",
    "round_id",
)


class AssessorTaskListMetadata(AssessmentRecordMetadata):
    """AssessorTaskListMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.

    Fields are:
    - project_name
    - project_reference (short_id)
    - workflow_status
    - date_submitted
    - fund_id
    - round_id
    """

    class Meta:
        model = AssessmentRecord
        exclude = tuple(
            field
            for field in AssessmentRecord.__table__.columns.keys()
            if field not in ASSESSOR_TASK_LIST_METADATA_FIELDS
        )

    @post_dump
    def discard_irrelevant_fields(self, item, many, **kwargs):
        """Discard irrelevant fields from the jsonb_blob."""
        item["date_submitted"] = item["jsonb_blob"]["date_submitted"]
        item["project_reference"] = item["short_id"]
        del item["short_id"]
        del item["jsonb_blob"]
        return item
