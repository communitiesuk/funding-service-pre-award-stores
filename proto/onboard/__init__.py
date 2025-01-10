from common.blueprints import Blueprint
from config import Config
from proto.onboard.web import web_blueprint

onboard_blueprint = Blueprint("proto_onboard", __name__)
onboard_blueprint.register_blueprint(web_blueprint, host=Config.ONBOARD_HOST)
