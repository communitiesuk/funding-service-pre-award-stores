import json

import pytest
from _helpers import delete_messages
from _helpers import receive_messages
from _helpers.import_application import import_applications_from_queue
from config.mappings.assessment_mapping_fund_round import (
    fund_round_mapping_config,
)
from tests._helpers import row_data


@pytest.fixture(scope="function")
def mock_sqs_recieve_message(request, mocker):
    fundround = request.node.get_closest_marker("fundround").args[0]
    appcount = request.node.get_closest_marker("appcount").args[0]

    fund_round_config = {fundround: fund_round_mapping_config[fundround]}
    application_json_strings = row_data(appcount, 1, 1, fund_round_config)
    messages = []
    for ind, application_json in enumerate(application_json_strings):
        messages.append(
            {
                "MessageId": str(ind + 1),
                "Body": json.loads(application_json),
                "ReceiptHandle": str(ind),
            }
        )

    mocker.patch(
        "_helpers._SQS_CLIENT.receive_message",
        return_value={"Messages": messages},
    )
    yield messages


@pytest.fixture(scope="function")
def mock_sqs_delete_message(request, mocker):
    appcount = request.node.get_closest_marker("appcount").args[0]
    mocker.patch(
        "_helpers._SQS_CLIENT.delete_message_batch",
        return_value={
            "Successful": [{"Id": str(count)} for count in range(appcount)]
        },
    )
    yield


@pytest.fixture(scope="function")
def mock_bulk_insert_application_records(mocker, mock_sqs_recieve_message):
    messages = mock_sqs_recieve_message
    mock_db_session = [
        {
            "application_id": msg["Body"]["id"],
            "round_id": msg["Body"]["round_id"],
            "short_ref": msg["Body"]["reference"],
        }
        for msg in messages
    ]
    with (
        mocker.patch(
            "_helpers.import_application.bulk_insert_application_record",
            return_value=mock_db_session,
        )
    ):
        yield


class TestSQSFunctions(object):
    @pytest.mark.fundround("NSTFR2")
    @pytest.mark.appcount(3)
    def test_receive_messages(self, request, mock_sqs_recieve_message):
        appcount = request.node.get_closest_marker("appcount").args[0]

        # Call the function
        messages = receive_messages(max_number=2)

        # Assertions
        assert len(messages) == appcount
        assert messages[0]["MessageId"] == "1"

    @pytest.mark.appcount(3)
    def test_delete_messages(self, request, mock_sqs_delete_message):
        appcount = request.node.get_closest_marker("appcount").args[0]

        # Call the function
        receipt_handles = [
            "receipt_handle_" + str(count) for count in range(appcount)
        ]
        response = delete_messages(receipt_handles)

        # Assertions
        assert len(response["Successful"]) == appcount

    @pytest.mark.fundround("NSTFR2")
    @pytest.mark.appcount(3)
    def test_import_application_queue(
        self,
        request,
        mock_sqs_recieve_message,
        mock_sqs_delete_message,
        mock_bulk_insert_application_records,
    ):
        appcount = request.node.get_closest_marker("appcount").args[0]

        # Call the function
        response = import_applications_from_queue()

        # Assertions
        assert len(response) == appcount
