import json
from functools import lru_cache

from db import db
from db.models.assessment_record.assessment_records import AssessmentRecords
from jsonpath_ng.ext import parse

COF_json_mapper = {
    "application_id": "$.id",
    "project_name": "$.project_name",
    "short_id": "$.reference",
    "fund_id": "$.fund_id",
    "round_id": "$.round_id",
    "funding_amount_requested": (
        '$.forms[*].questions[*].fields[?(@.key == "JzWvhj")].answer'
    ),
}


def get_mapper(application_type):

    match application_type:

        case "COF":
            return COF_json_mapper

        case "citizan_space":
            return {"id": "some key in some json somewhere."}


@lru_cache
def jsonpath_extractors(json_type: str):

    json_mapper = get_mapper(json_type)

    jsonpath_matchers = {
        key: parse(jsonpath_str)
        for key, jsonpath_str in json_mapper.items()
        if key != "DEFAULTS"
    }

    return jsonpath_matchers


def derive_values_from_json(json_as_dict, json_type):

    parsed_json_paths = jsonpath_extractors(json_type)

    found_values_from_json = dict()

    for key, jsonpath_query in parsed_json_paths.items():

        found_values_from_json[key] = (
            jsonpath_query.find(json_as_dict).pop().value
        )

    return found_values_from_json


def bulk_insert_application_record(json_strings, application_type):

    rows = []

    for single_json_string in json_strings:

        loaded_json = json.loads(single_json_string)

        row = {
            "jsonb_blob": loaded_json,
            "type_of_application": application_type,
        }

        derived_values = derive_values_from_json(loaded_json, application_type)

        row = {**row, **derived_values}
        rows.append(row)

        del loaded_json

    db.session.bulk_insert_mappings(AssessmentRecords, rows)
    db.session.commit()


# flake8: noqa
# def bulk_insert_application_record(json_strings, application_type):

#     record_rows = []
#     blob_rows = []

#     for single_json_string in json_strings:


#         loaded_json = json.loads(single_json_string)

#         row = {"jsonb_blob" : loaded_json, "type_of_application" : application_type}

#         derived_values = derive_values_from_json(loaded_json, application_type)

#         row = {**row, **derived_values}
#         record_rows.append(row)

#         blob_rows.append("jsonb_blob" : loaded_json, "application_id" : row["application_id"])

#         del loaded_json

#     db.session.bulk_insert_mappings(AssessmentRecords, record_rows)
#     db.session.bulk_insert_mappings(AssessmentJsonBlobs, record_rows)
#     db.session.commit()
