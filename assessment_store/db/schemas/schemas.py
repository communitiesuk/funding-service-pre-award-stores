from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from db.models.assessment_record.tag_association import TagAssociation
from db.models.comment import Comment
from db.models.comment import CommentsUpdate
from db.models.comment.enums import CommentType
from db.models.flags.assessment_flag import AssessmentFlag
from db.models.flags.flag_update import FlagUpdate
from db.models.qa_complete import QaComplete
from db.models.score import AssessmentRound
from db.models.score import Score
from db.models.tag.tag_types import TagType
from db.models.tag.tags import Tag
from marshmallow import fields
from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow.fields import Enum
from marshmallow.fields import Field
from marshmallow.fields import Integer
from marshmallow.fields import Method
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import UUID
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy rows
    into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    workflow_status = Enum(Status)
    language = Enum(Language)
    organisation_name = String()
    funding_type = String()
    local_authority = String()
    cohort = String()
    is_project_regional = Boolean()
    lead_contact_email = String()
    team_in_place = Boolean()
    datasets = Boolean()
    publish_datasets = String()
    flags = Nested("AssessmentFlagSchema", many=True)
    qa_complete = Nested("QaCompleteMetadata", many=True)
    tag_associations = Nested("TagAssociationNestedSchema", many=True)


class ScoreMetadata(SQLAlchemyAutoSchema):
    """ScoreMetadata The marshmallow class used to turn SQLAlchemy rows into json
    for return in http responses."""

    class Meta:
        model = Score
        include_relationships = True
        load_instance = True

    application_id = auto_field(dump_only=True)


class CommentMetadata(SQLAlchemyAutoSchema):
    """CommentMetadata The marshmallow class used to turn SQLAlchemy rows into
    json for return in http responses."""

    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    comment_type = Enum(CommentType)
    application_id = auto_field(dump_only=True)
    updates = Nested("CommentsUpdateSchema", many=True)


class CommentsUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CommentsUpdate


class QaCompleteMetadata(SQLAlchemyAutoSchema):
    """QaCompleteMetadata The marshmallow class used to turn SQLAlchemy rows into
    json for return in http responses."""

    class Meta:
        model = QaComplete
        include_relationships = True
        load_instance = True

    application_id = auto_field(dump_only=True)


class AssessorTaskListMetadata(AssessmentRecordMetadata):
    """AssessorTaskListMetadata The marshmallow class used to turn SQLAlchemy rows
    into json for return in http responses."""

    short_id = auto_field(data_key="short_id")
    date_submitted = Field(
        data_key="date_submitted", attribute="jsonb_blob.date_submitted"
    )


class AssessmentSubCriteriaMetadata(AssessmentRecordMetadata):
    """AssessmentSubCriteriaMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

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


class TagAssociationNestedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TagAssociation
        fields = ("id", "user_id", "associated", "tag", "created_at")

    tag = Nested("TagNestedSchema")


class JoinedTagAssociationSchema(SQLAlchemyAutoSchema):
    tag_id = UUID()
    type_id = UUID()
    value = String()
    purpose = String()
    associated = Boolean()
    application_id = UUID()
    user_id = UUID()
    created_at = String()

    class Meta:
        model = None  # Set the model to None since it doesn't directly map to a single model


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag


class TagNestedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        fields = ("id", "value", "active", "creator_user_id", "tag_type")

    def get_tag_type(self, obj):
        return {"id": obj.tag_type.id, "purpose": obj.tag_type.purpose}

    tag_type = Method("get_tag_type")


class JoinedTagSchema(SQLAlchemyAutoSchema):
    type_id = UUID()
    purpose = String()
    description = String()
    tag_association_count = Integer()

    class Meta:
        model = Tag


class AssessmentRoundMetadata(SQLAlchemyAutoSchema):
    scoring_system = fields.Function(lambda obj: obj.scoring_system.name)

    class Meta:
        model = AssessmentRound
