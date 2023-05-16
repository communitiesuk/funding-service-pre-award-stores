import uuid
from typing import List

from db import db
from db.models.round import Round
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


BaseModel: DefaultMeta = db.Model


class Fund(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    name = Column("name", db.String(), nullable=False, unique=False)
    title = Column("title", db.String(), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=True)
    description = Column("description", db.String(), nullable=False, unique=False)
    rounds: Mapped[List["Round"]] = relationship("Round")
