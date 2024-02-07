from typing import Dict

from db.queries.comments import create_comment_for_application_sub_crit
from db.queries.comments import get_comments_for_application_sub_crit
from db.queries.comments import update_comment_for_application_sub_crit
from flask import request


def comments_for_application_sub_criteria(
    application_id: str = None,
    sub_criteria_id: str = None,
    theme_id: str = None,
    comment_id: str = None,
) -> Dict:
    """comments_for_application_sub_criteria Function used by the get endpoint
    `/comment`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param theme_id: The stringified theme UUID.
    :param comment_id: The stringified comment UUID.
    :return: A List of dictionaries.

    """

    comment_metadatas = get_comments_for_application_sub_crit(application_id, sub_criteria_id, theme_id, comment_id)

    return comment_metadatas


def post_comments_for_application_sub_criteria() -> Dict:
    """post_comments_for_application_sub_criteria Function used by the post
    endpoint `/comment`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param comment: The comment to be added.
    :param user_id: The stringified user_id UUID.
    :param comment_type: The comment_type.
    :param theme_id: The stringified theme UUID.
    :return: A dictionary.

    """
    args = request.get_json()
    application_id = args["application_id"]
    sub_criteria_id = args["sub_criteria_id"]
    comment = args["comment"]
    comment_type = args["comment_type"]
    user_id = args["user_id"]
    theme_id = args["theme_id"]

    created_comment = create_comment_for_application_sub_crit(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment=comment,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
    )

    return created_comment


def put_comments_for_application_sub_criteria() -> Dict:
    """put_comments_for_application_sub_criteria Function used by the put endpoint
    `/comment`.

    :param comment: The comment to be updated.
    :param comment_id: The stringified comment_id UUID.
    :return: A dictionary.

    """
    args = request.get_json()
    comment = args["comment"]
    comment_id = args["comment_id"]

    updated_comment = update_comment_for_application_sub_crit(
        comment=comment,
        comment_id=comment_id,
    )

    return updated_comment
