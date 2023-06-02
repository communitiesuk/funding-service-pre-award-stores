"""

Revision ID: 5fe9a48b7739
Revises: eada7e01b1c2
Create Date: 2023-05-31 18:25:08.673303

FS-2701: Purpose of this script is converting the form_name column to jsonb, and populating it with the existing values.
This is similar to db/migrations/versions/eada7e01b1c2_.py:3, but for the form_name table.  We also migrate the
section title to jsonb.  The downgrade does the exact opposite, but aims to keep the data in tact.

Authors: https://github.com/tferns

"""
import sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "5fe9a48b7739"
down_revision = "eada7e01b1c2"
branch_labels = None
depends_on = None


def upgrade():

    # --- form_name table ---
    with op.batch_alter_table("form_name", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("form_name_json", sa.JSON(none_as_null=True), nullable=True)
        )

    query = sqlalchemy.text("SELECT section_id, form_name FROM form_name")
    form_name_entries = op.get_bind().execute(query)
    for section_id, form_name in form_name_entries:
        op.execute(
            f'UPDATE form_name SET form_name_json = \'{{"en": "{form_name}"}}\' '
            f"WHERE section_id = '{section_id}'"
        )

    with op.batch_alter_table("form_name", schema=None) as batch_op:
        batch_op.alter_column("form_name_json", nullable=False)
        batch_op.drop_column("form_name")

    # --- section table ---
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title_json", sa.JSON(none_as_null=True), nullable=True)
        )

    query = sqlalchemy.text("SELECT id, title FROM section")
    section_entries = op.get_bind().execute(query)
    for entry_id, title in section_entries:
        op.execute(
            f'UPDATE section SET title_json = \'{{"en": "{title}"}}\' '
            f"WHERE id = '{entry_id}'"
        )

    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.alter_column("title_json", nullable=False)
        batch_op.drop_column("title_content_id")
        batch_op.drop_column("title")


def downgrade():
    # --- section table ---
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "title_content_id", sa.INTEGER(), autoincrement=False, nullable=True
            )
        )

    query = sqlalchemy.text("SELECT id, title_json FROM section")
    section_entries = op.get_bind().execute(query)
    for entry_id, title_json in section_entries:
        title = title_json["en"]
        op.execute(f"UPDATE section SET title = '{title}' WHERE id = '{entry_id}'")

    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.alter_column("title", nullable=False)
        batch_op.drop_column("title_json")

    # --- form_name table ---
    with op.batch_alter_table("form_name", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("form_name", sa.VARCHAR(), autoincrement=False, nullable=True)
        )

    query = sqlalchemy.text("SELECT section_id, form_name_json FROM form_name")
    form_name_entries = op.get_bind().execute(query)
    for section_id, form_name_json in form_name_entries:
        form_name = form_name_json["en"]
        op.execute(
            f"UPDATE form_name SET form_name = '{form_name}' "
            f"WHERE section_id = '{section_id}'"
        )

    with op.batch_alter_table("form_name", schema=None) as batch_op:
        batch_op.alter_column("form_name", nullable=False)
        batch_op.drop_column("form_name_json")
