"""empty message.

Revision ID: 5b6e2e7c4ad8
Revises: 190bf5378715
Create Date: 2022-11-23 12:17:42.422276
"""
from alembic import op
from alembic_utils.pg_extension import PGExtension

# revision identifiers, used by Alembic.
revision = "5b6e2e7c4ad8"
down_revision = "190bf5378715"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    public_pg_trgm = PGExtension(schema="public", signature="pg_trgm")
    op.create_entity(public_pg_trgm)

    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.create_index(
            "ix_short_id",
            ["short_id"],
            unique=False,
            postgresql_ops={"short_id": "gin_trgm_ops"},
            postgresql_using="gin",
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_index(
            "ix_short_id",
            postgresql_ops={"short_id": "gin_trgm_ops"},
            postgresql_using="gin",
        )

    public_pg_trgm = PGExtension(schema="public", signature="pg_trgm")

    op.drop_entity(public_pg_trgm)

    # ### end Alembic commands ###
