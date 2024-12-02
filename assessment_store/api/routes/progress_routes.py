import copy
from typing import List

from flask import request

from config import Config
from db.queries.progress.queries import get_progress_for_app


def post_progress_for_applications(fund_id, round_id) -> List[dict]:
    application_ids = request.get_json()["application_ids"]
    return get_progress_for_applications(application_ids, fund_id, round_id)


def get_progress_for_applications(application_ids: List[str], fund_id, round_id) -> List[dict]:
    scored_criteria = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])["scored_criteria"]
    scored_sub_crit_list = [
        subcrit["id"] for crit in scored_criteria for subcrit in crit["sub_criteria"] if subcrit["id"] != "themes"
    ]
    app_prog_list = get_progress_for_app(application_ids)
    for app in app_prog_list:
        app["progress"] = int(100 * app["scored_sub_criterias"] / len(scored_sub_crit_list))

    return app_prog_list
