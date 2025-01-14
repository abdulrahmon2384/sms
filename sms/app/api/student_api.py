from flask import Blueprint, jsonify

# Create a Blueprint with the proper URL prefix
student_api_bp = Blueprint("student_api", __name__, url_prefix="/api")

@student_api_bp.route("/student", methods=["GET"])
def student_api():
    return jsonify({"api": {}})


