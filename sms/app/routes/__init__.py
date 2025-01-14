from flask import Blueprint

routes_bp = Blueprint("routes", __name__ )


from .student_routes import student_bp
from .teacher_routes import teacher_bp
from .admin_routes import admin_bp
from .auth_routes import auth_bp

routes_bp.register_blueprint(auth_bp)
routes_bp.register_blueprint(student_bp)
routes_bp.register_blueprint(teacher_bp)
routes_bp.register_blueprint(admin_bp)




