"""empty message

Revision ID: c2a339e2a973
Revises: b5f7bf2831de
Create Date: 2023-05-31 23:25:34.998461

FS-2701: Adds relevant welsh translations to the fund-store for section table.

Authors: https://github.com/tferns


"""

import json

import sqlalchemy
from alembic import op

# revision identifiers, used by Alembic.
revision = "c2a339e2a973"
down_revision = "b5f7bf2831de"
branch_labels = None
depends_on = None

english_title_to_welsh_title = {
    key.casefold(): value
    for key, value in {
        "1. About your organisation": "1. Ynglŷn â'ch sefydliad",
        "1.1 Organisation Information": "1.1 Gwybodaeth am y sefydliad",
        "1.2 Applicant Information": "1.2 Gwybodaeth am yr ymgeisydd",
        "2. About your project": "2. Ynglŷn â'ch prosiect",
        "2.1 Project Information": "2.1 Gwybodaeth am y prosiect",
        "2.2 Asset Information": "2.2 Gwybodaeth am yr ased",
        "3. Strategic case": "3. Achos strategol",
        "3.1 Community use": "3.1 Defnydd cymunedol",
        "3.2 Community engagement": "3.2 Ymgysylltu â'r gymuned",
        "3.3 Local support": "3.3 Cefnogaeth leol",
        "3.4 Community benefits": "3.4 Buddion i'r gymuned",
        "3.5 Environmental sustainability": "3.5 Cynaliadwyedd amgylcheddol",
        "4. Management case": "4. Achos rheoli",
        "4.1 Funding required": "4.1 Cyllid sydd ei angen",
        "4.2 Feasibility": "4.2 Dichonoldeb",
        "4.3 Risk": "4.3 Risg",
        "4.4 Operational costs": "4.4 Costau gweithredol",
        "4.4 Project Costs": "4.4 Costau'r prosiect",
        "4.5 Skills And Resources": "4.5 Sgiliau ac Adnoddau",
        "4.6 Community Representation": "4.6 Cynrychiolaeth gymunedol",
        "4.7 Inclusiveness And Integration": "4.7 Cynhwysiant ac Integreiddio",
        "4.8 Upload business plan": "4.8 Lanlwythwch y cynllun busnes",
        "5. Potential to deliver community benefits": "5. Potensial i gyflawni buddion cymunedol",
        "5. Subsidy control and state aid": "5. Rheoli cymorthdaliadau a chymorth gwladwriaethol",
        "5.1 Project qualification": "5.1 Cymhwystra'r prosiect",
        "6. Added value to community": "6. Gwerth ychwanegol i'r gymuned",
        "6. Check declarations": "6. Gwirio datganiadau",
        "6.1 Declarations": "6.1 Datganiadau",
        "7. Subsidy control / state aid": "7. Rheoli cymorthdaliadau a chymorth gwladwriaethol",
        "8. Check declarations": "8. Gwirio datganiadau",
        "About your organisation": "Ynglŷn â'ch sefydliad",
        "About your project": "Ynglŷn â'ch prosiect",
        "Added value to community": "Gwerth ychwanegol i'r gymuned",
        "Applicant Information": "Gwybodaeth am yr ymgeisydd",
        "Application": "Cais",
        "Assessment": "Asesu",
        "Asset Information": "Gwybodaeth am yr ased",
        "Before you start": "Cyn i chi ddechrau",
        "Check declarations": "Gwirio datganiadau",
        "Community Benefits": "Buddion cymunedol",
        "Community Engagement": "Ymgysylltu â'r gymuned",
        "Community Representation": "Cynrychiolaeth gymunedol",
        "Community Use": "Defnydd Cymunedol",
        "Community use": "Defnydd cymunedol",
        "Declarations": "Datganiadau",
        "Environmental Sustainability": "Cynaliadwyedd amgylcheddol",
        "Feasibility": "Dichonoldeb",
        "Funding Required": "Cyllid sydd ei angen",
        "Inclusiveness And Integration": "Cynhwysiant ac Integreiddio",
        "Local Support": "Cefnogaeth leol",
        "Management Case": "Achos rheoli",
        "Name you application": "Enwch eich cais",
        "Operational costs": "Costau gweithredol",
        "Organisation Information": "Gwybodaeth am y sefydliad",
        "Organisation information": "Gwybodaeth am y sefydliad",
        "Potential to deliver community benefits": "Potensial i gyflawni buddion cymunedol",
        "Project Costs": "Costau'r prosiect",
        "Project Information": "Gwybodaeth am y prosiect",
        "Project Qualification": "Cymhwystra'r prosiect",
        "Risk": "Risg",
        "Skills And Resources": "Sgiliau ac Adnoddau",
        "Strategic case": "Achos strategol",
        "Subsidy control / state aid": "Rheoli cymorthdaliadau a chymorth gwladwriaethol",
        "Upload Business Plan": "Lanlwythwch y cynllun busnes",
        "Value To The Community": "Gwerth i'r Gymuned",
    }.items()
}


def upgrade():
    connection = op.get_bind()
    query = sqlalchemy.text(
        "SELECT title_json FROM section WHERE round_id IN"
        " ('c603d114-5364-4474-a0c4-c41cbf4d3bbd',"
        " 'e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762')"
    )
    section_entries = connection.execute(query)

    for title_json, *_ in section_entries:
        original_english_title = title_json["en"]
        welsh_title = english_title_to_welsh_title.get(original_english_title.casefold())
        if not welsh_title:
            raise Exception(f"Could not find welsh title for {original_english_title}")

        welsh_title = welsh_title.replace("'", "''")
        title_json["cy"] = welsh_title
        new_title_json = json.dumps(title_json)

        update_query = sqlalchemy.text(
            f"UPDATE section SET title_json = '{new_title_json}' WHERE"
            f" title_json->>'en' = '{original_english_title}' AND round_id IN"
            " ('c603d114-5364-4474-a0c4-c41cbf4d3bbd',"
            " 'e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762')"
        )
        connection.execute(update_query)


def downgrade():
    connection = op.get_bind()
    query = sqlalchemy.text("SELECT title_json FROM section WHERE title_json->>'cy' IS NOT NULL")
    section_entries = connection.execute(query)

    for title_json, *_ in section_entries:
        original_welsh = title_json["cy"].replace("'", "''")

        del title_json["cy"]
        new_form_name_json_str = json.dumps(title_json)

        update_query = sqlalchemy.text(
            f"UPDATE section SET title_json = '{new_form_name_json_str}' WHERE"
            f" title_json->>'cy' = '{original_welsh}' AND round_id IN"
            " ('c603d114-5364-4474-a0c4-c41cbf4d3bbd',"
            " 'e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762')"
        )
        connection.execute(update_query)
