from flask import current_app
from sqlalchemy import update

import config.fund_loader_config.night_shelter.ns_r2 as nstf_config
from db import db
from db.models.section import Section


def update_section_titles(section_config):
    if len(section_config) > 0:
        for section in section_config:
            current_app.logger.info(
                f"\t\tUpdating section title from {section['old_title']} to {section['new_title']}."
            )
            stmt = (
                update(Section)
                .where(Section.title == section["old_title"])
                .where(Section.round_id == section["round_id"])
                .values(title=section["new_title"])
            )

            db.session.execute(stmt)
    else:
        current_app.logger.info("\t\tNo section config provided")
    db.session.commit()


def main() -> None:
    section_config = [
        {
            "old_title": "Name you application",
            "new_title": "Name your application",
            "round_id": nstf_config.NIGHT_SHELTER_ROUND_2_ID,
        },
        {
            "old_title": "7. Check declarations",
            "new_title": "7. Declarations",
            "round_id": nstf_config.NIGHT_SHELTER_ROUND_2_ID,
        },
        {
            "old_title": "1.1 Organisation Information",
            "new_title": "1.1 Organisation information",
            "round_id": nstf_config.NIGHT_SHELTER_ROUND_2_ID,
        },
    ]
    current_app.logger.info("Updating sections for NSTF")
    update_section_titles(section_config)
    current_app.logger.info("Update complete")


if __name__ == "__main__":
    from app import app

    with app.app.app_context():
        main()
