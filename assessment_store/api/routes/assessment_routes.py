# flake8: noqa
from typing import Dict
from typing import List

from config.mappings.assessment_mapping_fund_round import (
    transform_to_assessor_task_list_metadata,
)
from db.queries.assessment_records import get_metadata_for_fund_round_id
from db.queries.assessment_records.queries import find_assessor_task_list_state


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


def get_assessor_task_list_state(application_id: str) -> dict:
    """get_assessor_task_list_state Function used by the endpoint
    `/assessor_task_list/{application_id}`.

    :param application_id: The stringified application UUID.
    :return: A dictionary.
    """

    metadata = find_assessor_task_list_state(application_id)
    sections, criterias = transform_to_assessor_task_list_metadata(
        metadata["fund_id"], metadata["round_id"]
    )

    # We don't need to return this state.  It's only used to get the config above.
    del metadata["round_id"]

    # this... should be deleted? needed at the moment to populate fund name on the ui.
    # del metadata["fund_id"]

    metadata["sections"] = sections
    metadata["criterias"] = criterias

    return metadata
