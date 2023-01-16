# flake8: noqa
from typing import Dict
from typing import List

from db.queries import create_score_for_app_sub_crit
from db.queries import get_scores_for_app_sub_crit
from flask import request


def get_score_for_application_sub_criteria(
    application_id: str, sub_criteria_id: str, score_history: bool = False
) -> List[Dict]:
    """get_score_for_application_sub_criteria Function
    used by the get endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score_history: Boolean to return all scores if true
    :return: A List of dictionaries.
    """

    score_metadata = get_scores_for_app_sub_crit(
        application_id, sub_criteria_id, score_history
    )

    return score_metadata


def post_score_for_application_sub_criteria() -> Dict:
    """post_score_for_application_sub_criteria Function
    used by the post endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A dictionary.
    """
    args = request.get_json()
    application_id = args["application_id"]
    sub_criteria_id = args["sub_criteria_id"]
    score = args["score"]
    justification = args["justification"]
    user_id = args["user_id"]

    created_score = create_score_for_app_sub_crit(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        score=score,
        justification=justification,
        user_id=user_id,
    )

    return created_score
