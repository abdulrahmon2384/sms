from flask import Blueprint
from .admin_api import admin_api_bp
from .auth_api import auth_api_bp
from .student_api import student_api_bp
from .teacher_api import teacher_api_bp


api_bp = Blueprint("api", __name__)


api_bp.register_blueprint(admin_api_bp)
api_bp.register_blueprint(auth_api_bp)
api_bp.register_blueprint(student_api_bp)
api_bp.register_blueprint(teacher_api_bp)





