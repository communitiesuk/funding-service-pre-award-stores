#!/usr/bin/env python3
from app import app
import requests
from config import Config
import argparse
from db.queries import bulk_insert_application_record

parser = argparse.ArgumentParser(description='Import applcations from application store.')
parser.add_argument("--roundid", type=str)

args = parser.parse_args()

with app.app_context():

    applications_url = Config.APPLICATIONS_ENDPOINT + "?status_only=SUBMITTED" + f"?round_id={args.roundid}"

    form_jsons_list = requests.get(applications_url).json["forms"]

    bulk_insert_application_record(form_jsons_list)
