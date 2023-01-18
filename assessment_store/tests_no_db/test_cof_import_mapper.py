import json

from db.queries.assessment_records._helpers import derive_application_values


def test_derive_cof_values():
    single_application_json = "tests_no_db/test_data/single_application.json"

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"
    assert (
        "funding-service-design" == derived_fields["fund_id"]
    ), "Wrong Fund ID"
    assert "summer" == derived_fields["round_id"], "Wrong Round ID"
    assert (
        "test-application-id" == derived_fields["application_id"]
    ), "Wrong Application ID"
    assert (
        "Project name" == derived_fields["project_name"]
    ), "Wrong Project Name"
    assert (
        "community-centre" == derived_fields["asset_type"]
    ), "Wrong Asset Type"

    # Assert postcode & country extracted
