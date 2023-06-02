"""empty message

Revision ID: b5f7bf2831de
Revises: 5fe9a48b7739
Create Date: 2023-05-31 18:56:06.440068

FS-2701: Adds relevant welsh translations to the fund-store for form_name table.

Authors: https://github.com/tferns

"""
import json

import sqlalchemy
from alembic import op

# revision identifiers, used by Alembic.
revision = "b5f7bf2831de"
down_revision = "5fe9a48b7739"
branch_labels = None
depends_on = None

english_form_name_to_welsh_form_name = {
    "applicant-information": "gwybodaeth-am-yr-ymgeisydd",
    "asset-information": "gwybodaeth-am-yr-ased",
    "community-benefits": "buddion-cymunedol",
    "community-engagement": "ymgysylltu-a'r-gymuned",
    "community-representation": "cynrychiolaeth-gymunedol",
    "community-use": "defnydd-cymunedol",
    "declarations": "datganiadau",
    "environmental-sustainability": "cynaliadwyedd-amgylcheddol",
    "feasibility": "dichonoldeb",
    "funding-required": "cyllid-sydd-ei-angen",
    "inclusiveness-and-integration": "cynhwysiant-ac-integreiddio",
    "local-support": "cefnogaeth-leol",
    "organisation-information": "gwybodaeth-am-y-sefydliad",
    "project-costs": "costau'r-prosiect",
    "project-information": "gwybodaeth-am-y-prosiect",
    "project-qualification": "cymhwystra'r-prosiect",
    "risk": "risg",
    "skills-and-resources": "sgiliau-ac-adnoddau",
    "upload-business-plan": "lanlwythwch-y-cynllun-busnes",
    "value-to-the-community": "gwerth-i'r-gymuned",
    "applicant-information-cof-r3-w1": "gwybodaeth-am-yr-ymgeisydd-cof-r3-w1",
    "asset-information-cof-r3-w1": "gwybodaeth-am-yr-ased-cof-r3-w1",
    "community-benefits-cof-r3-w1": "buddion-cymunedol-cof-r3-w1",
    "community-engagement-cof-r3-w1": "ymgysylltiad-cymunedol-cof-r3-w1",
    "community-representation-cof-r3-w1": "cynrychiolaeth-gymunedol-cof-r3-w1",
    "community-use-cof-r3-w1": "defnydd-cymunedol-cof-r3-w1",
    "declarations-cof-r3-w1": "cadarnhadau-terfynol-cof-r3-w1",
    "environmental-sustainability-cof-r3-w1": "cynaliadwyedd-amgylcheddol-cof-r3-w1",
    "feasibility-cof-r3-w1": "dichonoldeb-cof-r3-w1",
    "funding-required-cof-r3-w1": "cyllid-sydd-ei-angen-cof-r3-w1",
    "inclusiveness-and-integration-cof-r3-w1": "cynhwysiant-ac-integreiddio-cof-r3-w1",
    "local-support-cof-r3-w1": "cefnogaeth-leol-cof-r3-w1",
    "operational-costs-cof-r3-w1": "costau-gweithredol-cof-r3-w1",
    "organisation-information-cof-r3-w1": "gwybodaeth-am-y-sefydliad-cof-r3-w1",
    "project-information-cof-r3-w1": "gwybodaeth-am-y-prosiect-cof-r3-w1",
    "project-qualifications-cof-r3-w1": "cymhwysedd-y-prosiect-cof-r3-w1",
    "risk-cof-r3-w1": "risg-cof-r3-w1",
    "skills-and-resources-cof-r3-w1": "sgiliau-ac-adnoddau-cof-r3-w1",
    "upload-business-plan-cof-r3-w1": "lanlwythwch-y-cynllun-busnes-cof-r3-w1",
}


def upgrade():
    connection = op.get_bind()
    query = sqlalchemy.text("SELECT form_name_json FROM form_name")
    form_name_entries = connection.execute(query)

    for form_name_json, *_ in form_name_entries:
        original_english_form_name = form_name_json["en"]
        english_form_name = original_english_form_name

        is_night_shelter = english_form_name.endswith("-ns")
        if is_night_shelter:
            continue

        welsh_form_name = english_form_name_to_welsh_form_name.get(english_form_name)
        if not welsh_form_name:
            raise Exception(
                f"Could not find welsh form name for {form_name_json['en']}"
            )

        welsh_form_name = welsh_form_name.replace("'", "''")

        form_name_json["cy"] = welsh_form_name

        new_form_name_json_str = json.dumps(form_name_json)
        update_query = sqlalchemy.text(
            f"UPDATE form_name SET form_name_json = '{new_form_name_json_str}' "
            f"WHERE form_name_json->>'en' = '{original_english_form_name}'"
        )
        connection.execute(update_query)


def downgrade():
    connection = op.get_bind()
    query = sqlalchemy.text(
        "SELECT form_name_json FROM form_name WHERE form_name_json->>'cy' IS NOT NULL"
    )
    form_name_entries = connection.execute(query)

    for form_name_json, *_ in form_name_entries:
        original_welsh_form_name = form_name_json["cy"].replace("'", "''")

        del form_name_json["cy"]
        new_form_name_json_str = json.dumps(form_name_json)

        update_query = sqlalchemy.text(
            f"UPDATE form_name SET form_name_json = '{new_form_name_json_str}' "
            f"WHERE form_name_json->>'cy' = '{original_welsh_form_name}'"
        )
        connection.execute(update_query)
