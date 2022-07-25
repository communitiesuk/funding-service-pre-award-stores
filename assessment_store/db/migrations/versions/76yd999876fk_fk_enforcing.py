"""empty message

Revision ID: 76yd999876fk
Revises: 91ed555648be
Create Date: 2022-07-15 14:02:23.602237

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op


# revision identifiers, used by Alembic.
revision = "76yd999876fk"
down_revision = "91ed555648be"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("scores_justifications")
    op.create_table(
        "scores_justifications",
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("assessment_id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
        sa.Column("assessor_user_id", sa.String(length=255), nullable=True),
        sa.Column("sub_criteria_id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("justification", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sub_criteria_id"],
            ["sub_criteria.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("scores_justifications")
    op.create_table(
    "scores_justifications",
    sa.Column(
        "id",
        sqlalchemy_utils.types.uuid.UUIDType(binary=False),
        nullable=False,
    ),
    sa.Column("created_at", sa.DateTime(), nullable=True),
    sa.Column("assessment_id", sa.String(length=255), nullable=True),
    sa.Column("assessor_user_id", sa.String(length=255), nullable=True),
    sa.Column("sub_criteria_id", sa.String(length=255), nullable=True),
    sa.Column("score", sa.Integer(), nullable=True),
    sa.Column("justification", sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(
        ["assessment_id"],
        ["assessment.id"],
    ),
    sa.ForeignKeyConstraint(
        ["sub_criteria_id"],
        ["sub_criteria.id"],
    ),
    sa.PrimaryKeyConstraint("id"),
    )
