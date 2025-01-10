from flask import render_template

from common.blueprints import Blueprint
from config import Config

admin_blueprint = Blueprint("admin", __name__)
grants_blueprint = Blueprint("grants", __name__)
admin_blueprint.register_blueprint(grants_blueprint, host=Config.ONBOARD_HOST)


@admin_blueprint.context_processor
def _home_service_nav_context():
    return dict(active_item_identifier="home")


@grants_blueprint.context_processor
def _grants_service_nav_context():
    return dict(active_item_identifier="grants")


@admin_blueprint.get("/")
def index():
    return render_template("onboard/admin/index.jinja.html")


@grants_blueprint.get("/grants/new")
def create_grant():
    return render_template("onboard/admin/create_grant.jinja.html")
