import json
from datetime import datetime, timezone
from unittest import mock
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from click.testing import CliRunner
from fsd_utils import Decision

from application_store._helpers.application import send_submit_notification
from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.applications import Applications
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.queries.application.queries import (
    create_application,
    get_application,
    submit_application,
    update_application_fields,
)
from application_store.db.queries.form.queries import add_new_forms
from application_store.db.queries.updating.queries import update_form
from application_store.external_services.exceptions import NotificationError
from assessment_store.config.mappings.assessment_mapping_fund_round import COF_ROUND_4_W2_ID
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from assessment_store.db.models.assessment_record.enums import Status
from assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
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
def existing_json_blob():
    return {
        "forms": [
            {
                "questions": [
                    {
                        "fields": [
                            {"key": "field1", "answer": "value1"},
                            {"key": "field2", "answer": "value2"},
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def new_json_blob():
    return {
        "forms": [
            {
                "questions": [
                    {
                        "fields": [
                            {"key": "field1", "answer": "value1"},
                            {"key": "field2", "answer": "value2"},
                        ]
                    }
                ]
            }
        ]
    }


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
    assert all(k in response.json for k in ("id", "email", "reference", "eoi_decision"))

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
    assert response.json["message"] == f"Unable to submit application {application_id}"


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


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "UNCOMPETED",
        "rounds": [],
    }
)
def test_fields_resubmitted_uncompeted_application(setup_submitted_application, mocker, _db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    original_answer = test_field["answer"]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    application.project_name = "A test project for resubmission"

    _db.session.add(application)
    _db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = _db.session.get(AssessmentRecord, application_id)

    for form in resubmitted_assessment.jsonb_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                if field["key"] == test_field["key"]:
                    assert field["answer"] == test_field["answer"]
                    try:
                        datetime.fromisoformat(list(field["history_log"][0].keys())[0])
                    except ValueError:
                        raise AssertionError("History log key is not an isoformat datetime") from None
                    assert list(field["history_log"][0].values())[0] == original_answer

    assert resubmitted_assessment.project_name == application.project_name
    assert resubmitted_assessment.workflow_status == Status.CHANGE_RECEIVED


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "UNCOMPETED",
        "rounds": [],
    }
)
def test_flags_resubmitted_uncompeted_application(setup_submitted_application, _db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    application.project_name = "A test project for resubmission"

    # Another test field that isn't modified
    test_field_2 = application.forms[1].json[0]["fields"][0]

    assessor_user_id = uuid4()
    # Flag associated with changed field (should be the only one that is resolved)
    flag_update_1 = FlagUpdate(
        justification="A flag to request changes",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_1 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_1],
        field_ids=[test_field["key"]],
        is_change_request=True,
    )

    # Flag associated with a field that is unchanged
    flag_update_2 = FlagUpdate(
        justification="A flag to request changes but shouldn't get resolved",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_2 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_2],
        field_ids=[test_field_2["key"]],
        is_change_request=True,
    )

    # Flag that isn't a change request
    flag_update_3 = FlagUpdate(
        justification="A flag that isn't a change request",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_3 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_3],
        field_ids=[test_field["key"]],
        is_change_request=False,
    )

    _db.session.add(assessment_flag_1)
    _db.session.add(assessment_flag_2)
    _db.session.add(assessment_flag_3)
    _db.session.add(application)
    _db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = _db.session.get(AssessmentRecord, application_id)

    assert resubmitted_assessment.project_name == application.project_name

    updated_assessment_flags = (
        _db.session.query(AssessmentFlag)
        .filter(AssessmentFlag.application_id == application_id, AssessmentFlag.latest_status == FlagStatus.RESOLVED)
        .all()
    )
    updated_flag_updates = (
        _db.session.query(FlagUpdate)
        .join(AssessmentFlag)
        .filter(AssessmentFlag.application_id == application_id, FlagUpdate.status == FlagStatus.RESOLVED)
        .all()
    )

    assert len(updated_assessment_flags) == 2, "All flags should have been resolved"
    assert len(updated_flag_updates) == 2, "All flags update should have a resolved status"

    assert updated_assessment_flags[0].id == assessment_flag_1.id
    assert updated_flag_updates[0].user_id == application.account_id
    assert updated_flag_updates[0].assessment_flag_id == updated_assessment_flags[0].id


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "COMPETED",
        "rounds": [],
    }
)
def test_resubmitted_application_from_competed_fund(setup_submitted_application, _db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    original_answer = test_field["answer"]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    original_project_name = application.project_name
    application.project_name = "A test project for resubmission"

    _db.session.add(application)
    _db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = _db.session.get(AssessmentRecord, application_id)

    for form in resubmitted_assessment.jsonb_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                if field["key"] == test_field["key"]:
                    assert field["answer"] == original_answer
                    assert "history_log" not in field

    assert resubmitted_assessment.project_name == original_project_name


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_no_changes(existing_json_blob, new_json_blob, mock_now):
    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob)

    # Should return empty set with no changed fields
    assert changed_fields == set()

    # There should be no history logs
    for form in new_json_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                assert "history_log" not in field


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_multiple_fields_changed(existing_json_blob, new_json_blob, mock_now):
    new_json_blob["forms"][0]["questions"][0]["fields"][0]["answer"] = "changed_value1"
    new_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"] = "changed_value2"
    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob)

    assert changed_fields == {"field1", "field2"}

    f1 = new_json_blob["forms"][0]["questions"][0]["fields"][0]
    f2 = new_json_blob["forms"][0]["questions"][0]["fields"][1]
    assert "history_log" in f1
    assert "history_log" in f2

    assert len(f1["history_log"]) == 1
    assert len(f2["history_log"]) == 1


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_existing_history_log_is_appended(existing_json_blob, new_json_blob, mock_now):
    # Set up existing history log for field
    new_json_blob["forms"][0]["questions"][0]["fields"][1]["history_log"] = [
        {"2023-12-31T23:59:59+00:00": "previous_value"}
    ]
    new_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"] = "another_new_value"

    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob)

    assert changed_fields == {"field2"}

    # History log should contain both previous changes
    f2 = new_json_blob["forms"][0]["questions"][0]["fields"][1]
    assert len(f2["history_log"]) == 2

    old_val = existing_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"]
    assert list(f2["history_log"][-1].values())[0] == old_val
