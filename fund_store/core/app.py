import connexion
import prance
from flask import Flask
from typing import Any, Dict
from pathlib import Path
from utils.definitions import get_project_root

project_root_path = str(get_project_root())

def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    parser = prance.ResolvingParser(main_file, strict=False)
    parser.parse()
    return parser.specification

def create_app() -> Flask:

    options = {"swagger_url": "/"}

    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir=project_root_path + "/openapi/",
        options=options
    )

    flask_app = connexion_app.app

    connexion_app.add_api(get_bundled_specs(project_root_path + "/openapi/api.yml"), validate_responses=True)

    return flask_app