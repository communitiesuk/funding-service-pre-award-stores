from flask import current_app, g, redirect, render_template
from flask_wtf.csrf import CSRFError
from fsd_utils.authentication.decorators import login_requested

from apply.default.account_routes import account_bp
from apply.default.application_routes import application_bp
from apply.default.content_routes import content_bp
from apply.default.routes import default_bp


def not_found(error):
    return render_template("apply/404.html", is_error=True), 404


def internal_server_error(error):
    current_app.logger.exception("Encountered 500: {error}", extra=dict(error=str(error)))
    return render_template("apply/500.html", is_error=True), 500

def unauthorised_error(error):
    return render_template("apply/500.html", is_error=True), 401


@login_requested
def csrf_token_expiry(error):
    if not g.account_id:
        return redirect(g.logout_url)
    current_app.logger.exception("Encountered 500: {error}", extra=dict(error=str(error)))
    return render_template("apply/500.html", is_error=True), 500


def register_error_handlers():
    application_bp.register_error_handler(404, not_found)
    content_bp.register_error_handler(404, not_found)
    default_bp.register_error_handler(404, not_found)
    account_bp.register_error_handler(404, not_found)

    application_bp.register_error_handler(500, internal_server_error)
    content_bp.register_error_handler(500, internal_server_error)
    default_bp.register_error_handler(500, internal_server_error)
    account_bp.register_error_handler(500, internal_server_error)
    default_bp.register_error_handler(Exception, internal_server_error)
    account_bp.register_error_handler(Exception, internal_server_error)
    application_bp.register_error_handler(Exception, internal_server_error)
    content_bp.register_error_handler(Exception, internal_server_error)


    default_bp.register_error_handler(401, unauthorised_error)
    application_bp.register_error_handler(401, unauthorised_error)
    content_bp.register_error_handler(401, unauthorised_error)
    account_bp.register_error_handler(401, unauthorised_error)

    default_bp.register_error_handler(CSRFError, csrf_token_expiry)
    application_bp.register_error_handler(CSRFError, csrf_token_expiry)
    content_bp.register_error_handler(CSRFError, csrf_token_expiry)
    account_bp.register_error_handler(CSRFError, csrf_token_expiry)
