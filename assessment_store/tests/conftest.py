import json
import random
from uuid import uuid4

import pytest
from app import create_app
from db.models.assessment_record.tag_association import TagAssociation
from db.models.flags.flags import Flag
from db.models.flags_v2.assessment_flag import AssessmentFlag
from db.models.flags_v2.flag_update import FlagUpdate
from db.models.tag.tag_types import TagType
from db.queries import bulk_insert_application_record
from db.queries import delete_assessment_record
from db.queries.tags.queries import insert_tags
from db.schemas.schemas import TagSchema
from db.schemas.schemas import TagTypeSchema
from tests._sql_infos import attach_listeners

# Loads the fixtures in this module in utils to create and
# clear the unit test DB
pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]
with open("tests/test_data/hand-crafted-apps.json", "r") as f:
    test_input_data = json.load(f)


@pytest.fixture(scope="function")
def seed_application_records(
    request, app, clear_test_data, enable_preserve_test_data, _db
):
    """
    Inserts test assessment_record data into the unit test DB according
    to what's supplied using the marker apps_to_insert.
    Supplies these inserted records back to the requesting test function
    """
    marker = request.node.get_closest_marker("apps_to_insert")
    if marker is None:
        apps = 1
    else:
        apps = marker.args[0]
    marker = request.node.get_closest_marker("unique_fund_round")
    if marker is None:
        unique_fund_round = False
    else:
        unique_fund_round = True

    inserted_applications = []

    random_fund_id = str(uuid4())
    random_round_id = str(uuid4())

    for app in apps:

        app_id = str(uuid4())
        app["id"] = app_id
        if unique_fund_round:
            app["fund_id"] = random_fund_id
            app["round_id"] = random_round_id
        app_flags = []
        app_flags_v2 = []
        if "flags" in app:
            app_flags = app.pop("flags")
        app_flags_v2 = []
        if "flags_v2" in app:
            app_flags_v2 = app.pop("flags_v2")
        app_tags = []
        if "app_tags" in app:
            app_tags = app.pop("app_tags")
        inserted_application = bulk_insert_application_record(
            [app], "COF", True
        )[0]
        app["flags"] = app_flags
        app["flags_v2"] = app_flags_v2
        app["app_tags"] = app_tags
        inserted_applications.append(inserted_application)
        for f in app_flags:
            flag = Flag(application_id=app_id, **f)
            _db.session.add(flag)
        for f in app_flags_v2:
            flag_update = FlagUpdate(
                justification=f["justification"],
                user_id=f["user_id"],
                status=f["status"],
                allocation=f["allocation"],
            )
            assessment_flag = AssessmentFlag(
                application_id=app_id,
                sections_to_flag=f["sections_to_flag"],
                latest_allocation=f["allocation"],
                latest_status=f["status"],
                updates=[flag_update],
            )
            _db.session.add(assessment_flag)
        for t in app_tags:
            tag = TagAssociation(application_id=app_id, tag_value=t)
            _db.session.add(tag)
        _db.session.commit()
    # Supplied the rows we inserted for tests to use in their actions
    yield inserted_applications

    for app in apps:
        app_id = app["id"]
        app_flags = app["flags"]
        for f in app_flags:
            flag = Flag.query.filter_by(application_id=app_id, **f).first()
            if flag:
                _db.session.delete(flag)
                _db.session.commit()
        delete_assessment_record(app_id)


@pytest.fixture(scope="function")
def seed_tags(
    request,
    app,
    clear_test_data,
    enable_preserve_test_data,
    _db,
    get_tag_types,
):
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Test tag 2",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    inserted_tags = insert_tags(
        tags_correct_format, fund_id_test, round_id_test
    )
    serialiser = TagSchema()
    serialised_associated_tags = [serialiser.dump(r) for r in inserted_tags]
    yield serialised_associated_tags


@pytest.fixture(scope="function")
def get_tag_types(
    request, app, clear_test_data, enable_preserve_test_data, _db
):

    tag_type = TagType(
        id=uuid4(),
        purpose=uuid4(),
        description="Test tag type",
    )

    _db.session.add(tag_type)
    _db.session.commit()

    tag_types = _db.session.query(TagType).all()
    if tag_types:
        serialiser = TagTypeSchema()
        serialised_tag_types = [serialiser.dump(r) for r in tag_types]
        yield serialised_tag_types


@pytest.fixture(scope="session")
def app():
    attach_listeners()

    app = create_app()

    yield app
