"""

Revision ID: eada7e01b1c2
Revises: c8404dc10813
Create Date: 2023-05-31 15:18:39.533053

FS-2701: Purpose of this script is converting the name, title and description columns to jsonb,
and populating them with the existing values.  The reason we're doing this is that we want to
hold translations in the database, keyed by language code, we keep the existing data as it's in
production, and we don't want to drop and re-create the entire database every time we make a change.
The downgrade does the exact opposite, but aims to keep the data in tact.

Authors: https://github.com/RamuniN, https://github.com/tferns

"""
import sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "eada7e01b1c2"
down_revision = "c8404dc10813"
branch_labels = None
depends_on = None


def upgrade():
    # --- fund table ---
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("name_json", sa.JSON(none_as_null=True), nullable=True)
        )
        batch_op.add_column(
            sa.Column("title_json", sa.JSON(none_as_null=True), nullable=True)
        )
        batch_op.add_column(
            sa.Column("description_json", sa.JSON(none_as_null=True), nullable=True)
        )

    query = sqlalchemy.text("SELECT id, name, title, description FROM fund")
    fund_entries = op.get_bind().execute(query)
    for entry_id, name, title, description in fund_entries:
        op.execute(
            f'UPDATE fund SET name_json = \'{{"en": "{name}"}}\', '
            f'title_json = \'{{"en": "{title}"}}\', '
            f'description_json = \'{{"en": "{description}"}}\' '
            f"WHERE id = '{entry_id}'"
        )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("name_json", nullable=False)
        batch_op.alter_column("title_json", nullable=False)
        batch_op.alter_column("description_json", nullable=False)
        batch_op.drop_column("description")
        batch_op.drop_column("title")
        batch_op.drop_column("name")

    # --- round table ---
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title_json", sa.JSON(none_as_null=True), nullable=True)
        )

    query = sqlalchemy.text("SELECT id, title FROM round")
    round_entries = op.get_bind().execute(query)
    for entry_id, title in round_entries:
        op.execute(
            f'UPDATE round SET title_json = \'{{"en": "{title}"}}\' '
            f"WHERE id = '{entry_id}'"
        )

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("title_json", nullable=False)
        batch_op.drop_column("title")


def downgrade():
    # --- round table ---
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True)
        )

    query = sqlalchemy.text("SELECT id, title_json FROM round")
    round_entries = op.get_bind().execute(query)
    for entry_id, title_json in round_entries:
        title = title_json["en"]
        op.execute(f"UPDATE round SET title = '{title}' WHERE id = '{entry_id}'")

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("title", nullable=False)
        batch_op.drop_column("title_json")

    # --- fund table ---
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True)
        )

    query = sqlalchemy.text(
        "SELECT id, name_json, title_json, description_json FROM fund"
    )
    fund_entries = op.get_bind().execute(query)
    for entry_id, name_json, title_json, description_json in fund_entries:
        name = name_json["en"]
        title = title_json["en"]
        description = description_json["en"]
        op.execute(
            f"UPDATE fund SET name = '{name}', "
            f"title = '{title}', "
            f"description = '{description}' "
            f"WHERE id = '{entry_id}'"
        )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("name", nullable=False)
        batch_op.alter_column("title", nullable=False)
        batch_op.alter_column("description", nullable=False)
        batch_op.drop_column("description_json")
        batch_op.drop_column("title_json")
        batch_op.drop_column("name_json")
