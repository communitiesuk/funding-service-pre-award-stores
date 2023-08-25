import json

import app
from config import Config
from db.queries import bulk_insert_application_record
from flask import current_app
from services import _SQS_QUEUE_URL
from services import delete_messages
from services import receive_messages


def import_applications_from_queue():
    batch_size = Config.SQS_BATCH_SIZE
    visibility_time = Config.SQS_VISIBILITY_TIME
    wait_time = Config.SQS_WAIT_TIME
    application_messages = receive_messages(
        _SQS_QUEUE_URL, batch_size, visibility_time, wait_time
    )

    application_json_list = []

    if application_messages:
        with app.app.app_context():
            for message in application_messages:
                application_json = message["Body"]
                if isinstance(application_json, str):
                    application_json = json.loads(application_json)
                application_json_list.append(application_json)

            # bulk insert the applications
            inserted_applications = bulk_insert_application_record(
                application_json_list,
                is_json=True,
            )
            insert_application_ids = [
                application["application_id"]
                for application in inserted_applications
            ]

            # delete the messages from queue
            reciept_handles_to_delete = []
            for message in application_messages:
                if (
                    message["MessageAttributes"]["application_id"][
                        "StringValue"
                    ]
                    in insert_application_ids
                ):
                    reciept_handles_to_delete.append(message["ReceiptHandle"])
            if reciept_handles_to_delete:
                delete_messages(_SQS_QUEUE_URL, reciept_handles_to_delete)

            for message in application_messages:
                receive_count = int(
                    message["Attributes"]["ApproximateReceiveCount"]
                )
                if receive_count == Config.AWS_DLQ_MAX_RECIEVE_COUNT:
                    current_app.logger.error(
                        f"Failed to import application with id: "
                        f"{message['MessageAttributes']['application_id']['StringValue']}. "
                        "Moving message to DLQ"
                    )

            # return inserted applications
            return inserted_applications
