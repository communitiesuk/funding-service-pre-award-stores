"""Makes scoring_system_id nullable

Revision ID: 006_scoring_system_id_null
Revises: 005_create_asmt_store_triggers
Create Date: 2024-12-03 15:17:11.355385

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "006_scoring_system_id_null"
down_revision = "005_create_asmt_store_triggers"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_round", schema=None) as batch_op:
        batch_op.alter_column("scoring_system_id", existing_type=sa.UUID(), nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_round", schema=None) as batch_op:
        batch_op.alter_column("scoring_system_id", existing_type=sa.UUID(), nullable=False)

    # ### end Alembic commands ###
