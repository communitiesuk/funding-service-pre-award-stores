from flask import redirect, render_template, request, url_for

from common.blueprints import Blueprint
from proto.common.data.services.applications import (
    get_application,
    get_application_section_data,
    set_application_section_complete,
    upsert_question_data,
)
from proto.common.data.services.question_bank import get_application_question
from proto.form_runner.forms import MarkAsCompleteForm, build_question_form

runner_blueprint = Blueprint("proto_form_runner", __name__)


@runner_blueprint.get("/application/<application_id>")
def application_tasklist(application_id):
    application = get_application(application_id)
    return render_template("form_runner/application_tasklist.html", application=application)


def _next_url_for_question(application_id, section, current_question_slug):
    question_slugs = [question.slug for question in section.questions]
    curr_index = question_slugs.index(current_question_slug)
    if curr_index == len(question_slugs) - 1:
        # TODO: section could have an attribute to toggle on/off 'show check-your-answers' page
        return url_for("proto_form_runner.check_your_answers", application_id=application_id, section_slug=section.slug)

    return url_for(
        "proto_form_runner.ask_application_question",
        application_id=application_id,
        section_slug=section.slug,
        question_slug=question_slugs[curr_index + 1],
    )


@runner_blueprint.route("/application/<application_id>/<section_slug>/<question_slug>", methods=["GET", "POST"])
def ask_application_question(application_id, section_slug, question_slug):
    application = get_application(application_id)
    question = get_application_question(application.round_id, section_slug, question_slug)
    form = build_question_form(application, question)
    if form.validate_on_submit():
        upsert_question_data(application, question, form.question.data)
        if "from_cya" in request.args:
            return redirect(
                url_for(
                    "proto_form_runner.check_your_answers", application_id=application_id, section_slug=section_slug
                )
            )
        return redirect(_next_url_for_question(application_id, question.section, question_slug))

    return render_template(
        "form_runner/question_page.html",
        application=application,
        question=question,
        section=question.section,
        form=form,
    )


@runner_blueprint.route("/application/<application_id>/<section_slug>/check-your-answers", methods=["GET", "POST"])
def check_your_answers(application_id, section_slug):
    section_data = get_application_section_data(application_id, section_slug)
    form = MarkAsCompleteForm()
    if form.validate_on_submit():
        if form.complete.data == "yes":
            set_application_section_complete(section_data)

        return redirect(url_for("proto_form_runner.application_tasklist", application_id=application_id))
    return render_template(
        "form_runner/check_your_answers.html",
        application_id=application_id,
        section=section_data.section,
        section_data=section_data,
        form=form,
    )
