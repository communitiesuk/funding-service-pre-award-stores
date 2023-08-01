# flake8: noqa
from db.queries.tags.queries import get_tag_by_id
from db.queries.tags.queries import insert_tags
from db.queries.tags.queries import select_tags_for_fund_round
from db.queries.tags.queries import select_tags_types
from db.queries.tags.queries import update_tags
from db.schemas.schemas import JoinedTagSchema
from db.schemas.schemas import TagSchema
from db.schemas.schemas import TagTypeSchema
from flask import abort
from flask import current_app
from flask import request
from flask import Response


def get_tags_for_fund_round(
    fund_id,
    round_id,
    tag_purpose: str = "ALL",
    tag_status: bool = True,
    search_term: str = "",
    search_in: str = None,
):
    tags = select_tags_for_fund_round(
        fund_id, round_id, tag_purpose, tag_status, search_term, search_in
    )

    if tags:
        serialiser = JoinedTagSchema()
        serialised_tags = [serialiser.dump(r) for r in tags]
        return serialised_tags

    return Response(
        response=[],
        status=204,
    )


def get_tag_types():

    tag_types = select_tags_types()

    if tag_types:
        serialiser = TagTypeSchema()
        serialised_tag_types = [serialiser.dump(r) for r in tag_types]
        return serialised_tag_types

    return Response(response="No tags types.", status=204)


def add_tag_for_fund_round(fund_id, round_id):
    args = request.get_json()
    tag_value = args["value"]
    tag_type_id = args["tag_type_id"]
    creator_user_id = args["creator_user_id"]

    tags = [
        {
            "value": tag_value,
            "tag_type_id": tag_type_id,
            "creator_user_id": creator_user_id,
        }
    ]

    inserted_tags = insert_tags(tags, fund_id, round_id)

    if inserted_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in inserted_tags]
        return serialised_tags
    current_app.logger.error(f"Add tags attempt failed for tags: {tags}.")
    abort(404)


def update_tags_for_fund_round(fund_id, round_id):
    args = request.get_json()

    tags = [
        {
            "id": arg.get("id"),
            "value": arg.get("value"),
            "tag_type_id": arg.get("tag_type_id"),
            "creator_user_id": arg.get("creator_user_id"),
            "active": arg.get("active"),
        }
        for arg in args
    ]

    updated_tags = update_tags(tags, fund_id, round_id)

    if updated_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in updated_tags]
        return serialised_tags
    current_app.logger.error(f"Update tags attempt failed for tags: {tags}.")
    abort(404)


def get_tag(fund_id, round_id, tag_id):
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    if not tag:
        return abort(404)
    return JoinedTagSchema().dump(tag)
