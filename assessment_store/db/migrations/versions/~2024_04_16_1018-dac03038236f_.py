"""Setting is_withdrawn to nullable=True, and renaming scoring system enum.

Revision ID: dac03038236f
Revises: 6c8205510de6
Create Date: 2024-04-16 10:18:08.511694

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dac03038236f"
down_revision = "6c8205510de6"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.alter_column("is_withdrawn", existing_type=sa.BOOLEAN(), nullable=False)

    op.execute("CREATE TYPE scoringsystem AS ENUM ('OneToFive', 'ZeroToThree')")
    op.execute(
        "ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE scoringsystem"
        " USING scoring_system::text::scoringsystem"
    )
    op.execute("DROP TYPE scoring_system_enum")


def downgrade():
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.alter_column("is_withdrawn", existing_type=sa.BOOLEAN(), nullable=True)
    op.execute("CREATE TYPE scoring_system_enum AS ENUM ('OneToFive', 'ZeroToThree')")
    op.execute(
        "ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE scoring_system_enum "
        "USING scoring_system::text::scoring_system_enum"
    )
    op.execute("DROP TYPE scoringsystem")
