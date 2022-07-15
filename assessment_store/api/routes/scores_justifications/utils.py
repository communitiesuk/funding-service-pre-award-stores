from typing import Dict

import requests
from config import Config


def calc_weights(
    fund_id: str,
    crit_id: str,
    list_of_scores: Dict[str, float],
    round_id: str,
    crit_name: str,
):
    """
    Takes a list of sub criteria and a round id
    """
    # dict_of_subcriteria = { "sub_crit_id" : score }
    # Use the round_id to "download"
    # the weights (look at the round store in the RIP)

    url = Config.ROUND_ENDPOINT.format(
        host=Config.LIVE_TEST_FUND_STORE_API_HOST,
        fund_id=fund_id,
        round_id=round_id,
    )

    r = requests.get(url)

    json = r.json()

    weights = json.get("assessment_criteria_weighting")

    total_score = sum(list_of_scores)

    weighted_score = total_score * weights[crit_name]

    return {"total_score": total_score, "weighted_score": weighted_score}
