"""The module containing all code related to the `comments` table
within the Postgres db.
"""

import uuid
from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import func
from db.models.comment.enums import CommentType

class Comment(db.Model):
    """Comment The sqlalchemy-flask model class used to define the
    `Comment` table in the Postgres database."""

    __tablename__ = "comments"

    id = db.Column(
        "comment_id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    application_id = db.Column(
        "application_id", UUID, ForeignKey("assessment_records.application_id")
    )

    comment = db.Column(
        "comment", db.Text(), nullable=False
    )

    user_id = db.Column("user_id", db.String(), nullable=False)

    date_created = db.Column(
        "date_created", db.DateTime(), server_default=func.now()
    )

    sub_criteria_id = db.Column(
        "sub_criteria_id", db.String(), nullable=True
    )

    comment_type = db.Column(
        "comment_type", ENUM(CommentType), nullable=True
    )

    theme_id = db.Column(
        "theme_id", db.String(), nullable=True
    )