from typing import Dict

from db import db
from db.models.flags_v2.assessment_flag import AssessmentFlag
from db.models.flags_v2.flag_update import FlagStatus
from db.models.flags_v2.flag_update import FlagUpdate
from sqlalchemy import select


def get_flags_for_application(application_id):
    stmt = select(AssessmentFlag).where(
        AssessmentFlag.application_id == application_id
    )
    results = db.session.scalars(stmt).all()
    return results


def get_flag_by_id(flag_id):
    stmt = select(AssessmentFlag).where(AssessmentFlag.id == flag_id)
    results = db.session.scalars(stmt).all()
    return results


def create_flag_for_application(
    justification: str,
    sections_to_flag: str,
    application_id: str,
    user_id: str,
    status: FlagStatus,
    allocation: str,
) -> Dict:
    flag_update = FlagUpdate(
        justification=justification,
        user_id=user_id,
        status=status,
        allocation=allocation,
    )
    assessment_flag = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=sections_to_flag,
        latest_allocation=allocation,
        latest_status=status,
        updates=[flag_update],
    )
    db.session.add(assessment_flag)
    db.session.commit()
    return assessment_flag


def add_update_to_assessment_flag(
    justification: str,
    user_id: str,
    status: FlagStatus,
    allocation: str,
    assessment_flag_id: str,
) -> Dict:

    stmt = select(AssessmentFlag).where(
        AssessmentFlag.id == assessment_flag_id
    )

    assessment_flag = db.session.scalars(stmt).one()

    flag_update = FlagUpdate(
        justification=justification,
        user_id=user_id,
        status=status,
        allocation=allocation,
        assessment_flag_id=assessment_flag_id,
    )
    assessment_flag.updates.append(flag_update)
    assessment_flag.latest_allocation = allocation
    assessment_flag.latest_status = status

    db.session.add(assessment_flag)
    db.session.commit()
    return assessment_flag
