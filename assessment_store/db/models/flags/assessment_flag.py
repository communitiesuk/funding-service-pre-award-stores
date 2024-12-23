from uuid import uuid4

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, UUID
from sqlalchemy.orm import relationship

from assessment_store.db.models.flags.flag_update import FlagStatus
from db import db

BaseModel: DefaultMeta = db.Model


class AssessmentFlag(BaseModel):
    def __init__(
        self,
        application_id,
        latest_status,
        latest_allocation,
        sections_to_flag,
        updates,
        **kwargs,
    ):
        self.application_id = application_id
        self.latest_allocation = latest_allocation
        self.latest_status = latest_status
        self.sections_to_flag = sections_to_flag
        self.updates = updates
        if "id" in kwargs:
            self.id = kwargs["id"]

    __tablename__ = "assessment_flag"

    id = Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    application_id = Column(
        "application_id",
        UUID(as_uuid=True),
        ForeignKey("assessment_records.application_id"),
    )
    latest_status = Column("latest_status", ENUM(FlagStatus))
    latest_allocation = Column("latest_allocation", String)
    sections_to_flag = db.Column("sections_to_flag", ARRAY(db.String(256)), nullable=True)
    updates = relationship("FlagUpdate", lazy="selectin")
