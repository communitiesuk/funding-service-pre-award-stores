"""empty message

Revision ID: 00f23b8cbe8b
Revises: 024379c68dfe
Create Date: 2023-07-27 14:01:18.700363

"""
import sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "00f23b8cbe8b"
down_revision = "4463ff0b0e9c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("application_fields_download_available", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE round
            SET application_fields_download_available = false
            """
        )
    )

    connection.execute(
        sqlalchemy.text(
            """
            UPDATE round
            SET application_fields_download_available = true
            WHERE short_name = 'R3W1'
            """
        )
    )

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("application_fields_download_available", nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("application_fields_download_available")

    # ### end Alembic commands ###
