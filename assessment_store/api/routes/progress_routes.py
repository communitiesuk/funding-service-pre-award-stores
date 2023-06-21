from typing import List

from config.mappings.cof_mapping_parts.cof_r2_scored_criteria import (
    scored_criteria,
)
from db.queries.progress.queries import get_progress_for_app
from flask import request


def post_progress_for_applications() -> List[dict]:
    application_ids = request.get_json()["application_ids"]
    return get_progress_for_applications(application_ids)


def get_progress_for_applications(application_ids: List[str]) -> List[dict]:

    scored_sub_crit_list = [
        subcrit["id"]
        for crit in scored_criteria
        for subcrit in crit["sub_criteria"]
        if subcrit["id"] != "themes"
    ]
    app_prog_list = get_progress_for_app(application_ids)
    for app in app_prog_list:
        app["progress"] = int(
            100 * app["scored_sub_criterias"] / len(scored_sub_crit_list)
        )

    return app_prog_list
