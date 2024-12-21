from os import getenv

import psycopg2
from flask import Flask, jsonify
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker, FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from fsd_utils.services.aws_extended_client import SQSExtendedClient
from sqlalchemy_utils import Ltree

from account_store.core.account import account_core_bp
from application_store.api.routes.application.routes import application_store_bp
from application_store.db.exceptions.application import ApplicationError
from config import Config
from fund_store.api.routes import fund_store_bp


def create_app() -> Flask:
    init_sentry()

    flask_app = Flask(__name__)

    flask_app.register_blueprint(account_core_bp, url_prefix="/account")
    flask_app.register_blueprint(fund_store_bp, url_prefix="/fund")
    flask_app.register_blueprint(application_store_bp, url_prefix="/application")

    # connexion_app.add_api(
    #     get_bundled_specs("/fund_store/openapi/api.yml"),
    #     validate_responses=True,
    #     base_path="/fund",
    # )
    #
    # connexion_app.add_api(
    #     get_bundled_specs("/application_store/openapi/api.yml"),
    #     validate_responses=True,
    #     resolver_error=501,
    #     base_path="/application",
    #     resolver=MethodResolver("api"),
    # )
    #
    # connexion_app.add_api(
    #     get_bundled_specs("/assessment_store/openapi/api.yml"),
    #     validate_responses=True,
    #     base_path="/assessment",
    #     resolver=MethodViewResolver("api"),
    # )
    #
    # connexion_app.add_api(
    #     get_bundled_specs("/account_store/openapi/api.yml"),
    #     validate_responses=False,
    #     base_path="/account",
    #     resolver=MethodResolver("api"),
    # )

    flask_app.config.from_object("config.Config")

    # Initialize sqs extended client
    create_sqs_extended_client(flask_app)

    from db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)

    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(flask_app, db, directory="db/migrations", render_as_batch=True)

    # Enable mapping of ltree datatype for sections
    psycopg2.extensions.register_adapter(Ltree, lambda ltree: psycopg2.extensions.QuotedString(str(ltree)))

    # Initialise logging
    logging.init_app(flask_app)

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))

    @flask_app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"code": 404, "message": str(error) or "Requested URL was not found on the server"}),
            404,
        )

    @flask_app.errorhandler(ApplicationError)
    def handle_application_error(error):
        response = jsonify({"detail": str(error)})
        response.status_code = 500
        return response

    return flask_app


def create_sqs_extended_client(flask_app):
    if (
        getenv("AWS_ACCESS_KEY_ID", "Access Key Not Available") == "Access Key Not Available"
        and getenv("AWS_SECRET_ACCESS_KEY", "Secret Key Not Available") == "Secret Key Not Available"
    ):
        flask_app.extensions["sqs_extended_client"] = SQSExtendedClient(
            region_name=Config.AWS_REGION,
            endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
            large_payload_support=Config.AWS_MSG_BUCKET_NAME,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=flask_app.logger,
        )
    else:
        flask_app.extensions["sqs_extended_client"] = SQSExtendedClient(
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION,
            endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
            large_payload_support=Config.AWS_MSG_BUCKET_NAME,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=flask_app.logger,
        )
