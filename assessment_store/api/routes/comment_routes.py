from typing import Dict

from db.queries.comments import create_comment_for_application_sub_crit
from db.queries.comments import get_comments_for_application_sub_crit
from flask import request


def comments_for_application_sub_criteria(
    application_id: str, sub_criteria_id: str, theme_id: str = None
) -> Dict:
    """comments_for_application_sub_criteria Function
    used by the get endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A List of dictionaries.
    """

    comment_metadatas = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id
    )

    return comment_metadatas


def post_comments_for_application_sub_criteria() -> Dict:
    """post_comments_for_application_sub_criteria Function
    used by the post endpoint `/applications/{application_id}/
    subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A dictionary.
    """
    args = request.get_json()
    application_id = args["application_id"]
    sub_criteria_id = args["sub_criteria_id"]
    comment = args["comment"]
    comment_type = args["comment_type"]
    user_id = args["user_id"]
    theme_id = args["theme_id"]

    created_score = create_comment_for_application_sub_crit(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment=comment,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
    )

    return created_score
