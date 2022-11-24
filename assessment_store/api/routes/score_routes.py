# flake8: noqa
from typing import Dict
from typing import List

from db.queries.scores import get_just_score_for_application_sub_crit
from db.queries.scores import post_just_score_for_application_sub_crit
from db.schemas import JustScoreMetadata


def latest_score_for_application_sub_criteria(
    application_id: str, sub_criteria_id: str
) -> Dict:
    """latest_score_for_application_sub_criteria Function 
    used by the get endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A dictionary.
    """

    latest_score = get_just_score_for_application_sub_crit(
        application_id=application_id, sub_criteria_id=sub_criteria_id
    )

    return latest_score


def post_score_for_application_sub_criteria(
    score: int, justification: str, application_id: str, timestamp: str, 
    sub_criteria_id: str, user_id: str
) -> Dict:
    """post_score_for_application_sub_criteria Function 
    used by the post endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A dictionary.
    """

    post_score = post_just_score_for_application_sub_crit(
        application_id=application_id, sub_criteria_id=sub_criteria_id,
        score=score, justification=justification, user_id=user_id,
        timestamp=timestamp
    )

    return post_score
