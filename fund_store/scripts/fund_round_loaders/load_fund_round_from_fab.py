# flake8: noqa
import os
import click

from fund_store.config.fund_loader_config.FAB import FAB_FUND_ROUND_CONFIGS
from db import db
from fund_store.db.queries import insert_base_sections
from fund_store.db.queries import insert_fund_data
from fund_store.db.queries import insert_or_update_application_sections
from fund_store.db.queries import upsert_round_data


@click.command()
@click.option("--fund_short_code", default="", help="Fund short code")
def load_fund_from_fab(fund_short_code) -> None:
    """
    Insert the FAB fund and round data into the database.
    See required schema for import here: file_location

    Accept comma separated funds too.
    """

    if fund_short_code == "":
        confirm = click.confirm("Are you sure you want to seed all FAB funds?", default=True)

        if not confirm:
            fund_short_code = click.prompt("Please enter a fund short code", default="CTDF")
        else:
            # Get a list of all Python files in the fund_round_loaders directory
            loader_module_names = [
                fund_config_file
                for fund_config_file in os.listdir("fund_store/config/fund_loader_config/FAB")
                if fund_config_file.endswith(".py")
            ]

            for module_name in loader_module_names:
                # Remove the ".py" extension to get the module name
                file_name = module_name[:-3]

                skip_files = ["__init__", "cof_25", "cof_25_eoi"]
                if file_name in skip_files:
                    continue

                if fund_short_code != "":
                    fund_short_code += ","

                # file names should inlcude the round short name "_" separated
                fund_short_code += module_name[:-3].upper().split("_")[0]

    funds_to_seed = fund_short_code
    print(f"Funds to seed: {funds_to_seed}")

    for fund_to_seed in funds_to_seed.split(","):
        FUND_CONFIG = FAB_FUND_ROUND_CONFIGS.get(fund_to_seed, None)
        if not FUND_CONFIG:
            raise ValueError(f"Config for fund {fund_to_seed} does not exist")

        if FUND_CONFIG:
            print(f"Preparing fund data for the {fund_to_seed} fund.")
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
