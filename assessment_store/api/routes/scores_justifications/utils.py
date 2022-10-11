import requests
from config import Config


def calc_weighted_scores_for_criteria(
    fund_id: str,
    crit_id: str,
    list_of_scores: list[float],
    round_id: str,
    crit_name: str,
    query_by_name: bool = True,
):
    """
    Takes a list of sub criteria and a round id
    """

    round_json = get_round_json(fund_id, round_id)
    weights = round_json.get("assessment_criteria_weighting")
    total_score = sum(list_of_scores)

    if query_by_name:
        weight = next(
            (item["value"] for item in weights if item["name"] == crit_name),
            None,
        )
    else:
        weight = next(
            (item["value"] for item in weights if item["id"] == crit_id), None
        )

    weighted_score = total_score * weight
    return {
        "total_score": total_score,
        "weighted_score": weighted_score,
        "weight": weight,
    }


def get_round_json(fund_id, round_id):
    url = Config.FUND_STORE_API_HOST + Config.SINGLE_ROUND_ENDPOINT.format(
        fund_id=fund_id,
        round_id=round_id,
    )

    round_store_response = requests.get(url)

    json_obj = round_store_response.json()
    return json_obj
