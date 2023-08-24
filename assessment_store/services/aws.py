import sys
from datetime import datetime
from os import getenv
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

_SQS_CLIENT = boto3.client(
    "sqs",
    region_name=getenv("AWS_REGION", None),
    endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
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


def submit_message(messages, DelaySeconds=1):
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
        QueueUrl=_SQS_QUEUE_URL,
        Entries=entries,
    )
    print(response)
    return response


def receive_messages(max_number, visibility_time=1, wait_time=1):
    """
    Receive a batch of messages in a single request from an SQS queue.

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
            QueueUrl=_SQS_QUEUE_URL,
            AttributeNames=["SentTimestamp"],
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            VisibilityTimeout=visibility_time,
            WaitTimeSeconds=wait_time,
        )
        if "Messages" in response.keys():
            messages = response["Messages"]
        elif response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"No more messages available in queue: {_SQS_QUEUE_URL}")
            return None

        for msg in messages:
            print(
                f"Received message: {msg['MessageId']}, {msg['Body']}"
            )  # msg["MessageAttributes"]
    except ClientError as error:
        print(f"Couldn't receive messages from queue: {_SQS_QUEUE_URL}")
        raise error
    else:
        return messages


def delete_messages(message_receipt_handles):
    """
    Delete a batch of messages from a queue in a single request.

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
            QueueUrl=_SQS_QUEUE_URL, Entries=entries
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


# TODO: Below function is for testing purpose, delete it later
def create_dummy_messages(DelaySeconds, batch_size):
    # Create a dummy application_json list
    from tests._helpers import row_data

    application_json_list = row_data(
        4,
        1,
        1,
        {
            "NSTFR2": {
                "fund_id": "13b95669-ed98-4840-8652-d6b7a19964db",
                "round_id": "fc7aa604-989e-4364-98a7-d1234271435a",
                "type_of_application": "NSTF",
            }
        },
    )

    # Submit the message
    count = 0
    print(
        f"Sending file application_json_list in batches of {batch_size} as messages."
    )
    while count < len(application_json_list):
        messages = [
            pack_message(application_json_list[index])
            for index in range(
                count, min(count + batch_size, len(application_json_list))
            )
        ]
        count = count + batch_size
        submit_message(messages, DelaySeconds)
        print(".", end="")
        sys.stdout.flush()
    print(f"Done. Sent {len(application_json_list)} messages.")

    return application_json_list


# TODO: Below function is for testing purpose, delete it later
def usage_demo(batch_size, DelaySeconds, visibility_time, wait_time):
    print("-" * 88)
    print("Welcome to the Amazon Simple Queue Service (Amazon SQS) demo!")
    print("-" * 88)

    received_applications = []

    # Create a dummy application_json list
    application_json_list = create_dummy_messages(DelaySeconds)

    # Recieve & delete the message
    print(
        f"Receiving, handling, and deleting messages in batches of {batch_size}."
    )
    more_messages = True
    while more_messages:
        received_messages = receive_messages(
            batch_size, visibility_time, wait_time
        )
        print(".", end="")
        sys.stdout.flush()
        message_receipt_handles = []
        if received_messages:
            for message in received_messages:
                id, body, datetime_str = unpack_message(message)
                received_applications.append(body)
                message_receipt_handles.append(message["ReceiptHandle"])
            delete_messages(message_receipt_handles)
        else:
            more_messages = False
    print("Done.")

    if all(
        [
            application_json_list[index] == received_applications[index]
            for index in range(len(application_json_list))
        ]
    ):
        print("Successfully reassembled all application id list!")
    else:
        print("Uh oh, some application id's were missed!")

    print("Thanks for watching!")
    print("-" * 88)


if __name__ == "__main__":
    # Queue Settings
    DelaySeconds = 0
    visibility_time = 0
    wait_time = 0
    batch_size = 2

    # usage_demo(batch_size, DelaySeconds, visibility_time, wait_time)
    create_dummy_messages(DelaySeconds, batch_size)
