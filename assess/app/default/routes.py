from flask import Blueprint
from flask import render_template
from app.config import ASSESSMENT_HUB_ROUTE

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return render_template("index.html", assessment_url=ASSESSMENT_HUB_ROUTE)


@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
