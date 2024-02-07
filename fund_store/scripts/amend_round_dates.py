#!/usr/bin/env python3
import argparse
from datetime import datetime

from db import db
from db.models import Round


def update_round_dates(round_id, new_open_date, new_deadline, new_assessment_deadline):
    round_to_update = Round.query.get(round_id)
    if new_open_date:
        round_to_update.opens = datetime.strptime(new_open_date, "%Y-%m-%d %H:%M:%S")

    if new_deadline:
        round_to_update.deadline = datetime.strptime(new_deadline, "%Y-%m-%d %H:%M:%S")

    if new_assessment_deadline:
        round_to_update.assessment_deadline = datetime.strptime(new_assessment_deadline, "%Y-%m-%d %H:%M:%S")

    if new_open_date or new_deadline or new_assessment_deadline:
        db.session.commit()
        print(f"Sucessfully updated the round dates for {round_id}.")


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round_id", help="Provide round id of a fund", required=True)
    parser.add_argument("--opens_date", help="Provide Round open date", required=False)
    parser.add_argument("--deadline_date", help="Provide Round deadline date", required=False)
    parser.add_argument(
        "--assessment_deadline_date",
        help="Provide Assessment deadline for the round",
        required=False,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    round_id = args.round_id

    update_round_dates(round_id, args.opens_date, args.deadline_date, args.assessment_deadline_date)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
