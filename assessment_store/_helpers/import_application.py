import requests
from _helpers import delete_message
from _helpers import receive_message
from _helpers import unpack_message
from app import app
from config import Config
from db.queries import insert_application_record
from fsd_utils import CommonConfig


def import_applications_from_queue():
    batch_size = 1
    wait_time = 2
    application_message = receive_message(batch_size, wait_time)

    if application_message:
        id, application_id, datetime_str = unpack_message(application_message)
        with app.app_context():

            applications_url = (
                CommonConfig.APPLICATION_STORE_API_HOST
                + Config.APPLICATIONS_ENDPOINT
                + f"?application_id={application_id}&status_only=SUBMITTED"
                + "&forms=true"
            )
            print(
                f"Preparing query to GET applications, using URL: '{applications_url}'"
            )
            app_store_response_json = requests.get(applications_url).json()[0]
            inserted_rows = insert_application_record(
                app_store_response_json,
                is_json=True,
            )
            print(inserted_rows)
            delete_message(application_message)
    return application_message
