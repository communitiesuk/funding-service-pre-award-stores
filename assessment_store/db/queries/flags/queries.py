"""Queries which are performed on the `flags` table.

Joins allowed.
"""
from typing import Dict

from db import db
from db.models import Flag
from db.models.flags.enums import FlagType
from db.schemas.schemas import FlagMetadata


def create_flag_for_application(
    justification: str,
    section_to_flag: str,
    application_id: str,
    user_id: str,
    flag_type: FlagType,
) -> Dict:
    flag = Flag(
        justification=justification,
        section_to_flag=section_to_flag,
        application_id=application_id,
        user_id=user_id,
        flag_type=flag_type,
    )
    db.session.add(flag)
    db.session.commit()

    metadata_serialiser = FlagMetadata()
    flag_metadata = metadata_serialiser.dump(flag)

    return flag_metadata


def retrieve_flags_for_application(application_ids: list[str]) -> dict:
    flags = (
        Flag.query.filter(Flag.application_id.in_(application_ids))
        .order_by(Flag.date_created.desc())
        .all()
    )

    metadata_serialiser = FlagMetadata()
    flag_metadatas = [metadata_serialiser.dump(flag) for flag in flags]

    return flag_metadatas
