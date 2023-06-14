#!/usr/bin/env python3
# flake8: noqa
import argparse

import requests
from app import app  # noqa: E402
from config import Config  # noqa: E402
from config.mappings.assessment_mapping_fund_round import (
    fund_round_mapping_config,
)
from db.queries import bulk_insert_application_record  # noqa: E402
from fsd_utils import CommonConfig  # noqa: E402


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import applications from application store."
    )
    parser.add_argument(
        "--roundid",
        type=str,
        help="Provide round id of a fund or fund-round short name (eg., COFR2, COFR3W1, NSTFR2...)",
        required=True,
    )
    parser.add_argument(
        "--app_type",
        type=str,
        help="Provide app type (eg., COF, NSTF...)",
        required=False,
    )
    parser.add_argument(
        "--use_short_name",
        type=bool,
        help="Set this to true if using shortname in roundid",
        required=False,
        default=False,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.roundid and args.use_short_name:
        roundid = fund_round_mapping_config[args.roundid]["round_id"]
        app_type = fund_round_mapping_config[args.roundid][
            "type_of_application"
        ]
    elif args.roundid and args.app_type:
        roundid = args.roundid
        app_type = args.app_type
    else:
        raise Exception("Please provide all the required arguments.")

    with app.app_context():

        applications_url = (
            CommonConfig.APPLICATION_STORE_API_HOST
            + Config.APPLICATIONS_ENDPOINT
            + "?status_only=SUBMITTED"
            + f"&round_id={roundid}"
            + "&forms=true"
        )
        print(
            f"Preparing query to GET applications, using URL: '{applications_url}'"
        )
        app_store_response_json = requests.get(applications_url).json()
        bulk_insert_application_record(
            app_store_response_json,
            application_type=app_type,
            is_json=True,
        )


if __name__ == "__main__":
    main()
