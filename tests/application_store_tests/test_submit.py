import json
from uuid import uuid4

import pytest

from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.applications import Applications
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.queries.application.queries import create_application, submit_application
from application_store.db.queries.form.queries import add_new_forms
from application_store.db.queries.updating.queries import update_form
from application_store.external_services.exceptions import NotificationError
from assessment_store.config.mappings.assessment_mapping_fund_round import COF_ROUND_4_W2_ID
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from tests.assessment_store_tests.test_assessment_mapping_fund_round import COF_FUND_ID


@pytest.fixture
def mock_successful_location_call(mocker):
    mocker.patch(
        "assessment_store.db.queries.assessment_records._helpers.get_location_json_from_postcode",
        return_value={
            "error": False,
            "postcode": "GU1 1LY",
            "county": "Hampshire",
            "region": "England",
            "country": "England",
            "constituency": "Guildford",
        },
    )


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


@pytest.fixture
def setup_completed_application(
    _db,
    app,
    clear_test_data,
    mocker,
):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])
    with open("tests/application_store_tests/seed_data/COF_R4W2_all_forms.json", "r") as f:
        cof_application = json.load(f)
        forms = cof_application["forms"]
    empty_forms = [form["name"] for form in forms]
    target_application = create_application(
        account_id=uuid4(), fund_id=COF_FUND_ID, round_id=COF_ROUND_4_W2_ID, language="en"
    )
    target_application.project_name = "test"
    application_id = target_application.id
    add_new_forms(forms=empty_forms, application_id=application_id)

    for form in forms:
        update_form(
            application_id,
            form["name"],
            form["questions"],
            True,
        )
    yield application_id


def test_submit_application_with_location_bad_key(
    _db, monkeypatch, setup_completed_application, mock_successful_location_call
):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "badkey",
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    application_id = setup_completed_application

    submit_application(application_id)
    assessment_record: AssessmentRecord = (
        _db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.location_json_blob
    assert assessment_record.location_json_blob["error"] is True


def test_submit_application_with_location(_db, setup_completed_application, monkeypatch, mock_successful_location_call):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "EfdliG",
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )

    application_id = setup_completed_application

    submit_application(application_id)
    assessment_record: AssessmentRecord = (
        _db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.location_json_blob
    assert assessment_record.location_json_blob["error"] is False
    assert assessment_record.location_json_blob["county"] == "Hampshire"


def test_submit_route_success(
    flask_test_client,
    mock_successful_submit_notification,
    _db,
    seed_application_records,
    mocker,
    mock_get_fund_data,
    mock_get_round,
    mock_data_key_mappings,
    mock_successful_location_call,
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


def test_submit_route_submit_error(flask_test_client, seed_application_records, mocker, mock_successful_location_call):
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


def test_submit_application_raises_error_on_db_violation(
    seed_application_records, mocker, _db, mock_data_key_mappings, mock_successful_location_call
):
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
    seed_application_records, mocker, _db, flask_test_client, mock_data_key_mappings, mock_successful_location_call
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
