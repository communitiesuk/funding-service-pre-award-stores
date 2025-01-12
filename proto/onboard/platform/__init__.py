from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.grants import get_all_grants

platform_blueprint = Blueprint("platform", __name__)


@platform_blueprint.get("/")
def index():
    grants = get_all_grants()
    return render_template("onboard/platform/home.html", grants=grants)
