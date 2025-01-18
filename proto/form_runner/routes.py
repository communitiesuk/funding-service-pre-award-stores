from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.applications import get_application

runner_blueprint = Blueprint("proto_form_runner", __name__)


@runner_blueprint.get("/application/<application_id>")
def application_tasklist(application_id):
    application = get_application(application_id)
    return render_template("form_runner/application_tasklist.html", application=application)
