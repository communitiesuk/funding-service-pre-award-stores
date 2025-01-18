from unittest.mock import MagicMock

import pytest

from apply.helpers import get_change_requests
from assessment_store.db.models.flags.flag_update import FlagStatus


@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch("apply.helpers.db.session.scalar")


def test_no_assessment_record(mock_db_session):
    mock_db_session.return_value = None
    result = get_change_requests("non_existent_application_id")

    assert result == {}


def test_no_change_requests(mock_db_session):
    assessment_record = MagicMock()
    assessment_record.change_requests = []
    mock_db_session.return_value = assessment_record
    result = get_change_requests("application_id")

    assert result == {}


def test_no_valid_updates(mock_db_session):
    change_request = MagicMock()
    change_request.field_ids = ["field1"]
    change_request.updates = [MagicMock(status=FlagStatus.RAISED, justification="justification1")]

    assessment_record = MagicMock()
    assessment_record.change_requests = [change_request]
    mock_db_session.return_value = assessment_record

    result = get_change_requests("application_id")

    assert result == {"field1": []}


def test_valid_updates(mock_db_session):
    change_request = MagicMock()
    change_request.field_ids = ["field1"]
    change_request.updates = [
        MagicMock(status=FlagStatus.RESOLVED, justification="justification1"),
        MagicMock(status=FlagStatus.RESOLVED, justification="justification2"),
        MagicMock(status=FlagStatus.RAISED, justification="justification3"),
    ]

    assessment_record = MagicMock()
    assessment_record.change_requests = [change_request]
    mock_db_session.return_value = assessment_record

    result = get_change_requests("application_id")

    assert result == {"field1": ["justification1", "justification2"]}


def test_multiple_change_requests_and_field_ids(mock_db_session):
    change_request1 = MagicMock()
    change_request1.field_ids = ["field1", "field2"]
    change_request1.updates = [
        MagicMock(status=FlagStatus.RESOLVED, justification="justification1"),
        MagicMock(status=FlagStatus.RESOLVED, justification="justification2"),
    ]

    change_request2 = MagicMock()
    change_request2.field_ids = ["field1"]
    change_request2.updates = [MagicMock(status=FlagStatus.RESOLVED, justification="justification3")]

    assessment_record = MagicMock()
    assessment_record.change_requests = [change_request1, change_request2]
    mock_db_session.return_value = assessment_record

    result = get_change_requests("application_id")

    assert result == {
        "field1": ["justification1", "justification2", "justification3"],
        "field2": ["justification1", "justification2"],
    }
