"""application data table

Revision ID: 012_application_data_table
Revises: 011_round_draft_column
Create Date: 2025-01-18 20:41:40.891633

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "012_application_data_table"
down_revision = "011_round_draft_column"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "proto_application",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("fake", sa.Boolean(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], name=op.f("fk_proto_application_account_id_account")),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_proto_application_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_application")),
    )
    op.create_table(
        "proto_application_section_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("proto_application_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["proto_application_id"],
            ["proto_application.id"],
            name=op.f("fk_proto_application_section_data_proto_application_id__21b3"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_application_section_data")),
    )


def downgrade():
    op.drop_table("proto_application_section_data")
    op.drop_table("proto_application")
