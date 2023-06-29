from uuid import uuid4

import pytest
from db.models import Flag
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Status
from db.models.flags_v2.flag_update import FlagStatus
from db.queries import create_flag_for_application
from db.queries import find_qa_complete_flag_for_applications
from db.queries import retrieve_flag_for_application
from db.queries.flags.queries import get_latest_flags_for_each
from db.queries.flags_v2.queries import add_update_to_assessment_flag
from db.queries.flags_v2.queries import (
    create_flag_for_application as create_flag_v2,
)
from db.queries.flags_v2.queries import get_flags_for_application
from sqlalchemy import select
from tests._helpers import get_assessment_record
from tests.conftest import test_input_data
from tests.test_data.flags import add_flag_update_request_json
from tests.test_data.flags import flag_config
from tests.test_data.flags import flag_config_v2


@pytest.mark.apps_to_insert([test_input_data[0]])
@pytest.mark.parametrize("flag_config", flag_config)
def test_create_flag_for_application(flag_config, seed_application_records):
    flag = Flag(**flag_config)
    result = create_flag_for_application(
        application_id=seed_application_records[0]["application_id"],
        justification=flag.justification,
        sections_to_flag=flag.sections_to_flag,
        user_id=flag.user_id,
        flag_type=flag.flag_type,
    )

    assert result["justification"] == flag.justification
    assert result["sections_to_flag"] == flag.sections_to_flag
    assert (
        result["application_id"]
        == seed_application_records[0]["application_id"]
    )
    assert result["user_id"] == flag.user_id
    assert result["flag_type"] == flag.flag_type.name


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "flags": flag_config[0:2]}]
)
def test_retrieve_flag_for_application(_db, seed_application_records):
    """Put two flags for the same application and expect the most
    recent flag to be retuned for the application."""
    result = retrieve_flag_for_application(
        seed_application_records[0]["application_id"]
    )

    assert result["justification"] == "Latest 1"
    assert result["sections_to_flag"][0] == "Test section 1"
    assert (
        result["application_id"]
        == seed_application_records[0]["application_id"]
    )


@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[1], "flags": [flag_config[4]]},
        {**test_input_data[2], "flags": [flag_config[0]]},
    ]
)
def test_find_qa_complete_flag_for_applications(_db, seed_application_records):
    """Put QA_COMPLETED flags in 2 out of 3 applications and
    only retrieve the metadata for the 1 with QA_COMPLETED"""

    result = find_qa_complete_flag_for_applications(
        [app["application_id"] for app in seed_application_records]
    )

    assert len(result) == 2
    assert (
        result[0]["application_id"]
        == seed_application_records[0]["application_id"]
    )
    assert result[0]["flag_type"] == "QA_COMPLETED"
    assert (
        result[1]["application_id"]
        == seed_application_records[1]["application_id"]
    )
    assert result[1]["flag_type"] == "QA_COMPLETED"


# TODO Remove skip once get_latest_flags_for_each can filter on fund/round id.
# In the meantime, will work if run in isolation
@pytest.mark.skip(reason="Filter on fund and round id")
@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[0], flag_config[1]]},
        {**test_input_data[1], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[2], "flags": [flag_config[4], flag_config[5]]},
    ]
)
def test_get_latest_flags_for_each(seed_application_records):
    result_list = get_latest_flags_for_each()

    assert len(result_list) == 3
    assert result_list[0]["justification"] == "Latest 1"
    assert result_list[1]["justification"] == "Latest 2"
    assert result_list[2]["justification"] == "Latest 3"


# TODO Remove skip once get_latest_flags_for_each can filter on fund/round id.
# In the meantime, will work if run in isolation
@pytest.mark.skip(reason="Filter on fund and round id")
@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[0], flag_config[1]]},
        {**test_input_data[1], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[2], "flags": [flag_config[4], flag_config[5]]},
    ]
)
def test_get_latest_flags_for_each_with_type_filter(seed_application_records):
    result_list = get_latest_flags_for_each("QA_COMPLETED")

    assert len(result_list) == 1
    assert result_list[0]["flag_type"] == "QA_COMPLETED"


# @pytest.mark.skip(reason="integrate flags into seeded data")
@pytest.mark.parametrize(
    "status_or_flag, expected_application_count",
    [
        (
            "NOT_STARTED",
            1,
        ),
        (
            "IN_PROGRESS",
            1,
        ),
        (
            "COMPLETED",
            1,
        ),
        (
            "FLAGGED",
            1,
        ),
        (
            "STOPPED",
            0,
        ),
        (
            "QA_COMPLETED",
            1,
        ),
        (
            "UNKNOWN_STATUS_OR_FLAG",
            3,
        ),
    ],
)
@pytest.mark.apps_to_insert(
    [
        test_input_data[0],
        {**test_input_data[1], "flags": [flag_config[2]]},
        {**test_input_data[2], "flags": [flag_config[1]]},
    ]
)
def test_get_most_recent_metadata_statuses_for_fund_round_id(
    _db, status_or_flag, expected_application_count, seed_application_records
):
    from db.queries.assessment_records.queries import (
        get_metadata_for_fund_round_id,
    )

    app_1 = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    app_2 = get_assessment_record(
        seed_application_records[1]["application_id"]
    )
    app_1.workflow_status = Status.IN_PROGRESS
    app_2.workflow_status = Status.COMPLETED
    _db.session.add_all([app_1, app_2])
    _db.session.commit()

    metadata = get_metadata_for_fund_round_id(
        seed_application_records[0]["fund_id"],
        seed_application_records[0]["round_id"],
        "",
        "",
        status_or_flag,
    )
    assert expected_application_count == len(metadata)


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_create_flag(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags_v2) == 0

    user_id = uuid4()
    flag_data = {
        "application_id": str(app_id),
        "sections_to_flag": ["section_1", "section_2"],
        "justification": "justifying the flag creation",
        "user_id": str(user_id),
        "status": FlagStatus.RAISED,
        "allocation": "TEAM_1",
    }
    create_result = create_flag_v2(**flag_data)
    assert create_result.latest_status == FlagStatus.RAISED

    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags_v2) == 1


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "flags_v2": [flag_config_v2[0]]}]
)
def test_add_flag_update(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags_v2) == 1
    assert len(results[0].flags_v2[0].updates) == 1
    assert results[0].flags_v2[0].latest_allocation == "TEAM_1"

    updated_flag = add_update_to_assessment_flag(
        **add_flag_update_request_json,
        assessment_flag_id=results[0].flags_v2[0].id,
    )
    assert (
        updated_flag.latest_allocation
        == add_flag_update_request_json["allocation"]
    )

    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags_v2) == 1
    assert len(results[0].flags_v2[0].updates) == 2
    assert results[0].flags_v2[0].latest_status == FlagStatus.STOPPED
    assert results[0].flags_v2[0].latest_allocation == "TEAM_2"


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "flags_v2": [flag_config_v2[0]]}]
)
def test_get_flags_for_application(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    result = get_flags_for_application(app_id)
    assert len(result) == 1
    assert result[0].updates[0].justification == "Test justification 2"
    assert result[0].sections_to_flag[0] == "Test section 2"
