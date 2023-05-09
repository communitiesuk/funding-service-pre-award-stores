"""Queries which are performed on the `flags` table.

Joins allowed.
"""
from typing import Dict
from typing import Iterable

from db import db
from db.models import Flag
from db.models.flags.enums import FlagType
from db.schemas.schemas import FlagMetadata
from sqlalchemy import and_


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


def retrieve_flag_for_application(application_id: str) -> dict:
    flag = (
        Flag.query.filter(Flag.application_id == application_id)
        .order_by(Flag.date_created.desc())
        .first()
    )

    metadata_serialiser = FlagMetadata()
    flag_metadata = metadata_serialiser.dump(flag)

    return flag_metadata


def find_qa_complete_flags(application_ids: Iterable[str]) -> dict[str, bool]:
    flags = Flag.query.filter(
        Flag.application_id.in_(application_ids),
        Flag.flag_type == "QA_COMPLETED",
    ).all()

    qa_completed_application_ids = {flag.application_id for flag in flags}
    return {
        app_id: app_id in qa_completed_application_ids
        for app_id in application_ids
    }


def find_qa_complete_flag(application_id):
    qa_complete_flag = Flag.query.filter(
        Flag.application_id == application_id, Flag.flag_type == "QA_COMPLETED"
    ).first()

    return {"is_qa_complete": bool(qa_complete_flag)}


def find_qa_complete_flag_for_applications(application_ids: list[str]) -> dict:
    flags = Flag.query.filter(
        Flag.application_id.in_(application_ids),
        Flag.flag_type == "QA_COMPLETED",
    ).all()

    metadata_serialiser = FlagMetadata()
    flag_metadatas = [metadata_serialiser.dump(flag) for flag in flags]

    return flag_metadatas


def retrieve_flags_for_applications(application_ids: list[str]) -> dict:
    flags = (
        Flag.query.filter(Flag.application_id.in_(application_ids))
        .order_by(Flag.date_created.desc())
        .all()
    )

    metadata_serialiser = FlagMetadata()
    flag_metadatas = [metadata_serialiser.dump(flag) for flag in flags]

    return flag_metadatas


def get_latest_flags_for_each(flag_type: str = None) -> dict:

    # Create subquery to select latest flag for applications
    subquery = (
        db.session.query(
            Flag.application_id,
            db.func.max(Flag.date_created).label("latest_date"),
        )
        .group_by(Flag.application_id)
        .subquery()
    )

    # JOIN with main query of flags
    query = db.session.query(Flag).join(
        subquery,
        and_(
            Flag.application_id == subquery.c.application_id,
            Flag.date_created == subquery.c.latest_date,
        ),
    )

    # Add filter of flag_type if provided
    if flag_type:
        query = query.where(Flag.flag_type == flag_type)

    flags = db.session.execute(query).scalars().all()

    metadata_serialiser = FlagMetadata()
    flag_metadatas = [metadata_serialiser.dump(flag) for flag in flags]

    return flag_metadatas
