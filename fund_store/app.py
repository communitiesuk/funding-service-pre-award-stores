import connexion
from flask import Flask
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from openapi.utils import get_bundled_specs


def create_app() -> Flask:

    connexion_options = {"swagger_url": "/"}
    connexion_app = connexion.FlaskApp(
        "Fund Store",
        specification_dir="/openapi/",
        options=connexion_options,
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

    return flask_app


app = create_app()
