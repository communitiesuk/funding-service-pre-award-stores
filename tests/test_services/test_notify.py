import uuid

import responses
from responses import matchers

from services.notify import Notification, get_notification_service


class TestNotificationService:
    """
    Test that the methods we've written for sending emails using the GOV.UK Notify Python SDK map to the expected
    HTTP API calls.
    """

    @responses.activate
    def test_send_magic_link(self, app):
        request_matcher = responses.post(
            url="https://api.notifications.service.gov.uk/v2/notifications/email",
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "email_address": "test@test.com",
                        "template_id": "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2",
                        "personalisation": {
                            "name of fund": "test fund",
                            "link to application": "https://magic-link",
                            "contact details": "contact@test.com",
                            "request new link url": "https://new-magic-link",
                        },
                        "reference": "abc123",
                    }
                )
            ],
            json={"id": "00000000-0000-0000-0000-000000000000"},  # partial GOV.UK Notify response
        )

        resp = get_notification_service().send_magic_link(
            "test@test.com",
            "https://magic-link",
            "test fund",
            "contact@test.com",
            "https://new-magic-link",
            "abc123",
        )
        assert resp == Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000000"))
        assert request_matcher.call_count == 1

    @responses.activate
    def test_send_incomplete_application_email(self, app):
        request_matcher = responses.post(
            url="https://api.notifications.service.gov.uk/v2/notifications/email",
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "email_address": "test@test.com",
                        "template_id": "944cb37d-c9e0-4731-88f5-d752514da57f",
                        "personalisation": {
                            "name of fund": "test fund",
                            "application reference": "appref-123",
                            "round name": "test round",
                            "question": {
                                "file": "YWJjZGVm",  # base64 'abcdef'
                                "filename": None,
                                "confirm_email_before_download": None,
                                "retention_period": None,
                            },
                            "contact email": "contact@test.com",
                        },
                        "reference": "abc123",
                    }
                )
            ],
            json={"id": "00000000-0000-0000-0000-000000000004"},  # partial GOV.UK Notify response
        )

        resp = get_notification_service().send_incomplete_application_email(
            "test@test.com",
            fund_name="test fund",
            application_reference="appref-123",
            round_name="test round",
            questions="YWJjZGVm",
            contact_help_email="contact@test.com",
            govuk_notify_reference="abc123",
        )
        assert resp == Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000004"))
        assert request_matcher.call_count == 1

    @responses.activate
    def test_send_eoi_pass_email(self, app):
        request_matcher = responses.post(
            url="https://api.notifications.service.gov.uk/v2/notifications/email",
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "email_address": "test@test.com",
                        "template_id": "04db42f4-a74e-4ab3-b9e2-565592fd6f46",
                        "personalisation": {
                            "name of fund": "COF-EOI",
                            "application reference": "app-123",
                            "date submitted": "10 February 2024 at 10:00am",
                            "round name": "test round",
                            "question": {
                                "file": "YWJjMTIz",  # base64 `abc123`
                                "filename": None,
                                "confirm_email_before_download": None,
                                "retention_period": None,
                            },
                            "full name": "Test User",
                        },
                        "reference": "abc123",
                    }
                )
            ],
            json={"id": "00000000-0000-0000-0000-000000000001"},  # partial GOV.UK Notify response
        )

        resp = get_notification_service().send_eoi_pass_email(
            "test@test.com",
            "Test User",
            language="en",
            fund_id="54c11ec2-0b16-46bb-80d2-f210e47a8791",
            fund_name="COF-EOI",
            application_reference="app-123",
            submission_date="2024-02-10T10:00:00.000000",
            round_name="test round",
            questions="YWJjMTIz",
            contact_help_email="contact@test.com",
            govuk_notify_reference="abc123",
        )
        assert resp == Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000001"))
        assert request_matcher.call_count == 1

    @responses.activate
    def test_send_eoi_pass_with_caveats_email(self, app):
        request_matcher = responses.post(
            url="https://api.notifications.service.gov.uk/v2/notifications/email",
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "email_address": "test@test.com",
                        "template_id": "705684c7-6985-4d4c-9170-08a85f47b8e1",
                        "personalisation": {
                            "name of fund": "COF-EOI",
                            "application reference": "app-123",
                            "date submitted": "10 February 2024 at 10:00am",
                            "round name": "test round",
                            "question": {
                                "file": "YWJjMTIz",  # base64 `abc123`
                                "filename": None,
                                "confirm_email_before_download": None,
                                "retention_period": None,
                            },
                            "caveats": ["a", "b", "c"],
                            "full name": "Test User",
                        },
                        "reference": "abc123",
                    }
                )
            ],
            json={"id": "00000000-0000-0000-0000-000000000002"},  # partial GOV.UK Notify response
        )

        resp = get_notification_service().send_eoi_pass_with_caveats_email(
            "test@test.com",
            "Test User",
            language="en",
            fund_id="54c11ec2-0b16-46bb-80d2-f210e47a8791",
            fund_name="COF-EOI",
            application_reference="app-123",
            submission_date="2024-02-10T10:00:00.000000",
            round_name="test round",
            questions="YWJjMTIz",
            caveats=["a", "b", "c"],
            contact_help_email="contact@test.com",
            govuk_notify_reference="abc123",
        )
        assert resp == Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000002"))
        assert request_matcher.call_count == 1

    @responses.activate
    def test_send_submit_application_email(self, app):
        request_matcher = responses.post(
            url="https://api.notifications.service.gov.uk/v2/notifications/email",
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "email_address": "test@test.com",
                        "template_id": "6adbba70-2fde-4ca7-94cb-7f7eb264efaa",
                        "personalisation": {
                            "name of fund": "COF-EOI",
                            "application reference": "app-123",
                            "date submitted": "10 February 2024 at 10:00am",
                            "round name": "test round",
                            "question": {
                                "file": "YWJjMTIz",
                                "filename": None,
                                "confirm_email_before_download": None,
                                "retention_period": None,
                            },
                            "URL of prospectus": "https://prospectus",
                            "contact email": "contact@test.com",
                        },
                        "reference": "abc123",
                    }
                )
            ],
            json={"id": "00000000-0000-0000-0000-000000000003"},  # partial GOV.UK Notify response
        )

        resp = get_notification_service().send_submit_application_email(
            "test@test.com",
            language="en",
            fund_name="COF-EOI",
            application_reference="app-123",
            submission_date="2024-02-10T10:00:00.000000",
            round_name="test round",
            questions="YWJjMTIz",
            prospectus_url="https://prospectus",
            contact_help_email="contact@test.com",
            govuk_notify_reference="abc123",
        )
        assert resp == Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000003"))
        assert request_matcher.call_count == 1
