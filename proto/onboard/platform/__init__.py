from flask import render_template, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.services.grants import get_all_grants, get_grant

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
    grants = get_all_grants()
    return render_template("onboard/platform/home.html", grants=grants)


@grants_blueprint.get("/grants/<code>")
def view_grant(code):
    grant = get_grant(code)
    return render_template(
        "onboard/platform/view_grant.html", grant=grant, back_link=url_for("proto_onboard.platform.grants.index")
    )
