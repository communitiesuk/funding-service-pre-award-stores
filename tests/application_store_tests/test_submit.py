import json
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from click.testing import CliRunner
from fsd_utils import Decision

from application_store._helpers.application import send_submit_notification
from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.applications import Applications
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.queries.application.queries import create_application, submit_application
from application_store.db.queries.form.queries import add_new_forms
from application_store.db.queries.updating.queries import update_form
from application_store.external_services.exceptions import NotificationError
from assessment_store.config.mappings.assessment_mapping_fund_round import COF_ROUND_4_W2_ID
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from assessment_store.scripts.derive_assessment_values import derive_assessment_values
from tests.assessment_store_tests.test_assessment_mapping_fund_round import COF_FUND_ID


@pytest.fixture
def mock_get_files(mocker):
    mocker.patch("application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])


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
def setup_completed_application(_db, app, clear_test_data, mocker, mock_get_files):
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
    _db,
    monkeypatch,
    setup_completed_application,
    mock_successful_location_call,
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
    mock_get_files,
):
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
    seed_application_records, mocker, _db, mock_data_key_mappings, mock_successful_location_call, mock_get_files
):
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
    seed_application_records,
    mocker,
    _db,
    flask_test_client,
    mock_data_key_mappings,
    mock_get_files,
    mock_successful_location_call,
):
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


@pytest.mark.parametrize("eoi_result", [({"decision": "BAD_VALUE"}), ({"decision": Decision.FAIL})])
def test_send_submit_notification_do_not_send(mocker, app, mock_get_files, eoi_result):
    mocker.patch("application_store._helpers.application.create_qa_base64file", return_value={"forms": []})
    mock_notifier = mocker.patch("application_store._helpers.application.Notification.send")
    send_submit_notification(
        application={},
        eoi_results=eoi_result,
        account=MagicMock(),
        application_with_form_json={},
        application_with_form_json_and_fund_name={},
        round_data=MagicMock(),
    )
    mock_notifier.assert_not_called()


@pytest.mark.parametrize(
    "eoi_result, exp_template, exp_contents",
    [
        (
            None,
            "APPLICATION_RECORD_OF_SUBMISSION",
            {
                "application": {},
                "contact_help_email": "contact@test.com",
            },
        ),
        (
            {"decision": Decision.PASS},
            "Full pass",
            {
                "application": {},
                "contact_help_email": "contact@test.com",
            },
        ),
        (
            {"decision": Decision.PASS_WITH_CAVEATS, "caveats": ["a", "b", "c"]},
            "Pass with caveats",
            {"application": {}, "contact_help_email": "contact@test.com", "caveats": ["a", "b", "c"]},
        ),
    ],
)
def test_send_submit_notification(mocker, app, mock_get_files, eoi_result, exp_template, exp_contents):
    mocker.patch("application_store._helpers.application.create_qa_base64file", return_value={"forms": []})
    mock_notifier = mocker.patch("application_store._helpers.application.Notification.send")
    mock_account = MagicMock()
    mock_account.email = "test@test.com"
    mock_account.full_name = "Test User"
    mock_round = MagicMock()
    mock_round.contact_email = "contact@test.com"
    send_submit_notification(
        application={},
        eoi_results=eoi_result,
        account=mock_account,
        application_with_form_json={},
        application_with_form_json_and_fund_name={},
        round_data=mock_round,
    )
    mock_notifier.assert_called_once()
    mock_notifier.assert_called_with(
        exp_template,
        "test@test.com",
        "Test User",
        exp_contents,
    )


@pytest.fixture
def setup_submitted_application(_db, setup_completed_application, monkeypatch, mock_successful_location_call):
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

    application_id = setup_completed_application

    submit_application(application_id)
    yield application_id


def test_derive_values_script(
    setup_submitted_application, _db, monkeypatch, mock_data_key_mappings, mock_successful_location_call
):
    application_id = str(setup_submitted_application)
    assessment_record: AssessmentRecord = _db.session.get(AssessmentRecord, application_id)
    assert assessment_record.asset_type == "No asset type specified."
    assert assessment_record.funding_amount_requested == 0
    assert assessment_record.location_json_blob == {
        "error": False,
        "postcode": "Not Available",
        "county": "Not Available",
        "region": "Not Available",
        "country": "Not Available",
        "constituency": "Not Available",
    }

    runner = CliRunner()

    # setup data mappings so running the script will change values
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "EfdliG",
            "asset_type": "oXGwlA",
            "funding_one": "ABROnB",
            "funding_two": ["tSKhQQ", "UyaAHw"],
            "funding_field_type": "multiInputField",
        }
    }
    monkeypatch.setattr(
        "assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )

    # call script and say not confirmation prompt (no commit)
    result = runner.invoke(derive_assessment_values, ["-a", application_id], input="n")
    assert result.exit_code == 0
    assessment_record_2: AssessmentRecord = _db.session.get(AssessmentRecord, application_id)
    assert assessment_record_2.asset_type == "No asset type specified."
    assert assessment_record_2.funding_amount_requested == 0
    assert assessment_record_2.location_json_blob == {
        "error": False,
        "postcode": "Not Available",
        "county": "Not Available",
        "region": "Not Available",
        "country": "Not Available",
        "constituency": "Not Available",
    }

    # Call script again but yes to prompt (commit == True)
    result = runner.invoke(derive_assessment_values, ["-a", application_id], input="y")
    assert result.exit_code == 0
    assessment_record_2: AssessmentRecord = _db.session.get(AssessmentRecord, application_id)
    assert assessment_record_2.asset_type == "cinema"
    assert assessment_record_2.funding_amount_requested == 1524
    assert assessment_record_2.location_json_blob["error"] is False
    assert assessment_record_2.location_json_blob["county"] == "Hampshire"
