import random
from db.models.assessment_records import find_field_by_key

def test_select_field_by_id(row_data):

    assessment_rows = row_data

    picked_row = random.choice(assessment_rows)

    # We pick a random row to extract some data from.
    picked_app_id = picked_row.application_id

    picked_questions = picked_row.application_json
    picked_question = random.choice(picked_questions)
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_field_by_key(picked_key, picked_app_id)[0]

    assert field_found == picked_field