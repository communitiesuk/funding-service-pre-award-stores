"""Purpose of this script is converting the instructions and application_guidance columns to jsonb,
and populating them with the existing values.  The reason we're doing this is that we want to
hold translations in the database, keyed by language code, we keep the existing data as it's in
production, and we don't want to drop and re-create the entire database every time we make a change.
The downgrade does the exact opposite, but aims to keep the data in tact.

Revision ID: 101ca9d39e50
Revises: ed3a28891090
Create Date: 2024-03-18 10:21:32.306916

"""

import json

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "101ca9d39e50"
down_revision = "ed3a28891090"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("instructions_json", sa.JSON(none_as_null=True), nullable=True))
        batch_op.add_column(sa.Column("application_guidance_json", sa.JSON(none_as_null=True), nullable=True))

    # Migrate existing data to newly created columns
    query = sa.text("SELECT id, instructions, application_guidance FROM round")
    round_entries = op.get_bind().execute(query)
    connection = op.get_bind()
    for entry_id, instructions, application_guidance in round_entries:
        update_query = sa.text(
            "UPDATE round SET instructions_json = :instructions_json, "
            "application_guidance_json = :application_guidance_json "
            "WHERE id = :entry_id"
        )

        params = {
            "entry_id": entry_id,
            "instructions_json": json.dumps({"en": instructions}) if instructions else None,
            "application_guidance_json": json.dumps({"en": application_guidance}) if application_guidance else None,
        }
        connection.execute(update_query, params)

    # Drop the columns
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("instructions")
        batch_op.drop_column("application_guidance")
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("instructions", sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("application_guidance", sa.VARCHAR(), autoincrement=False, nullable=True))

    # Migrate existing data to newly created columns
    query = sa.text("SELECT id, instructions_json, application_guidance_json  FROM round")
    round_entries = op.get_bind().execute(query)
    connection = op.get_bind()
    for entry_id, instructions_json, application_guidance_json in round_entries:
        instructions = instructions_json["en"] if instructions_json else ""
        application_guidance = application_guidance_json["en"] if application_guidance_json else None
        update_query = sa.text(
            "UPDATE round SET instructions = :instructions, application_guidance = :application_guidance WHERE id ="
            " :entry_id"
        )

        params = {"entry_id": entry_id, "instructions": instructions, "application_guidance": application_guidance}
        connection.execute(update_query, params)

    # Drop the columns
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("instructions", nullable=False)
        batch_op.drop_column("application_guidance_json")
        batch_op.drop_column("instructions_json")

    # ### end Alembic commands ###
