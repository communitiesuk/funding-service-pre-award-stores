from copy import deepcopy
from datetime import datetime
from unittest.mock import patch

from fsd_test_utils.test_config.useful_config import UsefulConfig

from db.models.event import EventType


def test_get_fund_by_id(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/123")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Fund Name 1"


def test_get_fund_by_short_name(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/ABC?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Fund Name 1"


def test_get_round_by_short_name(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/FND1/rounds/RND1?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 1"


def test_get_eoi_decision_schema(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/FND1/rounds/RND1/eoi_decision_schema?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result == {}


def test_get_round_by_id(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/FND1/rounds/RND1")
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 1"
    assert "eoi_decision_schema" not in result


def test_get_round_by_bad_id(flask_test_client, mocker):
    mocker.patch("api.routes.get_round_by_id", return_value=None)
    response = flask_test_client.get("/funds/FND1/rounds/RND1")
    assert response.status_code == 404


def test_get_eoi_decision_schema_bad_id(flask_test_client, mocker):
    mocker.patch("api.routes.get_round_by_id", return_value=None)
    response = flask_test_client.get("/funds/xxxxx/rounds/xxxxx/eoi_decision_schema")
    assert response.status_code == 404


def test_get_all_funds(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds")
    assert response.status_code == 200
    result = response.json
    assert result[0]["name"] == "Fund Name 1"


def test_get_all_funds_no_data(flask_test_client, mocker):
    mocker.patch("api.routes.get_all_funds", return_value=[])
    response = flask_test_client.get("/funds")
    assert response.status_code == 200


def test_get_app_sections_for_round(flask_test_client, mock_get_sections):
    response = flask_test_client.get(
        f"/funds/{UsefulConfig.COF_FUND_ID}/rounds/{UsefulConfig.COF_ROUND_2_ID}/sections/application"
    )
    assert response.status_code == 200
    result = response.json
    assert result[0]["title"] == "Top"


def test_get_assess_sections_for_round(flask_test_client, mock_get_sections):
    response = flask_test_client.get(
        f"/funds/{UsefulConfig.COF_FUND_ID}/rounds/{UsefulConfig.COF_ROUND_2_ID}/sections/assessment"
    )
    assert response.status_code == 200
    result = response.json
    assert result[0]["title"] == "Top"


def test_get_events_for_round(flask_test_client):
    mock_events = [
        {
            "id": "1",
            "round_id": "9",
            "type": EventType.APPLICATION_DEADLINE_REMINDER,
            "activation_date": datetime(2000, 10, 1),
            "processed": None,
        },
        {
            "id": "2",
            "round_id": "9",
            "type": EventType.APPLICATION_DEADLINE_REMINDER,
            "activation_date": datetime(2001, 7, 8),
            "processed": datetime(2001, 8, 8),
        },
    ]

    expected_response = deepcopy(mock_events)
    for response in expected_response:
        response["activation_date"] = response["activation_date"].isoformat()
        response["processed"] = response["processed"].isoformat() if response["processed"] else None
        response["type"] = response["type"].value
    with patch(
        "api.routes.get_events_for_round_from_db", return_value=mock_events
    ) as mock_get_events_for_round_from_db:
        response = flask_test_client.get("/funds/some_fund_id/rounds/some_round_id/events?only_unprocessed=true")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_events_for_round_from_db.assert_called_once_with(round_id="some_round_id", only_unprocessed=True)


def test_get_events_for_round_not_found(flask_test_client):
    with patch("api.routes.get_events_for_round_from_db", return_value=None) as mock_get_events_for_round_from_db:
        response = flask_test_client.get("/funds/some_fund_id/rounds/some_round_id/events")

        assert response.status_code == 404
        mock_get_events_for_round_from_db.assert_called_once_with(round_id="some_round_id", only_unprocessed=False)


def test_get_event(flask_test_client):
    mock_event = {
        "id": "1",
        "round_id": "9",
        "type": EventType.APPLICATION_DEADLINE_REMINDER,
        "activation_date": datetime(2000, 10, 1),
        "processed": None,
    }
    expected_response = deepcopy(mock_event)
    expected_response["activation_date"] = expected_response["activation_date"].isoformat()
    expected_response["processed"] = (
        expected_response["processed"].isoformat() if expected_response["processed"] else None
    )
    expected_response["type"] = expected_response["type"].value
    with patch("api.routes.get_event_from_db", return_value=mock_event) as mock_get_event_from_db:
        response = flask_test_client.get("/funds/some_fund_id/rounds/some_round_id/event/123")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_event_from_db.assert_called_once_with(round_id="some_round_id", event_id="123")


def test_get_event_not_found(flask_test_client):
    with patch("api.routes.get_event_from_db", return_value=None) as mock_get_events_for_round_from_db:
        response = flask_test_client.get("/funds/some_fund_id/rounds/some_round_id/event/123")

        assert response.status_code == 404
        mock_get_events_for_round_from_db.assert_called_once_with(round_id="some_round_id", event_id="123")


def test_set_event_to_processed(flask_test_client):
    mock_event = {
        "id": "1",
        "round_id": "9",
        "type": EventType.APPLICATION_DEADLINE_REMINDER,
        "activation_date": datetime(2000, 10, 1),
        "processed": datetime(2000, 11, 1),
    }
    expected_response = deepcopy(mock_event)
    expected_response["activation_date"] = expected_response["activation_date"].isoformat()
    expected_response["type"] = expected_response["type"].value
    expected_response["processed"] = expected_response["processed"].isoformat()
    with patch("api.routes.set_event_to_processed_in_db", return_value=mock_event) as mock_set_event_to_processed_in_db:
        response = flask_test_client.put("/funds/some_fund_id/rounds/some_round_id/event/123?processed=true")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_set_event_to_processed_in_db.assert_called_once_with(
            round_id="some_round_id", event_id="123", processed=True
        )
