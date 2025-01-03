from flask import render_template

from common.blueprints import Blueprint

grant_blueprint = Blueprint("grant_blueprint", __name__)


@grant_blueprint.get("/grant/<short_code>")
def grant_detail_handler(short_code):
    return render_template("grant/grant_detail.jinja.html")
