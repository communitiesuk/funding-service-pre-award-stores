import random

import pytest
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.models.flags.enums import FlagType
from db.queries.flags.queries import create_flag_for_application
from tests._expected_responses import APPLICATION_METADATA_RESPONSE
from tests._expected_responses import ASSESSMENTS_STATS_RESPONSE
from tests._helpers import get_rows_by_filters
from tests.conftest import test_input_data

from ._expected_responses import subcriteria_themes_and_expected_response

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"


@pytest.mark.apps_to_insert(test_input_data)
def test_get_assessments_stats(client, seed_application_records):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    # Get test applications
    applications = client.get(
        f"/application_overviews/{fund_id}/{round_id}"
    ).json

    # Add a QA_COMPLETED flag for the first application
    # so that one result from the set is flagged as QA_COMPLETED
    create_flag_for_application(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[0]["application_id"],
        user_id="abc",
        flag_type=FlagType.QA_COMPLETED,
    )

    response_json = client.get(
        f"/assessments/get-stats/{fund_id}/{round_id}"
    ).json

    assert response_json == ASSESSMENTS_STATS_RESPONSE

    # Test number of QA_COMPLETE Applications is correct
    # Add one more QA_COMPLETE flag to another application
    # and also FLAGGED so we can see that the most recent
    # flag does not interfere
    # "qa_completed" should return 2

    create_flag_for_application(
        justification="QA Complete Test 1",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        flag_type=FlagType.QA_COMPLETED,
    )

    create_flag_for_application(
        justification="QA Complete Test 1",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        flag_type=FlagType.FLAGGED,
    )

    response_json = client.get(
        f"/assessments/get-stats/{fund_id}/{round_id}"
    ).json

    assert response_json["qa_completed"] == 2


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
def test_gets_all_apps_for_fund_round(
    request, client, seed_application_records
):
    """test_gets_all_apps_for_fund_round Tests that the number of rows returned
    by filtering by round on `assessment_records` matches the number of
    applications per round specified by the test data generation process."""

    picked_row = seed_application_records[0]

    apps_per_round = 4

    random_round_id = picked_row["round_id"]
    random_fund_id = picked_row["fund_id"]
    application_id = picked_row["application_id"]

    response_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round

    # Check application overview returns flags in order of descending
    create_flag_for_application(
        justification="Test 1",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.FLAGGED,
    )

    create_flag_for_application(
        justification="Test 2",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.RESOLVED,
    )

    create_flag_for_application(
        justification="Test 3",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.STOPPED,
    )

    response_with_flag_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    application_to_check = None
    for application in response_with_flag_json:

        if application["application_id"] == application_id:
            application_to_check = application

    # Check that the last flag in the flag array is the latest flag added
    assert application_to_check["flags"][-1]["flag_type"] == "STOPPED"
    assert application_to_check["flags"][-1]["justification"] == "Test 3"


@pytest.mark.parametrize(
    "url, filter",
    [
        (
            "{fund_id}/{round_id}?search_term={short_id}",
            lambda row: AssessmentRecord.short_id == row["short_id"],
        ),
        (
            "{fund_id}/{round_id}?search_term={project_name}",
            lambda row: AssessmentRecord.project_name == row["project_name"],
        ),
        (
            "{fund_id}/{round_id}?asset_type={asset_type}",
            lambda row: AssessmentRecord.asset_type == row["asset_type"],
        ),
        (
            "{fund_id}/{round_id}?status=NOT_STARTED",
            lambda row: AssessmentRecord.workflow_status == "NOT_STARTED",
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_search(url, filter, client, seed_application_records):

    application = seed_application_records[0]

    filters = [filter(application)]

    rows = get_rows_by_filters(
        application["fund_id"], application["round_id"], filters
    )

    response_json = client.get(
        "/application_overviews/" + url.format(**application)
    ).json

    assert len(response_json) == len(rows)


@pytest.mark.skip(reason="used for tdd only")
def test_get_application_metadata_for_application_id(client):
    response_json = client.get(
        "/application_overviews/a3ec41db-3eac-4220-90db-c92dea049c00"
    ).json

    assert response_json == APPLICATION_METADATA_RESPONSE


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria(client, seed_application_records):
    """Test to check that sub criteria metadata and ordered themes are returned for
    a COFR2W2 sub criteria"""

    sub_criteria_id = "benefits"
    application_id = seed_application_records[0]["application_id"]
    response_json = client.get(
        f"/sub_criteria_overview/{application_id}/{sub_criteria_id}"
    ).json
    # The order of themes within a sub_criteria is important,
    # ensure it is preserved
    expected_theme_order = ["community_use", "risk_loss_impact"]
    actual_theme_order = []
    for theme in response_json["themes"]:
        actual_theme_order.append(theme["id"])
    assert expected_theme_order == actual_theme_order
    assert "short_id" in response_json
    assert "id" in response_json


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_metadata_for_false_sub_criteria_id(
    client, seed_application_records
):
    """Test to check that sub criteria metadata is
    not retuned for false sub criteria"""

    sub_criteria_id = "does-not-exist"
    application_id = seed_application_records[0]["application_id"]
    response = client.get(
        f"/sub_criteria_overview/{application_id}/{sub_criteria_id}"
    ).json

    assert response["status"] == 404
    assert response["title"] == "Not Found"
    assert response["detail"] == "sub_criteria: 'does-not-exist' not found."


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_theme_answers_field_id(
    request, client, seed_application_records
):
    """Test to check field_id with given application_id and
    theme_id"""

    theme_id = "feasibility"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert response.json[0]["field_id"] == "ieRCkI"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_update_ar_status_to_completed(
    request, client, seed_application_records
):
    """Test checks that the status code returned by the POST request is 204,
    which indicates that the request was successful and
    that the application status was updated to COMPLETED."""

    application_id = seed_application_records[0]["application_id"]
    response = client.post(f"/application/{application_id}/status/complete")

    assert response.status_code == 204


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_add_another_presentation_type(
    request, client, seed_application_records
):
    """Test to check presentation_types for add_another component
    with given application_id and theme_id"""

    theme_id = "funding_requested"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert response.status_code == 200
    assert response.json[0]["presentation_type"] == "grouped_fields"
    assert response.json[1]["presentation_type"] == "heading"
    assert response.json[2]["presentation_type"] == "description"
    assert response.json[3]["presentation_type"] == "amount"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_incorrect_theme_id(request, client, seed_application_records):
    """Test to check incorrect theme_id that is expected
    to return custom error along with the openapi validation
    error."""

    theme_id = "incorrect-theme-id"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert "Incorrect theme id" in response.json["detail"]


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_random_theme_content(seed_application_records):
    """Test the function with random theme id that maps
    the application & subcriteria theme and
    returns subcriteria_theme with an answer from
    application
    """
    application_id = seed_application_records[0]["application_id"]
    theme_id, expected_response = random.choice(
        list(subcriteria_themes_and_expected_response.items())
    )
    result = map_application_with_sub_criteria_themes(
        application_id,
        theme_id,
        COF_FUND_ID,
        COF_ROUND_2_W3_ID,
    )

    assert result[0]["answer"] == expected_response


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_convert_boolean_values(seed_application_records):
    """Test the function that convert boolean values to
    "Yes" and "No".
    Args: application_id, theme_id.
    """

    theme_id = "local-support"
    application_id = seed_application_records[0]["application_id"]

    results = map_application_with_sub_criteria_themes(
        application_id,
        theme_id,
        COF_FUND_ID,
        COF_ROUND_2_W3_ID,
    )

    assert [
        value["answer"] for value in results if value["field_id"] == "KqoaJL"
    ][0] == "No"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_application_json(client, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    response = client.get(f"/application/{application_id}/json")
    assert 200 == response.status_code

    json_blob = response.json
    assert application_id == json_blob["application_id"]
