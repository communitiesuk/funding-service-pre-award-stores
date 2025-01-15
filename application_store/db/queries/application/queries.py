import base64
import random
import string
from datetime import datetime, timezone
from io import BytesIO
from itertools import groupby
from typing import Optional

from flask import current_app
from fsd_utils import extract_questions_and_answers, generate_text_of_application
from sqlalchemy import exc, func, select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, load_only, noload
from sqlalchemy.sql.expression import Select

from application_store.db.exceptions import ApplicationError, SubmitError
from application_store.db.models import Applications
from application_store.db.models.application.enums import Status as ApplicationStatus
from application_store.db.schemas import ApplicationSchema
from application_store.external_services import get_fund, get_round
from application_store.external_services.aws import FileData, list_files_by_prefix
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from assessment_store.db.models.assessment_record.enums import Status as WorkflowStatus
from assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
from assessment_store.db.queries.assessment_records._helpers import derive_application_values
from config import Config
from db import db


def get_application(app_id, include_forms=False, as_json=False) -> dict | Applications:
    stmt: Select = select(Applications).filter(Applications.id == app_id)

    if include_forms:
        stmt.options(joinedload(Applications.forms))
        serialiser = ApplicationSchema()
    else:
        stmt.options(noload(Applications.forms))
        serialiser = ApplicationSchema(exclude=["forms"])

    row: Applications = db.session.scalars(stmt).unique().one()

    if as_json:
        json_row = serialiser.dump(row)
        return json_row
    else:
        return row


def get_applications(filters=None, include_forms=False, as_json=False) -> list[dict] | list[Applications]:
    if filters is None:
        filters = []
    stmt: Select = select(Applications)

    if len(filters) > 0:
        stmt = stmt.where(*filters)

    if include_forms:
        stmt = stmt.options(joinedload(Applications.forms))
        serialiser = ApplicationSchema()
    else:
        stmt = stmt.options(noload(Applications.forms))
        serialiser = ApplicationSchema(exclude=["forms"])

    rows: Applications = db.session.scalars(stmt).unique().all()

    if as_json:
        return [serialiser.dump(row) for row in rows]
    else:
        return rows


def get_application_status(app_id):
    application = get_application(app_id)
    return application.status


def random_key_generator(length: int = 6):
    key = "".join(random.choices(string.ascii_uppercase, k=length))
    while True:
        yield key


def _create_application_try(account_id, fund_id, round_id, key, language, reference, attempt) -> Applications:
    try:
        new_application_row = Applications(
            account_id=account_id,
            fund_id=fund_id,
            round_id=round_id,
            key=key,
            language=language,
            reference=reference,
        )
        db.session.add(new_application_row)
        db.session.commit()
        return new_application_row
    except IntegrityError:
        db.session.remove()
        current_app.logger.error(
            "Failed %(attempt)s attempt(s) to create application with"
            " application reference %(reference)s, for fund_id"
            " %(fund_id)s and round_id %(round_id)s",
            dict(attempt=attempt, reference=reference, fund_id=fund_id, round_id=round_id),
        )


def create_application(account_id, fund_id, round_id, language) -> Applications:
    fund = get_fund(fund_id)
    fund_round = get_round(fund_id, round_id)
    application_start_language = language
    if language == "cy" and not fund.welsh_available:
        application_start_language = "en"
    if fund and fund_round and fund.short_name and fund_round.short_name:
        new_application = None
        max_tries = 10
        attempt = 0
        key = None
        app_key_gen = random_key_generator()
        while attempt < max_tries and new_application is None:
            key = next(app_key_gen)
            new_application = _create_application_try(
                account_id=account_id,
                fund_id=fund_id,
                round_id=round_id,
                key=key,
                language=application_start_language,
                reference="-".join([fund.short_name, fund_round.short_name, key]),
                attempt=attempt,
            )
            attempt += 1

        if not new_application:
            raise ApplicationError(
                f"Max ({max_tries}) tries exceeded for create application"
                f" with application key {key}, for fund.short_name"
                f" {fund.short_name} and round.short_name"
                f" {fund_round.short_name}"
            )
        return new_application
    else:
        raise ApplicationError(f"Failed to create application. Fund round {round_id} for fund {fund_id} not found")


def get_all_applications() -> list:
    application_list = db.session.query(Applications).all()
    return application_list


def get_count_by_status(round_ids: Optional[list] = None, fund_ids: Optional[list] = None) -> dict[str, int]:
    query = db.session.query(
        Applications.fund_id,
        Applications.round_id,
        Applications.status,
        func.count(Applications.status),
    )

    if round_ids:
        query = query.filter(Applications.round_id.in_(round_ids))
    if fund_ids:
        query = query.filter(Applications.fund_id.in_(fund_ids))

    grouped_by_fund_round_result = (
        query.group_by(Applications.fund_id).group_by(Applications.round_id).group_by(Applications.status).all()
    )
    results = []
    unique_funds = {f[0] for f in grouped_by_fund_round_result}.union(fund_ids or [])
    for fund_id in unique_funds:
        unique_rounds = {row[1] for row in grouped_by_fund_round_result if row[0] == fund_id}.union(round_ids or [])
        rounds = []
        for round_id in unique_rounds:
            this_round_statuses = {
                s[2].name: s[3] for s in grouped_by_fund_round_result if s[0] == fund_id and s[1] == round_id
            }
            rounds.append(
                {
                    "round_id": round_id,
                    "application_statuses": {
                        **{s.name: 0 for s in ApplicationStatus},
                        **this_round_statuses,
                    },
                }
            )
        results.append({"fund_id": fund_id, "rounds": rounds})
    return results


def create_qa_base64file(application_data: dict, with_questions_file: bool):
    """
    If the query param with_questions_file is True then it will get the application questions ans answers,
    and then it will generate a formatted text document for an application with questions and answers.
    and this file will be base64 encoded.
    """
    if with_questions_file:
        fund_details = get_fund(application_data["fund_id"])
        q_and_a = extract_questions_and_answers(application_data["forms"], application_data["language"])
        contents = BytesIO(
            bytes(
                generate_text_of_application(q_and_a, fund_details.name, application_data["language"]),
                "utf-8",
            )
        ).read()
        if len(contents) > Config.DOCUMENT_UPLOAD_SIZE_LIMIT:
            raise ValueError("File is larger than 2MB")
        application_data = {
            **application_data,
            "questions_file": base64.b64encode(contents).decode("ascii"),
        }
        current_app.logger.info("Sending the Q and A base64 encoded file with the response")
    return application_data


def search_applications(**params):
    """
    Returns a list of applications matching required params
    """
    # datetime_start = params.get("datetime_start")
    # datetime_end = params.get("datetime_end")
    fund_id = params.get("fund_id")
    round_id = params.get("round_id")
    account_id = params.get("account_id")
    status_only = params.get("status_only")
    application_id = params.get("application_id")
    forms = params.get("forms")

    filters = []
    if fund_id:
        filters.append(Applications.fund_id == fund_id)
    if round_id:
        filters.append(Applications.round_id == round_id)
    if account_id:
        filters.append(Applications.account_id == account_id)
    if status_only:
        if " " in status_only:
            status_only = status_only.replace(" ", "_")
        if isinstance(status_only, list):
            filters.append(Applications.status.in_(status_only))
        else:
            filters.append(Applications.status == status_only)
    if application_id:
        filters.append(Applications.id == application_id)
    found_apps = get_applications(filters, include_forms=forms, as_json=True)
    return found_apps


def update_application_fields(existing_json_blob, new_json_blob) -> set:
    field_map = {}
    changed_fields = set()
    for form in existing_json_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                field_map[field["key"]] = field["answer"]

    for form in new_json_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                if field["answer"] != field_map.get(field["key"]):
                    changed_fields.add(field["key"])
                    if "history_log" in field:
                        field["history_log"].append(
                            {datetime.now(tz=timezone.utc).isoformat(): field_map[field["key"]]}
                        )
                    else:
                        field["history_log"] = [{datetime.now(tz=timezone.utc).isoformat(): field_map[field["key"]]}]

    return changed_fields


def submit_application(application_id) -> Applications:  # noqa: C901
    current_app.logger.info(
        "Submitting application %(application_id)s and importing to assessment store",
        dict(application_id=application_id),
    )
    try:
        application = get_application(application_id, include_forms=True)
        fund = get_fund(application.fund_id)
        all_application_files = list_files_by_prefix(application_id)
        application = process_files(application, all_application_files)

        # Mark the application as submitted
        application.date_submitted = datetime.now(timezone.utc)
        application.status = ApplicationStatus.SUBMITTED

        application_type = "".join(application.reference.split("-")[:1])

        application_as_dict = get_application(application_id, include_forms=True, as_json=True)

        derived_values = derive_application_values(application_as_dict)

        row = {
            **derived_values,
            "jsonb_blob": ApplicationSchema().dump(application),
            "type_of_application": application_type,
        }

        existing_application = db.session.scalar(
            select(AssessmentRecord)
            .where(
                AssessmentRecord.application_id == row["application_id"],
                AssessmentRecord.is_withdrawn.is_(False),
            )
            .options(load_only(AssessmentRecord.jsonb_blob))
        )

        if existing_application and fund.funding_type == "UNCOMPETED":
            # For uncompeted funds, the application may already exist and this may be a resubmission.

            # updating row json blob
            update_application_fields(existing_application.jsonb_blob, row["jsonb_blob"])
            row["workflow_status"] = WorkflowStatus.CHANGE_RECEIVED

            stmt = postgres_insert(AssessmentRecord).values(row)

            # setting with an update makes sure the derived values are recalculated
            update_row_statement = stmt.on_conflict_do_update(
                index_elements=[AssessmentRecord.application_id], set_=row
            ).returning(AssessmentRecord.application_id)

            db.session.execute(update_row_statement)

            change_requests = existing_application.change_requests
            for change_request in change_requests:
                flag_update = FlagUpdate(
                    justification="Applicant updated their submission",
                    status=FlagStatus.RESOLVED,
                    assessment_flag_id=change_request.id,
                    user_id=application.account_id,
                )
                change_request.updates.append(flag_update)
                change_request.latest_status = flag_update.status
                db.session.add(change_request)

            db.session.commit()
        else:
            stmt = postgres_insert(AssessmentRecord).values([row])

            upsert_rows_stmt = stmt.on_conflict_do_nothing(index_elements=[AssessmentRecord.application_id]).returning(
                AssessmentRecord.application_id
            )

            result = db.session.execute(upsert_rows_stmt)

            # Check if the inserted application is in result
            inserted_application_ids = [item.application_id for item in result]
            if not len(inserted_application_ids):
                current_app.logger.warning(
                    "Application already exists in the database: %(app_id)s", dict(app_id=row["application_id"])
                )
            else:
                current_app.logger.info(
                    "Successfully inserted application: %(app_id)s", dict(app_id=row["application_id"])
                )
            db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.exception(
            "Error occurred while submitting application %(application_id)s}",
            dict(application_id=row["application_id"]),
        )
        raise SubmitError(application_id=application_id) from e

    return application


def process_files(application: Applications, all_files: list[FileData]) -> Applications:
    comp_id_to_files = {comp_id: list(files) for comp_id, files in groupby(all_files, key=lambda x: x.component_id)}
    for form in application.forms:
        for component in form.json:
            for field in component["fields"]:
                comp_id = field["key"]
                if files := comp_id_to_files.get(comp_id):
                    field["answer"] = ", ".join(state.filename for state in files)
    return application


def update_project_name(form_name, question_json, application) -> None:
    if form_name.startswith("project-information") or form_name.startswith("gwybodaeth-am-y-prosiect"):
        for question in question_json:
            for field in question["fields"]:
                # field id for project name in json
                if field["title"] == "Project name":
                    try:
                        application.project_name = field["answer"]
                    except KeyError:
                        current_app.logger.info("Project name was not edited")
                        continue


def get_fund_id(application_id):
    """Function takes an application_id and returns the fund_id of that application."""
    try:
        application = db.session.query(Applications).filter_by(id=application_id).first()
        if application:
            return application.fund_id
        else:
            return None
    except Exception:
        current_app.logger.error(
            "Incorrect application id: %(application_id)s",
            dict(application_id=application_id),
        )
        return None


def attempt_to_find_and_update_project_name(question_json, application) -> None:
    """
    Updates the applications project name if the updated question_json
    contains a field_id match on the pre-configured project_name field_id.
    """
    round = get_round(application.fund_id, application.round_id)
    project_name_field_id = round.project_name_field_id

    for question in question_json:
        for field in question["fields"]:
            if field["key"] == project_name_field_id and "answer" in field.keys():
                return field["answer"]
