"""Queries which are performed on the `scores` table.

Joins allowed.
"""
from typing import Dict

from db import db
from db.models import AssessmentRecord
from db.models.score import Score
from db.schemas import ScoreMetadata
from sqlalchemy import select


def get_scores_for_app_sub_crit(
    application_id: str, sub_criteria_id: str, score_history: bool = False
) -> list[dict]:
    """get_scores_for_app_sub_crit executes a query on scores
    which returns the most recent score or all scores for the
    given application_id and sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score_history: Boolean value that reurns all scores if true
    :return: dictionary.
    """
    if score_history:
        stmt = (
            select(Score)
            .where(
                Score.application_id == application_id,
                Score.sub_criteria_id == sub_criteria_id,
            )
            .order_by(Score.date_created.desc())
        )
    else:
        stmt = (
            select(Score)
            .where(
                Score.application_id == application_id,
                Score.sub_criteria_id == sub_criteria_id,
            )
            .order_by(Score.date_created.desc())
            .limit(1)
        )

    score_rows = db.session.scalars(stmt)

    metadata_serialiser = ScoreMetadata()

    score_metadatas = [
        metadata_serialiser.dump(score_row) for score_row in score_rows
    ]

    return score_metadatas


def create_score_for_app_sub_crit(
    score: int,
    justification: str,
    application_id: str,
    sub_criteria_id: str,
    user_id: str,
) -> Dict:
    """create_score_for_app_sub_crit executes a query on scores
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
        score=score,
        justification=justification,
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        user_id=user_id,
    )
    db.session.add(score)
    db.session.commit()

    metadata_serialiser = ScoreMetadata()
    score_metadata = metadata_serialiser.dump(score)

    return score_metadata


def get_sub_criteria_to_latest_score_map(application_id: str) -> dict:
    stmt = (
        select([Score.sub_criteria_id, Score.score])
        .select_from(Score)
        .join(
            AssessmentRecord,
            Score.application_id == AssessmentRecord.application_id,
        )
        .where(AssessmentRecord.application_id == application_id)
        .order_by(Score.date_created.desc())
    )

    result = db.session.execute(stmt).fetchall()

    sub_criteria_to_latest_score = {}
    for sid, score in result:
        if sid not in sub_criteria_to_latest_score:
            sub_criteria_to_latest_score[sid] = score

    return sub_criteria_to_latest_score
