# flake8: noqa
from config.fund_loader_config.hsra.hsra import APPLICATION_BASE_PATH_HSRA
from config.fund_loader_config.hsra.hsra import ASSESSMENT_BASE_PATH_HSRA
from config.fund_loader_config.hsra.hsra import HSRA_ROUND_ID
from config.fund_loader_config.hsra.hsra import fund_config
from config.fund_loader_config.hsra.hsra import hsra_sections
from config.fund_loader_config.hsra.hsra import round_config
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data


def main() -> None:
    print("Inserting fund and round data for HSRA.")
    insert_fund_data(fund_config)
    insert_round_data(round_config)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_HSRA,
        ASSESSMENT_BASE_PATH_HSRA,
        HSRA_ROUND_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(HSRA_ROUND_ID, hsra_sections)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
