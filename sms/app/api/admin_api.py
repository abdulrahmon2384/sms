from flask import Blueprint, jsonify

# Create a Blueprint with the proper URL prefix
admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api")

@admin_api_bp.route("/testing", methods=["GET"])
def admin_api():
    return jsonify({"api": {}})
    










