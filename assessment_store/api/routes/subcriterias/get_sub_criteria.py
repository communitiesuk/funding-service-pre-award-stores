from config import Config
from api.models.sub_criteria import SubCriteria
from flask import current_app, abort

def get_all_subcriteria():
    sub_criterias = []
    for section in (
        Config.COF_R2W2_ASSESSMENT_MAPPING["scored_criteria"]
        + Config.COF_R2W2_ASSESSMENT_MAPPING["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            sub_criterias.append(sub_criteria)
    return sub_criterias

def get_matching_sub_criteria(sub_criteria_id):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    sub_criterias = get_all_subcriteria()
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        return matching_sub_criteria[0]
    elif len(matching_sub_criteria) > 1:
        msg="sub_criteria: '{sub_criteria_id}' duplicated."
        current_app.logger.error(msg)
        raise ValueError(msg)
    else:
        msg = f"sub_criteria: '{sub_criteria_id}' not found."
        current_app.logger.warn(msg)
        abort(404, description=msg)


def return_subcriteria_from_config(sub_criteria_id):
    sub_criteria = get_matching_sub_criteria(sub_criteria_id)
    # TODO get actual score submitted status when score table available
    score_submitted = False

    return SubCriteria.from_filtered_dict(
        {"score_submitted": score_submitted, **sub_criteria}
    )
