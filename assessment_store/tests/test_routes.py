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
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round


def test_search_by_short_id(client):
    round_id = "a950b75c-769f-41c7-9615-a6275d2f7c82"
    fund_id = "fd3abd75-6803-4a08-b098-e92263998373"

    response_json = client.get(
        f"""/application_overviews/{fund_id}/{round_id}
        ?search_term=COF-R2W2-HJPTUS"""
    ).json

    assert len(response_json) == 1


def test_search_by_assest_type(client):
    round_id = "a950b75c-769f-41c7-9615-a6275d2f7c82"
    fund_id = "fd3abd75-6803-4a08-b098-e92263998373"

    response_json = client.get(
        f"/application_overviews/{fund_id}/{round_id}?search_term=COF-R2W2-HJ"
    ).json

    assert len(response_json) == 1


def test_search_by_status(client):
    round_id = "a950b75c-769f-41c7-9615-a6275d2f7c82"
    fund_id = "fd3abd75-6803-4a08-b098-e92263998373"

    response_json = client.get(
        f"/application_overviews/{fund_id}/{round_id}?status=NOT_STARTED"
    ).json

    assert len(response_json) == 1
