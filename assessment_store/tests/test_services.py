from unittest import mock

import pytest

from services.data_services import send_notification_email


@pytest.mark.parametrize(
    "message, expected_message_in_content",
    [
        (None, False),  # Case without a custom message
        ("This is a custom message", True),  # Case with a custom message
    ],
)
@mock.patch("services.data_services.get_account_data")
@mock.patch("services.data_services.get_fund_data")
@mock.patch("services.data_services.create_assessment_url_for_application")
@mock.patch("services.data_services.Notification.send")
@mock.patch("services.data_services.current_app.logger")
def test_send_notification_email(
    mock_logger,
    mock_notification_send,
    mock_assessment_url,
    mock_get_fund_data,
    mock_get_account_data,
    message,
    expected_message_in_content,
    app,
):
    test_application = {
        "application_id": "app1",
        "fund_id": "fund1",
        "short_id": "APP123",
        "project_name": "Project X",
    }

    mock_get_account_data.side_effect = [
        {"email_address": "user@example.com", "full_name": "User One"},  # user data
        {"email_address": "assigner@example.com"},  # assigner data
    ]

    mock_get_fund_data.return_value = {"name": "Fund A"}
    mock_notification_send.return_value = "message-id-1234"
    mock_assessment_url.return_value = "assessment_url"

    send_notification_email(test_application, "user1", "assigner1", "assignment_template", message=message)

    content = {
        "fund_name": "Fund A",
        "reference_number": "APP123",
        "project_name": "Project X",
        "lead_assessor_email": "assigner@example.com",
        "assessment_link": "assessment_url",
    }

    if expected_message_in_content:
        content["message"] = message

    mock_notification_send.assert_called_once_with("assignment_template", "user@example.com", "User One", content)


@mock.patch("services.data_services.get_account_data")
@mock.patch("services.data_services.get_fund_data")
@mock.patch("services.data_services.create_assessment_url_for_application")
@mock.patch(
    "services.data_services.Notification.send",
    side_effect=Exception("Error sending notification"),
)
@mock.patch("services.data_services.current_app.logger")
def test_send_notification_email_failure(
    mock_logger,
    mock_notification_send,
    mock_assessment_url,
    mock_get_fund_data,
    mock_get_account_data,
    app,
):
    test_application = {
        "application_id": "app1",
        "fund_id": "fund1",
        "short_id": "APP123",
        "project_name": "Project X",
    }

    mock_get_account_data.side_effect = [
        {"email_address": "user@example.com", "full_name": "User One"},  # user data
        {"email_address": "assigner@example.com"},  # assigner data
    ]

    mock_get_fund_data.return_value = {"name": "Fund A"}

    send_notification_email(test_application, "user1", "assigner1", "assignment_template")

    mock_logger.info.assert_called_with(
        "Could not send email for template: assignment_template, user: user1, application app1"
    )
