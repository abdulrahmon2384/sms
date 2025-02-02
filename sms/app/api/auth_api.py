from flask import Blueprint, jsonify, request, session, abort
from flask_login import login_required, current_user
from .. import db, app, GOOGLE_API_KEY
from sqlalchemy import text
from ..libraries.backend_functions import *
import requests, json


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



@auth_api_bp.route('/api/register_school', methods=['POST', 'GET'])
def register_school():
    """Register a new school and create its schema."""
    
    school_name = request.args.get("name")  # Query parameter from URL
    if not school_name and request.method == "POST":
        data = request.get_json()  
        school_name = data.get("name")
    
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
    insession = session.get("userInfo")
    if insession:
        user = decrypt_and_decompress(insession)
        role = user.get("role")
        image_link = user.get("image_link")
        firstname = user.get("firstname")
    else:
        role = current_user.role
        image_link = current_user.image_link
        firstname = current_user.firstname
        
    if role.lower() == "head teacher":
            role = "admin"
    return jsonify({
                    "success": True if role else False, 
                    "role": role.lower(), "image": image_link, 
                    "name": firstname
                    })




# INTELLEVA CHATBOT API'S
@app.route('/api/intelleva_ai/save_chat', methods=['POST'])
def save_chat():
    user_message = request.json.get("user_message")
    ai_message = request.json.get("ai_message")
    actual_data = current_user.others

    if isinstance(actual_data, str):  
        chat_data = json.loads(actual_data)
    else: 
        chat_data = {"chatai": []}

    if user_message and ai_message:
        chat_data["chatai"].append({"type": "user", "message": user_message})
        chat_data["chatai"].append({"type": "ai", "message": ai_message})

    current_user.others = json.dumps(chat_data)
    db.session.add(current_user)
    db.session.commit()

    # print("\nSaved chat:", chat_data.get("chatai"))
    return jsonify({"success": True, "message": "Chat saved successfully"}), 200

@app.route('/api/intelleva_ai/load_history', methods=['GET'])
def get_chat():
    actual_data = current_user.others
    chat_data = {}
    if isinstance(actual_data, str):
        chat_data = json.loads(actual_data)

    chat_history = chat_data.get("chatai", [])
    return {"success": True, "chat": chat_history}, 200


@app.route("/api/intelleva_ai/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "User input is required"}), 400
        
        prompt = create_personalized_prompt(user_input)
        return gemini_response(prompt, GEMINI_API_URL, GOOGLE_API_KEY)
        
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@app.route('/api/intelleva_ai/clear_history', methods=['POST'])
def clear_chat():
    actual_data = current_user.others
    chat_data = {}
    
    if isinstance(actual_data, str):
        chat_data = json.loads(actual_data)

    chat_data["chatai"] = []
    current_user.others = json.dumps(chat_data)
    db.session.commit()

    return jsonify({"message": "Chat history cleared successfully"}), 200

