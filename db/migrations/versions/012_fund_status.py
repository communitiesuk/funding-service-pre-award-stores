"""fund status

Revision ID: 012_fund_status
Revises: 011_onboarding
Create Date: 2025-01-12 14:48:17.489346

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "012_fund_status"
down_revision = "011_onboarding"
branch_labels = None
depends_on = None

fund_status_enum = sa.Enum("DRAFT", "LIVE", "RETIRED", name="fundstatus")


def upgrade():
    fund_status_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_status", fund_status_enum, nullable=True))

    op.execute("UPDATE fund SET proto_status = 'LIVE'")

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("proto_status", nullable=False)


def downgrade():
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("proto_status")

    fund_status_enum.drop(op.get_bind(), checkfirst=True)
