"""empty message

Revision ID: 91934df64d2d
Revises: 746c2c89027f
Create Date: 2023-08-25 14:09:41.123423

"""

import sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "91934df64d2d"
down_revision = "746c2c89027f"
branch_labels = None
depends_on = None


def upgrade():
    # round
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("requires_feedback", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE round
            SET requires_feedback = false
            """
        )
    )

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("requires_feedback", nullable=False)

    # section
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.add_column(sa.Column("requires_feedback", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE section
            SET requires_feedback = false
            """
        )
    )

    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.alter_column("requires_feedback", nullable=False)


def downgrade():
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.drop_column("requires_feedback")

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("requires_feedback")
