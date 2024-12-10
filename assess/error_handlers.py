from flask import current_app, render_template, request

from assess.assessments.routes import assessment_bp
from assess.flagging.routes import flagging_bp
from assess.scoring.routes import scoring_bp
from assess.shared.routes import shared_bp
from assess.tagging.routes import tagging_bp


def not_found(error):
    current_app.logger.info("Encountered 404 against url {request_path}", extra=dict(request_path=request.path))
    return render_template("assess/404.html"), 404

def forbidden(error):
    # Override the default message to match design if no custom message is provided
    error.description = (
        "You do not have permission to access this page."
        if "It is either read-protected or not readable by the server." in error.description
        else error.description
    )

    current_app.logger.info("Encountered 403: {error}", extra=dict(error=str(error)))
    return (
        render_template("assess/403.html", error_description=error.description),
        403,
    )

def error_503(error):
    return render_template("assess/maintenance.html"), 503


def internal_server_error(error):
    current_app.logger.exception("Encountered 500: {error}", extra=dict(error=str(error)))
    return render_template("assess/500.html"), 500


def register_error_handlers():
    assessment_bp.register_error_handler(503, error_503)
    flagging_bp.register_error_handler(503, error_503)
    scoring_bp.register_error_handler(503, error_503)
    shared_bp.register_error_handler(503, error_503)
    tagging_bp.register_error_handler(503, error_503)

    assessment_bp.register_error_handler(403, forbidden)
    flagging_bp.register_error_handler(403, forbidden)
    scoring_bp.register_error_handler(403, forbidden)
    shared_bp.register_error_handler(403, forbidden)
    tagging_bp.register_error_handler(403, forbidden)

    assessment_bp.register_error_handler(404, not_found)
    flagging_bp.register_error_handler(404, not_found)
    scoring_bp.register_error_handler(404, not_found)
    shared_bp.register_error_handler(404, not_found)
    tagging_bp.register_error_handler(404, not_found)

    assessment_bp.register_error_handler(500, internal_server_error)
    assessment_bp.register_error_handler(Exception, internal_server_error)
    shared_bp.register_error_handler(500, internal_server_error)
    shared_bp.register_error_handler(Exception, internal_server_error)
    flagging_bp.register_error_handler(500, internal_server_error)
    flagging_bp.register_error_handler(Exception, internal_server_error)
    tagging_bp.register_error_handler(500, internal_server_error)
    tagging_bp.register_error_handler(Exception, internal_server_error)
    scoring_bp.register_error_handler(500, internal_server_error)
    scoring_bp.register_error_handler(Exception, internal_server_error)
