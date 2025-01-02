"""Create feedback_message column

Revision ID: 010_add_feedback_message
Revises: 009_relax_flag_json_constraints
Create Date: 2024-11-30 19:33:00.710210

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "010_add_feedback_message"
down_revision = "009_relax_flag_json_constraints"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.add_column(sa.Column("feedback_message", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.drop_column("feedback_message")
