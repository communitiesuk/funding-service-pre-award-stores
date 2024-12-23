"""Flask Production Environment Configuration."""

from distutils.util import strtobool
from os import getenv

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class ProductionConfig(DefaultConfig):
    ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK = strtobool(getenv("ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK", "False"))
