import json

from _helpers import delete_messages
from _helpers import receive_messages
from app import app
from db.queries import bulk_insert_application_record


def import_applications_from_queue():
    batch_size = 1
    wait_time = 2
    application_messages = receive_messages(batch_size, wait_time)

    application_json_list = []
    # application_id_list = []

    if application_messages:
        with app.app_context():
            for message in application_messages:
                application_json = message["Body"]
                # application_attributes = message["MessageAttributes"]["application_attributes"]
                # application_id_list.append(application_attributes["application_id"])
                if isinstance(application_json, str):
                    application_json = json.loads(application_json)
                application_json_list.append(application_json)
            inserted_applications = bulk_insert_application_record(
                application_json_list,
                is_json=True,
            )
            insert_application_ids = [
                application["application_id"]
                for application in inserted_applications
            ]
            reciept_handles_to_delete = []
            for message in application_messages:
                if message["Body"]["id"] in insert_application_ids:
                    reciept_handles_to_delete.append(message["ReceiptHandle"])
            delete_messages(reciept_handles_to_delete)
    return inserted_applications
