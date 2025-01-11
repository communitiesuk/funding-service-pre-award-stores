from flask import redirect, render_template, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.models.fund import ProtoGrantSchema
from proto.common.data.services.grants import create_grant
from proto.onboard.admin.forms import CreateGrantForm

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


@grants_blueprint.route("/grants/new", methods=["GET", "POST"])
def create_new_grant():
    form = CreateGrantForm()
    if form.validate_on_submit():
        try:
            create_grant(ProtoGrantSchema(**form.data))
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(url_for("proto_onboard.admin.index"))

    return render_template("onboard/admin/create_grant.jinja.html", form=form)
