from db.models.assessment_record.assessment_records import AssessmentRecord
from sqlalchemy import cast
from sqlalchemy import TEXT
from tests._helpers import get_random_row
from tests._helpers import get_rows_by_filters


def test_gets_all_apps_for_fund_round(request, client):
    """test_gets_all_apps_for_fund_round Tests that the number of rows returned
    by filtering by round on `assessment_records` matches the number of
    applications per round specified by the test data generation process."""

    picked_row = get_random_row(AssessmentRecord)

    current_run_is_random = request.config.getoption("randomdata")

    if current_run_is_random:
        apps_per_round = request.config.getoption("apps_per_round")
    else:
        # If you regenerate the deterministic test data you will have to change
        # this to the value you used.
        apps_per_round = 100

    random_round_id = picked_row.round_id

    random_fund_id = picked_row.fund_id

    response_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round


def test_search_by_short_id(client):
    picked_row = get_random_row(AssessmentRecord)

    response_json = client.get(
        f"""/application_overviews/{picked_row.fund_id}/{picked_row.round_id}
        ?search_term={picked_row.short_id}"""
    ).json

    assert len(response_json) == 1


def test_search_by_assest_type(client):
    picked_row = get_random_row(AssessmentRecord)
    filters = {AssessmentRecord.asset_type == picked_row.asset_type}

    rows = get_rows_by_filters(
        picked_row.fund_id, picked_row.round_id, filters
    )

    response_json = client.get(
        f"""/application_overviews/{picked_row.fund_id}/{picked_row.round_id}
        ?asset_type={picked_row.asset_type}"""
    ).json

    assert len(response_json) == len(rows)


def test_search_by_status(client):
    picked_row = get_random_row(AssessmentRecord)
    filters = {
        cast(AssessmentRecord.workflow_status, TEXT).like(
            f"%{picked_row.workflow_status}%"
        )
    }

    rows = get_rows_by_filters(
        picked_row.fund_id, picked_row.round_id, filters
    )

    response_json = client.get(
        f"""/application_overviews/{picked_row.fund_id}/{picked_row.round_id}
        ?status={picked_row.workflow_status}"""
    ).json

    assert len(response_json) == len(rows)
