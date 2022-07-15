"""Flask configuration."""
from os import environ
from pathlib import Path

from fsd_utils import configclass


@configclass
class DefaultConfig:

    # ---------------
    #  Application Config
    # ---------------

    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = environ.get("FLASK_ENV")

    # ---------------
    # APIs Config: contains api hosts (set in manifest.yml)
    # ---------------

    # Account Store
    ACCOUNT_STORE_API_HOST = environ.get("ACCOUNT_STORE_API_HOST")
    ACCOUNTS_ENDPOINT = "/accounts"
    ACCOUNT_ENDPOINT = "/accounts/{account_id}"

    # Application Store
    APPLICATION_STORE_API_HOST = environ.get("APPLICATION_STORE_API_HOST")
    APPLICATIONS_ENDPOINT = "/applications"
    APPLICATION_ENDPOINT = "/applications/{account_id}"

    # Fund Store
    FUND_STORE_API_HOST = environ.get("FUND_STORE_API_HOST", "fund_score_host")
    FUNDS_ENDPOINT = "/funds"
    FUND_ENDPOINT = "/funds/{fund_id}"
    ROUND_ENDPOINT = "{host}/funds/{fund_id}/rounds/{round_id}"
    LIVE_TEST_FUND_STORE_API_HOST = (
        "https://funding-service-design-fund-store-dev"
    )
    ".london.cloudapps.digital/"

    # Round Store
    ROUND_STORE_API_HOST = environ.get("ROUND_STORE_API_HOST")
    ROUNDS_ENDPOINT = "/funds/{fund_id}/rounds"

    # Notification Service
    NOTIFICATION_SERVICE_HOST = environ.get("NOTIFICATION_SERVICE_HOST")
    SEND_ENDPOINT = "/send"
    NOTIFY_TEMPLATE_MAGIC_LINK = "MAGIC_LINK"

    # ---------------
    # Security
    # ---------------

    # Allow inline scripts for swagger docs (for Talisman Config)
    SWAGGER_CSP = {
        "script-src": ["'self'", "'unsafe-inline'"],
        "style-src": ["'self'", "'unsafe-inline'"],
    }

    # ---------------
    # Database
    # ---------------

    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
