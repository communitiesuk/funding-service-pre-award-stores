#!/usr/bin/env python3
import argparse
import os
import sys

sys.path.insert(1, ".")


# from app import app  # noqa: E402
from db.queries.assessment_records.queries import (  # noqa: E402
    get_application_jsonb_blob,  # noqa: E402
)  # noqa: E402
from distutils.util import strtobool  # noqa: E402
from scripts.location_utils import (  # noqa: E402
    get_all_application_ids_for_fund_round,  # noqa: E402
)  # noqa: E402
from scripts.location_utils import get_all_location_data  # noqa: E402
from scripts.location_utils import get_application_form  # noqa: E402
from scripts.location_utils import get_postcode_from_questions  # noqa: E402
from scripts.location_utils import update_db_with_location_data  # noqa: E402
from scripts.location_utils import write_locations_to_csv  # noqa: E402


local_workspace = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
file_locations_csv = local_workspace + "/locations.csv"


def process_locations(
    fund_id, round_id, update_db: bool, write_csv: bool, csv_location
):
    """
    Runs within the app context to have access to DB etc. Uses the functions
    in `location_utils.py` to extract postcodes, retrieve location details,
    then update the DB with this information
    """
    with app.app_context():
        application_ids = get_all_application_ids_for_fund_round(
            fund_id, round_id
        )
        just_postcodes = []
        application_ids_to_postcodes = {}

        # extract the postcode from each application we have
        print(
            f"Extracting postcodes from {len(application_ids)}"
            f" applications for fund_id: {fund_id}, round_id: {round_id}"
        )
        for id in application_ids:
            app_json = get_application_jsonb_blob(id[0])
            questions = get_application_form(app_json)
            postcode = get_postcode_from_questions(questions)
            application_ids_to_postcodes[id] = postcode
            just_postcodes.append(postcode)
        postcodes_to_location_data = get_all_location_data(just_postcodes)

        if update_db:
            update_db_with_location_data(
                application_ids_to_postcodes, postcodes_to_location_data
            )
        if write_csv:
            print("Writing to csv")
            write_locations_to_csv(
                application_ids_to_postcodes,
                postcodes_to_location_data,
                csv_location,
            )


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fund_id", help="Provide fund id of a fund", required=True
    )
    parser.add_argument(
        "--round_id", help="Provide round id of a fund", required=True
    )
    parser.add_argument(
        "--update_db",
        help="Whether to update the DB with new location data",
        required=True,
    )
    parser.add_argument(
        "--write_csv",
        help="Whether to write location data to a CSV - "
        + "if yes, include param --csv_location",
        required=True,
    )
    parser.add_argument(
        "--csv_location",
        help="Absolute path to write CSV file to",
        required=False,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    process_locations(
        fund_id=args.fund_id,
        round_id=args.round_id,
        csv_location=args.csv_location,
        write_csv=strtobool(args.write_csv),
        update_db=strtobool(args.update_db),
    )


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
