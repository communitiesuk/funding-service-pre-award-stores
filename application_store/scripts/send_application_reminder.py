#!/usr/bin/env python3
import sys

from services.notify import get_notification_service

sys.path.insert(1, ".")

from datetime import datetime  # noqa: E402

import pytz  # noqa: E402
import requests  # noqa: E402
from flask import current_app  # noqa: E402

from application_store import external_services  # noqa: E402
from application_store.db.queries import search_applications  # noqa: E402
from application_store.external_services.exceptions import (
    NotificationError,  # noqa: E402
)
from config import Config  # noqa: E402


def application_deadline_reminder(flask_app):  # noqa:C901 from before ruff
    with flask_app.app_context():
        uk_timezone = pytz.timezone("Europe/London")
        current_datetime = datetime.now(uk_timezone).replace(tzinfo=None)
        funds = external_services.get_data(Config.FUND_STORE_API_HOST + Config.FUNDS_ENDPOINT)

        for fund in funds:
            fund_id = fund.get("id")
            round_info = external_services.get_data(
                Config.FUND_STORE_API_HOST + Config.FUND_ROUNDS_ENDPOINT.format(fund_id=fund_id)
            )

            for round in round_info:
                round_deadline_str = round.get("deadline")
                reminder_date_str = round.get("reminder_date")

                if not reminder_date_str:
                    current_app.logger.info(
                        "No reminder is set for the round %(round_title)s",
                        dict(round_title=round.get("title")),
                    )
                    continue

                application_reminder_sent = round.get("application_reminder_sent")

                # Convert the string dates to datetime objects
                round_deadline = datetime.strptime(round_deadline_str, "%Y-%m-%dT%H:%M:%S")
                reminder_date = datetime.strptime(reminder_date_str, "%Y-%m-%dT%H:%M:%S")

                if not application_reminder_sent and reminder_date < current_datetime < round_deadline:
                    round_id = round.get("id")
                    round_name = round.get("title")
                    contact_email = round.get("contact_email")
                    fund_info = external_services.get_data(
                        Config.FUND_STORE_API_HOST + Config.FUND_ENDPOINT.format(fund_id=fund_id)
                    )
                    fund_name = fund_info.get("name")

                    status = {
                        "status_only": ["IN_PROGRESS", "NOT_STARTED", "COMPLETED"],
                        "fund_id": fund_id,
                        "round_id": round_id,
                    }

                    not_submitted_applications = search_applications(**status)

                    all_applications = []
                    for application in not_submitted_applications:
                        application["round_name"] = round_name
                        application["fund_name"] = fund_name
                        application["contact_help_email"] = contact_email
                        account = external_services.get_account(account_id=application.get("account_id"))
                        application["account_email"] = account.email
                        application["deadline_date"] = round_deadline_str
                        all_applications.append({"application": application})

                    # Only one email per account_email
                    unique_email_account = {}
                    for application in all_applications:
                        unique_email_account[application["application"]["account_email"]] = application
                    unique_application_email_addresses = list(unique_email_account.values())

                    if len(unique_application_email_addresses) > 0:
                        for count, application in enumerate(unique_application_email_addresses, start=1):
                            email = {"email": application["application"]["account_email"]}

                            current_app.logger.info(
                                "Sending reminder %(count)s of %(total)s",
                                dict(count=count, total=len(unique_email_account)),
                            )

                            try:
                                notification = get_notification_service().send_application_deadline_reminder_email(
                                    email.get("email"),
                                    fund_name=application["application"]["fund_name"],
                                    application_reference=application["application"]["reference"],
                                    round_name=application["application"]["round_name"],
                                    deadline=application["application"]["deadline_date"],
                                    contact_help_email=application["application"]["contact_help_email"],
                                )
                                current_app.logger.info(
                                    "Sent notification %(notification_id)s for application %(application_reference)s",
                                    dict(
                                        notification_id=notification.id,
                                        application_reference=application["application"]["reference"],
                                    ),
                                )
                                if len(unique_application_email_addresses) == count:
                                    try:
                                        application_reminder_endpoint = (
                                            Config.FUND_STORE_API_HOST
                                            + Config.FUND_ROUND_APPLICATION_REMINDER_STATUS.format(round_id=round_id)
                                        )
                                        response = requests.put(application_reminder_endpoint)
                                        if response.status_code == 200:
                                            current_app.logger.info(
                                                "The application reminder has been"
                                                " sent successfully for round_id"
                                                " %(round_id)s",
                                                dict(found_id=round_id),
                                            )
                                    except Exception as e:
                                        current_app.logger.info(
                                            "There was an issue updating the"
                                            " application_reminder_sent column in the"
                                            " Round store for %(round_id)s. Errro %(errno)s",
                                            dict(round_id=round_id, errno=e),
                                        )

                            except NotificationError as e:
                                current_app.logger.error(e.message)

                    else:
                        current_app.logger.info("Currently, there are no non-submitted applications")
                else:
                    continue


if __name__ == "__main__":
    application_deadline_reminder()
