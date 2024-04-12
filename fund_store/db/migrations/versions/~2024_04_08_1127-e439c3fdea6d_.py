"""empty message

Revision ID: e439c3fdea6d
Revises: 7b877df0bd36
Create Date: 2024-04-08 11:27:02.139384

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e439c3fdea6d"
down_revision = "7b877df0bd36"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("contact_us_banner_json", sa.JSON(none_as_null=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("contact_us_banner_json")

    # ### end Alembic commands ###
