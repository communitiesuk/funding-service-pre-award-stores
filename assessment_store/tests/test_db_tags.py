import random
from uuid import uuid4

import pytest
from api.routes.tag_routes import get_tags_for_fund_round
from api.routes.tag_routes import update_tags_for_fund_round
from app import app
from db.queries.assessment_records.queries import associate_assessment_tags
from db.queries.tags.queries import get_tag_by_id
from db.queries.tags.queries import insert_tags
from tests.conftest import test_input_data

# _db.session.remove()
# This operation cleans up the session resources and ensures that
# the session is properly closed following the raised error.

tags_incorrect_format = [
    {
        "key": "Test tag 1",
        "purpose": "Green",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "Not recommended",
        "species": "silk",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "For discussion",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "Incomplete - not for review",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
]


def test_insert_tags(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Not recommended",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "For discussion",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Incomplete - not for review",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    tag_values = [x["value"] for x in tags_correct_format]
    result = insert_tags(tags_correct_format, fund_id_test, round_id_test)
    assert len(result) == 4
    assert [tag.value in tag_values for tag in result]


def test_insert_tags_fails_for_tag_with_special_chars(
    _db, clear_test_data, get_tag_types
):
    tag_type_ids = [t["id"] for t in get_tag_types]
    tag_special_chars = [
        {
            "value": "Test tag 1 !£",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(ValueError) as e_info:
        insert_tags(tag_special_chars, fund_id_test, round_id_test)
    assert (
        "The value should only contain apostrophes, hyphens, letters, digits, and spaces."
        in str(e_info.value)
    )
    _db.session.remove()


def test_insert_tags_for_same_fund_round_twice_fails(
    _db, clear_test_data, get_tag_types
):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        }
    ]
    insert_tags(tags_correct_format, fund_id_test, round_id_test)

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_correct_format, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_same_payload_fails(
    _db, clear_test_data, get_tag_types
):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    same_tags_with_different_cases = [
        {
            "value": "same test tag",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "same test tag",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(
            same_tags_with_different_cases, fund_id_test, round_id_test
        )

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_not_case_sensitive_fails(
    _db, clear_test_data, get_tag_types
):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    same_tags_with_different_cases = [
        {
            "value": "SAME TEST TAG NOT CASE",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "same test tag not case",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(
            same_tags_with_different_cases, fund_id_test, round_id_test
        )

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_tags_bad_tag_format(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(Exception) as e_info:
        insert_tags(tags_incorrect_format, fund_id_test, round_id_test)

    assert "'NoneType' object has no attribute 'strip" in str(e_info.value)
    _db.session.remove()


def test_insert_tag_with_unknown_type_id_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tags_unknown_tag_type = [
        {
            "value": "same test tag not case",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": "4dd2b7d8-12f0-482f-b64b-8809b19baa93",
        },
    ]
    with pytest.raises(Exception) as e_info:
        insert_tags(tags_unknown_tag_type, fund_id_test, round_id_test)

    assert "ForeignKeyViolation" in str(e_info.value)
    # This operation cleans up the session resources and ensures
    # that the session is properly closed following the raised error.
    _db.session.remove()


def test_get_tags(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Not recommended",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    insert_tags(tags_correct_format, fund_id_test, round_id_test)
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    tag_values = [x["value"] for x in tags_correct_format]
    assert len(result) == 2
    assert result[0]["value"] in tag_values
    assert all(
        key in result[0].keys()
        for key in [
            "round_id",
            "creator_user_id",
            "fund_id",
            "purpose",
            "created_at",
            "value",
            "id",
            "active",
        ]
    )


def test_deactivate_tags(_db, clear_test_data, seed_tags):
    seeded_tag = seed_tags[0]
    fund_id_test = seeded_tag["fund_id"]
    round_id_test = seeded_tag["round_id"]
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)
    # Deactivate tag
    tags_to_update = [{"active": False, "id": seeded_tag["id"]}]
    with app.test_request_context(json=tags_to_update):
        update_tags_for_fund_round(fund_id_test, round_id_test)
    result = get_tags_for_fund_round(
        fund_id_test, round_id_test, tag_status=True
    )
    assert len(result) == 1
    result = get_tags_for_fund_round(
        fund_id_test, round_id_test, tag_status=False
    )
    assert len(result) == 1
    # Reactivate tag
    tags_to_update = [{"active": True, "id": seeded_tag["id"]}]
    with app.test_request_context(json=tags_to_update):
        update_tags_for_fund_round(fund_id_test, round_id_test)
    result = get_tags_for_fund_round(
        fund_id_test, round_id_test, tag_status=True
    )
    assert len(result) == 2
    result = get_tags_for_fund_round(
        fund_id_test, round_id_test, tag_status=False
    )
    assert result.status_code == 204
    assert result.data.decode("utf-8") == ""


def test_deactivate_tags_fails_for_non_existent(
    _db, clear_test_data, seed_tags
):
    seeded_tag = seed_tags[0]
    fund_id_test = seeded_tag["fund_id"]
    round_id_test = seeded_tag["round_id"]
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)
    tags_to_update = [
        {"active": False, "id": "68d39aee-4f4a-42d2-a2e7-66c5934905a1"}
    ]

    # simulate request body
    with app.test_request_context(json=tags_to_update):
        with pytest.raises(Exception) as e_info:
            update_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(
        text in str(e_info.value)
        for text in ["Tag with id", "does not exist for fund_id"]
    )

    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)


def test_get_tag(seed_tags):
    tag_id = seed_tags[0]["id"]
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag
    assert str(tag.id) == tag_id
    assert tag.value == "Test tag 1"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_tag_includes_tag_association_count(
    seed_application_records, seed_tags
):
    tag_id = seed_tags[0]["id"]
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag
    assert str(tag.id) == tag_id
    assert tag.tag_association_count == 0
    assert tag.value == "Test tag 1"

    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {"id": tag["id"], "user_id": "1d49a41c-a13e-41ab-a89c-240b3de3fbda"}
        for tag in seed_tags
    ]
    associate_assessment_tags(app_id, new_tags)
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag
    assert str(tag.id) == tag_id
    assert tag.tag_association_count == 1
    assert tag.value == "Test tag 1"


def test_get_tag_bad_id(seed_tags):
    tag_id = str(uuid4())
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag is None
