from sqlalchemy import select, cast, func
from sqlalchemy.dialects.postgresql import JSONB
import json
from db import db

COF_json_mapper = {
    # "column name" : "jsonpath to value in jsonb blob".
    "application_id": "$.id",
    "project_name": "$.project_name",
    "short_id": "$.reference",
    "fund_id": "$.fund_id",
    "round_id": "$.round_id",
    "funding_amount_requested": (
        """$.forms[*].questions[*].fields[*] ? (@.key == "JzWvhj")."answer".double()
        + $.forms[*].questions[*].fields[*] ? (@.key == "jLIgoi")."answer".double() """
    ),
}


def get_mapper(application_type):

    match application_type:

        case "COF":
            return COF_json_mapper

        case _:
            raise KeyError("Valid application type not given.")


def derive_values_from_json(loaded_json, application_type):

    mapper = get_mapper(application_type)

    # Uses a CTE query to extract values from blob, faster then using 
    # python jsonpath libraries.

    loaded_blob = select(
        cast(loaded_json, JSONB).label("json_value"
    )).cte("blob")

    selects = [func.jsonb_path_query_first(loaded_blob.c.json_value, json_path).label(column_name) for column_name, json_path in mapper.items()]

    extract_fields_stmt = select(*selects).select_from(loaded_blob)

    return db.session.execute(extract_fields_stmt).one()._asdict()
