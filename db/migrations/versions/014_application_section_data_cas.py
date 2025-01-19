"""application section data cascade

Revision ID: 014_application_section_data_cas
Revises: 013_application_section_data_fix
Create Date: 2025-01-19 13:33:54.015274

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "014_application_section_data_cas"
down_revision = "013_application_section_data_fix"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.drop_constraint("fk_proto_application_section_data_proto_application_id__21b3", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_application_section_data_proto_application_id__21b3"),
            "proto_application",
            ["proto_application_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_proto_application_section_data_proto_application_id__21b3"), type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_proto_application_section_data_proto_application_id__21b3",
            "proto_application",
            ["proto_application_id"],
            ["id"],
        )
