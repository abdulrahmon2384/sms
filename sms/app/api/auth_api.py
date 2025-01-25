from flask import Blueprint, jsonify, request, session, abort
from flask_login import login_required
from .. import db, app, GOOGLE_API_KEY
from sqlalchemy import text
from ..libraries.backend_functions import *
import requests


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"



# Create a Blueprint with the proper URL prefix
auth_api_bp = Blueprint("auth_api", __name__)




# Fetch choosen school 
@auth_api_bp.route('/fetch_school', methods=['GET'])
def select_school():
     data = request.get_json()
     schoolID = data.get("schoolID")
     
     if not schoolID:
          return jsonify({"error": "School name is required"})
     
     session["schoolID"] = schoolID
     return jsonify({"message": "School ID found"})


@auth_api_bp.route('/register_school', methods=['POST', 'GET'])
def register_school():
    """Register a new school and create its schema."""
    
    # Handle query parameter or JSON input
    school_name = request.args.get("school_name")  # Query parameter from URL
    if not school_name and request.method == "POST":
        data = request.get_json()  # JSON payload
        school_name = data.get("school_name")
    
    if not school_name:
        return jsonify({"error": "School name is required"}), 400

    # Generate schema name
    temp_name = school_name.lower().replace(' ', '_')
    schoolID = generate_schoolID()
    schema_name = temp_name + "_" + schoolID

    try:
        # Create schema for the new school
        create_school_schema(schema_name, db, text)
        create_school_dataset(schema_name, db, text)

        return jsonify({"message": "School registered successfully", 
                        "school_id": schoolID, 
                        "school_name": school_name,
                        "schema": schema_name}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to register school: {str(e)}"}), 500



# Flask route to upload an image
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get the image file from the request
    if 'image' not in request.files:
        return jsonify({"error": "No image file part"}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Upload the image to Backblaze B2
        image_data = image.read()  # Read image data
        image_name = image.filename  # Use the original file name
        image_url = upload_image_to_b2(image_data, image_name)  # Upload to B2

        # Return the public URL of the uploaded image
        return jsonify({"message": "Image uploaded successfully", "image_url": image_url}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500


@app.route('/api/schools', methods=['GET'])
def get_school():
    schoolID = request.args.get("schoolID")

    if request.args.get("insession"):
        schoolID = session.get("schoolID")
    else:
        isValid_school = check_and_set_search_path(schoolID)
        if not isValid_school:
            abort(404, description="School not found")  # Return a 404 if school is not found
    
    # Load a temp dataset to the database ,This is just for testing
    # from .. import gsd

    schoolInfo = get_school_information().get("SchoolInfo")
    if schoolInfo:
        return jsonify(schoolInfo)
    
    abort(404, description="School not found")


@app.route('/api/submit-login-credentials', methods=['POST'])
def login():
    data = request.get_json()

    # Extract user inputs
    user_id = data.get('userId')
    password = data.get('password')
    role = data.get('role')

    if not user_id and not role and not password:
        return jsonify({"success": False, "message": "Invalid Credential"}), 401

    # Check if the user exists
    return authenticate_user(user_id, password, role)


@app.route('/api/current_user_role', methods=['POST'])
def user_role():
    role = session.get("role")
    return jsonify({"success": True if role else False, "role": role})




@app.route('/api/intelleva_ai/save_chat', methods=['POST'])
def save_chat():
    role = session.get("role")
    username = session.get("user_id")

    if not role or not username:
        return jsonify({"error": "Unauthorized access"}), 401

    user = {
        "student": Students.query.filter_by(username=username).first(),
        "teacher": Teachers.query.filter_by(username=username).first(),
        "admin": Admin.query.filter_by(username=username).first()
    }.get(role)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_message = request.json.get("user_message")
    ai_message = request.json.get("ai_message")

    # if not user_message or not ai_message:
    #    return jsonify({"error": "Both user_message and ai_message are required"}), 400

    user.unique_payment_account = user.unique_payment_account or {}
    user.unique_payment_account.setdefault("chatai", [])

    user.unique_payment_account["chatai"].extend([
        {"type": "user", "message": user_message},
        {"type": "ai", "message": ai_message}
    ])

    db.session.flush() 
    db.session.commit()

    print(user.unique_payment_account.get("chatai"))
    return jsonify({"success": True, "message": "Chat saved successfully"}), 200





@app.route('/api/intelleva_ai/load_history', methods=['GET'])
def get_chat():
    role = session.get("role")
    username = session.get("user_id")

    if not role or not username:
        return jsonify({"error": "Unauthorized access"}), 401

    user = {
        "student": Students.query.filter_by(username=username).first(),
        "teacher": Teachers.query.filter_by(username=username).first(),
        "admin": Admin.query.filter_by(username=username).first()
    }.get(role)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.unique_payment_account = user.unique_payment_account or {}
    chat_history = user.unique_payment_account.get("chatai", [])
    return jsonify(chat_history), 200

@app.route("/api/intelleva_ai/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "User input is required"}), 400
        
        prompt = create_personalized_prompt(user_input)

        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.8, "topK": 1, "topP": 1}
        }

        headers = {"Content-Type": "application/json", "x-goog-api-key": GOOGLE_API_KEY}
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        response_json = response.json()
        bot_response = (
            response_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No response available")
        )

        return jsonify({"response": bot_response})

    except requests.Timeout:
        return jsonify({"error": "AI service timeout, please try again later."}), 504

    except requests.RequestException as e:
        return jsonify({"error": f"AI service error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@app.route('/api/intelleva_ai/clear_history', methods=['POST'])
def clear_chat():
    role = session.get("role")
    username = session.get("user_id")

    if not role or not username:
        return jsonify({"error": "Unauthorized access"}), 401

    user = {
        "student": Students.query.filter_by(username=username).first(),
        "teacher": Teachers.query.filter_by(username=username).first(),
        "admin": Admin.query.filter_by(username=username).first()
    }.get(role)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Initialize unique_payment_account if missing
    user.unique_payment_account = user.unique_payment_account or {}

    # Clear the chat history
    user.unique_payment_account["chatai"] = []
    db.session.commit()

    return jsonify({"message": "Chat history cleared successfully"}), 200


