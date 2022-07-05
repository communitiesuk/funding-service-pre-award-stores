"""Flask Local Development Environment Configuration."""
import logging
from os import path

import redis
from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    SESSION_TYPE = (
        # Specifies how the token cache should be stored
        # in server-side session
        # "filesystem"
        "redis"
    )
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # External Services
    USE_LOCAL_DATA = True
    FUND_STORE_API_HOST = "fund_store"

    # RSA 256 KEYS
    _test_private_key_path = (
        Config.FLASK_ROOT + "/tests/keys/rsa256/private.pem"
    )
    with open(_test_private_key_path, mode="rb") as private_key_file:
        RSA256_PRIVATE_KEY = private_key_file.read()
    _test_public_key_path = Config.FLASK_ROOT + "/tests/keys/rsa256/public.pem"
    with open(_test_public_key_path, mode="rb") as public_key_file:
        RSA256_PUBLIC_KEY = public_key_file.read()

    # Redis
    REDIS_SESSIONS_URL = "redis://localhost:6379/0"
    SESSION_REDIS = redis.from_url(REDIS_SESSIONS_URL)

    # Security
    FORCE_HTTPS = False

    TALISMAN_SETTINGS = {
        "feature_policy": Config.FSD_FEATURE_POLICY,
        "permissions_policy": Config.FSD_PERMISSIONS_POLICY,
        "document_policy": Config.FSD_DOCUMENT_POLICY,
        "force_https": FORCE_HTTPS,
        "force_https_permanent": False,
        "force_file_save": False,
        "frame_options": "SAMEORIGIN",
        "frame_options_allow_from": None,
        "strict_transport_security": True,
        "strict_transport_security_preload": True,
        "strict_transport_security_max_age": Config.ONE_YEAR_IN_SECS,
        "strict_transport_security_include_subdomains": True,
        "content_security_policy": Config.SECURE_CSP,
        "content_security_policy_report_uri": None,
        "content_security_policy_report_only": False,
        "content_security_policy_nonce_in": None,
        "referrer_policy": Config.FSD_REFERRER_POLICY,
        "session_cookie_secure": True,
        "session_cookie_http_only": True,
        "session_cookie_samesite": Config.FSD_SESSION_COOKIE_SAMESITE,
        "x_content_type_options": True,
        "x_xss_protection": True,
    }

    # Database
    SQLITE_DB_NAME = "test_sqlite.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        Config.FLASK_ROOT, SQLITE_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
