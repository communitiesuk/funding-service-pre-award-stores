"""round draft column

Revision ID: 011_round_draft_column
Revises: 010_proto_re_migration
Create Date: 2025-01-18 14:50:36.675967

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = "011_round_draft_column"
down_revision = "010_proto_re_migration"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_draft", sa.Boolean(), nullable=True))

    op.execute(text("update round set proto_draft = false where proto_draft is null"))

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("proto_draft", existing_type=sa.Boolean(), nullable=False)


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("proto_draft")
