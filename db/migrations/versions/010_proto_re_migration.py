"""proto re-migration

Revision ID: 010_proto_re_migration
Revises: 009_relax_flag_json_constraints
Create Date: 2025-01-12 20:14:58.576909

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "010_proto_re_migration"
down_revision = "009_relax_flag_json_constraints"
branch_labels = None
depends_on = None

fund_status_enum = ENUM("DRAFT", "LIVE", "RETIRED", name="fundstatus", create_type=False)
question_type_enum = ENUM("TEXT_INPUT", "TEXTAREA", "RADIOS", name="questiontype", create_type=False)


def upgrade():
    fund_status_enum.create(op.get_bind(), checkfirst=True)
    question_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "data_standard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_data_standard")),
        sa.UniqueConstraint("slug", name=op.f("uq_data_standard_slug")),
    )
    op.create_table(
        "template_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_template_section_slug")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_template_section")),
        sa.UniqueConstraint("slug", name=op.f("uq_template_section_slug")),
    )
    op.create_table(
        "template_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("type", question_type_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("template_section_id", sa.Integer(), nullable=False),
        sa.Column("data_standard_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_template_question_slug")),
        sa.ForeignKeyConstraint(
            ["data_standard_id"], ["data_standard.id"], name=op.f("fk_template_question_data_standard_id_data_standard")
        ),
        sa.ForeignKeyConstraint(
            ["template_section_id"],
            ["template_section.id"],
            name=op.f("fk_template_question_template_section_id_template_section"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_template_question")),
        sa.UniqueConstraint("template_section_id", "order", name="uq_tq_order_for_section"),
        sa.UniqueConstraint("template_section_id", "slug", name="uq_tq_slug_for_section"),
    )
    op.create_table(
        "application_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_application_section_slug")),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_application_section_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_application_section")),
        sa.UniqueConstraint("round_id", "slug", name="uq_as_slug_for_round"),
    )
    op.create_table(
        "application_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("type", question_type_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("template_question_id", sa.Integer(), nullable=True),
        sa.Column("data_standard_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_application_question_slug")),
        sa.ForeignKeyConstraint(
            ["data_standard_id"],
            ["data_standard.id"],
            name=op.f("fk_application_question_data_standard_id_data_standard"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["application_section.id"],
            name=op.f("fk_application_question_section_id_application_section"),
        ),
        sa.ForeignKeyConstraint(
            ["template_question_id"],
            ["template_question.id"],
            name=op.f("fk_application_question_template_question_id_template_question"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_application_question")),
        sa.UniqueConstraint("section_id", "order", name="uq_aq_order_for_section"),
        sa.UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section"),
    )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_status", fund_status_enum, nullable=True))
        batch_op.add_column(sa.Column("proto_name", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("proto_name_cy", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("proto_created_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("proto_updated_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(sa.Column("proto_prospectus_link", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("proto_apply_action_description", sa.String(), nullable=True))

    op.execute(text("UPDATE fund SET proto_status = 'LIVE'"))

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("proto_status", nullable=False)

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_start_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("proto_end_date", sa.Date(), nullable=True))
        batch_op.add_column(
            sa.Column("proto_created_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("proto_updated_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("proto_updated_date")
        batch_op.drop_column("proto_created_date")
        batch_op.drop_column("proto_end_date")
        batch_op.drop_column("proto_start_date")

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("proto_apply_action_description")
        batch_op.drop_column("proto_prospectus_link")
        batch_op.drop_column("proto_updated_date")
        batch_op.drop_column("proto_created_date")
        batch_op.drop_column("proto_name_cy")
        batch_op.drop_column("proto_name")
        batch_op.drop_column("proto_status")

    op.drop_table("application_question")
    op.drop_table("application_section")
    op.drop_table("template_question")
    op.drop_table("template_section")
    op.drop_table("data_standard")

    question_type_enum.drop(op.get_bind(), checkfirst=True)
    fund_status_enum.drop(op.get_bind(), checkfirst=True)
