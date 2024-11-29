from collections import defaultdict
from datetime import datetime

import jsonpath_rw_ext
import requests
from flask import current_app

from config.mappings.assessment_mapping_fund_round import (
    fund_round_data_key_mappings,
)
from db.models.assessment_record import TagAssociation


def get_answer_value(application_json, answer_key):
    return (
        jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]")
        .find(application_json)[0]
        .value["answer"]
    )


def get_answer_value_for_multi_input(application_json, answer_key, value_key):
    answers = (
        jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]")
        .find(application_json)[0]
        .value["answer"]
    )

    funding_one = 0
    for answer in answers:
        funding_one = funding_one + int(float(answer[value_key]))
    return funding_one


def get_location_json_from_postcode(raw_postcode):
    """Make a POST request to the postcodes.io API with the provided postcode and
    extract the location data of postcode."""
    result = requests.post(
        url="http://api.postcodes.io/postcodes",
        json={"postcodes": [raw_postcode]},
        headers={"Content-Type": "application/json"},
    ).json()

    postcode_data = result["result"][0]["result"]
    location_data = (
        {
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
        if postcode_data
        else None
    )
    return location_data


def derive_application_values(application_json):  # noqa: C901 - historical sadness
    # TODO: implement mapping function to match
    #  fund+round fields to derived values
    derived_values = {}
    application_id = application_json["id"]
    print(f"deriving values for application id: {application_id}.")
    fund_round_shortname = "".join(application_json["reference"].split("-")[:2])

    # search for asset_type
    try:
        asset_type = "No asset type specified."
        if asset_key := fund_round_data_key_mappings[fund_round_shortname]["asset_type"]:
            asset_type = get_answer_value(application_json, asset_key)
    except Exception:
        print(f"Could not extract asset_type from application: {application_id}.")

    # search for capital funding
    funding_field_type = fund_round_data_key_mappings.get(fund_round_shortname, {}).get("funding_field_type")
    try:
        funding_one = 0
        if funding_one_keys := fund_round_data_key_mappings[fund_round_shortname]["funding_one"]:
            funding_one_keys = [funding_one_keys] if isinstance(funding_one_keys, str) else funding_one_keys

            if funding_field_type == "multiInputField" and len(funding_one_keys) > 1:
                funding_one = get_answer_value_for_multi_input(
                    application_json, funding_one_keys[0], funding_one_keys[1]
                )
            else:
                for key in funding_one_keys:
                    funding_one = funding_one + int(float(get_answer_value(application_json, key)))

    except Exception:
        print("Could not extract funding_value_one from application: " + f"{application_id}.")

    # search for revenue funding
    try:
        funding_two = 0
        if funding_two_keys := fund_round_data_key_mappings[fund_round_shortname]["funding_two"]:
            funding_two_keys = [funding_two_keys] if isinstance(funding_two_keys, str) else funding_two_keys
            if funding_field_type == "multiInputField" and len(funding_two_keys) > 1:
                funding_two = get_answer_value_for_multi_input(
                    application_json, funding_two_keys[0], funding_two_keys[1]
                )
            else:
                for key in funding_two_keys:
                    funding_two = funding_two + int(float(get_answer_value(application_json, key)))
    except Exception:
        print("Could not extract funding_value_two from application: " + f"{application_id}.")

    # search for location postcode
    try:
        location_data = ""
        if address_key := fund_round_data_key_mappings[fund_round_shortname]["location"]:
            address = get_answer_value(application_json, address_key)
            raw_postcode = address.split(",")[-1].strip().replace(" ", "").upper()
            location_data = get_location_json_from_postcode(raw_postcode)
            if not location_data:
                print(f"Invalid postcode '{raw_postcode}' provided for the application: {application_id}.")
    except Exception:
        print("Could not extract address from application: " + f"{application_id}.")

    derived_values["application_id"] = application_id
    if application_json["project_name"] is None and fund_round_shortname == "COFEOI":
        derived_values["project_name"] = (
            ""  # EOI does not have a project name form compoent. Maybe this has to become nullable?
        )
    else:
        derived_values["project_name"] = application_json["project_name"]

    derived_values["short_id"] = application_json["reference"]
    derived_values["fund_id"] = application_json["fund_id"]
    derived_values["round_id"] = application_json["round_id"]
    derived_values["funding_amount_requested"] = funding_one + funding_two
    derived_values["asset_type"] = asset_type
    derived_values["language"] = application_json["language"]
    if location_data:
        derived_values["location_json_blob"] = location_data
    else:
        derived_values["location_json_blob"] = {
            "error": True
            if fund_round_data_key_mappings[fund_round_shortname]["location"]
            else False  # if location is not mandatory for a fund, then treat error as `False`
        }

        FIELD_DEFAULT_VALUE = "Not Available"
        derived_values["location_json_blob"]["county"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["region"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["country"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["constituency"] = FIELD_DEFAULT_VALUE
        derived_values["location_json_blob"]["postcode"] = FIELD_DEFAULT_VALUE

    return derived_values


def get_most_recent_tags(tag_associations):
    # Create a dictionary to group tag_associations by tag_id
    tag_id_dict = {}
    for tag_assoc in tag_associations:
        tag_id = tag_assoc["tag"]["id"]
        tag_id_dict.setdefault(tag_id, []).append(tag_assoc)

    updated_tag_associations = []
    for assoc_list in tag_id_dict.values():
        # Sort each group by created_at timestamp to find the most recent entry
        sorted_tags = sorted(
            assoc_list,
            key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"),
            reverse=True,
        )
        # Append the most recent tag association to the updated list
        updated_tag_associations.append(sorted_tags[0])

    return updated_tag_associations


def update_tag_associations(assessment_metadatas):
    for metadata in assessment_metadatas:
        # Retrieve tag associations for the current metadata
        tag_associations = metadata.get("tag_associations", [])
        if tag_associations:
            # Update tag_associations for the current metadata with the most recent entries
            metadata["tag_associations"] = get_most_recent_tags(tag_associations)
    return assessment_metadatas


def get_existing_tags(application_id):
    """Queries the database for existing tags associated with a specific
    application, organises them by tag ID, and returns a defaultdict where each
    tag ID is associated with a list containing tuples of creation timestamps and
    their corresponding tag instances.

    Example:
        {'0000000-00000-00000-000001':
        [(datetime.datetime(2023, 11, 17, 18, 48, 25, tzinfo=datetime.timezone.utc),
          <TagAssociation db91a66b->), .......
          ]}

    """
    existing_tags = TagAssociation.query.filter(
        TagAssociation.application_id == application_id,
    ).all()
    list_existing_tags = defaultdict(list)
    for existing_tag in existing_tags:
        tag_id = str(existing_tag.tag_id)
        list_existing_tags[tag_id].append((existing_tag.created_at, existing_tag))
    return list_existing_tags


def filter_tags(incoming_tags, existing_tags):
    """If an incoming tag ID matches an existing tag ID, it skips that tag;
    otherwise, it appends the tag list from the existing tags to the filtered tags
    list."""
    filtered_tags = []
    for (
        existing_tag_id,
        existing_tag_list,
    ) in existing_tags.items():
        _incoming_tag = next(
            (incoming_tag for incoming_tag in incoming_tags if incoming_tag.get("id") == existing_tag_id),
            None,
        )
        if _incoming_tag:
            current_app.logger.info(
                "Tag id is already associated: {existing_tag_id}", extra=dict(existing_tag_id=existing_tag_id)
            )
        else:
            filtered_tags.append(existing_tag_list)
    return filtered_tags
