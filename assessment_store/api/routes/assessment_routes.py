# flake8: noqa
from typing import Dict
from typing import List

from api.models.sub_criteria import SubCriteria
from api.routes._helpers import transform_to_assessor_task_list_metadata
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from api.routes.subcriterias.get_sub_criteria import (
    return_subcriteria_from_mapping,
)
from db.queries import get_metadata_for_fund_round_id
from db.queries.assessment_records.queries import find_assessor_task_list_state
from db.queries.assessment_records.queries import (
    get_assessment_sub_critera_state,
)
from db.queries.comments.queries import get_sub_criteria_to_has_comment_map
from db.queries.scores.queries import get_sub_criteria_to_latest_score_map
from flask import current_app


def all_assessments_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "ALL",
    status: str = "ALL",
) -> List[Dict]:
    """all_assessments_for_fund_round_id Function used by the endpoint
    `/application_overviews/{fund_id}/{round_id}`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """

    app_list = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
    )
    return app_list


def sub_criteria(
    application_id: str,
    sub_criteria_id: str,
) -> Dict:
    """Returns metadata and themes for a sub_criteria
    `/sub_criteria_overview/{sub_criteria_id}`.

    :param sub_criteria_id: The stringified sub criteria id (NOT sub critria name).
    :return: A sub criteria dictionary.
    """
    current_app.logger.info(
        "Processing request for sub criteria: {sub_criteria_id}."
    )
    current_app.logger.info(
        "Searching asessment mapping for sub criteria: {sub_criteria_id}."
    )
    sub_criteria_config_from_mapping = return_subcriteria_from_mapping(
        sub_criteria_id
    )
    current_app.logger.info(
        "Getting application subcriteria metadata for application: {sub_criteria_id}."
    )
    application_metadata_for_subcriteria = get_assessment_sub_critera_state(
        application_id
    )
    sub_criteria = SubCriteria.from_filtered_dict(
        {
            **sub_criteria_config_from_mapping,
            **application_metadata_for_subcriteria,
        }
    )
    sub_criteria_dict = sub_criteria.to_dict()
    return sub_criteria_dict


def get_banner_state(application_id: str) -> dict:
    return get_assessment_sub_critera_state(application_id)


def get_assessor_task_list_state(application_id: str) -> dict:
    """get_assessor_task_list_state Function used by the endpoint
    `/assessor_task_list/{application_id}`.

    :param application_id: The stringified application UUID.
    :return: A dictionary.
    """

    metadata = find_assessor_task_list_state(application_id)
    score_map = get_sub_criteria_to_latest_score_map(application_id)
    comment_map = get_sub_criteria_to_has_comment_map(application_id)
    sections, criterias = transform_to_assessor_task_list_metadata(
        metadata["fund_id"], metadata["round_id"], score_map, comment_map
    )

    # we don't need to return round_id as it's not relevant to the frontend
    # (same with fund_id, but we're using that at the moment for fund_name)
    metadata = {k: v for k, v in metadata.items() if k not in ["round_id"]}

    metadata["sections"] = sections
    metadata["criterias"] = criterias

    return metadata


def get_sub_criteria_theme_answers(application_id: str, theme_id: str):
    """Function returns mapped answers from application & Sub_criteria_themes
    with given application_id and theme_id"""

    return map_application_with_sub_criteria_themes(application_id, theme_id)
