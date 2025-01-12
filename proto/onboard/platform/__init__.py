from flask import redirect, render_template, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.services.grants import get_all_grants_with_rounds, get_grant, get_grant_and_round
from proto.common.data.services.question_bank import add_template_sections_to_round, get_template_sections_and_questions
from proto.onboard.platform.forms import ChooseTemplateSectionsForm

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
def view_grant(grant_code):
    grant = get_grant(grant_code)
    return render_template(
        "onboard/platform/view_grant.html", grant=grant, back_link=url_for("proto_onboard.platform.grants.index")
    )


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>")
def view_round(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    return render_template(
        "onboard/platform/view_round.html",
        grant=grant,
        round=round,
        back_link=url_for("proto_onboard.platform.grants.view_grant", grant_code=grant_code),
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


# @rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/questions/<question_id>", methods=["GET", "POST"])
# def edit_application_round_question(grant_code, round_code, question_id):
#     question = get_application_question(grant_code, round_code, question_id)
#     return render_template()
