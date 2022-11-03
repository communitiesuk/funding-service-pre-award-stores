import random
from db.models.assessment_records import find_field_by_key
from tests.db_seed_data import random_apps, random_keys, random_questions

def test_select_field_by_id():

    random_index = random.choice(range(len(random_apps)))

    picked_app_id = random_apps[random_index]

    picked_field_key = random.choice(random_keys[random_index])

    for question_dict in random_questions[random_index]:
        for field_dict in question_dict["fields"]:
            if field_dict["key"] == picked_field_key:
                correct_answer = field_dict
                break

    assert find_field_by_key(picked_field_key, picked_app_id)[0] == correct_answer