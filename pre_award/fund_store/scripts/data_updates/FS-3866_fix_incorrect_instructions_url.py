from flask import current_app
from sqlalchemy import update

import pre_award.fund_store.config.fund_loader_config.cof.cof_r3 as cof_r3
from pre_award.db import db
from services.data.models.round import Round


def update_rounds_with_links(rounds):
    for round in rounds:
        current_app.logger.warning(
            "\tRound: {round_short_name} ({round_id})",
            extra=dict(round_short_name=round["short_name"], round_id=round["id"]),
        )
        if round.get("instructions"):
            current_app.logger.warning("\t\tUpdating instructions")
            stmt = (
                update(Round)
                .where(Round.id == round["id"])
                .values(
                    instructions=round["instructions"],
                )
            )

            db.session.execute(stmt)
        else:
            current_app.logger.warning("\t\tNo instructions defined")
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating instructions for COF R3W3")
    update_rounds_with_links(cof_r3.round_config_w3)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
