"""Create Application Store tables

Revision ID: 003_create_application_store
Revises: 002_create_fund_store_tables
Create Date: 2024-11-22 15:18:44.153089

"""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "003_create_application_store"
down_revision = "002_create_fund_store_tables"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "applications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.String(), nullable=False),
        sa.Column("fund_id", sa.String(), nullable=False),
        sa.Column("round_id", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("reference", sa.String(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=True),
        sa.Column("started_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM("NOT_STARTED", "IN_PROGRESS", "SUBMITTED", "COMPLETED", name="status"),
            nullable=False,
        ),
        sa.Column("date_submitted", sa.DateTime(), nullable=True),
        sa.Column("last_edited", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("language", postgresql.ENUM("en", "cy", name="language"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_applications")),
        sa.UniqueConstraint("fund_id", "round_id", "key", name="_reference"),
        sa.UniqueConstraint("reference", name=op.f("uq_applications_reference")),
    )
    op.create_table(
        "eligibility_update",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eligible", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_eligibility_update")),
    )
    op.create_table(
        "eligibility",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("form_id", sa.String(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=True),
        sa.Column("eligible", sa.Boolean(), nullable=True),
        sa.Column("application_id", sa.UUID(), nullable=False),
        sa.Column("date_submitted", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_eligibility_application_id_applications"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_eligibility")),
    )
    op.create_table(
        "end_of_application_survey_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("application_id", sa.UUID(), nullable=False),
        sa.Column("fund_id", sa.String(), nullable=False),
        sa.Column("round_id", sa.String(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column(
            "date_submitted",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_end_of_application_survey_feedback_application_id_applications"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_end_of_application_survey_feedback")),
        sa.UniqueConstraint("application_id", "page_number", name="_unique_application_page"),
    )
    op.create_table(
        "feedback",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("application_id", sa.UUID(), nullable=False),
        sa.Column("fund_id", sa.String(), nullable=False),
        sa.Column("round_id", sa.String(), nullable=False),
        sa.Column("section_id", sa.String(), nullable=False),
        sa.Column("feedback_json", sa.JSON(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("NOT_STARTED", "IN_PROGRESS", "SUBMITTED", "COMPLETED", name="status"),
            nullable=False,
        ),
        sa.Column(
            "date_submitted",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_feedback_application_id_applications"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feedback")),
        sa.UniqueConstraint("application_id", "section_id", name=op.f("uq_feedback_application_id")),
    )
    op.create_table(
        "forms",
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
        sa.Column("application_id", sa.UUID(), nullable=False),
        sa.Column("json", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("NOT_STARTED", "IN_PROGRESS", "SUBMITTED", "COMPLETED", name="status"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("has_completed", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_forms_application_id_applications"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_forms")),
        sa.UniqueConstraint("id", "name", name=op.f("uq_forms_id")),
    )
    op.create_table(
        "research_survey",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("application_id", sa.UUID(), nullable=False),
        sa.Column("fund_id", sa.String(), nullable=False),
        sa.Column("round_id", sa.String(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column(
            "date_submitted",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            name=op.f("fk_research_survey_application_id_applications"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_research_survey")),
        sa.UniqueConstraint("application_id", name=op.f("uq_research_survey_application_id")),
    )
    with op.batch_alter_table("assessment_field", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_assessment_field_id"), ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("assessment_field", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_assessment_field_id"), type_="unique")

    op.drop_table("research_survey")
    op.drop_table("forms")
    op.drop_table("feedback")
    op.drop_table("end_of_application_survey_feedback")
    op.drop_table("eligibility")
    op.drop_table("eligibility_update")
    op.drop_table("applications")
    op.execute("drop type language")
    op.execute("drop type status")
    # ### end Alembic commands ###