import connexion
import psycopg2
from connexion import FlaskApp
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from sqlalchemy_utils import Ltree

from db.models import Fund  # noqa
from db.models import Round  # noqa
from db.models import Section  # noqa
from openapi.utils import get_bundled_specs


def create_app() -> FlaskApp:

    init_sentry()
    connexion_app = connexion.App(
        "Fund Store",
    )

    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
    )
    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")
    from db import db
    from db import migrate

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
    return connexion_app


app = create_app()
application = app.app
