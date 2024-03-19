"""empty message

Revision ID: 108033941f74
Revises: 6928bebf9d54
Create Date: 2023-07-11 14:04:01.128224

"""

import sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "108033941f74"
down_revision = "6928bebf9d54"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("all_uploaded_documents_section_available", sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            """
            UPDATE fund
            SET all_uploaded_documents_section_available = false
            """
        )
    )

    connection.execute(
        sqlalchemy.text(
            """
            UPDATE fund
            SET all_uploaded_documents_section_available = true
            WHERE short_name = 'COF'
            """
        )
    )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("all_uploaded_documents_section_available", nullable=False)


def downgrade():
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("all_uploaded_documents_section_available")
