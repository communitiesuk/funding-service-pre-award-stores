"""empty message

Revision ID: ba5e693514cd
Revises:
Create Date: 2022-06-09 17:08:14.809145

"""
import sqlalchemy as sa
from alembic import op
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "ba5e693514cd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment",
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("application_id", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assessment_application_id"),
        "assessment",
        ["application_id"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_assessment_application_id"), table_name="assessment"
    )
    op.drop_table("assessment")
    # ### end Alembic commands ###
