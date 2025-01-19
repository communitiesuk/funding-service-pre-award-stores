"""add completed bool to section data

Revision ID: 016_copy_round_dates
Revises: 015_add_completed_bool_to_sectio
Create Date: 2025-01-19 14:22:29.126027

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "016_copy_round_dates"
down_revision = "015_add_completed_bool_to_sectio"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE round SET proto_start_date = opens::date, proto_end_date = deadline::date")


def downgrade():
    pass
