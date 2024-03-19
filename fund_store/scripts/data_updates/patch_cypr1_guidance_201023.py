from flask import current_app
from sqlalchemy import update

import config.fund_loader_config.cyp.cyp_r1 as cyp_r1
from db import db
from db.models.round import Round


def update_round_guidance(round_config):
    current_app.logger.info(f"Round: {round_config['short_name']}, id: {round_config['id']}")
    current_app.logger.info("\t\tUpdating round guidance")
    stmt = update(Round).where(Round.id == round_config["id"]).values(guidance_url=round_config["guidance_url"])

    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.info("Updating guidance url for CYP R1")
    update_round_guidance(cyp_r1.round_config[0])
    current_app.logger.info("Updates complete")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
