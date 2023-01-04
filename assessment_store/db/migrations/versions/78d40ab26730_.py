"""empty message

Revision ID: 78d40ab26730
Revises: 4208ac886129
Create Date: 2022-12-23 10:04:12.923579

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "78d40ab26730"
down_revision = "4208ac886129"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "flags",
        sa.Column("flag_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("justification", sa.Text(), nullable=False),
        sa.Column("section_to_flag", sa.Text(), nullable=False),
        sa.Column(
            "flag_type",
            postgresql.ENUM(
                "FLAGGED", "STOPPED", "QA_COMPLETED", name="flagtype"
            ),
            nullable=False,
        ),
        sa.Column(
            "resolution_reason",
            postgresql.ENUM(
                "QUERY_RESOLVED", "STOP_ASSESSMENT", name="resolutiontype"
            ),
            nullable=True,
        ),
        sa.Column("application_id", postgresql.UUID(), nullable=True),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name=op.f("fk_flags_application_id_assessment_records"),
        ),
        sa.PrimaryKeyConstraint("flag_id", name=op.f("pk_flags")),
    )


def downgrade():
    op.drop_table("flags")
