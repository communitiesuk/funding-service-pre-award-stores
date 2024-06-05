import connexion
from _helpers.task_executer_service import TaskExecutorService
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from connexion.resolver import MethodViewResolver
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from fsd_utils.sqs_scheduler.context_aware_executor import ContextAwareExecutor
from fsd_utils.sqs_scheduler.scheduler_service import scheduler_executor
from openapi.utils import get_bundled_specs


def create_app() -> Flask:
    init_sentry()
    connexion_options = {
        "swagger_url": "/",
    }
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/", options=connexion_options)
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodViewResolver("api"),
    )

    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")
    flask_app.json.sort_keys = False

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

    executor = ContextAwareExecutor(
        max_workers=Config.TASK_EXECUTOR_MAX_THREAD, thread_name_prefix="NotifTask", flask_app=flask_app
    )
    # Configure Task Executor service
    task_executor_service = TaskExecutorService(
        flask_app=flask_app,
        executor=executor,
        s3_bucket=Config.AWS_MSG_BUCKET_NAME,
        sqs_primary_url=Config.AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL,
        task_executor_max_thread=Config.TASK_EXECUTOR_MAX_THREAD,
        sqs_batch_size=Config.SQS_BATCH_SIZE,
        visibility_time=Config.SQS_VISIBILITY_TIME,
        sqs_wait_time=Config.SQS_WAIT_TIME,
        region_name=Config.AWS_REGION,
        endpoint_url_override=Config.AWS_ENDPOINT_OVERRIDE,
        aws_access_key_id=Config.AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SQS_ACCESS_KEY_ID,
    )
    # Configurations for Flask-Apscheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduler_executor,
        trigger="interval",
        seconds=flask_app.config["SQS_RECEIVE_MESSAGE_CYCLE_TIME"],  # Run the job every 'x' seconds
        kwargs={"task_executor_service": task_executor_service},
    )
    scheduler.start()

    return flask_app


app = create_app()
