import time
from typing import Optional

from flask import current_app, jsonify, request, send_file
from flask.views import MethodView
from fsd_utils import evaluate_response
from sqlalchemy.orm.exc import NoResultFound

from application_store._helpers import get_blank_forms, order_applications
from application_store._helpers.application import send_submit_notification
from application_store.db.exceptions.submit import SubmitError
from application_store.db.models.application.enums import Status
from application_store.db.queries import (
    add_new_forms,
    create_application,
    export_json_to_csv,
    export_json_to_excel,
    get_application,
    get_feedback,
    get_fund_id,
    get_general_status_applications_report,
    get_key_report_field_headers,
    get_report_for_applications,
    search_applications,
    submit_application,
    update_form,
    upsert_feedback,
)
from application_store.db.queries.application import create_qa_base64file
from application_store.db.queries.feedback import (
    retrieve_all_feedbacks_and_surveys,
    retrieve_end_of_application_survey_data,
    upsert_end_of_application_survey_data,
)
from application_store.db.queries.reporting.queries import (
    export_application_statuses_to_csv,
)
from application_store.db.queries.research import (
    retrieve_research_survey_data,
    upsert_research_survey_data,
)
from application_store.db.queries.statuses import (
    check_is_fund_round_open,
    update_statuses,
)
from application_store.external_services import (
    get_account,
    get_fund,
    get_round,
    get_round_eoi_schema,
)
from application_store.external_services.exceptions import (
    NotificationError,
)


class ApplicationsView(MethodView):
    def get(self, **kwargs):
        response_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }
        matching_applications = search_applications(**kwargs)
        order_by = kwargs.get("order_by", None)
        order_rev = kwargs.get("order_rev", None)
        sorted_applications = order_applications(matching_applications, order_by, order_rev)
        return sorted_applications, 200, response_headers

    def post(self):
        args = request.get_json()
        account_id = args["account_id"]
        round_id = args["round_id"]
        fund_id = args["fund_id"]
        language = args["language"]
        fund = get_fund(fund_id=fund_id)
        if language == "cy" and not fund.welsh_available:
            language = "en"
        empty_forms = get_blank_forms(fund_id=fund_id, round_id=round_id, language=language)
        application = create_application(
            account_id=account_id,
            fund_id=fund_id,
            round_id=round_id,
            language=language,
        )
        add_new_forms(forms=empty_forms, application_id=application.id)
        return application.as_dict(), 201

    def get_by_id(self, application_id, with_questions_file=False):
        try:
            return_dict = get_application(application_id, as_json=True, include_forms=True)
            return_dict = create_qa_base64file(return_dict, with_questions_file)
            return return_dict, 200
        except ValueError as e:
            current_app.logger.error("Value error getting application ID: {application_id}")
            raise e
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

    def get_key_application_data_report(self, application_id):
        try:
            return send_file(
                export_json_to_csv(get_report_for_applications(application_ids=[application_id])),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

    def get_applications_statuses_report(
        self,
        round_id: Optional[list] = None,
        fund_id: Optional[list] = None,
        format: Optional[str] = "csv",
    ):
        try:
            report_data = get_general_status_applications_report(
                round_id or None,
                fund_id or None,
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

        if format.lower() == "json":
            response = jsonify({"metrics": report_data})
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return send_file(
                export_application_statuses_to_csv(report_data),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )

    def get_key_applications_data_report(
        self,
        status=Status.SUBMITTED.name,
        round_id: Optional[str] = None,
        fund_id: Optional[str] = None,
    ):
        try:
            return send_file(
                export_json_to_csv(
                    get_report_for_applications(status=status, round_id=round_id, fund_id=fund_id),
                    get_key_report_field_headers(round_id),
                ),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

    def put(self):
        request_json = request.get_json(force=True)
        form_dict = {
            "application_id": request_json["metadata"]["application_id"],
            "form_name": request_json["metadata"].get("form_name"),
            "question_json": request_json["questions"],
            "is_summary_page_submit": request_json["metadata"].get("isSummaryPageSubmit", False),
        }
        try:
            updated_form = update_form(**form_dict)
            is_round_open = check_is_fund_round_open(form_dict["application_id"])
            if not is_round_open:
                current_app.logger.info("Round is closed so user will be redirected")
                return {}, 301
            return updated_form, 201
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

    def submit(self, application_id):
        should_send_email = True
        if request.args.get("dont_send_email") == "true":
            should_send_email = False

        # Do the submission
        try:
            application = submit_application(application_id)
        except SubmitError as submit_error:
            return {"message": f"Unable to submit application {submit_error.application_id}"}, 500

        # Get EOI decision
        fund_id = get_fund_id(application_id)
        round_data = get_round(fund_id, application.round_id)
        application_with_form_json = get_application(application_id, as_json=True, include_forms=True)
        if round_data.is_expression_of_interest:
            eoi_results = self.get_application_eoi_response(application_with_form_json)
            eoi_decision = eoi_results["decision"]
        else:
            eoi_results = None
            eoi_decision = None

        # Send notification
        try:
            if should_send_email:
                fund_data = get_fund(fund_id)
                account = get_account(account_id=application.account_id)
                language = application_with_form_json["language"]
                application_with_form_json_and_fund_name = {
                    **application_with_form_json,
                    "fund_name": fund_data.name_json[language],
                    "round_name": round_data.title_json[language],
                    "prospectus_url": round_data.prospectus_url,
                }

                send_submit_notification(
                    application_with_form_json=application_with_form_json,
                    eoi_results=eoi_results,
                    account=account,
                    application_with_form_json_and_fund_name=application_with_form_json_and_fund_name,
                    application=application,
                    round_data=round_data,
                )

        except NotificationError as e:
            current_app.logger.exception(
                "Notification error on sending SUBMIT notification for application {application_id}",
                exc_info=e,
                extra=dict(application_id=application_id),
            )

        return {
            "id": application_id,
            "reference": application_with_form_json["reference"],
            "email": account.email,
            "eoi_decision": eoi_decision,
        }, 201

    def post_feedback(self):
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        section_id = args["section_id"]
        feedback_json = args["feedback_json"]
        status = args["status"]

        feedback = upsert_feedback(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            section_id=section_id,
            feedback_json=feedback_json,
            status=status,
        )

        update_statuses(application_id, form_name=None)

        return feedback.as_dict(), 201

    def get_feedback_for_section(self, application_id, section_id):
        feedback = get_feedback(application_id, section_id)
        if feedback:
            return feedback.as_dict(), 200

        return {
            "code": 404,
            "message": f"Feedback not fund for {application_id}, {section_id}",
        }, 404

    def post_end_of_application_survey_data(self):
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        page_number = args["page_number"]
        data = args["data"]

        survey_data = upsert_end_of_application_survey_data(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            page_number=page_number,
            data=data,
        )

        update_statuses(application_id, form_name=None)

        return survey_data.as_dict(), 201

    def get_end_of_application_survey_data(self, application_id, page_number):
        survey_data = retrieve_end_of_application_survey_data(application_id, int(page_number))
        if survey_data:
            return survey_data.as_dict(), 200

        return {
            "code": 404,
            "message": f"End of application feedback survey data for {application_id}, {page_number} not found",
        }, 404

    def get_all_feedbacks_and_survey_report(self, **params):
        fund_id = params.get("fund_id")
        round_id = params.get("round_id")
        status = params.get("status_only")

        try:
            return send_file(
                path_or_file=export_json_to_excel(retrieve_all_feedbacks_and_surveys(fund_id, round_id, status)),
                mimetype="application/vnd.ms-excel",
                as_attachment=True,
                download_name=f"fsd_feedback_{str(int(time.time()))}.xlsx",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

    def get_application_eoi_response(self, application):
        eoi_schema = get_round_eoi_schema(application["fund_id"], application["round_id"], application["language"])
        result = evaluate_response(eoi_schema, application["forms"])
        return result

    def post_research_survey_data(self):
        """
        Endpoint to post research survey data.

        This method retrieves application_id, fund_id, round_id, and (form) data and will either
        create or update the research survey associated with that application. Finally the
        application status is checked.

        Returns:
            Research survey data in dict form and HTTP status code 201 (Created).
        """
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        data = args["data"]

        survey_data = upsert_research_survey_data(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            data=data,
        )

        update_statuses(application_id, form_name=None)

        return survey_data.as_dict(), 201

    def get_research_survey_data(self, application_id):
        """
        Endpoint to retrieve research survey data for a given application_id.

        Args:
            application_id (str): The ID of the application for which survey data is requested.

        Returns:
            If found, survey data in dict form is returned with 200 HTTP code
            Else an error message with HTTP status code 404.
        """
        survey_data = retrieve_research_survey_data(application_id)
        if survey_data:
            return survey_data.as_dict(), 200

        return {
            "code": 404,
            "message": f"Research survey data for {application_id} not found",
        }, 404
