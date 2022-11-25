# flake8: noqa
from typing import Dict
from typing import List

from config.mappings.assessment_mapping_fund_round import (
    fund_round_to_assessment_mapping,
)
from db.queries.assessment_records import get_metadata_for_fund_round_id
from db.queries.assessment_records.queries import find_assessment


def all_assessments_for_fund_round_id(
    fund_id: str, round_id: str
) -> List[Dict]:
    """all_assessments_for_fund_round_id Function used by the endpoint
    `/application_overviews/{fund_id}/{round_id}`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """

    app_list = get_metadata_for_fund_round_id(
        fund_id=fund_id, round_id=round_id
    )

    return app_list


def get_assessment_for_application_id(application_id: str) -> dict:
    """get_assessment Function used by the endpoint
    `/application_overviews/{application_id}`.

    :param application_id: The stringified application UUID.
    :return: A dictionary.
    """

    assessment_record = find_assessment(application_id)

    return assessment_record


def config_for_fund_round_id(fund_id: str, round_id: str) -> dict:
    """config_for_fund_round_id Function used by the endpoint
    `/config/{fund_id}/{round_id}`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A dictionary.
    """

    return fund_round_to_assessment_mapping[f"{fund_id}:{round_id}"]
