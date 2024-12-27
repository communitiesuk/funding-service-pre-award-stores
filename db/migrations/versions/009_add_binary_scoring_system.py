"""Adds a binary scoring system to allow a simple accept/reject option

Revision ID: "009_add_binary_scoring_system"
Revises: "008_extend_flag_for_change_req"
Create Date: 2024-12-19 16:30:00.346479

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "009_add_binary_scoring_system"
down_revision = "008_extend_flag_for_change_req"
branch_labels = None
depends_on = None

zero_to_one_id = "40d10744-b0c1-4af0-9cb9-df1058a3e930"


def upgrade():
    op.execute(
        sa.text(
            "INSERT INTO scoring_system (id, scoring_system_name, minimum_score, maximum_score) "
            "VALUES (:id, 'ZeroToOne', 0, 1)"
        ).bindparams(id=zero_to_one_id)
    )


def downgrade():
    op.execute(sa.text("DELETE FROM scoring_system where id=:id").bindparams(id=zero_to_one_id))
