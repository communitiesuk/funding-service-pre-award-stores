from common.blueprints import Blueprint
from config import Config
from proto.apply.web import web_blueprint

apply_blueprint = Blueprint("proto_apply", __name__)
apply_blueprint.register_blueprint(web_blueprint, host=Config.APPLY_HOST)
