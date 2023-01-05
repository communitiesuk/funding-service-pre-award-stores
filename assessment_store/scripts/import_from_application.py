#!/usr/bin/env python3
import argparse

import requests
from app import app
from config import Config
from db.queries import bulk_insert_application_record
from fsd_utils import CommonConfig

parser = argparse.ArgumentParser(
    description="Import applcations from application store."
)
parser.add_argument("--roundid", type=str)

args = parser.parse_args()

with app.app_context():

    applications_url = (
        CommonConfig.APPLICATION_STORE_API_HOST + Config.APPLICATIONS_ENDPOINT
        + "?status_only=SUBMITTED"
        + f"&round_id={args.roundid}"
    )

    app_store_response_json = requests.get(applications_url).json()

    for application in app_store_response_json:

        form_jsons_list = application["forms"]

        bulk_insert_application_record(form_jsons_list)
