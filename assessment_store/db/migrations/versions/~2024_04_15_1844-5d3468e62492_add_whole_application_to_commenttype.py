"""Add WHOLE_APPLICATION to CommentType.

Revision ID: 5d3468e62492
Revises: 6c8205510de6
Create Date: 2024-04-15 18:44:34.874758

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "5d3468e62492"
down_revision = "6c8205510de6"
branch_labels = None
depends_on = None

# Define the name of the enum type
enum_name = "commenttype"
# Define the old options
old_options = ("COMMENT",)
# Define the new options
new_options = ("COMMENT", "WHOLE_APPLICATION")
# Create the old enum type
old_type = sa.Enum(*old_options, name=enum_name)
# Create the new enum type
new_type = sa.Enum(*new_options, name=enum_name)


def upgrade():
    # Create a temporary "_status" type, convert and drop the "old" type
    tmp_type = sa.Enum(*new_options, name="_temp_" + enum_name)
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE comments ALTER COLUMN comment_type TYPE _temp_{enum_name}"
        f" USING comment_type::text::_temp_{enum_name}"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE comments ALTER COLUMN comment_type TYPE {enum_name}" f" USING comment_type::text::{enum_name}"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # Logic for downgrade (reverse of upgrade)
    # Create a temporary "_status" type, convert and drop the "old" type
    tmp_type = sa.Enum(*old_options, name="_temp_" + enum_name)
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE comments ALTER COLUMN comment_type TYPE _temp_{enum_name}"
        f" USING comment_type::text::_temp_{enum_name}"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        f"ALTER TABLE comments ALTER COLUMN comment_type TYPE {enum_name}" f" USING comment_type::text::{enum_name}"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
