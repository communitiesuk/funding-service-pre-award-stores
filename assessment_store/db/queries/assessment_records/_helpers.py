import jsonpath_rw_ext
import requests
from config.mappings.assessment_mapping_fund_round import (
    fund_round_data_key_mappings,
)


def get_answer_value(application_json, answer_key):
    return (
        jsonpath_rw_ext.parse(
            f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]"
        )
        .find(application_json)[0]
        .value["answer"]
    )


def get_location_json_from_postcode(raw_postcode):
    """Make a POST request to the postcodes.io API with the provided
    postcode and extract the location data of postcode."""
    result = requests.post(
        url="http://api.postcodes.io/postcodes",
        json={"postcodes": [raw_postcode]},
        headers={"Content-Type": "application/json"},
    ).json()

    postcode_data = result["result"][0]["result"]
    location_data = {
        "error": False,
        "postcode": raw_postcode,
        "county": postcode_data["admin_county"]
        if postcode_data["admin_county"]
        else postcode_data["admin_district"],
        "region": postcode_data["region"]
        if postcode_data["region"]
        else postcode_data["european_electoral_region"],
        "country": postcode_data["country"],
        "constituency": postcode_data["parliamentary_constituency"],
    }
    return location_data


def derive_application_values(application_json):
    # TODO: implement mapping function to match
    #  fund+round fields to derived values
    derived_values = {}
    application_id = application_json["id"]
    print(f"deriving values for application id: {application_id}.")
    fund_round_shortname = "".join(
        application_json["reference"].split("-")[:2]
    )

    # search for asset_type
    try:
        asset_key = fund_round_data_key_mappings[fund_round_shortname][
            "asset_type"
        ]
        asset_type = get_answer_value(application_json, asset_key)
    except Exception:
        print(
            f"Could not extract asset_type from application: {application_id}."
        )
        asset_type = "No asset type specified."

    # search for capital funding
    try:
        funding_one = 0
        funding_one_keys = fund_round_data_key_mappings[fund_round_shortname][
            "funding_one"
        ]
        funding_one_keys = (
            [funding_one_keys]
            if isinstance(funding_one_keys, str)
            else funding_one_keys
        )
        for key in funding_one_keys:
            funding_one = funding_one + int(
                float(get_answer_value(application_json, key))
            )

    except Exception:
        print(
            "Could not extract funding_value_one from application: "
            + f"{application_id}."
        )
        funding_one = 0

    # search for revenue funding
    try:
        funding_two = 0
        funding_two_keys = fund_round_data_key_mappings[fund_round_shortname][
            "funding_two"
        ]
        funding_two_keys = (
            [funding_two_keys]
            if isinstance(funding_two_keys, str)
            else funding_two_keys
        )
        for key in funding_two_keys:
            funding_two = funding_two + int(
                float(get_answer_value(application_json, key))
            )
    except Exception:
        print(
            "Could not extract funding_value_two from application: "
            + f"{application_id}."
        )
        funding_two = 0

    # search for location postcode
    try:
        address_key = fund_round_data_key_mappings[fund_round_shortname][
            "location"
        ]
        address = get_answer_value(application_json, address_key)
        raw_postcode = address.split(",")[-1].strip().replace(" ", "").upper()
        location_data = get_location_json_from_postcode(raw_postcode)
    except Exception:
        print(
            "Could not extract address from application: "
            + f"{application_id}."
        )
        location_data = ""

    derived_values["application_id"] = application_id
    derived_values["project_name"] = application_json["project_name"]
    derived_values["short_id"] = application_json["reference"]
    derived_values["fund_id"] = application_json["fund_id"]
    derived_values["round_id"] = application_json["round_id"]
    derived_values["funding_amount_requested"] = funding_one + funding_two
    derived_values["asset_type"] = asset_type
    if location_data:
        derived_values["location_json_blob"] = location_data
    else:
        derived_values["location_json_blob"] = {"error": True}

    FIELD_DEFAULT_VALUE = "Not Available"
    if derived_values["location_json_blob"]["error"] is True:
        derived_values["location_json_blob"]["county"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["region"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["country"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"][
            "constituency"
        ] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["postcode"] = FIELD_DEFAULT_VALUE

    return derived_values
