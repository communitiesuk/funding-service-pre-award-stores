import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db import db

BaseModel: DefaultMeta = db.Model


class Event(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    round_id = Column(
        "round_id",
        UUID(as_uuid=True),
        ForeignKey("round.id"),
        nullable=False,
    )
    type = Column("type", db.String(), nullable=False, unique=False)
    activation_date = Column("activation_date", DateTime(), nullable=False)
    processed = Column("processed", db.Boolean, default=False, nullable=False)
