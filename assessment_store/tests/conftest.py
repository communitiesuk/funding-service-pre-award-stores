import json
from uuid import uuid4

import pytest
from app import create_app
from db.models.flags.flags import Flag
from db.queries import bulk_insert_application_record
from db.queries import delete_assessment_record
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
        if "flags" in app:
            app_flags = app["flags"]
            app.pop("flags")
        inserted_application = bulk_insert_application_record(
            [app], "COF", True
        )[0]
        app["flags"] = app_flags
        inserted_applications.append(inserted_application)
        for f in app_flags:
            flag = Flag(application_id=app_id, **f)
            _db.session.add(flag)
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


@pytest.fixture(scope="session")
def app():
    attach_listeners()

    app = create_app()

    yield app
