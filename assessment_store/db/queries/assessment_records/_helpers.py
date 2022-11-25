from db import db
from sqlalchemy import cast
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import JSONB

cof_json_mapper = {
    # "column name" : "jsonpath to value in jsonb blob".
    "application_id": "$.id",
    "project_name": "$.project_name",
    "short_id": "$.reference",
    "fund_id": "$.fund_id",
    "round_id": "$.round_id",
    "funding_amount_requested": (
        "$.forms[*].questions[*].fields[*] ? (@.key =="
        ' "JzWvhj")."answer".double() + $.forms[*].questions[*].fields[*] ?'
        ' (@.key == "jLIgoi")."answer".double() '
    ),
    "asset_type": (
        '$.forms[*].questions[*].fields[*] ? (@.key == "yaQoxU")."answer"'
    ),
}


def get_mapper(application_type: str) -> dict:
    """get_mapper A factory returning the dictionary associated with the given
    `application_type`.

    :param application_type: An application type for which we have an
    associated mapper dict. For example, "cof" is associated with
    `cof_json_mapper` through this function.
    :raises KeyError: Raised if the given `application_type` doesn't have an
    associated dict.
    :return: A dictionary with keys equal to the column names in `db.models.
    AssessmentRecord` and values equal to the jsonpath which will extract the
    column values from a json with the corresponding application type.
    """

    match application_type:

        case "COF":
            return cof_json_mapper

        case _:
            raise KeyError("Valid application type not given.")


def derive_values_from_json(loaded_json: dict, application_type: str) -> dict:
    """derive_values_from_json Given a loaded json dictionary `loaded_json` and
    an `application_type` we extract key values from the json and return them
    as a dictionary.

    :param loaded_json: An application json which has been converted to a
    python `dict` object.
    :param application_type: A string matching the cases found in `get_mapper`
    :return: A dictionary containing the values extracted from `loaded_json`.
    Keys match the keys in the associated mapping dict, such as
    `cof_json_mapper`.
    """

    mapper = get_mapper(application_type)

    # Uses a CTE query to extract values from blob, faster then using
    # python jsonpath libraries.

    loaded_blob = select(cast(loaded_json, JSONB).label("json_value")).cte(
        "blob"
    )

    selects = [
        func.jsonb_path_query_first(loaded_blob.c.json_value, json_path).label(
            column_name
        )
        for column_name, json_path in mapper.items()
    ]

    extract_fields_stmt = select(*selects).select_from(loaded_blob)

    return db.session.execute(extract_fields_stmt).one()._asdict()
