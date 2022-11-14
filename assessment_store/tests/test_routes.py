from db.models.assessment_record.assessment_records import AssessmentRecords
from tests.helpers import get_random_row


def test_gets_all_apps_for_fund_round(request, client):

    picked_row = get_random_row(AssessmentRecords)

    apps_per_round = request.config.getoption("apps_per_round")

    random_round_id = picked_row.round_id

    random_fund_id = picked_row.fund_id

    response_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round
