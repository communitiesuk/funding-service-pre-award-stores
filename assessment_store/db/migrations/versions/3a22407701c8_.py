"""Empty message.

Revision ID: 3a22407701c8
Revises: 99ad87a4f888
Create Date: 2023-01-09 16:06:23.980091

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3a22407701c8"
down_revision = "99ad87a4f888"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE flagtype ADD VALUE 'RESOLVED'")
    op.drop_column("flags", "resolution_reason")
    op.execute("DROP TYPE resolutiontype;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE flagtype RENAME TO flagtype_old")
    op.execute("CREATE TYPE flagtype AS ENUM('FLAGGED', 'STOPPED', 'QA_COMPLETED')")
    op.execute(("ALTER TABLE flags ALTER COLUMN flag_type TYPE flagtype USING" " flag_type::text::flagtype"))
    op.execute("DROP TYPE flagtype_old;")

    resolution_type_enum = postgresql.ENUM("QUERY_RESOLVED", "STOP_ASSESSMENT", name="resolutiontype")
    resolution_type_enum.create(op.get_bind())
    op.add_column(
        "flags",
        sa.Column(
            "resolution_reason",
            resolution_type_enum,
            autoincrement=False,
            nullable=True,
        ),
    )

    # ### end Alembic commands ###
