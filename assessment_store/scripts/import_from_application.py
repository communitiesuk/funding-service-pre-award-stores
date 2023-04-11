#!/usr/bin/env python3
import argparse

import requests
from app import app  # noqa: E402
from config import Config  # noqa: E402
from db.queries import bulk_insert_application_record  # noqa: E402
from fsd_utils import CommonConfig  # noqa: E402


parser = argparse.ArgumentParser(
    description="Import applications from application store."
)
parser.add_argument("--roundid", type=str)

args = parser.parse_args()

with app.app_context():

    applications_url = (
        CommonConfig.APPLICATION_STORE_API_HOST
        + Config.APPLICATIONS_ENDPOINT
        + "?status_only=SUBMITTED"
        + f"&round_id={args.roundid}"
        + "&forms=true"
    )
    print(
        f"Preparing query to GET applications, using URL: '{applications_url}'"
    )
    app_store_response_json = requests.get(applications_url).json()
    bulk_insert_application_record(
        app_store_response_json, application_type="COFW3", is_json=True
    )
