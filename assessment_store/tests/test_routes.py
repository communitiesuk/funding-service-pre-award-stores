from db.models.assessment_record.assessment_records import AssessmentRecord
from tests._helpers import get_random_row


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
        f"""/application_overviews/{random_fund_id}/{random_round_id}
        ?search_term=COF-R2W2-HGBNFM"""
    ).json

    assert len(response_json) == apps_per_round
