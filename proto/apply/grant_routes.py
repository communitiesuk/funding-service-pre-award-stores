from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.grants import get_grant

grant_blueprint = Blueprint("grant_blueprint", __name__)


@grant_blueprint.get("/grant/<short_code>")
def grant_detail_handler(short_code):
    grants = get_grant()
    return render_template("grant/grant_detail.jinja.html")
