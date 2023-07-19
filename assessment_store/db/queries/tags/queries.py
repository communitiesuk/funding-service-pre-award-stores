from typing import List

from db import db
from db.models.tag.tag_types import TagType
from db.models.tag.tags import Tag
from flask import current_app


def insert_tags(tags, fund_id, round_id):
    """
    Inserts tags associated with a round.

    Args:
        tags (list): A list of tag dictionaries [{
                "value": "",
                "purpose": "",
                "creator_user_id": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        inserted_tags (list): This method returns a list of inserted tags (the tag id and key)
    """
    inserted_tags = []
    for tag_data in tags:
        value = tag_data.get("value")
        creator_user_id = tag_data.get("creator_user_id")
        tag_type_id = tag_data.get("tag_type_id")

        # Create a new tag instance and trigger validation
        tag = Tag(
            value=value,
            fund_id=fund_id,
            round_id=round_id,
            creator_user_id=creator_user_id,
            type_id=tag_type_id,
        )
        db.session.add(tag)

        try:
            db.session.flush()  # Flush changes to trigger validation
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error inserting tag '{value}': {str(e)}"
            )
            raise ValueError(f"Error inserting tag '{value}': {str(e)}")

        inserted_tags.append(tag)

    db.session.commit()
    return inserted_tags


def select_tags_for_fund_round(
    fund_id: str,
    round_id: str,
) -> List[Tag]:
    tags = (
        db.session.query(
            Tag.id,
            Tag.value,
            Tag.active,
            Tag.type_id,
            Tag.fund_id,
            Tag.round_id,
            Tag.creator_user_id,
            Tag.created_at,
            TagType.purpose.label("purpose"),
            TagType.description.label("description"),
        )
        .join(TagType, Tag.type_id == TagType.id)
        .filter(Tag.fund_id == fund_id)
        .filter(Tag.round_id == round_id)
        .all()
    )
    return tags


def select_tags_types() -> List[TagType]:
    return db.session.query(TagType).all()
