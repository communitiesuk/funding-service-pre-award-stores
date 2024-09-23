import traceback
from typing import Dict

import requests
from api.models.notification import Notification
from config import Config  # noqa: E402
from flask import current_app


def get_data(endpoint: str, payload: Dict = None):
    try:
        if payload:
            current_app.logger.info(f"Fetching data from '{endpoint}', with payload: {payload}.")
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
            current_app.logger.warning("Request successful but no resources returned for endpoint" f" '{endpoint}'.")
        else:
            current_app.logger.error(f"Could not get data for endpoint '{endpoint}' ")
    except requests.exceptions.RequestException as e:
        stack_trace = traceback.format_exc()
        current_app.logger.error(f"{e}\n{stack_trace}")


def get_account_data(account_id: str):
    return get_data(Config.ACCOUNT_STORE_API_HOST + Config.ACCOUNTS_ENDPOINT, {"account_id": account_id})


def get_fund_data(fund_id: str):
    return get_data(Config.FUND_STORE_API_HOST + Config.FUND_ENDPOINT.format(fund_id=fund_id, use_short_name=False))


def create_assessment_url_for_application(application_id: str):
    return Config.ASSESSMENT_FRONTEND_HOST + Config.ASSESSMENT_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )


def send_notification_email(application, user_id, assigner_id, template, message=None):
    """Sends a notification email to inform the user (specified by user_id) that
    an application has been assigned to them.

    Parameters:
        application (dict): dict of application details for the application that has been assigned
        user_id (str): id of assignee and recipient of email
        assigner_id (str): id of the assigner.
        template (str): template of email (either assignment or unassignment)
        message (str): Custom message provided by assigner

    """
    user_response = get_account_data(account_id=user_id)
    assigner_response = get_account_data(account_id=assigner_id)
    fund_response = get_fund_data(fund_id=application["fund_id"])

    content = {
        "fund_name": fund_response["name"],
        "reference_number": application["short_id"],
        "project_name": application["project_name"],
        "lead_assessor_email": assigner_response["email_address"],
        "assessment_link": create_assessment_url_for_application(application_id=application["application_id"]),
    }

    if message:
        content["message"] = message

    try:
        message_id = Notification.send(
            template,
            user_response["email_address"],
            user_response["full_name"] if user_response["full_name"] else None,
            content,
        )
        current_app.logger.info(f"Message added to the queue msg_id: [{message_id}]")
    except Exception:
        current_app.logger.info(
            f"Could not send email for template: {template}, user: {user_id}, "
            f"application {application['application_id']}"
        )


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
