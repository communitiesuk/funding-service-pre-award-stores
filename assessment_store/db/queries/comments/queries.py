"""Queries which are performed on the `scores` table.
Joins allowed.
"""

import json
from typing import Dict
from typing import List
from db import db
from db.models.comment.comments import Comment
from db.schemas import CommentMetadata
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.orm import load_only

# May need rewrite after testing
def get_comments_for_application_sub_crit(
    application_id: str, sub_criteria_id: str
) -> Dict:
    """get_comments_for_application_sub_crit executes a query on comments
    which returns a list of comments for the given application_id and 
    sub_criteria_id.
    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: dictionary.
    """
    stmt = select(Comment).where(
        Comment.application_id == application_id,
        Comment.sub_criteria_id == sub_criteria_id
        ).order_by(Comment.date_created.desc()).limit(1)

    comments_row = db.session.scalar(stmt)
    metadata_serialiser = CommentMetadata()
    comments_metadata = metadata_serialiser.dump(comments_row)

    return comments_metadata

def create_comment_for_application_sub_crit(
    application_id: str, 
    sub_criteria_id: str,
    comment: str,
    comment_type: str,
    user_id: str
) -> Dict:
    """create_comment_for_application_sub_crit executes a query on comments
    which creates a comment for the given application_id and 
    sub_criteria_id.
    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param comment: The comment string.
    :param comment_type: The type of comment for ENUM.
    :param date_created: The date_created.
    :param user_id: The stringified user_id.
    :return: dictionary.
    """
    score = Comment(
        application_id=application_id, 
        sub_criteria_id=sub_criteria_id,
        comment=comment,
        comment_type=comment_type,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()

    metadata_serialiser = CommentMetadata()
    comment_metadata = metadata_serialiser.dump(score)

    return comment_metadata