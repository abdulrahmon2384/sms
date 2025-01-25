import hashlib, os, json, string, random, time
from flask import redirect, url_for, session, jsonify
from flask_login import login_user
from .. import db, bcrypt, bucket, B2_BUCKET_URL
from sqlalchemy import text
from ..models import *



# this functiom return all you need to know about intelleva
def About_Intelleva():
    try:
        intelleva_info = {
            "app_name": "Intelleva",
            "meaning": "Intelleva is a fusion of 'Intelligence' and 'Elevate,' symbolizing smart, upscale education solutions designed to raise educational standards.",
            "description": (
                "Intelleva is an advanced school management system designed to simplify administrative tasks while "
                "offering luxurious and intelligent educational solutions. It provides a comprehensive platform for managing "
                "schools efficiently, ensuring seamless communication and data management across various stakeholders."
            ),
            "key_features": [
                "Student and teacher management",
                "Attendance tracking",
                "Performance evaluation",
                "Fee management",
                "Role-based access for Administrators, Teachers, and Students",
                "Communication tools for announcements and notifications",
                "Scalable design for multiple schools with unique IDs",
                "Financial tracking for revenues, expenses, and budgets"
            ],
            "user_roles": {
                "Administrator": (
                    "Manages the entire school, including student enrollment, teacher assignments, fee tracking, and "
                    "financial reports. Administrators oversee school operations, set class fees, and communicate "
                    "important updates."
                ),
                "Teacher": (
                    "Tracks student attendance and performance, provides grades and feedback, and manages their profile "
                    "information. Teachers have access to classroom data and communication tools."
                ),
                "Student": (
                    "Views their academic performance, attendance records, fee status, and class information. Students "
                    "receive announcements and can update their profiles as needed."
                )
            },
            "technical_stack": {
                "Programming Language": "Python",
                "Framework": "Flask",
                "Database Service": "Aiven (PostgreSQL)",
                "Cloud Storage": "Backblaze",
                "Architecture": "MVC (Model-View-Controller) pattern for scalability and maintainability"
            },
            "database_structure": {
                "type": "Hybrid model with shared and individual schemas",
                "shared_schema": [
                    "Schools table with unique school_id",
                    "Users table with roles (Admin, Teacher, Student) linked to school_id",
                    "Student Grades table for academic records"
                ],
                "individual_schema": [
                    "Each school has its schema with tables for students, teachers, attendance, fees, and history"
                ]
            },
            "ui_design": {
                "navigation": "Preserves state of visited pages to prevent script re-execution and optimize performance",
                "preloading": "Scripts and styles are preloaded for faster transitions",
                "themes": "Dark and light mode themes using Tailwind CSS"
            },
            "unique_identifiers": {
                "school_id": "Each school is assigned a unique ID to differentiate between similar school names",
                "user_id": "Unique identifier assigned to each user across schools"
            },
            "assistant_integration": {
                "purpose": "AI assistant responds dynamically to user queries based on role (Admin, Teacher, Student)",
                "data_sources": [
                    "General Intelleva knowledge",
                    "School-specific dataset",
                    "User-specific dataset"
                ],
                "response_behavior": (
                    "Provides personalized responses based on user role and data. Ensures accurate and relevant responses "
                    "by cross-referencing user context before replying."
                )
            }
        }

        return intelleva_info
    except Exception as e:
        return {"error": f"Failed to fetch Intelleva data: {str(e)}"}

def get_school_data():
    school = School_information.query.first()
    if not school:
        return None

    school_data = {
        "id": school.id,
        "school_name": school.school_name,
        "school_address": school.school_address,
        "school_phone": school.school_phone,
        "school_email": school.school_email,
        "school_logo_link": school.school_logo_link,
        "school_other_website": school.school_other_website,
        "school_total_students": school.school_total_students,
        "school_total_teachers": school.school_total_teachers,
        "school_total_admin": school.school_total_admin,
        "school_classes": school.school_classes or [],
        "school_teachers": school.school_teachers or [],
        "school_terms": school.school_terms or [],
        "school_result_type": school.school_result_type or [],
        "school_founded_year": school.school_founded_year,
        "school_total_revenues": school.school_total_revenues or {},
        "school_total_expenses": school.school_total_expenses or {},
        "school_total_budget": school.school_total_budget or {},
        "school_grades": school.school_grades or {},
        "school_location": school.school_location,
        "nationality": school.nationality,
        "zipcode": school.zipcode
    }
    
    return school_data

def get_teacher_data(username):
    teacher = Teachers.query.filter_by(username=username).first()
    
    if not teacher:
        return None

    return {
        "username": teacher.username,
        "firstname": teacher.firstname,
        "lastname": teacher.lastname,
        "dob": teacher.dob.strftime("%Y-%m-%d") if teacher.dob else None,
        "address": teacher.address,
        "email": teacher.email,
        "phonenumber": teacher.phonenumber,
        "gender": teacher.gender,
        "qualification": teacher.qualification,
        "years_of_experience": teacher.years_of_experience,
        "certifications": teacher.certifications,
        "teaching_specializations": teacher.teaching_specializations,
        "languages_spoken": teacher.languages_spoken,
        "emergency_contact": teacher.emergency_contact,
        "notes": teacher.notes,
        "hire_date": teacher.hire_date.strftime("%Y-%m-%d") if teacher.hire_date else None,
        "salarys": teacher.salarys,
        "subject_taught": teacher.subject_taught,
        "bio": teacher.bio,
        "marital_status": teacher.marital_status,
        "attendance_count": teacher.attendance_count,
        "role": teacher.role,
        "image_link": teacher.image_link,
     }

def get_student_data(username):
    student = Students.query.filter_by(username=username).first()
    
    if not student:
        return None

    student_data = {
        "username": student.username,
        "full_name": f"{student.firstname} {student.othername or ''} {student.lastname}".strip(),
        "address": student.address,
        "city": student.city,
        "zipcode": student.zipcode,
        "email": student.email,
        "homephone": student.homephone,
        "dob": student.dob.strftime("%Y-%m-%d") if student.dob else None,
        "gender": student.gender,
        "enroll_date": student.enroll_date.strftime("%Y-%m-%d") if student.enroll_date else None,
        "previous_school": student.previous_school,
        "medical_information": student.medical_information,
        "parental_consent": student.parental_consent,
        "languages_spoken": student.languages_spoken,
        "image_link": student.image_link,
        "role": student.role,
        "others_expenses": student.others_expenses or {},
        "unique_payment_account": student.unique_payment_account or {},
        "attendance_count": student.attendance_count or {},
    }
    
    return student_data

def get_admin_data(username):
    admin = Admin.query.filter_by(username=username).first()

    if not admin:
        return get_teacher_data(username)

    return {
        "username": admin.username,
        "firstname": admin.firstname,
        "lastname": admin.lastname,
        "email": admin.email,
        "phonenumber": admin.phonenumber,
        "access": admin.access,
        "role": admin.role,
        "image_link": admin.image_link,
    }






# Fuction for guidiance about intelleva to the chatbot
def intellva_ai_guidance_note() -> str:
    try:
        # Fetch Intelleva application information
        intelleva_info =About_Intelleva()

        # AI guidance note
        ai_guidance_note = f"""
            You are Intelleva AI, an intelligent assistant designed to help users as an Ai . 
            Your primary role is to provide accurate information and assistance based on the 
            features and capabilities of Intelleva, You can anser user question even if it is not related to intelleva
            Intelleva is described as: {intelleva_info.get('description', 'N/A')}\n\n
            Key Features of Intelleva include:\n
            - {', '.join(intelleva_info.get('key_features', []))}\n\n
            User roles and their functionalities:\n
        """

        # Add user role details dynamically
        for role, description in intelleva_info.get("user_roles", {}).items():
            ai_guidance_note += f"- {role}: {description}\n"

        ai_guidance_note += f"""
            Intelleva meanings: {intelleva_info.get("meaning", "what you suggest it might mean")}

            Your responses should be based on the provided information about Intelleva if user asked anything about it else answer user normally
            For any questions outside of Intelleva's scope, respond accordingly.
        """

        return ai_guidance_note

    except Exception as e:
        return  "..."

def school_info_guidance_note() -> str:
    try:
        school = get_school_data()
        
        # Create AI Guidance Note
        guidance_note = "This is the current school information available:\n\n"
        guidance_note += f"""
                School ID: {school['id']}\n
                School Name: {school['school_name']}\n
                Address: {school['school_address']}\n
                Phone: {school['school_phone']}, Email: {school['school_email']}\n
                Website: {school['school_other_website']}\n
                Total Students: {school['school_total_students']},
                Teachers: {school['school_total_teachers']}, 
                Admins: {school['school_total_admin']}\n
                Founded Year: {school['school_founded_year']}, Located in {school['school_location']}\n
                Nationality: {school['nationality']}, ZIP Code: {school['zipcode']}\n
                Classes Offered: {', '.join(school['school_classes'])}\n
                Result Types: {', '.join(school['school_result_type'])}\n
                Financial Overview (2024): Revenue - ${school['school_total_revenues']['2024']}, 
                Expenses - ${school['school_total_expenses']['2024']}, Budget - ${school['school_total_budget']['2024']}\n
                Teachers List: {', '.join([teacher['name'] + ' (' + teacher['subject'] + ')' for teacher in school['school_teachers']])}\n
                ------------------------------------------------------------\n
            """
        guidance_note += """
            Ensure to use this school information accurately when responding to user queries. 
            For general queries not related to school operations, respond as per the AI's general knowledge.
        """

        return guidance_note
    except Exception as e:
        print(e)
        return ""

def user_info_guidance_note(role, username) -> str:

    if not role and not username:
        return ""

    if role == "student":
        student_info = get_student_data(username)
        guidance_note = f"""
            The following is Current user which is a student's profile information:\n\n
            Username: {student_info['username']}\n
            Full Name: {student_info['full_name']}\n
            Address: {student_info['address']}, City: {student_info['city']}, ZIP Code: {student_info['zipcode']}\n
            Email: {student_info['email']}, Home Phone: {student_info['homephone']}\n
            Date of Birth: {student_info['dob']} (Age calculation required if needed)\n
            Gender: {student_info['gender']}\n
            Enrollment Date: {student_info['enroll_date']}\n
            Previous School: {student_info['previous_school']}\n
            Medical Information: {student_info['medical_information']}\n
            Parental Consent Given: {student_info['parental_consent']}\n
            Languages Spoken: {student_info['languages_spoken']}\n
            Profile Image: {student_info['image_link']}\n
            Role: {student_info['role'].capitalize()}\n\n
            Financial Information:\n
            - Other Expense: ${student_info['others_expenses']}\n
            - Payment Account Number: {student_info['unique_payment_account']}\n
            - Bank Name: {student_info['unique_payment_account']}\n\n
            Attendance Record:\n
            - {student_info['attendance_count']}\n
            This information should be used accurately when responding to queries related to the student's profile, attendance, and financial details.
        """
        return guidance_note
    
    elif role == "teacher":
        teacher_info = get_teacher_data(username)
        guidance_note = f"""
            The following is the Current user dat which is a teacher's profile information:\n\n
            Username: {teacher_info['username']}\n
            Full Name: {teacher_info['firstname']} {teacher_info['lastname']}\n
            Date of Birth: {teacher_info['dob']} (Age calculation required if needed)\n
            Address: {teacher_info['address']}\n
            Email: {teacher_info['email']}, Phone: {teacher_info['phonenumber']}\n
            Gender: {teacher_info['gender']}\n
            Marital Status: {teacher_info['marital_status']}\n
            Emergency Contact: {teacher_info['emergency_contact']}\n
            Qualification: {teacher_info['qualification']}\n
            Years of Experience: {teacher_info['years_of_experience']} years\n
            Certifications: {teacher_info['certifications']}\n
            Teaching Specializations: {teacher_info['teaching_specializations']}\n
            Languages Spoken: {teacher_info['languages_spoken']}\n
            Notes: {teacher_info['notes']}\n
            Bio: {teacher_info['bio']}\n
            Hire Date: {teacher_info['hire_date']}\n\n
            Salary Information:\n
            Salary: ${teacher_info['salarys']}\n
            Subjects Taught:\n
            - {', '.join(teacher_info['subject_taught'])}\n\n
            Attendance Record:\n
            {teacher_info['attendance_count']}\n
            Profile Image Link: {teacher_info['image_link']}\n
            Role: {teacher_info['role'].capitalize()}\n\n
            This information should be used accurately when responding to queries related to the teacher's profile, 
            salary, attendance, and professional details.
        """
        return guidance_note
    
    else:
        admin_info = get_admin_data(username)
        guidance_note = f"""
            The following is the administrator's profile information:\n\n
            Username: {admin_info['username']}\n
            Full Name: {admin_info['firstname']} {admin_info['lastname']}\n
            Email: {admin_info['email']}\n"
            Phone Number: {admin_info['phonenumber']}\n
            Access Granted: {'Yes' if admin_info['access'] else 'No'}\n
            Role: {admin_info['role'].capitalize()}\n
            Profile Image Link: {admin_info['image_link']}\n\n
            This information should be used to provide accurate responses related to administrative tasks, 
            system access, and profile management while ensuring confidentiality and security.
        """

        return guidance_note

  



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
            session["user_id"] = username
            session["role"] = role
            session["login"] = True
            session["note"] += (user_info_guidance_note(role, username))
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
        session["note"] = intellva_ai_guidance_note()
        session["note"] += school_info_guidance_note()
        
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





# Return user data and input for chatAi
def create_personalized_prompt(user_input):
     gudiance_note = session.get("note")

     # print(usegudiance_noter_data)
     if not gudiance_note:
         return f"User: {user_input}"
     
     prompt = f"{gudiance_note}\nUser: {user_input}\n \n"
     prompt += """
        Note: You are Intelleva AI, and your purpose is to assist users with their queries based on their role and relevant data. Ensure that you understand your role in providing context-aware, role-specific responses.
        Note: Do not display the User: input. Also, treat \\n as a new line character; do not show it in your output text. Ensure that your response is always readable. """
     return prompt

