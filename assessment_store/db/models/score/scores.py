"""The module containing all code related to the `scores` table
within the Postgres db.
"""
import uuid
from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Score(db.Model):
    """Score The sqlalchemy-flask model class used to define the
    `scores` table in the Postgres database."""

    __tablename__ = "scores"

    id = db.Column(
        "score_id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    score = db.Column(
        "score", db.Integer(), nullable=False
    )

    justification = db.Column(
        "justification", db.Text(), nullable=False
    )

    application_id = db.Column(
        "application_id", UUID, ForeignKey("assessment_records.application_id")
    )

    date_created = db.Column(
        "date_created", db.DateTime(), server_default=func.now()
    )

    sub_criteria_id = db.Column(
        "sub_criteria_id", db.String(),  nullable=False
    )

    user_id = db.Column("user_id", db.String(), nullable=False)
