import random
import string
import uuid

from db import db
from db.models.application.enums import Language, Status
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils.types import UUIDType


class Applications(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    account_id = db.Column("account_id", db.String(), nullable=False)
    fund_id = db.Column("fund_id", db.String(), nullable=False)
    round_id = db.Column("round_id", db.String(), nullable=False)
    key = db.Column("key", db.String(), nullable=False)
    language = db.Column("language", ENUM(Language), nullable=True)
    reference = db.Column("reference", db.String(), nullable=False, unique=True)
    project_name = db.Column(
        "project_name",
        db.String(),
        nullable=True,
    )
    started_at = db.Column("started_at", DateTime(), server_default=func.now())
    status = db.Column("status", ENUM(Status), default="NOT_STARTED", nullable=False)
    date_submitted = db.Column("date_submitted", DateTime())
    last_edited = db.Column("last_edited", DateTime(), server_default=func.now())
    forms = relationship("Forms")

    __table_args__ = (
        db.UniqueConstraint("fund_id", "round_id", "key", name="_reference"),
    )

    def as_dict(self):
        date_submitted = (
            self.date_submitted.isoformat() if self.date_submitted else "null"
        )
        return {
            "id": str(self.id),
            "account_id": self.account_id,
            "round_id": self.round_id,
            "fund_id": self.fund_id,
            "language": self.language.name if self.language else "en",
            "reference": self.reference,
            "project_name": self.project_name or None,
            "started_at": self.started_at.isoformat(),
            "status": self.status.name,
            "last_edited": (self.last_edited or self.started_at).isoformat(),
            "date_submitted": date_submitted,
        }
