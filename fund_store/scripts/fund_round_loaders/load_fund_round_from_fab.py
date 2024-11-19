# flake8: noqa
import click

from config.fund_loader_config.FAB import FAB_FUND_ROUND_CONFIGS
from db import db
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import upsert_round_data


@click.command()
@click.option("--fund_short_code", default="COF25-EOI", help="Fund short code", prompt=True)
def load_fund_from_fab(fund_short_code) -> None:
    """
    Insert the FAB fund and round data into the database.
    See required schema for import here: file_location
    """

    FUND_CONFIG = FAB_FUND_ROUND_CONFIGS.get(fund_short_code, None)
    if not FUND_CONFIG:
        raise ValueError(f"Config for fund {fund_short_code} does not exist")

    if FUND_CONFIG:
        print(f"Preparing fund data for the {fund_short_code} fund.")
        insert_fund_data(FUND_CONFIG, commit=False)

        for round_short_name, round in FUND_CONFIG["rounds"].items():

            round_base_path = round["base_path"]

            APPLICATION_BASE_PATH = ".".join([str(round_base_path), str(1)])
            ASSESSMENT_BASE_PATH = ".".join([str(round_base_path), str(2)])

            print(f"Preparing round data for the '{round_short_name}' round.")
            upsert_round_data([round], commit=False)

            # Section config is per round, not per fund
            print(f"Preparing base sections for {round_short_name}.")
            insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, round["id"])

            print(f"Preparing application sections for {round_short_name}.")
            insert_or_update_application_sections(round["id"], round["sections_config"])

    print(f"All config has been successfully prepared, now committing to the database.")
    db.session.commit()
    print(f"Config has now been committed to the database.")


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        load_fund_from_fab()
