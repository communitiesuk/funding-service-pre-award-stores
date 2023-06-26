import json

import pytest
from db.queries.assessment_records._helpers import derive_application_values


@pytest.fixture(scope="function")
def mock_data_key_mappings(monkeypatch):
    fund_round_data_key_mappings = {
        "TESTREF": {
            "location": "yEmHpp",
            "asset_type": "yaQoxU",
            "funding_one": "JzWvhj",
            "funding_two": "jLIgoi",
        }
    }
    monkeypatch.setattr(
        "db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    yield


def test_derive_cof_values_no_location(mock_data_key_mappings):
    single_application_json = (
        "tests/test_data/single_application_no_location.json"
    )

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

    assert (
        derived_fields["location_json_blob"]["error"] is True
    ), "wrong error value"
    assert (
        "Not Available" == derived_fields["location_json_blob"]["county"]
    ), "wrong county value"


@pytest.mark.parametrize(
    "postcode,expected_country",
    [
        ("B90 4RF", "England"),
        ("EX22 6TA", "England"),
    ],
)
def test_derive_cof_values_location_present_no_error(
    postcode, expected_country, mock_data_key_mappings
):
    single_application_json = (
        "tests/test_data/single_application_no_location.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
        # set mock location in json
        loaded_test_json["forms"][12]["questions"][2]["fields"][0][
            "answer"
        ] = f"Test Address,null, Test Town Or City,null, {postcode}"

    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"

    assert (
        derived_fields["location_json_blob"]["error"] is False
    ), "wrong error value"
    assert (
        expected_country == derived_fields["location_json_blob"]["country"]
    ), "wrong county value"


def test_derive_cof_values_location_present_with_error():
    single_application_json = (
        "tests/test_data/single_application_no_location.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    loaded_test_json["location_json_blob"] = {"error": True, "county": "error"}
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"

    assert (
        derived_fields["location_json_blob"]["error"] is True
    ), "wrong error value"
    assert (
        "Not Available" == derived_fields["location_json_blob"]["county"]
    ), "wrong county value"
