"""Flask Dev Pipeline Environment Configuration."""

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class DevConfig(DefaultConfig):
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
