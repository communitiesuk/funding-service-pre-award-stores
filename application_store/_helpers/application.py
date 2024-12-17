from operator import itemgetter

from flask import current_app
from fsd_utils import Decision
from fsd_utils.config.notify_constants import NotifyConstants

from application_store.config.key_report_mappings.mappings import (
    ROUND_ID_TO_KEY_REPORT_MAPPING,
)
from application_store.db.queries.application import create_qa_base64file
from application_store.db.queries.reporting.queries import (
    map_application_key_fields,
)
from application_store.external_services.models.notification import Notification
from config import Config


def order_applications(applications, order_by, order_rev):
    """
    Returns a list of ordered applications
    """
    if order_by and order_by in [
        "id",
        "status",
        "account_id",
        "assessment_deadline",
        "started_at",
        "last_edited",
    ]:
        applications = sorted(
            applications,
            key=itemgetter(order_by),
            reverse=int(order_rev),
        )
    return applications


def send_submit_notification(
    application_with_form_json,
    eoi_results,
    account,
    application_with_form_json_and_fund_name,
    application,
    round_data,
):
    contents = {
        NotifyConstants.APPLICATION_FIELD: create_qa_base64file(application_with_form_json_and_fund_name, True),
        NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: round_data.contact_email,
    }
    del contents[NotifyConstants.APPLICATION_FIELD]["forms"]
    full_name = account.full_name

    if eoi_results:
        eoi_decision = eoi_results["decision"]
        if not full_name:
            full_name = map_application_key_fields(
                application_with_form_json,
                ROUND_ID_TO_KEY_REPORT_MAPPING[application.round_id],
                application.round_id,
            ).get("lead_contact_name", "")

        match eoi_decision:
            case Decision.FAIL:
                return  # we don't send emails for a failure

            case Decision.PASS:
                notify_template = Config.NOTIFY_TEMPLATE_EOI_PASS

            case Decision.PASS_WITH_CAVEATS:
                notify_template = Config.NOTIFY_TEMPLATE_EOI_PASS_W_CAVEATS
                contents[NotifyConstants.APPLICATION_CAVEATS] = eoi_results["caveats"]
            case _:
                current_app.logger.error(
                    "Unknown eoi_decision [{eoi_decision}], unable to send submit notification",
                    extra=dict(eoi_decision=eoi_decision),
                )
                return
    else:
        notify_template = Config.NOTIFY_TEMPLATE_SUBMIT_APPLICATION

    message_id = Notification.send(
        notify_template,
        account.email,
        full_name.title() if full_name else None,
        contents,
    )

    current_app.logger.info(
        "Message added to the notification queue msg_id: [{message_id}]",
        extra=dict(message_id=message_id),
    )
