"""Queries which are performed on the `flags` table.

Joins allowed.
"""
from typing import Dict

from db import db
from db.models.qa_complete.qa_complete import QaComplete
from db.schemas.schemas import QaCompleteMetadata


def create_qa_complete_record(
    application_id: str,
    user_id: str,
) -> Dict:
    qa_complete_record = QaComplete(
        application_id=application_id,
        user_id=user_id,
    )
    db.session.add(qa_complete_record)
    db.session.commit()

    metadata_serialiser = QaCompleteMetadata()
    flag_metadata = metadata_serialiser.dump(qa_complete_record)

    return flag_metadata


def get_all_qa_complete_records() -> Dict:
    all_qa_complete_records = (
        QaComplete.query.order_by(QaComplete.date_created.desc())
        .all()
    )
    metadata_serialiser = QaCompleteMetadata()
    qa_complete_metadata_list = [metadata_serialiser.dump(qa_complete_record) for qa_complete_record in all_qa_complete_records]
    return qa_complete_metadata_list
