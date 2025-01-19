"""add completed bool to section data

Revision ID: 015_add_completed_bool_to_sectio
Revises: 014_application_section_data_cas
Create Date: 2025-01-19 14:22:29.126027

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "015_add_completed_bool_to_sectio"
down_revision = "014_application_section_data_cas"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.add_column(sa.Column("completed", sa.Boolean(), nullable=True))

    op.execute("update proto_application_section_data set completed=false")

    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.alter_column("completed", existing_type=sa.Boolean(), nullable=False)


def downgrade():
    with op.batch_alter_table("proto_application_section_data", schema=None) as batch_op:
        batch_op.drop_column("completed")
