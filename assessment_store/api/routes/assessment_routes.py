# flake8: noqa
from typing import Dict
from typing import List

from db.queries.assessment_records import get_metadata_for_fund_round_id
from db.schemas import AssessmentRecordMetadata


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
        fund_id=fund_id, round_id=round_id, search_term="COF-R2W2-HJPTUS"
    )

    return app_list
