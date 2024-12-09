import json
from argparse import Namespace
from unittest import mock
from uuid import uuid4

import pytest
from requests import Response

from assessment_store.config.mappings.assessment_mapping_fund_round import (
    fund_round_mapping_config,
)
from assessment_store.db.models.assessment_record.assessment_records import (
    AssessmentRecord,
)
from assessment_store.db.queries.assessment_records.queries import (
    insert_application_record,
)
from assessment_store.scripts.import_from_application import main
from tests.assessment_store_tests._helpers import row_data


@pytest.fixture(scope="function")
def mock_request_get_application(request):
    if "fundround" in request.fixturenames:
        fundround = request.getfixturevalue("fundround")
    if "roundid" in request.fixturenames:
        roundid = request.getfixturevalue("roundid")
        for k, v in fund_round_mapping_config.items():
            if v["round_id"] == roundid:
                fundround = k
                break
    appcount = request.getfixturevalue("appcount")
    fund_round_config = {fundround: fund_round_mapping_config[fundround]}
    application_json_strings = row_data(appcount, 1, 1, fund_round_config)
    application_json_list = [json.loads(application_json) for application_json in application_json_strings]
    with (
        mock.patch("requests.get", return_value=Response()),
        mock.patch("requests.Response.json", return_value=application_json_list),
    ):
        yield application_json_list


@pytest.fixture(scope="function")
def mock_args(request):
    if "fundround" in request.fixturenames:
        fundround = request.getfixturevalue("fundround")
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(fundround=fundround),
        ) as args:
            yield args
    if "roundid" in request.fixturenames:
        roundid = request.getfixturevalue("roundid")
        app_type = request.getfixturevalue("app_type")
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(roundid=roundid, app_type=app_type, fundround=None),
        ) as args:
            yield args


@pytest.fixture(scope="function")
def mock_bulk_insert_application_records(mock_request_get_application):
    application_json_list = mock_request_get_application
    mock_db_session = [
        Namespace(
            application_id=app_json["id"],
            round_id=app_json["round_id"],
            short_ref=app_json["reference"],
        )
        for app_json in application_json_list
    ]
    with mock.patch(
        "assessment_store.scripts.import_from_application.bulk_insert_application_record",
        return_value=mock_db_session,
    ):
        yield


@pytest.mark.parametrize(
    "fundround,appcount",
    [
        ("COFR2W3", 1),
        ("COFR3W1", 2),
        ("NSTFR2", 3),
    ],
)
def test_import_application_with_fundround(
    fundround,
    appcount,
    mock_args,
    mock_request_get_application,
    mock_bulk_insert_application_records,
):
    roundid = fund_round_mapping_config[fundround]["round_id"]
    inserted_rows = main()
    assert len(inserted_rows) == appcount
    assert inserted_rows[0].round_id == roundid
    short_ref = "".join(inserted_rows[0].short_ref.split("-")[:2])
    assert short_ref == fundround


@pytest.mark.parametrize(
    "roundid,app_type,appcount",
    [
        ("e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762", "COF", 1),
    ],
)
def test_import_application_with_roundid(
    roundid,
    app_type,
    appcount,
    mock_args,
    mock_request_get_application,
    mock_bulk_insert_application_records,
):
    inserted_rows = main()
    assert len(inserted_rows) == appcount
    assert inserted_rows[0].round_id == roundid
    assert app_type in inserted_rows[0].short_ref


@pytest.mark.parametrize("application_type, is_json", [("CTDF", True), (None, True)])
@pytest.mark.apps_to_insert([])
def test_insert_application_record(
    ctdf_application,
    application_type,
    is_json,
    mocker,
    seed_application_records,
    _db,
):
    ctdf_application["application_id"] = str(uuid4())
    mocker.patch(
        "assessment_store.db.queries.assessment_records.queries.derive_application_values",
        return_value={
            "application_id": ctdf_application["application_id"],
            "project_name": ctdf_application["project_name"],
            "short_id": ctdf_application["reference"],
            "fund_id": ctdf_application["fund_id"],
            "round_id": ctdf_application["round_id"],
            "funding_amount_requested": 0,
            "asset_type": "test",
            "language": ctdf_application["language"],
            "location_json_blob": {
                "error": False,
                "county": "Not Available",
                "region": "Not Available",
                "country": "Not Available",
                "constituency": "Not Available",
                "postcode": "Not Available",
            },
        },
    )

    result = insert_application_record(
        application_json_string=ctdf_application,
        application_type=application_type,
        is_json=is_json,
    )
    assert result

    inserted_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == ctdf_application["application_id"])
        .one_or_none()
    )
    assert inserted_record


@pytest.mark.apps_to_insert([])
def test_insert_application_record_duplicate(mocker, seed_application_records, _db, ctdf_application):
    ctdf_application["application_id"] = str(uuid4())
    derived_values = {
        "application_id": ctdf_application["application_id"],
        "project_name": ctdf_application["project_name"],
        "short_id": ctdf_application["reference"],
        "fund_id": ctdf_application["fund_id"],
        "round_id": ctdf_application["round_id"],
        "funding_amount_requested": 0,
        "asset_type": "test",
        "language": ctdf_application["language"],
        "location_json_blob": {
            "error": False,
            "county": "Not Available",
            "region": "Not Available",
            "country": "Not Available",
            "constituency": "Not Available",
            "postcode": "Not Available",
        },
    }

    mocker.patch(
        "assessment_store.db.queries.assessment_records.queries.derive_application_values",
        return_value=derived_values,
    )

    result = insert_application_record(
        application_json_string=ctdf_application,
        application_type=None,
        is_json=True,
    )
    assert result

    inserted_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == ctdf_application["application_id"])
        .one_or_none()
    )
    assert inserted_record
    assert inserted_record.asset_type == "test"

    # Update the data and attempt insert of duplicate row - should do nothing and not update

    derived_values["asset_type"] = "updated row"
    mocker.patch(
        "assessment_store.db.queries.assessment_records.queries.derive_application_values",
        return_value=derived_values,
    )

    result2 = insert_application_record(
        application_json_string=ctdf_application,
        application_type=None,
        is_json=True,
    )
    assert result2

    inserted_record2 = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == ctdf_application["application_id"])
        .one_or_none()
    )
    assert inserted_record2
    assert inserted_record2.asset_type == "test"
