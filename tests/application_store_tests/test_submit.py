import pytest

from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.applications import Applications
from application_store.db.models.application.enums import Language
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.queries.application.queries import submit_application
from application_store.external_services.exceptions import NotificationError
from assessment_store.config.mappings.assessment_mapping_fund_round import CTDF_FUND_ID, CTDF_ROUND_1_ID
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord


@pytest.mark.apps_to_insert(
    [
        {
            "account_id": "usera",
            "fund_id": CTDF_FUND_ID,
            "round_id": CTDF_ROUND_1_ID,
            "language": Language.en,
        },
    ]
)
def test_submit_route_success(
    flask_test_client,
    mock_successful_submit_notification,
    _db,
    seed_application_records,
    mocker,
    mock_get_fund_data,
    mock_get_round,
):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    application_id = target_application.id
    # project_info_form = next(form for form in target_application.forms if form.name == "project-information")
    # project_info_form.json = [
    #     {
    #         "category": "FabDefault",
    #         "question": "Project name",
    #         "fields": [{"key": "VcyKVN", "title": "Project name", "type": "text", "answer": "unit test"}],
    #         "status": "COMPLETED",
    #     },
    # ]

    # Update reference to a fund that has data mappings in assess
    target_application.reference = "CTDF-CR1-" + seed_application_records[0].reference.split("-")[2]
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

    assessment_record = (
        _db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record


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


def test_submit_application_raises_error_on_db_violation(seed_application_records, mocker, _db):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    target_application.reference = "CTDF-CR1-" + seed_application_records[0].reference.split("-")[2]
    target_application.project_name = None  # will cause not null constraint violation

    _db.session.add(target_application)
    _db.session.commit()
    application_id = target_application.id
    with pytest.raises(SubmitError) as se:
        submit_application(application_id)
        assert str(se) == f"Unable to submit application {application_id}"


def test_submit_application_route_succeeds_on_notify_error(seed_application_records, mocker, _db, flask_test_client):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    target_application = seed_application_records[0]
    application_id = target_application.id
    target_application.reference = "CTDF-CR1-" + seed_application_records[0].reference.split("-")[2]
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
