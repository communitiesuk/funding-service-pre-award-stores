import datetime

from flask import redirect, render_template, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.services.grants import create_grant, get_all_grants_with_rounds, get_grant, get_grant_and_round
from proto.common.data.services.question_bank import (
    add_template_sections_to_round,
    create_question,
    get_section_for_round,
    get_template_sections_and_questions,
)
from proto.common.data.services.round import create_round
from proto.onboard.platform.forms import ChooseTemplateSectionsForm, CreateGrantForm, CreateRoundForm, NewQuestionForm

platform_blueprint = Blueprint("platform", __name__)
grants_blueprint = Blueprint("grants", __name__)
rounds_blueprint = Blueprint("rounds", __name__)
templates_blueprint = Blueprint("templates", __name__)

# FIXME not good registering here
platform_blueprint.register_blueprint(grants_blueprint, host=Config.ONBOARD_HOST)
platform_blueprint.register_blueprint(rounds_blueprint, host=Config.ONBOARD_HOST)
platform_blueprint.register_blueprint(templates_blueprint, host=Config.ONBOARD_HOST)


@grants_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="grants")


@rounds_blueprint.context_processor
def _rounds_service_nav():
    return dict(active_navigation_tab="rounds")


@templates_blueprint.context_processor
def _templates_service_nav():
    return dict(active_navigation_tab="templates")


@grants_blueprint.get("/")
def index():
    grants = get_all_grants_with_rounds()
    return render_template("onboard/platform/home.html", grants=grants)


@grants_blueprint.get("/grants/<grant_code>")
def view_grant_overview(grant_code):
    grant = get_grant(grant_code)
    return render_template(
        "onboard/platform/view_grant_overview.html",
        grant=grant,
        back_link=url_for("proto_onboard.platform.grants.index"),
    )


@grants_blueprint.get("/grants/<grant_code>/rounds")
def view_grant_rounds(grant_code):
    grant = get_grant(grant_code)
    return render_template(
        "onboard/platform/view_grant_rounds.html",
        grant=grant,
        back_link=url_for("proto_onboard.platform.grants.index"),
    )


@grants_blueprint.get("/grants/<grant_code>/configuration")
def view_grant_configuration(grant_code):
    grant = get_grant(grant_code)
    return render_template(
        "onboard/platform/view_grant_configuration.html",
        grant=grant,
        back_link=url_for("proto_onboard.platform.grants.index"),
    )


@grants_blueprint.route("/create-grant", methods=["GET", "POST"])
def create_grant_view():
    form = CreateGrantForm()
    if form.validate_on_submit():
        try:
            grant = create_grant(**{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}})
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(url_for("proto_onboard.platform.grants.view_grant_overview", grant_code=grant.short_name))

    return render_template(
        "onboard/platform/create_grant.html", form=form, back_link=url_for("proto_onboard.platform.grants.index")
    )


@rounds_blueprint.route("/grants/<grant_code>/create-round", methods=["GET", "POST"])
def create_round_view(grant_code):
    grant = get_grant(grant_code)
    form = CreateRoundForm()
    if form.validate_on_submit():
        try:
            round = create_round(
                fund_id=grant.id,
                **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
                proto_start_date=datetime.date(2025, 1, 1),
                proto_end_date=datetime.date(2025, 1, 31),
            )
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(
                url_for(
                    "proto_onboard.platform.rounds.view_round",
                    grant_code=grant_code,
                    round_code=round.short_name,
                )
            )

    return render_template(
        "onboard/platform/create_round.html",
        form=form,
        back_link=url_for("proto_onboard.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>")
def view_round(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    return render_template(
        "onboard/platform/view_round.html",
        grant=grant,
        round=round,
        back_link=url_for("proto_onboard.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/choose-from-question-bank", methods=["GET", "POST"])
def choose_from_question_bank(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    template_sections = get_template_sections_and_questions()
    form = ChooseTemplateSectionsForm(template_sections)

    if form.validate_on_submit():
        add_template_sections_to_round(round.id, form.sections.data)
        return redirect(
            url_for("proto_onboard.platform.rounds.view_round", grant_code=grant_code, round_code=round_code)
        )

    return render_template("onboard/platform/choose_from_question_bank.html", grant=grant, round=round, form=form)


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/create-question", methods=["GET", "POST"]
)
def create_question_view(grant_code, round_code, section_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_round(round, section_id)
    form = NewQuestionForm(data={"order": max(q.order for q in section.questions) + 1})

    if form.validate_on_submit():
        create_question(
            section_id=section.id, **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}}
        )
        return redirect(
            url_for("proto_onboard.platform.rounds.view_round", grant_code=grant_code, round_code=round_code)
        )
    return render_template(
        "onboard/platform/create_question.html", grant=grant, round=round, section=section, form=form
    )


# @rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/questions/<question_id>", methods=["GET", "POST"])
# def edit_application_round_question(grant_code, round_code, question_id):
#     question = get_application_question(grant_code, round_code, question_id)
#     return render_template()
