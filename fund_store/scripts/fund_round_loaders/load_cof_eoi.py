# flake8: noqa
from config.fund_loader_config.cof.cof_r3 import APPLICATION_BASE_PATH_COF_EOI
from config.fund_loader_config.cof.cof_r3 import ASSESSMENT_BASE_PATH_COF_EOI
from config.fund_loader_config.cof.cof_r3 import COF_EOI_ROUND_id
from config.fund_loader_config.cof.cof_r3 import cof_eoi_sections
from config.fund_loader_config.cof.cof_r3 import round_config_eoi
from db.queries import insert_base_sections
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data


def main() -> None:
    print(
        "'insert_fund_config(...)' not required as COF_EOI shares the same fund"
        " config from COFR3w1."
    )
    print("Inserting round data.")
    insert_round_data(round_config_eoi)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_EOI,
        ASSESSMENT_BASE_PATH_COF_EOI,
        COF_EOI_ROUND_id,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_EOI_ROUND_id, cof_eoi_sections)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
