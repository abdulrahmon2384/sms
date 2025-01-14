from flask import Blueprint, jsonify, request, session, abort
from .. import db, app
from sqlalchemy import text
from ..libraries.backend_functions import *



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

    print(schoolID)
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

