from os import getenv

from config import Config
from fsd_utils.services.aws import SQSClient


if (
    getenv("PRIMARY_QUEUE_URL", "Primary Queue URL Not Set")
    == "Primary Queue URL Not Set"
):
    _SQS_CLIENT = SQSClient(
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION,
        endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
    )
else:
    _SQS_CLIENT = SQSClient(
        region_name=Config.AWS_REGION,
        endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
    )
