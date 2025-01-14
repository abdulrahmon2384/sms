from flask import Blueprint, jsonify

# Create a Blueprint with the proper URL prefix
teacher_api_bp = Blueprint("teacher_api", __name__, url_prefix="/api")

@teacher_api_bp.route("/teacher", methods=["GET"])
def teacher_api():
    return jsonify({"api": {}})



