"""empty message

Revision ID: 6928bebf9d54
Revises: c2a339e2a973
Create Date: 2023-06-01 10:44:52.762967

FS-2701: Insert welsh translations into fund/round tables.

Authors: https://github.com/tferns

"""

import json

import sqlalchemy
from alembic import op

# revision identifiers, used by Alembic.
revision = "6928bebf9d54"
down_revision = "c2a339e2a973"
branch_labels = None
depends_on = None

english_to_welsh_name = {
    key.casefold(): value
    for key, value in {
        "Community Ownership Fund": "Y Cronfa Perchnogaeth Gymunedol",
    }.items()
}

english_to_welsh_title = {
    key.casefold(): value
    for key, value in {
        "funding to save an asset in your community": "cyllid i achub ased yn eich cymuned",
    }.items()
}

english_to_welsh_description = {
    key.casefold(): value
    for key, value in {
        # TODO: Provide welsh translation
        "The Community Ownership Fund is a £150 million fund over 4 years to support community groups across England, Wales, Scotland and Northern Ireland to take ownership of assets which are at risk of being lost to the community.": (  # noqa
            "The Community Ownership Fund is a £150 million fund over 4 years to support community groups across England, Wales, Scotland and Northern Ireland to take ownership of assets which are at risk of being lost to the community."  # noqa
        )
    }.items()
}

english_to_welsh_round_title = {
    key.casefold(): value
    for key, value in {
        # TODO: Provide welsh translation
        "Round 2 Window 3": "Round 2 Window 3",
        "Round 2 Window 2": "Round 2 Window 2",
        "Round 3 Window 1": "Round 3 Window 1",
    }.items()
}


def upgrade():
    connection = op.get_bind()
    query = sqlalchemy.text("SELECT id, name_json, title_json, description_json FROM fund WHERE welsh_available = true")
    funds = connection.execute(query)

    for id, name_json, title_json, description_json in funds:
        english_name = name_json["en"]
        welsh_name = english_to_welsh_name.get(english_name.casefold())
        if not welsh_name:
            raise Exception(f"Could not find welsh name for {english_name}")
        name_json["cy"] = welsh_name
        new_name_json = json.dumps(name_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET name_json = '{new_name_json}' WHERE id = '{id}'")
        connection.execute(update_query)

        english_title = title_json["en"]
        welsh_title = english_to_welsh_title.get(english_title.casefold())
        if not welsh_title:
            raise Exception(f"Could not find welsh title for {english_title}")
        title_json["cy"] = welsh_title
        new_title_json = json.dumps(title_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET title_json = '{new_title_json}' WHERE id = '{id}'")
        connection.execute(update_query)

        english_description = description_json["en"]
        welsh_description = english_to_welsh_description.get(english_description.casefold())
        if not welsh_description:
            raise Exception(f"Could not find welsh description for {english_description}")
        description_json["cy"] = welsh_description
        new_description_json = json.dumps(description_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET description_json = '{new_description_json}' WHERE id = '{id}'")
        connection.execute(update_query)

    query = sqlalchemy.text("SELECT id, title_json FROM round WHERE fund_id = '47aef2f5-3fcb-4d45-acb5-f0152b5f03c4'")
    funds = connection.execute(query)

    for id, title_json in funds:
        english_title = title_json["en"]
        welsh_title = english_to_welsh_round_title.get(english_title.casefold())
        if not welsh_title:
            raise Exception(f"Could not find welsh title for {english_title}")
        title_json["cy"] = welsh_title
        new_title_json = json.dumps(title_json)
        update_query = sqlalchemy.text(f"UPDATE round SET title_json = '{new_title_json}' WHERE id = '{id}'")
        connection.execute(update_query)


def downgrade():
    connection = op.get_bind()

    query = sqlalchemy.text("SELECT id, title_json FROM round WHERE fund_id = '47aef2f5-3fcb-4d45-acb5-f0152b5f03c4'")
    funds = connection.execute(query)

    for id, title_json in funds:
        del title_json["cy"]
        new_title_json = json.dumps(title_json)
        update_query = sqlalchemy.text(f"UPDATE round SET title_json = '{new_title_json}' WHERE id = '{id}'")
        connection.execute(update_query)

    query = sqlalchemy.text("SELECT id, name_json, title_json, description_json FROM fund WHERE welsh_available = true")
    funds = connection.execute(query)

    for id, name_json, title_json, description_json in funds:
        del name_json["cy"]
        new_name_json = json.dumps(name_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET name_json = '{new_name_json}' WHERE id = '{id}'")
        connection.execute(update_query)

        del title_json["cy"]
        new_title_json = json.dumps(title_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET title_json = '{new_title_json}' WHERE id = '{id}'")
        connection.execute(update_query)

        del description_json["cy"]
        new_description_json = json.dumps(description_json)
        update_query = sqlalchemy.text(f"UPDATE fund SET description_json = '{new_description_json}' WHERE id = '{id}'")
        connection.execute(update_query)
