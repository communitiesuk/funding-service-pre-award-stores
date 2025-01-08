from unittest import mock

import pytest

from assessment_store.services.data_services import _send_notification_email, send_notification_email_assigned
from services.notify import NotificationService


@pytest.mark.parametrize(
    "message, expected_message_in_content",
    [
        (None, ""),  # Case without a custom message
        ("This is a custom message", "This is a custom message"),  # Case with a custom message
    ],
)
@mock.patch("assessment_store.services.data_services.get_account_data")
@mock.patch("assessment_store.services.data_services.get_fund_data")
@mock.patch("assessment_store.services.data_services.create_assessment_url_for_application")
@mock.patch("assessment_store.services.data_services.current_app.logger")
def test_send_notification_email_assigned(
    mock_logger,
    mock_assessment_url,
    mock_get_fund_data,
    mock_get_account_data,
    message,
    expected_message_in_content,
    mocker,
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
    mock_assessment_url.return_value = "assessment_url"

    mock_notification_service = mock.MagicMock()
    mocker.patch(
        "assessment_store.services.data_services.get_notification_service", return_value=mock_notification_service
    )

    send_notification_email_assigned(
        application=test_application, user_id="user1", assigner_id="assigner1", message=message
    )

    mock_notification_service.send_assessment_email.assert_called_once_with(
        email_address="user@example.com",
        template_id=NotificationService.ASSESSMENT_APPLICATION_ASSIGNED,
        fund_name="Fund A",
        reference_number="APP123",
        project_name="Project X",
        lead_assessor_email="assigner@example.com",
        assessment_link="assessment_url",
        assignment_message=expected_message_in_content,
    )


@mock.patch("assessment_store.services.data_services.get_account_data")
@mock.patch("assessment_store.services.data_services.get_fund_data")
@mock.patch("assessment_store.services.data_services.create_assessment_url_for_application")
@mock.patch("assessment_store.services.data_services.current_app.logger")
def test_send_notification_email_failure(
    mock_logger, mock_assessment_url, mock_get_fund_data, mock_get_account_data, app, mocker
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
    mock_notification_service = mock.MagicMock()
    mocker.patch(
        "assessment_store.services.data_services.get_notification_service", return_value=mock_notification_service
    )
    notification_error = Exception("Error sending notification")
    mock_notification_service.send_assessment_email.side_effect = notification_error

    send_notification_email_assigned(
        application=test_application, user_id="user1", assigner_id="assigner1", message="test message"
    )

    mock_logger.error.assert_called_with(
        "Could not send email for template: {template}, user: {user_id}, application {application_id}",
        extra={
            "template": NotificationService.ASSESSMENT_APPLICATION_ASSIGNED,
            "user_id": "user1",
            "application_id": "app1",
        },
        exc_info=notification_error,
    )
