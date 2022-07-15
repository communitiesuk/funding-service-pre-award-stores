from typing import Dict

import requests
from config import Config


def calc_weights(
    fund_id: str,
    crit_id: str,
    list_of_scores: Dict[str, float],
    round_id: str,
    crit_name: str,
    query_by_name: bool = True,
):
    """
    Takes a list of sub criteria and a round id
    """

    url = Config.ROUND_ENDPOINT.format(
        host=Config.LIVE_TEST_FUND_STORE_API_HOST,
        fund_id=fund_id,
        round_id=round_id,
    )

    r = requests.get(url)

    json = r.json()
    weights = json.get("assessment_criteria_weighting")
    total_score = sum(list_of_scores)

    if query_by_name:
        weight = weights[crit_name]
        weighted_score = total_score * weight
    else:
        weight = weights[crit_id]
        weighted_score = total_score * weight

    return {
        "total_score": total_score,
        "weighted_score": weighted_score,
        "weight": weight,
    }
