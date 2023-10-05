"""empty message

Revision ID: 342b7a05b923
Revises: 222a1c3b6321
Create Date: 2023-10-04 10:57:01.282981

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "342b7a05b923"
down_revision = "222a1c3b6321"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_withdrawn", sa.Boolean(), nullable=False, default=False
            )
        )


def downgrade():
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_column("is_withdrawn")
