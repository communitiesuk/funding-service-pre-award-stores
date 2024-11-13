import connexion
from connexion import FlaskApp
from flask import jsonify
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging

from openapi.utils import get_bundled_specs


def create_app() -> FlaskApp:
    init_sentry()
    connexion_app = connexion.App(
        __name__,
    )

    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
    )

    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    @flask_app.errorhandler(404)
    def not_found(error):
        flask_app.logger.warning("requested URL was not found on the server")
        return jsonify({"code": 404, "message": "Requested URL was not found on the server"}), 404

    return connexion_app


app = create_app()
application = app.app
