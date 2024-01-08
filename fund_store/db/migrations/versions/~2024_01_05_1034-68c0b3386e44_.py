"""empty message

Revision ID: 68c0b3386e44
Revises: e8552f721767
Create Date: 2024-01-05 10:34:45.138308

"""
import sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "68c0b3386e44"
down_revision = "e8552f721767"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("application_reminder_sent", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(sa.Column("reminder_date", sa.DateTime(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE round
            SET application_reminder_sent = true
            WHERE id NOT in ('4efc3263-aefe-4071-b5f4-0910abec12d2')
            """
        )
    )
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE round
            SET application_reminder_sent = false
            WHERE id in ('4efc3263-aefe-4071-b5f4-0910abec12d2')
            """
        )
    )
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column(
            sa.Column("application_reminder_sent", sa.Boolean(), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("reminder_date")
        batch_op.drop_column("application_reminder_sent")

    # ### end Alembic commands ###
