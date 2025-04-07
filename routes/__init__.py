from flask import Blueprint
from flask_jwt_extended import jwt_required
from routes import user_routes, post_routes, comment_routes, like_routes

bp = Blueprint('main', __name__)

bp.register_blueprint(user_routes.bp)
bp.register_blueprint(post_routes.bp)
bp.register_blueprint(like_routes.bp)
bp.register_blueprint(comment_routes.bp)
