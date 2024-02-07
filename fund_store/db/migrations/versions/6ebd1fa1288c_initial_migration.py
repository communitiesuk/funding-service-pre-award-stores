"""Initial migration

Revision ID: 6ebd1fa1288c
Revises:
Create Date: 2023-05-04 17:08:33.625388

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = "6ebd1fa1288c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(text("create extension if not exists ltree;"))
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assessment_field",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("field_type", sa.String(), nullable=False),
        sa.Column("display_type", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_field")),
        sa.UniqueConstraint("id", name=op.f("uq_assessment_field_id")),
    )
    op.create_table(
        "fund",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_fund")),
        sa.UniqueConstraint("short_name", name=op.f("uq_fund_short_name")),
    )
    op.create_table(
        "round",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("fund_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
        sa.Column("opens", sa.DateTime(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("assessment_deadline", sa.DateTime(), nullable=True),
        sa.Column("prospectus", sa.String(), nullable=False),
        sa.Column("privacy_notice", sa.String(), nullable=False),
        sa.Column("contact_email", sa.String(), nullable=True),
        sa.Column("contact_phone", sa.String(), nullable=True),
        sa.Column("contact_textphone", sa.String(), nullable=True),
        sa.Column("support_times", sa.String(), nullable=False),
        sa.Column("support_days", sa.String(), nullable=False),
        sa.Column("instructions", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["fund_id"], ["fund.id"], name=op.f("fk_round_fund_id_fund")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_round")),
        sa.UniqueConstraint("short_name", name=op.f("uq_round_short_name")),
    )
    op.create_table(
        "section",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("title_content_id", sa.Integer(), nullable=True),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.Column("weighting", sa.Integer(), nullable=True),
        sa.Column("path", sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_section_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_section")),
    )
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.create_index("ix_sections_path", ["path"], unique=False, postgresql_using="gist")

    op.create_table(
        "section_field",
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("field_id", sa.String(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["assessment_field.id"],
            name=op.f("fk_section_field_field_id_assessment_field"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["section.id"],
            name=op.f("fk_section_field_section_id_section"),
        ),
        sa.PrimaryKeyConstraint("section_id", "field_id", name=op.f("pk_section_field")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("section_field")
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.drop_index("ix_sections_path", postgresql_using="gist")

    op.drop_table("section")
    op.drop_table("round")
    op.drop_table("fund")
    op.drop_table("assessment_field")
    # ### end Alembic commands ###
