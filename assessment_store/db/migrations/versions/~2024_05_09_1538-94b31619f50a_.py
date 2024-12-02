"""Add ZeroToOne to ScoringSystem.

Revision ID: 94b31619f50a
Revises: 4bd13b6df99b
Create Date: 2024-05-09 15:38:33.124627

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "94b31619f50a"
down_revision = "4bd13b6df99b"
branch_labels = None
depends_on = None

# Define the name of the enum type
enum_name = "scoringsystem"
# Define the old options
old_options = ("OneToFive", "ZeroToThree")
# Define the new options
new_options = ("OneToFive", "ZeroToThree", "ZeroToOne")
# Create the old enum type
old_type = sa.Enum(*old_options, name=enum_name)
# Create the new enum type
new_type = sa.Enum(*new_options, name=enum_name)


def upgrade():
    # Create a temporary "_status" type, convert and drop the "old" type
    tmp_type = sa.Enum(*new_options, name="_temp_" + enum_name)
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE _temp_{enum_name}"
        f" USING scoring_system::text::_temp_{enum_name}"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE {enum_name}"
        f" USING scoring_system::text::{enum_name}"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # Logic for downgrade (reverse of upgrade)
    # Create a temporary "_status" type, convert and drop the "old" type
    tmp_type = sa.Enum(*old_options, name="_temp_" + enum_name)
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE _temp_{enum_name}"
        f" USING scoring_system::text::_temp_{enum_name}"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE assessment_round ALTER COLUMN scoring_system TYPE {enum_name}"
        f" USING scoring_system::text::{enum_name}"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
