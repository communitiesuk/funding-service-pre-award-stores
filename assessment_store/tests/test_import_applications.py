# noqa: E501
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
    fundround = request.getfixturevalue("fundround")
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
def mock_args_fundround(request):
    fundround = request.getfixturevalue("fundround")
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=Namespace(fundround=fundround),
    ) as args:
        yield args


@pytest.fixture(scope="function")
def mock_bulk_insert_application_records(
    request, mock_request_get_application
):
    application_json_list = mock_request_get_application
    mock_db_session = [
        Namespace(application_id=app_json["id"])
        for app_json in application_json_list
    ]  # mock.Mock()
    # mock_postgres_insert = mock.Mock()
    # mock_postgres_insert.return_value = mock_postgres_insert
    # mock_upsert_rows_stmt = mock.Mock()
    # mock_upsert_rows_stmt.on_conflict_do_nothing.return_value = mock_upsert_rows_stmt
    # mock_result = mock.Mock()
    # # mock_result.__iter__.return_value = iter([AssessmentRecord()])

    # # Calling bulk_insert_application_record with mocked data and checking if duplicated application id is being handled correctly # noqa: E501
    # with (mock.patch('db.queries.assessment_records.queries.postgres_insert', mock_postgres_insert),
    #         mock.patch('db.queries.assessment_records.queries.db.session.execute', return_value=mock_db_session),
    #         mock.patch('db.queries.assessment_records.queries.db.session.commit', return_value=None)
    #         ):
    #     #     mock.patch('main.AssessmentRecord', return_value=AssessmentRecord()),
    #     #     mock.patch('sqlalchemy.engine.ResultProxy', return_value=mock_result)):
    #     # mock_upsert_rows_stmt.return_value = mock.Mock()
    #     # mock_upsert_rows_stmt.return_value.returning.return_value = []
    #     # mock_db_session.return_value = mock.Mock()
    #     # mock_db_session.return_value.returning.return_value = [Namespace(application_id=app_json['id']) for app_json in application_json_list] # noqa: E501
    #     # with mock.patch('main.postgres_insert', mock_postgres_insert):
    #     yield

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
    request,
    fundround,
    appcount,
    mock_args_fundround,
    mock_request_get_application,
    mock_bulk_insert_application_records,
):
    inserted_rows = main()
    assert len(inserted_rows) == appcount
    assert True


# @pytest.mark.parametrize(
#     "roundid,app_type,appcount",
#     [
#         ("e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762", "COF", 1),
#     ],
# )
# def test_import_application_with_roundid(request, roundid, app_type, appcount, mock_args_fundround, mock_request_get_application, mock_bulk_insert_application_records): # noqa: E501
#     inserted_rows = main()
#     assert len(inserted_rows) == appcount
#     assert True
