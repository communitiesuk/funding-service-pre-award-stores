from common.blueprints import Blueprint
from config import Config
from proto.onboard.platform import platform_blueprint
from proto.onboard.web import web_blueprint

onboard_blueprint = Blueprint("proto_onboard", __name__)
onboard_blueprint.register_blueprint(web_blueprint, host=Config.ONBOARD_HOST)
onboard_blueprint.register_blueprint(platform_blueprint, host=Config.ONBOARD_HOST)
