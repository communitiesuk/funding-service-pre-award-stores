import connexion
from connexion import FlaskApp
from flask import jsonify
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker, FlaskRunningChecker
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

    from db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)

    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(flask_app, db, directory="db/migrations", render_as_batch=True)

    # Initialise logging
    logging.init_app(flask_app)

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))

    @flask_app.errorhandler(404)
    def not_found(error):
        return jsonify({"code": 404, "message": "Requested URL was not found on the server"}), 404

    return connexion_app


app = create_app()
application = app.app
