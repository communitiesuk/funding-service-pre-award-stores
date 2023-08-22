import logging
import sys
from datetime import datetime
from os import getenv
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger("SQS_Recieve")
logger.setLevel(logging.DEBUG)

_SQS_CLIENT = boto3.client(
    "sqs",
    region_name=getenv("AWS_REGION", "eu-west-2"),
    endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", "http://localhost:4566"),
)
_SQS_QUEUE_URL = _SQS_CLIENT.get_queue_url(
    QueueName=getenv("AWS_SQS_QUEUE_NAME", "fsd-queue"),
)["QueueUrl"]


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


# implement submit_message in applicatiopn-store
def submit_message(message):
    response = _SQS_CLIENT.send_message(
        QueueUrl=_SQS_QUEUE_URL,
        MessageBody=message["body"],
        DelaySeconds=123,
        MessageAttributes=message["attributes"],
    )
    print(response)


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
        if "Messages" in response.keys():
            messages = response["Messages"]
        elif response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.exception(
                "No messages available in queue: %s", _SQS_QUEUE_URL
            )
            return None

        for msg in messages:
            logger.info(
                "Received message: %s: %s", msg["MessageId"], msg["Body"]
            )  # msg["MessageAttributes"]
    except ClientError as error:
        logger.exception(
            "Couldn't receive messages from queue: %s", _SQS_QUEUE_URL
        )
        raise error
    else:
        return messages[0]


def delete_messages(messages):
    """
    Delete a batch of messages from a queue in a single request.

    :param queue: The queue from which to delete the messages.
    :param messages: The list of messages to delete.
    :return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    try:
        response = _SQS_CLIENT.delete_message(
            QueueUrl=_SQS_QUEUE_URL, ReceiptHandle=messages["ReceiptHandle"]
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(
                "Deleted %s: %s",
                messages["MessageId"],
                messages["ReceiptHandle"],
            )
        else:
            logger.warning(
                "Could not delete %s: %s",
                messages["MessageId"],
                messages["ReceiptHandle"],
            )
    except ClientError:
        logger.exception(
            "Couldn't delete messages from queue %s", _SQS_QUEUE_URL
        )
    else:
        return response


def usage_demo():
    """
    Shows how to:
    * Read the lines from this Python file and send the lines in
      batches of 10 as messages to a queue.
    * Receive the messages in batches until the queue is empty.
    * Reassemble the lines of the file and verify they match the original file.
    """

    print("-" * 88)
    print("Welcome to the Amazon Simple Queue Service (Amazon SQS) demo!")
    print("-" * 88)

    # Create a dummy application_id_list
    application_id_list = [str(uuid4()) for _ in range(0, 4)]

    # Submit the message
    count = 0
    batch_size = 1
    received_applications = []
    print(
        f"Sending file application_id_list in batches of {batch_size} as messages."
    )
    while count < len(application_id_list):
        messages = [
            pack_message(application_id_list[index])
            for index in range(
                count, min(count + batch_size, len(application_id_list))
            )
        ]
        count = count + batch_size
        submit_message(messages[0])
        print(".", end="")
        sys.stdout.flush()
    print(f"Done. Sent {len(application_id_list) - 1} messages.")

    # Recieve & delete the message
    print(
        f"Receiving, handling, and deleting messages in batches of {batch_size}."
    )
    more_messages = True
    while more_messages:
        received_message = receive_messages(batch_size, 2)
        print(".", end="")
        sys.stdout.flush()
        if received_message:
            id, body, datetime_str = unpack_message(received_message)
            received_applications.append(body)
            delete_messages(received_message)
        else:
            more_messages = False
    print("Done.")

    if all(
        [
            application_id_list[index] == received_applications[index]
            for index in range(len(application_id_list))
        ]
    ):
        print("Successfully reassembled all application id list!")
    else:
        print("Uh oh, some application id's were missed!")

    # queue.delete()

    print("Thanks for watching!")
    print("-" * 88)


if __name__ == "__main__":
    usage_demo()
