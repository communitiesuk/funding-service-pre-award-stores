import time
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

import boto3
import pytest
from fsd_utils.sqs_scheduler.context_aware_executor import ContextAwareExecutor
from moto import mock_aws
from sqlalchemy.exc import SQLAlchemyError

from _helpers.task_executer_service import TaskExecutorService
from config import Config
from tests.test_data.test_data_util import send_message_to_queue


class TestAssessmentTaskExecutorService(unittest.TestCase):
    @mock_aws
    @pytest.mark.usefixtures("live_server")
    def test_message_in_mock_environment_processing_without_errors(self):
        self._mock_aws_client()
        self._add_data_to_queue()

        self.task_executor.process_messages()

        self._check_is_data_available(0)

    @mock_aws
    @pytest.mark.usefixtures("live_server")
    @patch("db.queries.assessment_records.queries.db.session.execute")
    def test_message_in_mock_environment_processing_with_errors(self, mocked_execute):
        self._mock_aws_client()
        self._add_data_to_queue()

        mocked_execute.side_effect = SQLAlchemyError("Error calling notification service")
        self.task_executor.process_messages()
        time.sleep(5)
        self._check_is_data_available(1)

    def _mock_aws_client(self):
        self.flask_app = MagicMock()
        self.executor = ContextAwareExecutor(max_workers=10, thread_name_prefix="NotifTask", flask_app=self.flask_app)
        s3_connection = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="test_accesstoken",
            aws_secret_access_key="secret_key",  # pragma: allowlist secret
        )
        sqs_connection = boto3.client(
            "sqs",
            region_name="us-east-1",
            aws_access_key_id="test_accesstoken",
            aws_secret_access_key="secret_key",  # pragma: allowlist secret
        )
        s3_connection.create_bucket(Bucket=Config.AWS_MSG_BUCKET_NAME)
        self.queue_response = sqs_connection.create_queue(
            QueueName="import-queue.fifo", Attributes={"FifoQueue": "true"}
        )
        Config.AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = self.queue_response["QueueUrl"]
        self.task_executor = TaskExecutorService(
            flask_app=MagicMock(),
            executor=self.executor,
            s3_bucket=Config.AWS_MSG_BUCKET_NAME,
            sqs_primary_url=Config.AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL,
            task_executor_max_thread=Config.TASK_EXECUTOR_MAX_THREAD,
            sqs_batch_size=Config.SQS_BATCH_SIZE,
            visibility_time=Config.SQS_VISIBILITY_TIME,
            sqs_wait_time=Config.SQS_WAIT_TIME,
            region_name=Config.AWS_REGION,
            endpoint_url_override=Config.AWS_ENDPOINT_OVERRIDE,
            aws_access_key_id=Config.AWS_SQS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SQS_ACCESS_KEY_ID,
        )
        self.task_executor.sqs_extended_client.sqs_client = sqs_connection
        self.task_executor.sqs_extended_client.s3_client = s3_connection

    def _add_data_to_queue(self):
        for _x in range(1):
            application_attributes = {
                "application_id": {
                    "StringValue": "8be9756e-8404-4d79-9b70-abf15066845f",
                    "DataType": "String",
                },
                "S3Key": {
                    "StringValue": "assessment",
                    "DataType": "String",
                },
            }
            message_id = self.task_executor.sqs_extended_client.submit_single_message(
                queue_url=self.queue_response["QueueUrl"],
                message=send_message_to_queue,
                message_group_id="import_applications_group",
                message_deduplication_id=str(uuid4()),  # ensures message uniqueness
                extra_attributes=application_attributes,
            )
            assert message_id is not None

    def _check_is_data_available(self, count):
        response = self.task_executor.sqs_extended_client.receive_messages(
            queue_url=self.queue_response["QueueUrl"], max_number=1
        )
        assert len(response) == count
