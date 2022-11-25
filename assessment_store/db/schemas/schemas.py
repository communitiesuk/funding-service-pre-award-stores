from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    workflow_status = Enum(Status)
    language = Enum(Language)
