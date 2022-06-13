import connexion
from config.env import env
from connexion.resolver import MethodViewResolver
from flask import Flask
from openapi.utils import get_bundled_specs


def create_app(testing=False) -> Flask:
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")

    flask_app = connexion_app.app

    if testing:
        flask_app.config.from_object(
            "config.environments.unit_testing.UnitTestingConfig"
        )
    else:
        flask_app.config.from_object("config.Config")

    options = {
        "swagger_url": "/",
    }
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        options=options,
        resolver=MethodViewResolver("api"),
    )

    # This is needed to access the running app's environment config
    # outside the request context using env.config.get("VARIABLE_NAME")
    env.init_app(flask_app)

    from db import db, migrate

    db.init_app(flask_app)
    migrate.init_app(flask_app, db, directory="db/migrations")

    return flask_app


app = create_app()
