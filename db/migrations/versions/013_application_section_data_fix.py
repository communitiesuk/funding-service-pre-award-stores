"""application section data fix

Revision ID: 013_application_section_data_fix
Revises: 012_application_data_table
Create Date: 2025-01-19 13:16:47.883507

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "013_application_section_data_fix"
down_revision = "012_application_data_table"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.add_column(sa.Column("section_id", sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(
            batch_op.f("uq_proto_application_section_data_proto_application_id"), ["proto_application_id", "section_id"]
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_application_section_data_section_id_application_section"),
            "application_section",
            ["section_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_proto_application_section_data_section_id_application_section"), type_="foreignkey"
        )
        batch_op.drop_constraint(batch_op.f("uq_proto_application_section_data_proto_application_id"), type_="unique")
        batch_op.drop_column("section_id")
