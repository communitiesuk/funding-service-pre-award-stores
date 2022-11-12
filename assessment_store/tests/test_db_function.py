import json
import random
from db.models.assessment_record.assessment_records import AssessmentRecords

from db.models.assessment_record.helpers import find_answer_by_key_cof
from tests.helpers import get_random_row


def test_select_field_by_id():

    picked_row = get_random_row(AssessmentRecords)

    # We pick a random row to extract some data from.
    picked_app_id = picked_row.application_id

    picked_questions = random.choice(picked_row.jsonb_blob["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_cof(picked_key, picked_app_id)[0]

    assert field_found == picked_field
