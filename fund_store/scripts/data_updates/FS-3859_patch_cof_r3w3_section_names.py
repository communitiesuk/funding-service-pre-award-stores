# flake8: noqa
from config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_3_ID
from config.fund_loader_config.cof.cof_r3 import cof_r3w3_sections
from db.queries import update_application_section_names


def main() -> None:
    print("Updating section names to sentance case.")
    update_application_section_names(COF_ROUND_3_WINDOW_3_ID, cof_r3w3_sections, "cy")


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
