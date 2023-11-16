import traceback
from typing import Dict

import requests
from config import Config  # noqa: E402
from flask import current_app


def get_data(endpoint: str, payload: Dict = None):
    try:
        if payload:
            current_app.logger.info(
                f"Fetching data from '{endpoint}', with payload: {payload}."
            )
            response = requests.get(endpoint, payload)
        else:
            current_app.logger.info(f"Fetching data from '{endpoint}'.")
            response = requests.get(endpoint)
        if response.status_code == 200:
            if "application/json" == response.headers["Content-Type"]:
                return response.json()
            else:
                return response.content
        elif response.status_code == 204:
            current_app.logger.warn(
                "Request successful but no resources returned for endpoint"
                f" '{endpoint}'."
            )
        else:
            current_app.logger.error(
                f"Could not get data for endpoint '{endpoint}' "
            )
    except requests.exceptions.RequestException as e:
        stack_trace = traceback.format_exc()
        current_app.logger.error(f"{e}\n{stack_trace}")


def get_account_name(id: str):
    url = Config.ACCOUNT_STORE_API_HOST + Config.ACCOUNTS_ENDPOINT
    params = {"account_id": id}
    # When developing locally, all comments and scores (etc) are
    # created by the local debug user by default . This user is not seeded
    # in the account store, it is not required as we circumnavigate SSO in assessment frontend.
    if id == "00000000-0000-0000-0000-000000000000":
        return "Local Debug User"
    else:
        response = get_data(url, params)
    return response["full_name"]
