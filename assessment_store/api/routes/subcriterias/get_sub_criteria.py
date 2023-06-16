import copy
from collections import defaultdict

from config import Config
from db.queries.assessment_records.queries import get_application_jsonb_blob
from flask import abort
from flask import current_app


def get_all_subcriteria(fund_id, round_id):
    sub_criterias = []
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    for section in (
        display_config["scored_criteria"] + display_config["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            sub_criterias.append(sub_criteria)
    return sub_criterias


def return_subcriteria_from_mapping(sub_criteria_id, fund_id, round_id):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    display_config = copy.deepcopy(
        Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"]
    )
    sub_criterias = get_all_subcriteria(fund_id, round_id)
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        sub_crit = matching_sub_criteria[0]

        is_scored = False
        for criteria in display_config["scored_criteria"]:
            for sub_criteria in criteria["sub_criteria"]:
                if sub_criteria_id == sub_criteria["id"]:
                    is_scored = True
        sub_crit["is_scored"] = is_scored

        return sub_crit
    elif len(matching_sub_criteria) > 1:
        msg = "sub_criteria: '{sub_criteria_id}' duplicated."
        current_app.logger.error(msg)
        raise ValueError(msg)
    else:
        msg = f"sub_criteria: '{sub_criteria_id}' not found."
        current_app.logger.warn(msg)
        abort(404, description=msg)


def get_themes_fields(
    theme_id: str, fund_id: str, round_id: str
) -> list[dict]:
    """function takes a theme_id arg & returns a list
    of answers with given theme_id.
    """
    sub_criterias = get_all_subcriteria(fund_id, round_id)
    try:
        return [
            theme.get("answers")
            for themes in sub_criterias
            for theme in themes.get("themes")
            if theme_id == theme.get("id")
        ][0]
    except IndexError:
        current_app.logger.error(f"Incorrect theme id -> {theme_id}")
        return f"Incorrect theme id -> {theme_id}"


def get_application_form(app_json_blob):
    """function return list of all questions from application form"""

    return [
        questions
        for forms in app_json_blob["jsonb_blob"]["forms"]
        for questions in forms["questions"]
    ]


def convert_boolean_values(themes_fields: list[dict]) -> None:
    """function checks boolean values in themes_answers & replace
    boolean values to string. (False -> "No", True -> "Yes")
    Args:
        themes_fields (_type_): array of dict
    """
    current_app.logger.info("Converting boolean values to strings")
    for field in themes_fields:
        if "answer" not in field.keys():
            continue
        elif field["answer"] is False:
            field.update(answer="No")
        elif field["answer"] is True:
            field.update(answer="Yes")


# supports the old version of add-another which was
# not scalable and did not allow the adding of N* fields
def deprecated_sort_add_another_component_contents(
    themes_fields: list[dict],
) -> None:
    """function checks for special presentation_type "heading"
    in array of themes fields, if exists, adds question-value
    to an answer key for presentation_type "heading" theme and
    looks for presentation_type of "description" and "amount" with
    same presentation_type "heading"s field_id, retrieve words
    onlyproject-costs from strings of answers for
    presentation_type "description" theme& numbers only
    for presentation_type "amount" theme.

    Args:
        themes_answers (_type_): array of dict
    """
    for field in themes_fields:
        try:
            if field["presentation_type"] != "heading":
                continue

            field["answer"] = field["question"]
            for theme in themes_fields:
                if not field["field_id"] in theme.values():
                    continue

                if theme["presentation_type"] == "description":
                    description_answer = [
                        description.rsplit(": ", 1)[0]
                        for description in theme["answer"]
                    ]
                    theme["answer"] = description_answer

                if theme["presentation_type"] == "amount":
                    amount_answer = [
                        amount.rsplit(": ", 1)[1] for amount in theme["answer"]
                    ]
                    theme["answer"] = amount_answer
        except (KeyError, IndexError):
            current_app.logger.debug(
                f"Answer not provided for field_id: {field['field_id']}"
            )


# All in use children of MultiInputField in cofr3/nstfr2
# If we use or add new children, we may need to add support
_MULTI_INPUT_FORMAT_FRONTEND = defaultdict(
    lambda: "text",
    {
        "NumberField": "currency",
        "MultilineTextField": "html",
        # the default should handle these, but let's be explicit
        "RadioField": "text",
        "TextField": "text",
        "MonthYearField": "text",
        "YesNoField": "text",
    },
)

_MULTI_INPUT_FRE_FRONTEND_FORMATTERS = {
    "RadioField": lambda x: x.capitalize(),
    "YesNoField": lambda x: "Yes" if bool(x) else "No",
}


def format_add_another_component_contents(
    themes_fields: list[dict],
) -> list[dict]:
    for field in themes_fields:
        if field.get("presentation_type") != "table":
            continue

        title, table_config = field["question"]
        field["question"] = title

        component_id_to_answer_list = {}
        for answer_container in field["answer"]:
            for component_id, answer in answer_container.items():
                if component_id not in component_id_to_answer_list:
                    component_id_to_answer_list[component_id] = []
                component_id_to_answer_list[component_id].append(answer)

        table = []
        for component_id, column_config in table_config.items():
            title = column_config["column_title"]
            answers = component_id_to_answer_list.get(component_id)

            frontend_format = _MULTI_INPUT_FORMAT_FRONTEND.get(
                column_config["type"], "text"
            )
            pre_frontend_formatter = _MULTI_INPUT_FRE_FRONTEND_FORMATTERS.get(
                column_config["type"], lambda x: x
            )
            formatted_answers = [
                pre_frontend_formatter(answer) for answer in answers
            ]

            if formatted_answers:
                table.append([title, formatted_answers, frontend_format])
        field["answer"] = table

    return themes_fields


def map_grouped_fields_answers(theme: dict, questions: dict) -> tuple:
    """function looks for list of grouped field_ids such as ["JzWvhj", "jLIgoi"],
    maps them  with question keys and returns a list of answers
    for given field ids"""

    for question in questions:
        answer_list = tuple(
            (
                (app["title"], app["answer"])
                for app in question["fields"]
                for field_id in theme["field_id"]
                if "answer" in app.keys() and app["key"] == field_id
            )
        )
        if answer_list:
            theme["answer"] = answer_list


def map_single_field_answer(theme: list, questions: dict) -> str:
    """function looks for a field_id, maps it with question keys
    and returns an answer for given field id"""
    for question in questions:
        for app_fields in question["fields"]:
            if (
                theme["field_id"] == app_fields["key"]
                and "answer" in app_fields.keys()
            ):
                theme["answer"] = app_fields["answer"]


def map_application_with_sub_criteria_themes(
    application_id: str, theme_id: str, fund_id: str, round_id: str
):
    """function maps answers from application with assessor task list
    themes through field ids.
    Args: application_id, theme_id, fund_id, round_id
    Exceptions: returning custom exception along with openapi
    validation detail.
    """

    themes_fields = get_themes_fields(theme_id, fund_id, round_id)
    application_json_blob = get_application_jsonb_blob(application_id)
    questions = get_application_form(application_json_blob)

    current_app.logger.info("mapping subcriteria theme contents")
    for theme in themes_fields:
        try:
            if isinstance(theme["field_id"], list):
                map_grouped_fields_answers(theme, questions)
            else:
                map_single_field_answer(theme, questions)
        except TypeError:
            current_app.logger.error(f"Incorrect theme id -> {theme_id}")
            return f"Incorrect theme id -> {theme_id}"

    convert_boolean_values(themes_fields)

    # Does not sort on the new version of add-another simply pass the object through for display by assessment frontend
    # the old version of add-another which was not scalable and did not allow the adding of N* fields
    deprecated_sort_add_another_component_contents(themes_fields)

    return format_add_another_component_contents(themes_fields)
