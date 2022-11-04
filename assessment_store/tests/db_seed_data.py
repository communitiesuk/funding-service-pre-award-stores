import random
import string

from db.models.assessment_records import AssessmentRecords


def create_question_row_data():

    random_keys = [''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for i in range(6)]

    question_row = [
                {
                    "question": "About your organisation",
                    "fields": [
                        {
                            "key": random_keys[0],
                            "title": "Applicant name",
                            "type": "text",
                            "answer": "Coolio",
                        },
                        {
                            "key": random_keys[1],
                            "title": "Email",
                            "type": "text",
                            "answer": "a@example.com",
                        },
                        {
                            "key": random_keys[2],
                            "title": "Telephone number",
                            "type": "text",
                            "answer": "Wow",
                        },
                        {
                            "key": random_keys[3],
                            "title": "Website",
                            "type": "text",
                            "answer": "www.example.com",
                        },
                    ],
                },
                {
                    "question": "About your organisation",
                    "fields": [
                        {
                            "key": random_keys[4],
                            "title": "Applicant name",
                            "type": "text",
                            "answer": "cool",
                        },
                    ],
                },
                {
                    "question": "About your organisation",
                    "fields": [
                        {
                            "key": random_keys[5],
                            "title": "Applicant job",
                            "type": "text",
                            "answer": "cool",
                        },
                    ],
                },
            ]

    return (random_keys, question_row)

def create_rows(rows_to_make, avg_rows_per_app):

    keys_and_row = [(create_question_row_data()) for i in range(rows_to_make)]

    random_keys = [i for i,_ in keys_and_row]
    random_questions = [j for _,j in keys_and_row]

    apps = [f"app{i}" for i in range(round(rows_to_make/10))]

    random_apps = [random.choice(apps) for _ in random_questions]

    zipped_seed_data = zip(random_apps, random_keys, random_questions)

    AssessmentRows = [
        AssessmentRecords(application_id=app_id, application_json=app_json)
        for app_id, _, app_json in zipped_seed_data
    ]

    return AssessmentRows
