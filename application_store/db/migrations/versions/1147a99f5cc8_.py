"""empty message

Revision ID: 1147a99f5cc8
Revises: a0b9e8f859a9
Create Date: 2022-11-02 14:44:32.698940

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "1147a99f5cc8"
down_revision = "a0b9e8f859a9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.alter_column(
            "language", existing_type=sa.VARCHAR(), nullable=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.alter_column(
            "language", existing_type=sa.VARCHAR(), nullable=False
        )

    # ### end Alembic commands ###
