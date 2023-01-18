def load_json_strings_from_file(filename: str) -> list[str]:
    import json

    with open(f"tests/test_data/{filename}", "r") as f:
        parsed_json_apps_file = json.load(f)

    list_of_json_strings = [
        json.dumps(json_object) for json_object in parsed_json_apps_file
    ]

    return list_of_json_strings


def get_dynamic_rows(
    number_of_apps_per_round, number_of_funds, number_of_rounds
):

    from random import choice, sample
    from string import ascii_uppercase
    from uuid import uuid4

    from tests._application_store_json import application_store_json_template

    funds = [uuid4() for _ in range(number_of_funds)]

    verbs = ["Save", "Restore", "Refurbish", "Rebuild", "Remodel"]

    adjects = ["old", "humble", "derelict", "vintage", "loved", "beautiful"]

    places = [
        ("skatepark", "sporting"),
        ("pub", "pub"),
        ("cinema", "cinema"),
        ("community centre", "community-centre"),
        ("gallery", "gallery"),
        ("museum", "museum"),
    ]
    cities = [
        ("Bath", "England"),
        ("Birmingham", "England"),
        ("Bradford", "England"),
        ("Brighton", "England"),
        ("Bristol", "England"),
        ("Cambridge", "England"),
        ("Canterbury", "England"),
        ("Carlisle", "England"),
        ("Chelmsford", "England"),
        ("Chichester", "England"),
        ("Colchester", "England"),
        ("Exeter", "England", "EX44NT"),
        ("Gloucester", "England"),
        ("Hereford", "England"),
        ("Aberdeen", "Scotland", "AB11 6LX"),
        ("Dundee", "Scotland"),
        ("Dunfermline", "Scotland"),
        ("Edinburgh", "Scotland"),
        ("Bangor", "Wales"),
        ("Cardiff", "Wales", "CF10 1EP"),
        ("Newport", "Wales", "NP10 8QQ"),
    ]

    for count, fund_id in enumerate(funds):

        rounds = [uuid4() for _ in range(number_of_rounds)]

        for round_id in rounds:

            app_ids = [uuid4() for _ in range(number_of_apps_per_round)]

            for app_id in app_ids:

                picked_place = choice(places)
                picked_city = choice(cities)

                project_name = (
                    f"{choice(verbs)} the"
                    f" {choice(adjects)} {picked_place[0]} in {picked_city[0]}"
                )

                short_ref = "COF-R2W2-" + "".join(sample(ascii_uppercase, 6))

                print("Seeding db inc location info")
                location_json_blob = {
                    "location_error": "false",
                    "location_county": "test-county",
                    "location_region": picked_city[1],
                    "location_country": picked_city[1],
                    "location_postcode": picked_city[2]
                    if len(picked_city) > 2
                    else "QQ12QQ",
                    "location_constituency": "test-constituency",
                }
                yield application_store_json_template.substitute(
                    app_id=app_id,
                    project_name=project_name,
                    short_ref=short_ref,
                    round_id="c603d114-5364-4474-a0c4-c41cbf4d3bbd",
                    fund_id="47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
                    asset_type=picked_place[1],
                    **location_json_blob,
                )
