from flask import Blueprint, jsonify, request, session, abort
from flask_login import current_user, login_required
from ..models.admin_model import Admin
from ..models.student_model import Student
from ..models.teacher_model import Teacher
from ..models.school_model import School
from ..models.fee_model import Fee, Payment
from .. import db
import json
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
import numpy as np

# Create a Blueprint with the proper URL prefix
admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/admin")

# Dashboard statistics
@admin_api_bp.route("/dashboard/stats", methods=["GET"])
@login_required
def dashboard_stats():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get total students count
        total_students = Student.query.count()
        
        # Get total teachers count
        total_teachers = Teacher.query.count()
        
        # Get total fees collected
        total_fees_collected = db.session.query(func.sum(Payment.amount)).scalar() or 0
        
        # Get total outstanding fees
        total_fees = db.session.query(func.sum(Fee.amount)).scalar() or 0
        total_outstanding = total_fees - total_fees_collected
        
        # Get attendance rate
        # This is a placeholder - in a real implementation, you would calculate this from attendance records
        attendance_rate = 92.5
        
        # Get recent activities
        recent_activities = [
            {"type": "enrollment", "description": "New student enrolled", "timestamp": datetime.now().isoformat()},
            {"type": "payment", "description": "Fee payment received", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()},
            {"type": "attendance", "description": "Attendance marked for all classes", "timestamp": (datetime.now() - timedelta(hours=5)).isoformat()},
            {"type": "grade", "description": "Term grades updated", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
        ]
        
        return jsonify({
            "success": True,
            "stats": {
                "total_students": total_students,
                "total_teachers": total_teachers,
                "total_fees_collected": total_fees_collected,
                "total_outstanding": total_outstanding,
                "attendance_rate": attendance_rate,
                "recent_activities": recent_activities
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch dashboard statistics: {str(e)}"}), 500

# Student management endpoints
@admin_api_bp.route("/students", methods=["GET"])
@login_required
def get_students():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        class_filter = request.args.get('class', '')
        
        # Base query
        query = Student.query
        
        # Apply filters
        if search:
            query = query.filter(
                (Student.firstname.ilike(f'%{search}%')) | 
                (Student.lastname.ilike(f'%{search}%')) |
                (Student.email.ilike(f'%{search}%')) |
                (Student.student_id.ilike(f'%{search}%'))
            )
        
        if class_filter:
            query = query.filter(Student.class_assigned == class_filter)
        
        # Execute query with pagination
        students_page = query.paginate(page=page, per_page=per_page)
        
        # Format the results
        students = []
        for student in students_page.items:
            students.append({
                "id": student.id,
                "student_id": student.student_id,
                "firstname": student.firstname,
                "lastname": student.lastname,
                "email": student.email,
                "phone": student.phone,
                "class_assigned": student.class_assigned,
                "gender": student.gender,
                "image_link": student.image_link,
                "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
                "address": student.address,
                "status": student.status
            })
        
        return jsonify({
            "success": True,
            "students": students,
            "total": students_page.total,
            "pages": students_page.pages,
            "current_page": page
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students: {str(e)}"}), 500

@admin_api_bp.route("/students", methods=["POST"])
@login_required
def add_student():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstname', 'lastname', 'email', 'class_assigned', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if email already exists
        existing_student = Student.query.filter_by(email=data['email']).first()
        if existing_student:
            return jsonify({"error": "Email already exists"}), 400
        
        # Generate student ID
        # In a real implementation, you would have a more sophisticated ID generation logic
        student_id = f"STU-{datetime.now().strftime('%Y%m%d')}-{Student.query.count() + 1:03d}"
        
        # Create new student
        new_student = Student(
            student_id=student_id,
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data.get('phone', ''),
            class_assigned=data['class_assigned'],
            gender=data['gender'],
            image_link=data.get('image_link', ''),
            date_of_birth=datetime.fromisoformat(data['date_of_birth']) if 'date_of_birth' in data else None,
            address=data.get('address', ''),
            status='active',
            password='default_password'  # In a real implementation, you would generate a secure password
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Student added successfully",
            "student_id": student_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add student: {str(e)}"}), 500

@admin_api_bp.route("/students/<int:student_id>", methods=["PUT"])
@login_required
def update_student(student_id):
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Find the student
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        # Update fields
        if 'firstname' in data:
            student.firstname = data['firstname']
        if 'lastname' in data:
            student.lastname = data['lastname']
        if 'email' in data:
            # Check if email already exists for another student
            existing_student = Student.query.filter_by(email=data['email']).first()
            if existing_student and existing_student.id != student_id:
                return jsonify({"error": "Email already exists"}), 400
            student.email = data['email']
        if 'phone' in data:
            student.phone = data['phone']
        if 'class_assigned' in data:
            student.class_assigned = data['class_assigned']
        if 'gender' in data:
            student.gender = data['gender']
        if 'image_link' in data:
            student.image_link = data['image_link']
        if 'date_of_birth' in data:
            student.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
        if 'address' in data:
            student.address = data['address']
        if 'status' in data:
            student.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Student updated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update student: {str(e)}"}), 500

@admin_api_bp.route("/students/<int:student_id>", methods=["DELETE"])
@login_required
def delete_student(student_id):
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Find the student
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        # Delete the student
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Student deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete student: {str(e)}"}), 500

# Teacher management endpoints
@admin_api_bp.route("/teachers", methods=["GET"])
@login_required
def get_teachers():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        department_filter = request.args.get('department', '')
        
        # Base query
        query = Teacher.query
        
        # Apply filters
        if search:
            query = query.filter(
                (Teacher.firstname.ilike(f'%{search}%')) | 
                (Teacher.lastname.ilike(f'%{search}%')) |
                (Teacher.email.ilike(f'%{search}%')) |
                (Teacher.teacher_id.ilike(f'%{search}%'))
            )
        
        if department_filter:
            query = query.filter(Teacher.department == department_filter)
        
        # Execute query with pagination
        teachers_page = query.paginate(page=page, per_page=per_page)
        
        # Format the results
        teachers = []
        for teacher in teachers_page.items:
            teachers.append({
                "id": teacher.id,
                "teacher_id": teacher.teacher_id,
                "firstname": teacher.firstname,
                "lastname": teacher.lastname,
                "email": teacher.email,
                "phone": teacher.phone,
                "department": teacher.department,
                "subjects": teacher.subjects,
                "gender": teacher.gender,
                "image_link": teacher.image_link,
                "date_of_birth": teacher.date_of_birth.isoformat() if teacher.date_of_birth else None,
                "address": teacher.address,
                "status": teacher.status
            })
        
        return jsonify({
            "success": True,
            "teachers": teachers,
            "total": teachers_page.total,
            "pages": teachers_page.pages,
            "current_page": page
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch teachers: {str(e)}"}), 500

@admin_api_bp.route("/teachers", methods=["POST"])
@login_required
def add_teacher():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstname', 'lastname', 'email', 'department', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if email already exists
        existing_teacher = Teacher.query.filter_by(email=data['email']).first()
        if existing_teacher:
            return jsonify({"error": "Email already exists"}), 400
        
        # Generate teacher ID
        # In a real implementation, you would have a more sophisticated ID generation logic
        teacher_id = f"TCH-{datetime.now().strftime('%Y%m%d')}-{Teacher.query.count() + 1:03d}"
        
        # Create new teacher
        new_teacher = Teacher(
            teacher_id=teacher_id,
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data.get('phone', ''),
            department=data['department'],
            subjects=data.get('subjects', ''),
            gender=data['gender'],
            image_link=data.get('image_link', ''),
            date_of_birth=datetime.fromisoformat(data['date_of_birth']) if 'date_of_birth' in data else None,
            address=data.get('address', ''),
            status='active',
            password='default_password'  # In a real implementation, you would generate a secure password
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Teacher added successfully",
            "teacher_id": teacher_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add teacher: {str(e)}"}), 500

# Fee management endpoints
@admin_api_bp.route("/fees", methods=["GET"])
@login_required
def get_fees():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        class_filter = request.args.get('class', '')
        term_filter = request.args.get('term', '')
        
        # Base query
        query = Fee.query
        
        # Apply filters
        if class_filter:
            query = query.filter(Fee.class_name == class_filter)
        
        if term_filter:
            query = query.filter(Fee.term == term_filter)
        
        # Execute query with pagination
        fees_page = query.paginate(page=page, per_page=per_page)
        
        # Format the results
        fees = []
        for fee in fees_page.items:
            fees.append({
                "id": fee.id,
                "fee_id": fee.fee_id,
                "class_name": fee.class_name,
                "term": fee.term,
                "academic_year": fee.academic_year,
                "fee_type": fee.fee_type,
                "amount": fee.amount,
                "description": fee.description,
                "due_date": fee.due_date.isoformat() if fee.due_date else None,
                "status": fee.status
            })
        
        return jsonify({
            "success": True,
            "fees": fees,
            "total": fees_page.total,
            "pages": fees_page.pages,
            "current_page": page
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch fees: {str(e)}"}), 500

@admin_api_bp.route("/fees", methods=["POST"])
@login_required
def add_fee():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['class_name', 'term', 'academic_year', 'fee_type', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Generate fee ID
        fee_id = f"FEE-{datetime.now().strftime('%Y%m%d')}-{Fee.query.count() + 1:03d}"
        
        # Create new fee
        new_fee = Fee(
            fee_id=fee_id,
            class_name=data['class_name'],
            term=data['term'],
            academic_year=data['academic_year'],
            fee_type=data['fee_type'],
            amount=data['amount'],
            description=data.get('description', ''),
            due_date=datetime.fromisoformat(data['due_date']) if 'due_date' in data else None,
            status='active'
        )
        
        db.session.add(new_fee)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Fee added successfully",
            "fee_id": fee_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add fee: {str(e)}"}), 500

# School management endpoints
@admin_api_bp.route("/school", methods=["GET"])
@login_required
def get_school_info():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get the school information
        school = School.query.first()
        
        if not school:
            return jsonify({"error": "School information not found"}), 404
        
        return jsonify({
            "success": True,
            "school": {
                "id": school.id,
                "school_id": school.school_id,
                "name": school.name,
                "address": school.address,
                "phone": school.phone,
                "email": school.email,
                "website": school.website,
                "logo": school.logo,
                "current_term": school.current_term,
                "current_academic_year": school.current_academic_year,
                "school_motto": school.school_motto,
                "established_date": school.established_date.isoformat() if school.established_date else None
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch school information: {str(e)}"}), 500

@admin_api_bp.route("/school", methods=["PUT"])
@login_required
def update_school_info():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Get the school information
        school = School.query.first()
        
        if not school:
            return jsonify({"error": "School information not found"}), 404
        
        # Update fields
        if 'name' in data:
            school.name = data['name']
        if 'address' in data:
            school.address = data['address']
        if 'phone' in data:
            school.phone = data['phone']
        if 'email' in data:
            school.email = data['email']
        if 'website' in data:
            school.website = data['website']
        if 'logo' in data:
            school.logo = data['logo']
        if 'current_term' in data:
            school.current_term = data['current_term']
        if 'current_academic_year' in data:
            school.current_academic_year = data['current_academic_year']
        if 'school_motto' in data:
            school.school_motto = data['school_motto']
        if 'established_date' in data:
            school.established_date = datetime.fromisoformat(data['established_date'])
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "School information updated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update school information: {str(e)}"}), 500

# Communication endpoints
@admin_api_bp.route("/notifications", methods=["POST"])
@login_required
def send_notification():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'message', 'recipient_type']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # In a real implementation, you would send notifications to the specified recipients
        # For now, we'll just return a success message
        
        return jsonify({
            "success": True,
            "message": "Notification sent successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send notification: {str(e)}"}), 500

# Analytics endpoints
@admin_api_bp.route("/analytics/attendance", methods=["GET"])
@login_required
def attendance_analytics():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch actual attendance data
        # For now, we'll generate some sample data
        
        # Get the last 7 days
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        # Generate random attendance rates for each day
        attendance_rates = [round(np.random.uniform(85, 98), 1) for _ in range(7)]
        
        # Generate attendance by class
        classes = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
        class_attendance = {cls: round(np.random.uniform(85, 98), 1) for cls in classes}
        
        return jsonify({
            "success": True,
            "attendance": {
                "daily": {
                    "dates": dates,
                    "rates": attendance_rates
                },
                "by_class": {
                    "classes": classes,
                    "rates": list(class_attendance.values())
                }
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch attendance analytics: {str(e)}"}), 500

@admin_api_bp.route("/analytics/performance", methods=["GET"])
@login_required
def performance_analytics():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch actual performance data
        # For now, we'll generate some sample data
        
        # Generate performance by class
        classes = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
        class_performance = {cls: round(np.random.uniform(65, 90), 1) for cls in classes}
        
        # Generate performance by subject
        subjects = ['Mathematics', 'English', 'Science', 'Social Studies', 'Art', 'Physical Education']
        subject_performance = {subj: round(np.random.uniform(65, 90), 1) for subj in subjects}
        
        # Generate grade distribution
        grades = ['A', 'B', 'C', 'D', 'F']
        grade_distribution = [int(np.random.uniform(5, 30)) for _ in range(5)]
        
        return jsonify({
            "success": True,
            "performance": {
                "by_class": {
                    "classes": classes,
                    "averages": list(class_performance.values())
                },
                "by_subject": {
                    "subjects": subjects,
                    "averages": list(subject_performance.values())
                },
                "grade_distribution": {
                    "grades": grades,
                    "counts": grade_distribution
                }
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch performance analytics: {str(e)}"}), 500

@admin_api_bp.route("/analytics/finance", methods=["GET"])
@login_required
def finance_analytics():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch actual financial data
        # For now, we'll generate some sample data
        
        # Get the last 6 months
        months = [(datetime.now() - timedelta(days=30*i)).strftime('%b %Y') for i in range(5, -1, -1)]
        
        # Generate random revenue for each month
        revenue = [round(np.random.uniform(50000, 80000), 2) for _ in range(6)]
        
        # Generate random expenses for each month
        expenses = [round(np.random.uniform(30000, 50000), 2) for _ in range(6)]
        
        # Generate revenue by category
        categories = ['Tuition', 'Books', 'Uniforms', 'Transportation', 'Extracurricular']
        category_revenue = {cat: round(np.random.uniform(10000, 30000), 2) for cat in categories}
        
        # Calculate fee collection rate
        total_fees = 500000  # Example total fees for the term
        collected_fees = 375000  # Example collected fees
        collection_rate = (collected_fees / total_fees) * 100
        
        return jsonify({
            "success": True,
            "finance": {
                "monthly": {
                    "months": months,
                    "revenue": revenue,
                    "expenses": expenses
                },
                "by_category": {
                    "categories": categories,
                    "amounts": list(category_revenue.values())
                },
                "fee_collection": {
                    "total": total_fees,
                    "collected": collected_fees,
                    "rate": collection_rate
                }
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch finance analytics: {str(e)}"}), 500

# Session-based caching implementation
@admin_api_bp.route("/cache/clear", methods=["POST"])
@login_required
def clear_cache():
    if current_user.role.lower() != "admin" and current_user.role.lower() != "head teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Clear all cached data in the session
        for key in list(session.keys()):
            if key.startswith('cache_'):
                session.pop(key)
        
        return jsonify({
            "success": True,
            "message": "Cache cleared successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear cache: {str(e)}"}), 500
