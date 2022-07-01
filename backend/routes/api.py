from flask import Blueprint
from backend.models import user

print(__name__)
api = Blueprint('api', __name__)
user_bp = UserBp("users", __name__)
api.register_blueprint(user_bp, url_prefix='/users')