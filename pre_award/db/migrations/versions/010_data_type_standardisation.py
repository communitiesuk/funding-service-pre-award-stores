"""Standardising data types
 - Rename eoi_decision_schema to remove space at end of column name
 - Change owner_organisation_logo_uri to varchar

Revision ID: 010_
Revises: 009_relax_flag_json_constraints
Create Date: 2025-01-16 09:59:32.708872

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "010_"
down_revision = "009_relax_flag_json_constraints"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("eoi_decision_schema ", new_column_name="eoi_decision_schema")
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column(
            "owner_organisation_logo_uri", existing_type=sa.TEXT(), type_=sa.String(), existing_nullable=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("eoi_decision_schema", new_column_name="eoi_decision_schema ")
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column(
            "owner_organisation_logo_uri", existing_type=sa.String(), type_=sa.TEXT(), existing_nullable=True
        )

    # ### end Alembic commands ###
