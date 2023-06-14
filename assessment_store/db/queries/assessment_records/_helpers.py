import jsonpath_rw_ext


def get_answer_value(application_json, answer_key):
    return (
        jsonpath_rw_ext.parse(
            f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]"
        )
        .find(application_json)[0]
        .value["answer"]
    )


def derive_application_values(application_json):
    # TODO: implement mapping function to match
    #  fund+round fields to derived values
    derived_values = {}
    application_id = application_json["id"]
    print(f"deriving values for application id: {application_id}.")
    short_ref = application_json["reference"]
    try:
        asset_type = get_answer_value(application_json, "yaQoxU")
    except Exception:
        print(
            f"Could not extract asset_type from application: {application_id}."
        )
        asset_type = "Not asset type specified."
    try:
        if "COF-R2" in short_ref:  # cof r2
            funding_one = get_answer_value(application_json, "JzWvhj")
        elif "COF-R3W1" in short_ref:  # cof r3w1
            funding_one = get_answer_value(application_json, "ABROnB")
        elif "NSTF-R2" in short_ref:  # Night shelter R2
            funding_one = int(
                float(get_answer_value(application_json, "QUCvFy"))
                + float(get_answer_value(application_json, "pppiYl"))
            )
        else:
            funding_one = 0
    except Exception:
        print(
            "Could not extract funding_value_one from application: "
            + f"{application_id}."
        )
        funding_one = 0
    try:
        if "COF-R2" in short_ref:  # cof r2
            funding_two = get_answer_value(application_json, "jLIgoi")
        elif "COF-R3W1" in short_ref:  # cof r3w1
            funding_two = get_answer_value(application_json, "cLDRvN")
        elif "NSTF-R2" in short_ref:  # Night shelter R2
            funding_two = int(
                float(get_answer_value(application_json, "GRWtfV"))
                + float(get_answer_value(application_json, "zvPzXN"))
            )
        else:
            funding_two = 0
    except Exception:
        print(
            "Could not extract funding_value_two from application: "
            + f"{application_id}."
        )
        funding_two = 0
    derived_values["application_id"] = application_id
    derived_values["project_name"] = application_json["project_name"]
    derived_values["short_id"] = short_ref
    derived_values["fund_id"] = application_json["fund_id"]
    derived_values["round_id"] = application_json["round_id"]
    derived_values["funding_amount_requested"] = int(float(funding_one)) + int(
        float(funding_two)
    )
    derived_values["asset_type"] = asset_type
    if "location_json_blob" in application_json.keys():
        derived_values["location_json_blob"] = application_json[
            "location_json_blob"
        ]
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
