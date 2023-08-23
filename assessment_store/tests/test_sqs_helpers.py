# import unittest
# from unittest.mock import Mock
# from unittest.mock import patch
import pytest
from _helpers import delete_messages
from _helpers import receive_messages

# from botocore.exceptions import ClientError


@pytest.fixture(scope="function")
def mock_sqs_recieve_message(mocker):

    mocker.patch(
        "_helpers._SQS_CLIENT.receive_message",
        return_value={
            "Messages": [
                {"MessageId": "1", "Body": "Message 1"},
                {"MessageId": "2", "Body": "Message 2"},
            ]
        },
    )
    yield


@pytest.fixture(scope="function")
def mock_sqs_delete_message(mocker):

    mocker.patch(
        "_helpers._SQS_CLIENT.delete_message_batch",
        return_value={"Successful": [{"Id": "0"}, {"Id": "1"}], "Failed": []},
    )
    yield


class TestSQSFunctions(object):
    def test_receive_messages(self, mock_sqs_recieve_message):
        # Call the function
        messages = receive_messages(max_number=2)

        # Assertions
        assert len(messages) == 2
        assert messages[0]["MessageId"] == "1"
        assert messages[1]["Body"] == "Message 2"

    # @patch("_helpers._SQS_CLIENT")
    # def test_receive_messages_no_messages(self, mock_sqs_client):
    #     # Mock response from SQS with no messages
    #     mock_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    #     mock_sqs_client.receive_message.return_value = mock_response

    #     # Call the function
    #     messages = receive_messages(max_number=2)

    #     # Assertions
    #     assert messages is None

    # @patch("_helpers._SQS_CLIENT")
    # def test_receive_messages_error(self, mock_sqs_client):
    #     # Mock ClientError
    #     mock_sqs_client.receive_message.side_effect = ClientError({}, "ReceiveMessage")

    #     # Call the function and assert it raises an error
    #     with self.assertRaises(ClientError):
    #         receive_messages(max_number=2)

    def test_delete_messages(self, mock_sqs_delete_message):
        # Call the function
        response = delete_messages(["receipt_handle_0", "receipt_handle_1"])

        # Assertions
        assert len(response["Successful"]) == 2

    # @patch("_helpers._SQS_CLIENT")
    # def test_delete_messages_error(self, mock_sqs_client):
    #     # Mock ClientError
    #     mock_sqs_client.delete_message_batch.side_effect = ClientError({}, "DeleteMessageBatch")

    #     # Call the function and assert it doesn't raise an error
    #     response = delete_messages(["receipt_handle_0", "receipt_handle_1"])
    #     self.assertIsNone(response)
