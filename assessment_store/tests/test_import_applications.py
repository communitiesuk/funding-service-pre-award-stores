import json
from argparse import Namespace
from unittest import mock

import pytest
from config.mappings.assessment_mapping_fund_round import (
    fund_round_mapping_config,
)
from requests import Response
from scripts.import_from_application import main
from tests._helpers import row_data


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
    application_json_list = [
        json.loads(application_json)
        for application_json in application_json_strings
    ]
    with (
        mock.patch("requests.get", return_value=Response()),
        mock.patch(
            "requests.Response.json", return_value=application_json_list
        ),
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
            return_value=Namespace(
                roundid=roundid, app_type=app_type, fundround=None
            ),
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
    with (
        mock.patch(
            "scripts.import_from_application.bulk_insert_application_record",
            return_value=mock_db_session,
        )
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
