import pytest

from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.applications import Applications
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.queries.application.queries import submit_application
from application_store.external_services.exceptions import NotificationError
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord


@pytest.fixture(scope="function")
def mock_data_key_mappings(monkeypatch):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": None,
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    yield


def test_submit_route_success(
    flask_test_client,
    mock_successful_submit_notification,
    _db,
    seed_application_records,
    mocker,
    mock_get_fund_data,
    mock_get_round,
    mock_data_key_mappings,
):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    application_id = target_application.id
    target_application.project_name = "unit test project"

    _db.session.add(target_application)
    _db.session.commit()

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )

    assert response.status_code == 201
    assert all(k in response.json() for k in ("id", "email", "reference", "eoi_decision"))

    _db.session.expunge(target_application)
    application_after_submit = _db.session.query(Applications).where(Applications.id == application_id).one()

    assert application_after_submit.status == ApplicationStatus.SUBMITTED

    assessment_record: AssessmentRecord = (
        _db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.jsonb_blob["forms"]


def test_submit_route_submit_error(
    flask_test_client,
    seed_application_records,
    mocker,
):
    target_application = seed_application_records[0]
    application_id = target_application.id
    mocker.patch(
        "application_store.api.routes.application.routes.submit_application",
        side_effect=SubmitError(application_id=application_id),
    )

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )
    assert response.status_code == 500
    assert response.json()["message"] == f"Unable to submit application {application_id}"


def test_submit_application_raises_error_on_db_violation(seed_application_records, mocker, _db, mock_data_key_mappings):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    target_application.project_name = None  # will cause not null constraint violation

    _db.session.add(target_application)
    _db.session.commit()
    application_id = target_application.id
    with pytest.raises(SubmitError) as se:
        submit_application(application_id)
    assert type(se.value) is SubmitError
    assert str(se.value).startswith(f"Unable to submit application [{application_id}]")


def test_submit_application_route_succeeds_on_notify_error(
    seed_application_records, mocker, _db, flask_test_client, mock_data_key_mappings
):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    application_id = target_application.id
    target_application.project_name = "unit test project"

    _db.session.add(target_application)
    _db.session.commit()

    mocker.patch(
        "application_store.api.routes.application.routes.send_submit_notification",
        side_effect=NotificationError(),
    )

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )
    assert response.status_code == 201
