from flask import render_template

from common.blueprints import Blueprint

web_blueprint = Blueprint("web", __name__)


@web_blueprint.get("/cookies")
def cookies_handler():
    return render_template("apply/web/cookies.jinja.html")


@web_blueprint.get("/accessibility")
def accessibility_statement_handler():
    return render_template("apply/web/accessibility.jinja.html")
