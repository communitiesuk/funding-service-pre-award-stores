from typing import Dict, List

from db.queries.scores.queries import get_scores_for_app_sub_crit
from config.mappings.mapping_parts.scored_criteria import scored_criteria


def get_progress_for_application(
    application_id: str
) -> Dict:
    """get_progress_for_application Function 
    used by the get endpoint `/progress.
    :param application_id: The stringified application UUID.
    :return: An object containing the progress of the application
    """
    # count how many scored sub_crits there are and populate scored_sub_crit_list
    scored_sub_criteria_count = 0
    scored_sub_crit_list = []
    for crit in scored_criteria:
        scored_sub_criteria_count += len(crit["sub_criteria"])
        for subcrit in crit["sub_criteria"]:
            scored_sub_crit_list.append(subcrit["id"]) 

    # count how many of the application's scored subcrits are scored (get latest score per subcrit)
    scored_sub_crit_list_for_application = []
    for sub_crit in scored_sub_crit_list:
        scored_sub_crit_for_application = get_scores_for_app_sub_crit(application_id, sub_crit)
        scored_sub_crit_list_for_application += scored_sub_crit_for_application

    number_of_scored_sub_crits_for_application = len(scored_sub_crit_list_for_application)

    # calculate percenatage and return the int as the progress value
    progress = int(number_of_scored_sub_crits_for_application/scored_sub_criteria_count*100)    
    return_dict = {
        "application_id": application_id,
        "progress": progress,
        }
    return return_dict


def get_bulk_progress_for_applications(application_ids: List[str]) -> List[Dict]:
    """get_progress_for_application Function 
    used by the get endpoint `/progress.
    :param application_ids: List of stringified applications' UUIDs.
    :return: List of objects containing the progress of the application
    """
    progress_list = []
    for application_id in application_ids:
        progress = get_progress_for_application(application_id)
        progress_list.append(progress)
    return progress_list
