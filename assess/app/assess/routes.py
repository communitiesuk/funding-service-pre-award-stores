from app.assess.data import get_application
from app.assess.data import get_fund
from app.assess.data import get_funds
from app.assess.data import get_round
from app.assess.data import get_rounds
from app.config import ASSESSMENT_HUB_ROUTE
from flask import abort
from flask import Blueprint
from flask import render_template

assess_bp = Blueprint(
    "assess_bp",
    __name__,
    url_prefix=ASSESSMENT_HUB_ROUTE,
    template_folder="templates",
)


@assess_bp.route("/", methods=["GET"])
def funds():

    funds = get_funds()

    return render_template("funds.html", funds=funds)


@assess_bp.route("/<fund_id>/", methods=["GET"])
def fund(fund_id: str):

    fund = get_fund(fund_id)
    if not fund:
        abort(404)

    rounds = get_rounds(fund_id)

    return render_template("fund.html", fund=fund, rounds=rounds)


@assess_bp.route("/<fund_id>/<round_id>/", methods=["GET"])
def fund_round(fund_id: str, round_id: str):

    fund = get_fund(fund_id)
    if not fund:
        abort(404)

    fund_round = get_round(fund_id=fund_id, round_id=round_id)
    if not fund_round:
        abort(404)

    return render_template("round.html", fund=fund, round=fund_round)


@assess_bp.route(
    "/<fund_id>/<round_id>/application/<application_id>", methods=["GET"]
)
def application(fund_id: str, round_id: str, application_id: str):
    fund = get_fund(fund_id)
    if not fund:
        abort(404)

    fund_round = get_round(fund_id=fund_id, round_id=round_id)
    if not fund_round:
        abort(404)

    application = get_application(fund_id=fund_id, identifier=application_id)
    if not application:
        abort(404)

    return render_template(
        "application.html",
        fund=fund,
        round=fund_round,
        application=application,
    )

@assess_bp.route("/view_application/<fund_id>/<application_id>", methods=["GET"])
def view_application(application_id, fund_id):

    application_data = get_application(fund_id=fund_id, identifier=application_id)

    return render_template("assesser_project_view.html", application_data=application_data)
