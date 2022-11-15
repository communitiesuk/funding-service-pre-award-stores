import itertools
from pprint import pprint
from random import choice
from random import sample
from string import ascii_uppercase
from uuid import uuid4

from tests.application_store_json import application_store_json_template


def create_rows(number_of_apps_per_round, number_of_funds, number_of_rounds):

    funds = [uuid4() for _ in range(number_of_funds)]

    project_names = itertools.cycle([
        "Save the boardgame cafe in Colchester",
        "Remodel the vintage cinema in Bath",
        "Rebuild the beautiful spar in Falmouth",
        "Restore the derelict student union in Plymouth",
    ])

    for count,fund_id in enumerate(funds):

        rounds = [
        uuid4() for _ in range(number_of_rounds)
        ]

        for round_id in rounds:

            app_ids = [
                uuid4() for _ in range(number_of_apps_per_round)
            ]

            for app_id in app_ids:


                project_name = next(project_names)

                short_ref = "COF-R2W2-" + "".join(sample(ascii_uppercase, 6))

                yield application_store_json_template.substitute(
                    app_id=app_id,
                    project_name=project_name,
                    short_ref=short_ref,
                    round_id=round_id,
                    fund_id=fund_id,
                )
