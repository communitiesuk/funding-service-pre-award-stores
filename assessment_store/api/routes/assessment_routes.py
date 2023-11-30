# flake8: noqa
from typing import Dict
from typing import List

from api.models.sub_criteria import SubCriteria
from api.routes._helpers import transform_to_assessor_task_list_metadata
from api.routes.subcriterias.get_sub_criteria import (
    get_all_uploaded_document_field_answers,
)
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes_fields,
)
from api.routes.subcriterias.get_sub_criteria import (
    return_subcriteria_from_mapping,
)
from config.mappings.assessment_mapping_fund_round import (
    applicant_info_mapping,
)
from db.models.flags.flag_update import FlagStatus
from db.queries import get_metadata_for_fund_round_id
from db.queries.assessment_records.queries import find_assessor_task_list_state
from db.queries.assessment_records.queries import get_application_jsonb_blob
from db.queries.assessment_records.queries import get_assessment_export_data
from db.queries.assessment_records.queries import (
    get_assessment_sub_critera_state,
)
from db.queries.assessment_records.queries import get_metadata_for_application
from db.queries.assessment_records.queries import update_status_to_completed
from db.queries.comments.queries import get_sub_criteria_to_has_comment_map
from db.queries.qa_complete.queries import (
    get_qa_complete_record_for_application,
)
from db.queries.scores.queries import get_sub_criteria_to_latest_score_map
from flask import current_app


def assessment_metadata_for_application_id(application_id: str) -> Dict:
    return get_metadata_for_application(application_id)


def _fix_country(country):
    country = country.strip().casefold()
    if country == "northernireland":
        country = "northern ireland"
    return country


def all_assessments_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    funding_type: str = "ALL",
    asset_type: str = "ALL",
    status: str = "ALL",
    search_in: str = "",
    countries: str = "all",
    filter_by_tag: str = "",
    country: str = "ALL",
    region: str = "ALL",
    local_authority: str = "ALL",
    cohort: str = "ALL",
    publish_datasets: str = "ALL",
    datasets: str = "ALL",
    team_in_place: str = "ALL",
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
        countries=[_fix_country(c) for c in countries.split(",") if c],
        search_in=search_in,
        funding_type=funding_type,
        filter_by_tag=filter_by_tag,
        country=country,
        region=region,
        local_authority=local_authority,
        cohort=cohort,
        publish_datasets=publish_datasets,
        datasets=datasets,
        team_in_place=team_in_place,
    )
    return app_list


def sub_criteria(
    application_id: str,
    sub_criteria_id: str,
) -> Dict:
    """Returns metadata and themes for a sub_criteria
    `/sub_criteria_overview/{sub_criteria_id}`.

    :param sub_criteria_id: The stringified sub criteria id (NOT sub
        critria name).
    :return: A sub criteria dictionary.

    """
    current_app.logger.info(
        "Processing request for sub criteria: {sub_criteria_id}."
    )
    metadata = find_assessor_task_list_state(application_id)
    current_app.logger.info(
        "Searching assessment mapping for sub criteria: {sub_criteria_id}."
    )
    sub_criteria_config_from_mapping = return_subcriteria_from_mapping(
        sub_criteria_id, metadata["fund_id"], metadata["round_id"]
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
    qa_complete = get_qa_complete_record_for_application(application_id)

    metadata["sections"] = sections
    metadata["criterias"] = criterias
    metadata["qa_complete"] = qa_complete

    return metadata


def get_sub_criteria_theme_answers(application_id: str, theme_id: str):
    """Function returns mapped answers from application & Sub_criteria_themes with
    given application_id and theme_id."""
    metadata = find_assessor_task_list_state(application_id)
    return map_application_with_sub_criteria_themes(
        application_id, theme_id, metadata["fund_id"], metadata["round_id"]
    )


def get_all_uploaded_document_theme_answers(application_id: str):
    metadata = find_assessor_task_list_state(application_id)
    field_answers = get_all_uploaded_document_field_answers(
        metadata["fund_id"], metadata["round_id"]
    )
    return map_application_with_sub_criteria_themes_fields(
        application_id, "all_uploaded_documents", field_answers
    )


def update_ar_status_to_completed(application_id: str):
    """Function updates the status to COMPLETE for the given application_id."""
    update_status_to_completed(application_id)


def assessment_stats_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "ALL",
    status: str = "ALL",
    search_in: str = "",
    funding_type: str = "ALL",
    countries: str = "all",
) -> List[Dict]:
    """Function used by the endpoint `/assessments/get-stats/{fund_id}/{round_id}`
    that returns a dictionary of metrics about assessments for a given fund_id and
    round_id.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.

    """

    def determine_display_status(assessment):
        all_latest_status = [
            flag["latest_status"] for flag in assessment["flags"]
        ]
        if FlagStatus.STOPPED in all_latest_status:
            display_status = "STOPPED"
        elif all_latest_status.count(FlagStatus.RAISED) > 1:
            display_status = "MULTIPLE_FLAGS"
        elif all_latest_status.count(FlagStatus.RAISED) == 1:
            display_status = "FLAGGED"
        elif assessment["is_qa_complete"]:
            display_status = "QA_COMPLETED"
        else:
            display_status = assessment["workflow_status"]
        return display_status

    stats = {}
    assessments = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
        search_in=search_in,
        funding_type=funding_type,
        countries=[_fix_country(c) for c in countries.split(",") if c],
    )
    stats.update(
        {
            "completed": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "COMPLETED"
                ]
            ),
            "assessing": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "IN_PROGRESS"
                ]
            ),
            "not_started": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "NOT_STARTED"
                ]
            ),
            "qa_completed": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "QA_COMPLETED"
                ]
            ),
            "stopped": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "STOPPED"
                ]
            ),
            "flagged": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "FLAGGED"
                ]
            ),
            "multiple_flagged": len(
                [
                    1
                    for assessment in assessments
                    if determine_display_status(assessment) == "MULTIPLE_FLAGS"
                ]
            ),
            "total": len(assessments),
        }
    )

    return stats


def get_application_json(application_id):
    return get_application_jsonb_blob(application_id)


def get_application_data_for_export(
    fund_id: str, round_id: str, report_type: str
) -> List[Dict]:
    app_list = get_assessment_export_data(
        fund_id=fund_id,
        round_id=round_id,
        report_type=report_type,
        list_of_fields=applicant_info_mapping[fund_id],
    )

    return app_list
