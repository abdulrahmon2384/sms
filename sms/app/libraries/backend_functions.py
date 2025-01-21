import random
import string
import time
import hashlib

from flask import redirect, url_for, session, jsonify
from flask_login import login_user
from .. import db, bcrypt, bucket, B2_BUCKET_URL
from sqlalchemy import text
from ..models import *


# authenticate and login user
def authenticate_user(username, password, role):
    """
    Authenticate a user based on their role (Student, Teacher, Admin).
    
    :param username: Username provided by the user
    :param password: Password provided by the user
    :param role: Role of the user ('student', 'teacher', 'admin')
    :return: Flask response object (JSON with success/failure message)
    """
    user = None

    # Query the appropriate table based on role
    if role == "student":
        user = Students.query.filter_by(username=username).first()
    elif role == "teacher":
        user = Teachers.query.filter_by(username=username).first()
    else :
        user = Admin.query.filter_by(username=username).first()
  
    # Check if user exists and validate the password
    if user :
        if bcrypt.check_password_hash(user.key, password):
            login_user(user)  # Log the user in
            session["role"] = role
            session["login"] = True
            return jsonify({
                    "success": True,
                    "message": "Login successful.",
                    "role": role
                }), 200
        else:
            return jsonify({
                  "success": False, 
                  "message": "Password Incorrect"}), 401

    else:
        return jsonify({
                  "success": False, 
                  "message": "Invalid UserID"}), 401


# get current school information
def get_school_information() -> dict:
    try:
        school = School_information.query.first()
        if school.id:

            classes = school.school_classes.get("classes")
            grades = [classes[0] + " - " + classes[-1] if classes else "Unknown"]
            result = {"SchoolInfo":{
                        "id": str(school.id),
                        "name": school.school_name,
                        "location": school.school_address,  
                        "grades": grades,
                        "students": school.school_total_students,
                        "logo": school.school_logo_link,
                        "type": "Private"
                        }
                    }
            # print(type(result))
            return result
        
        else:
            return {"error": "School not found."}
    
    except Exception as e: 
        print(f"Error occurred: {e}")
        return {"error": "An error occurred while fetching the school information."}


# Check and set database path to sepecif school if found
def check_and_set_search_path(school_id):
    query = db.session.execute(
        text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schoolID LIMIT 1"),
        {"schoolID": school_id}
    ).fetchone()

    if query:
        # Set the search path if necessary
        db.session.execute(text("SET search_path TO :schoolID"), {"schoolID": school_id})
        session["schoolID"] = school_id
        
        db.session.commit()
        return True
    return False







# school models tables
def create_admin_table(schema_name, db, text):
    """Create the admin table in the school's schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.admin (
            username VARCHAR(100) PRIMARY KEY,
            firstname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            phonenumber VARCHAR(50),
            access BOOLEAN,
            key VARCHAR(200),
            role VARCHAR(50) DEFAULT 'Admin',
            image_link VARCHAR(100) DEFAULT 'https://f005.backblazeb2.com/file/School-management-system/default.png'
        );
    """))
def create_event_table(schema_name, db, text):
    """Create the events table in the school's schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.events (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
def create_announcement_table(schema_name, db, text):
    """Create the announcements table in the school's schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.announcements (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
def create_school_information_table(schema_name, db, text):
    """Create the school_information table in the school's schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.school_information (
            id SERIAL PRIMARY KEY,
            school_name VARCHAR(100) NOT NULL,
            school_address VARCHAR(100),
            school_phone VARCHAR(100),
            school_email VARCHAR(100),
            school_logo_link VARCHAR(500) DEFAULT 'https://f005.backblazeb2.com/file/School-management-system/images-1.jpeg',
            school_other_website VARCHAR(100),
            school_total_students INT DEFAULT 0,
            school_total_teachers INT DEFAULT 0,
            school_total_admin INT DEFAULT 0,
            school_classes JSON,
            school_teachers JSON,
            school_terms JSON,
            school_result_type JSON,
            school_founded_year VARCHAR(50) NOT NULL,
            school_total_revenues JSON,
            school_total_expenses JSON,
            school_total_budget JSON,
            school_grades JSON DEFAULT '{{}}',
            school_location VARCHAR(300),
            nationality VARCHAR(200),
            zipcode VARCHAR(50)
        );
    """))
def create_class_table(schema_name, db, text):
    """Create the class table in the school's schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.classes (
            id SERIAL PRIMARY KEY,
            class_name VARCHAR(100) NOT NULL,
            class_fee INT,
            class_subjects JSON,
            class_books JSON,
            class_description TEXT,
            class_time_table JSON,
            class_lesson_fee INT,
            materials VARCHAR(200),
            class_number_of_students JSON,
            teacher_username VARCHAR(100),
            FOREIGN KEY (teacher_username) REFERENCES {schema_name}.teachers(username),
            students JSON,
            result JSON,
            fee JSON,
            student_history JSON,
            students_attendance JSON
        );
    """))

def create_student_table(schema_name, db, text):
    """Create the student table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.students ( 
            username VARCHAR(100) PRIMARY KEY,
            firstname VARCHAR(100) NOT NULL,
            othername VARCHAR(100),
            lastname VARCHAR(100) NOT NULL,
            address VARCHAR(300) NOT NULL,
            city VARCHAR(100),
            zipcode VARCHAR(100),
            email VARCHAR(200),
            homephone VARCHAR(100),
            dob DATE,
            gender VARCHAR(50) NOT NULL,
            placeofbirth VARCHAR(100) NOT NULL,
            nationality VARCHAR(100) NOT NULL,
            enroll_date DATE NOT NULL,
            previous_school VARCHAR(200),
            medical_information VARCHAR(200),
            parental_consent BOOLEAN DEFAULT TRUE,
            languages_spoken VARCHAR(200),
            image_link VARCHAR(200) DEFAULT 'https://f005.backblazeb2.com/file/School-management-system/default.png',
            mother_firstname VARCHAR(100),
            mother_lastname VARCHAR(100),
            mother_address VARCHAR(200),
            mother_placeofemployment VARCHAR(200),
            mother_occupation VARCHAR(200),
            mother_town VARCHAR(200),
            mother_state VARCHAR(200),
            mother_cellphonenumber VARCHAR(50),
            mother_homephonenumber VARCHAR(50),
            mother_email VARCHAR(200),
            father_firstname VARCHAR(100),
            father_lastname VARCHAR(100),
            father_address VARCHAR(200),
            father_placeofemployment VARCHAR(200),
            father_occupation VARCHAR(200),
            father_town VARCHAR(200),
            father_state VARCHAR(200),
            father_cellphonenumber VARCHAR(50),
            father_homephonenumber VARCHAR(50),
            father_email VARCHAR(200),
            left_date DATE,
            key VARCHAR(300),
            role VARCHAR(50) DEFAULT 'Student',
            access BOOLEAN DEFAULT FALSE,
            others_expenses JSON,
            unique_payment_account JSON,
            attendance_count JSON,
            years JSON,
            class_id INT,
            FOREIGN KEY (class_id) REFERENCES {schema_name}.classes(id)
        );
    """))
    
def create_student_attendance_table(schema_name, db, text):
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.student_attendance (
            attendance_id SERIAL PRIMARY KEY,
            term VARCHAR(50) NOT NULL,
            morning_attendance TIMESTAMP DEFAULT NULL,
            evening_attendance TIMESTAMP DEFAULT NULL,
            comment TEXT,
            status VARCHAR(50) DEFAULT 'absent',
            late_arrival BOOLEAN,
            student_username VARCHAR(200) NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_username) REFERENCES {schema_name}.students(username),
            FOREIGN KEY (class_id) REFERENCES {schema_name}.classes(id)
        );
    """))
def create_results_table(schema_name, db, text):
    """Create the results table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.results (
            id SERIAL PRIMARY KEY,
            result_type VARCHAR(100) NOT NULL,
            term VARCHAR(50) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            marks_obtain INTEGER NOT NULL,
            total_mark INTEGER NOT NULL,
            submission_date TIMESTAMP NOT NULL,
            comment VARCHAR(1000),
            year VARCHAR(100),
            student_username VARCHAR(200) NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_username) REFERENCES {schema_name}.students(username),
            FOREIGN KEY (class_id) REFERENCES {schema_name}.classes(id)
        );
    """))

def create_student_fee_table(schema_name, db, text):
    """Create the student fee table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.student_fee (
            transaction_id VARCHAR(300) PRIMARY KEY ,
            year VARCHAR(20) NOT NULL,
            term VARCHAR(50) NOT NULL,
            fee_amount INTEGER NOT NULL,
            payment_date TIMESTAMP NOT NULL,
            payment_method VARCHAR(100),
            payment_status VARCHAR(100),
            payment_note VARCHAR(1000),
            student_username VARCHAR(200) NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_username) REFERENCES {schema_name}.students(username),
            FOREIGN KEY (class_id) REFERENCES {schema_name}.classes(id)
        );
    """))
def create_student_history_table(schema_name, db, text):
    """Create the student history table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.student_history (
            id SERIAL PRIMARY KEY,
            academy_year VARCHAR(50) NOT NULL,
            fee_paid JSON,
            exam_result JSON,
            attendance JSON,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            promotion_status VARCHAR(50),
            behavioral_notes TEXT,
            achievements VARCHAR(1000),
            special_programs VARCHAR(1000),
            student_username VARCHAR(200) NOT NULL,
            class_id INTEGER NOT NULL,
            teacher_username VARCHAR(200),
            FOREIGN KEY (student_username) REFERENCES {schema_name}.students(username),
            FOREIGN KEY (class_id) REFERENCES {schema_name}.classes(id),
            FOREIGN KEY (teacher_username) REFERENCES {schema_name}.teachers(username)
        );
    """))
def create_teacher_table(schema_name, db, text):
    """Create the teachers table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.teachers (  
            username VARCHAR(100) PRIMARY KEY,
            firstname VARCHAR(100) NOT NULL,
            lastname VARCHAR(100) NOT NULL,
            dob DATE,
            address VARCHAR(300),
            email VARCHAR(100),
            phonenumber VARCHAR(50),
            gender VARCHAR(50),
            qualification VARCHAR(50),
            years_of_experience INTEGER,
            certifications VARCHAR(200),
            teaching_specializations VARCHAR(100),
            languages_spoken VARCHAR(100),
            emergency_contact VARCHAR(50),
            notes TEXT,
            hire_date DATE,
            left_date DATE,
            current_salary INTEGER,
            salarys JSON,
            subject_taught JSON,
            bio TEXT,
            marital_status VARCHAR(50),
            attendance_count JSON DEFAULT '{{}}',
            role VARCHAR(50) DEFAULT 'Teacher',
            key VARCHAR(200),
            access BOOLEAN DEFAULT FALSE,
            image_link VARCHAR(200) DEFAULT 'https://f005.backblazeb2.com/file/School-management-system/default.png'
        );
    """))
def create_teacher_attendance_table(schema_name, db, text):
    """Create the teacher attendance table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.teacher_attendance (
            attendance_id SERIAL PRIMARY KEY,
            term VARCHAR(100) NOT NULL,
            morning_attendance TIMESTAMP NOT NULL,
            evening_attendance TIMESTAMP,
            comment TEXT,
            status VARCHAR(50),
            late_arrival BOOLEAN,
            teacher_username VARCHAR(200) NOT NULL,
            FOREIGN KEY (teacher_username) REFERENCES {schema_name}.teachers(username)
        );
    """))
def create_teacher_history_table(schema_name, db, text):
    """Create the teacher history table in the specified schema."""
    db.session.execute(text(f"""
        CREATE TABLE {schema_name}.teacher_history (
            id SERIAL PRIMARY KEY,
            year INTEGER NOT NULL,
            salarys JSON,
            attendance JSON,
            termclass JSON,
            role VARCHAR(50),
            teacher_username VARCHAR(200) NOT NULL,
            FOREIGN KEY (teacher_username) REFERENCES {schema_name}.teachers(username)
        );
    """))


# creating schools dataset tables 
def create_school_dataset(schema_name, db, text):

    # Step 1: Independent tables (no foreign key dependencies)
    create_admin_table(schema_name, db, text)
    create_event_table(schema_name, db, text)
    create_announcement_table(schema_name, db, text)
    create_school_information_table(schema_name, db, text)
    create_teacher_table(schema_name, db, text)  # Teachers table must be created before classes
    
    # Step 2: Tables with foreign keys referencing teachers and other primary tables
    create_class_table(schema_name, db, text)  # Depends on teacher table
    create_student_table(schema_name, db, text)  # Depends on class table

    # Step 3: Dependent tables that reference students, teachers, or classes
    create_student_attendance_table(schema_name, db, text)  # Depends on student and class tables
    create_results_table(schema_name, db, text)  # Depends on student and class tables
    create_student_fee_table(schema_name, db, text)  # Depends on student and class tables
    create_student_history_table(schema_name, db, text)  # Depends on student, class, and teacher tables
    
    create_teacher_attendance_table(schema_name, db, text)  # Depends on teacher table
    create_teacher_history_table(schema_name, db, text)  # Depends on teacher table

    # Commit all changes after table creation
    db.session.commit()


# create school schema to the database ####NOT IN USE FOR NOW
def create_school_schema(schema_name, db, text):
    """Create a new schema for the school in the database."""
    try:
        # SQL statement to create a schema (namespace) for the school
        db.session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        db.session.commit()
        print("created schema successfully")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating school schema: {str(e)}")



# login and redirect users
def login_user_and_redirect(user, role, next_page):
	login_user(user, remember=True)
	if role == "head teacher":
		return redirect(url_for('routes.admin.dashboard'))
	return redirect(url_for(next_page))


# generate UUID for schools
def generate_schoolID(length=8) -> str:
    """Generate a unique short ID using timestamp and random characters."""
    # Ensure that the final ID is between 8 and 12 characters
    if length < 8 or length > 12:
        raise ValueError("ID length must be between 8 and 12 characters.")
    
    timestamp = int(time.time() * 1000)
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    combined_string = f"{timestamp}{random_part}"
    short_id = hashlib.md5(combined_string.encode()).hexdigest()[:length]
    
    return short_id


# generate UUID for student including student schoolID
def generate_unique_id(school_id, length=8) -> str:
    """Generate a unique ID for users across all schools."""
    
    # Validate length
    if length < 8 or length > 12:
        raise ValueError("ID length must be between 8 and 12 characters.")
    
    school_str = str(school_id).zfill(4)  # Use a 4-digit school ID, pad with zeros if needed
    timestamp = int(time.time() * 1000)
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    combined_string = f"{school_str}{timestamp}{random_part}"
    short_id = hashlib.md5(combined_string.encode()).hexdigest()[:length]
    
    return short_id



# Function to upload image to B2
def upload_image_to_b2(image_data, image_name):
    # Upload the image to B2
    file_info = bucket.upload_bytes(image_data, image_name)
    file_url = B2_BUCKET_URL + file_info.file_name
    return file_url




