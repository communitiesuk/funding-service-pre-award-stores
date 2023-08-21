import logging
from os import getenv

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger("SQS_Recieve")
logger.setLevel(logging.DEBUG)

_SQS_CLIENT = boto3.client(
    "sqs",
    region_name=getenv("AWS_REGION", None),
    endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
)
_SQS_QUEUE_URL = _SQS_CLIENT.get_queue_url(
    QueueName=getenv("AWS_SQS_QUEUE_NAME"),
)["QueueUrl"]


def receive_messages(max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        response = _SQS_CLIENT.receive_message(
            QueueUrl=_SQS_QUEUE_URL,
            AttributeNames=["SentTimestamp"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=0,
            WaitTimeSeconds=wait_time,
        )
        messages = response["Messages"]

        for msg in messages:
            logger.info("Received message: %s: %s", msg.message_id, msg.body)
    except ClientError as error:
        logger.exception(
            "Couldn't receive messages from queue: %s", _SQS_QUEUE_URL
        )
        raise error
    else:
        return messages


def delete_messages(messages):
    """
    Delete a batch of messages from a queue in a single request.

    :param queue: The queue from which to delete the messages.
    :param messages: The list of messages to delete.
    :return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    try:
        entries = [
            {"Id": str(ind), "ReceiptHandle": msg.receipt_handle}
            for ind, msg in enumerate(messages)
        ]
        response = _SQS_CLIENT.delete_message(
            QueueUrl=_SQS_QUEUE_URL, Entries=entries
        )
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                logger.info(
                    "Deleted %s", messages[int(msg_meta["Id"])].receipt_handle
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                logger.warning(
                    "Could not delete %s",
                    messages[int(msg_meta["Id"])].receipt_handle,
                )
    except ClientError:
        logger.exception(
            "Couldn't delete messages from queue %s", _SQS_QUEUE_URL
        )
    else:
        return response
