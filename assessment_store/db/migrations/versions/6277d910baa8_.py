"""empty message

Revision ID: 6277d910baa8
Revises: 4bdc171458b2
Create Date: 2023-07-12 11:09:23.553438

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6277d910baa8"
down_revision = "4bdc171458b2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "qa_complete",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "application_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["assessment_records.application_id"],
            name=op.f("fk_qa_complete_application_id_assessment_records"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_qa_complete")),
    )

    op.execute("ALTER TYPE flagstatus RENAME TO flagstatus_old")
    op.execute(
        "CREATE TYPE flagstatus AS ENUM ('RAISED', 'STOPPED', 'RESOLVED')"
    )
    op.execute(
        "ALTER TABLE flag_update ALTER COLUMN status TYPE flagstatus USING status::text::flagstatus"
    )
    op.execute(
        "ALTER TABLE assessment_flag ALTER COLUMN latest_status TYPE flagstatus USING latest_status::text::flagstatus"
    )
    op.execute("DROP TYPE flagstatus_old")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table("qa_complete")

    op.execute("ALTER TYPE flagstatus RENAME TO flagstatus_old")
    op.execute(
        "CREATE TYPE flagstatus AS ENUM ('RAISED', 'STOPPED', 'QA_COMPLETE', 'RESOLVED')"
    )
    op.execute(
        "ALTER TABLE flag_update ALTER COLUMN status TYPE flagstatus USING status::text::flagstatus"
    )
    op.execute(
        "ALTER TABLE assessment_flag ALTER COLUMN latest_status TYPE flagstatus USING latest_status::text::flagstatus"
    )
    op.execute("DROP TYPE flagstatus_old")
    # ### end Alembic commands ###
