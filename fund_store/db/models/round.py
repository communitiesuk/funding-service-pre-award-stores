import uuid

from db import db
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Boolean


BaseModel: DefaultMeta = db.Model


class Round(BaseModel):
    __table_args__ = (UniqueConstraint("fund_id", "short_name"),)
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    # fund_id: Mapped[UUID] = mapped_column(ForeignKey("fund.id"))
    fund_id = Column(
        "fund_id",
        UUID(as_uuid=True),
        ForeignKey("fund.id"),
        nullable=False,
    )
    title_json = Column(
        "title_json", JSON(none_as_null=True), nullable=False, unique=False
    )
    short_name = Column("short_name", db.String(), nullable=False, unique=False)
    opens = Column("opens", DateTime())
    deadline = Column("deadline", DateTime())
    assessment_deadline = Column("assessment_deadline", DateTime())
    prospectus = Column("prospectus", db.String(), nullable=False, unique=False)
    privacy_notice = Column("privacy_notice", db.String(), nullable=False, unique=False)
    contact_email = Column("contact_email", db.String(), nullable=True, unique=False)
    contact_phone = Column("contact_phone", db.String(), nullable=True, unique=False)
    contact_textphone = Column(
        "contact_textphone", db.String(), nullable=True, unique=False
    )
    support_times = Column("support_times", db.String(), nullable=False, unique=False)
    support_days = Column("support_days", db.String(), nullable=False, unique=False)
    instructions = Column("instructions", db.String(), nullable=False, unique=False)
    feedback_link = Column("feedback_link", db.String(), unique=False)
    project_name_field_id = Column(
        "project_name_field_id", db.String(), unique=False, nullable=False
    )
    application_guidance = Column(
        "application_guidance", db.String(), nullable=True, unique=False
    )
    guidance_url = Column("guidance_url", db.String(), nullable=True, unique=False)
    all_uploaded_documents_section_available = Column(
        "all_uploaded_documents_section_available",
        Boolean,
        default=False,
        nullable=False,
    )
    application_fields_download_available = Column(
        "application_fields_download_available",
        db.Boolean,
        default=False,
        nullable=False,
    )
    display_logo_on_pdf_exports = Column(
        "display_logo_on_pdf_exports",
        db.Boolean,
        default=False,
        nullable=False,
    )
    mark_as_complete_enabled = Column(
        "mark_as_complete_enabled",
        db.Boolean,
        default=False,
        nullable=False,
    )
    feedback_survey_config = Column(
        "feedback_survey_config", JSON(none_as_null=True), nullable=True, unique=False
    )
    eligibility_config = Column(
        "eligibility_config", JSON(none_as_null=True), nullable=True, unique=False
    )
