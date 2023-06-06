import config.fund_loader_config.night_shelter.ns_r2 as ns_r2
from db import db
from db.models.section import Section
from flask import current_app
from sqlalchemy import update
from sqlalchemy_utils import Ltree


def update_section_weightings(section):
    current_app.logger.warning(
        f"\tSection: {section['tree_path']} ({section['section_name']['en']})"
    )
    current_app.logger.warning("\t\tUpdating weighting")
    stmt = (
        update(Section)
        .where(Section.path == Ltree(section["tree_path"]))
        .values(weighting=section["weighting"])
    )

    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating section weightings for NSTF R2")
    ns_sections = ns_r2.r2_application_sections
    sections_to_update = [
        f"{ns_r2.APPLICATION_BASE_PATH}.3",
        f"{ns_r2.APPLICATION_BASE_PATH}.4",
    ]
    for section in ns_sections:
        if section["tree_path"] in sections_to_update:
            update_section_weightings(section)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
