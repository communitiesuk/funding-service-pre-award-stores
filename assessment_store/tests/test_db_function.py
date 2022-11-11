import json
import random

from db.models.assessment_record.helpers import find_answer_by_key_cof


def test_select_field_by_id(row_data):

    picked_row = random.choice(row_data["test_rows"])

    picked_row = json.loads(picked_row)

    # We pick a random row to extract some data from.
    picked_app_id = picked_row["id"]

    picked_questions = random.choice(picked_row["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_cof(picked_key, picked_app_id)[0]

    assert field_found == picked_field
