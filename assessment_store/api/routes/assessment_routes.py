# flake8: noqa
from typing import Dict
from typing import List
from api.routes.subcriterias.get_sub_criteria import (
    return_subcriteria_from_config,
)
from db.queries.assessment_records import get_metadata_for_fund_round_id
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
    sub_criteria_id: str,
) -> Dict:
    """Returns metadata and themes for a sub_criteria
    `/sub_criteria_overview/{sub_criteria_id}`.

    :param sub_criteria_id: The stringified sub criteria id (NOT sub critria name).
    :return: A sub criteria dictionary.
    """
    current_app.logger.info("Processing request for sub criteria: {sub_criteria_id}.")
    sub_criteria = return_subcriteria_from_config(sub_criteria_id)
    sub_criteria_dict = sub_criteria.to_dict()
    return sub_criteria_dict
