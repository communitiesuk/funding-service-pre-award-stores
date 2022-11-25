from db.models.assessment_record import AssessmentRecord
from db.models.score import JustScore
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord
        exclude = ["jsonb_blob", "application_json_md5"]

    workflow_status = Enum(Status)
    language = Enum(Language)


class JustScoreMetadata(SQLAlchemyAutoSchema):
    """JustScoreMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = JustScore
        include_relationships = True
        load_instance = True
    
    application_id = auto_field(dump_only=True)

