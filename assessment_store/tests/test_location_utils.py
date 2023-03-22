import csv
import json
import os

from scripts.location_utils import extract_location_data
from scripts.location_utils import get_all_location_data
from scripts.location_utils import get_application_form
from scripts.location_utils import get_postcode_from_questions
from scripts.location_utils import write_locations_to_csv


def test_get_application_form():

    single_application_json = (
        "tests/test_data/single_application_jsonb_blob.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)

    result = get_application_form(loaded_test_json)
    assert 45 == len(result), "unexpected number of questions"


def test_get_postcode_from_questions():
    expected = "QQ127QQ"

    test_json_file = "tests/test_data/questions_from_single_application.json"

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    result = get_postcode_from_questions(loaded_test_json)
    assert expected == result, "wrong postcode returned"


def test_extract_location_data_success():
    postcode = "PL13RE"

    test_json_file = "tests/test_data/postcodes_io_response.json"

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    item_under_test = loaded_test_json["result"][1]
    assert postcode == item_under_test["query"]

    result = extract_location_data(item_under_test)
    assert result[postcode]
    assert result[postcode]["error"] is False
    assert result[postcode]["country"] == "England"
    assert result[postcode]["constituency"] == "Plymouth, Sutton and Devonport"
    assert result[postcode]["region"] == "South West"
    assert result[postcode]["county"] == "Plymouth"


def test_extract_location_data_error():
    postcode = "QQ127QQ"

    test_json_file = "tests/test_data/postcodes_io_response.json"

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    item_under_test = loaded_test_json["result"][3]
    assert postcode == item_under_test["query"]

    result = extract_location_data(item_under_test)
    assert result[postcode]
    assert result[postcode]["error"] is True


def test_get_all_location_data():
    just_postcodes = ["NP203EB", "PL13RE", "QQ123QQ"]
    result = get_all_location_data(just_postcodes)
    assert 3 == len(result)
    assert result[just_postcodes[0]]
    assert result[just_postcodes[0]]["error"] is False
    assert "Wales" == result[just_postcodes[0]]["country"]
    assert result[just_postcodes[1]]
    assert result[just_postcodes[1]]["error"] is False
    assert "England" == result[just_postcodes[1]]["country"]
    assert result[just_postcodes[2]]
    assert result[just_postcodes[2]]["error"]


def test_write_csv_file():

    location = {
        "error": False,
        "county": "test_county",
        "country": "test_country",
        "constituency": "test_constituency",
        "region": "test_region",
        "postcode": "QQ121EE",
    }

    application_ids_to_postcodes = {("111122223333", "abc123"): "QQ121EE"}

    postcodes_to_location_data = {"QQ121EE": location}

    target_file = (
        os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/test_csv.csv"
    )
    write_locations_to_csv(
        application_ids_to_postcodes, postcodes_to_location_data, target_file
    )
    print("CSV file written to" + target_file)

    with open(target_file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assert location["postcode"] == row["postcode"]
            assert "abc123" == row["application_id"]
