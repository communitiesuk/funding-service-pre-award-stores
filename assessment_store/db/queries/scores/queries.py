"""Queries which are performed on the `scores` table.

Joins allowed.
"""
import json
from typing import Dict
from typing import List

from db import db
from db.models.score import Score
from db.queries.assessment_records._helpers import derive_values_from_json
from db.schemas import ScoreMetadata
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import defer


def get_latest_score_for_application_sub_crit(
    application_id: str, sub_criteria_id: str
) -> Dict:
    """get_latest_score_for_application_sub_crit executes a query on scores
    which returns the most recent score for the given application_id and 
    sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: dictionary.
    """
    stmt = select(Score).where(
        Score.application_id == application_id,
        Score.sub_criteria_id == sub_criteria_id
        ).order_by(Score.date_created.desc())

    latest_score_metadata = db.session.scalar(stmt)
    metadata_serialiser = ScoreMetadata()
    latest_score_metadata = metadata_serialiser.dump(latest_score_metadata)

    return latest_score_metadata


def create_score_for_application_sub_crit(
    score: int, justification: str, application_id: str, 
    sub_criteria_id: str, user_id: str
) -> Dict:
    """create_score_for_application_sub_crit executes a query on scores
    which creates a justified score for the given application_id and 
    sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score: The score integer.
    :param justification: The justification text.
    :param date_created: The date_created.
    :param user_id: The stringified user_id.
    :return: dictionary.
    """
    score = Score(
        score=score, justification=justification, application_id=application_id, 
        sub_criteria_id=sub_criteria_id,user_id=user_id
    )
    db.session.add(score)
    db.session.commit()
    
    metadata_serialiser = ScoreMetadata()
    score_metadata = metadata_serialiser.dump(score)
    
    return score_metadata
