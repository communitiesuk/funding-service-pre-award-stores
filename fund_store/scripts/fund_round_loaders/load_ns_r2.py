# flake8: noqa
from config.fund_loader_config.night_shelter.ns_r2 import APPLICATION_BASE_PATH
from config.fund_loader_config.night_shelter.ns_r2 import ASSESSMENT_BASE_PATH
from config.fund_loader_config.night_shelter.ns_r2 import NIGHT_SHELTER_ROUND_2_ID
from config.fund_loader_config.night_shelter.ns_r2 import fund_config
from config.fund_loader_config.night_shelter.ns_r2 import r2_application_sections
from config.fund_loader_config.night_shelter.ns_r2 import round_config
from db.queries import insert_assessment_sections
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import upsert_round_data


def main() -> None:
    print("Inserting fund data for the Night Shelter fund.")
    insert_fund_data(fund_config)
    print("Inserting round data for round 2 of the Night Shelter fund.")
    upsert_round_data(round_config)

    print("Inserting base sections for Night Shelter Round 2.")
    insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, NIGHT_SHELTER_ROUND_2_ID)
    print("Inserting application sections for Night Shelter Round 2.")
    insert_or_update_application_sections(NIGHT_SHELTER_ROUND_2_ID, r2_application_sections)


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
