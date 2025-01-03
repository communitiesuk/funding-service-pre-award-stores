from common.blueprints import Blueprint
from config import Config
from proto.apply.grant_routes import grant_blueprint

apply_blueprint = Blueprint("proto_apply_blueprint", __name__)
apply_blueprint.register_blueprint(grant_blueprint, host=Config.APPLY_HOST)
