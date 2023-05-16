import uuid

from db import db
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID


BaseModel: DefaultMeta = db.Model


class Round(BaseModel):
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
    title = Column("title", db.String(), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=True)
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
