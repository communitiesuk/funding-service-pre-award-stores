"""Empty message.

Revision ID: 5ce0b8e0e1b6
Revises: 190bf5378715
Create Date: 2022-11-25 14:24:40.464115

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5ce0b8e0e1b6"
down_revision = "190bf5378715"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.add_column(sa.Column("asset_type", sa.String(length=255), nullable=False))
        batch_op.create_index(
            batch_op.f("ix_assessment_records_asset_type"),
            ["asset_type"],
            unique=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_assessment_records_asset_type"))
        batch_op.drop_column("asset_type")

    # ### end Alembic commands ###
