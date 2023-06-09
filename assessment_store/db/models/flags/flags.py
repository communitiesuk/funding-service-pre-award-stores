"""The module containing all code related to the `flags` table
within the Postgres db.
"""
import uuid

from db import db
from db.models.flags.enums import FlagType
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Flag(db.Model):
    """Flag: The sqlalchemy-flask model class used to define the
    `flags` table in the Postgres database."""

    __tablename__ = "flags"

    id = db.Column(
        "flag_id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    flag_type = db.Column("flag_type", ENUM(FlagType), nullable=False)

    application_id = db.Column(
        "application_id", UUID, ForeignKey("assessment_records.application_id")
    )

    date_created = db.Column(
        "date_created", db.DateTime(), server_default=func.now()
    )

    user_id = db.Column("user_id", db.String(), nullable=False)

    justification = db.Column("justification", db.Text(), nullable=True)

    # section_to_flag = db.Column("section_to_flag", ARRAY(db.String(256)), nullable=True)
    sections_to_flag = db.Column(
        "sections_to_flag", ARRAY(db.String(256)), nullable=True
    )
