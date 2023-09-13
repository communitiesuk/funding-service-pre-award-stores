from datetime import datetime
from os import getenv
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from config import Config


if (
    getenv("PRIMARY_QUEUE_URL", "Primary Queue URL Not Set")
    == "Primary Queue URL Not Set"
):
    _SQS_CLIENT = boto3.client(
        "sqs",
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION,
        endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
    )
else:
    _SQS_CLIENT = boto3.client(
        "sqs",
        region_name=Config.AWS_REGION,
        endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
    )

_SQS_QUEUE_URL = (
    Config.AWS_PRIMARY_QUEUE_URL
    or _SQS_CLIENT.get_queue_url(
        QueueName=getenv("AWS_SQS_QUEUE_NAME", "fsd-queue"),
    )["QueueUrl"]
)


def pack_message(msg_body):
    return {
        "body": msg_body,
        "attributes": {
            "id": {"StringValue": str(uuid4()), "DataType": "String"},
            "datetime": {
                "StringValue": str(datetime.now()),
                "DataType": "String",
            },
        },
    }


def unpack_message(msg):
    return (
        msg["MessageAttributes"]["id"]["StringValue"],
        msg["Body"],
        msg["MessageAttributes"]["datetime"]["StringValue"],
    )


def submit_message(queue_url, messages, DelaySeconds=1):
    """
    Send a batch of messages in a single request to an SQS queue.
    This request may return overall success even when some messages were not sent.
    The caller must inspect the Successful and Failed lists in the response and
    resend any failed messages.

    :param queue_url: SQS Queue url.
    :param queue: The queue to receive the messages.
    :param messages: The messages to send to the queue. These are simplified to
                     contain only the message body and attributes.
    :return: The response from SQS that contains the list of successful and failed
             messages.
    """
    try:
        entries = [
            {
                "Id": str(ind),
                "MessageBody": msg["body"],
                "MessageAttributes": msg["attributes"],
                "DelaySeconds": DelaySeconds,
            }
            for ind, msg in enumerate(messages)
        ]
        response = _SQS_CLIENT.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries,
        )
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                print(
                    f"Message sent to the queue {_SQS_QUEUE_URL}, MessageId: {msg_meta['MessageId']}"
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                print(
                    f"Failed to send messages to queue: {_SQS_QUEUE_URL}, "
                    f"attributes {messages[int(msg_meta['Id'])]['attributes']}"
                )
    except ClientError as error:
        print(f"Send messages failed to queue: {_SQS_QUEUE_URL}")
        raise error
    else:
        return response


def receive_messages(queue_url, max_number, visibility_time=1, wait_time=1):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue_url: SQS Queue url
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param visibility_time: The maximum time for message to temporarily invisible to other receivers.
                            This gives the initial receiver a chance to process the message. If the receiver
                            successfully processes and deletes the message within the visibility timeout,
                            the message is removed from the queue.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        response = _SQS_CLIENT.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["SentTimestamp", "ApproximateReceiveCount"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=visibility_time,
            WaitTimeSeconds=wait_time,
        )
        if "Messages" in response.keys():
            messages = response["Messages"]
        elif response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"No more messages available in queue: {_SQS_QUEUE_URL}")
            return []

        for msg in messages:
            print(
                f"Received message ID: {msg['MessageId']}, Attributes: {msg['MessageAttributes']}"
            )
    except Exception as error:
        print(
            f"Couldn't receive messages from queue: {_SQS_QUEUE_URL} Error: {error}"
        )
        raise error
    else:
        return messages


def delete_messages(queue_url, message_receipt_handles):
    """
    Delete a batch of messages from a queue in a single request.

    :param queue_url: SQS Queue url
    :param message_receipt_handles: The list of messages handles to delete.
    :return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    try:
        entries = [
            {"Id": str(ind), "ReceiptHandle": receipt_handle}
            for ind, receipt_handle in enumerate(message_receipt_handles)
        ]
        response = _SQS_CLIENT.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if "Successful" in response:
            for msg_meta in response["Successful"]:
                print(
                    f"Deleted {message_receipt_handles[int(msg_meta['Id'])]}"
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                print(
                    f"Could not delete {message_receipt_handles[int(msg_meta['Id'])]}"
                )
    except ClientError:
        print(f"Couldn't delete message from queue {_SQS_QUEUE_URL}")
    else:
        return response
