import uuid
from typing import List

from db import db
from db.models.round import Round
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean


BaseModel: DefaultMeta = db.Model


class Fund(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    name_json = Column("name_json", JSON(none_as_null=True), nullable=False, unique=False)
    title_json = Column("title_json", JSON(none_as_null=True), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=True)
    description_json = Column("description_json", JSON(none_as_null=True), nullable=False, unique=False)
    rounds: Mapped[List["Round"]] = relationship("Round")
    welsh_available = Column("welsh_available", Boolean, default=False, nullable=False)
    owner_organisation_name = Column("owner_organisation_name", db.String(), nullable=False, unique=False)
    owner_organisation_shortname = Column("owner_organisation_shortname", db.String(), nullable=False, unique=False)
    owner_organisation_logo_uri = Column("owner_organisation_logo_uri", db.Text(), nullable=True, unique=False)
