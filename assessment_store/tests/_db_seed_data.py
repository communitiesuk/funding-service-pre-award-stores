def get_deterministic_rows():

    import json

    with open("tests/test_data/apps.json", "r") as f:

        parsed_json_apps_file = json.load(f)

    list_of_json_strings = [
        json.dumps(json_object) for json_object in parsed_json_apps_file
    ]

    return list_of_json_strings


def get_dynamic_rows(
    number_of_apps_per_round, number_of_funds, number_of_rounds
):

    from random import choice
    from random import sample
    from string import ascii_uppercase
    from uuid import uuid4

    from tests._application_store_json import application_store_json_template

    funds = [uuid4() for _ in range(number_of_funds)]

    verbs = ["Save", "Restore", "Refurbish", "Rebuild", "Remodel"]

    adjects = ["old", "humble", "derelict", "vintage", "loved", "beautiful"]

    places = [
        "skatepark",
        "pub",
        "cinema",
        "community centre",
    ]
    cities = [
        "Bath",
        "Birmingham",
        "Bradford",
        "Brighton",
        "Bristol",
        "Cambridge",
        "Canterbury",
        "Carlisle",
        "Chelmsford",
        "Chichester",
        "Colchester",
        "Exeter",
        "Gloucester",
        "Hereford",
        "Aberdeen",
        "Dundee",
        "Dunfermline",
        "Edinburgh",
        "Bangor",
        "Cardiff",
        "Newport",
    ]

    for count, fund_id in enumerate(funds):

        rounds = [uuid4() for _ in range(number_of_rounds)]

        for round_id in rounds:

            app_ids = [uuid4() for _ in range(number_of_apps_per_round)]

            for app_id in app_ids:

                project_name = (
                    f"{choice(verbs)} the"
                    f" {choice(adjects)} {choice(places)} in {choice(cities)}"
                )

                short_ref = "COF-R2W2-" + "".join(sample(ascii_uppercase, 6))

                yield application_store_json_template.substitute(
                    app_id=app_id,
                    project_name=project_name,
                    short_ref=short_ref,
                    round_id=round_id,
                    fund_id=fund_id,
                )
