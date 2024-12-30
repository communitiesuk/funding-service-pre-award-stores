"""Allow nullable user_id in flag_update and allow editable json on assessment_records.
Add two new workflow statuses

Revision ID: "009_relax_flag_json_constraints"
Revises: "008_extend_flag_for_change_req"
Create Date: 2024-12-19 16:30:00.346479

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "009_relax_flag_json_constraints"
down_revision = "008_extend_flag_for_change_req"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("flag_update", schema=None) as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.VARCHAR(), nullable=True)

    op.execute("DROP TRIGGER IF EXISTS block_updates_on_app_blob on assessment_records")

    op.execute("alter type status add value 'CHANGE_REQUESTED' after 'COMPLETED'")
    op.execute("alter type status add value 'CHANGE_RECEIVED' after 'CHANGE_REQUESTED'")


def downgrade():
    with op.batch_alter_table("flag_update", schema=None) as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.VARCHAR(), nullable=False)
