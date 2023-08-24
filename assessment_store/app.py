import connexion
from connexion.resolver import MethodViewResolver
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from openapi.utils import get_bundled_specs


def create_app() -> Flask:
    init_sentry()
    connexion_options = {
        "swagger_url": "/",
    }
    connexion_app = connexion.FlaskApp(
        __name__, specification_dir="openapi/", options=connexion_options
    )
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodViewResolver("api"),
    )

    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)

    from db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)
    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(
        flask_app,
        db,
        directory="db/migrations",
        render_as_batch=True,
        compare_type=True,
        compare_server_default=True,
    )

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))

    # Configurations for Flask-Apscheduler
    from flask_apscheduler import APScheduler

    scheduler = APScheduler()

    flask_app.config["SCHEDULER_API_ENABLED"] = True
    flask_app.config["JOBS"] = [
        {
            "id": "sqs_process_queues",
            "func": "_helpers.import_application:import_applications_from_queue",
            "trigger": "interval",
            "seconds": flask_app.config[
                "SQS_RECEIVE_MESSAGE_CYCLE_TIME"
            ],  # Run the job every 'x' seconds
        }
    ]
    scheduler.init_app(flask_app)
    scheduler.start()

    return flask_app


app = create_app()
