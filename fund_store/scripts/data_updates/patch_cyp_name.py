import config.fund_loader_config.cyp.cyp_r1 as cyp_r1
from db import db
from db.models.fund import Fund
from flask import current_app
from sqlalchemy import update


def update_fund_name(fund_config):
    current_app.logger.info(f"Fund: {fund_config['short_name']}")
    current_app.logger.info("\t\tUpdating fund name")
    stmt = (
        update(Fund)
        .where(Fund.id == fund_config["id"])
        .values(name_json=fund_config["name_json"])
    )

    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.info("Updating fund name for CYP")
    update_fund_name(cyp_r1.fund_config)
    current_app.logger.info("Updates complete")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
