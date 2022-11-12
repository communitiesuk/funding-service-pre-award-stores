from random import choice
from random import sample
from string import ascii_uppercase
from uuid import uuid4

from tests.application_store_json import application_store_json_template


def create_rows(number_of_apps, round_id="", fund_id=""):

    ids = [str(uuid4()) for _ in range(number_of_apps)]

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

    for app_id in ids:

        project_name = (
            f"{choice(verbs)} the {choice(adjects)} {choice(places)} in"
            f" {choice(cities)}"
        )

        short_ref = "COF-R2W2-" + "".join(sample(ascii_uppercase, 6))

        yield application_store_json_template.substitute(
            app_id=app_id, project_name=project_name, short_ref=short_ref,
            round_id=round_id, fund_id=fund_id
        )
