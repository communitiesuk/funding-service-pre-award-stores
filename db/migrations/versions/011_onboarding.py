"""onboarding

Revision ID: 011_onboarding
Revises: 010_proto_migration
Create Date: 2025-01-12 11:13:12.077215

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "011_onboarding"
down_revision = "010_proto_migration"
branch_labels = None
depends_on = None


def upgrade():
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
        sa.Column("type", sa.Enum("TEXT_INPUT", "TEXTAREA", "RADIOS", name="questiontype"), nullable=False),
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
        sa.Column("type", sa.Enum("TEXT_INPUT", "TEXTAREA", "RADIOS", name="questiontype"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("template_question_id", sa.Integer(), nullable=False),
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


def downgrade():
    op.drop_table("application_question")
    op.drop_table("application_section")
    op.drop_table("template_question")
    op.drop_table("template_section")
    op.drop_table("data_standard")
