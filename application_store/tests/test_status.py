from tests.helpers import expected_data_within_get_response
from tests.helpers import expected_data_within_put_response


def test_update_status_response(flask_test_client):
    """_summary_: Function sends an application_id
    as endpoint AND question & status as args
    & returns expected output

    Args:
        flask_test_client
    """
    # Test get respose with GET request for NOT STARTED & COMPLETED
    expected_data_NOT_STARTED = {"Q1": "NOT STARTED", "Q2": "COMPLETED"}
    expected_data_within_get_response(
        flask_test_client,
        "/fund/status/uuidv4",
        expected_data_NOT_STARTED,
        debug=True,
    )

    # Test get respose with PUT & GET request for IN PROGRESS & COMPLETED
    expected_data_IN_PROGRESS = {"Q1": "IN PROGRESS", "Q2": "COMPLETED"}
    expected_data_within_put_response(
        flask_test_client,
        "/fund/status/uuidv4" + "?new_status=IN PROGRESS&question_name=Q1",
    )
    expected_data_within_get_response(
        flask_test_client,
        "/fund/status/uuidv4",
        expected_data_IN_PROGRESS,
        debug=True,
    )

    # Test get respose with get request for COMPLETED & COMPLETED
    expected_data_COMPLETED = {"Q1": "COMPLETED", "Q2": "COMPLETED"}
    expected_data_within_put_response(
        flask_test_client,
        "/fund/status/uuidv4" + "?new_status=COMPLETED&question_name=Q1",
    )
    expected_data_within_get_response(
        flask_test_client,
        "/fund/status/uuidv4",
        expected_data_COMPLETED,
        debug=True,
    )
