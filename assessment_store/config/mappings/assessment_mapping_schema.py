field_id_schema = {"type": ["string", "array"], "items": {"type": "string"}}

answer_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "field_id": field_id_schema,
            "form_name": {"type": "string"},
            "path": {"type": "string"},
            "field_type": {
                "type": "string",
                "enum": [
                    "textField",
                    "yesNoField",
                    "radiosField",
                    "datePartsField",
                    "UkAddressField",
                    "websiteField",
                    "multiInputField",
                    "multilinetextField",
                    "emailAddressField",
                    "telephonenumberField",
                    "numberField",
                    "checkboxesField",
                    "fileUploadField",
                    "clientSideFileUploadField",
                    "freetextField",
                    "monthYearField",
                ],
            },
            "presentation_type": {
                "type": "string",
                "enum": [
                    "text",
                    # covers:
                    # "textField",
                    # "yesNoField",
                    # "radiosField",
                    # "datePartsField",
                    # "websiteField",
                    # "numberField",
                    # "emailAddressField",
                    # "telephonenumberField",
                    # "monthYearField",
                    "free_text",
                    # freetextField
                    "address",
                    # covers:
                    # "UkAddressField",
                    "list",
                    # covers:
                    # "multiInputField",
                    # "multilinetextField",
                    # "checkboxesField",
                    "file",
                    # covers:
                    # "fileUploadField",
                    "grouped_fields",
                    # covers:
                    # "multipleFields",
                    "heading",
                    # covers:
                    # "section title for add-another component",
                    "description",
                    # covers:
                    # "question description for add-another component",
                    "amount",
                    # covers:
                    # "amount (£) for add-another component question"
                    "s3bucketPath",
                    # covers:
                    # "clientSideFileUploadField",
                    "table",
                    # covers:
                    # new add-another component with children support
                    # see https://github.com/communitiesuk/digital-form-builder/pull/161
                ],
            },
            "question": {"type": ["string", "array"]},
        },
        "additionalProperties": False,
        "minProperties": 4,
    },
}

themes_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "answers": answer_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

sub_criteria_schema = {
    "id": "sub_criteria_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "themes": themes_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

unscored_section_schema = {
    "id": "unscored_section_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "sub_criteria": sub_criteria_schema,
        },
        "additionalProperties": False,
        "minProperties": 3,
    },
}

scored_criteria_schema = {
    "id": "scored_criteria_schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "weighting": {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1,
            },
            "sub_criteria": sub_criteria_schema,
        },
        "additionalProperties": False,
        "minProperties": 4,
    },
}

top_level_assessment_mapping_schema = {
    "id": "top_level_assessment_mapping_schema",
    "type": "object",
    "properties": {
        "schema_id": {"type": "string"},
        "unscored_sections": unscored_section_schema,
        "scored_criteria": scored_criteria_schema,
    },
    "additionalProperties": False,
    "minProperties": 3,
}
