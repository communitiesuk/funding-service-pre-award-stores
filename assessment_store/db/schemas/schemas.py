from db.models.assessment_record import AssessmentRecords
from db.models.assessment_record.enums import Status
from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    class Meta:
        model = AssessmentRecords
        exclude = ["jsonb_blob", "application_json_md5"]

    workflow_status = Enum(Status)
