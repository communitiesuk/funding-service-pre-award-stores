from functools import lru_cache

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
