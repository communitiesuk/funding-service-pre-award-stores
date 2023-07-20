from db.models import Flag
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from db.models.assessment_record.tag_association import TagAssociation
from db.models.comment import Comment
from db.models.comment.enums import CommentType
from db.models.flags.enums import FlagType
from db.models.flags_v2.assessment_flag import AssessmentFlag
from db.models.flags_v2.flag_update import FlagUpdate
from db.models.qa_complete import QaComplete
from db.models.score import Score
from db.models.tag.tag_types import TagType
from db.models.tag.tags import Tag
from marshmallow import fields
from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow.fields import Enum
from marshmallow.fields import Field
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import UUID
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    workflow_status = Enum(Status)
    language = Enum(Language)
    flags = Nested(
        "FlagMetadata", many=True
    )  # TODO: Retrieve only latest flag
    organisation_name = String()
    funding_type = String()
    local_authority = String()
    flags_v2 = Nested("AssessmentFlagSchema", many=True)
    qa_complete = Nested("QaCompleteMetadata", many=True)


class ScoreMetadata(SQLAlchemyAutoSchema):
    """ScoreMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Score
        include_relationships = True
        load_instance = True

    application_id = auto_field(dump_only=True)


class CommentMetadata(SQLAlchemyAutoSchema):
    """CommentMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    comment_type = Enum(CommentType)
    application_id = auto_field(dump_only=True)


class FlagMetadata(SQLAlchemyAutoSchema):
    """CommentMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Flag
        include_relationships = True
        load_instance = True

    flag_type = Enum(FlagType)
    application_id = auto_field(dump_only=True)


class QaCompleteMetadata(SQLAlchemyAutoSchema):
    """QaCompleteMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = QaComplete
        include_relationships = True
        load_instance = True

    application_id = auto_field(dump_only=True)


class AssessorTaskListMetadata(AssessmentRecordMetadata):
    """AssessorTaskListMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    short_id = auto_field(data_key="short_id")
    date_submitted = Field(
        data_key="date_submitted", attribute="jsonb_blob.date_submitted"
    )


class AssessmentSubCriteriaMetadata(AssessmentRecordMetadata):
    """AssessmentSubCriteriaMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    funding_amount_requested = auto_field(data_key="funding_amount_requested")
    project_name = auto_field(data_key="project_name")
    fund_id = auto_field(data_key="fund_id")
    workflow_status = Enum(Status)


class ProgressSchema(Schema):
    application_id = fields.Str()
    scored_sub_criterias = fields.Int()


class AssessmentFlagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AssessmentFlag

    application_id = auto_field(dump_only=True)
    updates = Nested("FlagUpdateSchema", many=True)


class FlagUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FlagUpdate


class TagTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TagType


class TagAssociationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TagAssociation
        fields = ("id", "tag_id", "application_id")


class JoinedTagAssociationSchema(SQLAlchemyAutoSchema):
    tag_id = UUID()
    type_id = UUID()
    value = String()
    purpose = String()
    associated = Boolean()
    application_id = UUID()
    user_id = UUID()

    class Meta:
        model = None  # Set the model to None since it doesn't directly map to a single model


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag


class JoinedTagSchema(SQLAlchemyAutoSchema):

    type_id = UUID()
    purpose = String()
    description = String()

    class Meta:
        model = Tag
